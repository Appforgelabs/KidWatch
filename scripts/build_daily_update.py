#!/usr/bin/env python3
"""
Build history.json from raw browser-scraped YouTube data.
Run as: python3 build_daily_update.py
"""

import json
import re
from datetime import datetime, timedelta, timezone
from collections import Counter
from pathlib import Path
import random

# ── Raw video data scraped from YouTube history ──────────────────────────────
RAW_VIDEOS = [{"title":"Peppa Pig in Avatar World VS Toca World | George Catches a Cold 😰","channel":"Dino Avatar","duration":"4 minutes, 30 seconds","url":"https://www.youtube.com/watch?v=kkebnd4qW60"},{"title":"Cocomelon Intro Logo with JJ's Animals Crying Lego Bricks Logo Sponsored By Preview 2 Effects","channel":"Maizrobo","duration":"3 minutes, 57 seconds","url":"https://www.youtube.com/watch?v=ZEtqiw8YR1U"},{"title":"How To Make PBS Kids Dash Logo Effects Sponsored By Preview 2 Effects On KineMaster","channel":"Gerrard","duration":"15 minutes","url":"https://www.youtube.com/watch?v=JUA2VHuwtw0"},{"title":"PBS Kids ID / System Cue Compilation (1999-2022)","channel":"Peeebs","duration":"5 minutes, 37 seconds","url":"https://www.youtube.com/watch?v=2sQ1JQKrOe4"},{"title":"Find the ODD One Out - Logo Challenge 🍏🎧📱 | 60 Ultimate Levels Quiz | Quiz Dino","channel":"Quiz Dino","duration":"26 minutes","url":"https://www.youtube.com/watch?v=Raw0xcRniew"},{"title":"Guess Correct Logo ✅ - Logo Challenge | 30 Levels Quiz 2023","channel":"QUIZ CAKE","duration":"11 minutes, 16 seconds","url":"https://www.youtube.com/watch?v=Bm-1zEfEg5k"},{"title":"(most viewed)\"Halloween Noodle and Pals\" Logo Effects | Spoir","channel":"Spoir","duration":"3 minutes, 53 seconds","url":"https://www.youtube.com/watch?v=rI26hNUs3Y4"},{"title":"Logo Effects Pixel Art Minecraft Compilation 2024 V8","channel":"Ikigai Effects","duration":"2 minutes, 45 seconds","url":"https://www.youtube.com/watch?v=uH5svWnv9_0"},{"title":"Cocomelon Little Pocket Library: Read Aloud 6 Book Collection for Children and Toddlers","channel":"Shall We Read A Book?","duration":"5 minutes, 48 seconds","url":"https://www.youtube.com/watch?v=NL3AZ57hqh8"},{"title":"Peppa Pig: World Adventures - Full Game - Nintendo Switch Gameplay","channel":"Best Game Videos","duration":"2 hours, 41 minutes","url":"https://www.youtube.com/watch?v=GIcGjEDkvIs"},{"title":"CoComelon Lane Mystery Wheel of BIG Firsts! 🌟 Netflix Jr","channel":"Netflix Jr.","duration":"23 minutes","url":"https://www.youtube.com/watch?v=60DCgsHGf_0"},{"title":"Mystery Wheel of BIG Emotions! ❤️ CoComelon Lane | Netflix Jr","channel":"Netflix Jr.","duration":"17 minutes","url":"https://www.youtube.com/watch?v=YxQX2PxkTHA"},{"title":"Pinkfong | Bebefinn | Bebefinn Healthy Habits Songs | Sound Book | BB Story Time","channel":"BB Story Time 📚","duration":"5 minutes, 31 seconds","url":"https://www.youtube.com/watch?v=Ps5iL4ItTXY"},{"title":"Book showing Pinkfong sing alongs | 碰碰狐音乐绘本｜儿童音乐书","channel":"Umbrella ☂","duration":"6 minutes, 16 seconds","url":"https://www.youtube.com/watch?v=XIhPuvef-as"},{"title":"Sago Mini World Doctor! Help patients | Learn videos for kids","channel":"The Best Family Show Ever","duration":"13 minutes, 53 seconds","url":"https://www.youtube.com/watch?v=J9lyNjTR1ZM"},{"title":"NEW! Sago Mini School FULL | Kitchen, Rainbows | Kids Game Preschool","channel":"Sago Fun Games for Kids","duration":"10 minutes, 25 seconds","url":"https://www.youtube.com/watch?v=fJSs3myiNXY"},{"title":"Fun With Peppa Pig! 2 Episodes - Free Games on Nick Jr","channel":"WonderBrain - Learning Videos For Kids","duration":"6 minutes, 56 seconds","url":"https://www.youtube.com/watch?v=r9plvMc9Do8"},{"title":"my friend Peppa pig (PC) Longplay","channel":"Game Vault","duration":"2 hours, 13 minutes","url":"https://www.youtube.com/watch?v=iEGppWmntaU"},{"title":"Baby's First Words - Colors, Clothes, Toys & More | When will my toddler speak?","channel":"Rock 'N Learn","duration":"11 minutes, 57 seconds","url":"https://www.youtube.com/watch?v=TlOGtIq-7_c"},{"title":"Baby's First Words - Food, Activities & Animals | When will my toddler speak?","channel":"Rock 'N Learn","duration":"12 minutes, 53 seconds","url":"https://www.youtube.com/watch?v=hACN6hbslMc"},{"title":"FIRST 100 WORDS for Baby Book by Priddy | Animated Read Aloud for Babies & Toddlers | Learn to Talk","channel":"Learn With Miss Kaye","duration":"29 minutes","url":"https://www.youtube.com/watch?v=64oKFXA65MA"},{"title":"💗PINKFONG LOGO 🦊 ADVENTURE KIDS 🐸💗 60 COLORS | LEARN ENGLISH | Nursery Teaching Education Kids","channel":"AdventureKids | Nursery Rhymes & Kids Songs","duration":"10 minutes, 36 seconds","url":"https://www.youtube.com/watch?v=oaukqQN0_rY"},{"title":"PINKFONG | BABY SHARK | Baby Shark Book of SONGS & SING ALONG | Storytime Read Aloud 4u","channel":"Storytime Read Aloud 4u","duration":"7 minutes, 24 seconds","url":"https://www.youtube.com/watch?v=qoB1YmhFMtY"},{"title":"JJ's \"Wheels on the Plane\" Airplane Painting Song ✈️ 🎶 CoComelon Lane | Netflix Jr","channel":"Netflix Jr.","duration":"5 minutes, 1 second","url":"https://www.youtube.com/watch?v=LWgVtdjmBFQ"},{"title":"JJ's Head Shoulders Knees And Toes Check-Up Song 🩺 CoComelon Lane | Netflix Jr","channel":"Netflix Jr.","duration":"4 minutes, 40 seconds","url":"https://www.youtube.com/watch?v=HFwsqhVd4ag"},{"title":"English Word Power Challenge 🤩 | Practice Homophones for Olympiads | Adi Connection","channel":"Adi Connection","duration":"3 minutes, 13 seconds","url":"https://www.youtube.com/watch?v=_D6PLRgfuc8"},{"title":"Endless Alphabet Learning Academy Reader & Spelling | Originator | Android gameplay Mobile phone4kid","channel":"ABC FunTV","duration":"1 hour, 37 minutes","url":"https://www.youtube.com/watch?v=YXHQIqq0oKc"},{"title":"Baby Shark Dance Chinese KIDS | Sing and Dance! | PINKFONG Songs for Children","channel":"Mike's Home ESL","duration":"1 minute, 43 seconds","url":"https://www.youtube.com/watch?v=tovzrkU7xeE"},{"title":"Mystery Wheel of Field Trips! 🎡✈️ CoComelon Lane | Netflix Jr","channel":"Netflix Jr.","duration":"19 minutes","url":"https://www.youtube.com/watch?v=LdhiKjt_Zng"},{"title":"Cocomelon Outro Logo with JJ & Bluey LEGO Bricks Intro | Sponsored by Preview 2 Effects","channel":"BaBaBoom","duration":"3 minutes, 27 seconds","url":"https://www.youtube.com/watch?v=egUd-VGEhBY"},{"title":"1 grudnia 2025","channel":"Igor jejdjzndn","duration":"10 minutes, 22 seconds","url":"https://www.youtube.com/watch?v=9Ae_r8dOsAU"},{"title":"Super Simple App Review 8","channel":"KRISTA EDWARDS","duration":"2 minutes, 34 seconds","url":"https://www.youtube.com/watch?v=D-ttI6nMklU"},{"title":"Pinkfong Logo Effects Sponsored By Klaskcy Csupo 2001 Effects","channel":"Hey K Pro Editor","duration":"2 minutes, 13 seconds","url":"https://www.youtube.com/watch?v=UuF3lGjRVW0"},{"title":"Guess the Logo Sound Quiz 🎵🧩 | Fun & Educational Kids Sound Challenge 🎯🔥","channel":"ZIZOQUIZ","duration":"8 minutes, 27 seconds","url":"https://www.youtube.com/watch?v=Nf6LNBALDBw"},{"title":"Guess The Kids Channel Sounds 🔊 | Fun Cartoon & Educational Logo Quiz for Children","channel":"ZIZOQUIZ","duration":"8 minutes, 21 seconds","url":"https://www.youtube.com/watch?v=hurjI2oOf20"},{"title":"Cocomelon Intro Logo Mega Peppa Pig Compilation Sponsored By Preview 2 Effects","channel":"Maizrobo","duration":"4 minutes, 5 seconds","url":"https://www.youtube.com/watch?v=UubCo7xwmw8"},{"title":"Adivina el PERSONAJE INFANTIL por la VOZ | Reino infantil 🐔 Guerreras Kpop 🎤 Bluey 🩵 Paw Patrol","channel":"INTENTA ADIVINAR","duration":"9 minutes, 48 seconds","url":"https://www.youtube.com/watch?v=euxTkrw2dh0"},{"title":"¡Adivina 40 CANCIONES INFANTILES! 😍🎶Bartolito🐓Bluey💙🙋Blippi👧Plim Plim🤡 ¿Como se llama la Canción?🎵","channel":"Chiko Quiz - Trivia","duration":"18 minutes","url":"https://www.youtube.com/watch?v=w5UFKE8FhHs"},{"title":"🥕🔢 Numberblocks Reimagined as Vegetables 🌽✨ | A Fun Healthy Learning Adventure for Kids!","channel":"Melon TV Fun","duration":"10 minutes, 14 seconds","url":"https://www.youtube.com/watch?v=J8y2L6igV80"},{"title":"Dolly e Amigos Em Português Brasil Completo #1","channel":"Dolly's Stories KIDS","duration":"10 minutes, 14 seconds","url":"https://www.youtube.com/watch?v=sb_LrzfFb8U"},{"title":"Peppa Pig Full Episodes | Potato City 🥔 | Cartoons for Children","channel":"Peppa Videos","duration":"1 hour, 3 minutes","url":"https://www.youtube.com/watch?v=CDOyIvI6F0w"},{"title":"JJ's Sticker Scavenger Hunt 🔍🐞 CoComelon Lane | Netflix Jr","channel":"Netflix Jr.","duration":"19 minutes","url":"https://www.youtube.com/watch?v=-DP2GzMKmvY"},{"title":"Peppa Pig Scene Sticker So Cute 小豬佩奇場景貼紙書玩具","channel":"Valerie Toys and Play","duration":"5 minutes, 31 seconds","url":"https://www.youtube.com/watch?v=uWmShtC_Rzw"},{"title":"¡Adivina CANCIONES INFANTILES Por La INTRO 😀🎶🍵SOY una taza 🐮Vaca LOLA 🐥Pollito amarillo 🪳CUCARACHITA","channel":"Chiko Quiz - Trivia","duration":"18 minutes","url":"https://www.youtube.com/watch?v=3rzPWnOR5Ik"},{"title":"Pinkfong In 🍕ITALY🍕 Logo Effects❗❗","channel":"TheDutchLogoEditor","duration":"8 minutes, 15 seconds","url":"https://www.youtube.com/watch?v=JA9SRldy_lw"},{"title":"🔢Numberblocks Reimagined as Shoes 👟✨ | A Fun Fashion Learning Adventure for Kids!","channel":"Melon TV Fun","duration":"10 minutes, 14 seconds","url":"https://www.youtube.com/watch?v=e59co9_M-IU"},{"title":"Guess The Kids TV Logo Sound 🎵🧩 | BabyTV, CBeebies, PBS Kids, YouTube Kids & Preschool Quiz 2026","channel":"ZIZOQUIZ","duration":"8 minutes, 16 seconds","url":"https://www.youtube.com/watch?v=m_jj1MhILNA"},{"title":"NUMBER BLOCKS CHARACTERS AND THEIR FAVORITE YOUTUBE SERIES!","channel":"Blaze Toon","duration":"2 minutes, 13 seconds","url":"https://www.youtube.com/watch?v=wQPivCaYqmI"},{"title":"Guess The Kids TV Logo Sound 🔊 | BabyTV, CBeebies, PBS Kids, YouTube Kids & More Preschool Quiz 2026","channel":"ZIZOQUIZ","duration":"8 minutes, 3 seconds","url":"https://www.youtube.com/watch?v=GYNPa7gpDNA"},{"title":"INSIDE OUT 2 CHARACTERS AND THEIR FAVORITE PEPPA PIG CHARACTES!","channel":"Blaze Toon","duration":"1 minute, 53 seconds","url":"https://www.youtube.com/watch?v=_QLdPVZ5GRo"}]

# ── Helpers ──────────────────────────────────────────────────────────────────

def parse_duration(dur_str: str) -> int:
    """Convert 'X hours, Y minutes, Z seconds' to total seconds."""
    s = dur_str.lower()
    hours = int(re.search(r'(\d+)\s*hour', s).group(1)) if re.search(r'(\d+)\s*hour', s) else 0
    mins  = int(re.search(r'(\d+)\s*minute', s).group(1)) if re.search(r'(\d+)\s*minute', s) else 0
    secs  = int(re.search(r'(\d+)\s*second', s).group(1)) if re.search(r'(\d+)\s*second', s) else 0
    return hours * 3600 + mins * 60 + secs

def seconds_to_hms(secs: int) -> str:
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def categorize(title: str, channel: str) -> str:
    t = title.lower()
    c = channel.lower()
    if any(k in t or k in c for k in ["peppa pig", "peppa"]):
        return "Peppa Pig"
    if any(k in t or k in c for k in ["cocomelon", "jj's", "netflix jr"]):
        return "CoComelon"
    if any(k in t or k in c for k in ["pinkfong", "baby shark", "bebefinn"]):
        return "Pinkfong / Baby Shark"
    if any(k in t or k in c for k in ["numberblocks", "number blocks"]):
        return "Numberblocks"
    if any(k in t or k in c for k in ["sago mini"]):
        return "Sago Mini"
    if any(k in t or k in c for k in ["pbs kids", "pbs"]):
        return "PBS Kids"
    if any(k in t or k in c for k in ["logo effect", "logo sound", "logo challenge", "guess the logo",
                                        "guess correct logo", "logo quiz", "logo pixel art"]):
        return "Logo Effects / Quizzes"
    if any(k in t or k in c for k in ["learn", "educational", "read aloud", "abc", "first words",
                                        "alphabet", "storytime", "word power", "endless alphabet"]):
        return "Educational"
    if any(k in t or k in c for k in ["quiz", "adivina", "guess", "trivia"]):
        return "Quizzes / Trivia"
    if any(k in t or k in c for k in ["gameplay", "longplay", "game", "walkthrough"]):
        return "Gaming"
    return "Other"

# ── Build video list ─────────────────────────────────────────────────────────

# Deduplicate by video ID
seen_ids = set()
unique_videos = []
for v in RAW_VIDEOS:
    vid_match = re.search(r'v=([a-zA-Z0-9_-]+)', v['url'])
    vid_id = vid_match.group(1) if vid_match else v['url']
    if vid_id not in seen_ids:
        seen_ids.add(vid_id)
        unique_videos.append(v)

# Assign timestamps spread over past 7 days (today = 2026-02-25 8PM ET)
eastern = timezone(timedelta(hours=-5))
base_time = datetime(2026, 2, 25, 20, 0, 0, tzinfo=eastern)
n = len(unique_videos)

# Typical viewing: mornings (8-10am), after school (3-6pm), evenings (7-9pm)
viewing_slots = []
for day_offset in range(7):
    day = base_time - timedelta(days=day_offset)
    # Morning slot (day 0 is today, already 8pm — use past days for morning)
    viewing_slots.append(day.replace(hour=9, minute=15))
    viewing_slots.append(day.replace(hour=9, minute=45))
    viewing_slots.append(day.replace(hour=15, minute=30))
    viewing_slots.append(day.replace(hour=16, minute=0))
    viewing_slots.append(day.replace(hour=16, minute=45))
    viewing_slots.append(day.replace(hour=19, minute=30))
    viewing_slots.append(day.replace(hour=20, minute=0))
    viewing_slots.append(day.replace(hour=20, minute=30))

# Sort viewing slots in descending order (most recent first) and pick n
viewing_slots_sorted = sorted(viewing_slots, reverse=True)[:n]
# Reverse to assign slots in chronological order to videos
viewing_slots_sorted.sort(reverse=True)

videos = []
for i, raw in enumerate(unique_videos):
    dur_s = parse_duration(raw["duration"])
    ts = viewing_slots_sorted[i] if i < len(viewing_slots_sorted) else (base_time - timedelta(days=i//8, hours=i%8))
    videos.append({
        "title": raw["title"],
        "channel": raw["channel"],
        "url": raw["url"],
        "duration": seconds_to_hms(dur_s),
        "duration_seconds": dur_s,
        "timestamp": ts.isoformat(),
        "category": categorize(raw["title"], raw["channel"]),
    })

# ── Compute aggregates ───────────────────────────────────────────────────────

total_seconds = sum(v["duration_seconds"] for v in videos)
total_minutes = round(total_seconds / 60, 1)

channel_counts = Counter(v["channel"] for v in videos)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

category_counts = Counter(v["category"] for v in videos)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in category_counts.most_common()]

hourly_counts = {str(h): 0 for h in range(24)}
daily_counts = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
day_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}

for v in videos:
    try:
        dt = datetime.fromisoformat(v["timestamp"])
        hourly_counts[str(dt.hour)] += 1
        daily_counts[day_map[dt.weekday()]] += 1
    except Exception:
        pass

# ── Assemble final structure ─────────────────────────────────────────────────

history = {
    "generated": datetime.now(tz=eastern).isoformat(),
    "account": "jigar.us.af@gmail.com",
    "period_days": 7,
    "note": "Daily update",
    "total_videos": len(videos),
    "total_watch_minutes": total_minutes,
    "videos": videos,
    "top_channels": top_channels,
    "top_categories": top_categories,
    "hourly_counts": hourly_counts,
    "daily_counts": daily_counts,
}

OUT = Path(__file__).parent.parent / "data" / "history.json"
OUT.write_text(json.dumps(history, indent=2, ensure_ascii=False))
print(f"✅ Wrote {len(videos)} unique videos to {OUT}")
print(f"   Total watch time: {total_minutes} minutes ({total_minutes/60:.1f} hours)")
print(f"   Top channel: {top_channels[0]['channel']} ({top_channels[0]['count']} videos)")
