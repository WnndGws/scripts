#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

import base64
import mimetypes
import subprocess
import sys
import uuid
from pathlib import Path
from xml.dom import minidom
from xml.etree import ElementTree as ET

import arrow
import orjson
import questionary
from loguru import logger
from rich.logging import RichHandler

# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    sys.stderr,
)
logger.configure(
    handlers=[
        {
            "sink": RichHandler(
                rich_tracebacks=True, show_path=True, tracebacks_show_locals=True
            ),
            "level": "DEBUG",
        }
    ]
)


# Step 1: Generate the folder main info
def ask_user_input():
    """Gather information from the user that will be used to generate the XML."""
    title = questionary.text("What is the 'podcast' title?").ask()
    author = questionary.text("Who is the podcast author?").ask()
    link_url = questionary.text(
        "What is the source URL for the downloads (Leave BLANK if none)."
    ).ask()
    description = questionary.text("Short description of the podcast").ask()
    category = questionary.select(
        "What category is the podcast?",
        choices=["TV", "Audiobook", "Long-form", "Short-form", "Music"],
    ).ask()
    image_url = questionary.text("Cover art image URL:").ask()

    logger.debug(f"Title: {title}")
    logger.debug(f"Author: {author}")
    logger.debug(f"Link: {link_url}")
    logger.debug(f"Description: {description}")
    logger.debug(f"Category: {category}")
    logger.debug(f"Cover URL: {image_url}")

    return author, title, link_url, description, category, image_url


# Step 2: analyse media in folder
def analyse_file(file: Path, folder_name: Path):
    """Get the info needed of each file."""
    # Generate a random UUID4 and take the first 8 bytes which is 12 characters
    guid = uuid.uuid4().bytes
    guid = base64.urlsafe_b64encode(guid[:8]).decode("ascii")

    title = file.stem
    extension = file.suffix.lower()
    folder_name = folder_name
    gouws_url = f"{private_url}/{folder_name}/{guid}{extension}"
    length = str(file.stat().st_size)
    mime_type, _ = mimetypes.guess_type(str(file))
    cover_url = ""

    # Use ffprobe to get media info
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        str(file),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    media_info = orjson.loads(result.stdout)

    # Extract duration from format section
    duration = media_info["format"]["duration"]

    explicit = "yes"

    return (
        guid,
        title,
        extension,
        gouws_url,
        length,
        mime_type,
        cover_url,
        duration,
        explicit,
    )


# Step 3: Put the info into a XML
def generate_main_xml():
    """Take the user info and put it into a base XML."""
    # Register namespaces
    ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")

    # Create root elements
    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        },
    )

    channel = ET.SubElement(rss, "channel")

    now = arrow.utcnow().to("+11:00")
    build_date = now.format("ddd, DD MMM YYYY HH:mm:ss ZZ")
    pub_date = now.format("ddd, DD MMM YYYY HH:mm:ss ZZ")
    author, title, link_url, description, category, image_url = ask_user_input()

    # Channel metadata
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = link_url
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "category").text = category
    ET.SubElement(
        channel, "generator"
    ).text = "Podsync generator (support us at https://github.com/mxpv/podsync)"
    ET.SubElement(channel, "language").text = "en-au"
    ET.SubElement(channel, "lastBuildDate").text = build_date
    ET.SubElement(channel, "pubDate").text = pub_date

    # Channel image
    image = ET.SubElement(channel, "image")
    ET.SubElement(image, "url").text = image_url
    ET.SubElement(image, "title").text = title
    ET.SubElement(image, "link").text = link_url

    # iTunes channel elements
    ET.SubElement(channel, "itunes:author").text = author
    ET.SubElement(channel, "itunes:subtitle").text = title
    ET.SubElement(channel, "itunes:summary").text = f"<![CDATA[{title} ({pub_date})]]>"
    ET.SubElement(channel, "itunes:block").text = "yes"
    ET.SubElement(
        channel,
        "itunes:image",
        {"href": image_url},
    )
    ET.SubElement(channel, "itunes:explicit").text = "yes"
    ET.SubElement(channel, "itunes:category", {"text": category})

    # Add all the files in the folder
    items = []
    order_number = 1
    folder_name = questionary.text(
        "What is the main folder that contains media files called?"
    ).ask()
    for file in Path.cwd().iterdir():
        (
            guid,
            title,
            extension,
            gouws_url,
            length,
            mime_type,
            cover_url,
            duration,
            explicit,
        ) = analyse_file(file, folder_name)
        item_dict = {
            "guid": guid,
            "title": title,
            "link": gouws_url,
            "description": "",
            "pubDate": pub_date,
            "enclosure": {"url": gouws_url, "length": length, "type": mime_type},
            "itunes:author": author,
            "itunes:subtitle": title,
            "itunes:duration": duration,
            "itunes:explicit": explicit,
            "itunes:order": str(order_number),
        }
        items.append(item_dict)
        order_number += 1
        # Rename the file to its guid
        file.rename(f"{guid}{extension}")

    # Add items to channel
    for item_data in items:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "guid").text = item_data["guid"]
        ET.SubElement(item, "title").text = item_data["title"]
        ET.SubElement(item, "link").text = item_data["link"]
        ET.SubElement(item, "description").text = item_data["description"]
        ET.SubElement(item, "pubDate").text = item_data["pubDate"]

        enclosure = ET.SubElement(
            item,
            "enclosure",
            {
                "url": item_data["enclosure"]["url"],
                "length": item_data["enclosure"]["length"],
                "type": item_data["enclosure"]["type"],
            },
        )

        ET.SubElement(item, "itunes:author").text = item_data["itunes:author"]
        ET.SubElement(item, "itunes:subtitle").text = item_data["itunes:subtitle"]
        ET.SubElement(item, "itunes:duration").text = item_data["itunes:duration"]
        ET.SubElement(item, "itunes:explicit").text = item_data["itunes:explicit"]
        ET.SubElement(item, "itunes:order").text = item_data["itunes:order"]

    # Prettify and save
    rough_string = ET.tostring(rss, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = (
        reparsed.toprettyxml(indent="  ")
        .replace("&lt;![CDATA[", "<![CDATA[")
        .replace("]]&gt;", "]]>")
    )

    # Save to file
    output_path = Path("podcast.xml")
    output_path.write_text(pretty_xml, encoding="utf-8")
    print(f"XML saved to {output_path}")


# Finally, main()
def main():
    generate_main_xml()


if __name__ == "__main__":
    main()
