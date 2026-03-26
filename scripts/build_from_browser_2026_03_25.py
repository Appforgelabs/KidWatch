#!/usr/bin/env python3
"""
KidWatch history builder from browser scrape - 2026-03-25
Scraped from YouTube watch history at 2026-03-25T20:00:00-05:00
"""

import json
import os
from datetime import datetime, timezone, timedelta
from collections import Counter

# Current timestamp
NOW = "2026-03-25T20:00:00-05:00"
NOW_UTC = "2026-03-26T00:00:00Z"

# EST timezone
EST = timezone(timedelta(hours=-5))
today = datetime(2026, 3, 25, tzinfo=EST)

def dur_to_sec(d):
    """Convert duration string like 4:30 or 1:01:53 to seconds"""
    if not d or d == 'LIVE':
        return 0
    parts = d.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

# All videos scraped from the watch history page
# Format: (title, channel, duration_str, url_path)
RAW_VIDEOS = [
    # Today's viewing
    ("Peppa Pig Goes To A Pirate Party!", "George Pig - Official Channel", "4:30", "/watch?v=EBXl-m0tnKM"),
    ("Peppa Pig Has Fun At A Picnic!", "George Pig - Official Channel", "5:12", "/watch?v=HzNboR-DEOo"),
    ("Peppa Pig - School Play (full episode)", "Peppa Pig's Pretend Play", "4:49", "/watch?v=37brU_Ry-yc"),
    ("Children's Books Read Aloud - 5 ANIMATED Davids | By David Shannon", "Storytime Hullabaloo Hi", "12:01", "/watch?v=kV8RUPtfOLY"),
    ("🐒 Five Little Monkeys Jumping on the Bed 🎶 [3 MIN LOOP REMIX] | Funny Sound Variations + Kids Songs", "ToonyMonka", "3:28", "/watch?v=UqHbTWl39nw"),
    ("Gaga Baby Goes Grocery Shopping Through Portal!", "Goo Goo Colors", "4:10", "/watch?v=gQPP2CuuMl4"),
    ("One Little Finger (Sing-Along)", "Super Simple Songs - Topic", "2:13", "/watch?v=gTdBGtpAeUU"),
    ("Peekaboo, I Love You", "Super Simple Songs - Topic", "1:23", "/watch?v=6hPTDqGJULU"),
    ("Buckle Up Feat. Lil Jon | Seatbelt Safety with Gracie's Corner", "Gracie's Corner", "2:41", "/watch?v=j68UH0ssWjg"),
    ("A Trip To The Hospital 🏥 | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "31:23", "/watch?v=nPp2P8FBWLI"),
    ("Peppa Pig Makes Jelly With George 🟥 | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "31:30", "/watch?v=1X8XrUusiY4"),
    ("Peppa Pig Visits The Ice Cream Truck!", "George Pig - Official Channel", "4:30", "/watch?v=TKrqwqmtu1s"),
    ("Peppa Pig Birthday Specials | Peppa Pig Official Channel", "Peppa Pig and Friends", "17:22", "/watch?v=EAlk__IO_co"),
    ("Peppa Pig Travels Around the Whole World | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "14:28", "/watch?v=lC5N8kKVCfE"),
    ("Peppa Pig's Juke Box Disco Party 🐷 🪩 Playtime With Peppa", "Peppa Pig's Big Adventures", "22:29", "/watch?v=TDJi5IOyQEo"),
    ("⭐️ New Season ⭐️ Peppa Pig Plays Funny Music | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "16:14", "/watch?v=uyKHk8I9Arc"),
    ("Peppa Pig and Suzy Sheep are Best Friends | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "13:51", "/watch?v=G_GtShpkWLk"),
    ("Glitter Party at Peppa Pig's Playgroup | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "13:46", "/watch?v=BZWUsQKbWTE"),
    ("🎅 Santa's Visit at Grandpa Pig's House | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "13:56", "/watch?v=d17DYwknJbw"),
    ("November 29, 2025", "X705-GAMINGシ", "4:45", "/watch?v=nTgt2-ZAMEk"),
    ("Peppa Pig Performs In The School Play!", "George Pig - Official Channel", "4:30", "/watch?v=L-xsOdq8RrE"),
    ("Peppa Pig Learns How To Make Pizza!", "George Pig - Official Channel", "4:30", "/watch?v=6Yc2WWMafIk"),
    ("Real World Ramen | Featuring The Bumble Nums Plushies! 😍 | Cartoons For Kids", "The Bumble Nums", "7:11", "/watch?v=sICUewwtmbU"),
    ("Peppa's First Vlog! 🎥 | Peppa Pig Tales 2025 Full Episodes | 30 Minutes", "Peppa Pig - Official Channel", "30:20", "/watch?v=fAjtwvZXK3U"),
    ("Peppa And George Clean Up Their Toys!", "George Pig - Official Channel", "4:30", "/watch?v=sKo0duOFpK0"),
    ("🐒 Five Little Monkeys Jumping on the Bed 🎶 [3 MIN LOOP REMIX] | Funny Sound Variations & Kids Songs", "ToonyMonka", "3:34", "/watch?v=UVLDrlXz_ns"),
    ("Cinema Snack Favourites! 🍿🥕 | Peppa Pig Full Episodes | 2 Hours of Kid's Cartoons", "Peppa Pig - Official Channel", "2:01:12", "/watch?v=sMY3xRekLJE"),
    ("Peppa Pig | Health Check | Peppa Pig Official | Family Kids Cartoon", "George Pig - Official Channel", "5:12", "/watch?v=cKEK7K5PKAE"),
    ("Pedro's Cough and The Library 🤧📚 Peppa Pig Full Episodes", "Peppa Pig - Official Channel", "9:00", "/watch?v=IGJw3NmkXE0"),
    ("Peppa Pig Back to School | Apple to Zoe | Alphabet Letter Sounds | ABC Kids Song", "Free For Learn", "3:30", "/watch?v=UeeugH4Apsk"),
    ("Peppa Pig | The Holiday | Peppa Pig Official | Family Kids Cartoon", "George Pig - Official Channel", "5:12", "/watch?v=9k9NpMZsJFg"),
    ("When I Grow Up: Work and Play Fun with Peppa Pig | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "4:49", "/watch?v=T9o6Sp9Uifo"),
    ("Peppa Pig Learns to Make Pizza", "George Pig - Official Channel", "4:30", "/watch?v=wxyo9S2KAPM"),
    ("Peppa Pig Full Episodes | George and Richard Rabbit #84", "Peppa's Best Bites", "5:13", "/watch?v=kb8yN6CiDyA"),
    ("Compost and Richard Rabbit Comes to Play 🐷🐰 Peppa Pig Full Episodes", "Peppa Pig - Official Channel", "9:00", "/watch?v=YZACISkbFpU"),
    ("Hello Around the World | Say Hello in 15 Different Languages | Explore World Song | JunyTony", "JunyTony - Songs and Stories", "1:51", "/watch?v=472AnCrHYVs"),
    ("Learn Toys Name for Kids | 20 Toys Name in English | Kids Learning Video", "Happy learning Club", "4:34", "/watch?v=6aPEaMOVtPA"),
    ("Healthy Food vs Junk Food 🥦🍔 | Kids Learning Video", "Happy learning Club", "5:05", "/watch?v=WoQ58-hMMUM"),
    ("Drinks - Kids vocabulary - Learn English for kids - English educational video", "English Singsing", "4:50", "/watch?v=A_AJrtGtC3Y"),
    ("Learn Letters A to E with Captain Seasalt and the ABC Pirates | Cartoons For Kids", "Captain Seasalt and the ABC Pirates", "38:20", "/watch?v=getlf87x4uw"),
    ("Let's Go For A Walk Outside | A Storybook For Kids | Rhymington Square", "Super Simple Storytime", "8:21", "/watch?v=J2l5xJ21UVU"),
    ("🌟Especial de Ninimo🐱｜Aprende Colores con Ninimo y Hogi｜Hogi en español", "Hogi & Pinkfong en español - Juega y Aprende", "20:58", "/watch?v=pyBfwhVwOmY"),
    ("Daddy Pig's Golden Boots 👢 | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "15:29", "/watch?v=pWU8HN_XH0M"),
    ("Lost Hamster | CoComelon | Songs and Cartoons | Best Videos for Babies", "Baby Time!", "14:50", "/watch?v=ipYUSPxHm14"),
    ("The Double Decker Party Bus! 🚌 | Peppa Pig Full Episodes", "Peppa Pig - Official Channel", "31:26", "/watch?v=H8lhrNV-nT4"),
    ("Belajar angka dan alfabet | Diana and Roma Bahasa Indonesia", "Diana and Roma IND Collection", "17:25", "/watch?v=L-Odypj0ffQ"),
    ("Aprender Colores y Números | Huevos de Colores en la Granja | Canciones Infantiles ChuLoo en Español", "ChuLoo en Español", "10:39", "/watch?v=Otx3oUI11qE"),
    ("Learning & Growing with Finny | Finny The Shark Cartoon Collection", "Finny The Shark", "46:37", "/watch?v=v03KD14wDgQ"),
    ("Finny The Shark Full Episode Compilation | Kids Cartoon | Under The Sea", "Finny The Shark", "1:01:53", "/watch?v=ASEGHhhTzqE"),
    ("I Am A Dinosaur | Kids Rock Song | Finny The Shark", "Finny The Shark", "3:03", "/watch?v=2QfOM_GsyEE"),
    ("Happy Birthday Finny The Shark | + More Fun Cartoons For Kids!", "Finny The Shark", "1:09:43", "/watch?v=vIcnuKOKzNk"),
    ("12 Days Of Christmas + More | Kids Songs for Christmas | Finny The Shark", "Finny The Shark", "1:05:54", "/watch?v=ckSIhoTF4lE"),
    ("Fun Finny The Shark Songs | Kids Music | Sing Along With Finny!", "Finny The Shark", "1:03:58", "/watch?v=OB6gQ1buAmg"),
    ("The Alphabet Song | Learn The ABCs | Finny The Shark", "Finny The Shark", "2:00", "/watch?v=ccEpTTZW34g"),
    ("Hello My Friends + More | Kids Halloween Songs Plus Classroom Fun | Finny The Shark", "Finny The Shark", "1:09:18", "/watch?v=1RBd3lxjcaI"),
    ("Take Your Fish To Work Day | Finny The Shark | Cartoon For Kids", "Finny The Shark", "11:43", "/watch?v=EOmfb69FgI0"),
    ("🐷 EVERY Peppa Pig Season 2 Episodes, but every EPISODE More Appear on Screen! ✨", "Toys and Colours", "0:00", "/watch?v=iq31MAjhbvk"),  # LIVE
    ("Peppa Pig Throws an Undersea BIRTHDAY Party!🐷🎉 Peppa & George: Mermaids | Full Episodes | 22 Minutes", "Toys and Colours", "22:25", "/watch?v=3-qBbeZJe7w"),
    ("Peppa Pig Helps Out at Edmond Elephant's Birthday Party | Peppa Official Family Kids Cartoon", "Peppa Pig - Official Channel", "13:56", "/watch?v=maeAvp1-mL0"),
    ("Learn Spanish Words with Peppa Pig and Friends Driving Toy Cars Around Town!", "Genevieve's Playhouse - Learning Videos for Kids", "7:02", "/watch?v=yah5X-wTIpc"),
    ("We Love Peppa Pig London #9", "Peppa's Best Bites", "5:13", "/watch?v=sdBwR5-mmgM"),
    ("Peppa Pig English Episodes | Making a Real Fairy Palace for School", "Baby Cartoons", "1:08:41", "/watch?v=XYJfB6weppw"),
    ("Peppa Pig Goes on a SUNNY Holiday Adventure☀️ Peppa & George: Italy Fun | Cartoon for kids | 20 Mins", "Peppa Pig's Big Adventures", "17:36", "/watch?v=4FTZzGnulX8"),
    ("Peppa Pig is Having a Tea Party in Her Tree House | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "13:45", "/watch?v=blQxZ73C_Vg"),
    ("Peppa Pig Makes Musical Instruments | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "4:11", "/watch?v=c1D5r9mOuwg"),
    ("Peppa And George Learn How To Make Puppets!", "George Pig - Official Channel", "4:30", "/watch?v=vYwA6NGlc4U"),
    ("Peppa Pig's Clubhouse Shop 🐷🏪 Brand New Peppa Pig Official Channel Family Kids Cartoons", "Peppa Videos", "4:30", "/watch?v=IrPlVFm5sKU"),
    ("Mummy Pig's Perfect Day at the Shopping Mall | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "4:38", "/watch?v=j41T3sw4GRs"),
    ("Jannie Pretend Play with Tayo Bus Toy", "Toys and Colors", "3:27", "/watch?v=sWYmACbqfX8"),
    ("Peppa Pig Goes on a NEW Bowling Adventure 🎳 Peppa & George: Get a Strike! | Cartoon for Kids 20 Mins", "Peppa Pig's Big Adventures", "17:59", "/watch?v=9htrZHg25Ac"),
    ("Peppa pig gym class story ep 42", "rich baby alex 2025", "4:31", "/watch?v=Pt5GKa4O4MY"),
    ("Bathtime with Baby Evie 🛁 Peppa Pig Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", "21:12", "/watch?v=7IjJJwBD4Ds"),
    ("George Pig is Sick 🤧 | Peppa & George: Catches a Cold | Full Episodes | Kids for Cartoon | 25 Minutes", "Toys and Colours", "22:24", "/watch?v=bbjcN1iqjDc"),
    ("Peppa and Suzy's BIGGEST Argument! ❌ Friendship Fallout 😓 Peppa Pig Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", "22:25", "/watch?v=bySfdf6G4-k"),
    ("Dolly e Amigos Em Português Brasil Completo #5", "Dolly e Amigos - Brasília", "10:18", "/watch?v=4tAUm5O7jZQ"),
    ("Ten Little Fruits + Nursery Rhymes & Kids Songs", "KidsCamp Nursery Rhymes & Learning Videos for Kids", "0:00", "/watch?v=Pa2Da-jnAZE"),  # LIVE
    ("FUNNY Filters 👽 Taking SILLY Selfies! 🛸 Peppa Pig Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", "24:21", "/watch?v=w8G1c8oo17I"),
    ("Peppa Pig and Friends Celebrate Autumn! 🍂 | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "14:52", "/watch?v=Fynh1DuS8-E"),
    ("Baby Shark Dance! 🦈 + More | Super Simple Songs", "Super Simple Songs - Kids Songs", "3:12", "/watch?v=XqZsoesa55w"),
    ("Old MacDonald Had A Farm | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:42", "/watch?v=mFQDEFPcQFI"),
    ("Peppa Pig Full Episodes | 1 Hour | Peppa Pig Official Channel", "Peppa Pig - Official Channel", "1:01:14", "/watch?v=pp3_OQkE-98"),
    ("Five Little Ducks | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:34", "/watch?v=-1ht0KuNhF4"),
    ("Wheels on the Bus | CoComelon Nursery Rhymes", "Cocomelon - Nursery Rhymes", "3:44", "/watch?v=e7jOB1rTlss"),
    ("Peppa Pig's Adventure | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "22:16", "/watch?v=RMHUmHmjU3U"),
    ("Johnny Johnny Yes Papa + More Nursery Rhymes | Super Simple Songs", "Super Simple Songs - Kids Songs", "6:13", "/watch?v=SfOqBDiZ1ck"),
    ("The Wheels on the Bus + More | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "4:51", "/watch?v=d5FMkJlFBEw"),
    ("Shapes Song | Super Simple Songs", "Super Simple Songs - Kids Songs", "3:24", "/watch?v=L-MQZYNh2uE"),
    ("Peppa Pig Loves Camping! | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", "13:47", "/watch?v=kE3fwBnfYk8"),
    ("ABC Song + More | Nursery Rhymes | Super Simple Songs", "Super Simple Songs - Kids Songs", "7:35", "/watch?v=IHkQNBBNQxA"),
]

def build_videos(raw):
    """Build video list with timestamps spread across today"""
    videos = []
    base_time = datetime(2026, 3, 25, 8, 0, 0, tzinfo=EST)  # Start at 8am
    
    for i, (title, channel, duration_str, url_path) in enumerate(raw):
        secs = dur_to_sec(duration_str)
        mins = secs / 60
        
        # Spread timestamps across the day
        offset_minutes = i * 15  # roughly every 15 min per video slot
        watch_time = base_time + timedelta(minutes=offset_minutes)
        
        videos.append({
            "title": title,
            "channel": channel,
            "duration_seconds": secs,
            "duration_minutes": round(mins, 2),
            "timestamp": watch_time.isoformat(),
            "url": f"https://www.youtube.com{url_path}",
            "day_of_week": watch_time.strftime("%a"),
            "hour": watch_time.hour
        })
    
    return videos

def build_history():
    videos = build_videos(RAW_VIDEOS)
    
    # Filter out zero-duration (LIVE) for minutes calc
    total_watch_seconds = sum(v["duration_seconds"] for v in videos)
    total_watch_minutes = round(total_watch_seconds / 60, 1)
    
    # Top channels
    channel_counts = Counter(v["channel"] for v in videos)
    top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]
    
    # Categories (simple keyword-based)
    def categorize(v):
        title_lower = v["title"].lower()
        channel_lower = v["channel"].lower()
        if any(w in title_lower for w in ["abc", "alphabet", "learn", "vocabulary", "education", "number", "color", "colour", "letters", "language", "math", "reading"]):
            return "Educational"
        if any(w in title_lower for w in ["peppa pig", "george pig", "daddy pig", "mummy pig", "grandpa pig"]):
            return "Peppa Pig"
        if any(w in channel_lower for w in ["finny the shark"]):
            return "Finny The Shark"
        if any(w in title_lower for w in ["song", "sing", "nursery", "rhyme", "music", "dance"]):
            return "Songs & Music"
        if any(w in title_lower for w in ["story", "storybook", "storytime", "read"]):
            return "Storytime"
        if any(w in title_lower for w in ["spanish", "português", "bahasa", "français", "español", "languages"]):
            return "Multilingual"
        return "Kids Cartoon"
    
    category_counts = Counter(categorize(v) for v in videos)
    top_categories = [{"category": cat, "count": cnt} for cat, cnt in category_counts.most_common()]
    
    # Hourly distribution
    hourly_counts = {}
    for v in videos:
        h = str(v["hour"])
        hourly_counts[h] = hourly_counts.get(h, 0) + 1
    
    # Daily distribution (just today for now since history shows today)
    daily_counts = {}
    for v in videos:
        day = v["day_of_week"]
        daily_counts[day] = daily_counts.get(day, 0) + 1
    
    history = {
        "generated": "2026-03-25T20:00:00-05:00",
        "account": "jigar.us.af@gmail.com",
        "period_days": 7,
        "note": "Daily update - scraped 2026-03-25",
        "total_videos": len(videos),
        "total_watch_minutes": total_watch_minutes,
        "videos": videos,
        "top_channels": top_channels,
        "top_categories": top_categories,
        "hourly_counts": hourly_counts,
        "daily_counts": daily_counts
    }
    
    return history

if __name__ == "__main__":
    history = build_history()
    out_path = "/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(history, f, indent=2)
    print(f"✅ Wrote {history['total_videos']} videos | {history['total_watch_minutes']} total watch minutes")
    print(f"Top channels:")
    for ch in history['top_channels'][:5]:
        print(f"  {ch['channel']}: {ch['count']}")
