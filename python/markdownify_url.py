#!/usr/bin/env python
## Download and save a url TLD and all sub-domains

from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

import click
import httpx
import regex as re
from bs4 import BeautifulSoup
from loguru import logger
from markdownify import markdownify as md
from tenacity import retry, stop_after_attempt, wait_fixed

# Set the maximum recursion depth
MAX_DEPTH = 10

# Create a set to store visited links
visited_links = set()


def add_newline_on_case_change(s):
    # Use a regular expression to insert a newline between a lowercase and uppercase letter
    return re.sub(r"([a-z])([A-Z])", r"\1\n\2", s)


def add_newline_after_uppercase_series(s):
    # Regular expression to match a group of consecutive uppercase words longer than 2 letters
    return re.sub(r"((?:[A-Z]{3,}\s*)+)", r"\n\n\1\n", s)


def replace_dash_with_newline_bullet(s):
    # Replace all occurrences of " - " with "\n* "
    return re.sub(r" \\- ", r"\n* ", s)


# Helper function to clean URLs, remove fragments, and ensure they are internal
def is_internal_link(no_child, base_url, link):
    if not no_child:
        parsed_base = urlparse(base_url)
        parsed_link = urlparse(link)

        # Exclude intrapage links with fragments like '#section'
        if parsed_link.fragment:
            return False

        # Compare the domain of the link with the base URL domain
        return parsed_link.netloc == parsed_base.netloc or parsed_link.netloc == ""
    return False


# Retry failed requests up to 3 times, waiting 2 seconds between attempts
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_page(url):
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    return response


# Recursively follow internal links to a maximum depth
def scrape_and_convert(no_child, base_url, url, depth=0):
    if url in visited_links or depth > MAX_DEPTH:
        return ""

    visited_links.add(url)

    try:
        response = fetch_page(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that are likely sidebars, navigation bars, or footers
        for element in soup.select(
            "aside, .sidebar, .nav, .menu, footer, .widget, .breadcrumb"
        ):
            element.decompose()  # Removes the sidebar elements from the DOM

        # Extract the headings and convert them to markdown headings
        markdown_content = ""
        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            level = int(heading.name[1])  # Get the heading level (e.g., 1 for <h1>)
            markdown_content += f"{'#' * level} {heading.get_text().strip()}\n\n"

        # Convert the remaining HTML content to Markdown
        content = soup.get_text()
        markdown_content += md(content)

        # Find and follow internal links recursively
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_link = urljoin(base_url, href)
            full_link, _ = urldefrag(
                full_link
            )  # Remove the fragment identifier if present

            if (
                is_internal_link(no_child, base_url, full_link)
                and full_link not in visited_links
            ):
                logger.info(f"Found internal link: {full_link}")
                markdown_content += scrape_and_convert(base_url, full_link, depth + 1)

        markdown_content = add_newline_on_case_change(markdown_content)
        markdown_content = add_newline_after_uppercase_series(markdown_content)
        markdown_content = replace_dash_with_newline_bullet(markdown_content)
        return markdown_content

    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e!s}")
        return ""


@click.command()
@click.option(
    "--url", prompt="Enter the URL to scrape", help="The base URL for scraping."
)
@click.option(
    "--no-child",
    prompt="Flag to disable scraping sub-domains",
    is_flag=True,
    default=False,
    help="Flag to disable scraping sub-domains",
)
def main(no_child, url):
    # Ensure the base URL starts with http(s)
    if not re.match(r"https?://", url):
        logger.error("Invalid URL. Please make sure it starts with http:// or https://")
        return

    # Scrape the website and convert contents to Markdown
    markdown_content = scrape_and_convert(no_child, url, url)

    # Save the final content to a Markdown file
    output_file = Path("contents.md")
    output_file.write_text(markdown_content)

    logger.info(f"Scraping completed. Markdown content saved to {output_file}")


if __name__ == "__main__":
    main()
