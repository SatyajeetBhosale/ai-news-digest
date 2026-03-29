"""
summariser.py — AI News Summariser
Reads articles.json, sends to Claude AI, saves structured digest to digest.md
"""

import json
import os

import anthropic

# ── CONFIG ───────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
ARTICLES_FILE = os.path.join(BASE_DIR, "articles.json")
DIGEST_FILE   = os.path.join(BASE_DIR, "digest.md")
ENV_FILE      = os.path.join(BASE_DIR, ".env")
# ─────────────────────────────────────────────────────────────────────────────


def load_env():
    """Load API key from .env file — handles UTF-16 encoding from Windows PowerShell."""
    if os.path.exists(ENV_FILE):
        raw     = open(ENV_FILE, "rb").read()
        cleaned = raw.replace(b"\xff\xfe", b"").replace(b"\xfe\xff", b"").replace(b"\x00", b"")
        for line in cleaned.decode("utf-8").strip().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()


def load_articles() -> list:
    with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_articles_for_prompt(articles: list) -> str:
    """Format articles into a compact text block for the Claude prompt."""
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['source']}] {a['title']}")
        if a.get("summary"):
            lines.append(f"   {a['summary'][:300]}")
        lines.append(f"   Link: {a['url']}")
        lines.append("")
    return "\n".join(lines)


def summarise(articles: list) -> str:
    """Send articles to Claude AI and get back a structured digest."""
    client    = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    articles_text = format_articles_for_prompt(articles)

    prompt = f"""You are an AI news analyst. Below are {len(articles)} AI news articles from the past 7 days.

{articles_text}

Please write a weekly AI digest with the following sections:

## 🗞️ Weekly AI Digest — {__import__('datetime').date.today().strftime('%d %B %Y')}

## 🔥 Top 5 Stories This Week
List the 5 most important or interesting stories. For each:
- Bold headline
- 2-3 sentence explanation of what happened and why it matters
- Source and link

## 📦 New Tools & Product Releases
List any new AI tools, models, or product launches mentioned. Keep each to 1-2 lines.

## 🧠 What This Means For Agile Coaches & Change Leaders
3-4 bullet points on how this week's AI developments are relevant to:
- Team ways of working
- Organisational change
- Product delivery
- Leadership and decision making

## 📌 Quick Links
A clean list of all article titles with their links.

Keep the tone professional but conversational. Be specific — avoid vague generalisations."""

    print(f"🤖 Sending {len(articles)} articles to Claude AI...")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def main():
    load_env()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in .env file.")
        exit(1)

    print("\n📰 AI News Summariser\n")

    articles = load_articles()
    print(f"✅ Loaded {len(articles)} articles from articles.json")

    digest = summarise(articles)

    with open(DIGEST_FILE, "w", encoding="utf-8") as f:
        f.write(digest)

    print(f"✅ Digest saved to digest.md")
    print("Next step: run emailer.py")


if __name__ == "__main__":
    main()
