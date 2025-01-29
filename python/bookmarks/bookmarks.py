#!/usr/bin/env -S uv run

# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx", "regex", "arrow", "polars", "typer"]
# ///

from pathlib import Path

import arrow
import httpx
import polars as pl
import regex
import typer


def fetch_page_title(url: str) -> str:
    # Fetch the page content
    with httpx.Client() as client:
        response = client.get(url)
        html_content = response.text

    # Use regex to extract the <title>...</title>
    pattern = r"<title[^>]*>(.*?)</title>"
    match = regex.search(pattern, html_content, regex.IGNORECASE | regex.DOTALL)

    # Return the title if found, otherwise an empty string
    return match.group(1).strip() if match else ""


def main(url: str = typer.Option(..., help="URL to store")):
    page_title = fetch_page_title(url)
    file_path = Path("my_database.parquet")

    # Load existing DataFrame if the file exists, otherwise create an empty one
    if file_path.exists():
        df = pl.read_parquet(file_path)
    else:
        df = pl.DataFrame(
            schema={"url": pl.Utf8, "title": pl.Utf8, "timestamp": pl.Utf8}
        )

    # Check if URL already exists in the DataFrame
    exists = df.filter(pl.col("url") == url).height > 0

    # If it's not there, append a new row
    if not exists:
        new_row = pl.DataFrame(
            {
                "url": [url],
                "title": page_title,
                "timestamp": [arrow.now().format("YYYY-MM-DD HH:mm:ss")],
            }
        )
        df = pl.concat([df, new_row], how="vertical")
        df.write_parquet(file_path)

    print(df)


if __name__ == "__main__":
    typer.run(main)
