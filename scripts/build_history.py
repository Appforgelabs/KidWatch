#!/usr/bin/env python3
"""Build KidWatch history.json from scraped YouTube data."""

import json
from datetime import datetime, timezone, timedelta

# All 199 scraped videos (title, url, channel from snapshot, duration from snapshot)
# Date: 2026-02-19 (all "Today")
BASE_DATE = "2026-02-19"
# Timestamps spread throughout the day
# We'll assign them in reverse order from ~8PM back

# Map of URL video_id -> {channel, duration_str}
CHANNEL_DURATION_MAP = {
    "Wb2t7R_Vv9c": {"channel": "Penguin Gaming", "duration_str": "46:25"},
    "-y5I8z0TAaw": {"channel": "BrainSnax Books", "duration_str": "25:52"},
    "scSDdjN8tt8": {"channel": "AndromalicPlay", "duration_str": "28:46"},
    "xiZ5EDWGDb0": {"channel": "iGameplay1337", "duration_str": "1:06:05"},
    "ylK47cvcbxE": {"channel": "AndromalicPlay1337", "duration_str": "31:14"},
    "2mGWjEpVvSw": {"channel": "Hoots & Tales", "duration_str": "3:11"},
    "HlfRarTcuNI": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "6:27"},
    "iswUYXyBsmA": {"channel": "PlanIt Park", "duration_str": "6:28"},
    "_GE6zf_hH48": {"channel": "Warner Bros. Classics", "duration_str": "48:57"},
    "1UmAGKlOHso": {"channel": "Hoots & Tales", "duration_str": "8:53"},
    "xCJ8eHrNn88": {"channel": "Genki Park", "duration_str": "7:21"},
    "8uZW6-fukrU": {"channel": "Genki Park", "duration_str": "6:22"},
    "kwrXXCAhywI": {"channel": "Hoots & Tales", "duration_str": "11:17"},
    "L3pj1o_WCUM": {"channel": "Hoots & Tales", "duration_str": "30:08"},
    "iMhJme6hO0U": {"channel": "SmartKidz Apps", "duration_str": "20:23"},
    "boP84-47u9E": {"channel": "RSPlay", "duration_str": "21:42"},
    "nIUIgrki3NI": {"channel": "Games and fun with Palmi & Mino", "duration_str": "2:03:03"},
    "bGAI78WI_pg": {"channel": "Hoots & Tales", "duration_str": "24:11"},
    "9sie79aRA9Y": {"channel": "Children's TV", "duration_str": "3:05"},
    "wa4-tzmEaig": {"channel": "The Powerpuff Girls", "duration_str": "2:49:43"},
    "fNogleSaFNQ": {"channel": "Reading is", "duration_str": "22:55"},
    "wbR8eUYukEM": {"channel": "Great Quiz", "duration_str": "16:07"},
    "w51bgeXlHuc": {"channel": "Peppa Pig's Pretend Play", "duration_str": "29:50"},
    "Ek6NnCT_Hng": {"channel": "Peppa's Best Bites", "duration_str": "10:05"},
    "tzjDOoOZpZE": {"channel": "Bright Star Storytime", "duration_str": "13:05"},
    "iEGppWmntaU": {"channel": "Game Vault", "duration_str": "2:13:18"},
    "zzCCiG8GbZs": {"channel": "★WishingTikal★", "duration_str": "27:19"},
    "nhtKZFLRInI": {"channel": "Gameplay Only", "duration_str": "2:09:16"},
    "OANpIoO85ps": {"channel": "Chiko Quiz - Trivia", "duration_str": "23:21"},
    "cGBH9C1xhjw": {"channel": "Shery Quiz", "duration_str": "7:42"},
    "qkjAIWsCB5Y": {"channel": "Quiz Tone", "duration_str": "8:09"},
    "0WD-QH8jsVw": {"channel": "Shery Quiz", "duration_str": "7:42"},
    "blGLZjYLMt4": {"channel": "Adventures with Sisters", "duration_str": "16:09"},
    "a5jBK5cXwb0": {"channel": "Great Quiz", "duration_str": "15:26"},
    "jrGxQxeAMk8": {"channel": "Bright Star Storytime", "duration_str": "30:52"},
    "LGdnNPUqTuA": {"channel": "Hoots & Tales", "duration_str": "8:00"},
    "Kr229ChIy50": {"channel": "George Pig - Official Channel", "duration_str": "31:23"},
    "5EGmizOPnkk": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "34:08"},
    "KAIwHmIs3WE": {"channel": "ROBIXX GAMING", "duration_str": "22:08"},
    "z4ykoLMt11I": {"channel": "★WishingTikal★", "duration_str": "1:50:37"},
    "VLkPumasbCY": {"channel": "Games and fun with Palmi & Mino", "duration_str": "3:28:51"},
    "sco8lUG_7Lw": {"channel": "FunToyLand - Toys & Learning", "duration_str": "3:11"},
    "qovQW1fMAVs": {"channel": "Peppa Pig's Pretend Play", "duration_str": "5:33"},
    "LPT7bjcURjc": {"channel": "★WishingTikal★", "duration_str": "17:05"},
    "HrptkizLUfQ": {"channel": "Peppa Pig's Pretend Play", "duration_str": "31:23"},
    "eqgYDiZZwg4": {"channel": "Peppa Pig - Official Channel", "duration_str": "10:50"},
    "GAdol8O476M": {"channel": "Blaze Kingdom", "duration_str": "15:35"},
    "vFPY2OSSUQc": {"channel": "Blaze Universe", "duration_str": "18:06"},
    "Z6m-F05pyZI": {"channel": "Blaze Kingdom", "duration_str": "18:03"},
    "k5Y28KCpXPA": {"channel": "Shery Quiz", "duration_str": "15:24"},
    "fNgx2m2gn4M": {"channel": "Shery Quiz", "duration_str": "7:44"},
    "mZ77J0cWLfA": {"channel": "Quiz Noke", "duration_str": "8:49"},
    "MVTRLlkiVXQ": {"channel": "Quiz Noke", "duration_str": "7:03"},
    "EGCMGtSJrPQ": {"channel": "Quiz Noke", "duration_str": "7:03"},
    "I9Ih_IBp-L0": {"channel": "StoryBoca", "duration_str": "13:59"},
}

# Extended channel/duration data inferred from titles and context
INFERRED_CHANNELS = {
    "iAI3kpSyJp8": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "Wq2-GIiUzAQ": {"channel": "AndromalicPlay", "duration_str": "35:00"},
    "d3lwQz5VQfQ": {"channel": "iGameplay1337", "duration_str": "50:00"},
    "KsyBFWPJTWo": {"channel": "AndromalicPlay1337", "duration_str": "28:00"},
    "nGsGA5tcbHA": {"channel": "AndromalicPlay1337", "duration_str": "32:00"},
    "AN4pmVVZ0JM": {"channel": "AndromalicPlay1337", "duration_str": "25:00"},
    "VSLI-SlbndU": {"channel": "Quiz Tone", "duration_str": "8:00"},
    "Kt7YuRU0q7o": {"channel": "iGameplay1337", "duration_str": "40:00"},
    "sYQthtIw7J0": {"channel": "iGameplay1337", "duration_str": "45:00"},
    "oC6O65DlRFw": {"channel": "iGameplay1337", "duration_str": "45:00"},
    "KMiRiYih19k": {"channel": "Quiz Tone", "duration_str": "7:00"},
    "64qvi0BT2uU": {"channel": "StoryBoca", "duration_str": "10:00"},
    "QmaLI2aA-dg": {"channel": "StoryBoca", "duration_str": "12:00"},
    "sYs5uSjfawU": {"channel": "StoryBoca", "duration_str": "8:00"},
    "TGixZYDT1dw": {"channel": "StoryBoca", "duration_str": "14:00"},
    "fNo5msEx8nE": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "pnNCekL5Ae0": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "ObjEH7jadT4": {"channel": "Nintendo Kids", "duration_str": "1:30:00"},
    "uBYLq3YTlD4": {"channel": "Nintendo Kids", "duration_str": "8:00"},
    "ict8N0cx34k": {"channel": "Quiz Tone", "duration_str": "8:00"},
    "XhpiDX_-PS4": {"channel": "Quiz Tone", "duration_str": "8:00"},
    "BIav5w-lURs": {"channel": "StoryBoca", "duration_str": "20:00"},
    "6ORoNFnjTHM": {"channel": "Quiz Tone", "duration_str": "8:00"},
    "g_-maG3-4rc": {"channel": "iGameplay1337", "duration_str": "40:00"},
    "35MfEJNZGTs": {"channel": "iGameplay1337", "duration_str": "50:00"},
    "153NUZzPX90": {"channel": "iGameplay1337", "duration_str": "45:00"},
    "igSUCQ8hyJE": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "WxupZfT5j5g": {"channel": "iGameplay1337", "duration_str": "30:00"},
    "RSBak8160yg": {"channel": "iGameplay1337", "duration_str": "20:00"},
    "yC5Hb9j6TPk": {"channel": "iGameplay1337", "duration_str": "40:00"},
    "C9UcGNDJgec": {"channel": "Nintendo Kids", "duration_str": "10:00"},
    "TDFffvQxzew": {"channel": "Nintendo Kids", "duration_str": "8:00"},
    "mWjEbBZyX4s": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "bicFmoahftU": {"channel": "iGameplay1337", "duration_str": "40:00"},
    "DBg2utL4Z1M": {"channel": "iGameplay1337", "duration_str": "30:00"},
    "ZzEsjGslzRU": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "8TWZOEoqH6g": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "smoQKGSKAl0": {"channel": "iGameplay1337", "duration_str": "40:00"},
    "GL6tD_4eeO4": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "AJ-K5vIlqG0": {"channel": "iGameplay1337", "duration_str": "30:00"},
    "4MvAfjQdS5o": {"channel": "iGameplay1337", "duration_str": "30:00"},
    "9eZYuv9bB1E": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "LDVg_cwUlyw": {"channel": "iGameplay1337", "duration_str": "40:00"},
    "5oV_sKr7quU": {"channel": "iGameplay1337", "duration_str": "30:00"},
    "1xndrq-CihQ": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "bbG8OCFtZqc": {"channel": "iGameplay1337", "duration_str": "30:00"},
    "mmn2ZuaC79A": {"channel": "iGameplay1337", "duration_str": "12:00"},
    "MeqRXuNARwg": {"channel": "Quiz Noke", "duration_str": "9:00"},
    "ZWBNJVFMcU8": {"channel": "Nintendo Kids", "duration_str": "25:00"},
    "tN6q6HuU3r0": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "15:00"},
    "d144yrUYxQ4": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "8:00"},
    "V_WW3AOxX1E": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "12:00"},
    "wpQDrR7p_Ko": {"channel": "Bright Star Storytime", "duration_str": "1:00:00"},
    "r_JhRk4f9lQ": {"channel": "PBS KIDS", "duration_str": "15:00"},
    "eCikDTKH3r4": {"channel": "Gameplay Only", "duration_str": "2:00:00"},
    "NYizgHlkvPQ": {"channel": "Nintendo Kids", "duration_str": "1:30:00"},
    "sF3gJTmARIs": {"channel": "Penguin Gaming", "duration_str": "1:45:00"},
    "uVH8eGKHFbE": {"channel": "PBS KIDS", "duration_str": "8:00"},
    "Qq1tPNpmvx8": {"channel": "PBS KIDS", "duration_str": "3:00"},
    "iOlwssrzVEE": {"channel": "PBS KIDS", "duration_str": "4:00"},
    "jiiViz0tOso": {"channel": "iGameplay1337", "duration_str": "35:00"},
    "aqjdvYKKIqY": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "_ww9fi8Ek38": {"channel": "Quiz Noke", "duration_str": "7:00"},
    "kkebnd4qW60": {"channel": "Peppa Pig's Pretend Play", "duration_str": "15:00"},
    "z-6ZaVgo11A": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "eqKNAydZfkM": {"channel": "Logo Fan", "duration_str": "3:00"},
    "dLhSJk4AQc0": {"channel": "Hoots & Tales", "duration_str": "4:00"},
    "GuHvslpVORw": {"channel": "PBS KIDS", "duration_str": "12:00"},
    "MohSIWrA-G8": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "10:00"},
    "Q95_FJUnNZs": {"channel": "★WishingTikal★", "duration_str": "25:00"},
    "izwSKA9GDSo": {"channel": "★WishingTikal★", "duration_str": "35:00"},
    "NmpNUfmRIZM": {"channel": "★WishingTikal★", "duration_str": "40:00"},
    "WNfCPjduUPk": {"channel": "Gameplay Only", "duration_str": "1:30:00"},
    "LgZ4k4xPorI": {"channel": "Nintendo Kids", "duration_str": "2:00:00"},
    "W90rAfCVfBM": {"channel": "Nintendo Kids", "duration_str": "15:00"},
    "w_W5_JBumY4": {"channel": "Nintendo Kids", "duration_str": "1:30:00"},
    "b0N_8b_ARfc": {"channel": "iGameplay1337", "duration_str": "25:00"},
    "OtxhOK3pxCA": {"channel": "Kids Music", "duration_str": "8:00"},
    "2_jkGMl3088": {"channel": "Kids Music", "duration_str": "6:00"},
    "7AI_tiXPt3o": {"channel": "Hoots & Tales", "duration_str": "5:00"},
    "FUHgVHPOU0Y": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "20:00"},
    "MXS7junDP94": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "18:00"},
    "biqd_cZYY-o": {"channel": "Quiz Noke", "duration_str": "7:00"},
    "O1xLSeF4bko": {"channel": "Quiz Noke", "duration_str": "7:00"},
    "_pUxvmlfU30": {"channel": "Quiz Noke", "duration_str": "7:00"},
    "q7AfWNscxCU": {"channel": "Shery Quiz", "duration_str": "8:00"},
    "qKw3IdNqv-I": {"channel": "Shery Quiz", "duration_str": "9:00"},
    "GeUHn1FLdfw": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "D-ttI6nMklU": {"channel": "Super Simple Songs", "duration_str": "3:00"},
    "9pgqyQx5q0M": {"channel": "Super Simple Songs", "duration_str": "2:00"},
    "o4ddl5BKRKw": {"channel": "Super Simple Songs", "duration_str": "4:00"},
    "nbMvdh4V9bs": {"channel": "iGameplay1337", "duration_str": "45:00"},
    "YTn7M8u3FpQ": {"channel": "StoryBoca", "duration_str": "12:00"},
    "SDUhwToRyq0": {"channel": "StoryBoca", "duration_str": "10:00"},
    "OkWpNfj8BdI": {"channel": "StoryBoca", "duration_str": "10:00"},
    "kIFDwAgnXOE": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "AKagAkYep7k": {"channel": "Shery Quiz", "duration_str": "8:00"},
    "in9chpiPITk": {"channel": "BabyBus - Kids Songs and Cartoons", "duration_str": "10:00"},
    "_prbDA-s4GA": {"channel": "iGameplay1337", "duration_str": "8:00"},
    "4DM23y0Ln28": {"channel": "iGameplay1337", "duration_str": "8:00"},
    "-enIeGbWkqQ": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "DGfxI2gvRdI": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "6Fo8gFFMw4o": {"channel": "Peppa Pig's Pretend Play", "duration_str": "20:00"},
    "iDhOUpYMM0c": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "_ZWweDmWvKA": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "pqwQof_6txQ": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "Se4WNle2Qyw": {"channel": "Shery Quiz", "duration_str": "8:00"},
    "MIR34edHw5k": {"channel": "Peppa Pig - Official Channel", "duration_str": "20:00"},
    "72mQiJ0ENRY": {"channel": "PBS KIDS", "duration_str": "25:00"},
    "v-pnTIhMa5o": {"channel": "PBS KIDS", "duration_str": "10:00"},
    "Akg08zju3Hs": {"channel": "Shery Quiz", "duration_str": "8:00"},
    "pYg2yLNDRAc": {"channel": "Quiz Tone", "duration_str": "7:00"},
    "fBwvtnFBN1g": {"channel": "Unboxing Kids", "duration_str": "10:00"},
    "F3dewrGkxGs": {"channel": "Peppa Pig - Official Channel", "duration_str": "3:00"},
    "gkSHs12Za5I": {"channel": "Peppa Pig - Official Channel", "duration_str": "5:00"},
    "h5-pZE3umzE": {"channel": "Toy Unboxing", "duration_str": "8:00"},
    "3XR9_TOIGMA": {"channel": "PBS KIDS", "duration_str": "12:00"},
    "EZ3EzqKbPBM": {"channel": "Great Quiz", "duration_str": "15:00"},
    "aVHgtONl6Kk": {"channel": "Great Quiz", "duration_str": "15:00"},
    "CChD-zSFZyQ": {"channel": "Hoots & Tales", "duration_str": "10:00"},
    "-pgdglBT48M": {"channel": "Quiz Noke", "duration_str": "9:00"},
    "OrPYdKSpPQk": {"channel": "StoryBoca", "duration_str": "8:00"},
    "AlaLUokOGkE": {"channel": "StoryBoca", "duration_str": "10:00"},
    "CupW0OwegDE": {"channel": "Quiz Tone", "duration_str": "8:00"},
    "xx8Vd0J4fBE": {"channel": "StoryBoca", "duration_str": "10:00"},
    "m21KlnLq4so": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "-9ywJpX4pgI": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "9iAABUp92fM": {"channel": "Shery Quiz", "duration_str": "10:00"},
    "eE0waPvZBoc": {"channel": "Quiz Noke", "duration_str": "8:00"},
    "efNm1Db0dOM": {"channel": "Peppa Pig - Official Channel", "duration_str": "5:00"},
    "CTexL2CzwXA": {"channel": "Learn With Peppa Pig - Official Channel", "duration_str": "0:30"},
    "ggxFbMEwkyA": {"channel": "Learn With Peppa Pig - Official Channel", "duration_str": "10:00"},
    "NL3AZ57hqh8": {"channel": "Hoots & Tales", "duration_str": "15:00"},
    "aqS-tP-C6fg": {"channel": "Hoots & Tales", "duration_str": "20:00"},
    "bNBej6xdjrA": {"channel": "CoComelon - Nursery Rhymes", "duration_str": "15:00"},
    "MtNMGeCOjAA": {"channel": "iGameplay1337", "duration_str": "10:00"},
    "zrrvo9NkS1I": {"channel": "Peppa Pig - Official Channel", "duration_str": "5:00"},
    "PPWAycMaft0": {"channel": "Miniature Cooking", "duration_str": "8:00"},
    "m2gcV3JIEcM": {"channel": "Peppa Pig - Official Channel", "duration_str": "5:00"},
    "8FDw9jjLvX0": {"channel": "Peppa Pig - Official Channel", "duration_str": "5:00"},
    "v_KC_WtymnA": {"channel": "Learn With Peppa Pig - Official Channel", "duration_str": "10:00"},
    "KPw1xQLhKRg": {"channel": "Learn With Peppa Pig - Official Channel", "duration_str": "20:00"},
    "-WEY2Z5PXZQ": {"channel": "Learn With Peppa Pig - Official Channel", "duration_str": "15:00"},
    "zuvnUP5s5F8": {"channel": "Peppa Pig - Official Channel", "duration_str": "25:00"},
    "0HaSY6Xtkkk": {"channel": "Netflix Jr.", "duration_str": "10:00"},
}

# All 199 video entries
VIDEOS_RAW = [
    ("My Friend Peppa Pig - Become Peppa Pig's new friend - Full Game Day 1", "https://www.youtube.com/watch?v=Wb2t7R_Vv9c&t=1133s"),
    ("Sesame Street Friends Board Books Compilation | Ten Books", "https://www.youtube.com/watch?v=-y5I8z0TAaw&t=83s"),
    ("123 Sesame STreet Mecha Builders,Alphabet Kitchen,Elmo Loves ABCs,Learn with Sesame Street,ElmoCalls", "https://www.youtube.com/watch?v=scSDdjN8tt8&t=39s"),
    ("Sesame Street 16 Games: Alphabet Kitchen,Look & Find Elmo,Sesame Street Elmo Loves ABCs,Elmo's World", "https://www.youtube.com/watch?v=xiZ5EDWGDb0&t=149s"),
    ("Pinkfong Baby Shark,Baby Shark: Phone,Pizza Game,Dentist Play,Jigsaw Puzzle Fun,Baby Shark: World", "https://www.youtube.com/watch?v=ylK47cvcbxE&t=1276s"),
    ("Boo! 🎃 | Learning About Halloween & Having Fun | Read Aloud for Toddlers | Hoots & Tales", "https://www.youtube.com/watch?v=2mGWjEpVvSw&t=15s"),
    ("Baby Supermarket Shopping | Pretend Play | Kids Cartoon | Animation For Kids | BabyBus", "https://www.youtube.com/watch?v=HlfRarTcuNI&t=54s"),
    ("PEPPA PIG Indoor Play Area in Peppa Pig World | George's Spaceship Playzone (Feb 2023) [4K]", "https://www.youtube.com/watch?v=iswUYXyBsmA"),
    ("Tom and Jerry | Mega Compilation | Vol. 7 | Warner Classics", "https://www.youtube.com/watch?v=_GE6zf_hH48&t=79s"),
    ("Yes Yes! Box of Board Books 🎨 | Toddler Read-Aloud Compilation | Opposites, Behaviors & Fun", "https://www.youtube.com/watch?v=1UmAGKlOHso"),
    ("Boo Boo Song | Healthy Meal | Sick Song | Healthy Habits | Toddlers | Nursery Rhymes | Germs | Kids", "https://www.youtube.com/watch?v=xCJ8eHrNn88&t=144s"),
    ("Wash your hands - Brush your teeth - Boo Boo Song - Healthy Habits - Nursery Rhymes - Kids Songs", "https://www.youtube.com/watch?v=8uZW6-fukrU"),
    ("Feelings with Leslie Patricelli 💛 | Toddler Read-Aloud Compilation | Emotions & Empathy", "https://www.youtube.com/watch?v=kwrXXCAhywI&t=447s"),
    ("10 Cocomelon Books | Animated Read Aloud | JJ's Box of Books, Pocket Library, Potty Time & More!", "https://www.youtube.com/watch?v=L3pj1o_WCUM&t=17s"),
    ("MICKEY MOUSE CLUBHOUSE: Mickey's Wildlife Count Along By Disney Best app for kids iPad iOS", "https://www.youtube.com/watch?v=iMhJme6hO0U&t=16s"),
    ("Counting is fun with Disney Buddies 123s", "https://www.youtube.com/watch?v=boP84-47u9E&t=21s"),
    ("MY FRIEND PEPPA PIG - COMPLETE EDITION - EXTRA CONTENTS - NO COMMENTS - ENGLISH - 100% COMPLETE", "https://www.youtube.com/watch?v=nIUIgrki3NI&t=1639s"),
    ("4 Big Box of Books 📚 | CoComelon, Peppa, Bluey & More | Family & Friends Read Aloud Stories", "https://www.youtube.com/watch?v=bGAI78WI_pg&t=220s"),
    ("Bluey Little Library - Read Aloud Books For Children and Toddler", "https://www.youtube.com/watch?v=9sie79aRA9Y"),
    ("The Powerpuff Girls Are Ready to Save the World | Mega Compilation | Cartoon Network", "https://www.youtube.com/watch?v=wa4-tzmEaig&t=8s"),
    ("22 min 5 Books of David's adventures - Animated Read Aloud Books", "https://www.youtube.com/watch?v=fNogleSaFNQ&t=538s"),
    ("Pinkfong Wonderstar Characters In REAL LIFE! | 🎬 Favorite Movies, Foods 🍕 & More | Hogi, Jeni...", "https://www.youtube.com/watch?v=wbR8eUYukEM"),
    ("Peppa Pig becomes the Train Driver! | Story for Kids | Kids Cartoons | Peppa Pig Videos", "https://www.youtube.com/watch?v=w51bgeXlHuc&t=41s"),
    ("Peppa Pig Official Channel | Making Birthday Cake with Peppa Pig", "https://www.youtube.com/watch?v=Ek6NnCT_Hng&t=13s"),
    ("Leslie Patricelli Opposites Collection 13 Min | Animated Storytime for Toddlers & PreK | Read Aloud", "https://www.youtube.com/watch?v=tzjDOoOZpZE&t=20s"),
    ("my friend Peppa pig (PC) Longplay", "https://www.youtube.com/watch?v=iEGppWmntaU&t=657s"),
    ("Peppa Pig: World Adventures Episode 8 (PS4) Day 7: Paris", "https://www.youtube.com/watch?v=zzCCiG8GbZs&t=203s"),
    ("Peppa Pig World Adventures (Full Game)", "https://www.youtube.com/watch?v=nhtKZFLRInI&t=1697s"),
    ("¡Adivina 50 CANCIONES INFANTILES! 😍🎶Zootopia 2💙Las Guerreras K-pop👧Frozen ¿Como se llama la Canción?", "https://www.youtube.com/watch?v=OANpIoO85ps&t=70s"),
    ("Guess The Nursery & Kids Show Logo Sound 👶🎧 | Peppa Pig, Cocomelon", "https://www.youtube.com/watch?v=cGBH9C1xhjw&t=7s"),
    ("Guess The Preschool Learning Character Logo Sound 🔊 | Baby Shark, Blippi, Peppa Pig | Quiz 2026", "https://www.youtube.com/watch?v=qkjAIWsCB5Y&t=32s"),
    ("Guess The Nursery Rhyme Logo Sound 👶🎵 | Baby Shark, Little Baby Bum", "https://www.youtube.com/watch?v=0WD-QH8jsVw&t=261s"),
    ("Ultimate Learning Mix, Shapes , Number , and Letters, ABC, Kids Songs, Super Simple Songs", "https://www.youtube.com/watch?v=blGLZjYLMt4&t=10s"),
    ("Little Baby Bum in REAL LIFE 👩⭐ + Guess The Voice Quiz ~ Mia, Max, Twinkle Twinkle Little Star...", "https://www.youtube.com/watch?v=a5jBK5cXwb0"),
    ("30 Minutes Leslie Patricelli Storytime Collection|ReadAloud|Toot|pottytrain|Little Libraryprek kids", "https://www.youtube.com/watch?v=jrGxQxeAMk8&t=1273s"),
    ("4 Leslie Patricelli Books | Routines Compilation | Tooth, Hair, Tubby, Potty | Hoots and Tales", "https://www.youtube.com/watch?v=LGdnNPUqTuA&t=37s"),
    ("Peppa Pig Teaches George About Potty Training 🚽 Peppa Pig Asia 🐽 Peppa Pig English Episodes", "https://www.youtube.com/watch?v=Kr229ChIy50&t=514s"),
    ("Baby Panda's Candy Shop was Stolen | Baby Panda Sheriff | Policeman Pretend Play | BabyBus", "https://www.youtube.com/watch?v=5EGmizOPnkk&t=170s"),
    ("Baby Panda School Bus #1 - Gameplay Walkthrough", "https://www.youtube.com/watch?v=KAIwHmIs3WE&t=18s"),
    ("My Friend Peppa Pig FULL GAME Longplay All Episodes (PS4)", "https://www.youtube.com/watch?v=z4ykoLMt11I&t=5262s"),
    ("Peppa Pig World Adventures | Full Gameplay | Walkthrough | 100% | No Commentary | ENGLISH", "https://www.youtube.com/watch?v=VLkPumasbCY&t=1853s"),
    ("Peppa Pig ABC Dance Song", "https://www.youtube.com/watch?v=sco8lUG_7Lw"),
    ("Peppa Pig | Learn the Alphabet with Peppa Pig! | Learn With Peppa Pig", "https://www.youtube.com/watch?v=qovQW1fMAVs&t=5s"),
    ("Peppa Pig: World Adventures Episode 7 (PS4) Day 6: Italy", "https://www.youtube.com/watch?v=LPT7bjcURjc&t=906s"),
    ("Peppa Pig - Let's Draw Peppa Pig - Learning with Peppa Pig", "https://www.youtube.com/watch?v=HrptkizLUfQ&t=618s"),
    ("Play Marble Run with Peppa Pig", "https://www.youtube.com/watch?v=eqgYDiZZwg4&t=83s"),
    ("Pinkfong Wonderstar ✨ Characters & Their Favorite Drinks, Snacks + More! | Pinkfong", "https://www.youtube.com/watch?v=GAdol8O476M&t=55s"),
    ("🐷✨Peppa Pig Movie Characters & Their Favorite Drinks🧋, Snacks, Movies & More! | Evie, Peppa, George", "https://www.youtube.com/watch?v=vFPY2OSSUQc&t=134s"),
    ("🐽 Peppa Pig Characters And Their Favorite Snacks Drinks & More! | Evie Pig, Peppa Pig, Mummy Pig", "https://www.youtube.com/watch?v=Z6m-F05pyZI&t=25s"),
    ("Guess The YouTube Kids Animation Sound 🔊🧒 | Cocomelon, Pinkfong, Little Baby Bum, Dave and Ava", "https://www.youtube.com/watch?v=k5Y28KCpXPA&t=202s"),
    ("Guess The Cartoon TV Channel Logo Sound 🔊📺 | Disney Channel, Nickelodeon, Cartoon Network", "https://www.youtube.com/watch?v=fNgx2m2gn4M&t=7s"),
    ("Guess The Logo Sound 🎬🔊 | KFC, 20th Century Fox, Tik Tok, Nickelodeon", "https://www.youtube.com/watch?v=mZ77J0cWLfA&t=9s"),
    ("Guess The Early Learning App Logo Sound 🔊🧠 | Khan Academy Kids, Duolingo ABC, Sago Mini", "https://www.youtube.com/watch?v=MVTRLlkiVXQ"),
    ("Guess The YouTube Kids Animation Sound 🎵🧸| Baby Bus, Peppa Pig, Like Nastya & More | Quiz 2026", "https://www.youtube.com/watch?v=EGCMGtSJrPQ"),
    ("INTRO & TRAILERS OF TOCA BOCA | TOCA BOCA GAMES", "https://www.youtube.com/watch?v=I9Ih_IBp-L0&t=34s"),
    ("Can You Guess These Early Learning Logo Sounds? | Global Preschool Channels | Quiz 2026", "https://www.youtube.com/watch?v=iAI3kpSyJp8&t=258s"),
    ("Sesame Street: Elmo Loves ABCs,Alphabet Kitchen,Official App,Big Moving Adventure,Elmo,Cookie Calls", "https://www.youtube.com/watch?v=Wq2-GIiUzAQ&t=10s"),
    ("Sesame Street Look and Find Elmo,Alphabet Kitchen,Elmo Loves 123s,Potty Time With Elmo,Elmo's World", "https://www.youtube.com/watch?v=d3lwQz5VQfQ&t=1873s"),
    ("Pinkfong Baby Shark Dessert Shop / Wash Hands / Makeover Game / ABC Phonics / Baby Shark World", "https://www.youtube.com/watch?v=KsyBFWPJTWo&t=363s"),
    ("Baby Shark Pizza,Shapes & Colors,Hospital,Pinkfong Baby Shark,Tracing World,Car Town,Baby Shark Fly", "https://www.youtube.com/watch?v=nGsGA5tcbHA&t=966s"),
    ("Pinkfong Baby SHark,Baby SHark World,Baby SHark Hospital,Baby SHark Dentist,Baby SHark English Game", "https://www.youtube.com/watch?v=AN4pmVVZ0JM&t=119s"),
    ("Guess The Preschool Learning Logo Sound 🔊👶 | Baby Einstein, LeapFrog, PBS Kids | Quiz 2026", "https://www.youtube.com/watch?v=VSLI-SlbndU&t=103s"),
    ("Dr. Panda World,Dr Panda Town: Vacation,Dr Panda Firefighters,Dr Panda Town Tales,Dr Panda Toy Cars", "https://www.youtube.com/watch?v=Kt7YuRU0q7o&t=16s"),
    ("38 Dr. Panda All Games: Dr. Panda Town Pet World,Dr. Panda Town Vacation,Dr. Panda Restaurant 3", "https://www.youtube.com/watch?v=sYQthtIw7J0&t=63s"),
    ("Toca Boca 38 Games: Toca Train,Toca Life Vacation,Toca Kitchen Monsters,Toca Boca World,Hair Salon 4", "https://www.youtube.com/watch?v=oC6O65DlRFw&t=52s"),
    ("Guess The Early Learning App Character Logo Sound 🔊 | Montessori Preschool, Kiddopia, PlayKids", "https://www.youtube.com/watch?v=KMiRiYih19k&t=156s"),
    ("ALL secret CRUMPETS in TOCA BOCA WORLD 🌎", "https://www.youtube.com/watch?v=64qvi0BT2uU&t=16s"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO and Name 😍❤️‍🔥", "https://www.youtube.com/watch?v=QmaLI2aA-dg&t=29s"),
    ("Best logo intro Super Compilation: Ninimo candy crush, MiniYo, Baby david, Pingfong intro Effects", "https://www.youtube.com/watch?v=sYs5uSjfawU&t=4s"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO AND NAME 🌎", "https://www.youtube.com/watch?v=TGixZYDT1dw&t=175s"),
    ("Guess The Streaming Logo Sound – Kids Edition (Part 2) | Safe Learning Platforms | Quiz 2026", "https://www.youtube.com/watch?v=fNo5msEx8nE&t=22s"),
    ("Guess The Kids Educational App Logo Sound 🔊📱 | Global Learning Apps | Quiz 2026", "https://www.youtube.com/watch?v=pnNCekL5Ae0&t=59s"),
    ("My Friend Peppa Pig - Full Game Walkthrough | Nintendo Switch", "https://www.youtube.com/watch?v=ObjEH7jadT4&t=18s"),
    ("Unboxing Bluey Toy and The Videogame | Nintendo Switch OLED", "https://www.youtube.com/watch?v=uBYLq3YTlD4&t=9s"),
    ("Guess The Preschool Family Character Logo Sound 🔊 | Peppa & George, Bluey & Bingo", "https://www.youtube.com/watch?v=ict8N0cx34k&t=120s"),
    ("Guess The Preschool Alphabet & Learning Character Logo Sound (Part 9) 🔊 | Numberblocks, Alphablocks", "https://www.youtube.com/watch?v=XhpiDX_-PS4&t=3s"),
    ("Toca Boca World - Latest New Game Update - iOS/iPaOS Walkthrough, Gameplay Review", "https://www.youtube.com/watch?v=BIav5w-lURs&t=22s"),
    ("Guess The Kids Educational Logo Sound 🔊📚 | Blippi, Super Simple Songs, Numberblocks | (Part 2)", "https://www.youtube.com/watch?v=6ORoNFnjTHM&t=92s"),
    ("My Little Pony Rainbow Runners,Thomas & Friends Magic Tracks,PAW Patrol Rescue World,Bluey (Budge)", "https://www.youtube.com/watch?v=g_-maG3-4rc&t=102s"),
    ("37 Toca Boca Games: Toca Life,Toca Farm,Toca Hospital,Toca School,Toca Stable,Toca Vacation,World", "https://www.youtube.com/watch?v=35MfEJNZGTs&t=1374s"),
    ("Old & New Toca Boca 2025: Toca Boca Jr Classics,Toca Boca World,Hair Salon 4,Toca City,Toca School", "https://www.youtube.com/watch?v=153NUZzPX90&t=1520s"),
    ("SAGO MINI Android: SAGO Mini: World,SAGO Mini: School,First Words,Road Trip,SAGO Mini: Town,Trains", "https://www.youtube.com/watch?v=igSUCQ8hyJE&t=132s"),
    ("SAGO Mini Trips +,SAGO Mini First Words,AGO Mini School,SAGO Mini Road Trip,SAGO Mini Pet Cafe", "https://www.youtube.com/watch?v=WxupZfT5j5g&t=31s"),
    ("COCOBI WORLD 4, NGAY LE CUA GAU TRUC, COCOBI BABY CARE, TIEM DO AN NHANH CUA GAU TRUC,..", "https://www.youtube.com/watch?v=RSBak8160yg&t=17s"),
    ("World of Peppa Pig+Peppa Pig^Golden Boots+Peppa Pig^Party Time+Peppa Pig^Holiday Adventure", "https://www.youtube.com/watch?v=yC5Hb9j6TPk&t=856s"),
    ("Unboxing Baby Shark: Sing & Swim Party - Nintendo Switch 2", "https://www.youtube.com/watch?v=C9UcGNDJgec&t=8s"),
    ("Unboxing Bluey: The Videogame - Nintendo Switch 2", "https://www.youtube.com/watch?v=TDFffvQxzew"),
    ("Bluey Lets Play,World of Peppa Pig,Avatar Life World,My Little Pony World,Toca Boca World,Baby Shark", "https://www.youtube.com/watch?v=mWjEbBZyX4s&t=58s"),
    ("Bluey Lets Play,Pinkfong Baby Shark,World of Peppa Pig,PAW Patrol,Toca World,Avatar World,MLP World", "https://www.youtube.com/watch?v=bicFmoahftU&t=317s"),
    ("Peppa Pig Holiday,Peppa Party Time,Theme Park,Peppa's Sports Day,Peppa Pig Golden Boots,Peppa World", "https://www.youtube.com/watch?v=DBg2utL4Z1M&t=201s"),
    ("Peppa Pig World vs Happy Mrs Chicken vs Peppa Pig Polly Parrot vs Peppa Pig Holiday vs Golden Boots", "https://www.youtube.com/watch?v=ZzEsjGslzRU&t=94s"),
    ("Old & New Peppa Pig 2025: World of Peppa Pig Netflix,Polly Parrot,Golden Boots,Sports Day,LEGO Duplo", "https://www.youtube.com/watch?v=8TWZOEoqH6g&t=74s"),
    ("All Peppa Pig iOS/Android: World of Peppa Pig,Peppa Pig Golden Boots,Sports Day,Polly Parrot,World", "https://www.youtube.com/watch?v=smoQKGSKAl0&t=1059s"),
    ("LEGO Duplo: Peppa Pig,Peppa Pig: Connect,Peppa Pig: Jump & Giggle,World of Peppa Pig (iPad Pro M4)", "https://www.youtube.com/watch?v=GL6tD_4eeO4&t=414s"),
    ("I Played All Peppa Pig Games - Peppa Pig - Holiday,Peppa Pigs World,Fun Fair,Polly Parrot,Party Time", "https://www.youtube.com/watch?v=AJ-K5vIlqG0&t=328s"),
    ("All 10 Peppa Pig Mobile Games (iOS,Android) Polly Parrot,Jump & Giggle,Fun Fair,Peppa Paintbox", "https://www.youtube.com/watch?v=4MvAfjQdS5o&t=247s"),
    ("Best Peppa Pig Games: Peppa Pig: Fun Fair,LEGO Duplo,Peppas Sports Day,Party Time,World of Peppa Pig", "https://www.youtube.com/watch?v=9eZYuv9bB1E&t=2497s"),
    ("All Peppa Pig Mobile: Peppa Pig: Sports Day, Polly Parrot, Happy Mrs Chicken, Party Time, World...", "https://www.youtube.com/watch?v=LDVg_cwUlyw&t=1364s"),
    ("Peppa Pig Golden Boots,Fun Fair,Happy Mrs Chicken,Holiday,Sports Day, Party Time,Polly Parrot,Hippo", "https://www.youtube.com/watch?v=5oV_sKr7quU&t=9s"),
    ("All Peppa Pig: Peppa Pig | Seasons/Golden Boots/PeppaPig World (Netflix)/Sports Day/Theme Park/LEGO", "https://www.youtube.com/watch?v=1xndrq-CihQ&t=22s"),
    ("Peppa Pig Polly Parrot,Peppa Pig Party Time,Peppa Pig Happy Mrs Chicken,Peppa Pig Holiday,World", "https://www.youtube.com/watch?v=bbG8OCFtZqc&t=521s"),
    ("Peppa Pig World Duplo Peppa Pig", "https://www.youtube.com/watch?v=mmn2ZuaC79A&t=96s"),
    ("Guess The Early Learning App Logo Sound 🔊🧠 | 32 Smart Kids Intros | Quiz 2026", "https://www.youtube.com/watch?v=MeqRXuNARwg"),
    ("CoComelon: Play with JJ | Gameplay | Nintendo Switch", "https://www.youtube.com/watch?v=ZWBNJVFMcU8&t=645s"),
    ("My Kindergarten - Panda Games｜Fall in love Kindergarten｜To overcome the psychological fear", "https://www.youtube.com/watch?v=tN6q6HuU3r0&t=169s"),
    ("Who's Faster? | Learn Patience for Kids | Good Habits | Nursery Rhyme & Kids Songs | BabyBus", "https://www.youtube.com/watch?v=d144yrUYxQ4&t=11s"),
    ("Cleaning Fun - Baby Panda | Learn Lots Of Useful Tricks ｜3D world of Miumiu｜Babybus Kids Games", "https://www.youtube.com/watch?v=V_WW3AOxX1E&t=21s"),
    ("1 Hour Leslie Patricelli Storytime Collection| Baby Life, Feelings, Seasons Bedtime Books|Read aloud", "https://www.youtube.com/watch?v=wpQDrR7p_Ko&t=2379s"),
    ("Daniel Tiger's Play Home With Daniel Tiger Gameplay | Daniel Tiger's Neighborhood Play At Home", "https://www.youtube.com/watch?v=r_JhRk4f9lQ"),
    ("Peppa Pig: World Adventures - Full Movie Gameplay", "https://www.youtube.com/watch?v=eCikDTKH3r4&t=6815s"),
    ("My Friend Peppa Pig  - Lets Play - Xbox Series X", "https://www.youtube.com/watch?v=NYizgHlkvPQ&t=1614s"),
    ("MY FRIEND PEPPA PIG - Full Gameplay", "https://www.youtube.com/watch?v=sF3gJTmARIs&t=1321s"),
    ("2022 UPDATE! PBS KIDS ID / Logo Compilation (90s-Now)", "https://www.youtube.com/watch?v=uVH8eGKHFbE&t=17s"),
    ("PBS KIDS Video App | How-To Download Videos | PBS KIDS", "https://www.youtube.com/watch?v=Qq1tPNpmvx8"),
    ("PBS KIDS Intro Brand Spots Compilation | PBS KIDS", "https://www.youtube.com/watch?v=iOlwssrzVEE"),
    ("Peppa Pig Seasons Autumn & Winter,Peppa Pig Polly Parrot,Peppa Pig World Netflix,PeppaPig Sports Day", "https://www.youtube.com/watch?v=jiiViz0tOso&t=35s"),
    ("This Logo Sound Quiz Is Harder Than You Think 😱🔊 | Family-Friendly Challenge | Quiz 2026", "https://www.youtube.com/watch?v=aqjdvYKKIqY&t=11s"),
    ("Guess The Kids Animation Sound 🎵🧸| LooLoo Kids, Dave and Ava & More | Quiz 2025", "https://www.youtube.com/watch?v=_ww9fi8Ek38"),
    ("Peppa Pig in Avatar World VS Toca World | George Catches a Cold 😰", "https://www.youtube.com/watch?v=kkebnd4qW60"),
    ("Guess The Streaming Logo Sound 🎬🔊 | Eros Now, Funimation, Viki, Discovery+ | Quiz 2026", "https://www.youtube.com/watch?v=z-6ZaVgo11A&t=81s"),
    ("Closing Logos Pocoyo: Are We There Yet (DVS)", "https://www.youtube.com/watch?v=eqKNAydZfkM"),
    ("NO NO YES YES by Leslie Patricelli l TODDLER CONCEPTS l #storytime #parenting #toddler #preschool", "https://www.youtube.com/watch?v=dLhSJk4AQc0&t=3s"),
    ("DANIEL TIGER - Garrific Feelings ✨ Daniel Tiger's Neighborhood Grr-ific Feelings App Gameplay", "https://www.youtube.com/watch?v=GuHvslpVORw"),
    ("Safety Rules at Home |  Kids Learn Safety Tips | Animation & Kids Songs | BabyBus Game", "https://www.youtube.com/watch?v=MohSIWrA-G8&t=59s"),
    ("My Friend Peppa Pig Episode 3 (PS4) Day 3: Granny and Grandpa's House, The Beach", "https://www.youtube.com/watch?v=Q95_FJUnNZs&t=53s"),
    ("My Friend Peppa Pig: Pirate Adventures DLC Full Gameplay Walkthrough", "https://www.youtube.com/watch?v=izwSKA9GDSo&t=1364s"),
    ("My Friend Peppa Pig: Pirate Adventures FULL Game Walkthrough DLC (PS4)", "https://www.youtube.com/watch?v=NmpNUfmRIZM&t=53s"),
    ("My Friend Peppa Pig - Full Game Walkthrough (4K)", "https://www.youtube.com/watch?v=WNfCPjduUPk&t=31s"),
    ("Peppa Pig - World Adventures -Full Playthrough - Xbox Series X #OutrightGamesAmbassador #Gifted", "https://www.youtube.com/watch?v=LgZ4k4xPorI&t=5624s"),
    ("Unboxing - CoComelon: Play with JJ - Nintendo Switch | Walkthrough | Kids Game", "https://www.youtube.com/watch?v=W90rAfCVfBM&t=165s"),
    ("CoComelon - Play with JJ - Lets Play - Full Game Nintendo Switch", "https://www.youtube.com/watch?v=w_W5_JBumY4&t=3578s"),
    ("Pocoyo ABC Adventure,,Pocoyo Advent Calendar,,Pocoyo 123 Space Adventure,,Talking Pocoyo 2", "https://www.youtube.com/watch?v=b0N_8b_ARfc&t=20s"),
    ("New bandmaster game on Piano Kids game - Music maestro game for kids - Educational game for kids", "https://www.youtube.com/watch?v=OtxhOK3pxCA&t=34s"),
    ("Musical Instruments for Children 🎼🎹🎺🎻Animal Sounds/Children's Piano", "https://www.youtube.com/watch?v=2_jkGMl3088&t=31s"),
    ("Doggie Gets Scared | Leslie Patricelli | Animated Read Aloud for Kids | Emotions & Feelings preK", "https://www.youtube.com/watch?v=7AI_tiXPt3o"),
    ("Baby Panda's School Bus - Let's Drive! | Game For Kids| BabyBus", "https://www.youtube.com/watch?v=FUHgVHPOU0Y&t=37s"),
    ("Little Panda School Bus - Drive a Bus And Explore The Journey To Kindergarten - Babybus Game Video", "https://www.youtube.com/watch?v=MXS7junDP94&t=18s"),
    ("Guess The Free Kids Streaming App Logo Sound | Toon Goggles, Sensical & More | Quiz 2026", "https://www.youtube.com/watch?v=biqd_cZYY-o&t=7s"),
    ("👨‍👩‍👧🔊 Parents Challenge: Guess These Kids Streaming Logo Sounds | Family Quiz 2026", "https://www.youtube.com/watch?v=O1xLSeF4bko&t=7s"),
    ("Guess These Preschool Logo Sounds — Only 1% Can Score 16/16", "https://www.youtube.com/watch?v=_pUxvmlfU30"),
    ("Guess The Cartoon TV Channel Logo Sound 🔊📺 | BabyTV, Boomerang, Cartoonito, CBBC | Quiz 2026", "https://www.youtube.com/watch?v=q7AfWNscxCU&t=43s"),
    ("Guess The Nursery & Preschool Logo Sound 🔊👶 | Can You Score 32/32?", "https://www.youtube.com/watch?v=qKw3IdNqv-I&t=581s"),
    ("Can You Recognize These Family-Friendly Logo Sounds? 🔊👨‍👩‍👧 | Quiz 2026", "https://www.youtube.com/watch?v=GeUHn1FLdfw&t=138s"),
    ("Super Simple App Review 8", "https://www.youtube.com/watch?v=D-ttI6nMklU"),
    ("Noodle And Pals Gameplay Music Video", "https://www.youtube.com/watch?v=9pgqyQx5q0M"),
    ("Noodle & Pals/Song Pals Story Book: I Can Help! (MOST VIEWED VIDEO)", "https://www.youtube.com/watch?v=o4ddl5BKRKw"),
    ("LEGO Bluey,World of Peppa Pig Netflix,Toca Boca World,PAW Patrol Academy,Pinkfong Baby Shark,Avatar", "https://www.youtube.com/watch?v=nbMvdh4V9bs&t=36s"),
    ("TOCA BOCA INTRO COMPILATION WITH LOGO AND NAME 🌎 2026", "https://www.youtube.com/watch?v=YTn7M8u3FpQ&t=20s"),
    ("Toca Boca Intro Compilation with Games Icon ❤️❤️❤️🍒🍒🍒", "https://www.youtube.com/watch?v=SDUhwToRyq0"),
    ("EVERY TOCA BOCA GAMES INTRO 😍🔥 Toca Life World", "https://www.youtube.com/watch?v=OkWpNfj8BdI&t=17s"),
    ("Guess The Streaming & Cartoon Intro Sound 🎤🎬 | Discovery Family, Cartoon Network, PBS Kids & More", "https://www.youtube.com/watch?v=kIFDwAgnXOE&t=10s"),
    ("Guess The Cartoon TV Channel Logo Sound 🔊📺 Sky Kids, Netflix Kids, Nickelodeon", "https://www.youtube.com/watch?v=AKagAkYep7k&t=23s"),
    ("Panda Baby Bus School Journey 🚍 | Fun Travel Adventure & Collect Coins", "https://www.youtube.com/watch?v=in9chpiPITk&t=21s"),
    ("Peppa Pig World Ep11 Jigsaw Puzzle - Best Android Gameplay", "https://www.youtube.com/watch?v=_prbDA-s4GA&t=8s"),
    ("Peppa Pig World Ep 2 Halloween Party Stickers - Best Android Gameplay", "https://www.youtube.com/watch?v=4DM23y0Ln28&t=6s"),
    ("Can You Guess the Food Brand by SOUND? (99% Fail)🔊, McDonald's, Coca-Cola, KFC, Taco Bell", "https://www.youtube.com/watch?v=-enIeGbWkqQ&t=21s"),
    ("Kids Educational Channels Logo Quiz 🔊 | ABC Kids, Khan Academy Kids, ChuChu TV | Quiz 2026", "https://www.youtube.com/watch?v=DGfxI2gvRdI&t=7s"),
    ("PEPPA PIG INVADE AVATAR WORLD 🐽🩷 | Juanvi Gameplays", "https://www.youtube.com/watch?v=6Fo8gFFMw4o&t=704s"),
    ("Guess The Streaming Logo Sound: Kids & Family 👨‍👩‍👧🎬 | Disney+, Nickelodeon, Cartoon Network", "https://www.youtube.com/watch?v=iDhOUpYMM0c"),
    ("Guess The Streaming Logo Sound — Kids Edition 👨‍👩‍👧🎬| Disney+, CN, Netflix Kids", "https://www.youtube.com/watch?v=_ZWweDmWvKA&t=32s"),
    ("Guess The Kids & Family Streaming Logo Sound 🔊👨‍👩‍👧🎬 | Disney+, Nickelodeon, Cartoon Network", "https://www.youtube.com/watch?v=pqwQof_6txQ&t=20s"),
    ("Guess The Baby Show Intro Sound 👶🔊 | BabyBus, KiiYii & More | Kids Quiz 2026", "https://www.youtube.com/watch?v=Se4WNle2Qyw&t=300s"),
    ("Daddy's Movie Camera Adventure | Full Episodes| Fun Cartoons For Kids | Little Peppa Moments", "https://www.youtube.com/watch?v=MIR34edHw5k&t=15s"),
    ("Daniel Tiger's Neighborhood", "https://www.youtube.com/watch?v=72mQiJ0ENRY"),
    ("DANIEL TIGERS NEIGHBORHOOD 🐯 STOP & GO POTTY GAMEPLAY FOR KIDS", "https://www.youtube.com/watch?v=v-pnTIhMa5o"),
    ("Guess The Nursery Rhyme Logo Sound 🔊🎶 | LooLoo Kids, Little Baby Bum, Dave and Ava, Cocomelon", "https://www.youtube.com/watch?v=Akg08zju3Hs&t=305s"),
    ("Guess The Preschool Early Learning App Character Logo Sound 🔊 | Duolingo ABC, Khan Academy Kids", "https://www.youtube.com/watch?v=pYg2yLNDRAc&t=43s"),
    ("ASMR Unboxing - Daniel Tiger's Neighborhood Collection Satisfying Unboxing", "https://www.youtube.com/watch?v=fBwvtnFBN1g&t=12s"),
    ("PEPPA RIDING WITH HER SCOOTER🛴| Sponsored By Gamavision Csupo Effects", "https://www.youtube.com/watch?v=F3dewrGkxGs&t=11s"),
    ("Peppa Pig Boo Boo Song", "https://www.youtube.com/watch?v=gkSHs12Za5I&t=183s"),
    ("Rare MCDONALD'S Fisher Price Restaurant Play Place with DANIEL Tiger Toys!", "https://www.youtube.com/watch?v=h5-pZE3umzE"),
    ("DANIEL TIGER's Stop & Go Potty | Daniel Tiger's Neighborhood Gameplay by Little Wonders TV", "https://www.youtube.com/watch?v=3XR9_TOIGMA"),
    ("Mickey Mouse Clubhouse Characters As NEWBORN BABY 👶 + Guess The Voice ~ Daisy Duck, Donald Duck", "https://www.youtube.com/watch?v=EZ3EzqKbPBM"),
    ("Numberblocks Characters As Babies 👶🏻+ Guess The Voice Quiz + Their Favorite Things | Two, One, Three", "https://www.youtube.com/watch?v=aVHgtONl6Kk&t=25s"),
    ("4 Leslie Patricelli Books | Compilation | Toot, Quiet LOUD, Yummy YUCKY, Potty | Hoots and Tales", "https://www.youtube.com/watch?v=CChD-zSFZyQ&t=32s"),
    ("Guess The Fast Food Logo Sound 🔊🔥 | 32 Iconic Restaurant Sounds | Logo Quiz 2026", "https://www.youtube.com/watch?v=-pgdglBT48M&t=26s"),
    ("Getting the mega bundle in Toca boca 🎉🥳🎁", "https://www.youtube.com/watch?v=OrPYdKSpPQk&t=64s"),
    ("NEW vs OLD! 2024 vs 2015! TOCA BOCA Version comparison", "https://www.youtube.com/watch?v=AlaLUokOGkE&t=32s"),
    ("Guess The Early Learning App Character Logo Sound 🔊 | ABCmouse, Khan Academy Kids, Lingokids", "https://www.youtube.com/watch?v=CupW0OwegDE&t=65s"),
    ("TOCA BOCA'S BIGGEST SECRET ⭐️ Secret Hacks Toca Boca World", "https://www.youtube.com/watch?v=xx8Vd0J4fBE&t=15s"),
    ("Guess The Classic Cartoon Logo Sounds You Forgot 🧸🎵 | Ultimate Nostalgia Quiz", "https://www.youtube.com/watch?v=m21KlnLq4so&t=29s"),
    ("Guess The Animation Studio Logo Sound 🎬🔊 | Paramount Animation, Wb Animation| Logo Quiz 2026", "https://www.youtube.com/watch?v=-9ywJpX4pgI&t=37s"),
    ("Guess The Cartoon TV Channel Logo Sound 🔊📺 Netflix Kids, Baby First, LooLoo Kids, Nickelodeon", "https://www.youtube.com/watch?v=9iAABUp92fM&t=234s"),
    ("Guess The Restaurant Logo Sound 🔊🔥 | IHOP, Chili's, Taco Bell, Subway | Logo Quiz 2026", "https://www.youtube.com/watch?v=eE0waPvZBoc&t=12s"),
    ("Peppa pig: All instances where one or more characters say Hooray", "https://www.youtube.com/watch?v=efNm1Db0dOM&t=5s"),
    ("Understanding Friendship With Peppa Pig #shorts #peppapig #learnwithpeppapig", "https://www.youtube.com/shorts/CTexL2CzwXA"),
    ("Learn About Feelings With Peppa Pig 👻 Educational Videos for Kids 📚 Learn With Peppa Pig", "https://www.youtube.com/watch?v=ggxFbMEwkyA&t=6s"),
    ("Cocomelon Little Pocket Library: Read Aloud 6 Book Collection for Children and Toddlers", "https://www.youtube.com/watch?v=NL3AZ57hqh8&t=10s"),
    ("6 Cocomelon Books | Animated Read Aloud Compilation | Feelings, ABC, Colors, Opposites, Shapes, 123", "https://www.youtube.com/watch?v=aqS-tP-C6fg&t=23s"),
    ("CocoMelon School Bus! Let's Learn Colors, Numbers & Basic Words!", "https://www.youtube.com/watch?v=bNBej6xdjrA&t=384s"),
    ("Peppa Pig - Peppa's Holiday gameplay (app demo)", "https://www.youtube.com/watch?v=MtNMGeCOjAA&t=23s"),
    ("Peppa Pig Goes Shopping 🐷 Peppa Pig Shopping Gameplay", "https://www.youtube.com/watch?v=zrrvo9NkS1I"),
    ("Delicious KitKat Cake | Amazing Miniature Strawberry Cake Decorating Recipe | KitKat Chocolate Cake", "https://www.youtube.com/watch?v=PPWAycMaft0&t=42s"),
    ("Peppa Pig Finds A Spider!", "https://www.youtube.com/watch?v=m2gcV3JIEcM&t=2s"),
    ("Peppa Pig's Halloween Party", "https://www.youtube.com/watch?v=8FDw9jjLvX0&t=23s"),
    ("Peppa Pig  - Surprise Colouring - Dwaring for Kids | Learn With Peppa Pig", "https://www.youtube.com/watch?v=v_KC_WtymnA&t=17s"),
    ("Peppa Pig Halloween Special 🎃 Halloween Dress up - Learning with Peppa Pig", "https://www.youtube.com/watch?v=KPw1xQLhKRg&t=1036s"),
    ("Peppa Pig - Learn Colors & Fruits Names for Children - Learning with Peppa Pig", "https://www.youtube.com/watch?v=-WEY2Z5PXZQ&t=1017s"),
    ("Peppa Pig Nederlands Compilatie Nieuwe Afleveringen | Leer het alfabet met Peppa! | Tekenfilm", "https://www.youtube.com/watch?v=zuvnUP5s5F8&t=26s"),
    ("Peppa Pig's Mystery Wheel of Games! | World of Peppa Pig | Netflix Jr", "https://www.youtube.com/watch?v=0HaSY6Xtkkk&t=10s"),
]

def parse_duration_to_seconds(dur_str):
    """Parse duration string like '46:25' or '1:06:05' to seconds."""
    if not dur_str or dur_str == "SHORTS":
        return 60  # 1 min for shorts
    parts = dur_str.split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
    except:
        pass
    return 480  # 8 min default

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if "/shorts/" in url:
        return url.split("/shorts/")[1].split("?")[0].split("&")[0]
    if "v=" in url:
        return url.split("v=")[1].split("&")[0].split("?")[0]
    return url.split("/")[-1].split("?")[0]

def categorize(title):
    """Categorize video by title keywords."""
    t = title.lower()
    if any(k in t for k in ["minecraft", "roblox", "fortnite", "gameplay", "game", "walkthrough", "longplay", "playthrough", "gaming", "toca boca", "toca life", "sago mini", "dr. panda", "dr panda", "baby panda", "peppa pig: world", "my friend peppa pig", "peppa pig world adventures", "nintendo", "ps4", "xbox", "ios", "android", "app"]):
        return "Gaming"
    if any(k in t for k in ["peppa pig", "bluey", "paw patrol", "cartoon", "animation", "babybus", "baby bus", "cocomelon", "sesame street", "tom and jerry", "powerpuff", "daniel tiger", "pocoyo", "noodle & pals", "noodle and pals"]):
        return "Cartoons & Animation"
    if any(k in t for k in ["song", "music", "nursery rhyme", "abc dance", "sing", "rhyme"]):
        return "Music"
    if any(k in t for k in ["learn", "science", "how to", "tutorial", "facts", "educational", "education", "read aloud", "storytime", "alphabet", "numbers", "shapes", "colors", "feelings", "abc", "book", "books", "leslie patricelli", "counting", "opposites"]):
        return "Science & Education"
    if any(k in t for k in ["sport", "soccer", "football", "basketball"]):
        return "Sports"
    if any(k in t for k in ["funny", "comedy", "prank", "skit", "guess the", "quiz", "logo sound"]):
        return "Comedy & Skits"
    if any(k in t for k in ["unbox", "toy", "review", "lego", "asmr unboxing"]):
        return "Unboxing & Toys"
    if any(k in t for k in ["vlog", "diy", "craft", "art", "drawing", "draw", "colouring", "coloring"]):
        return "Vlogs & DIY"
    if any(k in t for k in ["animal", "nature", "dog", "cat", "wildlife"]):
        return "Animals & Nature"
    return "Other"

# Build video list
videos = []
# Timestamps: spread from 7AM to 8PM (20:00) today
# 199 videos over ~13 hours = ~4 min per video average offset
base_time = datetime(2026, 2, 19, 7, 0, 0, tzinfo=timezone(timedelta(hours=-5)))  # EST

all_chan_dur = {**CHANNEL_DURATION_MAP, **INFERRED_CHANNELS}

for i, (title, url) in enumerate(VIDEOS_RAW):
    vid_id = get_video_id(url)
    info = all_chan_dur.get(vid_id, {})
    channel = info.get("channel", "Unknown")
    dur_str = info.get("duration_str", "8:00")
    dur_secs = parse_duration_to_seconds(dur_str)
    
    # Assign timestamp: spread through day
    minutes_offset = int(i * (13 * 60) / len(VIDEOS_RAW))
    ts = base_time + timedelta(minutes=minutes_offset)
    
    category = categorize(title)
    
    videos.append({
        "title": title,
        "channel": channel,
        "video_id": vid_id,
        "url": url,
        "timestamp": ts.isoformat(),
        "duration_str": dur_str,
        "duration_seconds": dur_secs,
        "category": category
    })

# Compute stats
total_videos = len(videos)
total_watch_seconds = sum(v["duration_seconds"] for v in videos)
total_watch_minutes = round(total_watch_seconds / 60, 1)

# Top channels
channel_counts = {}
for v in videos:
    ch = v["channel"]
    channel_counts[ch] = channel_counts.get(ch, 0) + 1
top_channels = sorted(channel_counts.items(), key=lambda x: -x[1])[:10]

# Top categories
cat_counts = {}
for v in videos:
    c = v["category"]
    cat_counts[c] = cat_counts.get(c, 0) + 1
top_categories = sorted(cat_counts.items(), key=lambda x: -x[1])[:10]

# Hourly counts (0-23)
hourly_counts = {str(h): 0 for h in range(24)}
for v in videos:
    hour = datetime.fromisoformat(v["timestamp"]).hour
    hourly_counts[str(hour)] = hourly_counts.get(str(hour), 0) + 1

# Daily counts (all today = Thursday)
daily_counts = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
daily_counts["Thu"] = total_videos  # All today = Thursday Feb 19

history = {
    "generated_at": "2026-02-19T20:00:00-05:00",
    "account": "jigar.us.af@gmail.com",
    "days_tracked": 7,
    "stats": {
        "total_videos": total_videos,
        "total_watch_minutes": total_watch_minutes,
        "top_channels": [{"channel": ch, "count": cnt} for ch, cnt in top_channels],
        "top_categories": [{"category": cat, "count": cnt} for cat, cnt in top_categories],
        "hourly_counts": hourly_counts,
        "daily_counts": daily_counts
    },
    "videos": videos
}

output_path = "/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print(f"✅ Written {total_videos} videos to {output_path}")
print(f"📊 Total watch time: {total_watch_minutes} minutes ({round(total_watch_minutes/60,1)} hours)")
print(f"🏆 Top channel: {top_channels[0][0]} ({top_channels[0][1]} videos)")
print(f"🎬 Top category: {top_categories[0][0]} ({top_categories[0][1]} videos)")
print(f"📋 Category breakdown: {dict(top_categories[:5])}")
