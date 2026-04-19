"""
scraper.py — Fetches and parses articles from local news websites.
"""

import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
import sys
import feedparser

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; LocalPodcastBot/1.0; "
        "+https://github.com/tom-wardley971/local-news-podcast)"
    )
}


@dataclass
class Article:
    site_name: str
    headline: str
    body: str
    url: str


def scrape_site(site: dict) -> list[Article]:
    """Scrape articles from a single site config."""
    articles = []
    url = site["url"]
    feed_url = url+"/feed"
    name = site["name"]

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        articles.append(
            Article(
                site_name=name,
                headline=entry.title or "(No headline)",
                body=BeautifulSoup(entry.summary, "html.parser").get_text(),  # Cap body length to keep tokens manageable
                url=entry.link or "No Link",
            )
        )

    print(f"  ✅ {name}: {len(articles)} articles scraped")
    return articles


def scrape_all_sites(sites: list[dict]) -> list[Article]:
    """Scrape all configured sites and return combined article list."""
    all_articles = []
    for site in sites:
        print(f"  🌐 Scraping: {site['name']} ...")
        all_articles.extend(scrape_site(site))
    return all_articles
