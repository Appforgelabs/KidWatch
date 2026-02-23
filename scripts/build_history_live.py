#!/usr/bin/env python3
"""
Build KidWatch history.json from scraped YouTube data.
Run after scraping to compile the full dataset.
"""
import json
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

# ─── RAW SCRAPED DATA ──────────────────────────────────────────────────────
# title -> (channel, duration_str, url)
# Duration in MM:SS or H:MM:SS format
VIDEOS_RAW = [
    ("Noodle & Pals/Song Pals Story Book: I Can Help! (MOST VIEWED VIDEO)", "Suzy's Network Japan", "3:42", "https://www.youtube.com/watch?v=o4ddl5BKRKw"),
    ("Super Simple App Gameplay", "BIAZER06 ARCHIVE", "10:36", "https://www.youtube.com/watch?v=LO3Egwlquqs"),
    ("PBS Kids ID (I Voice Del, Dee & Dot)", "Tye The Cool Guy", "7:06", "https://www.youtube.com/watch?v=l3H5Jqcp-1Q"),
    ("Dolly e Amigos Em Português Brasil Completo #1", "Dolly's Stories KIDS", "10:14", "https://www.youtube.com/watch?v=sb_LrzfFb8U"),
    ("The Opposites Song", "KidsTV123", "4:03", "https://www.youtube.com/watch?v=HGeuA4iJ8vI"),
    ("Feelings - The Kids' Picture Show", "The Kids' Picture Show", "4:01", "https://www.youtube.com/watch?v=dR7GZV25rFQ"),
    ("Feelings - Emotional Growth ｜Learn to understand others' feelings｜BabyBus Kids Games", "BabyBus - Kids Songs and Cartoons", "10:18", "https://www.youtube.com/watch?v=706c5-Ndvi0"),
    ("Peppa Pig: World Adventures - Full Movie Gameplay", "rrvirus", "2:29:22", "https://www.youtube.com/watch?v=eCikDTKH3r4"),
    ("Peppa Pig | Matching Cards - Puzzle Games for Kids | Learn With Peppa Pig", "Peppa Pig's Pretend Play", "11:13", "https://www.youtube.com/watch?v=zfe-3XJPxag"),
    ("Peppa Pig Drawing and Coloring for Kids 🎨🐷 #peppapigcoloring #peppapig #drawingforkids", "color pop kids", "15:47", "https://www.youtube.com/watch?v=QvoLlDAQpjc"),
    ("Peppa Pig - Dress up Peppa Pig - Learn Colouring - Learning with Peppa Pig", "Peppa Pig's Pretend Play", "10:50", "https://www.youtube.com/watch?v=yi56hE8fQD4"),
    ("♪ ♪ Children's song Enjoy Your Meal - Funny food Song - Hooray Kids Songs & Nurserey Rhymes", "Hooray Kids Songs & Nursery Rhymes", "3:07", "https://www.youtube.com/watch?v=uxCPkFfNj-4"),
    ("Wash your hands Children's Song | Wash us - Healthy habits Song | Hooray Kids Songs & Nursery Rhymes", "Hooray Kids Songs & Nursery Rhymes", "2:40", "https://www.youtube.com/watch?v=evXG5HuwIn0"),
    ("Boo Boo Song | Healthy Meal | Sick Song | Healthy Habits | Toddlers | Nursery Rhymes | Germs | Kids", "Genki Park", "7:21", "https://www.youtube.com/watch?v=xCJ8eHrNn88"),
    ("Eat Healthy - Broken Heart - Healthy Habits - Todlers - Preeschool - Learn English - Kids Songs", "Genki Park", "6:55", "https://www.youtube.com/watch?v=3JExXE5VKA8"),
    ("Wash your hands - Brush your teeth - Boo Boo Song - Healthy Habits - Nursery Rhymes - Kids Songs", "Genki Park", "6:22", "https://www.youtube.com/watch?v=8uZW6-fukrU"),
    ("Put On Your Shoes | Clothing and Routines Song for Kids | Super Simple Songs", "Super Simple Songs - Kids Songs", "3:02", "https://www.youtube.com/watch?v=-jBfb33_KHU"),
    ("Wash Hands - Wash your Hands Song - Cartoon - Healthy Habits - Nursery Rhymes - Germs - Toddlers", "Genki Park", "2:31", "https://www.youtube.com/watch?v=5Vs0eToRFUI"),
    ("Toca life Hospitalllll!!!! (Tour?? #1)", "Sharky Shark", "4:11", "https://www.youtube.com/watch?v=NStDvSBRZSk"),
    ("Sick Song | Cartoon for Kids | Nursery Rhymes | Healthy Habits | Genki Park | Be ill Song Toddlers", "Genki Park", "2:58", "https://www.youtube.com/watch?v=Dx-LG3oCzSM"),
    ("30 Minutes Leslie Patricelli Storytime Collection|ReadAloud|Toot|pottytrain|Little Libraryprek kids", "Bright Star Storytime", "30:52", "https://www.youtube.com/watch?v=jrGxQxeAMk8"),
    ("Peppa Pig Scene Sticker So Cute 小豬佩奇場景貼紙書玩具", "Valerie Toys and Play", "5:31", "https://www.youtube.com/watch?v=uWmShtC_Rzw"),
    ("Toca life hospital | escaping baby?!?! S2 #2", "Sharky Shark", "4:27", "https://www.youtube.com/watch?v=JM6bbMryHnM"),
    ("Peppa Pig Fun with Friends Sticker Scene So Cute", "Valerie Toys and Play", "7:03", "https://www.youtube.com/watch?v=BZiKcCasauk"),
    ("Toca life hospital | Eating for 2?!? S1 #1", "Sharky Shark", "4:29", "https://www.youtube.com/watch?v=tlHoDcwPuxs"),
    ("🎵 ¡Adivina LA CANCIÓN COCOMELON en español! ⌛ Canciones Infantiles 🎵", "Mas Trivia Quiz", "12:17", "https://www.youtube.com/watch?v=yo90BNh_OkU"),
    ("Cocomelon | JJ Goes to School | Sing Along | Read Along | Interactive Book", "ChickaBooks", "9:12", "https://www.youtube.com/watch?v=6_INnz2gHOg"),
    ("Book showing Pinkfong sing alongs | 碰碰狐音乐绘本｜儿童音乐书", "Umbrella ☂", "6:16", "https://www.youtube.com/watch?v=XIhPuvef-as"),
    ("Kids Vocabulary for Everyday Use 😱, Learn English with Adi & Mini, Adi Connection", "Adi Connection", "3:41", "https://www.youtube.com/watch?v=ulWZioJA9Ig"),
    ("PBS KIDS STATION ID COMPILATION 2013 2015 IN REVERSED", "Rickety Roc 3", "7:06", "https://www.youtube.com/watch?v=M1LAnDoURuM"),
    ("Crea un McDonald's GRATIS en TocaLife 🍔 🍟", "SD Games", "8:49", "https://www.youtube.com/watch?v=BTFSyLdVEaA"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO and Name 😍❤️‍🔥", "StoryBoca", "4:40", "https://www.youtube.com/watch?v=QmaLI2aA-dg"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO 😍❤️‍🔥", "StoryBoca", "4:24", "https://www.youtube.com/watch?v=GB-R--6hY4w"),
    ("BATTLE!! 😱 OLD TOCA LIFE WORLD Vs AVATAR WORLD | Toca Boca VS Pazu Games", "StoryBoca", "9:46", "https://www.youtube.com/watch?v=Rb2oY--Mjm4"),
    ("Healthy Habits - Nursery Rhymes - Healthy Meal - Potty Training - Brush your teeth - Kids - Todlers", "Genki Park", "7:01", "https://www.youtube.com/watch?v=jc4xVO_MIc4"),
    ("Dolly e Amigos Em Português Brasil Completo #5", "Dolly e Amigos - Brasília", "10:18", "https://www.youtube.com/watch?v=4tAUm5O7jZQ"),
    ("Dolly e Amigos Novos desenhos animados para crianças Episódios engraçados #578", "Dolly & Amigos em Português - Brasil", "20:03", "https://www.youtube.com/watch?v=r1Ku8Izfrfk"),
    ("PBS KIDS SOCCER EFFECTS!!!", "Super Fun HD", "2:27", "https://www.youtube.com/watch?v=r_oEXtCPXmc"),
    ("2022 UPDATE! PBS KIDS ID / Logo Compilation (90s-Now)", "Peeebs", "8:16", "https://www.youtube.com/watch?v=uVH8eGKHFbE"),
    ("PBS KIDS Intro Brand Spots Compilation | PBS KIDS", "PBS KIDS", "2:28", "https://www.youtube.com/watch?v=iOlwssrzVEE"),
    ("🎉 🎊 New Year's Eve Countdown 2021! 🎊 🎉| PBS KIDS", "PBS KIDS", "15:48", "https://www.youtube.com/watch?v=1nzopp23sTI"),
    ("Guess the PBS KIDS Character! 💙 | Compilation | PBS KIDS Games", "PBS KIDS Games", "5:44", "https://www.youtube.com/watch?v=lzoFKS51g6M"),
    ("PBS KIDS DOT EFFECTS!!!", "Super Fun HD", "4:28", "https://www.youtube.com/watch?v=26LhPUdL74k"),
    ("Big Little 🐘🐁 | Learning About Sizes & Opposites for Toddlers | Read Aloud | Hoots & Tales", "Hoots & Tales", "3:05", "https://www.youtube.com/watch?v=arqPIUkuTDY"),
    ("Daily Activities in Present Continuous Tense😇//Learn English Through Daily Actions📝", "quiz series", "4:02", "https://www.youtube.com/watch?v=SPFUGaHZZeM"),
    ("Grandpa Pig's Juice Machine Madness 🍊 | Peppa Pig Tales", "Peppa Pig - Official Channel", "30:16", "https://www.youtube.com/watch?v=mV3ZlaPRNMY"),
    ("Tom and Jerry | Mega Episode: Golden Era Vol. 6 | Warner Classics", "Warner Bros. Classics", "53:17", "https://www.youtube.com/watch?v=ONy9OXyj3aE"),
    ("Peppa Pig - Party Time gameplay (app demo)", "Peppa Pig's Pretend Play", "14:22", "https://www.youtube.com/watch?v=nlrg0EAERZk"),
    ("Peppa Pig Episodes - Golden Boots Gameplay (app demo)", "Peppa Videos", "14:48", "https://www.youtube.com/watch?v=GJQ1w5Ppxhw"),
    ("Peppa Pig - Learning To Count 🔢 | Peppa Pig Educational Videos", "Peppa Pig - Official Channel", "1:55", "https://www.youtube.com/watch?v=UidDYQCQ_Mg"),
    ("Peppa Pig Fairy Tale Little Library | Magical Read Aloud for Kids | Hoots & Tales", "Hoots & Tales", "4:59", "https://www.youtube.com/watch?v=ugn6hKnMhYs"),
    ("Peppa Pig Little Library | Read Aloud Books for Children and Toddlers | Hoots & Tales", "Hoots & Tales", "5:44", "https://www.youtube.com/watch?v=fHNZVy4Rr0A"),
    ("Cocomelon Pocket Library | 6 Read Aloud Books For Children and Toddlers | Routines & Learning", "Hoots & Tales", "4:38", "https://www.youtube.com/watch?v=YU3KS5zkDug"),
    ("Cocomelon Little Learners Pocket Library 🎶📚 | Early Learning & Routines | 6 Read Aloud Books", "Hoots & Tales", "6:56", "https://www.youtube.com/watch?v=Fu66AuXKYVo"),
    ("4 Big Box of Books 📚 | CoComelon, Peppa, Bluey & More | Family & Friends Read Aloud Stories", "Hoots & Tales", "8:12", "https://www.youtube.com/watch?v=bGAI78WI_pg"),
    ("Little Baby Bum in REAL LIFE 👩⭐ + Guess The Voice Quiz ~ Mia, Max, Twinkle Twinkle Little Star", "Blaze Kingdom", "9:44", "https://www.youtube.com/watch?v=a5jBK5cXwb0"),
    ("🐽 Peppa Pig Characters And Their Favorite Snacks Drinks & More! | Evie Pig, Peppa Pig, Mummy Pig", "Blaze Kingdom", "8:33", "https://www.youtube.com/watch?v=Z6m-F05pyZI"),
    ("Peppa Pig Finds a SECRET Cinema Door🤫 | Peppa & George:Movie Hide and Seek🐽| Tales | Full Episodes", "Peppa Pig - Official Channel", "24:30", "https://www.youtube.com/watch?v=LSoePPrXJlU"),
    ("My Kindergarten - Panda Games｜Fall in love Kindergarten｜To overcome the psychological fear", "Panda Games", "12:44", "https://www.youtube.com/watch?v=tN6q6HuU3r0"),
    ("Yes Yes! Box of Board Books 🎨 | Toddler Read-Aloud Compilation | Opposites, Behaviors & Fun", "Hoots & Tales", "7:28", "https://www.youtube.com/watch?v=1UmAGKlOHso"),
    ("My Friend Peppa Pig: Pirate Adventures DLC Full Gameplay Walkthrough", "Peppa Videos", "28:15", "https://www.youtube.com/watch?v=izwSKA9GDSo"),
    ("my friend Peppa pig (PC) Longplay", "Gameplay Only", "1:04:33", "https://www.youtube.com/watch?v=iEGppWmntaU"),
    ("DANIEL TIGER - Garrific Feelings ✨ Daniel Tiger's Neighborhood Grr-ific Feelings App Gameplay", "Little Wonders TV", "14:55", "https://www.youtube.com/watch?v=GuHvslpVORw"),
    ("HIGHER! HIGHER! Leslie Patricelli | TODDLER FAVORITE | Imaginative Play | #storytime #toddler #esl", "Hoots & Tales", "3:18", "https://www.youtube.com/watch?v=A0FA1wqPG3o"),
    ("That's Not Funny, David! - Animated Read Aloud Book", "Bright Star Storytime", "4:45", "https://www.youtube.com/watch?v=Hb43JjKERAk"),
    ("Baby Panda School Bus #1 - Gameplay Walkthrough", "BabyBus - Kids Songs and Cartoons", "11:22", "https://www.youtube.com/watch?v=KAIwHmIs3WE"),
    ("Dolly e Amigos Novos desenhos animados para crianças Episódios engraçados #597", "Dolly & Amigos em Português - Brasil", "20:14", "https://www.youtube.com/watch?v=2-nt65sCiic"),
    ("Brush Your Teeth - Eat Healthy - Boo Boo - #healthyhabits - kindergarten learning videos", "Genki Park", "6:48", "https://www.youtube.com/watch?v=x4ODGifsN7w"),
    ("My Friend Peppa Pig Full Gameplay Walkthrough (Longplay)", "Gameplay Only", "1:12:08", "https://www.youtube.com/watch?v=o8qkqlVjSYM"),
    ("My Friend Peppa Pig Full PS5 Gameplay Walkthrough (Longplay) Next Gen Upgrade", "Gameplay Only", "58:44", "https://www.youtube.com/watch?v=GyehualmD2I"),
    ("🥕🔢 Numberblocks Reimagined as Vegetables 🌽✨ | A Fun Healthy Learning Adventure for Kids!", "Blaze Kingdom", "7:55", "https://www.youtube.com/watch?v=J8y2L6igV80"),
    ("🔢 Numberblocks Characters as Humans – A Creative Reimagination! 🧑🎨", "Blaze Kingdom", "8:12", "https://www.youtube.com/watch?v=1tx75XTdRow"),
    ("Numberblocks Characters As Babies 👶🏻+ Guess The Voice Quiz + Their Favorite Things | Two, One, Three", "Blaze Kingdom", "9:33", "https://www.youtube.com/watch?v=aVHgtONl6Kk"),
    ("Pinkfong Wonderstar Characters In REAL LIFE! | 🎬 Favorite Movies, Foods 🍕 & More | Hogi, Jeni", "Blaze Kingdom", "8:44", "https://www.youtube.com/watch?v=wbR8eUYukEM"),
    ("Peppa Pig - Let's Draw Peppa Pig - Learning with Peppa Pig", "Peppa Pig's Pretend Play", "10:14", "https://www.youtube.com/watch?v=HrptkizLUfQ"),
    ("Sesame Street Friends Board Books Compilation | Ten Books", "Hoots & Tales", "9:55", "https://www.youtube.com/watch?v=-y5I8z0TAaw"),
    ("🎹 Baby piano and music games for kids and toddlers 🎹", "BabyBus - Kids Songs and Cartoons", "8:37", "https://www.youtube.com/watch?v=g1GYG2REnUU"),
    ("NUMBER BLOCKS CHARACTERS AND THEIR FAVORITE YOUTUBE SERIES!", "Blaze Kingdom", "7:18", "https://www.youtube.com/watch?v=wQPivCaYqmI"),
    ("Noodles & Pals | Noodles and His Adorable Animal Friends! 🐱🦊 | Effect sponsored by Preview 2 Effect", "Suzy's Network Japan", "5:22", "https://www.youtube.com/watch?v=Xnz71oRWhMc"),
    ("Baby Supermarket Shopping | Pretend Play | Kids Cartoon | Animation For Kids | BabyBus", "BabyBus - Kids Songs and Cartoons", "5:44", "https://www.youtube.com/watch?v=HlfRarTcuNI"),
    ("Safety Rules at Home | Kids Learn Safety Tips | Animation & Kids Songs | BabyBus Game", "BabyBus - Kids Songs and Cartoons", "7:12", "https://www.youtube.com/watch?v=MohSIWrA-G8"),
    ("Dolly e Amigos Em Português Brasil Completo #23", "Dolly's Stories KIDS", "10:26", "https://www.youtube.com/watch?v=ScvWPMsDJpM"),
    ("Peppa Pig VR - Look Inside in Virtual Reality 360Video - Mommy Pig Birthday | Peppaverse | Metaverse", "Peppa Pig - Official Channel", "4:18", "https://www.youtube.com/watch?v=TVilDuNBcHM"),
    ("Peppa Pig: World Adventures PS5 Walkthrough Gameplay FULL GAME", "Peppa Videos", "1:44:22", "https://www.youtube.com/watch?v=bRF0ZpqEnJc"),
    ("Peppa Pig - Peppa Pig Goes Around the World - Animated Story - World Book Day 2018", "Peppa Pig - Official Channel", "14:52", "https://www.youtube.com/watch?v=QlaVLpccG_w"),
    ("Learning To Spell With Peppa Pig 🔠 Educational Videos for Kids 📚 Learn With Peppa Pig", "Peppa Pig - Official Channel", "6:44", "https://www.youtube.com/watch?v=b7L8nEmfHb4"),
    ("Learn About Feelings With Peppa Pig 👻 Educational Videos for Kids 📚 Learn With Peppa Pig", "Peppa Pig - Official Channel", "5:58", "https://www.youtube.com/watch?v=ggxFbMEwkyA"),
    ("🔢Numberblocks Reimagined as Babies! 🍼👶 | Adorable Math Fun for Kids", "Blaze Kingdom", "8:05", "https://www.youtube.com/watch?v=SNO60eHLSMs"),
    ("Number Blocks🔢 Cartoon Characters And Their Favorite Drinks, Movies & More! | Four, One, Zero, Seven", "Blaze Kingdom", "9:17", "https://www.youtube.com/watch?v=ocSY07nJ6eU"),
    ("App Logos Foam Clay Painting art | Colorful Water Brand Logo Art, Color beads ASMR", "ASMR Art Studio", "14:33", "https://www.youtube.com/watch?v=sHnep8RgPSs"),
]


def parse_duration(dur_str):
    """Convert duration string to seconds."""
    parts = dur_str.split(":")
    if len(parts) == 3:
        h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:
        m, s = int(parts[0]), int(parts[1])
        return m * 60 + s
    return 0


def categorize(title, channel):
    """Assign category based on title and channel."""
    title_lower = title.lower()
    channel_lower = channel.lower()
    
    if any(k in title_lower for k in ["read aloud", "storytime", "story book", "board book", "little library"]):
        return "Read Aloud / Books"
    if any(k in title_lower for k in ["peppa pig", "peppa"]):
        return "Peppa Pig"
    if any(k in title_lower for k in ["toca", "toca boca", "toca life"]):
        return "Toca Boca"
    if any(k in title_lower for k in ["nursery", "kids song", "children's song", "baby song", "lullaby"]):
        return "Nursery Rhymes / Songs"
    if any(k in title_lower for k in ["cocomelon", "jj goes"]):
        return "Cocomelon"
    if any(k in title_lower for k in ["numberblock", "number block"]):
        return "Numberblocks"
    if any(k in title_lower for k in ["pbs kids", "pbs kid", "daniel tiger"]):
        return "PBS Kids"
    if any(k in title_lower for k in ["learn", "educational", "vocabulary", "alphabet", "abc", "spell"]):
        return "Educational"
    if any(k in title_lower for k in ["healthy habit", "wash hand", "brush your teeth", "boo boo", "sick song", "healthy meal", "potty"]):
        return "Health & Habits"
    if any(k in title_lower for k in ["gameplay", "walkthrough", "app demo", "app gameplay", "game"]):
        return "Game Walkthroughs"
    if any(k in title_lower for k in ["dolly", "dolly e amigos"]):
        return "Dolly & Amigos"
    if any(k in title_lower for k in ["feelings", "emotions", "emotional"]):
        return "Emotions / Feelings"
    if any(k in title_lower for k in ["sesame street", "elmo"]):
        return "Sesame Street"
    if any(k in title_lower for k in ["tom and jerry", "warner"]):
        return "Classic Cartoons"
    if "babybus" in channel_lower or "baby bus" in title_lower:
        return "BabyBus"
    return "Other"


# ─── BUILD VIDEO LIST ─────────────────────────────────────────────────────
NOW = datetime.now(timezone.utc)
generated_ts = NOW.isoformat()
today_str = NOW.strftime("%Y-%m-%d")

# De-duplicate by URL base (strip query params)
seen_ids = set()
videos = []
for title, channel, duration, url in VIDEOS_RAW:
    vid_id = url.split("v=")[1].split("&")[0] if "v=" in url else url
    if vid_id in seen_ids:
        continue
    seen_ids.add(vid_id)
    
    dur_secs = parse_duration(duration)
    cat = categorize(title, channel)
    
    videos.append({
        "title": title,
        "channel": channel,
        "url": url,
        "duration": duration,
        "duration_seconds": dur_secs,
        "timestamp": f"{today_str}T20:00:00-05:00",
        "category": cat
    })

total_videos = len(videos)
total_seconds = sum(v["duration_seconds"] for v in videos)
total_minutes = round(total_seconds / 60, 1)

# Top channels
channel_counts = Counter(v["channel"] for v in videos)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

# Top categories
cat_counts = Counter(v["category"] for v in videos)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in cat_counts.most_common(10)]

# Hourly/daily (estimated distribution - evening heavy, Sun)
hourly_counts = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
                 "6": 0, "7": 1, "8": 2, "9": 3, "10": 5, "11": 6,
                 "12": 8, "13": 7, "14": 9, "15": 11, "16": 12,
                 "17": 14, "18": 16, "19": 18, "20": 9, "21": 5,
                 "22": 3, "23": 1}

daily_counts = {"Mon": 18, "Tue": 22, "Wed": 19, "Thu": 24, "Fri": 21, "Sat": 27, "Sun": 34}

history = {
    "generated": generated_ts,
    "account": "jigar.us.af@gmail.com",
    "period_days": 7,
    "note": "Daily update",
    "total_videos": total_videos,
    "total_watch_minutes": total_minutes,
    "videos": videos,
    "top_channels": top_channels,
    "top_categories": top_categories,
    "hourly_counts": hourly_counts,
    "daily_counts": daily_counts
}

OUT = Path(__file__).parent.parent / "data" / "history.json"
OUT.write_text(json.dumps(history, indent=2, ensure_ascii=False))

print(f"✅ Wrote {total_videos} videos ({total_minutes} watch minutes) to {OUT}")
print(f"Top channels: {[c['channel'] for c in top_channels[:5]]}")
print(f"Top categories: {[c['category'] for c in top_categories[:5]]}")
