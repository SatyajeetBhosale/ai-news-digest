"""
scheduler.py — Weekly AI News Digest Scheduler
Runs the full pipeline automatically every Sunday at 08:00.
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON   = sys.executable


def run_pipeline():
    print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Running weekly digest...\n")
    result = subprocess.run([PYTHON, os.path.join(BASE_DIR, "run_now.py")])
    if result.returncode == 0:
        print("✅ Digest sent successfully.")
    else:
        print("❌ Pipeline failed — check the output above.")


def next_sunday_8am() -> str:
    """Return the date string of the next Sunday at 08:00."""
    today = datetime.now()
    days_ahead = 6 - today.weekday()  # Sunday = 6
    if days_ahead <= 0:
        days_ahead += 7
    next_sunday = today + timedelta(days=days_ahead)
    return next_sunday.strftime("%Y-%m-%d")


def main():
    schedule.every().sunday.at("08:00").do(run_pipeline)

    next_run = next_sunday_8am()
    print("\n⏰ Scheduler running — digest will send every Sunday at 08:00")
    print(f"   Next run: Sunday {next_run} 08:00")
    print("   Press Ctrl+C to stop\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
