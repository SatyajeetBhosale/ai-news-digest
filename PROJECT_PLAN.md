# AI News Digest Agent — Project Plan

## What It Does
A weekly AI news digest delivered to your email every Sunday morning.
Scrapes latest AI news from 6 sources, summarises with Claude AI, and emails a clean digest automatically.

---

## Phase 1 — Install Libraries

Two new libraries needed:
```
pip install feedparser schedule
```

| Library | Purpose |
|---|---|
| `feedparser` | Reads RSS feeds from news sites |
| `schedule` | Runs tasks automatically at set times |

Already installed (from job tool):

| Library | Purpose |
|---|---|
| `anthropic` | Claude AI API |
| `requests` | HTTP requests |
| `playwright` | Browser automation |

---

## Phase 2 — Project Structure

```
D:\AgileOS\news-digest\
├── news_scraper.py      ← NEW — fetches AI news from RSS feeds
├── summariser.py        ← NEW — Claude AI creates digest
├── emailer.py           ← NEW — sends email to inbox
├── scheduler.py         ← NEW — runs every Sunday at 8am
├── run_now.py           ← NEW — runs immediately for testing
├── articles.json        ← AUTO GENERATED — raw articles from scraper
├── digest.md            ← AUTO GENERATED — Claude's summary
└── .env                 ← NEW — API key + email credentials
```

---

## Each File Explained

### `news_scraper.py` — NEW
Connects to 6 RSS feeds, filters last 7 days of articles, saves to `articles.json`.

**Input:** Nothing — runs on its own
**Output:** `articles.json`

**News Sources:**
| Source | RSS Feed |
|---|---|
| Hacker News AI | https://hnrss.org/frontpage?q=AI |
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ |
| The Verge AI | https://www.theverge.com/ai-artificial-intelligence/rss/index.xml |
| VentureBeat AI | https://venturebeat.com/category/ai/feed/ |
| MIT Tech Review | https://www.technologyreview.com/feed/ |
| Google AI Blog | https://blog.google/technology/ai/rss/ |

---

### `summariser.py` — NEW
Reads `articles.json`, sends to Claude AI, gets back structured digest, saves to `digest.md`.

**Input:** `articles.json`
**Output:** `digest.md`

**Digest structure Claude produces:**
- 🔥 Top 5 Stories of the week
- 📦 New Tools & Product Releases
- 🧠 What This Means For Agile Coaches

---

### `emailer.py` — NEW
Reads `digest.md`, converts to HTML email, sends to your Gmail.

**Input:** `digest.md`
**Output:** 📧 Email in your inbox

> Note: Gmail needs an **App Password** — a special password just for apps.
> Your normal Gmail password won't work. Takes 2 minutes to set up.

---

### `scheduler.py` — NEW
Runs scraper → summariser → emailer every Sunday at 8am.
Leave it running in the background — no manual steps needed.

**Input:** Nothing
**Output:** Triggers all 3 files above in sequence

---

### `run_now.py` — NEW
Same as scheduler but runs immediately. Used for testing.

**Input:** Nothing
**Output:** Triggers all 3 files above immediately

---

### `articles.json` — AUTO GENERATED
Raw list of articles fetched from RSS feeds. Created fresh every run.

```json
[
  {
    "title": "OpenAI launches GPT-5",
    "source": "TechCrunch",
    "url": "https://...",
    "published": "2026-03-29",
    "summary": "OpenAI today announced..."
  }
]
```

---

### `digest.md` — AUTO GENERATED
Claude's structured summary. Created fresh every run.

```
## 🔥 Top 5 Stories
1. OpenAI launches GPT-5...

## 📦 New Tools Released
...

## 🧠 What This Means For Agile Coaches
...
```

---

### `.env` — NEW
Stores your credentials securely. Never committed to GitHub.

```
ANTHROPIC_API_KEY=your-key
EMAIL_SENDER=satyajeet356@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_RECEIVER=satyajeet356@gmail.com
```

---

## Full Flow

```
Every Sunday 8am (scheduler.py)
        │
        ▼
news_scraper.py   →   articles.json
        │
        ▼
summariser.py     →   digest.md
        │
        ▼
emailer.py        →   📧 Your inbox
```

---

## Build Order
1. ✅ Phase 1 — Install libraries
2. news_scraper.py
3. summariser.py
4. emailer.py
5. run_now.py (test end to end)
6. scheduler.py (set and forget)
