"""
run_now.py — Run the full AI News Digest pipeline immediately.
Runs: news_scraper → summariser → emailer in sequence.
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON   = sys.executable


def run(script: str, label: str):
    print(f"\n{'='*50}")
    print(f"▶  {label}")
    print(f"{'='*50}")
    result = subprocess.run([PYTHON, os.path.join(BASE_DIR, script)])
    if result.returncode != 0:
        print(f"\n❌ {script} failed. Stopping pipeline.")
        sys.exit(1)


def main():
    print("\n🚀 AI News Digest — Running Full Pipeline\n")
    run("news_scraper.py", "Step 1/3 — Fetching AI news...")
    run("summariser.py",   "Step 2/3 — Summarising with Claude AI...")
    run("emailer.py",      "Step 3/3 — Sending email...")
    print("\n✅ Pipeline complete — check your inbox!\n")


if __name__ == "__main__":
    main()
