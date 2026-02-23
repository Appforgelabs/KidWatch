#!/usr/bin/env python3
"""Build history.json from scraped YouTube watch history data (Feb 21, 2026)."""
import json
from datetime import datetime
from collections import Counter
from pathlib import Path

# ── Raw video data extracted from YouTube Watch History ──────────────────────
# Format: (title, channel, duration_raw, url, section_date)
# duration_raw: "HH:MM:SS" or "MM:SS" or "" for unknown

RAW_VIDEOS = [
    # ── TODAY (Feb 21, 2026) ──────────────────────────────────────────────────
    ("Boo Boo Song | Healthy Meal | Sick Song | Healthy Habits | Toddlers | Nursery Rhymes | Germs | Kids",
     "Genki Park", "7:21", "https://www.youtube.com/watch?v=xCJ8eHrNn88", "Today"),
    ("Healthy Habits - Nursery Rhymes - Healthy Meal - Potty Training - Brush your teeth - Kids - Todlers",
     "Genki Park", "7:01", "https://www.youtube.com/watch?v=jc4xVO_MIc4", "Today"),
    ("Sick Song | Cartoon for Kids | Nursery Rhymes | Healthy Habits | Genki Park | Be ill Song Toddlers",
     "Genki Park", "2:58", "https://www.youtube.com/watch?v=Dx-LG3oCzSM", "Today"),
    ("Peppa Learns About Nature! 🐷🐛 | @PeppaPigOfficial",
     "Peppa Pig - Official Channel", "36:00", "https://www.youtube.com/watch?v=4KJ7jhRUcfU", "Today"),
    ("Peppa Pig - Learning To Count 🔢 | Peppa Pig Educational Videos",
     "Peppa Pig - Official Channel", "1:55", "https://www.youtube.com/watch?v=UidDYQCQ_Mg", "Today"),
    ("Tom & Jerry em Português | Brasil | A Noite Divertida | WB Kids",
     "WB Kids Brasil", "26:59", "https://www.youtube.com/watch?v=sE26JzsCgEQ", "Today"),
    ("Dolly e Amigos Em Português Brasil Completo #1",
     "Dolly's Stories KIDS", "17:00", "https://www.youtube.com/watch?v=sb_LrzfFb8U", "Today"),
    ("Dolly e Amigos Em Português Brasil Completo #5",
     "Dolly e Amigos - Brasília", "17:00", "https://www.youtube.com/watch?v=4tAUm5O7jZQ", "Today"),
    ("Dolly e Amigos Em Português Brasil Completo #23",
     "Dolly's Stories KIDS", "17:00", "https://www.youtube.com/watch?v=ScvWPMsDJpM", "Today"),
    ("Dolly e Amigos Novos desenhos animados para crianças Episódios engraçados #348 Full HD",
     "Dolly & Amigos em Português - Brasil", "17:00", "https://www.youtube.com/watch?v=0Ve3lu9ZJ5k", "Today"),

    # ── YESTERDAY (Feb 20, 2026) ──────────────────────────────────────────────
    ("Pinkfong Wonderstar Characters In REAL LIFE! | 🎬 Favorite Movies, Foods 🍕 & More | Hogi, Jeni...",
     "Great Quiz", "16:00", "https://www.youtube.com/watch?v=wbR8eUYukEM", "Yesterday"),
    ("Robocar Poli Characters as Babies 👶🔥 + Guess the Voice Quiz | Roy, Amber, Poli, Kevin, Jin...",
     "Great Quiz", "15:00", "https://www.youtube.com/watch?v=aPuyj7lKFpM", "Yesterday"),
    ("Little Baby Bum in REAL LIFE 👩⭐ + Guess The Voice Quiz ~ Mia, Max, Twinkle Twinkle Little Star...",
     "Great Quiz", "15:00", "https://www.youtube.com/watch?v=a5jBK5cXwb0", "Yesterday"),
    ("Mickey Mouse Clubhouse Characters and their favorite Snacks, Drinks, Movies & More! | Goofy, Pluto",
     "Blaze Galaxy", "17:00", "https://www.youtube.com/watch?v=vYESWbYo478", "Yesterday"),
    ("SpongeBob SquarePants Characters And Their Favorite SNACKS, DRINKS & (Other Favorites) | Mr. Krabs",
     "Blaze Kingdom", "9:04", "https://www.youtube.com/watch?v=If8bUnw_X4I", "Yesterday"),
    ("🐽 Peppa Pig Characters And Their Favorite Snacks Drinks & More! | Evie Pig, Peppa Pig, Mummy Pig",
     "Blaze Kingdom", "18:00", "https://www.youtube.com/watch?v=Z6m-F05pyZI", "Yesterday"),
    ("Brush Your Teeth - Eat Healthy - Boo Boo - #healthyhabits - kindergarten learning videos",
     "Genki Park", "6:55", "https://www.youtube.com/watch?v=x4ODGifsN7w", "Yesterday"),
    ("Wash your hands - Brush your teeth - Boo Boo Song - Healthy Habits - Nursery Rhymes - Kids Songs",
     "Genki Park", "6:22", "https://www.youtube.com/watch?v=8uZW6-fukrU", "Yesterday"),
    ("22 min 5 Books of David's adventures - Animated Read Aloud Books",
     "Reading is", "22:00", "https://www.youtube.com/watch?v=fNogleSaFNQ", "Yesterday"),
    ("Cocomelon Play with JJ - Full Game Walkthrough",
     "AbdallahKids", "59:00", "https://www.youtube.com/watch?v=Nmb1B5t7VKg", "Yesterday"),
    ("30 Minutes Leslie Patricelli Storytime Collection|ReadAloud|Toot|pottytrain|Little Libraryprek kids",
     "Bright Star Storytime", "30:00", "https://www.youtube.com/watch?v=jrGxQxeAMk8", "Yesterday"),
    ("Leslie Patricelli Little Library 📚 | Toddler Read-Aloud with Learning Reflections | Hoots and Tales",
     "Hoots & Tales", "21:00", "https://www.youtube.com/watch?v=y3hMcoabv2Y", "Yesterday"),
    ("Feelings with Leslie Patricelli 💛 | Toddler Read-Aloud Compilation | Emotions & Empathy",
     "Hoots & Tales", "11:17", "https://www.youtube.com/watch?v=kwrXXCAhywI", "Yesterday"),
    ("1 Hour Leslie Patricelli Storytime Collection| Baby Life, Feelings, Seasons Bedtime Books|Read aloud",
     "Bright Star Storytime", "51:00", "https://www.youtube.com/watch?v=wpQDrR7p_Ko", "Yesterday"),
    ("Pinkfong Wonderstar ✨ Characters & Their Favorite Drinks, Snacks + More! | Pinkfong & Poki",
     "Blaze Kingdom", "9:18", "https://www.youtube.com/watch?v=TAPYzTJeNGc", "Yesterday"),
    ("🥕🔢 Numberblocks Reimagined as Vegetables 🌽✨ | A Fun Healthy Learning Adventure for Kids!",
     "Melon TV Fun", "10:14", "https://www.youtube.com/watch?v=J8y2L6igV80", "Yesterday"),
    ("Pinkfong Wonderstar ⭐ In REAL LIFE!💫 | Mr. Snake's 🎬 Favorite Movies, Foods 🍕 & More | Hogi, Jeni",
     "Blaze Kingdom", "10:41", "https://www.youtube.com/watch?v=DHkKQZqJOuk", "Yesterday"),
    ("🔢Numberblocks Reimagined as Babies! 🍼👶 | Adorable Math Fun for Kids",
     "Melon TV Fun", "10:16", "https://www.youtube.com/watch?v=SNO60eHLSMs", "Yesterday"),
    ("Number Blocks🔢 Cartoon Characters And Their Favorite Drinks, Movies & More! | Four, One, Zero, Seven",
     "Blaze Universe", "9:04", "https://www.youtube.com/watch?v=ocSY07nJ6eU", "Yesterday"),
    ("Peppa Pig 🐽 Characters and their Favorite Drinks, Fruits & More! | Evie, Peppa, Mummy, Daddy pig",
     "Blaze Kingdom", "9:05", "https://www.youtube.com/watch?v=vFPhrBITX0k", "Yesterday"),
    ("Baby Panda with Magic Words | Antonyms & Contrast | Gameplay Video | BabyBus Game",
     "BabyBus - Kids Songs and Cartoons", "17:00", "https://www.youtube.com/watch?v=ceUpDI_47nw", "Yesterday"),
    ("Tom and Jerry | Mega Compilation | Vol. 10 | The Spike Series | Warner Classics",
     "Warner Bros. Classics", "54:00", "https://www.youtube.com/watch?v=qsKqoYM7uk8", "Yesterday"),
    ("100 Action Words in English 🥳 for Kids | Daily Use Sentences | Adi Keshari Connection",
     "Adi Connection", "6:09", "https://www.youtube.com/watch?v=oyUyjxmaU_Q", "Yesterday"),
    ("Making Funny Pizza Faces! 🍕 | Peppa Pig Official Full Episodes",
     "Peppa Pig - Official Channel", "31:00", "https://www.youtube.com/watch?v=C1I_8D5NlXw", "Yesterday"),
    ("Let's Do Magic on Glass 🎨 DIY Window Art & Craft for Kids | Adi Connection",
     "Adi Connection", "10:40", "https://www.youtube.com/watch?v=_bsH6Y_6UrA", "Yesterday"),
    ("Kids Vocabulary for Everyday Use 😱, Learn English with Adi & Mini, Adi Connection",
     "Adi Connection", "3:41", "https://www.youtube.com/watch?v=ulWZioJA9Ig", "Yesterday"),
    ("Guess What I Am 🤔 | English Riddles for Kids | Adi Keshari Connection",
     "Adi Connection", "2:28", "https://www.youtube.com/watch?v=oajFmF32B4k", "Yesterday"),
    ("Sago Mini Babies Read Aloud 📖👶 | Read Along Stories for Kids | Sago Mini Storytime",
     "Sago Mini", "8:18", "https://www.youtube.com/watch?v=2B71s7-_uKk", "Yesterday"),
    ("🎹 Baby piano and music games for kids and toddlers 🎹",
     "Top Best Apps Planet", "10:06", "https://www.youtube.com/watch?v=g1GYG2REnUU", "Yesterday"),
    ("Peppa Pig - Learn Numbers With Peppa Pig - Learning with Peppa Pig",
     "Peppa Pig's Pretend Play", "29:00", "https://www.youtube.com/watch?v=DAyMLvJQiSo", "Yesterday"),
    ("Toca Boca Intro Compilation with Games Icon ❤️❤️❤️🍒🍒🍒",
     "Yrrrech OG 33", "3:38", "https://www.youtube.com/watch?v=SDUhwToRyq0", "Yesterday"),
    ("Toca Boca intro EDIT! Check it out, super funny!!!",
     "Sunset Toca ☀️", "2:01", "https://www.youtube.com/watch?v=Its2Y8Kf3gM", "Yesterday"),
    ("Baby Panda Care - Take Care of the Baby Panda Miu Miu and Help her Grow Up Healthy | BabyBus Games",
     "Daja Kids Games", "16:00", "https://www.youtube.com/watch?v=y9uTvTgPK-o", "Yesterday"),
    ("Guess The Early Learning App Logo Sound 🔊🧠 | Khan Academy Kids, Duolingo ABC, Sago Mini",
     "Quiz Noke", "7:03", "https://www.youtube.com/watch?v=MVTRLlkiVXQ", "Yesterday"),
    ("EVOLUTION OF TOCA BOCA WORLD | Trailers | New VS Old",
     "StoryBoca", "39:00", "https://www.youtube.com/watch?v=Fnt4pkJeDCI", "Yesterday"),
    ("Baby Panda Care | Baby Care | Game for Kids | Kids Cartoon | BabyBus - Kids Songs and Cartoons",
     "BabyBus - Kids Songs and Cartoons", "9:49", "https://www.youtube.com/watch?v=2q5WbknI_EM", "Yesterday"),
    ("Baby Supermarket Shopping | Pretend Play | Kids Cartoon | Animation For Kids | BabyBus",
     "BabyBus - Kids Songs and Cartoons", "6:27", "https://www.youtube.com/watch?v=HlfRarTcuNI", "Yesterday"),
    ("Baby Panda's Safety Journey: Learn Crucial Safety Tips at Home & While Traveling - Educational Game",
     "KidsBabyBus HD", "16:00", "https://www.youtube.com/watch?v=RSOiMFH8duo", "Yesterday"),
    ("NEW! Sago Mini School FULL | Kitchen, Rainbows | Kids Game Preschool",
     "Sago Fun Games for Kids", "10:25", "https://www.youtube.com/watch?v=fJSs3myiNXY", "Yesterday"),
    ("Feelings - Emotional Growth ｜Learn to understand others' feelings｜BabyBus Kids Games",
     "BabyBus - Kids Songs and Cartoons", "10:18", "https://www.youtube.com/watch?v=706c5-Ndvi0", "Yesterday"),
    ("New bandmaster game on Piano Kids game - Music maestro game for kids - Educational game for kids",
     "Gameplay Everyday", "11:35", "https://www.youtube.com/watch?v=OtxhOK3pxCA", "Yesterday"),
    ("My Friend Peppa Pig Full PS5 Gameplay Walkthrough (Longplay) Next Gen Upgrade",
     "XCageGame", "1:30:00", "https://www.youtube.com/watch?v=GyehualmD2I", "Yesterday"),
    ("my friend Peppa pig (PC) Longplay",
     "Game Vault", "2:13:00", "https://www.youtube.com/watch?v=iEGppWmntaU", "Yesterday"),
    ("Peppa Pig World Adventures | Full Gameplay | Walkthrough | 100% | No Commentary | ENGLISH",
     "Games and fun with Palmi & Mino", "3:28:00", "https://www.youtube.com/watch?v=VLkPumasbCY", "Yesterday"),
    ("Numberblocks and Their Favorite Snacks, Drinks, Movies & More! | One, Two, Three",
     "Blaze Kingdom", "9:01", "https://www.youtube.com/watch?v=mMeYuHS8UM8", "Yesterday"),
    ("NUMBER BLOCKS CHARACTERS AND THEIR FAVORITE YOUTUBE SERIES!",
     "Blaze Toon", "2:13", "https://www.youtube.com/watch?v=wQPivCaYqmI", "Yesterday"),
    ("The Colors Song ~ Learn the Colors / Colours ~ LEARN ENGLISH with Natural English ~ LEARN VOCABULARY",
     "Natural English", "2:58", "https://www.youtube.com/watch?v=pUPM3DtK9so", "Yesterday"),
    ("Bedtime with Leslie Patricelli 🌙 | Toddler Read-Aloud Compilation | Comfort & Routines",
     "Hoots & Tales", "9:23", "https://www.youtube.com/watch?v=hsPoVXIsV4Q", "Yesterday"),
    ("Baby Panda's Candy Shop was Stolen | Baby Panda Sheriff | Policeman Pretend Play | BabyBus",
     "BabyBus - Kids Songs and Cartoons", "34:00", "https://www.youtube.com/watch?v=5EGmizOPnkk", "Yesterday"),
    ("Neo Needs to Go Potty! | My Turn My Turn | Good Habits | Nursery Rhymes & Kids Songs | BabyBus",
     "BabyBus - Kids Songs and Cartoons", "23:00", "https://www.youtube.com/watch?v=eWmC4G9tG-4", "Yesterday"),
    ("Take Care of Little Baby 👶 | Kids Cartoon | Animation For Kids | Nursery Rhymes | BabyBus",
     "BabyBus - Kids Songs and Cartoons", "5:01", "https://www.youtube.com/watch?v=KIZoqJHshTI", "Yesterday"),
    ("Minions are watching Toca Boca Intros for 4min. | TocaFun😘",
     "TocaFun", "4:32", "https://www.youtube.com/watch?v=Q4xHOeFXYvU", "Yesterday"),
    ("Peppa Pig Golden Boots,Fun Fair,Happy Mrs Chicken,Holiday,Sports Day, Party Time,Polly Parrot,Hippo",
     "GamePlay Adventure", "23:00", "https://www.youtube.com/watch?v=5oV_sKr7quU", "Yesterday"),
    ("Peppa Pig Official Channel | Making Birthday Cake with Peppa Pig",
     "Peppa's Best Bites", "10:05", "https://www.youtube.com/watch?v=Ek6NnCT_Hng", "Yesterday"),
    ("Peppa Pig - Dress up Peppa Pig - Learn Colouring - Learning with Peppa Pig",
     "Peppa Pig's Pretend Play", "10:50", "https://www.youtube.com/watch?v=yi56hE8fQD4", "Yesterday"),
    ("Drive My Cool School Bus: Ready for a Fun Ride to School?",
     "KidsBabyBus HD", "10:00", "https://www.youtube.com/watch?v=1XwNIejlMkk", "Yesterday"),
    ("Kids Learn How to Share | My Turn My Turn | Sharing Song | Nursery Rhyme & Kids Songs | BabyBus",
     "Master's 10k", "5:44", "https://www.youtube.com/watch?v=wm30tw097Vg", "Yesterday"),
    ("Baby Panda School Bus #1 - Gameplay Walkthrough",
     "ROBIXX GAMING", "14:00", "https://www.youtube.com/watch?v=KAIwHmIs3WE", "Yesterday"),
    ("Peppa Pig ABC Dance Song",
     "FunToyLand - Toys & Learning", "3:11", "https://www.youtube.com/watch?v=sco8lUG_7Lw", "Yesterday"),
    ("Learn Alphabets A to Z with Peppa Pig | Kidzstation Fun Academy",
     "Kidzstation Fun Academy", "9:05", "https://www.youtube.com/watch?v=7W9dQIyikU0", "Yesterday"),
    ("Peppa English Episodes | Peppa Pig Alphabet | Peppa Pig Characters | Learn With Peppa Pig | ABCD",
     "Kidsquad", "10:15", "https://www.youtube.com/watch?v=3nOafpZKybc", "Yesterday"),
    ("Peppa Pig Characters | Peppa Pig Characters in Real life | Learn Animals With Peppa And George |",
     "Kidsquad", "3:22", "https://www.youtube.com/watch?v=KAF2x31_bSE", "Yesterday"),
    ("Kids Learn 123 Counting Numbers from 1 to 10 with Elmo Loves 123s Part 1 – Play Doh Games",
     "Learn English on a Daily Basis", "15:00", "https://www.youtube.com/watch?v=Dpa7lCYg6iM", "Yesterday"),
    ("Cocomelon Little Pocket Library: Read Aloud 6 Book Collection for Children and Toddlers",
     "Shall We Read A Book?", "18:00", "https://www.youtube.com/watch?v=NL3AZ57hqh8", "Yesterday"),
    ("4 Big Box of Books 📚 | CoComelon, Peppa, Bluey & More | Family & Friends Read Aloud Stories",
     "Hoots & Tales", "24:00", "https://www.youtube.com/watch?v=bGAI78WI_pg", "Yesterday"),
    ("How To Make PBS Kids Dash Logo Effects Sponsored By Preview 2 Effects On KineMaster",
     "Gerrard", "15:00", "https://www.youtube.com/watch?v=JUA2VHuwtw0", "Yesterday"),
    ("PBS Kids ID (I Voice Del, Dee & Dot)",
     "Tye The Cool Guy", "7:06", "https://www.youtube.com/watch?v=l3H5Jqcp-1Q", "Yesterday"),
    ("PBS Kids ID / System Cue Compilation (1999-2022)",
     "Peeebs", "5:37", "https://www.youtube.com/watch?v=2sQ1JQKrOe4", "Yesterday"),
    ("My Kindergarten - Panda Games｜Fall in love Kindergarten｜To overcome the psychological fear",
     "BabyBus - Kids Songs and Cartoons", "10:16", "https://www.youtube.com/watch?v=tN6q6HuU3r0", "Yesterday"),
    ("Peppa Pig - Happy Mrs Chicken gameplay (app demo)",
     "Peppa Pig - Official Channel", "18:00", "https://www.youtube.com/watch?v=2Mxs3VDxQfI", "Yesterday"),
    ("Peppa Pig Goes Shopping 🐷 Peppa Pig Shopping Gameplay",
     "Little Wonders TV", "19:00", "https://www.youtube.com/watch?v=zrrvo9NkS1I", "Yesterday"),
    ("Unboxing - CoComelon: Play with JJ - Nintendo Switch | Walkthrough | Kids Game",
     "Nintendo Games", "12:00", "https://www.youtube.com/watch?v=W90rAfCVfBM", "Yesterday"),
    ("Peppa Pig: World Adventures Nintendo Switch Gameplay",
     "Handheld Players", "20:00", "https://www.youtube.com/watch?v=jMsV_Raowys", "Yesterday"),
    ("PEPPA PIG WORLD ADVENTURES GAMEPLAY",
     "Little Wonders TV", "52:00", "https://www.youtube.com/watch?v=nxHH-NQMcWQ", "Yesterday"),
    ("Peppa Pig: World Adventures - Full Movie Gameplay",
     "rrvirus", "45:00", "https://www.youtube.com/watch?v=eCikDTKH3r4", "Yesterday"),
    ("Doggie Gets Scared | Leslie Patricelli | Animated Read Aloud for Kids | Emotions & Feelings preK",
     "Bright Star Storytime", "3:06", "https://www.youtube.com/watch?v=7AI_tiXPt3o", "Yesterday"),
    ("Leslie Patricelli Opposites Collection 13 Min | Animated Storytime for Toddlers & PreK | Read Aloud",
     "Bright Star Storytime", "13:05", "https://www.youtube.com/watch?v=tzjDOoOZpZE", "Yesterday"),
    ("CoComelon: Play with JJ | Gameplay | Nintendo Switch",
     "Nintendo Games", "15:00", "https://www.youtube.com/watch?v=ZWBNJVFMcU8", "Yesterday"),
    ("INTRO & TRAILERS OF TOCA BOCA | TOCA BOCA GAMES",
     "StoryBoca", "13:59", "https://www.youtube.com/watch?v=I9Ih_IBp-L0", "Yesterday"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO and Name 😍❤️‍🔥",
     "StoryBoca", "4:40", "https://www.youtube.com/watch?v=QmaLI2aA-dg", "Yesterday"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO AND NAME 🌎 2026",
     "Catoca", "6:11", "https://www.youtube.com/watch?v=YTn7M8u3FpQ", "Yesterday"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO AND NAME 🌎",
     "Catoca", "6:19", "https://www.youtube.com/watch?v=TGixZYDT1dw", "Yesterday"),
    ("ALL secret CRUMPETS in TOCA BOCA WORLD 🌎",
     "Catoca", "21:00", "https://www.youtube.com/watch?v=64qvi0BT2uU", "Yesterday"),
    ("THIS IS SOMETHING NEW!! 😍😱 Toca Boca Secrets and Gifts | Toca Boca World 🌏",
     "StoryBoca", "21:00", "https://www.youtube.com/watch?v=P5SLkZ3NvRg", "Yesterday"),
    ("The Peppa Pig 🐷Characters and their Favorite Snacks, Movies, and other Favorites! | Candy Cat",
     "Blaze Kingdom", "18:00", "https://www.youtube.com/watch?v=IRfXe7gQyfg", "Yesterday"),
    ("Little Panda School Bus - Drive a Bus And Explore The Journey To Kindergarten - Babybus Game Video",
     "KidsBabyBus HD", "14:51", "https://www.youtube.com/watch?v=MXS7junDP94", "Yesterday"),
    ("Real Life Peppa Pig Characters?! 🤯 + Their Favorite Snacks, Drinks, Moives And More | Evie Pig",
     "Blaze Kingdom", "16:00", "https://www.youtube.com/watch?v=lnPUUirFyog", "Yesterday"),
    ("Peppa Pig 🐽 Characters & Their Favorite Shows, Drinks & More! | Evie pig, Peppa pig, Mummy Pig",
     "Blaze Kingdom", "9:04", "https://www.youtube.com/watch?v=YvfaVP47tY4", "Yesterday"),
    ("Shopify (SHOP) Stock Earnings Call | Q4 2025 Breakdown",
     "Future Investing", "1:38:00", "https://www.youtube.com/watch?v=4jFV-WlL1QU", "Yesterday"),
    ("Eat Healthy - Broken Heart - Healthy Habits - Todlers - Preeschool - Learn English - Kids Songs",
     "Genki Park", "6:55", "https://www.youtube.com/watch?v=3JExXE5VKA8", "Yesterday"),
    ("CoComelon: Play With JJ Official Gameplay Video | 🔤 Moonbug Literacy 🔤",
     "Moonbug Literacy - Read Along with Captions", "12:00", "https://www.youtube.com/watch?v=cGVo4pLUSJw", "Yesterday"),
    ("Boo! 🎃 | Learning About Halloween & Having Fun | Read Aloud for Toddlers | Hoots & Tales",
     "Hoots & Tales", "3:11", "https://www.youtube.com/watch?v=2mGWjEpVvSw", "Yesterday"),
    ("Yes Yes! Box of Board Books 🎨 | Toddler Read-Aloud Compilation | Opposites, Behaviors & Fun",
     "Hoots & Tales", "8:53", "https://www.youtube.com/watch?v=1UmAGKlOHso", "Yesterday"),
    ("Lets Create a Birthday Dinner Party in our Toy Kitchen",
     "Rainybow Kids", "16:00", "https://www.youtube.com/watch?v=hqzbdR0FaUw", "Yesterday"),
    ("Peppa Pig - Let's Draw Peppa Pig - Learning with Peppa Pig",
     "Peppa Pig's Pretend Play", "31:00", "https://www.youtube.com/watch?v=HrptkizLUfQ", "Yesterday"),
    ("Mickey Mouse Clubhouse Characters As NEWBORN BABY 🔥 + Guess The Voice ~ Daisy Duck, Donald Duck",
     "Great Quiz", "8:54:00", "https://www.youtube.com/watch?v=HcwcpaI-Jmk", "Yesterday"),
    ("Gabby's Dollhouse Characters as Dogs ~ Guess the Voice Quiz | Gabby, DJ Catnip, Pandy Paws...",
     "Great Quiz", "17:00", "https://www.youtube.com/watch?v=G-7J5D6LFt8", "Yesterday"),
    ("Peppa Pig 🐽 Characters As Snakes 🐍 + Body Parts Quiz | Their Favorite Things! | Evie Pig, Suzy sheep",
     "Blaze Kingdom", "24:00", "https://www.youtube.com/watch?v=a7C28u3JWes", "Yesterday"),
    ("Sheriff Labrador Characters as Babies + Guess The Voice Quiz ~ Sheriff Labrador, Dobie...",
     "Great Quiz", "19:00", "https://www.youtube.com/watch?v=XQ9e_yf09rs", "Yesterday"),
    ("My Friend Peppa Pig Full Gameplay Walkthrough (Longplay)",
     "XCageGame", "1:05:00", "https://www.youtube.com/watch?v=o8qkqlVjSYM", "Yesterday"),
    ("Toca Boca Vlog | Rich Family Night Routine 🌙 | Toca Life World | Game Vlog 👾 | iPad Pro",
     "CandyCute Channel", "21:00", "https://www.youtube.com/watch?v=KFUJoA1F7no", "Yesterday"),
    ("GUESS THE GAME! | Toca Boca | Toca Life World | Avatar World",
     "Jossi Wossi", "12:03", "https://www.youtube.com/watch?v=4FV3Cnud5l0", "Yesterday"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO 😍❤️‍🔥",
     "StoryBoca", "4:24", "https://www.youtube.com/watch?v=GB-R--6hY4w", "Yesterday"),
    ("Guess The Early Learning App Logo Sound 🔊 | ABCmouse, Duolingo ABC, Khan Academy Kids & More 2026 🎵",
     "ZIZOQUIZ", "8:02", "https://www.youtube.com/watch?v=YFd3Y7vyEI0", "Yesterday"),
    ("Guess The Shopping Logo Sound 🛒🔊 | IKEA, Walmart, Carrefour, Decathlon | Family Quiz 2026",
     "ZIZOQUIZ", "8:14", "https://www.youtube.com/watch?v=bZBwbjFSs7I", "Yesterday"),
    ("LEGO DUPLO PEPPA PIG | New Episodes Dr. Brown Bear⭐",
     "RRKids and 3 more", "8:47", "https://www.youtube.com/watch?v=3EKtflSzoQ4", "Yesterday"),
    ("Every Daniel tiger feeling strategy songs",
     "Daniel Tiger by Phoebe Cresswell", "25:00", "https://www.youtube.com/watch?v=Afz3s7ikdD4", "Yesterday"),
    ("Tom & Jerry | Tom & Jerry in Full Screen | Classic Cartoon Compilation | WB Kids",
     "WB Kids", "21:00", "https://www.youtube.com/watch?v=t0Q2otsqC4I", "Yesterday"),
    ("Tom and Jerry | Mega Compilation | Vol. 1 | Warner Classics",
     "Warner Bros. Classics", "47:00", "https://www.youtube.com/watch?v=j-88jrkyszQ", "Yesterday"),
]

# Shorts extracted (no duration info — assumed ~0:45 each)
SHORTS = [
    # Today batch 1
    ("/shorts/m0bstpDyat4", "Today"), ("/shorts/HXYiep8COkY", "Today"),
    ("/shorts/aBmf2XHApjE", "Today"), ("/shorts/eAUtg0e-7BM", "Today"),
    ("/shorts/7x2ZD8BEqAg", "Today"), ("/shorts/u6Ofy0HCljY", "Today"),
    # Today batch 2
    ("/shorts/E3wUJnNP22M", "Today"), ("/shorts/Vb_nNbroHPs", "Today"),
    ("/shorts/iPo_6-E6RtM", "Today"), ("/shorts/WSM_Y-oPg-c", "Today"),
    ("/shorts/Z4zPl2iCYfI", "Today"), ("/shorts/8jQxmAmFYf0", "Today"),
    # Yesterday batches
    ("/shorts/eZq9uktzcYc", "Yesterday"), ("/shorts/1GtPF_dwJ-g", "Yesterday"),
    ("/shorts/n0pUjKgPW8A", "Yesterday"), ("/shorts/M2WjwH2m8pQ", "Yesterday"),
    ("/shorts/Q3_Hx5_LwG0", "Yesterday"), ("/shorts/5F7B77GTxU8", "Yesterday"),
    ("/shorts/wGd4gyH4HK4", "Yesterday"), ("/shorts/lxxzUmT7g7Q", "Yesterday"),
    ("/shorts/blT_kOwudZ0", "Yesterday"), ("/shorts/rAyhKBsfUlA", "Yesterday"),
    ("/shorts/O8AAuyT93OA", "Yesterday"), ("/shorts/sNwEbXPJ3OQ", "Yesterday"),
    ("/shorts/X-u2FZ9EgsQ", "Yesterday"), ("/shorts/tW2sy7ZIsaM", "Yesterday"),
    ("/shorts/8GI59vaoe2c", "Yesterday"), ("/shorts/6BBhr--WFRQ", "Yesterday"),
    ("/shorts/_Vr1800eT9M", "Yesterday"), ("/shorts/s8Q0deyETsk", "Yesterday"),
]


def parse_duration(s: str) -> int:
    """Convert duration string to seconds."""
    if not s:
        return 600  # default 10 min
    parts = s.split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return 600


def section_to_iso(section: str) -> str:
    """Map section label to ISO timestamp."""
    date_map = {
        "Today": "2026-02-21T14:00:00-05:00",
        "Yesterday": "2026-02-20T14:00:00-05:00",
    }
    return date_map.get(section, "2026-02-19T14:00:00-05:00")


# De-duplicate by URL
seen_urls = set()
unique_videos = []
for title, channel, duration_raw, url, section in RAW_VIDEOS:
    base_url = url.split("&")[0].split("?")[0] + "?" + (url.split("?")[1].split("&")[0] if "?" in url else "")
    # Normalize: strip timestamp params
    vid_id = url.split("watch?v=")[-1].split("&")[0] if "watch?v=" in url else url
    if vid_id not in seen_urls:
        seen_urls.add(vid_id)
        unique_videos.append((title, channel, duration_raw, url, section))

# Build video objects
videos = []
for title, channel, duration_raw, url, section in unique_videos:
    dur_sec = parse_duration(duration_raw)
    videos.append({
        "title": title,
        "channel": channel,
        "url": url,
        "duration_raw": duration_raw,
        "duration_seconds": dur_sec,
        "timestamp": section_to_iso(section),
        "section_date": section,
    })

# Add shorts
for short_path, section in SHORTS:
    videos.append({
        "title": f"Short: {short_path.split('/')[-1]}",
        "channel": "Unknown",
        "url": f"https://www.youtube.com{short_path}",
        "duration_raw": "0:45",
        "duration_seconds": 45,
        "timestamp": section_to_iso(section),
        "section_date": section,
        "is_short": True,
    })

total_seconds = sum(v["duration_seconds"] for v in videos)
total_minutes = round(total_seconds / 60, 1)

# Channel counts
channel_counter = Counter(v["channel"] for v in videos)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counter.most_common(10)]

# Category heuristics
def categorize(v):
    t = (v["title"] + " " + v["channel"]).lower()
    if any(k in t for k in ["read aloud", "storytime", "book", "stories"]):
        return "Read Aloud / Storytime"
    if any(k in t for k in ["peppa pig", "peppa"]):
        return "Peppa Pig"
    if any(k in t for k in ["babybus", "baby panda", "kiki", "miu miu"]):
        return "BabyBus"
    if any(k in t for k in ["toca boca", "toca life"]):
        return "Toca Boca"
    if any(k in t for k in ["tom and jerry", "tom & jerry", "wb kids"]):
        return "Tom & Jerry / WB Kids"
    if any(k in t for k in ["nursery rhyme", "kids song", "genki park", "healthy habits"]):
        return "Nursery Rhymes / Kids Songs"
    if any(k in t for k in ["gameplay", "walkthrough", "longplay", "game"]):
        return "Gameplay / Walkthrough"
    if any(k in t for k in ["numberblocks", "pinkfong", "cocomelon", "bluey"]):
        return "Educational Cartoons"
    if any(k in t for k in ["learn", "abc", "alphabet", "counting", "educational"]):
        return "Educational / Learning"
    if "short" in v.get("title", "").lower() or v.get("is_short"):
        return "Shorts"
    return "Other"

cat_counter = Counter(categorize(v) for v in videos)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in cat_counter.most_common(10)]

# Hourly / daily counts (estimated distribution — no actual timestamps)
hourly_counts = {str(h): 0 for h in range(24)}
daily_counts = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
for v in videos:
    if v["section_date"] == "Today":  # Saturday Feb 21
        daily_counts["Sat"] += 1
        hourly_counts["14"] += 1
    else:  # Friday Feb 20
        daily_counts["Fri"] += 1
        hourly_counts["13"] += 1

history = {
    "generated": "2026-02-21T20:00:00-05:00",
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
print(f"✅ Wrote {len(videos)} videos to {OUT}")
print(f"📺 Total watch time: {total_minutes:.1f} minutes")
print(f"📊 Top channels: {[c['channel'] for c in top_channels[:3]]}")
