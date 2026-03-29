# AI News Digest Agent — Execution Plan

A step-by-step guide to build and run the AI News Digest Agent from scratch.

---

## Step 1 — Install Libraries

Run this command in your terminal:
```
D:\AgileOS\job-tool\Scripts\pip.exe install feedparser schedule
```

**What it does:**
- Installs `feedparser` — reads RSS feeds from news websites
- Installs `schedule` — runs tasks automatically at set times

**Expected output:**
```
Successfully installed feedparser-6.0.12 schedule-1.2.2
```

---

## Step 2 — news_scraper.py — Fetch AI News

### What this file does
`news_scraper.py` is the first step in the pipeline. It goes out to the internet, fetches the latest AI news from 6 trusted sources, and saves everything to a local file (`articles.json`) for the next step to read.

### What's inside the file

**RSS Feeds configured (6 sources):**
```
Hacker News     → https://hnrss.org/frontpage?q=AI
TechCrunch AI   → https://techcrunch.com/category/artificial-intelligence/feed/
The Verge AI    → https://www.theverge.com/ai-artificial-intelligence/rss/index.xml
VentureBeat AI  → https://venturebeat.com/category/ai/feed/
MIT Tech Review → https://www.technologyreview.com/feed/
Google AI Blog  → https://blog.google/technology/ai/rss/
```

**Key functions:**
- `fetch_feed(source, url, cutoff)` — connects to one RSS feed, loops through all articles, skips anything older than 7 days, strips HTML tags from summaries, returns a clean list of articles
- `main()` — loops through all 6 feeds, combines everything into one list, sorts by newest first, saves to `articles.json`

**What each article looks like in articles.json:**
```json
{
  "title": "OpenAI launches new model",
  "source": "TechCrunch AI",
  "url": "https://techcrunch.com/...",
  "published": "2026-03-28",
  "summary": "OpenAI today announced..."
}
```

### Run command
```
D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\news_scraper.py
```

### Expected output
```
🗞️  AI News Scraper
   Fetching articles from last 7 days...

  📡 Fetching: Hacker News...
     ✅ 12 articles found
  📡 Fetching: TechCrunch AI...
     ✅ 8 articles found
  ...

💾 Saved 45 articles to articles.json
```

**Output file:** `articles.json`

---

## Step 3 — Set Up .env File

**Purpose:** The `.env` file stores your secret credentials — your Anthropic API key (to call Claude AI) and your Gmail credentials (to send the email digest). This file is never committed to GitHub so your passwords stay private.

### Step 3a — Get Your Gmail App Password

**Why do you need this?**
Gmail does not allow apps to use your normal Gmail password for security reasons. Instead, Google lets you create a special one-time **App Password** just for this tool. It takes 2 minutes.

**Steps:**
1. Go to **myaccount.google.com**
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google" — click **2-Step Verification** (must be ON — if not, enable it first)
4. Scroll to the very bottom of the 2-Step Verification page
5. Click **App passwords**
6. In the "App name" field type: `News Digest`
7. Click **Create**
8. Google shows you a **16-character password** (e.g. `abcd efgh ijkl mnop`)
9. **Copy it** — you will only see it once
10. Remove the spaces when using it — it becomes `abcdefghijklmnop`

---

### Step 3b — Create the .env File

Run this command — replace both values with your real ones:
```
D:\AgileOS\job-tool\Scripts\python.exe -c "f=open('D:/AgileOS/news-digest/.env','w',encoding='utf-8'); f.write('ANTHROPIC_API_KEY=your-actual-key\nEMAIL_SENDER=satyajeet356@gmail.com\nEMAIL_PASSWORD=your-16-char-password\nEMAIL_RECEIVER=satyajeet356@gmail.com\n'); f.close(); print('Done')"
```

**Replace:**
- `your-actual-key` → your Anthropic API key (same one used for the job tool)
- `your-16-char-password` → the Gmail App Password you just copied (no spaces)

**Expected output:**
```
Done
```

**What gets created:**
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
EMAIL_SENDER=satyajeet356@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
EMAIL_RECEIVER=satyajeet356@gmail.com
```

> ⚠️ Never share this file or commit it to GitHub — it contains your passwords.

---

## Step 4 — summariser.py — Generate AI Digest with Claude

### What this file does
`summariser.py` is the brain of the pipeline. It takes all the raw articles from `articles.json`, sends them to Claude AI in one big prompt, and asks Claude to write a structured weekly digest. The output is saved to `digest.md`.

### What's inside the file

**Key functions:**
- `load_env()` — reads credentials from `.env` file. Uses a special byte-level reader to handle UTF-16 encoding issues that Windows PowerShell sometimes creates
- `load_articles()` — reads `articles.json` and returns the full list
- `format_articles_for_prompt(articles)` — converts each article into a readable text block so Claude can process it. Format: `1. [TechCrunch AI] OpenAI launches... Link: https://...`
- `summarise(articles)` — the main function that calls Claude AI. Sends all articles with a structured prompt asking Claude to produce 4 sections

**The prompt tells Claude to write:**
```
## 🔥 Top 5 Stories This Week
  → 5 most important stories with 2-3 sentence explanation + source link

## 📦 New Tools & Product Releases
  → List of new AI tools, models, or launches (1-2 lines each)

## 🧠 What This Means For Agile Coaches & Change Leaders
  → 3-4 bullet points connecting AI news to team ways of working,
    organisational change, product delivery, and leadership

## 📌 Quick Links
  → Clean numbered list of all articles with links
```

**Claude model used:** `claude-sonnet-4-6` with 4,000 max tokens

### Run command
```
D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\summariser.py
```

### Expected output
```
📰 AI News Summariser

✅ Loaded 45 articles from articles.json
🤖 Sending 45 articles to Claude AI...
✅ Digest saved to digest.md
Next step: run emailer.py
```

**Output file:** `digest.md`

---

## Step 5 — emailer.py — Send Email to Inbox

### What this file does
`emailer.py` is the final step. It reads the `digest.md` that Claude wrote, converts the Markdown formatting into a styled HTML email, and sends it to your Gmail inbox using Gmail's SMTP service.

### What's inside the file

**Key functions:**

- `load_env()` — same UTF-16 safe `.env` reader as summariser.py. Loads `EMAIL_SENDER`, `EMAIL_PASSWORD`, and `EMAIL_RECEIVER` from the `.env` file

- `markdown_to_html(md)` — converts Markdown formatting into HTML using regex:
  - `## Heading` → `<h2>Heading</h2>`
  - `**bold**` → `<strong>bold</strong>`
  - `*italic*` → `<em>italic</em>`
  - `[text](url)` → `<a href="url">text</a>`
  - `- bullet` → `<li>` inside `<ul>`
  - `---` → `<hr>` horizontal divider line
  - Blank lines → paragraph breaks

- `build_email_html(digest_md)` — wraps the converted HTML in a full email template with:
  - Dark navy header (`#1a1a2e` gradient) with gold "Weekly AI Digest" title
  - White content area with the digest body
  - Small footer with auto-generation note
  - Max width 640px (standard email width)

- `send_email(subject, html_body, sender, password, receiver)` — connects to Gmail's SMTP server on port 465 (SSL encrypted), logs in with your App Password, and sends the email

**Gmail SMTP settings used:**
```
Server:  smtp.gmail.com
Port:    465
Method:  SSL (SMTP_SSL)
Login:   your Gmail address + App Password
```

**Email subject format:**
```
🗞️ Weekly AI Digest — 29 March 2026
```

### Run command
```
D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\emailer.py
```

### Expected output
```
📧 AI News Emailer

   Sending to satyajeet356@gmail.com...
✅ Email sent successfully!
   Subject: 🗞️ Weekly AI Digest — 29 March 2026
   Check your inbox at satyajeet356@gmail.com
```

**Check your inbox** — you should receive the digest email within seconds.

**If it fails, common fixes:**
- Check your Gmail App Password is correct in `.env` (no spaces, 16 characters)
- Make sure 2-Step Verification is ON in your Google account
- Check you used an App Password, not your normal Gmail password

---

## Step 6 — run_now.py — Test Everything Together

### What this file does
`run_now.py` is a convenience script that runs all three steps back to back in a single command. Use this whenever you want to generate and send a fresh digest immediately without running each file separately — for testing or for a one-off manual run.

### What's inside the file

**Key function:**
- `run(script, label)` — runs a single Python script using `subprocess`. If a script fails (e.g. scraper crashes), it prints an error and **stops the pipeline immediately** — it won't try to send a broken digest
- `main()` — calls all 3 scripts in order: scraper → summariser → emailer

**What it does step by step:**
1. Prints "Running Full Pipeline"
2. Runs `news_scraper.py` — fetches fresh articles, saves `articles.json`
3. Runs `summariser.py` — sends articles to Claude, saves `digest.md`
4. Runs `emailer.py` — reads `digest.md`, sends email to your inbox
5. Prints "Pipeline complete — check your inbox!"

**If any step fails** — it stops there and prints which script failed. So you won't get a blank email if the scraper broke.

### Run command
```
D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\run_now.py
```

### Expected output
```
🚀 AI News Digest — Running Full Pipeline

==================================================
▶  Step 1/3 — Fetching AI news...
==================================================
🗞️  AI News Scraper
   ...
💾 Saved 45 articles to articles.json

==================================================
▶  Step 2/3 — Summarising with Claude AI...
==================================================
📰 AI News Summariser
🤖 Sending 45 articles to Claude AI...
✅ Digest saved to digest.md

==================================================
▶  Step 3/3 — Sending email...
==================================================
📧 AI News Emailer
   Sending to satyajeet356@gmail.com...
✅ Email sent successfully!

✅ Pipeline complete — check your inbox!
```

---

## Step 7 — scheduler.py — Schedule Weekly (Set and Forget)

### What this file does
`scheduler.py` keeps running in the background and automatically triggers the full pipeline every Sunday at 8am. Once you start it, you don't need to do anything — the digest will just arrive in your inbox every week without you touching a single command.

### What's inside the file

**Key functions:**
- `run_pipeline()` — called automatically every Sunday at 08:00. Runs `run_now.py` (which triggers all 3 scripts). Prints the timestamp when it starts so you can see the history in the terminal
- `next_sunday_8am()` — calculates and displays the date of the next Sunday so you know exactly when the first run will happen
- `main()` — sets up the weekly Sunday 08:00 schedule using the `schedule` library, then enters an infinite loop that checks every 60 seconds whether it's time to run

**How the loop works:**
```
Every 60 seconds → check: is it Sunday 08:00?
  → Yes → run full pipeline → send email
  → No  → go back to sleep for 60 seconds
```

**Important:** The terminal must stay open for the scheduler to keep running. If you close the terminal, the scheduler stops. To make it truly permanent (runs even when you're not logged in), you would add it to Windows Task Scheduler — but for now, leaving the terminal open is enough.

### Run command
```
D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\scheduler.py
```

### Expected output
```
⏰ Scheduler running — digest will send every Sunday at 08:00
   Next run: Sunday 2026-04-06 08:00
   Press Ctrl+C to stop
```

After this, nothing more happens until Sunday 8am — then you'll see:
```
⏰ [2026-04-06 08:00] Running weekly digest...
🚀 AI News Digest — Running Full Pipeline
...
✅ Digest sent successfully.
```

**To stop the scheduler:** press `Ctrl+C` in the terminal.

---

## Step 8 — Make the Scheduler Permanent (Windows Task Scheduler)

### The problem with scheduler.py

`scheduler.py` only works as long as the terminal window stays open. The moment you close the terminal — or restart your PC — the scheduler stops. This means:

- You close the terminal by accident → no more Sunday emails
- You restart Windows → have to remember to run `scheduler.py` again
- You go on holiday → no one is keeping the terminal open → no digest

This is not "set and forget" — it requires you to babysit a terminal window.

### Why Windows Task Scheduler is better

Windows Task Scheduler is a built-in Windows feature that runs programs automatically on a schedule — **completely independent of any terminal window**. It runs in the background as a Windows service, which means:

| | scheduler.py | Windows Task Scheduler |
|---|---|---|
| Terminal must stay open | ✅ Yes | ❌ No |
| Survives PC restart | ❌ No | ✅ Yes |
| Works when you're logged out | ❌ No | ✅ Yes |
| Requires any manual steps each week | ✅ Yes | ❌ No |
| Truly "set and forget" | ❌ No | ✅ Yes |

With Windows Task Scheduler, you set it up once and it runs every Sunday at 8am forever — even after restarts, even if you never open a terminal again.

### How to set it up (one-time setup, ~5 minutes)

**Step 1 — Open Task Scheduler**
1. Press `Windows key + S`
2. Type `Task Scheduler`
3. Click to open it

**Step 2 — Create a new task**
1. In the right panel, click **Create Basic Task...**
2. Name it: `AI News Digest`
3. Description: `Weekly AI news digest — runs every Sunday at 8am`
4. Click **Next**

**Step 3 — Set the trigger**
1. Select **Weekly**
2. Click **Next**
3. Set Start time: `8:00 AM`
4. Tick only **Sunday**
5. Click **Next**

**Step 4 — Set the action**
1. Select **Start a program**
2. Click **Next**
3. In the **Program/script** field, enter:
   ```
   D:\AgileOS\job-tool\Scripts\python.exe
   ```
4. In the **Add arguments** field, enter:
   ```
   D:\AgileOS\news-digest\run_now.py
   ```
5. Click **Next**

**Step 5 — Finish**
1. Tick **Open the Properties dialog when I click Finish**
2. Click **Finish**
3. In the Properties dialog → **Conditions** tab → untick **"Start the task only if the computer is on AC power"** (so it runs on battery too)
4. Click **OK**

That's it. Every Sunday at 8am, Windows will run the full pipeline and send the digest to your inbox — no terminal, no manual steps.

### To test it worked
Right-click the task in Task Scheduler → click **Run** → check your inbox within 2 minutes.

### To disable it later
Right-click the task → **Disable**. Re-enable any time.

### Cons of Windows Task Scheduler

| Problem | Detail |
|---|---|
| **Laptop must be on** | If your laptop is fully shut down at 8am Sunday, the task is skipped entirely |
| **Sleep workaround** | You can tick "Wake the computer to run this task" in the Conditions tab — but this only works if the laptop is in Sleep mode, not shut down or hibernated |
| **Tied to your machine** | If you get a new laptop or reinstall Windows, you have to set it all up again |
| **Local only** | Only runs on your specific laptop — no backup if something goes wrong with the machine |

**Bottom line:** Windows Task Scheduler is fine if your laptop is usually sleeping (not shut down) on Sunday mornings. If you travel, shut your laptop down at night, or want something truly reliable — use one of the cloud options below.

---

## Step 9 — Alternative Scheduling Options

### Why consider an alternative?

Windows Task Scheduler requires your laptop to be on or sleeping. If it is shut down, the digest is missed. Cloud-based options run on servers that are always on — your laptop state is completely irrelevant.

---

### Option A — GitHub Actions (Recommended — Free, Always On)

**What it is:** GitHub can run your Python script on their own servers on a schedule — for free. No laptop needed. No server to manage. You just push your code to GitHub and add one config file.

**How it works:**
- Your code lives on GitHub (you're pushing there anyway)
- You add a file called `.github/workflows/digest.yml` that tells GitHub: "run `run_now.py` every Sunday at 8am"
- GitHub's servers run it on schedule — your laptop can be off, closed, or in another country

**Cost:** Free (GitHub Actions gives 2,000 free minutes/month — your digest uses about 2 minutes per run)

**Pros:**
- Completely free
- Always runs — 100% independent of your laptop
- No servers to set up or maintain
- One extra config file added to your existing GitHub repo
- Logs every run so you can see if it succeeded or failed

**Cons:**
- Requires your code to be on GitHub (which you're doing anyway)
- `.env` credentials can't be committed to GitHub — you store them as GitHub Secrets instead (takes 2 minutes to set up)
- Slight learning curve for the config file format (YAML) — but Claude can write it for you

**The config file looks like this (Claude writes this for you):**
```yaml
# .github/workflows/digest.yml
name: Weekly AI Digest
on:
  schedule:
    - cron: '0 8 * * 0'   # Every Sunday at 8am UTC
jobs:
  send-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install feedparser anthropic
      - run: python news-digest/run_now.py
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_RECEIVER: ${{ secrets.EMAIL_RECEIVER }}
```

**To set it up:**
1. Push your code to GitHub (Step 10 of this plan)
2. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
3. Add your 4 credentials as secrets (ANTHROPIC_API_KEY, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER)
4. Add the `.github/workflows/digest.yml` file to your repo
5. Done — GitHub handles everything from here

---

### Option B — PythonAnywhere (Easiest Cloud Option — Free)

**What it is:** A website specifically designed to host and run Python scripts. You upload your files, set a schedule, and their servers run it — no configuration files, no YAML, no complex setup.

**How it works:**
- Create a free account at pythonanywhere.com
- Upload your news-digest files
- Go to the **Tasks** tab and set: "run `run_now.py` every Sunday at 8am"
- Their servers handle everything

**Cost:** Free tier — allows 1 scheduled task per day (more than enough for weekly)

**Pros:**
- Simplest cloud option — no config files or code changes needed
- Visual interface — everything done through a website
- Always on — completely independent of your laptop
- Free for this use case

**Cons:**
- Free tier has limitations (1 task/day, limited CPU time)
- Your files and credentials live on their servers — minor privacy consideration
- Less control than GitHub Actions
- If PythonAnywhere changes their pricing, you'd need to migrate

**To set it up:**
1. Go to pythonanywhere.com → create a free account
2. Go to **Files** tab → upload all your `news-digest/` files
3. Go to **Consoles** tab → open a Bash console → run `pip install feedparser anthropic`
4. Create your `.env` file on their server with your credentials
5. Go to **Tasks** tab → set the schedule to run `run_now.py` every Sunday at 8am
6. Done

---

### Comparison: All Scheduling Options

| | scheduler.py | Windows Task Scheduler | GitHub Actions | PythonAnywhere |
|---|---|---|---|---|
| Works when laptop is off | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| Works when laptop is sleeping | ❌ No | ✅ Yes (with wake setting) | ✅ Yes | ✅ Yes |
| Survives laptop restart | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Cost | Free | Free | Free | Free |
| Setup complexity | None | Low | Medium | Low |
| Truly set and forget | ❌ No | Mostly | ✅ Yes | ✅ Yes |
| Recommended for | Testing only | Laptop always sleeping | Best overall | Simplest cloud |

**Recommended path:**
- Just testing → use `run_now.py` manually
- Laptop usually sleeping Sunday mornings → Windows Task Scheduler
- Want it to work no matter what → GitHub Actions (best long-term choice)

---

## Full File Structure

```
D:\AgileOS\news-digest\
├── news_scraper.py      ← Step 2: Fetches AI news from 6 RSS feeds → articles.json
├── summariser.py        ← Step 4: Claude AI reads articles → digest.md
├── emailer.py           ← Step 5: Converts digest.md to HTML → sends to inbox
├── run_now.py           ← Step 6: Runs all 3 steps above in one command
├── scheduler.py         ← Step 7: Runs automatically every Sunday at 8am
├── articles.json        ← Auto generated — raw articles (output of news_scraper.py)
├── digest.md            ← Auto generated — Claude's summary (output of summariser.py)
├── .env                 ← Your credentials (never committed to GitHub)
├── PROJECT_PLAN.md      ← Full project overview
└── EXECUTION_PLAN.md    ← This file
```

---

## Quick Reference — All Commands

| Step | File | Command |
|---|---|---|
| Install libraries | — | `D:\AgileOS\job-tool\Scripts\pip.exe install feedparser schedule` |
| Fetch news | `news_scraper.py` | `D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\news_scraper.py` |
| Set up credentials | `.env` | See Step 3 above |
| Generate digest | `summariser.py` | `D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\summariser.py` |
| Send email | `emailer.py` | `D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\emailer.py` |
| Test everything | `run_now.py` | `D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\run_now.py` |
| Start scheduler | `scheduler.py` | `D:\AgileOS\job-tool\Scripts\python.exe D:\AgileOS\news-digest\scheduler.py` |
