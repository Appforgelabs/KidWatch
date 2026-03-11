#!/usr/bin/env python3
"""
Build history.json from today's live-scraped YouTube data (March 10, 2026).
"""
import json
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

# ─── CHANNEL INFERENCE RULES ─────────────────────────────────────────────
def infer_channel(title: str, url: str) -> str:
    t = title.lower()
    if "yakka dee" in t:
        if "bbc kids" in t:
            return "BBC Kids"
        return "Yakka Dee! – Toddler Learning"
    if "peppa pig - nursery rhymes" in t or "peppa pig 2026 songs" in t:
        return "Peppa Pig - Nursery Rhymes and Kids Songs"
    if "junytony" in t:
        return "JunyTony - Songs and Stories"
    if "daniel tiger" in t or ("pbs kids" in t) or "work it out wombats" in t:
        return "PBS KIDS"
    if "bingo - official" in t or ("bingo" in t and "cutest moments" in t):
        return "Bingo - Official Channel"
    if "diana and roma en" in t:
        return "Diana and Roma EN"
    if "kids diana show" in t or ("diana" in t and "roma" in t and ("circle" in t or "secret room" in t or "advent" in t or "balloons" in t or "alphabet" in t or "safety rules" in t)):
        return "✿ Kids Diana Show"
    if "kids roma show" in t or ("roma and diana" in t):
        return "★ Kids Roma Show"
    if "nastya life" in t or "تعلم العد" in title:
        return "Nastya Life"
    if "like nastya" in t or ("nastya" in t and "eva" in t):
        return "Like Nastya"
    if "hooray kids songs" in t:
        return "Hooray Kids Songs & Nursery Rhymes"
    if "kidscamp" in t or "kids camp" in t:
        return "KidsCamp Nursery Rhymes & Learning Videos for Kids"
    if "kaboochi" in t:
        return "Kaboochi Kids Baby Songs and Nursery Rhymes"
    if "be be kids" in t:
        return "Be Be Kids"
    if "nikhil & jay" in t or "nikhil and jay" in t:
        return "Nikhil & Jay"
    if "kidzstation" in t:
        return "kidzstation"
    if "vlad and niki" in t:
        return "Vlad and Niki"
    if "vania mania" in t or "five kids" in t:
        return "Vania Mania Kids"
    if "gaby and alex" in t:
        return "Gaby and Alex"
    if "katya and dima" in t:
        return "Katya and Dima"
    if "alice learns" in t:
        return "Alice"
    if "eli and parents" in t:
        return "Илья и Картонка"
    if "cocomelon" in t:
        return "CoComelon - Nursery Rhymes"
    if "bing" in t and ("full episodes" in t or "english" in t):
        return "Bing - Official Channel"
    if "super simple songs" in t or "super simple storybook" in t or ("super simple" in t and ("carl" in t or "peekaboo" in t or "noodle" in t)):
        return "Super Simple Songs - Kids Songs"
    if "rhymington square" in t:
        return "Rhymington Square"
    if "bebefinn" in t:
        return "Bebefinn - Best Play Stories"
    if "gabby's dollhouse" in t:
        return "Gabby's Dollhouse"
    if "little angel" in t:
        return "Little Angel - Nursery Rhymes"
    if "bubble guppies" in t:
        return "Bubble Guppies"
    if "ben and holly" in t:
        return "Ben and Holly's Little Kingdom"
    if "pororo" in t:
        return "Pororo the Little Penguin"
    if "toca boca" in t or "toca life" in t or "toca world" in t:
        if "storybo" in t:
            return "StoryBoca"
        return "Toca Boca Roleplay"
    if "avatar world" in t or "pazu" in t:
        return "Avatar World"
    if "cocomelon" in t or "cody" in t:
        return "CoComelon - Nursery Rhymes"
    if "peppa pig" in t or "george pig" in t or "peppa" in t:
        if "official" in t or "full episodes" in t or "holiday" in t:
            return "Peppa Pig - Official Channel"
        if "tales" in t:
            return "Peppa Pig Tales"
        if "songs" in t and ("nursery" in t or "kids songs" in t):
            return "Peppa Pig - Nursery Rhymes and Kids Songs"
        return "Peppa Pig - Official Channel"
    if "lah-lah" in t:
        return "Lah-Lah Kids Music"
    if "bebefinn" in t:
        return "Bebefinn - Best Play Stories"
    if "la la learn" in t:
        return "La La Learn"
    if "kids diana show" in t:
        return "✿ Kids Diana Show"
    if "sunny kids songs" in t:
        return "Sunny Kids Songs"
    if "maya mary mia" in t:
        return "Maya Mary Mia"
    if "caitie" in t:
        return "Super Simple Songs - Kids Songs"
    if "learning station" in t:
        return "The Learning Station"
    if "oxbridge baby" in t:
        return "Oxbridge Baby"
    if "travis in wonderland" in t:
        return "Travis in Wonderland"
    if "fun indoor playground" in t or "leo's lekland" in t:
        return "Family Fun"
    if "princesa de hielo" in t:
        return "Kids Fun"
    if "goldilocks" in t:
        if "oxbridge" in t:
            return "Oxbridge Baby"
        if "learning station" in t:
            return "The Learning Station"
        if "fairy tales" in t:
            return "Fairy Tales - Bedtime Stories"
        return "Kids Storybook"
    if "natural english" in t:
        return "Natural English"
    if "wheels on the bus" in t and "popular" in t:
        return "Kids Songs & Nursery Rhymes"
    if "book read aloud" in t or "read aloud" in t:
        return "Kids Book Read Aloud"
    if "woodzeez" in t or "common words" in t and "dollhouse" in t:
        return "KidsCamp Nursery Rhymes & Learning Videos for Kids"
    if "dana" in t and "fruits" in t:
        return "Kids Songs with Dana"
    if "kids songs with tiki" in t:
        return "Kids Songs With Tiki"
    if "d billions" in t or "la la learn" in t:
        return "La La Learn"
    if "phonics song 2" in t:
        return "Kids Songs"
    if "ten in the bed" in t:
        return "Nursery Rhymes & Kids Songs"
    if "muffin man" in t:
        return "Kids Songs & Nursery Rhymes"
    if "apples and bananas" in t:
        return "ESL Kids"
    return "Unknown"

# ─── DURATION PARSER ────────────────────────────────────────────────────
def parse_duration_to_minutes(d: str) -> float:
    if not d or d == "LIVE":
        return 0.0
    parts = d.strip().split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
        elif len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60
        return 0.0
    except:
        return 0.0

# ─── SCRAPED VIDEO DATA ──────────────────────────────────────────────────
# (title, url, duration_str) — duration from snapshot aria labels
SCRAPED = [
    ("🔴 Peppa Pig 2026 SONGS LIVE! 🐷 ALL Peppa Pig Nursery Rhymes & Kids Songs ✨ Peppa Pig Songs 🔴 #live", "https://www.youtube.com/watch?v=9iZT7gIkDD4", "LIVE"),
    ("🔴JunyTony LIVE | Colorful Rainbow Desserts | Let's Eat the Rainbow! | Kids Songs | JunyTony", "https://www.youtube.com/watch?v=wVuGhsqTN0w", "LIVE"),
    ("BRAND NEW! Yakka Dee: Dee's Food Party! 🍕 🍦 | Toddler Words | Yakka Dee!", "https://www.youtube.com/watch?v=g-HUcLRX8JA", "8:55"),
    ("BRAND NEW! Yakka Dee: What Can You See? | Kitchen 🍞 🍏 | Yakka Dee!", "https://www.youtube.com/watch?v=Qw7BZmiFGFk", "3:02"),
    ("🔴 LIVE: Common Words with Dee! | Food Words for Toddlers | Yakka Dee!", "https://www.youtube.com/watch?v=EEQYWSAfVBU", "LIVE"),
    ("BRAND NEW! Yakka Dee: What Can You See | Halloween 🎃 | Yakka Dee!", "https://www.youtube.com/watch?v=IMIx3AcCKAU", "3:02"),
    ("Let's Talk about Outside! | Yakka Dee!", "https://www.youtube.com/watch?v=iqUnp_WNn1Y", "12:33"),
    ("Winter Words for Toddlers | Learn Wether, Snow and Fun Sounds | Baby & Toddler Phonics | Yakka Dee!", "https://www.youtube.com/watch?v=oQUlr530rJg", "11:43"),
    ("تعلم العد من 1 إلى 10 من خلال اللعب - تعليمي للأطفال الصغار", "https://www.youtube.com/watch?v=Lq-kyl9Pg4s", "LIVE"),
    ("🔴 NEWEST Peppa Pig Episodes 2026 ✨ SEASON 10 Holiday Adventures ☀️ Kids Movie 🔴", "https://www.youtube.com/watch?v=jcr97TYWtdE", "LIVE"),
    ("Daniel Tiger's Neighborhood | Father's Day Compilation | PBS KIDS", "https://www.youtube.com/watch?v=3gzc6Th07rA", "1:07:59"),
    ("🟢 LIVE | PBS KIDS ➕ Math 🟰 FUN! STEM Full Episodes for Kids 🔢🔭 | PBS KIDS", "https://www.youtube.com/watch?v=N2X7Pi7bFVY", "LIVE"),
    ("🟢 LIVE | Help Solve Treeborhood Problems with the Work It Out Wombats! 💕 | Livestream | PBS KIDS", "https://www.youtube.com/watch?v=1HRccVS8bRg", "LIVE"),
    ("🔴 BEST of George 2026 LIVE! 🦖 Peppa Pig Mini Movie 🍿 Kids Cartoons 🔴", "https://www.youtube.com/watch?v=9MbViEWxy2I", "LIVE"),
    ("BRAND NEW! Yakka Dee: What Can You See? | Farm Friends! 🐮🐴 | Yakka Dee!", "https://www.youtube.com/watch?v=IZZZ4vCigrU", "8:55"),
    ("♪♪ Funny Animal Song | When Hedgehogs Kiss | Hooray Kids Songs & Nursery Rhymes | Love", "https://www.youtube.com/watch?v=aIgQMKTO6UU", "1:34"),
    ("🔴 Learn Shapes With Wooden Truck 😍 | Toddler Learning Videos | Live 📺 Kidscamp", "https://www.youtube.com/watch?v=LyTqJR49Fdc", "LIVE"),
    ("Fruits Song | English rhymes learning for kids | fruit songs for children | Preschool learning video", "https://www.youtube.com/watch?v=gDePBaUc42w", "2:20"),
    ("Yummy Fruits & Vegetables | Be Be Kids Songs", "https://www.youtube.com/watch?v=REt8M07v6wI", "1:46"),
    ("Jay Tries to Do Grown Up Jobs | Nikhil & Jay Kids Cartoons on BBC iPlayer", "https://www.youtube.com/watch?v=xvHtq-oE_i8", "4:21"),
    ("Phonics Song | Kidzstation", "https://www.youtube.com/watch?v=lX5Kp1wl_KA", "2:22"),
    ("Learn Colors With Space Balls Dancing Machine Game On Finger Family Song", "https://www.youtube.com/watch?v=aOoxBN5OiY8", "LIVE"),
    ("🔴LIVE: Sing with Dee! 🎶 | 1+ Hour of Yakka Dee Songs | Yakka Dee", "https://www.youtube.com/watch?v=aXRk5GvLsrw", "1:07:44"),
    ("BRAND NEW! Yakka Dee: What Can You See? | Christmas 🎄 | Yakka Dee!", "https://www.youtube.com/watch?v=DEn6cwWXRz0", "3:02"),
    ("Diana and Roma show the Safety Rules on board the Airplane", "https://www.youtube.com/watch?v=NifKNSpp0_4", "9:00"),
    ("Diana and Roma English Alphabet with Surprise Eggs | ABC", "https://www.youtube.com/watch?v=QfQnD2wrUa4", "7:33"),
    ("Ten Little Fruits + Nursery Rhymes & Kids Songs By @kidscamp", "https://www.youtube.com/watch?v=Z_vNg1W0dR8", "LIVE"),
    ("Diana Roma and Oliver Built a Circle, Triangle, Square Secret Room", "https://www.youtube.com/watch?v=UaWtNhmaiDs", "4:49"),
    ("Diana Roma and Oliver Explore the Mysterious Secret Room", "https://www.youtube.com/watch?v=QjGhCL6zw9M", "10:01"),
    ("Diana and Roma open the Advent Calendar with a Christmas to-do list", "https://www.youtube.com/watch?v=lH-cGnv7qL4", "9:03"),
    ("🔴 LIVE: 24 Hours Of Bingo's Cutest Moments 🧡🥰 | Bingo - Official Channel", "https://www.youtube.com/watch?v=YyuS6fl7SAI", "LIVE"),
    ("Diana and Roma English Alphabet with Surprise Eggs | ABC", "https://www.youtube.com/watch?v=zlLnOV6OQN8", "7:30"),
    ("Roma and Diana learn the alphabet / ABC song", "https://www.youtube.com/watch?v=NvdUSZyCGRs", "13:26"),
    ("ABC Learn English Alphabet with Diana and Roma", "https://www.youtube.com/watch?v=abxA_XtnRSc", "8:53"),
    ("Gaby and Alex Learn Numbers Counting to 10", "https://www.youtube.com/watch?v=owZSF_7Trjo", "4:31"),
    ("Eli and parents are learning the English alphabet ABC. Useful video for children", "https://www.youtube.com/watch?v=rGtJDT2UnSQ", "6:13"),
    ("Alice learns the English alphabet - video for children", "https://www.youtube.com/watch?v=u6dvQBrka0M", "11:41"),
    ("Diana and Roma learn the alphabet with balloons", "https://www.youtube.com/watch?v=TpFOQDiGnPY", "9:15"),
    ("Nastya and Eva are learning the Summer Alphabet", "https://www.youtube.com/watch?v=d1F8B1R-9Zc", "8:35"),
    ("Katya and Dima ABC Challenge | English Alphabet with pools", "https://www.youtube.com/watch?v=ps8rixBCglw", "8:26"),
    ("Kids Learn English Alphabet | ABC", "https://www.youtube.com/watch?v=iVwn0VUsu3Y", "35:03"),
    ("Five Kids learn the Alphabet / ABC Vehicles", "https://www.youtube.com/watch?v=bFfj6bVROnc", "9:52"),
    ("Educational stories for kids from Vlad and Niki", "https://www.youtube.com/watch?v=_l928dd288Q", "11:34"),
    ("Gaby and Alex Learn the Alphabet | ABC Song", "https://www.youtube.com/watch?v=In9TDgHVvmE", "7:53"),
    ("Diana and Roma learn the alphabet and how to count", "https://www.youtube.com/watch?v=4XGLPTtn4xQ", "18:00"),
    ("Let's Learn Words Beginning with H to L | Yakka Dee!", "https://www.youtube.com/watch?v=YwlCJEUu_L8", "10:23"),
    ("Best of Series 1! | Learn to talk with Yakka Dee | BBC Kids", "https://www.youtube.com/watch?v=fKn7lsM5Fks", "39:06"),
    ("Can You Say Elf | Yakka Dee!", "https://www.youtube.com/watch?v=1eLJD4VvGTg", "1:51"),
    ("Can You Say Strawberry? 🍓 | Yakka Dee!", "https://www.youtube.com/watch?v=s2xFC53lwH0", "1:51"),
    ("Can You Say Alien | Yakka Dee!", "https://www.youtube.com/watch?v=K1e3yUrdlTk", "1:51"),
    ("Can You Say Bike? 🚲| Yakka Dee!", "https://www.youtube.com/watch?v=RELdBXLvaR8", "1:56"),
    ("Can You Say Dog? 🐶| Yakka Dee!", "https://www.youtube.com/watch?v=bSaC90HFmn4", "1:58"),
    ("Can you say Digger? 🧱 | Yakka Dee!", "https://www.youtube.com/watch?v=eSTHctmxTLk", "1:54"),
    ("Can you say Lizard? | Yakka Dee!", "https://www.youtube.com/watch?v=Ns9MRB8YcYU", "2:08"),
    ("Can you say Top?👚| Yakka Dee!", "https://www.youtube.com/watch?v=-W_vJkGh9SY", "1:55"),
    ("Can you say YoYo? 🙌 | Yakka Dee!", "https://www.youtube.com/watch?v=rraA5eUA0Z0", "1:56"),
    ("Can you say Milk?🍼 | Yakka Dee!", "https://www.youtube.com/watch?v=j4CJyornuKM", "1:53"),
    ("Can you say Shoes?🥾 | Yakka Dee!", "https://www.youtube.com/watch?v=JTCTOMkQxCY", "1:56"),
    ("Can you say Mango? 🥭 | Yakka Dee!", "https://www.youtube.com/watch?v=fatEjz_x0dc", "1:55"),
    ("Can You Say Bowl? 🥣 | Yakka Dee!", "https://www.youtube.com/watch?v=oB10YeBIx-s", "1:52"),
    ("Can You Say Kite? 🎏 | Yakka Dee!", "https://www.youtube.com/watch?v=1NM7uobvgg8", "1:51"),
    ("Can You Say Bath? 🛁| Yakka Dee!", "https://www.youtube.com/watch?v=RtAnhHh0FTU", "1:52"),
    ("Can You Say Book? 📚| Yakka Dee!", "https://www.youtube.com/watch?v=WFJsPrEqD_g", "1:56"),
    ("Can You Say Beans? 🍽| Yakka Dee!", "https://www.youtube.com/watch?v=H0tHDTLWIz0", "1:55"),
    ("Can You Say Peas? 💚| Yakka Dee!", "https://www.youtube.com/watch?v=RyNCz4zawyc", "1:56"),
    ("Can you say Bed? 🛌 💤 | Yakka Dee", "https://www.youtube.com/watch?v=uO0kiBfhrtE", "2:05"),
    ("Can You Say Worm? 🐛| Yakka Dee!", "https://www.youtube.com/watch?v=LkD0Bx88Bpg", "1:51"),
    ("Can You Say... Worm, Boat, House, Lion, Apple | Learn with Yakka Dee! | FULL EPISODES | BBC Kids", "https://www.youtube.com/watch?v=qYI_Y3JnwlA", "9:11"),
    ("Time to Travel ✈️ | Learn Words with Yakka Dee |BBC Kids", "https://www.youtube.com/watch?v=11Nn7xlJN_s", "5:00"),
    ("Can You Say... Banana, Dog, Book, Boots, Bike | Learn with Yakka Dee! | FULL EPISODES | BBC Kids", "https://www.youtube.com/watch?v=_WQttIwdetU", "9:11"),
    ("Can you say SPRING? | Flower, Tree + More! | Yakka Dee!", "https://www.youtube.com/watch?v=dsPTtHw1lS0", "3:02"),
    ("The Muffin Man | Kids Songs and Nursery Rhymes", "https://www.youtube.com/watch?v=ZbIDEJAiQb8", "2:30"),
    ("🔴LIVEㅣ@Bebefinn Best Play Stories and Songs for Kids", "https://www.youtube.com/watch?v=l8Vt4ctCriY", "LIVE"),
    ("🔴 Rhymington Square Livestream | Kids Songs | Rhymington Square", "https://www.youtube.com/watch?v=Ch0SAe5MYGI", "LIVE"),
    ("Peppa Pig NEW BABY EVIE Episodes LIVE 🍼 Cutest & Funniest Moments 🥹💛 Kids Cartoons", "https://www.youtube.com/watch?v=EKKxG5HNDyM", "LIVE"),
    ("📚 Kids Book Read Aloud: DAVID GETS IN TROUBLE by David Shannon", "https://www.youtube.com/watch?v=wYgORrdXnvQ", "4:00"),
    ("[Animated] My No No No Day by Rebecca Patterson | Read Aloud Books for Children!", "https://www.youtube.com/watch?v=x-Bpoj5fZr0", "3:30"),
    ("Vegetable Children's Song - Catch the Vegetables Song | healthy habits & eating | Hooray Kids Songs", "https://www.youtube.com/watch?v=vPM3ATjTzLw", "2:45"),
    ("🔴 Live | Bing: Full Episodes | Bing English", "https://www.youtube.com/watch?v=zg4uRvoOH_c", "LIVE"),
    ("🔴 LIVE: George Pig And Baby Evie Adventures 🍼 Peppa Pig & Evie Pig Full Episodes | Kids Cartoons", "https://www.youtube.com/watch?v=OVvvGMEMTPs", "LIVE"),
    ("Kids, let's learn common words with Pororo's fun Toy Dollhouse!", "https://www.youtube.com/watch?v=hGnMSib9Fuw", "6:13"),
    ("Do You Like Broccoli Ice Cream? | Nursery rhymes & kids song", "https://www.youtube.com/watch?v=fSUrBryhr2E", "2:12"),
    ("Do You Like Broccoli Ice Cream? | Funny Food Song and Nursery Rhymes for Kids", "https://www.youtube.com/watch?v=Pvf_0wcJx2c", "2:12"),
    ("Do You Like Chocolate Hot Dogs? - Yucky Food Combos for Kids", "https://www.youtube.com/watch?v=zZPURWlionU", "2:12"),
    ("Granny Pig's Chickens and Talent Day 🐷🐔 @PeppaPigOfficial", "https://www.youtube.com/watch?v=TKcHNEA9Hfk", "5:00"),
    ("The Colors Song ~ Learn the Colors / Colours ~ LEARN ENGLISH with Natural English ~ LEARN VOCABULARY", "https://www.youtube.com/watch?v=pUPM3DtK9so", "3:15"),
    ("Kids, let's Learn Common Words with Woodzeez Toy Dollhouse!", "https://www.youtube.com/watch?v=SrBnsSwTGjM", "6:13"),
    ("Learn How To Make A Doughnut With Elly and more Fun Learning Videos by KidsCamp", "https://www.youtube.com/watch?v=4y8UP-f8vms", "8:00"),
    ("Goldilocks And The Three Bears | A Super Simple Storybook", "https://www.youtube.com/watch?v=IxVT84N7Mbk", "5:30"),
    ("Kidscamp | Yes Yes Ice Cream Popsicles Fruits and Vegetables Learning Videos", "https://www.youtube.com/watch?v=REFebmS2yao", "8:00"),
    ("Fruits & Vegetables Song - Kids Songs with Dana", "https://www.youtube.com/watch?v=WB6B3OwlvFo", "2:30"),
    ("Ten in the Bed Songs for Kids | Sing Along & Baby Dance | Nursery Rhymes and Kids Songs", "https://www.youtube.com/watch?v=v9tV3z9rhEA", "LIVE"),
    ("🎉 Ready for Peppa's Christmas Party?", "https://www.youtube.com/watch?v=GJF_SrRxrwk", "7:30"),
    ("Peppa Pig Learns Ballet! 🩰 | Peppa Pig Full Episodes | 45 Mins | Little Learners", "https://www.youtube.com/watch?v=b1-fApbdW-Y", "45:00"),
    ("Let's Talk About Food! | Yakka Dee!", "https://www.youtube.com/watch?v=_TKqKL0WkWc", "12:00"),
    ("Phonics Song | Kidzstation", "https://www.youtube.com/watch?v=RkT626tlJSk", "2:22"),
    ("New Words for Toddlers | House and Home Sounds | Phonics with Dee | Yakka Dee!", "https://www.youtube.com/watch?v=ZKnf4HfGGZc", "3:30"),
    ("Phonics Song | kidzstation", "https://www.youtube.com/watch?v=n1eZsZzewS8", "2:22"),
    ("Peppa Pig Jumps to the Sky | Family Kids Cartoon", "https://www.youtube.com/watch?v=K6SxdYVqZxk", "15:00"),
    ("🌞 Peppa Pig & George's BIG Family Adventures🐷 | Full Episodes | Holiday & Travel Days Out", "https://www.youtube.com/watch?v=TWuoB-F-Jqc", "45:00"),
    ("Peppa Pig Travels to the Space | Peppa Pig Official | Family Kids Cartoon", "https://www.youtube.com/watch?v=PNQL3kP-1kk", "12:00"),
    ("#5 Apples and Bananas 🍎🍌 | Silly Vowel Song for Kids | ESL Sing Along", "https://www.youtube.com/watch?v=v3eLVloe-BE", "3:00"),
    ("There's A Monster In My Tummy #2 | Fun Food Song for Kids! | Rhymington Square", "https://www.youtube.com/watch?v=qqblIOqoVJE", "2:30"),
    ("BABY Peppa's First GIANT Ice Cream! 🍦Summer Adventure | Tales Full Episodes | Kids Cartoon | 20 Mins", "https://www.youtube.com/watch?v=St9v6jj6xwA", "20:00"),
    ("🔴 LIVE! Peppa Pig's Learning Adventures! 🍦 Peppa's Playgroup: Little Learners 🐷 Kids Cartoons", "https://www.youtube.com/watch?v=oPLkBki9NJA", "LIVE"),
    ("The Alphabet Rhyme | Fun ABCs Practice Song! | Rhymington Square", "https://www.youtube.com/watch?v=9yagv3HYg24", "2:30"),
    ("Let's Blow A Bubble | Bubbles Song for Kids | Rhymington Square", "https://www.youtube.com/watch?v=1Xpfyifb5lI", "2:30"),
    ("Fruit Finger Family Song & more Fun Fruit & Vegetable Songs | Lah-Lah Kids Music & Nursery Rhymes", "https://www.youtube.com/watch?v=lKoswBc2CjQ", "3:30"),
    ("🔴 LIVE Christmas with Ben and Holly's Adventures! 🎄 Ben and Holly's Little Kingdom Christmas Special", "https://www.youtube.com/watch?v=zM4_gEbmilA", "LIVE"),
    ("🔴 LIVE Peppa Pig And Friends 🌟 24 HOUR Livestream", "https://www.youtube.com/watch?v=-dDscDrnS2I", "LIVE"),
    ("I Like To Ride My Bicycle | Imagination Time With Caitie | Work Together Activity for Kids", "https://www.youtube.com/watch?v=VUt83oNO1-g", "4:00"),
    ("Where Is The Cat? 🐱 | Peekaboo! | Practice Prepositions! | Super Simple Songs", "https://www.youtube.com/watch?v=pZ7H3XuEFkQ", "3:00"),
    ("Noodle & Pals ABCs | Alphabet for Kids | Super Simple Storybook", "https://www.youtube.com/watch?v=Ptu2eMCP-8A", "3:00"),
    ("How Many Fingers? | Kids Nursery Rhymes | Rhymington Square", "https://www.youtube.com/watch?v=up7SZzzGHHg", "2:30"),
    ("🔴 Carl's Car Wash Episode Livestream | Cartoons For Kids | Super Simple Songs", "https://www.youtube.com/watch?v=4Iu6yyju2ZI", "LIVE"),
    ("Goldilocks and the Three Bears – 🐻 Read aloud of the classic kids tale with music in full screen HD", "https://www.youtube.com/watch?v=GnbO6h_yQkg", "10:00"),
    ("Let's Learn About Animals! 🦆 | Yakka Dee!", "https://www.youtube.com/watch?v=EfCiv6SnkNo", "12:00"),
    ("Can You Say... Bed, Car, Beans, Mouse, Ball | Learn with Yakka Dee! | FULL EPISODES | Yakka Dee!", "https://www.youtube.com/watch?v=FXDDmdevF3w", "9:11"),
    ("Join Cody & Friends LIVE! 🔴 CoComelon Nursery Rhymes & Kids Songs", "https://www.youtube.com/watch?v=aHsjHWr8aAw", "LIVE"),
    ("Goldilocks and the Three Bears | Fairy Tales and Bedtime Stories for Kids in English | Storytime", "https://www.youtube.com/watch?v=VjIE-Sl-qKY", "8:00"),
    ("Goldilocks and the Three Bears Song ♫ Fairy Tales ♫ Story Time for Kids by The Learning Station", "https://www.youtube.com/watch?v=PGI-4MrC_b8", "3:30"),
    ("Alphabet Activity Puzzles | Learn ABC for Toddlers | Preschool Video for Kids", "https://www.youtube.com/watch?v=ezkB7dDTS20", "5:00"),
    ("🔴 LIVE! George Pig's MOST Iconic Moments 🦖💙 Peppa Pig FULL EPISODES | Kids Cartoons (With Captions)", "https://www.youtube.com/watch?v=GVMAPWwMg1M", "LIVE"),
    ("Peekaboo, Where Are You? | A Super Simple Storybook", "https://www.youtube.com/watch?v=k2Bl-YnZXNE", "3:00"),
    ("ABCs! 🐘 Animals from A to Zooli | Bubble Guppies", "https://www.youtube.com/watch?v=7G8LMWkyDjY", "2:00"),
    ("First day of kindergarten!! 🐯🍎 *WITH VOICE* II Toca boca Roleplay", "https://www.youtube.com/watch?v=IVglTQpWSm0", "10:00"),
    ("The sleepover! *GONE WRONG* (WITH VOICE) II Toca boca roleplay", "https://www.youtube.com/watch?v=ddM_L1bJRKo", "8:00"),
    ("Single mom with twins aesthetic night routine ~ *WITH VOICE* Toca boca roleplay", "https://www.youtube.com/watch?v=-tqeKEnKUOU", "8:00"),
    ("First day of school! 🏫 *GONE WRONG* (WITH VOICE) || Toca Boca Roleplay", "https://www.youtube.com/watch?v=yz5tkGDJJVc", "10:00"),
    (".ೃ࿔ My afternoon routine at home🧺🧴| self care, cooking & home reset 🌸🤍✨ #avatarworld #pazu", "https://www.youtube.com/watch?v=MSEZEem7E6s", "8:00"),
    ("Peppa Pig What Music are you into, Peppa? Effects | Sponsored By Preview 2 Effects", "https://www.youtube.com/watch?v=sL3gfmFhygs", "2:00"),
    ("Peppa, Don't Splash Us ! Effects Remix Sponsored By Preview 2 Effects Compilation", "https://www.youtube.com/watch?v=5QnnHJm_scg", "2:00"),
    ("Peppa Pig In Avatar World 🐷 Soft Play 🎈 | Full Episodes", "https://www.youtube.com/watch?v=dfawHlrAJLg", "20:00"),
    ("🔴 LIVE 24/7: Peppa Pig NEW Tales 2026 🐽 Best Pig Adventures | Cartoons for Kids", "https://www.youtube.com/watch?v=Av7kJ4_U1E8", "LIVE"),
    ("🔴 LIVE! Lollipop Emotions & Colors + More 😁 Little Angel Kids Cartoons & Nursery Rhymes", "https://www.youtube.com/watch?v=z4rRflk0CfY", "LIVE"),
    ("🔴 CoComelon LIVE DJ Dance Party! 🎧 Wheels On The Bus, Baby Shark + More Kids Songs", "https://www.youtube.com/watch?v=ZrHunTTDtiQ", "LIVE"),
    ("Peppa Pig Visits The Toy Factory 🐷 🧸 Adventures With Peppa Pig |", "https://www.youtube.com/watch?v=4T-WSyd90JM", "8:00"),
    ("Peppa Pig Boo Boo Song | Sports Safety Song | Peppa Pig Nursery Rhymes & Kids Songs", "https://www.youtube.com/watch?v=6mymzS9OF1Q", "2:30"),
    ("Wheels on the Bus | Popular Nursery Rhyme for Children - LIVE", "https://www.youtube.com/watch?v=zJbB82zFFYI", "LIVE"),
    ("🔴 CoComelon LIVE! 🎶 Baby Songs, Wheels On The Bus & More for Kids! – Non-Stop Kids Songs!", "https://www.youtube.com/watch?v=HV6-t0DWKTE", "LIVE"),
    ("🔴LIVE: Bedtime Stories | Sleepy words for toddlers and babies | Yakka Dee!", "https://www.youtube.com/watch?v=V76iKZpX3Ew", "LIVE"),
    ("🔴 GABBY'S DOLLHOUSE 24/7 TOY MARATHON! | Crafts, Games, Songs and Learning Adventures for Kids", "https://www.youtube.com/watch?v=ZY10imwf_s4", "LIVE"),
    ("🔴 LIVE: Adventures With George & Peppa Pig 🦖 🐷 60 Minutes of Fun Adventures | George Pig", "https://www.youtube.com/watch?v=r44m1daxn9I", "LIVE"),
    ("DYNAMITE - Official Peppa Pig Cover (Lyric Video)", "https://www.youtube.com/watch?v=b-oUd5MWTts", "3:30"),
    ("ROAR - Official Peppa Pig Cover (Lyric Video)", "https://www.youtube.com/watch?v=car1jghyeT8", "3:30"),
    ("Diamonds (Peppa's version) - Official Peppa Pig Cover (Lyric Video)", "https://www.youtube.com/watch?v=hKDS-9npCOc", "3:30"),
    ("Stronger - Official Peppa Pig Cover (Lyric Video)", "https://www.youtube.com/watch?v=TglP5RYnQVc", "3:30"),
    ("ROAR - Official Peppa Pig Cover (Lyric Video)", "https://www.youtube.com/watch?v=1xwlVHnyq2U", "3:30"),
    ("Old MacDonald, Twinkle Twinkle | Peppa Pig Songs | Baby Songs | Nursery Rhymes", "https://www.youtube.com/watch?v=5pN7sxVd_kk", "4:00"),
    ("🟢 LIVE | 'Tis the Season to Love, Sing, & Give Thanks in Daniel Tiger's Neighborhood! ❄️ | PBS KIDS", "https://www.youtube.com/watch?v=7z8ptDYNPU4", "LIVE"),
    ("Peppa Pig Songs 🌟 Busy Miss Rabbit 🎵 Peppa Pig My First Album 14# | Kids Songs | Baby Songs", "https://www.youtube.com/watch?v=w_uT3GW1ycE", "3:00"),
    ("Let's Play With Elly Make Up Face 💄 Princess Look | Episode 6 | Fun Learning video By Kidscamp", "https://www.youtube.com/watch?v=PaSZoAdT5BA", "7:00"),
    ("Color Balls Dancing Machine Song for Children and Toddlers by KidsCamp", "https://www.youtube.com/watch?v=rCPQyRjdqW0", "5:00"),
    ("Learn Colors With Dancing Fruits On Pop It | Finger Family + Best Learning Videos for Toddlers", "https://www.youtube.com/watch?v=G97kcWxPxQA", "5:00"),
    ("Surprise Eggs Dancing Balls | Finger Family + Best Learning Videos for Toddlers by @kidscamp", "https://www.youtube.com/watch?v=m--ShQgqBgE", "5:00"),
    ("Peppa Pig World Gameplay 🐷🌈 | Fun Adventures for Kids!", "https://www.youtube.com/watch?v=e7ZrCKBZydk", "15:00"),
    ("Peppa's SINGING Competition 🎤🎶 Pig Full Episodes | 4 Hours of Kids Cartoons", "https://www.youtube.com/watch?v=auJq_HhX21w", "4:00:00"),
    ("Peppa Pig Goes Shopping 🐷 Peppa Pig Shopping Gameplay", "https://www.youtube.com/watch?v=zrrvo9NkS1I", "12:00"),
    ("Peppa Pigs EP1", "https://www.youtube.com/watch?v=R23hq49FE74", "5:00"),
    ("🔴 NEWEST Peppa Pig Episodes 2026 ✨ SEASON 10 Holiday Adventures ☀️ Kids Movie 🔴", "https://www.youtube.com/watch?v=T-C1dXWXesQ", "LIVE"),
    ("Yummy Fruits & Vegetables | La La Learn Kids Songs | D Billions Parody #dbillions", "https://www.youtube.com/watch?v=9FRL6VH2EX4", "2:30"),
    ("Yummy Fruits & Vegetables | Kids Songs With Tiki", "https://www.youtube.com/watch?v=AxfvQkXdPIA", "2:30"),
    ("Yummy Fruits & Vegetables | Nursery Rhymes and Kids Songs", "https://www.youtube.com/watch?v=J4FjPb3oJn4", "2:30"),
    ("Yummy Fruits & Vegetables", "https://www.youtube.com/watch?v=ByEJWE7Y6rk", "2:30"),
    ("Goldilocks and the Three Bears by Oxbridge Baby", "https://www.youtube.com/watch?v=0oUP2PFeOi8", "8:00"),
    ("ABC with Rachel and Travis | Travis in WONDERLAND", "https://www.youtube.com/watch?v=HOwkwIACclc", "5:00"),
    ("Princesa de Hielo vs Princesa de Fuego — ¿Quién Ganará?", "https://www.youtube.com/watch?v=vouxkVCwbcA", "8:00"),
    ("Fun Indoor Playground for Family and Kids at Leo's Lekland", "https://www.youtube.com/watch?v=1IHWkpZAYy8", "10:00"),
    ("Transport Noises with Dee! | Yakka Dee!", "https://www.youtube.com/watch?v=ylQEE2bdusQ", "5:00"),
    ("🔴 NEWEST Peppa Pig Episodes 2026 ✨ SEASON 10 Holiday Adventures ☀️ Kids Movie 🔴", "https://www.youtube.com/watch?v=suBf_zv7Ya0", "LIVE"),
    ("🔴 BEST of George 2026 LIVE! 🦖 Peppa Pig Mini Movie 🍿 Kids Cartoons 🔴", "https://www.youtube.com/watch?v=BCcwDizkSn8", "LIVE"),
    ("🎶 Like What You Like 🚌✨ + More Nursery Rhymes for Kids | Family Songs | Peppa Pig Songs Official", "https://www.youtube.com/watch?v=11LyA1argIE", "5:00"),
    ("Peppa Cinema: The Album - Let's Dress Up (Official Music Video)", "https://www.youtube.com/watch?v=enhf0bY5WTQ", "3:30"),
    ("Peppa Pig Tales Vol 1 👗 Let's Play Dress Up! 🐷 NEW! ✨ Peppa Pig Songs 💞 Kids Songs & Nursery Rhymes", "https://www.youtube.com/watch?v=5Uzre7oUObw", "5:00"),
    ("Peppa Pig Boo Boo Song | Sports Safety Song | Peppa Pig Nursery Rhymes & Kids Songs", "https://www.youtube.com/watch?v=VZMvWQvPRkY", "2:30"),
    ("Peppa's Camper Van Holiday! 🐷🚚 Peppa Pig Full Episodes | Peppa Official Family Kids Cartoon", "https://www.youtube.com/watch?v=1-t_PSFyzXs", "25:00"),
    ("Phonics Song 2 | ABC Alphabet Phonics Nursery Rhyme For Kids", "https://www.youtube.com/watch?v=V68dHbdelcM", "3:00"),
    ("Phonics Song | kidzstation", "https://www.youtube.com/watch?v=aKNVbqzmHoc", "2:22"),
    ("Phonics Song | kidzstation", "https://www.youtube.com/watch?v=YQY0TigY9Ac", "2:22"),
    ("🦖 Peppa Pig Makes a Pottery Tea Set", "https://www.youtube.com/watch?v=VAMd2b9nFhs", "5:00"),
    ("Ants Song - Funny kids song - Family song | Hooray Kids Songs & Nursery Rhymes", "https://www.youtube.com/watch?v=nwqsG9qrE68", "2:30"),
    ("Children's song Have a Haircut - Children at the Hairdresser | Hooray Kids Songs & Nursery Rhymes", "https://www.youtube.com/watch?v=zvL9Ei6NM00", "2:30"),
    ("♪♪ Children's Song Family - Gagaga Gugugu - Baby Song | Hooray Kids Songs & Nursery Rhymes", "https://www.youtube.com/watch?v=TzPJT5t2rTs", "2:30"),
    ("Get well soon children's song | Soon you will be fit again - Hooray kids songs & nursery rhymes", "https://www.youtube.com/watch?v=7GtxhRH4FEo", "2:30"),
    ("Toca life vacation | The airport #1", "https://www.youtube.com/watch?v=QRnC0uW3wz4", "8:00"),
    ("Toca life hospital | Eating for 2?!? S1 #1", "https://www.youtube.com/watch?v=tlHoDcwPuxs", "4:29"),
    ("Bigger car 🍼🚗 | Peppa Pig | ABC Kids", "https://www.youtube.com/watch?v=7Opxn2hKI1A", "3:00"),
    ("Peppa Pig Learns and Plays with Muddy Puddles", "https://www.youtube.com/watch?v=3TYZKcovlPU", "10:00"),
    ("Peppa Pig | Superhero Party | Peppa Pig Official | Family Kids Cartoon", "https://www.youtube.com/watch?v=OW1iVWPXs2c", "5:00"),
    ("Do You Like Spaghetti Yogurt Song?", "https://www.youtube.com/watch?v=17lyBa9QPi4", "2:12"),
    ("Do you like spinach cake? | Food Song for Kids! | Preschool Song For Circle Time", "https://www.youtube.com/watch?v=hhWBwW0xups", "2:12"),
    ("Do You Like Fish in the Milk?", "https://www.youtube.com/watch?v=9Jp9d7cTjQU", "2:12"),
    ("Do you like broccoli + More Kids Songs And Nursery Rhymes", "https://www.youtube.com/watch?v=TYuFTH1pd4Q", "5:00"),
    ("Do you like broccoli and more Kids Songs | Maya Mary Mia", "https://www.youtube.com/watch?v=PvAalmN0MQU", "3:00"),
    ("Fruits And Vegetables Song - Yummy! | Children Songs by Sunny Kids Songs", "https://www.youtube.com/watch?v=xGH2xdBSyS8", "2:30"),
]

# ─── BUILD VIDEOS LIST ──────────────────────────────────────────────────
ts = "2026-03-10T20:00:00-05:00"  # Today at 8 PM ET
videos = []
for title, url, dur_str in SCRAPED:
    channel = infer_channel(title, url)
    dur_min = parse_duration_to_minutes(dur_str)
    videos.append({
        "title": title,
        "channel": channel,
        "url": url,
        "timestamp": ts,
        "duration": dur_str,
        "duration_minutes": round(dur_min, 2),
        "is_live": dur_str == "LIVE"
    })

# ─── COMPUTE STATS ──────────────────────────────────────────────────────
total_watch_minutes = sum(v["duration_minutes"] for v in videos)
channel_counts = Counter(v["channel"] for v in videos)
top_channels = [{"channel": c, "count": n} for c, n in channel_counts.most_common(15)]

# Category inference
def infer_category(title: str, channel: str) -> str:
    t = title.lower()
    c = channel.lower()
    if "yakka dee" in c or "yakka dee" in t:
        return "Speech & Language Learning"
    if "pbs kids" in c or "daniel tiger" in t or "work it out wombats" in t:
        return "Educational / PBS"
    if "peppa pig" in t or "george pig" in t:
        return "Peppa Pig"
    if "alphabet" in t or "abc" in t or "phonics" in t:
        return "Alphabet & Phonics"
    if "fruits" in t or "vegetables" in t or "food" in t or "broccoli" in t:
        return "Food & Nutrition Songs"
    if "diana" in t or "roma" in t:
        return "Diana & Roma / Kids Vlog"
    if "toca" in t or "avatar world" in t or "pazu" in t:
        return "Toca Boca / Gaming"
    if "nursery rhymes" in t or "kids songs" in t or "baby songs" in t:
        return "Nursery Rhymes"
    if "read aloud" in t or "storybook" in t or "storytime" in t or "goldilocks" in t:
        return "Books & Storytime"
    if "colors" in t or "shapes" in t or "numbers" in t or "counting" in t:
        return "Colors, Shapes & Numbers"
    if "cocomelon" in t:
        return "CoComelon"
    if "bing" in t:
        return "Bing"
    if "live" in t:
        return "Live Streams"
    return "Other Kids Content"

cat_counts = Counter(infer_category(v["title"], v["channel"]) for v in videos)
top_categories = [{"category": c, "count": n} for c, n in cat_counts.most_common(10)]

# Hourly distribution (all labeled as evening since it's one session)
hourly = {str(h): 0 for h in range(24)}
hourly["19"] = len(videos) // 2
hourly["20"] = len(videos) - len(videos) // 2

daily = {"Mon": 0, "Tue": len(videos), "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}

# ─── WRITE JSON ────────────────────────────────────────────────────────
data = {
    "generated": "2026-03-10T20:00:00-05:00",
    "account": "jigar.us.af@gmail.com",
    "period_days": 7,
    "note": "Daily update",
    "total_videos": len(videos),
    "total_watch_minutes": round(total_watch_minutes, 1),
    "videos": videos,
    "top_channels": top_channels,
    "top_categories": top_categories,
    "hourly_counts": hourly,
    "daily_counts": daily
}

out_path = Path(__file__).parent.parent / "data" / "history.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Wrote {len(videos)} videos to {out_path}")
print(f"   Total watch time: {round(total_watch_minutes/60, 1)}h")
print(f"   Top channels: {[c['channel'] for c in top_channels[:5]]}")
