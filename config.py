# ============================================================
#  LOCAL PODCAST - CONFIGURATION
#  Edit this file to set up your podcast
# ============================================================

# --- Your Podcast ---
PODCAST_TITLE = "My Local Area Daily"
PODCAST_DESCRIPTION = "A daily AI-generated summary of local news."
PODCAST_LANGUAGE = "en"

# Your GitHub Pages URL (after you enable GitHub Pages on the repo)
# Format: https://<your-github-username>.github.io/<your-repo-name>
PODCAST_BASE_URL = "https://YOUR_USERNAME.github.io/YOUR_REPO_NAME"

# --- Sites to Scrape ---
# Add as many sites as you like.
# For each site, you need to find the CSS selector that targets article/story elements.
# Tip: Right-click a headline in your browser → Inspect → find the wrapping tag.
SITES = [
    {
        "name": "Example Local News",
        "url": "https://baysidenews.com.au",
        # CSS selector for individual article/story containers
        "article_selector": "article",
        # CSS selector for the headline within each article (relative to article)
        "headline_selector": "h2, h3",
        # CSS selector for the body text (relative to article)
        "body_selector": "p",
        # Max articles to pull from this site
        "max_articles": 10,
    },
    # Add more sites here:
    # {
    #     "name": "Town Council News",
    #     "url": "https://www.mycouncil.gov.uk/news",
    #     "article_selector": ".news-item",
    #     "headline_selector": "h2",
    #     "body_selector": ".summary",
    #     "max_articles": 5,
    # },
]

# --- AI Settings ---
# Approx how long you want the podcast (in minutes). Affects script length.
TARGET_DURATION_MINUTES = 2

# Voice for OpenAI TTS: alloy, echo, fable, onyx, nova, shimmer
TTS_VOICE = "nova"

# --- Podcast Host Details (for RSS feed) ---
AUTHOR_NAME = "Local Podcast Bot"
AUTHOR_EMAIL = "podcast@example.com"
