"""
rss_updater.py — Creates/updates a podcast-compatible RSS feed (feed/feed.xml).

The feed is committed to the repo and served via GitHub Pages.
MP3s are linked to GitHub Release assets.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
from config import (
    PODCAST_TITLE,
    PODCAST_DESCRIPTION,
    PODCAST_LANGUAGE,
    PODCAST_BASE_URL,
    AUTHOR_NAME,
    AUTHOR_EMAIL,
)


FEED_PATH = Path("feed/feed.xml")
ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def _register_namespaces():
    ET.register_namespace("itunes", ITUNES_NS)
    ET.register_namespace("", "")


def _itunes(tag: str) -> str:
    return f"{{{ITUNES_NS}}}{tag}"


def load_or_create_feed() -> ET.ElementTree:
    """Load existing feed or create a fresh one."""
    _register_namespaces()

    if FEED_PATH.exists():
        return ET.parse(FEED_PATH)

    # Build a new feed from scratch
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:itunes", ITUNES_NS)

    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = PODCAST_TITLE
    ET.SubElement(channel, "description").text = PODCAST_DESCRIPTION
    ET.SubElement(channel, "language").text = PODCAST_LANGUAGE
    ET.SubElement(channel, "link").text = PODCAST_BASE_URL
    ET.SubElement(channel, _itunes("author")).text = AUTHOR_NAME
    ET.SubElement(channel, _itunes("explicit")).text = "false"

    owner = ET.SubElement(channel, _itunes("owner"))
    ET.SubElement(owner, _itunes("name")).text = AUTHOR_NAME
    ET.SubElement(owner, _itunes("email")).text = AUTHOR_EMAIL

    return ET.ElementTree(rss)


def add_episode(
    tree: ET.ElementTree,
    date_str: str,
    mp3_url: str,
    mp3_size_bytes: int,
    duration_seconds: int = 0,
    script_excerpt: str = "",
) -> ET.ElementTree:
    """Prepend a new episode item to the channel."""
    root = tree.getroot()
    channel = root.find("channel")

    item = ET.Element("item")

    title = f"{PODCAST_TITLE} — {date_str}"
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = script_excerpt[:500] or f"Your local news for {date_str}."
    ET.SubElement(item, "pubDate").text = datetime.now(timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )
    ET.SubElement(item, "guid").text = mp3_url

    enclosure = ET.SubElement(item, "enclosure")
    enclosure.set("url", mp3_url)
    enclosure.set("length", str(mp3_size_bytes))
    enclosure.set("type", "audio/mpeg")

    if duration_seconds:
        mins = duration_seconds // 60
        secs = duration_seconds % 60
        ET.SubElement(item, _itunes("duration")).text = f"{mins}:{secs:02d}"

    ET.SubElement(item, _itunes("title")).text = title
    ET.SubElement(item, _itunes("explicit")).text = "false"

    # Insert at top (after channel metadata, before existing items)
    # Find position of first existing item
    children = list(channel)
    first_item_index = next(
        (i for i, c in enumerate(children) if c.tag == "item"), len(children)
    )
    channel.insert(first_item_index, item)

    return tree


def save_feed(tree: ET.ElementTree):
    """Write the RSS feed to disk."""
    FEED_PATH.parent.mkdir(exist_ok=True)
    tree.write(FEED_PATH, encoding="unicode", xml_declaration=True)
    print(f"  ✅ RSS feed updated: {FEED_PATH}")


def update_rss_feed(
    date_str: str,
    mp3_url: str,
    mp3_path: Path,
    script: str,
):
    """Full update flow: load feed, add episode, save."""
    tree = load_or_create_feed()
    mp3_size = mp3_path.stat().st_size if mp3_path.exists() else 0
    tree = add_episode(
        tree,
        date_str=date_str,
        mp3_url=mp3_url,
        mp3_size_bytes=mp3_size,
        script_excerpt=script[:500],
    )
    save_feed(tree)
