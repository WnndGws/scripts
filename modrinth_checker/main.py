from pathlib import Path
from typing import List, Optional, Tuple, Union

import httpx
import orjson
import questionary
import typer
from packaging.version import InvalidVersion, Version
from rich.console import Console
from rich.table import Table

MOD_IDS_FILE = Path("mod_ids.txt")
API_URL_VERSIONS = "https://api.modrinth.com/v2/project/{}/version"
API_URL = "https://api.modrinth.com/v2/project/"

console = Console()


def save_mod_ids(mod_ids: list[str]) -> None:
    if MOD_IDS_FILE.exists():
        existing_ids = set(MOD_IDS_FILE.read_text(encoding="utf-8").splitlines())
    else:
        existing_ids = set()
    new_ids = [mid for mid in mod_ids if mid not in existing_ids]
    if new_ids:
        with MOD_IDS_FILE.open("a", encoding="utf-8") as f:
            for mid in new_ids:
                f.write(mid + "\n")


def load_mod_ids() -> list[str]:
    if MOD_IDS_FILE.exists():
        return MOD_IDS_FILE.read_text(encoding="utf-8").splitlines()
    return []


def fetch_mod_name(client: httpx.Client, mod_id: str) -> str:
    try:
        response = client.get(API_URL + mod_id, timeout=5)
        response.raise_for_status()
        data = orjson.loads(response.content)
        return data.get("title", "Unknown")
    except Exception:
        return "Unknown"


def fetch_mod_versions_info(client: httpx.Client, mod_id: str) -> dict | None:
    try:
        mod_name = fetch_mod_name(client, mod_id)
        response = client.get(API_URL_VERSIONS.format(mod_id), timeout=5)
        response.raise_for_status()
        versions = orjson.loads(response.content)
        filtered_versions = [
            v
            for v in versions
            if any(loader in v.get("loaders", []) for loader in ("fabric", "quilt"))
        ]
        if not filtered_versions:
            return None
        max_game_version = max(
            (max(v.get("game_versions", [])) for v in filtered_versions), default=None
        )
        first_version = filtered_versions[0]
        return {
            "mod_name": mod_name,
            "project_id": first_version.get("project_id"),
            "max_game_version": max_game_version,
            "name": first_version.get("name"),
            "mod_id": mod_id,
            "version_id": first_version.get("id"),
        }
    except Exception:
        return None


def export_download_links_for_version(version: str, mod_ids: list[str]) -> None:
    download_links_file = Path(f"download_links_{version}.txt")
    missing_links_file = Path(f"missing_links_{version}.txt")

    with (
        httpx.Client() as client,
        download_links_file.open("w", encoding="utf-8") as dl_f,
        missing_links_file.open("w", encoding="utf-8") as miss_f,
    ):
        for mod_id in mod_ids:
            try:
                mod_name = fetch_mod_name(client, mod_id)
                response = client.get(API_URL_VERSIONS.format(mod_id), timeout=5)
                response.raise_for_status()
                versions = orjson.loads(response.content)

                # Filter fabric/quilt versions
                fabric_quilt_versions = [
                    v
                    for v in versions
                    if any(
                        loader in v.get("loaders", []) for loader in ("fabric", "quilt")
                    )
                ]

                # Find versions matching the specified game version
                matched_versions = [
                    v
                    for v in fabric_quilt_versions
                    if version in v.get("game_versions", [])
                ]

                if not matched_versions:
                    miss_f.write(f"{mod_name} ({mod_id}) - No matching version\n")
                    continue

                # Pick the latest version by date_published
                latest_version = max(
                    matched_versions,
                    key=lambda v: v.get("date_published", ""),
                )

                files = latest_version.get("files", [])
                if not files:
                    miss_f.write(f"{mod_name} ({mod_id}) - No download link\n")
                    continue

                # Write only the first file's URL as the latest download link
                url = files[0].get("url")
                if url:
                    dl_f.write(f"{mod_name} ({mod_id}) - {url}\n")
                else:
                    miss_f.write(f"{mod_name} ({mod_id}) - No download link\n")

            except Exception as e:
                miss_f.write(f"{mod_id} - Error: {e}\n")


def main(
    no_fabric_quilt: bool = typer.Option(
        False, "--no-fabric-quilt", help="Exclude mods with fabric/quilt versions"
    ),
    max_version: str | None = typer.Option(
        None,
        "--max-version",
        help="Show only mods whose max version is lower than this",
    ),
    show_all: bool = typer.Option(
        False, "--all", help="Show all mods regardless of versions"
    ),
    export_version: str | None = typer.Option(
        None,
        "--export-version",
        help="Export download links for all mods for the specified version",
    ),
):
    mod_ids: list[str] = []
    while True:
        mod_id = questionary.text("Enter mod_id (empty to finish):").ask()
        if not mod_id:
            break
        mod_ids.append(mod_id.strip())

    if mod_ids:
        save_mod_ids(mod_ids)
    else:
        mod_ids = load_mod_ids()
        if not mod_ids:
            console.print("[red]No mod IDs saved yet.[/red]")
            return

    if export_version:
        console.print(f"Exporting download links for version: {export_version}")
        export_download_links_for_version(export_version, mod_ids)
        console.print(
            f"Done. See download_links_{export_version}.txt and missing_links_{export_version}.txt"
        )
        return

    table = Table(title="Filtered Modrinth Versions")
    table.add_column("Mod Name", style="cyan", no_wrap=True)
    table.add_column("Project ID", style="magenta")
    table.add_column("Max Game Version", style="green")
    table.add_column("Version ID", style="cyan", no_wrap=True)
    table.add_column("Version Name", style="yellow")

    max_ver_obj: Version | None = None
    if max_version:
        try:
            max_ver_obj = Version(max_version)
        except InvalidVersion:
            console.print(f"[red]Invalid max-version filter: {max_version}[/red]")
            return

    rows: list[tuple[str | Version, list[str]]] = []

    with httpx.Client() as client:
        for mod_id in mod_ids:
            info = fetch_mod_versions_info(client, mod_id)
            if info:
                max_ver = info["max_game_version"]
                if no_fabric_quilt:
                    # Skip mods that have fabric/quilt versions (info exists means they have)
                    continue
                if max_ver_obj:
                    try:
                        max_ver_parsed = Version(max_ver)
                        if max_ver_parsed >= max_ver_obj:
                            continue
                    except InvalidVersion:
                        pass
                rows.append(
                    (
                        max_ver or "",
                        [
                            info["mod_name"],
                            info["mod_id"],
                            max_ver or "N/A",
                            info["version_id"] or "N/A",
                            info["name"] or "N/A",
                        ],
                    )
                )
            # No fabric/quilt versions found
            elif no_fabric_quilt or show_all:
                rows.append(
                    (
                        "",
                        [mod_id, "-", "-", "[red]No fabric/quilt versions[/red]", ""],
                    )
                )

    def version_key(item: tuple[str | Version, list[str]]) -> Version:
        ver_str = item[0]
        try:
            return Version(ver_str)
        except (InvalidVersion, TypeError):
            return Version("0")

    rows.sort(key=version_key)

    for _, row in rows:
        table.add_row(*row)

    console.print(table)


if __name__ == "__main__":
    typer.run(main)
