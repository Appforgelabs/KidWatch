#!/usr/bin/env python3
"""Build history.json from browser-scraped data 2026-03-21"""

import json
from pathlib import Path
from datetime import datetime, timezone

TODAY = "2026-03-21T20:00:00-05:00"

VIDEOS_RAW = [
    ("FBumlcEqxJA", "No, David Funny Animated Video", "Storytime with Sonia Panda", "3:53", "https://www.youtube.com/watch?v=FBumlcEqxJA"),
    ("qoRflt9gSnI", "Свинка Пеппа в Роблокс! - Сезон 2 - Серия 2: Лучшая подружка Пеппы", "DudduTV Duddu", "6:52", "https://www.youtube.com/watch?v=qoRflt9gSnI"),
    ("WY8t55anmHk", "peppa the fat belly go to the bus 🚌 Season 1 episode 1", "Miss Kandice💕", "13:06", "https://www.youtube.com/watch?v=WY8t55anmHk"),
    ("YyNrQyUjwFk", "Logo Effects l Pixel Art Minecraft Compilation l Preview 2 Warner Home Video (1997) Effects", "BritishEdits", "2:21", "https://www.youtube.com/watch?v=YyNrQyUjwFk"),
    ("PqmOeHX_g7Y", "Logo Effects Pixel Art Minecraft Compilation l 2025", "UK Edits", "2:16", "https://www.youtube.com/watch?v=PqmOeHX_g7Y"),
    ("O8aZUFrKRRQ", "Logo Effects Pixel Art Minecraft Compilation 2025", "Ikigai Effects", "1:47", "https://www.youtube.com/watch?v=O8aZUFrKRRQ"),
    ("8r2mrUBweUc", "Logo Effects Pixel Art Minecraft Compilation 2024 V14", "BritishEdits", "2:55", "https://www.youtube.com/watch?v=8r2mrUBweUc"),
    ("pg6PcyJrQow", "Logo Effects Pixel Art Minecraft Compilation l 2025", "UK Edits", "2:07", "https://www.youtube.com/watch?v=pg6PcyJrQow"),
    ("GY7GCOYlQ_A", "Best logo intro Super Compilation Effects: YouTube lego, ABC kids tv, cocomelon pingfong logo Effects", "Dharmendra Pro Editor", "16:55", "https://www.youtube.com/watch?v=GY7GCOYlQ_A"),
    ("1mC-CR8AtrA", "TOCA WORLD STORIES!!!", "♡ᴛᴏᴄᴀ_sɪʀᴇᴇɴ♡", "12:10", "https://www.youtube.com/watch?v=1mC-CR8AtrA"),
    ("jZL_y18QpNU", "Cocomelon New Outro Logo: Effects (Preview 2 Frank V2 Effects)", "Dharmendra Pro Editor", "3:26", "https://www.youtube.com/watch?v=jZL_y18QpNU"),
    ("T_A9csA1GSE", "(most viewed)Chu Chu Tv Effects (Sponsored by Preview 2 Effects)", "Dharmendra Pro Editor", "2:31", "https://www.youtube.com/watch?v=T_A9csA1GSE"),
    ("4BeEIodba4M", "Peppa Pig Relaxes With Meditation 🐷 🧘‍♀️ Adventures With Peppa Pig", "Adventures With Peppa Pig", "31:27", "https://www.youtube.com/watch?v=4BeEIodba4M"),
    ("mJ3WDyt3rEs", "The Lunch Thief - Bedtime Stories for Kids in English | ChuChu TV Storytime", "ChuChuTV Storytime for Kids", "7:34", "https://www.youtube.com/watch?v=mJ3WDyt3rEs"),
    ("WEZ88_S8p2A", "Cussly's Politeness - ChuChuTV Storytime Good Habits Bedtime Stories for Kids", "ChuChuTV Storytime for Kids", "8:45", "https://www.youtube.com/watch?v=WEZ88_S8p2A"),
    ("eK8e9lrV6p0", "Olivia's New School - Good Habits Bedtime Stories & Moral Stories for Kids - ChuChu TV", "ChuChuTV Storytime for Kids", "4:21", "https://www.youtube.com/watch?v=eK8e9lrV6p0"),
    ("ixG-EkxjT9Y", "Man In The Park - Bedtime Stories for Kids in English | ChuChu TV Storytime for Children", "ChuChuTV Storytime for Kids", "6:16", "https://www.youtube.com/watch?v=ixG-EkxjT9Y"),
    ("uD6xHoYALVQ", "Peppa Pig Relaxes With Meditation 🐷 🧘‍♀️ Adventures With Peppa Pig", "Adventures With Peppa Pig", "31:27", "https://www.youtube.com/watch?v=uD6xHoYALVQ"),
    ("AFWxSzKsvbY", "Strength in Unity - Storytime Adventures Ep. 2 - ChuChu TV", "ChuChuTV Storytime for Kids", "13:10", "https://www.youtube.com/watch?v=AFWxSzKsvbY"),
    ("EGS5tSMiHkc", "Peppa Pigs Airplane Adventure 🐷 🛩 Adventures With Peppa Pig", "Adventures With Peppa Pig", "1:02:28", "https://www.youtube.com/watch?v=EGS5tSMiHkc"),
    ("bT4HoMY6xuw", "Delphine Donkey Comes to Visit 💤 | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "2:01:28", "https://www.youtube.com/watch?v=bT4HoMY6xuw"),
    ("kc7QNcZf7Vo", "Peppa Pig's VLOG With Delphine Donkey 🫏 | Peppa & Friends 💕 | Tales Full Episodes | Cartoon | 1 Hour", "Peppa Pig and Friends", "1:00:22", "https://www.youtube.com/watch?v=kc7QNcZf7Vo"),
    ("NT7YWA5eETc", "Delphine Donkey Visits | Full Episodes| Fun Cartoons For Kids | Little Peppa Moments", "Little Peppa Moments", "31:30", "https://www.youtube.com/watch?v=NT7YWA5eETc"),
    ("qURTlRUvcnA", "Picnic in the Thunderstorm 🐽 Peppa Pig and Friends Full Episodes", "Peppa Pig and Friends", "1:02:52", "https://www.youtube.com/watch?v=qURTlRUvcnA"),
    ("ganqsmwN8tw", "The NEW Blue Car 🚗 🐽 Peppa Pig and Friends Full Episodes", "Peppa Pig and Friends", "1:02:52", "https://www.youtube.com/watch?v=ganqsmwN8tw"),
    ("UHoWLbfKvYA", "Fun Run Spaghetti! 🐽 Peppa Pig and Friends Full Episodes", "Peppa Pig and Friends", "1:25:54", "https://www.youtube.com/watch?v=UHoWLbfKvYA"),
    ("6iXLWPq_uBA", "Babysitting | 🐷 Adventures With Peppa Pig", "Adventures With Peppa Pig", "4:30", "https://www.youtube.com/watch?v=6iXLWPq_uBA"),
    ("GhFAJmoZqT4", "Peppa Pig Travels To The Future 🐷 🕰 Adventures Of Peppa Pig", "Adventures With Peppa Pig", "31:25", "https://www.youtube.com/watch?v=GhFAJmoZqT4"),
    ("Y-uqVdb1BOk", "Peppa's Very Muddy Playtime 🧽 🐽 Peppa Pig and Friends Full Episodes", "Peppa Pig and Friends", "1:02:57", "https://www.youtube.com/watch?v=Y-uqVdb1BOk"),
    ("7U9cuh9N6Yw", "The Talking Car 🚗 🐽 Peppa Pig and Friends Full Episodes", "Peppa Pig and Friends", "1:02:34", "https://www.youtube.com/watch?v=7U9cuh9N6Yw"),
    ("TGIap_eaScs", "Peppa Pig Becomes A Giant In Tiny Land 😮 🐽 Peppa Pig and Friends Full Episodes", "Peppa Pig and Friends", "32:02", "https://www.youtube.com/watch?v=TGIap_eaScs"),
    ("fpEy9m_t0To", "Peppa Pig - Viaggio in Aereo! | Cartoni per Bambini | WildBrain Laboratorio dello Studio", "WildBrain Laboratorio dello Studio", "24:19", "https://www.youtube.com/watch?v=fpEy9m_t0To"),
    ("GBKoxncURVM", "George's CHEEKY Birthday Party 🎈 Bouncy Castle Fun! 🏰 Peppa Pig Full Episodes | 30 Minutes", "George Pig - Official Channel", "31:27", "https://www.youtube.com/watch?v=GBKoxncURVM"),
    ("yah5X-wTIpc", "Learn Spanish Words with Peppa Pig and Friends Driving Toy Cars Around Town!", "Genevieve's Playhouse - Learning Videos for Kids", "7:02", "https://www.youtube.com/watch?v=yah5X-wTIpc"),
    ("OYzIUntnh70", "Diana and Peppa Pig Theme Park", "✿ Kids Diana Show", "12:01", "https://www.youtube.com/watch?v=OYzIUntnh70"),
    ("XFWvogQgc7I", "Blippi Explores Jungle Animals! | Educational Videos for Kids | Blippi and Meekah Kids TV", "Meekah - Educational Videos for Kids", "15:07", "https://www.youtube.com/watch?v=XFWvogQgc7I"),
    ("Dvov7D1Wyzg", "Blippi Visits Slides at an Indoor Playground! | Learn with Blippi | Educational Videos for Toddlers", "Blippi Wonders - Educational Cartoons for Kids", "12:27", "https://www.youtube.com/watch?v=Dvov7D1Wyzg"),
    ("SrBnsSwTGjM", "Kids, let's Learn Common Words with Woodzeez Toy Dollhouse!", "Genevieve's Playhouse - Learning Videos for Kids", "11:37", "https://www.youtube.com/watch?v=SrBnsSwTGjM"),
    ("KVVdJUrKoMA", "Johny Johny Yes Papa Sports & Games Nursery Rhyme - 3D Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "3:03", "https://www.youtube.com/watch?v=KVVdJUrKoMA"),
    ("e0O6lW38ew4", "Doctor Daisy, MD | S1 E25 | Full Episode | Mickey Mouse Clubhouse", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=e0O6lW38ew4"),
    ("_nAu9D-8srA", "Learning Colors – Colorful Eggs on a Farm", "Мирошка ТВ", "5:11", "https://www.youtube.com/watch?v=_nAu9D-8srA"),
    ("V8LG1oiohd4", "All Jolly Phonics Songs a-z | Repeated with Actions | Alphabetical Order | Belgrave Phonics", "Belgrave St. Bartholomew's Academy", "13:20", "https://www.youtube.com/watch?v=V8LG1oiohd4"),
    ("V9hvxLl1ln8", "In The Kitchen + More | Happy Songs & Fun For Preschool! | Noodle & Pals", "Noodle & Pals", "1:10:04", "https://www.youtube.com/watch?v=V9hvxLl1ln8"),
    ("O1YohX-1KXc", "Halloween + Classroom Songs With Noodle & Pals | Happy Halloween! 🎃", "Noodle & Pals", "1:07:50", "https://www.youtube.com/watch?v=O1YohX-1KXc"),
    ("W38unLel7co", "What Will You Be For Halloween? | Costumes Song for Kids | Noodle & Pals", "Noodle & Pals", "2:37", "https://www.youtube.com/watch?v=W38unLel7co"),
    ("GlprS1K_Hxw", "Best of 2025! 🎉 | Your Favorite Preschool Songs | Happy New Year from Noodle & Pals!", "Noodle & Pals", "59:41", "https://www.youtube.com/watch?v=GlprS1K_Hxw"),
    ("GGbm73UAfUs", "What's Inside The Toy Box? 🎁 | Favorite Toy Song | Surprises with Noodle & Pals!", "Noodle & Pals", "2:38", "https://www.youtube.com/watch?v=GGbm73UAfUs"),
    ("HO7sudbpLp0", "🔴 Noodle and Pals Livestream | Kids Songs | Super Simple Songs", "Super Simple Live - 24 Hour Livestreams for Kids", "LIVE", "https://www.youtube.com/watch?v=HO7sudbpLp0"),
    ("tMuax8_AaNA", "A Very Merry Noodle & Pals Christmas! ⭐️ | Super Simple Christmas Songs for Kids & Families", "Noodle & Pals", "1:07:07", "https://www.youtube.com/watch?v=tMuax8_AaNA"),
    ("RryPY87OPeM", "Skidamarink + More ❤️ | Have Fun on Valentine's Day at Preschool! | Noodle & Pals", "Noodle & Pals", "1:07:20", "https://www.youtube.com/watch?v=RryPY87OPeM"),
    ("npgoG8kF_zk", "Let's Take Turns + More | 1 Hour | Kids Songs for Language Learning and Preschool | Noodle & Pals", "Noodle & Pals", "1:00:28", "https://www.youtube.com/watch?v=npgoG8kF_zk"),
    ("37CNa6NHnww", "I'm A Little Train + More | 🚂 Pretend To Be A Choo Choo Train! | Preschool Hits | Noodle & Pals", "Noodle & Pals", "1:09:00", "https://www.youtube.com/watch?v=37CNa6NHnww"),
    ("UQ0qWhY-4sE", "Put On Your Costume | Get ready for Halloween with Noodle & Pals", "Noodle & Pals", "3:13", "https://www.youtube.com/watch?v=UQ0qWhY-4sE"),
    ("DzgwbVZr_VU", "Quicksand, Lava, Sharks + more! 🌋🦈 🐍 | Dance Along Compilation | Danny Go! Songs for Kids", "Danny Go!", "18:06", "https://www.youtube.com/watch?v=DzgwbVZr_VU"),
    ("L9NnDUKDIGk", "\"Glow in the Dark Shapes Dance!\" Glow Sticks Brain Break | Danny Go! Songs for Kids", "Danny Go!", "3:37", "https://www.youtube.com/watch?v=L9NnDUKDIGk"),
    ("rmwENNtC9RU", "Best Peppa Pig Learning Video for Kids - George's Birthday Party Adventure!", "Genevieve's Playhouse - Learning Videos for Kids", "11:24", "https://www.youtube.com/watch?v=rmwENNtC9RU"),
    ("BxGhz77eDSM", "Let's go on a plane trip - Going to Paris - Darn David", "Darn David Official", "3:24", "https://www.youtube.com/watch?v=BxGhz77eDSM"),
    ("q-6g_viAcIk", "\"The Color Dance Game!\" 🌈 Would You Rather Brain Break | Danny Go! Songs for Kids", "Danny Go!", "3:49", "https://www.youtube.com/watch?v=q-6g_viAcIk"),
    ("QHPi3tVbq6U", "Grocery Store DASH! 🍌🛒🍕 Swipe & Scan Dance | Adventure Run | Danny Go! Songs for Kids", "Danny Go!", "4:41", "https://www.youtube.com/watch?v=QHPi3tVbq6U"),
    ("nEUTY8n2iZo", "\"The Floor is Lava Dance!\" 🌋 Danny Go! Kids Brain Break Activity Songs", "Danny Go!", "3:14", "https://www.youtube.com/watch?v=nEUTY8n2iZo"),
    ("XDJHcUkkjHA", "Wiggle, Freeze, Spin + more! | Dance Along | Dance Compilation | Danny Go! Songs for Kids", "Danny Go!", "16:23", "https://www.youtube.com/watch?v=XDJHcUkkjHA"),
    ("DsUPVERZFlI", "\"The Wiggle Dance!\" 🪱 Danny Go! Brain Break Songs for Kids", "Danny Go!", "3:09", "https://www.youtube.com/watch?v=DsUPVERZFlI"),
    ("QGiHZxYuDhA", "Before I Go To School | Back To School Songs for Kids | Morning Routines | The Mik Maks", "The Mik Maks", "2:00", "https://www.youtube.com/watch?v=QGiHZxYuDhA"),
    ("h9PlG8w7_R8", "I Like Broccoli Ice Cream Song VERSION 2 - Funny Food song for kids by Bella and Beans TV", "Bella & Beans TV", "2:02", "https://www.youtube.com/watch?v=h9PlG8w7_R8"),
    ("YvFCEJ0XGHY", "🔴 LIVE! Peppa Pig's Learning Adventures! 🍦 Peppa's Playgroup: Little Learners 🐷 Kids Cartoons", "Peppa's Playgroup: Little Learners", "3:58:53", "https://www.youtube.com/watch?v=YvFCEJ0XGHY"),
    ("lA7Cju_wQLc", "More Real Life Funny Food Combinations, Do You Like Broccoli Ice Cream Song by Bella and Beans TV", "Bella & Beans TV", "1:55", "https://www.youtube.com/watch?v=lA7Cju_wQLc"),
    ("v1a-lUvk7lo", "I Like Broccoli Ice Cream Song - Funny Food song for kids by Bella and Beans TV", "Bella & Beans TV", "1:53", "https://www.youtube.com/watch?v=v1a-lUvk7lo"),
]


def parse_duration(d):
    """Parse duration string to seconds."""
    if d == "LIVE" or not d:
        return 0
    parts = d.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0


def fmt_seconds(s):
    if s >= 3600:
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        return f"{h}:{m:02d}:{sec:02d}"
    m = s // 60
    sec = s % 60
    return f"{m}:{sec:02d}"


def build():
    from collections import Counter
    videos = []
    for vid_id, title, channel, dur_str, url in VIDEOS_RAW:
        dur_sec = parse_duration(dur_str)
        dur_fmt = dur_str if dur_str != "LIVE" else "0:00"
        videos.append({
            "video_id": vid_id,
            "title": title,
            "channel": channel,
            "duration": dur_fmt,
            "duration_seconds": dur_sec,
            "timestamp": TODAY,
            "url": url,
        })

    total_seconds = sum(v["duration_seconds"] for v in videos)
    total_minutes = round(total_seconds / 60, 1)

    channel_counts = Counter(v["channel"] for v in videos)
    top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

    # Simple category assignment
    category_map = {
        "Peppa Pig": ["Peppa Pig", "Adventures With Peppa Pig", "Peppa Pig and Friends",
                      "Peppa Pig - Official Channel", "Little Peppa Moments", "George Pig - Official Channel",
                      "WildBrain Laboratorio dello Studio", "Miss Kandice💕", "DudduTV Duddu",
                      "Peppa's Playgroup: Little Learners"],
        "Nursery Rhymes & Songs": ["Noodle & Pals", "Super Simple Live - 24 Hour Livestreams for Kids",
                                   "CVS 3D Rhymes & Kids Songs", "Belgrave St. Bartholomew's Academy",
                                   "The Mik Maks", "Bella & Beans TV"],
        "Dance & Movement": ["Danny Go!"],
        "Storytime & Books": ["Storytime with Sonia Panda", "ChuChuTV Storytime for Kids",
                              "♡ᴛᴏᴄᴀ_sɪʀᴇᴇɴ♡"],
        "Educational": ["Genevieve's Playhouse - Learning Videos for Kids", "Blippi Wonders - Educational Cartoons for Kids",
                        "Meekah - Educational Videos for Kids", "Disney Jr.", "Мирошка ТВ",
                        "✿ Kids Diana Show", "Darn David Official"],
        "Logo Effects": ["BritishEdits", "UK Edits", "Ikigai Effects", "Dharmendra Pro Editor"],
    }
    cat_counts = Counter()
    for v in videos:
        matched = False
        for cat, channels in category_map.items():
            if v["channel"] in channels:
                cat_counts[cat] += 1
                matched = True
                break
        if not matched:
            cat_counts["Other"] += 1

    top_categories = [{"category": c, "count": n} for c, n in cat_counts.most_common()]

    data = {
        "generated": "2026-03-21T20:00:00-05:00",
        "account": "jigar.us.af@gmail.com",
        "period_days": 7,
        "note": "Daily update",
        "total_videos": len(videos),
        "total_watch_minutes": total_minutes,
        "videos": videos,
        "top_channels": top_channels,
        "top_categories": top_categories,
        "hourly_counts": {"20": len(videos)},
        "daily_counts": {"Sat": len(videos)},
    }

    out = Path(__file__).parent.parent / "data" / "history.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"✅ Wrote {len(videos)} videos, {total_minutes} minutes to {out}")
    return data


if __name__ == "__main__":
    build()
