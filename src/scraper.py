"""
scraper.py — Fetches and parses articles from local news websites.
"""

import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
import sys

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
    name = site["name"]

    try:
        response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        response.raise_for_status()
        print(f"Status: {response.status_code}")
    except httpx.HTTPError as e:
        print(f"  ⚠️  Could not fetch {name}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    containers = soup.select(site["article_selector"])

    print(f"Number of articles: {len(containers)}")

    if not containers:
        print(f"  ⚠️  No elements matched selector '{site['article_selector']}' on {name}")
        return []

    for container in containers[: site.get("max_articles", 10)]:
        # Extract headline
        headline_el = container.select_one(site["headline_selector"])
        headline = headline_el.get_text(strip=True) if headline_el else ""

        # Extract body text (concatenate all matching paragraphs)
        body_els = container.select(site["body_selector"])
        body = " ".join(el.get_text(strip=True) for el in body_els)

        # Try to find a link
        link_el = container.find("a", href=True)
        article_url = ""
        if link_el:
            href = link_el["href"]
            article_url = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")

        # Skip if no useful content
        if not headline and not body:
            continue

        articles.append(
            Article(
                site_name=name,
                headline=headline or "(No headline)",
                body=body[:800],  # Cap body length to keep tokens manageable
                url=article_url,
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
