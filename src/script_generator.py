"""
script_generator.py — Uses Claude to turn scraped articles into a podcast script.
"""

import anthropic
from scraper import Article
from config import TARGET_DURATION_MINUTES, PODCAST_TITLE


def build_articles_text(articles: list[Article]) -> str:
    """Format articles into a clean block of text for the prompt."""
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(f"[{i}] SOURCE: {a.site_name}")
        lines.append(f"    HEADLINE: {a.headline}")
        if a.body:
            lines.append(f"    SUMMARY: {a.body}")
        lines.append("")
    return "\n".join(lines)


def generate_podcast_script(articles: list[Article], date_str: str) -> str:
    """Call Claude API to generate a natural-sounding podcast script."""

    articles_text = build_articles_text(articles)
    word_target = TARGET_DURATION_MINUTES * 130  # ~130 words per minute for spoken word

    prompt = f"""You are a friendly, engaging local radio presenter hosting a daily news podcast called "{PODCAST_TITLE}".

Today's date is {date_str}.

Below are the articles scraped from local news websites today:

---
{articles_text}
---

Write a podcast script of approximately {word_target} words that:
1. Opens with a warm, natural greeting and today's date
2. Groups related stories together naturally
3. Uses conversational language — this is spoken word, not an article
4. Avoids reading out URLs or source names awkwardly
5. Transitions smoothly between stories using phrases like "Meanwhile...", "In other news...", "Closer to home..."
6. Ends with a friendly sign-off

Write ONLY the script itself — no stage directions, no headings, no markdown. Just the words to be spoken."""

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    script = message.content[0].text
    print(f"  ✅ Script generated ({len(script.split())} words)")
    return script
