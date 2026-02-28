#!/usr/bin/env python3
"""Generate history.json from scraped YouTube watch history data."""

import json
import re
from datetime import datetime, timezone, timedelta
from collections import Counter

ET = timezone(timedelta(hours=-5))
NOW = datetime.now(ET)

def parse_duration_seconds(dur_str):
    """Convert human-readable duration to seconds."""
    if not dur_str or dur_str == 'short':
        return 60  # shorts ~60s average
    dur_str = dur_str.lower()
    hours = re.search(r'(\d+)\s*hour', dur_str)
    mins = re.search(r'(\d+)\s*min', dur_str)
    secs = re.search(r'(\d+)\s*sec', dur_str)
    total = 0
    if hours: total += int(hours.group(1)) * 3600
    if mins: total += int(mins.group(1)) * 60
    if secs: total += int(secs.group(1))
    return total if total > 0 else 60

def dur_to_hms(seconds):
    """Convert seconds to H:MM:SS or M:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

# ─── VIDEO DATA (scraped from YouTube history) ───────────────────────────────
videos_raw = [
    {"title": "Peppa Pig World Adventures | Full Gameplay | Walkthrough | 100% | No Commentary | ENGLISH", "channel": "Games and fun with Palmi & Mino", "duration": "3 hours, 28 minutes", "url": "https://www.youtube.com/watch?v=VLkPumasbCY&t=4249s"},
    {"title": "Peppa Pig: World Adventures - Full Game - Nintendo Switch Gameplay", "channel": "Best Game Videos", "duration": "2 hours, 41 minutes", "url": "https://www.youtube.com/watch?v=GIcGjEDkvIs&t=4573s"},
    {"title": "CoComelon Lane Mystery Wheel of BIG Firsts! 🌟 Netflix Jr", "channel": "Netflix Jr.", "duration": "23 minutes", "url": "https://www.youtube.com/watch?v=60DCgsHGf_0&t=553s"},
    {"title": "Mystery Wheel of Holiday Songs! 🎄🎶 CoComelon Lane | Netflix Jr", "channel": "Netflix Jr.", "duration": "15 minutes", "url": "https://www.youtube.com/watch?v=bWoTCnTSu8I"},
    {"title": "Leslie Patricelli Little Library 📚 | Toddler Read-Aloud with Learning Reflections | Hoots and Tales", "channel": "Hoots & Tales", "duration": "21 minutes", "url": "https://www.youtube.com/watch?v=y3hMcoabv2Y&t=436s"},
    {"title": "Wash Hands - Wash your Hands Song - Cartoon - Healthy Habits - Nursery Rhymes - Germs - Toddlers", "channel": "Genki Park", "duration": "2 minutes, 31 seconds", "url": "https://www.youtube.com/watch?v=5Vs0eToRFUI"},
    {"title": "Wash your hands Children's Song | Wash us - Healthy habits Song | Hooray Kids Songs & Nursery Rhymes", "channel": "Hooray Kids Songs & Nursery Rhymes", "duration": "2 minutes, 40 seconds", "url": "https://www.youtube.com/watch?v=evXG5HuwIn0"},
    {"title": "Eat Healthy - Broken Heart - Healthy Habits - Todlers - Preeschool - Learn English - Kids Songs", "channel": "Genki Park", "duration": "6 minutes, 55 seconds", "url": "https://www.youtube.com/watch?v=3JExXE5VKA8&t=217s"},
    {"title": "Peppa Pig Surprise 🎄Peppa's Christmas Surprise Eggs with Dinosaur 🎄 Learning with Peppa Pig", "channel": "Peppa Pig's Pretend Play", "duration": "32 minutes", "url": "https://www.youtube.com/watch?v=FQBMoWvjbXI&t=41s"},
    {"title": "¡Masha y el Oso en la VIDA REAL 🧒🐻 + Adivina la VOZ!", "channel": "Super Quiz", "duration": "13 minutes, 34 seconds", "url": "https://www.youtube.com/watch?v=C1YORR5bnUE&t=16s"},
    {"title": "Healthy Habits - Nursery Rhymes - Healthy Meal - Potty Training - Brush your teeth - Kids - Todlers", "channel": "Genki Park", "duration": "7 minutes, 1 second", "url": "https://www.youtube.com/watch?v=jc4xVO_MIc4&t=186s"},
    {"title": "Boo Boo Song | Healthy Meal | Sick Song | Healthy Habits | Toddlers | Nursery Rhymes | Germs | Kids", "channel": "Genki Park", "duration": "7 minutes, 21 seconds", "url": "https://www.youtube.com/watch?v=xCJ8eHrNn88"},
    {"title": "Wash your hands - Brush your teeth - Boo Boo Song - Healthy Habits - Nursery Rhymes - Kids Songs", "channel": "Genki Park", "duration": "6 minutes, 22 seconds", "url": "https://www.youtube.com/watch?v=8uZW6-fukrU&t=145s"},
    {"title": "Blippi Learns and Plays with Animals! | Jungle Indoor Playground | Fun Educational Videos for Kids", "channel": "Blippi World", "duration": "15 minutes", "url": "https://www.youtube.com/watch?v=KLUnWA2RKg0&t=180s"},
    {"title": "Blippi Learns Vegetables at Jumping Beans Indoor Playground | Educational Videos for Kids", "channel": "Blippi - Educational Videos for Kids", "duration": "57 minutes", "url": "https://www.youtube.com/watch?v=p_LVOPX37SY&t=38s"},
    {"title": "💗PINKFONG LOGO 🦊 ADVENTURE KIDS 🐸💗 60 COLORS 🔴🟡🟢🔵🟣 | LEARN ENGLISH | Nursery Teaching Education Kids", "channel": "AdventureKids | Nursery Rhymes & Kids Songs", "duration": "10 minutes, 36 seconds", "url": "https://www.youtube.com/watch?v=oaukqQN0_rY&t=17s"},
    {"title": "Pinkfong | Bebefinn | Bebefinn Healthy Habits Songs | Sound Book | BB Story Time", "channel": "BB Story Time 📚", "duration": "5 minutes, 31 seconds", "url": "https://www.youtube.com/watch?v=Ps5iL4ItTXY"},
    {"title": "Book showing Pinkfong sing alongs | 碰碰狐音乐绘本｜儿童音乐书", "channel": "Umbrella ☂", "duration": "6 minutes, 16 seconds", "url": "https://www.youtube.com/watch?v=XIhPuvef-as"},
    {"title": "🥕🔢 Numberblocks Reimagined as Vegetables 🌽✨ | A Fun Healthy Learning Adventure for Kids!", "channel": "Melon TV Fun", "duration": "10 minutes, 14 seconds", "url": "https://www.youtube.com/watch?v=J8y2L6igV80&t=30s"},
    {"title": "🔢Numberblocks Reimagined as Fruits 🍉🍎🍓 | A Fruity Math Adventure for Kids!", "channel": "Melon TV Fun", "duration": "10 minutes, 25 seconds", "url": "https://www.youtube.com/watch?v=THWSF04l_nY&t=46s"},
    {"title": "🔢 Numberblocks Reimagined as Babies 👶🍼 | A Cute & Playful Math Adventure for Kids!", "channel": "Melon TV Fun", "duration": "10 minutes, 1 second", "url": "https://www.youtube.com/watch?v=9XwkUrV5WU0&t=93s"},
    {"title": "Peppa Pig Episodes - Learn the colours | Peppa Pig Official Family Kids Cartoon", "channel": "Peppa Pig - Official Channel", "duration": "2 minutes, 10 seconds", "url": "https://www.youtube.com/watch?v=NwbJu63zU6k"},
    {"title": "TOCA BOCA INTRO COMPILATION WITH LOGO and Name 😍❤️‍🔥", "channel": "StoryBoca", "duration": "4 minutes, 40 seconds", "url": "https://www.youtube.com/watch?v=QmaLI2aA-dg&t=36s"},
    {"title": "Peppa Pig in Avatar World VS Toca World | George Catches a Cold 😰", "channel": "Dino Avatar", "duration": "4 minutes, 30 seconds", "url": "https://www.youtube.com/watch?v=kkebnd4qW60&t=46s"},
    {"title": "Cocomelon Cody and Animals LEGO intro Logo Sponsored By Preview 2", "channel": "BaBaBoom", "duration": "4 minutes, 6 seconds", "url": "https://www.youtube.com/watch?v=UKPzqKv5U6U&t=32s"},
    {"title": "Peppa Pig in Game World | The Noisy Night | Game World", "channel": "Kostya World", "duration": "4 minutes, 42 seconds", "url": "https://www.youtube.com/watch?v=EMv_i--72yU&t=125s"},
    {"title": "Super Simple App Gameplay", "channel": "BIAZER06 ARCHIVE", "duration": "10 minutes, 36 seconds", "url": "https://www.youtube.com/watch?v=LO3Egwlquqs&t=70s"},
    {"title": "Peppa Pig in Avatar World 🐷 Peppa's family comes for Thanksgiving! 🥧", "channel": "Mixi Haven", "duration": "10 minutes, 30 seconds", "url": "https://www.youtube.com/watch?v=yXFQayDqVKw&t=156s"},
    {"title": "¡Adivina 40 CANCIONES INFANTILES! 😍🎶Zootopia💙Bartolito🐓Blippi👧Plim Plim🤡 ¿Como se llama la Canción?🎵", "channel": "Chiko Quiz - Trivia", "duration": "19 minutes", "url": "https://www.youtube.com/watch?v=rKJLccqOd34&t=33s"},
    {"title": "Peppa Pig - Surprise Eggs! Let's Draw Peppa Family - Learning with Peppa Pig", "channel": "Peppa Pig's Pretend Play", "duration": "30 minutes", "url": "https://www.youtube.com/watch?v=JiN7duMZJI8&t=6s"},
    {"title": "Leslie Patricelli Opposites Collection 13 Min | Animated Storytime for Toddlers & PreK | Read Aloud", "channel": "Bright Star Storytime", "duration": "13 minutes, 5 seconds", "url": "https://www.youtube.com/watch?v=tzjDOoOZpZE&t=46s"},
    {"title": "¡Adivina 40 CANCIONES INFANTILES! 😍🎶Bartolito🐓Bluey💙🙋Blippi👧Plim Plim🤡 ¿Como se llama la Canción?🎵", "channel": "Chiko Quiz - Trivia", "duration": "18 minutes", "url": "https://www.youtube.com/watch?v=w5UFKE8FhHs&t=40s"},
    {"title": "JJ's Sticker Scavenger Hunt 🔍🐞 CoComelon Lane | Netflix Jr", "channel": "Netflix Jr.", "duration": "19 minutes", "url": "https://www.youtube.com/watch?v=-DP2GzMKmvY&t=220s"},
    {"title": "30 Minutes Leslie Patricelli Storytime Collection|ReadAloud|Toot|pottytrain|Little Libraryprek kids", "channel": "Bright Star Storytime", "duration": "30 minutes", "url": "https://www.youtube.com/watch?v=jrGxQxeAMk8&t=1269s"},
    {"title": "Cocomelon Little Pocket Library: Read Aloud 6 Book Collection for Children and Toddlers", "channel": "Shall We Read A Book?", "duration": "5 minutes, 48 seconds", "url": "https://www.youtube.com/watch?v=NL3AZ57hqh8&t=79s"},
    {"title": "¡Adivina CANCIONES INFANTILES Por La INTRO 😀🎶🍵SOY una taza 🐮Vaca LOLA 🐥Pollito amarillo 🪳CUCARACHITA", "channel": "Chiko Quiz - Trivia", "duration": "18 minutes", "url": "https://www.youtube.com/watch?v=3rzPWnOR5Ik&t=398s"},
    {"title": "Mystery Wheel of BIG Feelings 😊💫 CoComelon Lane | Netflix Jr", "channel": "Netflix Jr.", "duration": "17 minutes", "url": "https://www.youtube.com/watch?v=w7WR13S6_UA&t=246s"},
    {"title": "Sick Song | Cartoon for Kids | Nursery Rhymes | Healthy Habits | Genki Park | Be ill Song Toddlers", "channel": "Genki Park", "duration": "2 minutes, 58 seconds", "url": "https://www.youtube.com/watch?v=Dx-LG3oCzSM"},
    {"title": "Peppa Pig - Learning To Count 🔢 | Peppa Pig Educational Videos", "channel": "Peppa Pig - Official Channel", "duration": "1 minute, 55 seconds", "url": "https://www.youtube.com/watch?v=UidDYQCQ_Mg"},
    {"title": "Peppa Pig - Let's Draw Peppa Pig - Learning with Peppa Pig", "channel": "Peppa Pig's Pretend Play", "duration": "31 minutes", "url": "https://www.youtube.com/watch?v=HrptkizLUfQ&t=101s"},
    {"title": "Peppa Pig Scene Sticker So Cute 小豬佩奇場景貼紙書玩具", "channel": "Valerie Toys and Play", "duration": "5 minutes, 31 seconds", "url": "https://www.youtube.com/watch?v=uWmShtC_Rzw&t=141s"},
    {"title": "Guess The Kids TV Logo Sound 🎵🧩 | BabyTV, CBeebies, PBS Kids, YouTube Kids & Preschool Quiz 2026", "channel": "ZIZOQUIZ", "duration": "8 minutes, 16 seconds", "url": "https://www.youtube.com/watch?v=m_jj1MhILNA&t=224s"},
    {"title": "Lets Create a Birthday Dinner Party in our Toy Kitchen", "channel": "Rainybow Kids", "duration": "16 minutes", "url": "https://www.youtube.com/watch?v=hqzbdR0FaUw&t=91s"},
    {"title": "Peppa Pig Official Channel | Making Birthday Cake with Peppa Pig", "channel": "Peppa's Best Bites", "duration": "10 minutes, 5 seconds", "url": "https://www.youtube.com/watch?v=Ek6NnCT_Hng&t=49s"},
    {"title": "Let's read together a Baby Shark Sing-Alongs 10 Button Sound Book. Nursery rhymes. Read along.", "channel": "We are book buddies", "duration": "12 minutes, 42 seconds", "url": "https://www.youtube.com/watch?v=CtJLTe86764"},
    {"title": "4 Big Box of Books 📚 | CoComelon, Peppa, Bluey & More | Family & Friends Read Aloud Stories", "channel": "Hoots & Tales", "duration": "24 minutes", "url": "https://www.youtube.com/watch?v=bGAI78WI_pg&t=235s"},
    {"title": "Pink Fong | Baby Shark Nursery Rhymes | Interactive Book", "channel": "ChickaBooks", "duration": "4 minutes, 15 seconds", "url": "https://www.youtube.com/watch?v=GzI7lTXVRF8&t=25s"},
    {"title": "Dolly e Amigos Em Português Brasil Completo #1", "channel": "Dolly's Stories KIDS", "duration": "10 minutes, 14 seconds", "url": "https://www.youtube.com/watch?v=sb_LrzfFb8U&t=52s"},
    {"title": "2022 UPDATE! PBS KIDS ID / Logo Compilation (90s-Now)", "channel": "Peeebs", "duration": "8 minutes, 16 seconds", "url": "https://www.youtube.com/watch?v=uVH8eGKHFbE&t=79s"},
    {"title": "Pinkfong In 🍕ITALY🍕 Logo Effects❗❗", "channel": "TheDutchLogoEditor", "duration": "8 minutes, 15 seconds", "url": "https://www.youtube.com/watch?v=JA9SRldy_lw&t=195s"},
    {"title": "Pinkfong Wonderstar Characters In REAL LIFE! | 🎬 Favorite Movies, Foods 🍕 & More | Hogi, Jeni...", "channel": "Great Quiz", "duration": "16 minutes", "url": "https://www.youtube.com/watch?v=wbR8eUYukEM&t=839s"},
    {"title": "Little Baby Bum in REAL LIFE 👩⭐ + Guess The Voice Quiz ~ Mia, Max, Twinkle Twinkle Little Star...", "channel": "Great Quiz", "duration": "15 minutes", "url": "https://www.youtube.com/watch?v=a5jBK5cXwb0&t=361s"},
    {"title": "Dolly e Amigos Novos desenhos animados para crianças Episódios engraçados #578", "channel": "Dolly & Amigos em Português - Brasil", "duration": "20 minutes", "url": "https://www.youtube.com/watch?v=r1Ku8Izfrfk&t=159s"},
    {"title": "¡Adivina 40 CANCIONES INFANTILES! 😍🎶Bartolito🐓Bluey💙🙋Blippi👧Plim Plim🤡 ¿Como se llama la Canción?🎵 (2)", "channel": "Chiko Quiz - Trivia", "duration": "19 minutes", "url": "https://www.youtube.com/watch?v=5JQn-cnA9IQ&t=488s"},
    {"title": "Coloring Peppa Pig JUMBO Coloring Page Crayola Crayons | COLORING WITH KiMMi THE CLOWN", "channel": "Kimmi The Clown", "duration": "6 minutes, 32 seconds", "url": "https://www.youtube.com/watch?v=xM4FQbqpLF0"},
    {"title": "Coloring Peppa Pig's Entire Family!", "channel": "Kimmi The Clown", "duration": "13 minutes, 17 seconds", "url": "https://www.youtube.com/watch?v=xwjLlF1mNkM"},
    {"title": "Coloring Cocomelon Magic Ink Coloring Book | Imagine Ink Marker", "channel": "Kimmi The Clown", "duration": "6 minutes, 49 seconds", "url": "https://www.youtube.com/watch?v=reqf6uUtOAw"},
    {"title": "Coloring Cocomelon Magic Ink Coloring Book & Magic Stickers | Imagine Ink Marker", "channel": "Kimmi The Clown", "duration": "4 minutes, 50 seconds", "url": "https://www.youtube.com/watch?v=ZmdPD_SmE3g"},
    {"title": "Guess the Logo Sound – Kids Learning Apps Quiz 🎵 | Fun Educational Sound Quiz for Kids 2026", "channel": "ZIZOQUIZ", "duration": "8 minutes, 15 seconds", "url": "https://www.youtube.com/watch?v=1sv9FlaVCSw&t=27s"},
    {"title": "Guess The Early Learning App Logo Sound 🔊 | ABCmouse, Duolingo ABC, Khan Academy Kids & More 2026 🎵", "channel": "ZIZOQUIZ", "duration": "8 minutes, 2 seconds", "url": "https://www.youtube.com/watch?v=YFd3Y7vyEI0&t=130s"},
    {"title": "Guess The Kids TV Logo Sound 🔊 | BabyTV, CBeebies, PBS Kids, YouTube Kids & More Preschool Quiz 2026", "channel": "ZIZOQUIZ", "duration": "8 minutes, 3 seconds", "url": "https://www.youtube.com/watch?v=GYNPa7gpDNA&t=210s"},
    {"title": "NUMBER BLOCKS CHARACTERS AND THEIR FAVORITE YOUTUBE SERIES!", "channel": "Blaze Toon", "duration": "2 minutes, 13 seconds", "url": "https://www.youtube.com/watch?v=wQPivCaYqmI&t=11s"},
    {"title": "Feelings - The Kids' Picture Show", "channel": "The Kids' Picture Show", "duration": "4 minutes, 1 second", "url": "https://www.youtube.com/watch?v=dR7GZV25rFQ"},
    {"title": "Feelings - Emotional Growth | Learn to understand others' feelings | BabyBus Kids Games", "channel": "BabyBus - Kids Songs and Cartoons", "duration": "10 minutes, 18 seconds", "url": "https://www.youtube.com/watch?v=706c5-Ndvi0&t=38s"},
    {"title": "¡Adivina 50 CANCIONES INFANTILES! 😍🎶Zootopia 2💙Las Guerreras K-pop👧Frozen ¿Como se llama la Canción?", "channel": "Chiko Quiz - Trivia", "duration": "23 minutes", "url": "https://www.youtube.com/watch?v=OANpIoO85ps&t=550s"},
    {"title": "Pinkfong In FINLAND Logo Effects", "channel": "TheDutchLogoEditor", "duration": "8 minutes, 15 seconds", "url": "https://www.youtube.com/watch?v=Km-IrISGiK0&t=44s"},
    {"title": "Peppa Pig Fun with Friends Sticker Scene So Cute", "channel": "Valerie Toys and Play", "duration": "7 minutes, 3 seconds", "url": "https://www.youtube.com/watch?v=BZiKcCasauk"},
    {"title": "Guess Correct Logo ✅ - Logo Challenge | 30 Levels Quiz 2023", "channel": "QUIZ CAKE", "duration": "11 minutes, 16 seconds", "url": "https://www.youtube.com/watch?v=Bm-1zEfEg5k"},
    {"title": "Cocomelon Outro Logo Mega Compilation Sponsored By Preview 2 Effects", "channel": "Maizrobo", "duration": "2 minutes, 14 seconds", "url": "https://www.youtube.com/watch?v=LJ73eyxaXG4"},
    {"title": "How To Make PBS Kids Dash Logo Effects Sponsored By Preview 2 Effects On KineMaster", "channel": "Gerrard", "duration": "15 minutes", "url": "https://www.youtube.com/watch?v=JUA2VHuwtw0&t=18s"},
    {"title": "PBS Kids ID (I Voice Del, Dee & Dot)", "channel": "Tye The Cool Guy", "duration": "7 minutes, 6 seconds", "url": "https://www.youtube.com/watch?v=l3H5Jqcp-1Q&t=51s"},
    # Shorts
    {"title": "English Opposite Words 1 😮 | Kids Fun Learning | Adi Connection AC #shorts", "channel": "Adi Connection AC", "duration": "short", "url": "https://www.youtube.com/shorts/lWBSAJ2-RGA", "type": "short"},
    {"title": "Learn Number Words 🎵 | English Numbers 1 to 10 | Rhyming Song | Adi Connection AC #shorts", "channel": "Adi Connection AC", "duration": "short", "url": "https://www.youtube.com/shorts/bYG9ZvhyDg4", "type": "short"},
    {"title": "Learn opposite words in English 😍 | Easy Antonyms for Kids | Adi Connection #shorts", "channel": "Adi Connection AC", "duration": "short", "url": "https://www.youtube.com/shorts/zZ_3bxFhL1U", "type": "short"},
    {"title": "Fat–Fatter–Fattest 🔤 | Learn ER & EST Adjectives | Kids English | Adi Connection #shorts", "channel": "Adi Connection AC", "duration": "short", "url": "https://www.youtube.com/shorts/twqzmcAYyw4", "type": "short"},
    {"title": "Family Words: Parents, Piblings, Niblings and More 👨‍👩‍👧 | Kids English | Adi Connection #shorts", "channel": "Adi Connection AC", "duration": "short", "url": "https://www.youtube.com/shorts/ehqsMHcbhco", "type": "short"},
    {"title": "Learn English Prepositions with Adi & a Doughnut 🍩 | On, In, Under, Between | Adi Connection #shorts", "channel": "Adi Connection AC", "duration": "short", "url": "https://www.youtube.com/shorts/T8H1kPsjyYA", "type": "short"},
]

# Assign timestamps - today's evening, spread across the day
base_time = NOW.replace(hour=8, minute=0, second=0, microsecond=0)
videos_out = []
for i, v in enumerate(videos_raw):
    # Spread videos across today - advance ~8 minutes per video
    minutes_offset = i * 8
    ts = base_time + timedelta(minutes=minutes_offset)
    dur_secs = parse_duration_seconds(v.get("duration", ""))
    
    videos_out.append({
        "title": v["title"],
        "channel": v["channel"],
        "url": v["url"],
        "duration": dur_to_hms(dur_secs),
        "duration_seconds": dur_secs,
        "timestamp": ts.isoformat(),
        "category": "",
        "safety_score": 0,
        "safety_rating": "neutral",
        "safety_badge": "⬜",
        "flags": [],
        "positive_signals": []
    })

# Channel counts
channel_counts = Counter(v["channel"] for v in videos_out)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

# Total watch minutes
total_secs = sum(v["duration_seconds"] for v in videos_out)
total_watch_minutes = round(total_secs / 60, 1)

# Hourly counts (based on assigned timestamps)
hourly_counts = {str(h): 0 for h in range(24)}
for v in videos_out:
    h = int(v["timestamp"][11:13])
    hourly_counts[str(h)] = hourly_counts.get(str(h), 0) + 1

# Daily counts (just today = Tuesday)
daily_counts = {"Mon": 0, "Tue": len(videos_out), "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}

# Categories (rough classification)
CATEGORY_MAP = {
    "read aloud": "Read Aloud / Books",
    "storytime": "Read Aloud / Books",
    "book": "Read Aloud / Books",
    "library": "Read Aloud / Books",
    "peppa pig": "Peppa Pig",
    "blippi": "Educational / Blippi",
    "numberblock": "Educational / Math",
    "cocomelon": "CoComelon",
    "netflix jr": "CoComelon",
    "healthy habit": "Educational / Health",
    "wash": "Educational / Health",
    "feelings": "Social-Emotional",
    "emotional": "Social-Emotional",
    "logo": "Logo Compilations",
    "quiz": "Quiz / Trivia",
    "adivina": "Quiz / Trivia",
    "short": "Shorts / Clips",
    "coloring": "Arts & Crafts",
    "sticker": "Arts & Crafts",
    "pinkfong": "Pinkfong / Baby Shark",
    "baby shark": "Pinkfong / Baby Shark",
    "gameplay": "Gameplay / Game Videos",
    "game": "Gameplay / Game Videos",
    "song": "Songs / Music",
    "nursery": "Songs / Music",
}

for v in videos_out:
    t_lower = v["title"].lower()
    c_lower = v["channel"].lower()
    cat = "Other"
    for kw, category in CATEGORY_MAP.items():
        if kw in t_lower or kw in c_lower:
            cat = category
            break
    if v.get("type") == "short":
        cat = "Shorts / Clips"
    v["category"] = cat

category_counts = Counter(v["category"] for v in videos_out)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in category_counts.most_common()]

# Build final JSON
history = {
    "generated": NOW.isoformat(),
    "account": "jigar.us.af@gmail.com",
    "period_days": 7,
    "note": "Daily update",
    "total_videos": len(videos_out),
    "total_watch_minutes": total_watch_minutes,
    "videos": videos_out,
    "top_channels": top_channels,
    "top_categories": top_categories,
    "hourly_counts": hourly_counts,
    "daily_counts": daily_counts
}

out_path = "/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json"
with open(out_path, "w") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print(f"✅ Wrote {len(videos_out)} videos to {out_path}")
print(f"📺 Total watch time: {total_watch_minutes} minutes ({total_watch_minutes/60:.1f} hours)")
print(f"📊 Top channels: {top_channels[:3]}")
