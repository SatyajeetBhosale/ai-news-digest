# AI News Digest Agent

A fully automated weekly AI news digest delivered to your email every Sunday morning. No manual steps after setup.

---

## Why This Exists

AI is moving fast — new models, tools, and research drop every week. Keeping up means visiting dozens of websites, reading through noise, and trying to figure out what actually matters.

This agent solves that. It:
- Scrapes the latest AI news from 6 trusted sources every week
- Sends everything to Claude AI, which reads and filters it
- Writes a structured digest focused on what matters — top stories, new tools, and what it means for your work
- Emails the digest to your inbox automatically every Sunday at 8am

You set it up once. Every Sunday morning, the digest arrives — no browser tabs, no manual effort.

---

## What You Get in the Email

Each digest has 4 sections:

| Section | What's in it |
|---|---|
| 🔥 Top 5 Stories | The 5 most important AI stories of the week with context on why they matter |
| 📦 New Tools & Releases | New AI models, products, and launches — 1-2 lines each |
| 🧠 What This Means For Agile Coaches | How this week's AI developments connect to team ways of working, organisational change, and product delivery |
| 📌 Quick Links | Full numbered list of all articles with links |

---

## News Sources

| Source | What it covers |
|---|---|
| Hacker News | Developer and technical AI discussions |
| TechCrunch AI | AI company news, funding, product launches |
| The Verge AI | Consumer AI and product coverage |
| VentureBeat AI | Enterprise AI and industry analysis |
| MIT Technology Review | Research, policy, and deeper AI analysis |
| Google AI Blog | Google's own AI releases and research |

---

## How It Works

```
Every Sunday 8am
       │
       ▼
news_scraper.py   →   Fetches articles from 6 RSS feeds   →   articles.json
       │
       ▼
summariser.py     →   Claude AI reads and writes digest    →   digest.md
       │
       ▼
emailer.py        →   Converts to HTML email, sends        →   📧 Your inbox
```

---

## File Structure

```
ai-news-digest/
├── news_scraper.py              ← Fetches AI news from 6 RSS feeds
├── summariser.py                ← Sends articles to Claude AI, generates digest
├── emailer.py                   ← Converts digest to HTML email, sends via Gmail
├── run_now.py                   ← Runs full pipeline immediately (for testing)
├── scheduler.py                 ← Runs pipeline every Sunday at 8am (local)
├── .github/
│   └── workflows/
│       └── digest.yml           ← GitHub Actions: runs on GitHub servers every Sunday
├── .env                         ← Your credentials (not committed — see below)
├── .gitignore                   ← Excludes .env, articles.json, digest.md
├── PROJECT_PLAN.md              ← Project overview
└── EXECUTION_PLAN.md            ← Full step-by-step build and run guide
```

---

## Setup

### Prerequisites
- Python 3.10 or higher
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)
- A Gmail account with a Gmail App Password (see Step 2 below)

---

### Step 1 — Clone the repo and install libraries

```bash
git clone https://github.com/SatyajeetBhosale/ai-news-digest.git
cd ai-news-digest
pip install feedparser anthropic schedule
```

---

### Step 2 — Get a Gmail App Password

Gmail does not allow apps to use your regular Gmail password. You need to create a special **App Password** — takes 2 minutes.

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google" → click **2-Step Verification** (must be ON)
4. Scroll to the bottom → click **App passwords**
5. In the App name field type: `News Digest`
6. Click **Create**
7. Google shows a **16-character password** e.g. `abcd efgh ijkl mnop`
8. Copy it — you will only see it once
9. Remove spaces when using it: `abcdefghijklmnop`

---

### Step 3 — Create your .env file

Create a file called `.env` in the project folder with the following contents:

```
ANTHROPIC_API_KEY=your-anthropic-api-key
EMAIL_SENDER=your-gmail@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
EMAIL_RECEIVER=your-gmail@gmail.com
```

Replace each value with your real credentials. This file is excluded from git — your passwords will never be committed.

> **Tip:** Run this command to create the file safely (avoids encoding issues on Windows):
> ```
> python -c "f=open('.env','w',encoding='utf-8'); f.write('ANTHROPIC_API_KEY=your-key\nEMAIL_SENDER=you@gmail.com\nEMAIL_PASSWORD=yourpassword\nEMAIL_RECEIVER=you@gmail.com\n'); f.close(); print('Done')"
> ```

---

### Step 4 — Test the full pipeline

Run everything in one command:

```bash
python run_now.py
```

Expected output:
```
🚀 AI News Digest — Running Full Pipeline

▶  Step 1/3 — Fetching AI news...
💾 Saved 42 articles to articles.json

▶  Step 2/3 — Summarising with Claude AI...
✅ Digest saved to digest.md

▶  Step 3/3 — Sending email...
✅ Email sent successfully!

✅ Pipeline complete — check your inbox!
```

Check your inbox — you should receive the digest email within seconds.

---

## Scheduling Options

Once the pipeline works, you have 3 options to automate it:

### Option 1 — GitHub Actions (Recommended — Free, Always On)

GitHub runs the pipeline on their servers every Sunday at 8am — completely independent of your laptop. Your laptop can be off, closed, or in another country.

**Setup:**

1. Push your code to GitHub
2. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
3. Add these 4 secrets:

| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `EMAIL_SENDER` | Your Gmail address |
| `EMAIL_PASSWORD` | Your 16-char App Password (no spaces) |
| `EMAIL_RECEIVER` | Your Gmail address |

4. The `.github/workflows/digest.yml` file is already in this repo — no extra steps needed
5. Go to **Actions** tab → **Weekly AI News Digest** → **Run workflow** to test immediately

> **Timezone note:** The workflow runs at `02:30 UTC` which equals `08:00 IST`. To change for your timezone, edit the cron value in `digest.yml`. Use [crontab.guru](https://crontab.guru) to convert your local time to UTC.

---

### Option 2 — Windows Task Scheduler (Local)

Runs on your laptop every Sunday at 8am. Works even without a terminal open — but requires your laptop to be on or sleeping (not shut down).

1. Press `Windows key + S` → type `Task Scheduler` → open it
2. Click **Create Basic Task**
3. Name: `AI News Digest`
4. Trigger: Weekly → Sunday → 8:00 AM
5. Action: Start a program
   - Program: `C:\path\to\python.exe`
   - Arguments: `C:\path\to\ai-news-digest\run_now.py`
6. In Properties → Conditions tab → tick **Wake the computer to run this task**

---

### Option 3 — Run Manually

Skip scheduling entirely. Run `python run_now.py` whenever you want a fresh digest. Takes about 2 minutes.

---

## Running Individual Steps

If you want to run each step separately:

```bash
# Step 1 — Fetch news only
python news_scraper.py

# Step 2 — Generate digest only (requires articles.json)
python summariser.py

# Step 3 — Send email only (requires digest.md)
python emailer.py

# Run all 3 together
python run_now.py

# Start local scheduler (runs every Sunday 8am, terminal must stay open)
python scheduler.py
```

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ANTHROPIC_API_KEY not found` | `.env` file missing or wrong path | Create `.env` in the same folder as the scripts |
| `Username and Password not accepted` | Wrong Gmail App Password | Re-enter the App Password — 16 chars, no spaces, from App Passwords page |
| `digest.md not found` | Running emailer before summariser | Run `summariser.py` first, or use `run_now.py` |
| `0 articles found` from a source | RSS feed temporarily down | Normal — other sources will still work |
| GitHub Actions shows green but no email | Email failed silently | Check the run logs under the **Run digest pipeline** step for the actual error |

---

## Requirements

```
feedparser
anthropic
schedule
```

Standard library only (no extra installs needed): `smtplib`, `json`, `os`, `re`, `datetime`, `subprocess`

---

## Built With

- [Anthropic Claude API](https://www.anthropic.com) — AI summarisation (`claude-sonnet-4-6`)
- [feedparser](https://feedparser.readthedocs.io) — RSS feed parsing
- [smtplib](https://docs.python.org/3/library/smtplib.html) — Gmail SMTP email sending
- [GitHub Actions](https://github.com/features/actions) — Automated weekly scheduling

---

## License

MIT — free to use, modify, and share.
