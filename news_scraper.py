"""
news_scraper.py — AI News Scraper
Fetches latest AI news from 6 RSS feeds and saves to articles.json
"""

import json
import os
import re
import feedparser
from datetime import datetime, timezone, timedelta

# ── CONFIG ───────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE  = os.path.join(BASE_DIR, "articles.json")
DAYS_BACK    = 7   # Only fetch articles from last 7 days

RSS_FEEDS = [
    {"source": "Hacker News",     "url": "https://hnrss.org/frontpage?q=AI"},
    {"source": "TechCrunch AI",   "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"source": "The Verge AI",    "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"},
    {"source": "VentureBeat AI",  "url": "https://venturebeat.com/category/ai/feed/"},
    {"source": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
    {"source": "Google AI Blog",  "url": "https://blog.google/technology/ai/rss/"},
]
# ─────────────────────────────────────────────────────────────────────────────


def fetch_feed(source: str, url: str, cutoff: datetime) -> list:
    """Fetch articles from a single RSS feed and filter by date."""
    print(f"  📡 Fetching: {source}...")
    articles = []

    try:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            # Parse published date
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

            # Skip if older than cutoff or no date
            if not published or published < cutoff:
                continue

            # Extract summary and strip HTML tags
            summary = ""
            if hasattr(entry, "summary"):
                summary = re.sub(r"<[^>]+>", "", entry.summary).strip()
                summary = summary[:500]  # Limit length

            articles.append({
                "title":     entry.get("title", "No title").strip(),
                "source":    source,
                "url":       entry.get("link", ""),
                "published": published.strftime("%Y-%m-%d"),
                "summary":   summary
            })

        print(f"     ✅ {len(articles)} articles found")

    except Exception as e:
        print(f"     ❌ Failed: {e}")

    return articles


def main():
    print("\n🗞️  AI News Scraper")
    print(f"   Fetching articles from last {DAYS_BACK} days...\n")

    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)
    all_articles = []

    for feed in RSS_FEEDS:
        articles = fetch_feed(feed["source"], feed["url"], cutoff)
        all_articles.extend(articles)

    # Sort by date — newest first
    all_articles.sort(key=lambda x: x["published"], reverse=True)

    # Save to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved {len(all_articles)} articles to articles.json")
    print("Next step: run summariser.py")


if __name__ == "__main__":
    main()
