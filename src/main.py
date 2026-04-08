"""
main.py — Orchestrates the full daily podcast pipeline.

Steps:
  1. Scrape local news sites
  2. Generate podcast script via Claude
  3. Generate MP3 via OpenAI TTS
  4. Upload MP3 to GitHub Release (done by the workflow, not here)
  5. Update RSS feed
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Allow running from repo root or src/
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from config import SITES, PODCAST_BASE_URL
from scraper import scrape_all_sites
from script_generator import generate_podcast_script
from audio_generator import generate_audio
from rss_updater import update_rss_feed

from dotenv import load_dotenv
load_dotenv()


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n🎙️  Local Podcast Generator — {date_str}\n")

    # 1. Scrape
    print("📰 Step 1: Scraping sites...")
    articles = scrape_all_sites(SITES)

    if not articles:
        print("\n❌ No articles found. Check your selectors in config.py. Exiting.")
        sys.exit(1)

    print(f"\n   Total articles collected: {len(articles)}\n")

    # 2. Generate script
    print("✍️  Step 2: Generating podcast script with Claude...")
    script = generate_podcast_script(articles, date_str)

    # Save script for debugging
    script_path = Path("output") / f"script_{date_str}.txt"
    script_path.parent.mkdir(exist_ok=True)
    script_path.write_text(script)
    print(f"   Script saved to {script_path}\n")

    # 3. Generate audio
    print("🔊 Step 3: Generating audio with OpenAI TTS...")
    audio_filename = f"podcast_{date_str}.mp3"
    audio_path = generate_audio(script, audio_filename)
    print()

    # 4. Build the URL where this MP3 will live (GitHub Release asset URL)
    # The workflow uploads the file to a GitHub Release tagged with the date.
    # GitHub Release asset URLs follow this pattern:
    repo = os.environ.get("GITHUB_REPOSITORY", "YOUR_USERNAME/YOUR_REPO")
    mp3_url = (
        f"https://github.com/{repo}/releases/download/{date_str}/{audio_filename}"
    )

    # 5. Update RSS feed
    print("📡 Step 4: Updating RSS feed...")
    update_rss_feed(
        date_str=date_str,
        mp3_url=mp3_url,
        mp3_path=audio_path,
        script=script,
    )

    print("\n✅ Pipeline complete!")
    print(f"   🎵 Audio:    output/{audio_filename}")
    print(f"   📋 Script:   output/script_{date_str}.txt")
    print(f"   📡 RSS feed: feed/feed.xml")
    print(f"\n   Subscribe to your podcast at:")
    print(f"   {PODCAST_BASE_URL}/feed/feed.xml\n")


if __name__ == "__main__":
    main()
