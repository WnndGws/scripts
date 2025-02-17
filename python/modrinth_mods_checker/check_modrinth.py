#!/usr/bin/env python3

from pathlib import Path
from typing import List

import httpx
import orjson
import polars as pl
import regex as re

VERSIONS_OF_INTEREST = [
    "1.21.0",
    "1.21.1",
    "1.21.2",
    "1.21.3",
    "1.21.4",
]


def pivot_versions(df: pl.DataFrame) -> pl.DataFrame:
    # Group by mod_name and loader, gathering all game_versions into one list
    grouped = (
        df.group_by(["mod_name", "loader"])
        .agg(pl.col("game_version"))
        .rename({"game_version": "versions_col"})
    )

    # Create a column for each version in VERSIONS_OF_INTEREST
    # Use pl.lit("Yes")/pl.lit("No") so Polars doesn't interpret them as columns
    for ver in VERSIONS_OF_INTEREST:
        grouped = grouped.with_columns(
            pl.when(pl.col("versions_col").list.contains(ver))
            .then(pl.lit("Yes"))
            .otherwise(pl.lit("-"))
            .alias(ver)
        )

    # Remove the original list column now that we've created individual columns
    return grouped.drop("versions_col")


def fetch_versions(mod_slug: str):
    url = f"https://api.modrinth.com/v2/project/{mod_slug}/version"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return orjson.loads(response.content)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return None
        raise


def filter_by_loaders(df: pl.DataFrame, loaders_to_match: List[str]) -> pl.DataFrame:
    condition = None
    for loader in loaders_to_match:
        loader_condition = pl.col("loaders").list.contains(loader)
        condition = (
            loader_condition if condition is None else (condition | loader_condition)
        )
    filtered_df = df.filter(condition)
    if filtered_df.is_empty():
        fallback_data = {}
        for col in df.columns:
            fallback_data[col] = [""] if col == "game_versions" else [None]
        return pl.DataFrame(fallback_data)
    return filtered_df


def create_mod_table(df: pl.DataFrame, mod_name: str) -> pl.DataFrame:
    exploded = df.explode("loaders").explode("game_versions")
    return (
        exploded.select(
            [
                pl.lit(mod_name).alias("mod_name"),
                pl.col("loaders").alias("loader"),
                pl.col("game_versions").alias("game_version"),
            ]
        )
        .filter(
            (pl.col("game_version") == "")
            | (
                pl.col("game_version")
                .str.extract(r"^1\.(\d+)", 1)
                .cast(pl.Int64, strict=False)
                .fill_null(0)
                >= 21
            )
        )
        .unique()
    )


def ensure_loader(
    final_df: pl.DataFrame, mod_name: str, loader_name: str
) -> pl.DataFrame:
    existing = final_df.filter(
        (pl.col("mod_name") == mod_name) & (pl.col("loader") == loader_name)
    )
    if existing.is_empty():
        row = pl.DataFrame(
            {
                "mod_name": [mod_name],
                "loader": [loader_name],
                "game_version": [None],
            }
        )
        final_df = final_df.vstack(row)
    return final_df


def main() -> pl.DataFrame:
    loaders = ["fabric", "quilt", "wynand"]
    mods = [
        "bookshelf-lib",
        "inventory-profiles-next",
    ]
    total_df = pl.DataFrame([])

    for mod_name in mods:
        data = fetch_versions(mod_name)
        if data is None:
            row = pl.DataFrame(
                {
                    "mod_name": [mod_name],
                    "loader": [None],
                    "game_version": [None],
                }
            )
            final_df = row
        else:
            df = pl.DataFrame(data)
            filtered_df = filter_by_loaders(df, loaders)
            mod_table_df = create_mod_table(filtered_df, mod_name)
            final_df = mod_table_df
            for loader in loaders:
                final_df = ensure_loader(final_df, mod_name, loader)

        total_df = total_df.vstack(final_df)

    # Now pivot to have columns "1.21.0", "1.21.1", etc., with 'Yes' or 'No'.
    final_pivot = pivot_versions(total_df)
    return final_pivot


if __name__ == "__main__":
    print(main())
