import typer
from packaging.version import Version, InvalidVersion
from pathlib import Path
import questionary
import httpx
from rich.console import Console
from rich.table import Table
from rich import print_json

MOD_IDS_FILE = Path("mod_ids.txt")
API_URL_VERSIONS = "https://api.modrinth.com/v2/project/{}/version"
API_URL = "https://api.modrinth.com/v2/project/"

console = Console()


def save_mod_ids(mod_ids):
    if MOD_IDS_FILE.exists():
        existing_ids = set(MOD_IDS_FILE.read_text().splitlines())
    else:
        existing_ids = set()
    new_ids = [mid for mid in mod_ids if mid not in existing_ids]
    if new_ids:
        with MOD_IDS_FILE.open("a", encoding="utf-8") as f:
            for mid in new_ids:
                f.write(mid + "\n")


def load_mod_ids():
    if MOD_IDS_FILE.exists():
        return MOD_IDS_FILE.read_text().splitlines()
    return []


def fetch_mod_name(mod_id):
    try:
        response = httpx.get(API_URL + mod_id, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("title", "Unknown")
    except Exception:
        return "Unknown"


def fetch_mod_versions_info(mod_id):
    try:
        mod_name = fetch_mod_name(mod_id)
        response = httpx.get(API_URL_VERSIONS.format(mod_id), timeout=5)
        response.raise_for_status()
        versions = response.json()
        filtered_versions = [
            v
            for v in versions
            if any(loader in v.get("loaders", []) for loader in ("fabric", "quilt"))
        ]
        if not filtered_versions:
            return None
        # Find version with max game_versions lexicographically
        max_game_version = max(
            (max(v.get("game_versions", [])) for v in filtered_versions), default=None
        )
        # Pick the first filtered version's project_id and name (all share same project_id)
        first_version = filtered_versions[0]
        return {
            "mod_name": mod_name,
            "project_id": first_version.get("project_id"),
            "max_game_version": max_game_version,
            "name": first_version.get("name"),
            "mod_id": mod_id,
        }
    except Exception:
        return None


def main(
    filter_version: str = typer.Option(
        None, help="Only show mods with max_game_version < this version"
    ),
):
    mod_ids = []
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

    table = Table(title="Filtered Modrinth Versions")
    table.add_column("Mod ID", style="cyan", no_wrap=True)
    table.add_column("Mod Name", style="cyan", no_wrap=True)
    table.add_column("Project ID", style="magenta")
    table.add_column("Max Game Version", style="green")
    table.add_column("Version Name", style="yellow")

    filter_ver_obj = None
    if filter_version:
        try:
            filter_ver_obj = Version(filter_version)
        except InvalidVersion:
            console.print(f"[red]Invalid version filter: {filter_version}[/red]")
            return

    for mod_id in mod_ids:
        info = fetch_mod_versions_info(mod_id)
        if info:
            max_ver = info["max_game_version"]
            if max_ver is None:
                show = True
            elif filter_ver_obj:
                try:
                    max_ver_obj = Version(max_ver)
                    show = max_ver_obj < filter_ver_obj
                except InvalidVersion:
                    show = True
            else:
                show = True

            if show:
                table.add_row(
                    info["mod_id"],
                    info["project_id"],
                    max_ver or "N/A",
                    info["name"] or "N/A",
                )
        else:
            table.add_row(mod_id, "-", "-", "[red]No fabric/quilt versions[/red]")

    console.print(table)


if __name__ == "__main__":
    typer.run(main)
