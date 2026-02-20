#!/usr/bin/env python3
"""
KidWatch Pipeline — YouTube Watch History Scraper
Logs into YouTube via the openclaw browser profile,
scrapes watch history for the configured account,
and outputs structured JSON to data/history.json

Usage: Run by cron agent with browser access via openclaw browser profile.
The agent logs in as the configured Google account and scrapes
https://www.youtube.com/feed/history
"""

import json
import re
import datetime
from pathlib import Path
from collections import Counter, defaultdict

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "history.json"

# YouTube categories mapping (simplified)
CATEGORY_KEYWORDS = {
    "Gaming": ["minecraft", "roblox", "fortnite", "game", "gaming", "gameplay", "let's play", "playthrough"],
    "Cartoons & Animation": ["cartoon", "animation", "animated", "anime", "peppa", "paw patrol", "bluey"],
    "Music": ["music", "song", "official video", "mv", "lyrics", "audio"],
    "Science & Education": ["science", "learn", "how to", "tutorial", "education", "facts", "experiment", "history"],
    "Sports": ["sport", "soccer", "football", "basketball", "nba", "nfl", "fifa"],
    "Comedy & Skits": ["funny", "comedy", "prank", "skit", "hilarious", "laugh"],
    "Unboxing & Toys": ["unbox", "toy", "review", "haul", "lego", "playmobil"],
    "Vlogs & DIY": ["vlog", "day in", "diy", "craft", "art", "drawing", "painting"],
    "Animals & Nature": ["animal", "nature", "dog", "cat", "wildlife", "zoo", "pet"],
    "Other": []
}

def categorize_video(title: str, channel: str) -> str:
    title_lower = title.lower()
    channel_lower = channel.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == "Other":
            continue
        if any(kw in title_lower or kw in channel_lower for kw in keywords):
            return category
    return "Other"

def parse_watch_history(raw_videos: list) -> dict:
    """Process raw video list into structured stats."""
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=7)

    recent = [v for v in raw_videos if v.get("watched_at") and
              datetime.datetime.fromisoformat(v["watched_at"]) > cutoff]

    channels = Counter(v.get("channel", "Unknown") for v in recent)
    categories = Counter(
        categorize_video(v.get("title", ""), v.get("channel", ""))
        for v in recent
    )

    hourly = defaultdict(int)
    daily = defaultdict(int)
    total_minutes = 0

    for v in recent:
        if v.get("watched_at"):
            dt = datetime.datetime.fromisoformat(v["watched_at"])
            hourly[dt.hour] += 1
            daily[dt.strftime("%a")] += 1
        if v.get("duration_seconds"):
            total_minutes += v["duration_seconds"] / 60

    return {
        "generated": now.isoformat(),
        "period_days": 7,
        "total_videos": len(recent),
        "total_watch_minutes": round(total_minutes),
        "videos": recent[:50],  # keep last 50 for display
        "top_channels": [{"channel": c, "count": n} for c, n in channels.most_common(10)],
        "top_categories": [{"category": c, "count": n} for c, n in categories.most_common()],
        "hourly_counts": {str(h): hourly[h] for h in range(24)},
        "daily_counts": {d: daily[d] for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
    }

def save_output(data: dict):
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(data, indent=2))
    print(f"✅ Saved {data['total_videos']} videos to {OUTPUT_FILE}")

if __name__ == "__main__":
    # Placeholder — actual scraping done by cron agent via browser
    print("KidWatch pipeline module loaded.")
    print("Run via cron agent with browser access.")
