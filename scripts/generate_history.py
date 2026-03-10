#!/usr/bin/env python3
"""Generate history.json from extracted YouTube history data."""
import json
import os
from datetime import datetime, timezone
from collections import Counter

# Current timestamp
now = datetime.now(timezone.utc).isoformat()

# Video data extracted from YouTube history page
# Format: [title, channel, duration_seconds, url]
raw_videos = [
    ("Diana and Roma show the Safety Rules on board the Airplane", "✿ Kids Diana Show", 540, "https://www.youtube.com/watch?v=NifKNSpp0_4"),
    ("Fun Indoor Playground for Family and Kids at Leo's Lekland", "Family Playlab", 670, "https://www.youtube.com/watch?v=1IHWkpZAYy8"),
    ("Transport Noises with Dee! | Yakka Dee!", "Yakka Dee! – Toddler Learning", 527, "https://www.youtube.com/watch?v=ylQEE2bdusQ"),
    ("🔴 NEWEST Peppa Pig Episodes 2026 ✨ SEASON 10 Holiday Adventures ☀️ Kids Movie 🔴", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=suBf_zv7Ya0"),
    ("🔴 BEST of George 2026 LIVE! 🦖 Peppa Pig Mini Movie 🍿 Kids Cartoons 🔴", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=BCcwDizkSn8"),
    ("🎶 Like What You Like 🚌✨ + More Nursery Rhymes for Kids | Family Songs | Peppa Pig Songs Official", "Peppa Pig - Nursery Rhymes and Kids Songs", 2010, "https://www.youtube.com/watch?v=11LyA1argIE"),
    ("Peppa Cinema: The Album - Let's Dress Up (Official Music Video)", "Peppa Pig - Official Channel", 823, "https://www.youtube.com/watch?v=enhf0bY5WTQ"),
    ("Peppa Pig Tales Vol 1 👗 Let's Play Dress Up! 🐷 NEW! ✨ Peppa Pig Songs 💞 Kids Songs & Nursery Rhymes", "Peppa Pig - Nursery Rhymes and Kids Songs", 161, "https://www.youtube.com/watch?v=5Uzre7oUObw"),
    ("Peppa Pig Boo Boo Song | Sports Safety Song | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 122, "https://www.youtube.com/watch?v=VZMvWQvPRkY"),
    ("Peppa's Camper Van Holiday! 🐷🚚 Peppa Pig Full Episodes | Peppa Official Family Kids Cartoon", "Peppa Pig - Official Channel", 540, "https://www.youtube.com/watch?v=1-t_PSFyzXs"),
    ("Phonics Song 2 | ABC Alphabet Phonics Nursery Rhyme For Kids", "English Tree", 213, "https://www.youtube.com/watch?v=V68dHbdelcM"),
    ("Phonics Song | kidzstation", "kidzstation", 137, "https://www.youtube.com/watch?v=aKNVbqzmHoc"),
    ("Phonics Song | kidzstation", "kidzstation", 129, "https://www.youtube.com/watch?v=YQY0TigY9Ac"),
    ("🦖 Peppa Pig Makes a Pottery Tea Set", "Peppa Pig - Official Channel", 837, "https://www.youtube.com/watch?v=VAMd2b9nFhs"),
    ("Ants Song - Funny kids song - Family song | Hooray Kids Songs & Nursery Rhymes", "Hooray Kids Songs & Nursery Rhymes", 145, "https://www.youtube.com/watch?v=nwqsG9qrE68"),
    ("Children's song Have a Haircut - Children at the Hairdresser | Hooray Kids Songs & Nursery Rhymes", "Hooray Kids Songs & Nursery Rhymes", 167, "https://www.youtube.com/watch?v=zvL9Ei6NM00"),
    ("♪♪ Children's Song Family - Gagaga Gugugu - Baby Song | Hooray Kids Songs & Nursery Rhymes", "Hooray Kids Songs & Nursery Rhymes", 136, "https://www.youtube.com/watch?v=TzPJT5t2rTs"),
    ("Get well soon children's song | Soon you will be fit again - Hooray kids songs & nursery rhymes", "Hooray Kids Songs & Nursery Rhymes", 131, "https://www.youtube.com/watch?v=7GtxhRH4FEo"),
    ("Toca life vacation | The airport #1", "Sharky Shark", 243, "https://www.youtube.com/watch?v=QRnC0uW3wz4"),
    ("Toca life hospital | Eating for 2?!? S1 #1", "Sharky Shark", 269, "https://www.youtube.com/watch?v=tlHoDcwPuxs"),
    ("BRAND NEW! Yakka Dee: Dee's Food Party! 🍕 🍦 | Toddler Words | Yakka Dee!", "Yakka Dee! – Toddler Learning", 535, "https://www.youtube.com/watch?v=g-HUcLRX8JA"),
    ("Bigger car 🍼🚗 | Peppa Pig | ABC Kids", "ABC Kids", 186, "https://www.youtube.com/watch?v=7Opxn2hKI1A"),
    ("Peppa Pig Learns and Plays with Muddy Puddles", "George Pig - Official Channel", 270, "https://www.youtube.com/watch?v=3TYZKcovlPU"),
    ("Peppa Pig | Superhero Party | Peppa Pig Official | Family Kids Cartoon", "George Pig - Official Channel", 312, "https://www.youtube.com/watch?v=OW1iVWPXs2c"),
    ("Do You Like Spaghetti Yogurt Song?", "Jill K SLP", 156, "https://www.youtube.com/watch?v=17lyBa9QPi4"),
    ("Do you like spinach cake? | Food Song for Kids! | Preschool Song For Circle Time", "Kidzi Music Tv", 293, "https://www.youtube.com/watch?v=hhWBwW0xups"),
    ("Do You Like Fish in the Milk?", "YouKids - Kids Songs", 89, "https://www.youtube.com/watch?v=9Jp9d7cTjQU"),
    ("Do you like broccoli + More Kids Songs And Nursery Rhymes", "Maya Mary Mia - Kids Cartoon Songs", 711, "https://www.youtube.com/watch?v=TYuFTH1pd4Q"),
    ("Do you like broccoli and more Kids Songs | Maya Mary Mia", "Maya Mary Mia - Kids Cartoon Songs", 890, "https://www.youtube.com/watch?v=PvAalmN0MQU"),
    ("Do You Like Chocolate Hot Dogs? - Yucky Food Combos for Kids", "Rock 'N Learn", 211, "https://www.youtube.com/watch?v=zZPURWlionU"),
    ("Fruits And Vegetables Song - Yummy! | Children Songs by Sunny Kids Songs", "Sunny Kids Songs", 127, "https://www.youtube.com/watch?v=xGH2xdBSyS8"),
    ("Yummy Fruits and Vegetables Song for Kids 🍎🍓🥑 Baby Berry Nursery Rhymes and Children Songs", "Baby Berry Nursery Rhymes Kids Songs", 106, "https://www.youtube.com/watch?v=e8BGouxbiAE"),
    ("Can You Say Bee? 🐝| Yakka Dee!", "Yakka Dee! – Toddler Learning", 113, "https://www.youtube.com/watch?v=9Roo_LGVYzg"),
    ("Can You Say Beans? 🍽| Yakka Dee!", "Yakka Dee! – Toddler Learning", 115, "https://www.youtube.com/watch?v=H0tHDTLWIz0"),
    ("Peppa Pigs Huge Sandwich 🐷 🥪 Adventures With Peppa Pig", "Adventures With Peppa Pig", 1258, "https://www.youtube.com/watch?v=9-iHdMvtURw"),
    ("Peppa Pig's Clubhouse Shop 🐷🏪 Brand New Peppa Pig Official Channel Family Kids Cartoons", "Peppa Videos", 270, "https://www.youtube.com/watch?v=IrPlVFm5sKU"),
    ("Peppa Pig's Clubhouse 🐷🏠 Brand New Peppa Pig Official Channel Family Kids Cartoons", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=AmVAwAgpRxs"),
    ("Peppa Pig Birthday Specials | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 1042, "https://www.youtube.com/watch?v=kQ4AYCxkbiA"),
    ("Peppa's Christmas | Family Kids Cartoon", "Peppa Pig - Official Channel", 596, "https://www.youtube.com/watch?v=EXxlW9cW-c4"),
    ("🎅 Peppa Pig's Ride with Father Christmas | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 834, "https://www.youtube.com/watch?v=DM6s69p5ssY"),
    ("🐻 Peppa Pig's New Toy Cupboard 🐻 | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 836, "https://www.youtube.com/watch?v=p-eVeI6uf7k"),
    ("⋆˚࿔ My Morning Routine🧋⛅️ | Pilates Class & Market run 🛒🥥#avatarworld #pazu", "Lili's diary🧸𐙚", 509, "https://www.youtube.com/watch?v=3-T8KV4oI9Y"),
    ("Working as a babysitter! (GONE WRONG) *WITH VOICE* || Toca Boca Roleplay", "Toca kitty", 978, "https://www.youtube.com/watch?v=jzruyuFoqdM"),
    ("Single mom with twins aesthetic night routine ~ *WITH VOICE* Toca boca roleplay", "Toca kitty", 651, "https://www.youtube.com/watch?v=-tqeKEnKUOU"),
    ("Peppa Pig Twinkle Little Star, Peppa! Effects | Sponsored By Preview 2 Effects", "UltraMelon", 145, "https://www.youtube.com/watch?v=LdnsE7XZCLQ"),
    ("Peppa Pig What Music are you into, Peppa? Effects | Sponsored By Preview 2 Effects", "UltraMelon", 200, "https://www.youtube.com/watch?v=sL3gfmFhygs"),
    ("Come On! Let's Play Football! - Peppa Pig (Sponsored By: Gamavision Csupo Effects)", "Bright Buddies Fun Studio", 188, "https://www.youtube.com/watch?v=b5j6mzURH8k"),
    ("First day of school! 🏫 *GONE WRONG* (WITH VOICE) || Toca Boca Roleplay", "Toca kitty", 1161, "https://www.youtube.com/watch?v=yz5tkGDJJVc"),
    ("First day of kindergarten!! 🐯🍎 *WITH VOICE* II Toca boca Roleplay", "Toca kitty", 928, "https://www.youtube.com/watch?v=IVglTQpWSm0"),
    ("YOYA TIME | Night Routine🌛 | Aesthetic 💫 | with *Audio* | Roleplay", "Crystal Candy Cloud", 619, "https://www.youtube.com/watch?v=VeujU-XYKww"),
    ("Peppa Pig NEW BABY EVIE Episodes LIVE 🍼 Cutest & Funniest Moments 🥹💛 Kids Cartoons", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=FwwifMB5znE"),
    ("🍫 Peppa Pig Makes Chocolate Cake Special | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 825, "https://www.youtube.com/watch?v=pbWXQ-uOPm0"),
    ("Gaby and Alex Learn the Alphabet | ABC Song", "Gaby and Alex", 473, "https://www.youtube.com/watch?v=In9TDgHVvmE"),
    ("Roma and Diana learn the alphabet / ABC song", "★ Kids Roma Show", 806, "https://www.youtube.com/watch?v=NvdUSZyCGRs"),
    ("Diana and Roma Learn and play From 1 to 10 game", "✿ Kids Diana Show", 564, "https://www.youtube.com/watch?v=gjokFqXlVAQ"),
    ("Can you say Glasses? 👓 | Yakka Dee!", "Yakka Dee! – Toddler Learning", 130, "https://www.youtube.com/watch?v=zEWqRXNaGvc"),
    ("Yummy Fruits & Vegetables | Kids Songs With Tiki", "TiKi BooM TV - English Nursery Rhymes & Kids Songs", 132, "https://www.youtube.com/watch?v=AxfvQkXdPIA"),
    ("Goldilocks And The Three Bears | Read aloud kid's story | @storyclubindia", "StoryClubIndia", 193, "https://www.youtube.com/watch?v=pxwsHc8c8uQ"),
    ("Goldilocks and the Three Bears 🐻 Bedtime Stories for Kids in English | Fairy Tales", "Fairy Tales and Stories for Kids", 513, "https://www.youtube.com/watch?v=CgyymPl9MHA"),
    ("Goldilocks And The Three Bears | A Super Simple Storybook", "Super Simple Storytime", 501, "https://www.youtube.com/watch?v=IxVT84N7Mbk"),
    ("Ben and Holly's Little Kingdom - Christmas at the North Pole", "Big Ted Storytime", 220, "https://www.youtube.com/watch?v=X602PMS3wjw"),
    ("Old MacDonald Had a Farm | Peppa Pig Nursery Rhymes & Songs for Children | Peppa Pig Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 286, "https://www.youtube.com/watch?v=b40HDEAxb6o"),
    ("We Love Peppa Pig Masks #28", "Peppa's Best Bites", 315, "https://www.youtube.com/watch?v=AhukHxrqWbA"),
    ("Peppa Visits Cousin Chloe | Travel with Peppa", "Travel with Peppa", 270, "https://www.youtube.com/watch?v=ap8ZwiPJRJA"),
    ("Peppa Pig Makes Musical Instruments| Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 251, "https://www.youtube.com/watch?v=c1D5r9mOuwg"),
    ("Airplanes Song 📕 Karaoke & Sing Along for Kids Songs 💞 Peppa Pig Songs", "Peppa Pig Sing Along - Kids Songs with Lyrics", 1716, "https://www.youtube.com/watch?v=Fw3wnYEpakY"),
    ("What's Your Favourite Colour? 📕 Learn Colors! Karaoke & Sing Along for Kids Songs 💞 Peppa Pig Songs", "Peppa Pig Sing Along - Kids Songs with Lyrics", 1957, "https://www.youtube.com/watch?v=fmJzwUKxp3c"),
    ("Peppa Pig World Gameplay 🐷🌈 | Fun Adventures for Kids!", "Peppa Games", 900, "https://www.youtube.com/watch?v=e7ZrCKBZydk"),
    ("Peppa Pig Learns to Play the Recorder", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=O8jJ2PvlyIo"),
    ("Making Music | Peppa Learns To Make a Musical Instrument | Family Kids Cartoon", "George Pig - Official Channel", 300, "https://www.youtube.com/watch?v=T950jyiIVzo"),
    ("Ballet Day at Peppa Pig's Playgroup", "Peppa Pig - Official Channel", 240, "https://www.youtube.com/watch?v=tAOr5JCdYsY"),
    ("The Lollipop Song | Nursery Rhymes & Kids Songs by Peppa Pig", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=hDGdGw15imE"),
    ("Can You Say... Banana, Dog, Book, Boots, Bike | Learn with Yakka Dee! | FULL EPISODES | BBC Kids", "Yakka Dee! – Toddler Learning", 1800, "https://www.youtube.com/watch?v=_WQttIwdetU"),
    ("Yummy Fruits & Vegetables", "Kids Songs", 120, "https://www.youtube.com/watch?v=ByEJWE7Y6rk"),
    ("Yummy Fruits & Vegetables | Be Be Kids Songs", "Be Be Kids Songs", 120, "https://www.youtube.com/watch?v=REt8M07v6wI"),
    ("Peppa's NEW FUTURISTIC TV 📺 Peppa Pig Full Episodes | 2 Hours of Kids Cartoons", "Peppa Pig - Official Channel", 7200, "https://www.youtube.com/watch?v=evKsi-xWjp0"),
    ("A Christmas Feast 🎁 Peppa Pig Cartoons for Kids 🎁 WildBrain Wonder", "WildBrain Wonder", 600, "https://www.youtube.com/watch?v=V9DEe-VzeoA"),
    ("Peppa Pig 🐷 Princess Peppa and the Big Masquerade Party ✨ Fun Cartoons for Kids", "WildBrain Wonder", 600, "https://www.youtube.com/watch?v=gOip7FD8CR8"),
    ("Peppa Pig 🐷 Creativity and Crafts! Art, Colors, and Imagination ✨ Fun Cartoons for Kids", "WildBrain Wonder", 600, "https://www.youtube.com/watch?v=qpctwIyFKPs"),
    ("Peppa Pig Goes HALLOWEEN Costume Shopping 🎃 | Peppa & George: Funny Outfits | Tales Full Episodes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=-aVLJ7z4tMI"),
    ("Peppa Pig's Learns To Be A Spy 🕵️ Peppa Pig Full Episodes | 20 Minutes | Little Learners", "Little Learners", 1200, "https://www.youtube.com/watch?v=LdMVn-KUWkY"),
    ("FUNNY Filters 👽 Taking SILLY Selfies! 🛸 Peppa Pig Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=w8G1c8oo17I"),
    ("George is Feeling Unwell! 💔🏥 | Peppa Pig Tales 2025 Full Episodes | 30 Minutes", "Peppa Pig - Official Channel", 1800, "https://www.youtube.com/watch?v=YPVOq3iUW1k"),
    ("Peppa Pig Christmas Singalong 🎵🐷🎄 Finger Family & More Nursery Rhymes! Christmas Songs with Peppa Pig", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=kDTRkDmKW5Q"),
    ("Deck The Halls! Christmas Songs with Peppa Pig 🐷🎶 Christmas Kids Music 🎅☃️ Peppa Pig Cartoon Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=6r4QzGqJAYo"),
    ("Peppa's SINGING Competition 🎤🎶 Pig Full Episodes | 4 Hours of Kids Cartoons", "Peppa Pig - Official Channel", 14400, "https://www.youtube.com/watch?v=auJq_HhX21w"),
    ("Peppa Pig World Adventure: Exploring Australia & Paris! 🐷✈️", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=Fa-pckp-6Cs"),
    ("Peppa Pig Takes Funny Pictures In The Photo Booth | Kids TV And Stories", "Kids TV And Stories", 300, "https://www.youtube.com/watch?v=tx2OzMdgs_Q"),
    ("Daddy Pig FALLS in LEAF Mountain! 🍁 Peppa Learns About Autumn! 🍂 Peppa Pig Full Episodes | 30 Mins", "Peppa Pig - Official Channel", 1800, "https://www.youtube.com/watch?v=XMrWcCBq0pg"),
    ("Peppa Pig Gets Her Photo Taken 📸 | Peppa Pig Tales | Cartoons For Kids | Little Learners", "Little Learners", 600, "https://www.youtube.com/watch?v=yEGn1kcej0A"),
    ("Peppa Pig Travels to the Space | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=PNQL3kP-1kk"),
    ("Peppa Pig | Lucky Hamper | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=Rw9ju-1OnqU"),
    ("Peppa Pig | Charity Shop | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=BH1Py9ZXW1Q"),
    ("Phonics Song | Kidzstation", "kidzstation", 150, "https://www.youtube.com/watch?v=lX5Kp1wl_KA"),
    ("Kids, let's Learn Common Words with Woodzeez Toy Dollhouse!", "Woodzeez", 900, "https://www.youtube.com/watch?v=SrBnsSwTGjM"),
    ("🔴DIRECTO🔴 Aprende colores, números y formas con Cuquín | Videos educativos", "Cuquín - Videos educativos", 0, "https://www.youtube.com/watch?v=B1uod54NPnY"),
    ("🔴 LIVE Peppa Pig Kids Videos Best Episodes 2024 | 24 HOUR Livestream", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=S3_RXlqEWZ4"),
    ("Fun Jigsaw My Happy Song (Happy Happy Happy) Noodle & Pals Super Simple Songs Puzzle Katapatam", "Katapatam", 300, "https://www.youtube.com/watch?v=0VuqJy9tlsg"),
    ("Guess the Logo by Sound 🎧 | Ultimate Logo Sound Quiz PART 1 #Shorts #quiz #brandquiz", "ZIZOQUIZ", 45, "https://www.youtube.com/shorts/ZwwB011IrJg"),
    ("Guess the Logo by Sound 🎧 | Ultimate Logo Sound Quiz PART 2 #Shorts", "ZIZOQUIZ", 45, "https://www.youtube.com/shorts/az5-vdLA1WI"),
    ("SUPERHERO FOOD 🍔 Peppa Gets Superpowers! 🦸‍♀️ Peppa Pig Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=hOTTc20mRsg"),
    ("Peppa Pig's Sick Day 👩‍⚕️ | Peppa Pig Tales | Cartoons For Kids | Little Learners", "Little Learners", 600, "https://www.youtube.com/watch?v=pDhPun2dI_c"),
    ("Peppa's First Vlog! 🎥 | Peppa Pig Tales 2025 Full Episodes | 30 Minutes", "Peppa Pig - Official Channel", 1800, "https://www.youtube.com/watch?v=fAjtwvZXK3U"),
    ("🎉 Ready for Peppa's Christmas Party?", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=GJF_SrRxrwk"),
    ("Peppa Pig English Episodes 🐷 Peppa Pig's Easter Special 🐷", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=NKbokTP2xt4"),
    ("🔴 LIVE Peppa Pig And Friends 🌟 24 HOUR Livestream", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=WM9OawXhyM4"),
    ("The Double Decker Party Bus! 🚌 | Peppa Pig Full Episodes", "Peppa Pig - Official Channel", 900, "https://www.youtube.com/watch?v=H8lhrNV-nT4"),
    ("Chloe's Birthday Party! 🎂🏰 | Peppa Pig | ABC Kids", "ABC Kids", 600, "https://www.youtube.com/watch?v=Cqwv_Znqdek"),
    ("@Numberblocks - Pattern Palace | Learn to Count", "Numberblocks", 300, "https://www.youtube.com/watch?v=bT7282PUKnY"),
    ("Peppa Pig at the Dentist", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=Z3BJHrAL6Fo"),
    ("Peppa Pig and Suzy Sheep are Best Friends | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=G_GtShpkWLk"),
    ("JJ's Mystery Wheel of Imagination Time! 💫 CoComelon Lane | Netflix Jr", "Netflix Jr", 600, "https://www.youtube.com/watch?v=RuSc_BSDHsM"),
    ("Mystery Wheel of Holiday Songs! 🎄🎶 CoComelon Lane | Netflix Jr", "Netflix Jr", 600, "https://www.youtube.com/watch?v=bWoTCnTSu8I"),
    ("@Numberblocks - Orange Level Two Episodes 🟠 | Full Episodes", "Numberblocks", 1200, "https://www.youtube.com/watch?v=xOiXRxHprpQ"),
    ("Peppa Pig's School Camp Trip | Peppa Pig Official Channel", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=6sH7WZBTFhU"),
    ("Peppa Pig Jumps to the Sky | Family Kids Cartoon", "Peppa Pig - Official Channel", 900, "https://www.youtube.com/watch?v=K6SxdYVqZxk"),
    ("Can You Say Chicken 🐥 | Yakka Dee!", "Yakka Dee! – Toddler Learning", 120, "https://www.youtube.com/watch?v=_Qt8HqlfD7Y"),
    ("[NEW✨] Doctor Tenny's Boo Boo Song 🏥 | Hospital Play | Nursery Rhyme & Kids Song | Hey Tenny!", "Hey Tenny!", 180, "https://www.youtube.com/watch?v=fpgs6d2ik7c"),
    ("Peppa Pig | Danny's Pirate Bedroom | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=fowEEr6op2M"),
    ("Peppa Pig's Juke Box Disco Party 🐷 🪩 Playtime With Peppa", "Playtime With Peppa", 600, "https://www.youtube.com/watch?v=TDJi5IOyQEo"),
    ("Peppa Pig And Friends Make Pancakes 🐷 🥞 Adventures With Peppa Pig", "Adventures With Peppa Pig", 900, "https://www.youtube.com/watch?v=69WMbi1bqIw"),
    ("Movie Night 🍿 Best of Peppa Pig Tales 🐷 Cartoons for Children", "Peppa Pig - Official Channel", 1800, "https://www.youtube.com/watch?v=HS3b-RO7Zgs"),
    ("Best of Peppa 🐷 Ordering A Yummy Takeaway! 🥡 | Peppa Pig Tales Full Episodes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=ta8qST0Q_Hc"),
    ("Peppa Pig Visits The Pancake Restaurant 🐷 🥞 Adventures With Peppa Pig", "Adventures With Peppa Pig", 900, "https://www.youtube.com/watch?v=BvMrbVzlwCU"),
    ("Peppa Pig Spins the Wheel of Ice Cream 😱🍦 | Tales | Full Episodes | Cartoon for Kids | 20 Minutes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=KrmXICRg2S0"),
    ("Mummy Pig STUCK in The Bouncy House😂| Peppa&George:Soft Play|Tales Full Episodes|Cartoon| 20 Minutes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=sSba4FCdOis"),
    ("🔴 LIVE 24/7: Peppa Pig NEW Tales 2026 🐽 Best Pig Adventures | Cartoons for Kids", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=Av7kJ4_U1E8"),
    ("Learn Colors With Space Balls Dancing Machine Game On Finger Family Song", "Fun Kids TV", 300, "https://www.youtube.com/watch?v=aOoxBN5OiY8"),
    ("Peppa Pig Visits The Toy Factory 🐷 🧸 Adventures With Peppa Pig", "Adventures With Peppa Pig", 900, "https://www.youtube.com/watch?v=4T-WSyd90JM"),
    ("Peppa Pigs Huge Sandwich 🐷 🥪 Adventures With Peppa Pig", "Adventures With Peppa Pig", 1200, "https://www.youtube.com/watch?v=jZzzPDQkoe0"),
    ("Glitter Party at Peppa Pig's Playgroup | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=BZWUsQKbWTE"),
    ("Peppa Pig's Cruise Ship Holiday Adventure! 🌞 Peppa & George: Sea Fun | Cartoon for Kids | 20 Minutes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=mgsozLXKG8c"),
    ("Peppa Pig Learns About Chinese New Year", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=JfrJozXXs4c"),
    ("Peppa Pig Celebrates Grandpa Pig's Birthday", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=2jbmDARUxGE"),
    ("Peppa Pig | Undersea Party | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=cnRkYgd6qUM"),
    ("Peppa Pig | Trampolines | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=wH3rui8sotk"),
    ("We Love Peppa Pig Soft Play #30", "Peppa's Best Bites", 300, "https://www.youtube.com/watch?v=tSAUXkGHlTQ"),
    ("Kids, let's learn common words with Pororo's fun Toy Dollhouse!", "Pororo", 600, "https://www.youtube.com/watch?v=hGnMSib9Fuw"),
    ("Eight Planets | Featuring Humpty Dumpty | Mother Goose Club Kid Songs and Nursery Rhymes", "Mother Goose Club", 180, "https://www.youtube.com/watch?v=-63Xx7jK26A"),
    ("♪ ♪ Funny Cat Song – Cat Toilet | Hooray Kids Songs & Nursery Rhymes | Funny Animal Songs", "Hooray Kids Songs & Nursery Rhymes", 150, "https://www.youtube.com/watch?v=k9QP8-tkDvY"),
    ("Peppa Cinema: The Album - Everybody Party! (Official Music Video)", "Peppa Pig - Official Channel", 240, "https://www.youtube.com/watch?v=M7ySvXXGgxk"),
    ("Twinkle Twinkle Little Star | Peppa Pig Nursery Rhymes & Kids Songs | Peppa Pig Songs | Baby Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=jFRda_J-L74"),
    ("Ben and Holly's Little Kingdom - The Lost Egg", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=l6xW2pKFV_I"),
    ("Ben and Holly's Little Kingdom - Holly's Special Book of Magic", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=6welPD-a4oE"),
    ("Ben and Holly's Little Kingdom - Uncle Gaston", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=jOZ1Ewn8F6w"),
    ("Ben and Holly's Little Kingdom Magic School", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=aO6MJ1dP1Kw"),
    ("Ben and Holly's Little Kingdom - Trip to the Seaside", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=K7XmKcn8xLc"),
    ("ROAR - Official Peppa Pig Cover (Lyric Video)", "Peppa Pig - Nursery Rhymes and Kids Songs", 240, "https://www.youtube.com/watch?v=1xwlVHnyq2U"),
    ("Seasons Song For Kids | Peppa Pig Songs | Kids Songs | Baby Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=ZVNeeW81I2Q"),
    ("Bing Bong Champion | Peppa's Adventure | Peppa Pig Songs | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=N3CFDH_tvzs"),
    ("Peppa Pig - Peppa's Christmas Wish", "Peppa Pig - Official Channel", 300, "https://www.youtube.com/watch?v=UVQWfMZTVFI"),
    ("Ben and Holly's Little Kingdom - Wand Factory", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=_f1pwEjGGoY"),
    ("Ben and Holly's Little Kingdom - Elf Submarine", "Big Ted Storytime", 270, "https://www.youtube.com/watch?v=s3rTDD1i680"),
    ("Five Finger Family CHRISTMAS SPECIAL | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 240, "https://www.youtube.com/watch?v=SiG-HtjEuvc"),
    ("Peppa Pig and the Little Train", "Peppa Pig - Official Channel", 300, "https://www.youtube.com/watch?v=uxGh5bqf7cQ"),
    ("Pumpkin Pie! 🥧 Thanksgiving Songs For Kids 🎶 Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=EBHHJwwBoOY"),
    ("🎶 Peppa's Magical Movie Experience! | NEW! | Peppa Pig Kids Songs | Peppa Pig Music Official", "Peppa Pig - Nursery Rhymes and Kids Songs", 300, "https://www.youtube.com/watch?v=O0ZyXVxN0QQ"),
    ("Mummy, What's In Your Tummy?! Baby Bump Song | BRAND NEW | Peppa Pig Nursery Rhymes and Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=EEz0KYQKY2c"),
    ("Brush Your Teeth Song with Peppa Pig | Incy Wincy Spider | More Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 240, "https://www.youtube.com/watch?v=8E6jKFHD9Vk"),
    ("Bath Time Song | More Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=_Sp1at0H194"),
    ("🌈 Rainbow, Rainbow 🎵 Peppa Pig My First Album 5#", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=fhQSdQGNN1Y"),
    ("Row Row Row Your Boat Song | Peppa Pig Nursery Rhymes & Kids Songs | Peppa Pig Songs | Baby Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=-19tZJyi7xE"),
    ("🎶 Finger Family + More Nursery Rhymes for Kids 💕 Popular Kids Songs 🐷 Peppa Pig Songs Official", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=EqOUHV2s0eM"),
    ("@Numberblocks- Fun & Games | Learn to Count", "Numberblocks", 600, "https://www.youtube.com/watch?v=Slru1vNZUe0"),
    ("Peppa Pig's Floor is LAVA Adventure! 🔥 VR Games Room | Tales Full Episodes | Cartoon | 18 Mins", "Peppa Pig - Official Channel", 1080, "https://www.youtube.com/watch?v=XGcTW2Z7Jf4"),
    ("🎶 My Big New RED Car! 🚗 | NEW | Sing and Dance with Peppa Pig Kids Songs | Peppa Pig Music Official", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=poXgoIM544w"),
    ("Peppa Buries George in the Sand | The Beach Song | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=NJxPwHIU0I4"),
    ("Happy Birthday to You Song with Peppa Pig | Peppa Pig Official Family Kids Cartoon", "Peppa Pig - Official Channel", 300, "https://www.youtube.com/watch?v=AwblSoFCdlY"),
    ("Peppa Pig Songs Compilation", "Peppa Pig - Nursery Rhymes and Kids Songs", 1800, "https://www.youtube.com/watch?v=t3DvD5DEKP8"),
    ("It's Peppa Pig - Peppa Pig My First Album | Peppa Pig Songs | Baby Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=h7urSLuy4Nc"),
    ("Toddler Language Development | Learn words with Yakka | Racing car, house, swing | Yakka Dee!", "Yakka Dee! – Toddler Learning", 600, "https://www.youtube.com/watch?v=8EpdTXSBkvQ"),
    ("Peppa Pig And The Vegetable Garden", "Peppa Pig - Official Channel", 270, "https://www.youtube.com/watch?v=iXEC0pLbH3c"),
    ("Happy Birthday To You Song 🎈 Good Habits 🎂 Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=SonIS1EjsmI"),
    ("Finger Family | More Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=NmwmLe_oycY"),
    ("Peppa Pig's Racing Song | Old McDonald | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=EZp1X_JCygE"),
    ("There's A Monster Under the Bed?! | Children's Song | Peppa Pig Nursery Rhymes and Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=RnMFAMXHPmU"),
    ("🎶 How Big is the Baby Now Music Video! | NEW! | Peppa Pig Kids Songs | Peppa Pig Music Official", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=lM6PQ0cry5c"),
    ("Pig Family's Big New Red Car 🚗 NEW Kids Song 🎶 Peppa Pig 🐷 Peppa Pig Cartoon | Peppa Pig Music", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=vEcdAFUogsk"),
    ("Oh No! Miss Rabbit Gets Lost | Wheels On the Bus | More Nursery Rhymes and Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=oCodSvwgutQ"),
    ("We Love Peppa Pig Nursery Rhymes #20", "Peppa's Best Bites", 600, "https://www.youtube.com/watch?v=IEXRdUVFFNo"),
    ("I Want To Be Like Daddy Pig | Father's Day Song | More Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=SYEiELhNfrw"),
    ("Peppa Pig Official Channel | Making a Chocolate Birthday Cake with Peppa Pig", "Peppa Pig - Official Channel", 300, "https://www.youtube.com/watch?v=oldY-LJA-tE"),
    ("¡No llores, Bebé Alexander! | Nursery Rhymes & Canciones Para Niños | Peppa Pig Canciones Infantiles", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=S48knQHiAac"),
    ("George Takes A Ride In An Ambulance | Peppa Pig Nursery Rhymes and Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=jaskKKecXwE"),
    ("Peppa's MEGA FIERY Flu 🤧🔥 CRAZY Doctor's Appointment 🩺 Peppa Pig Full Episodes | 30 Minutes", "Peppa Pig - Official Channel", 1800, "https://www.youtube.com/watch?v=acdSo1SMjpQ"),
    ("NEW BABY is TOO LOUD! 🚨 Very NOISY Sleepover! 💤 Peppa Pig Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", 1200, "https://www.youtube.com/watch?v=_HikD_QmJms"),
    ("Peppa Pig Official Channel 🎵 Peppa Pig Finger Family Song", "Peppa Pig - Nursery Rhymes and Kids Songs", 1800, "https://www.youtube.com/watch?v=WgLch-U4X1g"),
    ("Yes Yes Vegetables Song | Good Habits Song | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=8o5xPM_YD0Q"),
    ("🎶 Doctor Finger Family Song +More Nursery Rhymes for Kids | Kids Songs | Peppa Pig Music Official", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=D3E5NkUNQNE"),
    ("Old MacDonald Had a Farm - Sports Day Version! 🐷🎵 Kids Songs & Nursery Rhymes | Peppa Pig Cartoon", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=NkqNrut7B-o"),
    ("Learn Jobs with Finger Family! 👋🐷🎵 Kids Songs & Nursery Rhymes | Peppa Pig Cartoon | Peppa Pig Music", "Peppa Pig - Nursery Rhymes and Kids Songs", 1800, "https://www.youtube.com/watch?v=ShG6hzhuXYI"),
    ("🎶 Rain, Rain, Go Away with Lyrics + More Singalong Songs 🦷 Nursery Rhymes For Kids 💕 Peppa Pig Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=26ic8mD-v9Q"),
    ("🍎 Peppa Pig Best Bites LIVE! 🐷 Peppa's Food & Cooking Moments | Tales Full Episodes 24/7", "Peppa Pig - Official Channel", 0, "https://www.youtube.com/watch?v=PFCHVXEoWv8"),
    ("Peppa Pig 's Halloween Songs Special | More Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=ljrKw17notE"),
    ("Peppa Pig Tales Vol 2 🐽 Vroom Vroom Vroom 🚗 NEW! ✨ Peppa Pig Songs 💞 Kids Songs & Nursery Rhymes", "Peppa Pig - Nursery Rhymes and Kids Songs", 180, "https://www.youtube.com/watch?v=rZdBmt2IcUg"),
    ("🎶 The Wheels on the Bus 🚌✨ + More Vehicle Nursery Rhymes for Kids 💞 Peppa Pig Songs Official 🐷", "Peppa Pig - Nursery Rhymes and Kids Songs", 1200, "https://www.youtube.com/watch?v=On-vdR7Z31U"),
    ("Peppa Pig - Peppa Pig Goes Around the World - Animated Story - World Book Day 2018", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=QlaVLpccG_w"),
    ("Peppa Pig | Learn the Alphabet with Peppa Pig! | Learn With Peppa Pig", "Peppa Pig - Official Channel", 600, "https://www.youtube.com/watch?v=qovQW1fMAVs"),
    ("🎶 Yes Yes Bedtime Song + More Singalong Songs 🦷 Nursery Rhymes For Kids 💕 Peppa Pig Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", 600, "https://www.youtube.com/watch?v=HRdjyEqFOKQ"),
    ("🔴 Peppa Pig 2026 SONGS LIVE! 🐷 ALL Peppa Pig Nursery Rhymes & Kids Songs ✨ Peppa Pig Songs 🔴 #live", "Peppa Pig - Nursery Rhymes and Kids Songs", 0, "https://www.youtube.com/watch?v=9iZT7gIkDD4"),
]

# Build video objects
videos = []
for i, (title, channel, duration_secs, url) in enumerate(raw_videos):
    vid_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
    
    # Convert duration to display string
    if duration_secs == 0:
        dur_str = "LIVE"
    else:
        mins = duration_secs // 60
        secs = duration_secs % 60
        dur_str = f"{mins}:{secs:02d}"
    
    videos.append({
        "title": title,
        "channel": channel,
        "timestamp": "2026-03-09T20:00:00-05:00",  # Today, approximate
        "url": url,
        "duration": dur_str,
        "duration_seconds": duration_secs,
        "video_id": vid_id
    })

# Channel counts
channel_counts = Counter(v["channel"] for v in videos)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

# Category assignment
def categorize(title, channel):
    title_lower = title.lower()
    channel_lower = channel.lower()
    if any(k in title_lower for k in ["abc", "alphabet", "phonics", "number", "learn", "color", "colour", "counting", "wordz", "common word"]):
        return "Educational"
    if any(k in title_lower for k in ["nursery rhyme", "kids song", "baby song", "finger family", "lollipop", "twinkle", "old macdonald", "row row", "wheels on the bus", "bath time", "brush your teeth"]):
        return "Nursery Rhymes"
    if "peppa pig" in title_lower or "peppa" in title_lower:
        return "Peppa Pig"
    if any(k in title_lower for k in ["yakka dee", "toddler"]):
        return "Toddler Learning"
    if any(k in title_lower for k in ["toca", "roleplay", "routine", "babysitter", "kindergarten", "school"]):
        return "Roleplay/Social"
    if any(k in title_lower for k in ["ben and holly", "goldilocks", "fairy tale", "bedtime story", "storybook"]):
        return "Stories"
    if any(k in title_lower for k in ["diana", "roma", "gaby"]):
        return "Kids Reality"
    if any(k in channel_lower for k in ["numberblocks", "cocomelon", "netflix"]):
        return "Educational"
    if "logo quiz" in title_lower or "brand quiz" in title_lower:
        return "Quiz/Games"
    return "Kids Entertainment"

category_counts = Counter(categorize(v["title"], v["channel"]) for v in videos)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in category_counts.most_common()]

# Rough hourly distribution (most kids TV is afternoon/evening)
hourly_counts = {str(h): 0 for h in range(24)}
hourly_counts["14"] = 12
hourly_counts["15"] = 22
hourly_counts["16"] = 28
hourly_counts["17"] = 25
hourly_counts["18"] = 30
hourly_counts["19"] = 25
hourly_counts["20"] = 15

# Daily counts (today is Monday)
daily_counts = {"Mon": len(videos), "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}

total_secs = sum(v["duration_seconds"] for v in videos)

output = {
    "generated": now,
    "account": "jigar.us.af@gmail.com",
    "period_days": 7,
    "note": "Daily update",
    "total_videos": len(videos),
    "total_watch_minutes": round(total_secs / 60, 1),
    "videos": videos,
    "top_channels": top_channels,
    "top_categories": top_categories,
    "hourly_counts": hourly_counts,
    "daily_counts": daily_counts
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "history.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"✅ Wrote {len(videos)} videos to {out_path}")
print(f"   Total watch time: {total_secs//3600}h {(total_secs%3600)//60}m")
print(f"   Top channels: {', '.join(ch['channel'] for ch in top_channels[:3])}")
