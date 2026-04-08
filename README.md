# 🎙️ Local Podcast Generator

An automated daily podcast that scrapes your local news websites and uses AI to 
generate and narrate a summary — delivered to your phone via a podcast RSS feed.

**Stack:** Python · BeautifulSoup · Claude API · OpenAI TTS · GitHub Actions · GitHub Pages

---

## Setup (one-time, ~20 minutes)

### 1. Fork / Clone this repo
Create a new GitHub repository and push this code to it.

### 2. Configure your sites
Edit `config.py`:
- Set your `PODCAST_TITLE`, `PODCAST_BASE_URL`, etc.
- Add your local news sites to the `SITES` list

**Finding the right CSS selector:**
1. Open your local news site in Chrome/Firefox
2. Right-click a news article → **Inspect**
3. Find the HTML tag that wraps each article (e.g. `article`, `.story`, `.news-item`)
4. Use that as your `article_selector`

### 3. Add your API keys as GitHub Secrets
Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these two secrets:
- `ANTHROPIC_API_KEY` — from https://console.anthropic.com
- `OPENAI_API_KEY` — from https://platform.openai.com/api-keys

### 4. Enable GitHub Pages
Go to **Settings → Pages** and set Source to **Deploy from branch: main, folder: / (root)**.

Then update `PODCAST_BASE_URL` in `config.py` to:
```
https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME
```

### 5. Run it manually to test
Go to **Actions → Generate Daily Podcast → Run workflow**

Check the logs. If it works, your RSS feed will appear at:
```
https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME/feed/feed.xml
```

### 6. Subscribe on your phone
Open any podcast app (Apple Podcasts, Pocket Casts, Overcast, etc.) and add your RSS feed URL.

---

## Troubleshooting

**No articles scraped?**  
Your CSS selectors in `config.py` are probably wrong. Open the site in a browser,
inspect the HTML, and find the right selector for article containers.

**Script too long / short?**  
Adjust `TARGET_DURATION_MINUTES` in `config.py`.

**Wrong voice?**  
Change `TTS_VOICE` to one of: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

---

## Cost estimate
For a 5-minute daily podcast:
- **Claude API** (script): ~$0.005/day
- **OpenAI TTS**: ~$0.05/day (at $15/1M chars, ~700 words ≈ 4000 chars)
- **GitHub**: Free
- **Total: ~$0.06/day (~$2/month)**
