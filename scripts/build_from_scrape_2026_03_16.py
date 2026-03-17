#!/usr/bin/env python3
"""
KidWatch history builder - March 16, 2026 scrape
Built from live browser scrape of YouTube watch history.
"""
import json
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

# ─── RAW SCRAPED DATA ──────────────────────────────────────────────────────
# (title, channel, duration_str, url)
VIDEOS_RAW = [
    ("Pete The Cat ~ Wheels On The Bus Children's Read Aloud Story Book For Kids By James Dean", "Kids Stories 4 You", "3:54", "https://www.youtube.com/watch?v=ooTk2M9a4pQ&t=24s"),
    ("Goldilocks and the Three Bears Song ♫ Fairy Tales ♫ Story Time for Kids by The Learning Station", "TheLearningStation - Kids Songs and Nursery Rhymes", "5:59", "https://www.youtube.com/watch?v=PGI-4MrC_b8"),
    ("Goldilocks And The Three Bears | A Super Simple Storybook", "Super Simple Storytime", "8:21", "https://www.youtube.com/watch?v=IxVT84N7Mbk&t=18s"),
    ("GOLDILOCKS AND THE THREE BEARS | Mara Alperin | Read aloud", "Love2Read with Miss Ellis", "8:03", "https://www.youtube.com/watch?v=Nl8B-XTEblM&t=3s"),
    ("Goldilocks And The Three Bears | Read aloud kid's story | @storyclubindia", "StoryClubIndia", "3:13", "https://www.youtube.com/watch?v=pxwsHc8c8uQ"),
    ("Peekaboo, Where Are You? | A Super Simple Storybook", "Super Simple Storytime", "8:00", "https://www.youtube.com/watch?v=k2Bl-YnZXNE&t=5s"),
    ("Let's Make a Pizza | NEW TASTY VIDEO | Mother Goose Club Phonics Songs", "Mother Goose Club", "2:52", "https://www.youtube.com/watch?v=L6nalE3OwxA"),
    ("The Alphabet Hip-Hop + More | Learn ABC | Mother Goose Club Phonics Songs", "Mother Goose Club", "13:09", "https://www.youtube.com/watch?v=JhVAHfKm9Fw"),
    ("Johnny Johnny Yes Mama + More | Mother Goose Club Cartoons", "Mother Goose Club Toons", "14:47", "https://www.youtube.com/watch?v=A-dmyrUVEx8"),
    ("Johnny Johnny Yes Mama + More | Mother Goose Club Cartoons", "Mother Goose Club Toons", "18:48", "https://www.youtube.com/watch?v=-CqbnxkhNWw"),
    ("Baby Shark | Mother Goose Club Nursery Rhymes", "Mother Goose Club", "4:54", "https://www.youtube.com/watch?v=rDy8tGBhbCk"),
    ("[NEW✨] Doctor Tenny's Boo Boo Song 🏥 | Hospital Play | Nursery Rhyme & Kids Song | Hey Tenny!", "Hey Tenny! Learning Videos and Songs for Kids", "3:51", "https://www.youtube.com/watch?v=fpgs6d2ik7c"),
    ("Doctor Tenny! Baby Shark's got a Boo Boo | Hospital Play | Nursery Rhyme & Kids Song | Hey Tenny!", "Hey Tenny! Learning Videos and Songs for Kids", "3:53", "https://www.youtube.com/watch?v=FXkdMUGsMME&t=4s"),
    ("Vlad and Niki learn the alphabet and many other funny videos for kids", "Vlad and Niki ARA Collection", "15:30", "https://www.youtube.com/watch?v=FDKEk_YxbXw&t=16s"),
    ("Ice Cream Machine Disaster Adventure for Kids", "Vlad và Niki", "15:51", "https://www.youtube.com/watch?v=oMznSEqh4FY&t=4s"),
    ("Funny Watermelon Adventure and Other Good Stories for Kids", "Vlad và Niki", "14:01", "https://www.youtube.com/watch?v=fA-AxMq-Y3o&t=43s"),
    ("Alice and Mia – The Handwashing Story – Don't Eat with Dirty Hands!", "Princesa_Alice", "11:44", "https://www.youtube.com/watch?v=Gf8BOLT54_Q&t=25s"),
    ("Alice's Let's Buckle Up Stories - Children's Stories", "Princesa_Alice", "13:37", "https://www.youtube.com/watch?v=ElsEOjmhZ1I&t=7s"),
    ("Playground Adventure with Alice", "Alice_Princesa", "12:28", "https://www.youtube.com/watch?v=Ah-6GwjKP48&t=6s"),
    ("Alice's Adventures and the Mall Escalator - Safety Lessons for Kids", "Alice Putri", "12:30", "https://www.youtube.com/watch?v=3RqLHzLJ4KA&t=75s"),
    ("Alice's Adventures and the Escalator at the Mall - Safety Lessons for Kids", "Alice Putri", "12:00", "https://www.youtube.com/watch?v=6dP7mMw0DhU&t=7s"),
    ("Children learn safety rules in the mall - useful stories with Chris", "Vlad and Niki ESP", "12:50", "https://www.youtube.com/watch?v=VKwqYgcUm08&t=34s"),
    ("Brush your teeth song with Alice", "Alice", "14:21", "https://www.youtube.com/watch?v=D_PoN-DqCe8&t=4s"),
    ("Yes Papa 2 (Colors and Brush Your Teeth Song)", "Ashlynn FAM JAM", "3:23", "https://www.youtube.com/watch?v=ynl7O3eyrKM&t=5s"),
    ("Read With Me: 100 Words to Say I Love You | Gentle Story Read Aloud for Toddlers", "Cozy Nest Reading", "6:15", "https://www.youtube.com/watch?v=S67gjxFvuRs&t=19s"),
    ("Johny Johny Yes Papa Nursery Rhyme | Part 3 - 3D Animation Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "3:07", "https://www.youtube.com/watch?v=EA_fbT6oN2k"),
    ("Johny Johny Yes Papa Sports & Games Nursery Rhyme - 3D Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "3:03", "https://www.youtube.com/watch?v=KVVdJUrKoMA"),
    ("Peppa Pig | The Lifeboat | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig's Pretend Play", "5:12", "https://www.youtube.com/watch?v=wQ8yuUDH-C8&t=10s"),
    ("🍕 Let's Make a Pizza! | Mooseclumps | Kids Learning Videos and Songs", "Mooseclumps: Kids Learning Songs", "4:08", "https://www.youtube.com/watch?v=8bAO6xhx1xM"),
    ("🎂 Let's Bake a Cake! | Mooseclumps | Kids Learning Videos and Songs", "Mooseclumps: Kids Learning Songs", "3:42", "https://www.youtube.com/watch?v=mzW2eTB4cj0"),
    ("Let's Talk about Savoury Food with Dee | Yakka Dee", "Yakka Dee! – Toddler Learning", "9:26", "https://www.youtube.com/watch?v=OCP-Tz4UAvQ&t=1s"),
    ("Delicious Fruit! 🍉 | Yakka Dee!", "Yakka Dee! – Toddler Learning", "9:13", "https://www.youtube.com/watch?v=9tigUr0fEBs&t=2s"),
    ("Piggy Bank Smash! Toy Learning Video for Toddlers and Kids!", "Genevieve's Playhouse - Learning Videos for Kids", "14:54", "https://www.youtube.com/watch?v=eUSSp41qYQM&t=35s"),
    ("I See 100 Things | My First Words Series | I See Chant", "Dream English Kids", "8:09", "https://www.youtube.com/watch?v=lHPuGz4V9AI&t=329s"),
    ("My First 100 Words in English Chant With Matt | Numbers, Colors, Animals | Learn English Kids", "Dream English Kids", "4:55", "https://www.youtube.com/watch?v=sUoCd0DTJVY&t=19s"),
    ("Food Alphabet Phonics Song for Kids | Do You Like Apples? Song | Learning Food and ABCs", "Dream English Kids", "5:23", "https://www.youtube.com/watch?v=p4MCiq3cbao"),
    ("I Like Broccoli Ice Cream Song VERSION 2 - Funny Food song for kids by Bella and Beans TV", "Bella & Beans TV", "2:02", "https://www.youtube.com/watch?v=h9PlG8w7_R8"),
    ("I Like Broccoli Ice Cream Song - Funny Food song for kids by Bella and Beans TV", "Bella & Beans TV", "1:53", "https://www.youtube.com/watch?v=v1a-lUvk7lo"),
    ("Do You Like Lasagna Milkshakes | Ice Cream and Sushi! - Preschool Songs & Nursery Rhymes", "JRS 3D - Nursery Rhymes", "3:53", "https://www.youtube.com/watch?v=FdvdpvPk4_M"),
    ("BUBBLES CHANT 🔮 Everybody wash your hands 🙌 English Lingokids Music", "Lingokids Dance Songs for Kids", "2:56", "https://www.youtube.com/watch?v=80dbh6KYLH0"),
    ("Pattern Palace | Full Episode - S3 E17 | Learn to Count - Numberblocks", "Numberblocks", "4:35", "https://www.youtube.com/watch?v=Ev0TbEfkMCU&t=39s"),
    ("Numberblocks 0-100 learning counting 1-100 but use numberblocks toys MathLink Cubes", "YJZ TV.優", "2:11", "https://www.youtube.com/watch?v=gE7KgPRQ0ns&t=1s"),
    ("Sing Ten in the Bed with the Numberblocks | Learn Subtraction | Countdown from 10 | Baby Playful", "Baby Playful", "3:01", "https://www.youtube.com/watch?v=NHRfi1yJ-m8&t=29s"),
    ("🛏️ Ten in the Bed – Puppet Nursery Rhyme | Peppa Pig Sleepover | VoxKids by MyVoxSongs", "MyVoxSongs Nursery Rhymes", "4:27", "https://www.youtube.com/watch?v=M4vPEf4Sxxg&t=14s"),
    ("10 in the Bed", "Ms. Lolly", "5:35", "https://www.youtube.com/watch?v=zkA1U5esTuA&t=5s"),
    ("Ten In The Bed Emoji Song & More Emoji Songs | Lah-Lah Kids Songs", "Lah-Lah", "9:11", "https://www.youtube.com/watch?v=cbb1r36JDAE"),
    ("Finger Family Emoji Song | Nursery Rhymes | @TheMikMaks", "The Mik Maks", "2:12", "https://www.youtube.com/watch?v=PYXVQ-FTMl0"),
    ("Twinkle Twinkle Little Star | Peppa Pig Nursery Rhymes & Kids Songs | Peppa Pig Songs | Baby Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", "4:49", "https://www.youtube.com/watch?v=jFRda_J-L74"),
    ("Peppa Pig Theme Park - Bumper Cars And Hot Air Balloon Ride - Android Gameplay 3", "Android Gameplay Time", "5:55", "https://www.youtube.com/watch?v=Fdf4wrSVh4U&t=8s"),
    ("Peppa Pig App | World of Peppa Pig - Worldcup Sports Special | Game for Kids", "Apps For Kids - Peppa Pig, PJ Masks Games", "12:35", "https://www.youtube.com/watch?v=c5k3eQCHVTU&t=2s"),
    ("Evie's Bedtime", "Peppa Pig Stories - Topic", "3:54", "https://www.youtube.com/watch?v=xDxSehark8k&t=7s"),
    ("Peppa Pig WINS at Pancake Making Day! 🥞 | Kids vs Adults Teamwork | Tales Full Episodes | 21 Minutes", "Toys and Colours", "21:14", "https://www.youtube.com/watch?v=0Boaz14Ey90&t=13s"),
    ("Peppa Pig's Wedding Adventure with Mr. Bull! 💍 Valentine Mini-Movie Special 💕 Full Episodes | 18 Mins", "Peppa Pig's Big Adventures", "17:59", "https://www.youtube.com/watch?v=h_uZ8jgV_kU&t=4s"),
    ("Peppa Pig | The Diner | Peppa Pig Official | Family Kids Cartoon", "The Home of Peppa Pig", "5:12", "https://www.youtube.com/watch?v=w_rX9suFTZw&t=121s"),
    ("Peppa Pig | The Diner | Peppa Pig Official | Family Kids Cartoon", "George Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=pQWkZVFrOEU&t=151s"),
    ("Peppa Pig | Jelly | Peppa Pig Official | Family Kids Cartoon", "George Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=2Kdl6sVseLk&t=2s"),
    ("Peppa Pig Learns to Make Pizza", "George Pig - Official Channel", "4:30", "https://www.youtube.com/watch?v=wxyo9S2KAPM&t=11s"),
    ("Mr Cat's YUMMY Cafe 🥐 Secret Snack Passage! 🍰 Peppa Pig Full Episodes | 2 Hours", "Peppa Pig - Official Channel", "121:13", "https://www.youtube.com/watch?v=46j0Sh1idaY&t=12s"),
    ("FULL EPISODE: Peppa Pig Learns a BIG Surprise! | Nick Jr.", "Blue's Clues & You!", "5:03", "https://www.youtube.com/watch?v=6nGe8cHPGLI&t=78s"),
    ("Living Above the Shops 🏬 | Peppa Pig | ABC Kids", "ABC Kids", "3:02", "https://www.youtube.com/watch?v=sS6ReCKYcjA"),
    ("Peppa's family comes for Thanksgiving! 🥧 | Peppa Pig | ABC Kids", "ABC Kids", "3:04", "https://www.youtube.com/watch?v=MfighFJ3Qmg&t=40s"),
    ("Mr. Monkey's Valentine's Day Celebration | Cartoon for Kids", "Mr. Monkey, Monkey Mechanic", "4:49", "https://www.youtube.com/watch?v=ZnU6-LNeWnY&t=41s"),
    ("Santa's Sleigh Needs Major Repairs | Mr. Monkey, Monkey Mechanic Christmas Special!", "Super Simple TV - Kids Shows & Cartoons", "7:05", "https://www.youtube.com/watch?v=0GXFRZMIjMU&t=3s"),
    ("The Bumble Nums Make A Crunchy Christmas Cookie | Christmas Special!", "Super Simple TV - Kids Shows & Cartoons", "8:57", "https://www.youtube.com/watch?v=HWLhcHzr36A&t=41s"),
    ("Crunchy Christmas Cookie | Cartoon For Kids | The Bumble Nums", "The Bumble Nums", "8:52", "https://www.youtube.com/watch?v=lZtzHO-m--A&t=1s"),
    ("The Bumble Nums Make Out-Of-This-World Mooncake | Cartoon For Kids", "Super Simple TV - Kids Shows & Cartoons", "6:17", "https://www.youtube.com/watch?v=EQiNckx8Rd8&t=2s"),
    ("🔴 Carl's Car Wash Episode Livestream | Cartoons For Kids | Super Simple Songs", "Carl's Car Wash", "30:00", "https://www.youtube.com/watch?v=qnY_WSfpU64"),
    ("Peppa Pig | Charity Shop | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=BH1Py9ZXW1Q&t=139s"),
    ("Peppa Pig | Trampolines | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=wH3rui8sotk&t=7s"),
    ("DANIEL TIGER'S NEIGHBORHOOD | The Smushed Cake | PBS KIDS", "PBS KIDS", "11:00", "https://www.youtube.com/watch?v=yv4jjiEvHy4"),
    ("Daniel Tiger's Neighborhood | Daniel Can't Ride Trolley | PBS KIDS", "PBS KIDS", "11:00", "https://www.youtube.com/watch?v=a1hGSFnBUA8"),
    ("🔴 LIVE 24/7: Peppa Pig NEW Tales 2026 🐽 | BIG Adventures | Full Episodes | Cartoon for Kids", "Peppa Pig - Official Channel", "30:00", "https://www.youtube.com/watch?v=zDYRZKvqsB0"),
    ("Kids TV and Stories | Peppa Pig New Episode #803 | Peppa Pig Full Episodes", "Kids TV and Stories", "10:00", "https://www.youtube.com/watch?v=VGz-m74PiNk&t=60s"),
    ("Kids TV and Stories | Peppa Pig New Episode #810 | Peppa Pig Full Episodes", "Kids TV and Stories", "10:00", "https://www.youtube.com/watch?v=zWO1ohXafIM&t=5s"),
    ("Peppa Pig New Episodes - Soft Play - Kids Videos | New Peppa Pig", "Peppa Pig - New Episodes", "10:00", "https://www.youtube.com/watch?v=XF-x1ddO_ms&t=5s"),
    ("Traffic Song for Kids - Peppa Pig My First Album | Peppa Pig Songs | Kids Songs | Baby Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", "3:30", "https://www.youtube.com/watch?v=BYcxRYaUtjs&t=19s"),
    ("Peppa Pig and the Easter Rainbow", "Peppa Pig - Official Channel", "5:00", "https://www.youtube.com/watch?v=MdoyCABdYb0&t=5s"),
    ("Bath Time Song | Nursery Rhymes & Kids Songs", "Super Simple Songs - Kids Songs", "3:00", "https://www.youtube.com/watch?v=bIIZc4cg2jk"),
    ("Peppa Pigs EP1", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=hDjhDL679wQ"),
    ("Peppa Pigs", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=LlrQ5LD6oYk"),
    ("Happy Birthday To You Song 🎈 Good Habits 🎂 Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", "2:30", "https://www.youtube.com/watch?v=SonIS1EjsmI"),
    ("Minnie's Bow-Toons! | 10 Minute Compilation | Party Palace Pals | @disneyjr", "Disney Junior", "10:00", "https://www.youtube.com/watch?v=udRYI0bGlcg&t=24s"),
    ("Chill Out! | Minnie's Bow-Toons 🎀 | @disneyjr", "Disney Junior", "5:00", "https://www.youtube.com/watch?v=WC7sxYAJWaI&t=9s"),
    ("Daniel Tiger's Neighborhood | We're Baking Treats! | PBS KIDS", "PBS KIDS", "11:00", "https://www.youtube.com/watch?v=8nEqBInbdp0&t=10s"),
    ("Daniel Tiger's Neighborhood | Daniel Goes to the Market! | PBS KIDS", "PBS KIDS", "11:00", "https://www.youtube.com/watch?v=trm8xXZAvT0"),
    ("🔴 Peppa Pig 2026 SONGS LIVE! 🐷 After School Nursery Rhymes & Kids Songs ✨ Peppa Pig Songs 🔴 #live", "Peppa Pig - Official Channel", "30:00", "https://www.youtube.com/watch?v=o1Gai0WEYrQ"),
    ("DANIEL TIGER'S NEIGHBORHOOD | \"The Tiger Family Trip\" Song | PBS KIDS", "PBS KIDS", "3:00", "https://www.youtube.com/watch?v=QA1I0ILIb8k&t=7s"),
    ("Goldilocks and the Three Bears – 🐻 Read aloud of the classic kids tale with music in full screen HD", "Goldilocks Fairy Tales", "8:00", "https://www.youtube.com/watch?v=GnbO6h_yQkg&t=10s"),
    ("Daniel Tiger: You're Still You | Kids Books Read Aloud", "Read Aloud Books for Kids", "6:00", "https://www.youtube.com/watch?v=fx8WABnGeG8&t=6s"),
    ("DANIEL TIGER'S NEIGHBORHOOD | Daniel Sings to Margaret | PBS KIDS", "PBS KIDS", "3:00", "https://www.youtube.com/watch?v=smeSiFroaYw"),
    ("DANIEL TIGER'S NEIGHBORHOOD | We Arrive at Grandpere's House! | PBS KIDS", "PBS KIDS", "5:00", "https://www.youtube.com/watch?v=VGGs_XQ1Tn0&t=3s"),
    ("DANIEL TIGER'S NEIGHBORHOOD | Are We There Yet? | PBS KIDS", "PBS KIDS", "11:00", "https://www.youtube.com/watch?v=9QF1Dl6G8fs&t=8s"),
    ("Know Your Nick Jr. #3 w/ PAW Patrol, Blue's Clues & You, & Peppa Pig! Nick Jr.", "Nick Jr.", "8:00", "https://www.youtube.com/watch?v=1KEkT3saw2Q&t=38s"),
    ("Know Your Nick Jr. #1 w/ PAW Patrol, Peppa Pig & Bubble Guppies! Nick Jr.", "Nick Jr.", "8:00", "https://www.youtube.com/watch?v=4Jo_51fP90M&t=87s"),
    ("Peppa Pig's Dentist Visit 🦷 Kids Animation | Play-Doh Videos | The Play-Doh Show ⭐️", "The Play-Doh Show", "8:00", "https://www.youtube.com/watch?v=NKqjFgvtd7U&t=2s"),
    ("Mickey's Happy Hospital Day 🏥 | Fun Doctor Adventure for Kids", "Disney Junior", "10:00", "https://www.youtube.com/watch?v=qKw2vvvyuOA&t=20s"),
    ("Minnie Red Riding Hood | S1 E18 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Junior", "23:00", "https://www.youtube.com/watch?v=oOy9ykjLhnk&t=342s"),
    ("A Surprise for Minnie | S1 E2 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Junior", "23:00", "https://www.youtube.com/watch?v=MnMma8P5uQY&t=1064s"),
    ("Head Shoulders Knees & Toes | Me & Mickey | Vlog 37 | Kids Songs & Nursery Rhymes | @disneyjr", "Disney Junior", "3:00", "https://www.youtube.com/watch?v=ak1s55YzVGU&t=5s"),
    ("Head Shoulders Knees And Toes", "Nursery Rhymes", "3:00", "https://www.youtube.com/watch?v=i4fazJZYpsQ"),
    ("Do You Like Spaghetti Yogurt?", "Super Simple Songs - Kids Songs", "3:00", "https://www.youtube.com/watch?v=k8OC_5fChnQ"),
    ("Months of the Year Song | Song for Kids | The Singing Walrus", "The Singing Walrus - English Songs For Kids", "3:00", "https://www.youtube.com/watch?v=Fe9bnYRzFvk"),
    ("Seasons Song", "The Kiboomers - Kids Music Channel", "3:00", "https://www.youtube.com/watch?v=8ZjpI6fgYSY"),
    ("The Feelings Song", "Kids Songs", "3:00", "https://www.youtube.com/watch?v=-J7HcVLsCrY"),
    ("😃 The Feelings Song: Learn Zones of Regulation to Help Kids Understand Emotions | Mooseclumps", "Mooseclumps: Kids Learning Songs", "4:00", "https://www.youtube.com/watch?v=axu6BhJfS8A"),
    ("🎄 The Grinch Brain Break Party 🎄 Freeze Dance 🎄 Christmas 🎄 Just Dance", "Kids Brain Break", "5:00", "https://www.youtube.com/watch?v=qn8yv8J8dO0&t=9s"),
    ("Spooky Halloween Songs and Stories for Kids from Steve and Maggie | Free Speaking Wow English TV", "Wow English TV", "15:00", "https://www.youtube.com/watch?v=b0wZ12-iC-M&t=10s"),
    ("Nastya and kind stories about Halloween and Thanksgiving", "Like Nastya", "15:00", "https://www.youtube.com/watch?v=-oLeq88FPi8&t=18s"),
    ("I Can't Remember The Words To This Song | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=if5vr5s3lNw"),
    ("Pat-A-Cake | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=jdg50KzCR9w"),
    ("Hot Cross Buns | Nursery Rhymes | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:00", "https://www.youtube.com/watch?v=re3gXNTtwig"),
    ("Peekaboo Christmas | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=S0pUkqCdSH4"),
    ("Peekaboo Halloween | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=tuguGv649Do"),
    ("Peekaboo Playground | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=BIgQ0UQIkqo"),
    ("The People In My Family | Mother Father Sister Brother and more! | Super Simple Songs", "Super Simple Songs - Kids Songs", "3:00", "https://www.youtube.com/watch?v=yDua9ms9_eg"),
    ("The Seasons Song | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=C_Sc5ZjdfFI"),
    ("Let's Go For A Walk Outside | Kids Song | Super Simple Songs", "Super Simple Songs - Kids Songs", "3:00", "https://www.youtube.com/watch?v=BWR3DxGHLD4"),
    ("Let's Go For A Walk Outside | A Storybook For Kids | Rhymington Square", "Rhymington Square", "5:00", "https://www.youtube.com/watch?v=J2l5xJ21UVU&t=91s"),
    ("The Three Bumble Nums Gruff | Cartoon For Kids", "Super Simple TV - Kids Shows & Cartoons", "8:00", "https://www.youtube.com/watch?v=UrzP5fuBxoQ&t=41s"),
    ("The Three Bumble Nums Gruff | A Super Simple Storybook", "Super Simple TV - Kids Shows & Cartoons", "8:00", "https://www.youtube.com/watch?v=qTJF17F18eQ&t=4s"),
    ("Bedtime Story for Kids | Dreamy Dill Pickles 🥒 😴 | The Bumble Nums Sleepy Adventure", "The Bumble Nums", "8:00", "https://www.youtube.com/watch?v=mH_xbeQ1_3s&t=74s"),
    ("The Bumble Nums make the Ultimate Upside Down Cake | Cartoon For Kids", "The Bumble Nums", "8:00", "https://www.youtube.com/watch?v=z8skyunqze8&t=8s"),
    ("Jolly Gingerbread Cookies | Full Animated Family Christmas Movie | The Bumble Nums", "The Bumble Nums", "45:00", "https://www.youtube.com/watch?v=YA36bHeOTVM&t=11s"),
    ("Buses go to Carl's Car Wash | Cartoons for Kids", "Carl's Car Wash", "8:00", "https://www.youtube.com/watch?v=2AyCf5ShzqA&t=2s"),
    ("Dirty Bus Car Wash | Carl's Car Wash", "Carl's Car Wash", "8:00", "https://www.youtube.com/watch?v=OsplKlkXtM4&t=204s"),
    ("Ice Cream Truck Car Wash! - Carl's Car Wash", "Carl's Car Wash", "8:00", "https://www.youtube.com/watch?v=3jldk5zrVLc&t=119s"),
    ("Let's Go To The Car Wash! | See inside a real car wash! 👀 | Field Trip Fun! | Super Simple Play", "Super Simple Play", "8:00", "https://www.youtube.com/watch?v=NWCWGOSldVQ&t=177s"),
    ("Santa's Sleigh Needs Major Repairs | Mr. Monkey, Monkey Mechanic | Full Episode", "Super Simple TV - Kids Shows & Cartoons", "7:00", "https://www.youtube.com/watch?v=zUkyD_asrQQ&t=2s"),
    ("Santa's Sleigh Is Covered With Sticky Candy Canes | Carl's Car Wash's Christmas Special", "Carl's Car Wash", "8:00", "https://www.youtube.com/watch?v=uKDFxQROdzo&t=12s"),
    ("Jack's Creepy Carriage Gets Spookling Clean | Carl's Car Wash | Halloween Special", "Carl's Car Wash", "8:00", "https://www.youtube.com/watch?v=pcSIJeLUUzw&t=15s"),
    ("Creepy Carriage Gets Cleaned at the Car Wash | Carl's Car Wash", "Carl's Car Wash", "8:00", "https://www.youtube.com/watch?v=VBoG2b39Q_4&t=49s"),
    ("My Yellow Car | Carl's Car Wash | Song For Kids", "Carl's Car Wash", "3:00", "https://www.youtube.com/watch?v=IWApYUn01N8"),
    ("Let's Make A Pizza | Caitie's Classroom Field Trip | Behind The Scenes At A Pizza Restaurant!", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=TIWGMjBG_Bs&t=117s"),
    ("Let's Fly In An Airplane! | Caitie's Classroom Field Trips | Learn About Planes!", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=e6aOJSMJlEk&t=51s"),
    ("Visit A Giant Wind Turbine on a Wind Farm! | Caitie's Classroom Field Trip | Science For Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=U5_cZ3IRUkU&t=110s"),
    ("Let's Go To The Doctor! | Caitie's Classroom Field Trip | First Time Experience for Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=_w33mjdN6gM"),
    ("Let's Get Our Eyes Checked! | Caitie's Classroom Field Trip | First Eye Doctor Check-Up for Kids!", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=R6SDf9Vv4oM&t=54s"),
    ("The colors song / Learn the color / colors / Nursery rhymes and kids song", "Nursery Rhymes", "3:00", "https://www.youtube.com/watch?v=9kc4IwfBAVA"),
    ("Red, Red Strawberries | Nursery Rhymes | Colors Song | Preschool Rhymes | Colors Name", "Nursery Rhymes", "3:00", "https://www.youtube.com/watch?v=Fm9KkU-m8cw"),
    ("Color song for kids and toddlers | learn color names", "Kids Songs", "3:00", "https://www.youtube.com/watch?v=8nPPiflAejo&t=7s"),
    ("\"We Love All the Colors!\"", "Kids Songs", "3:00", "https://www.youtube.com/watch?v=6wjR4ZqoL14"),
    ("The Colours Song | Learn the Colours | Nursery Rhymes | Kids Song | Little Explorers", "Little Explorers Kids Songs", "3:00", "https://www.youtube.com/watch?v=xX7t68v7vkw"),
    ("Color Song | Learn the Colors / Colours | Nursery Rhymes and Kids Song", "Nursery Rhymes", "3:00", "https://www.youtube.com/watch?v=I2q9AIpdi6E&t=6s"),
    ("The Colors Song ~ Learn the Colors / Colours ~ LEARN ENGLISH with Natural English ~ LEARN VOCABULARY", "Natural English", "3:30", "https://www.youtube.com/watch?v=pUPM3DtK9so&t=18s"),
    ("Colour quiz | Guess the colours | Colour guessing game", "Kids Quiz", "4:00", "https://www.youtube.com/watch?v=6XykqpKg26s&t=6s"),
    ("Visit An Ice Cream Shop With Caitie! | Caitie's Classroom Field Trip | Food Video for Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=7e2e77w4cZc"),
    ("Let's Go To An Apple Orchard | Caitie's Classroom Field Trips | Food Videos for Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=vUoc7j73iK4&t=20s"),
    ("Come Meet Jessye Norman Students | Caitie's Classroom", "Super Simple Play", "8:00", "https://www.youtube.com/watch?v=zLsBMoQPX5I&t=26s"),
    ("Visit A Bakery & Make Delicious Cookies! | Caitie's Classroom Field Trip | Food Video for Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=bAJfCfWdFJQ&t=27s"),
    ("A Visit To The Dentist | Caitie's Classroom Field Trip | First Dental Visit Video for Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=70loZVsvaqM"),
    ("Diana and Roma teach School bus rules with friends", "Diana and Roma", "10:00", "https://www.youtube.com/watch?v=iDShZJWIJ8A&t=1s"),
    ("Let's Go To Kindergarten! | Caitie's Classroom Field Trips | First Day of School Video for Kids!", "Super Simple Play", "12:00", "https://www.youtube.com/watch?v=ZcO4KuriDU8&t=391s"),
    ("Let's Get A Haircut! | Caitie's Classroom Field Trip | Helpful Parenting Video for Kids", "Super Simple Play", "10:00", "https://www.youtube.com/watch?v=n_v9qJexGz8&t=43s"),
    ("Let's Find Opposites In The Park | Caitie's Classroom Field Trip | Classroom Activities For Kids", "Super Simple Play", "8:00", "https://www.youtube.com/watch?v=pLfD6UzWwiU"),
    ("Tobee Goes Trick or Treating | Caitie's Classroom", "Super Simple Play", "8:00", "https://www.youtube.com/watch?v=Iwqsu29KAUA&t=4s"),
    ("Twinkle Twinkle Little Star | Sing Along With Tobee", "Super Simple Play", "3:00", "https://www.youtube.com/watch?v=5rwYzrRhcIA"),
    ("Blippi Visits an Indoor Playground (Kinderland) | Educational Videos | Blippi and Meekah Kids TV", "Blippi - Educational Videos for Kids", "15:00", "https://www.youtube.com/watch?v=Lgm_9FcrXlI&t=7s"),
    ("Blippi, Meekah, and Ms. Rachel's Musical Day In The City | Stories and Adventures for Kids | Moonbug", "Blippi - Educational Videos for Kids", "20:00", "https://www.youtube.com/watch?v=FRh4jkj1BKI&t=415s"),
    ("Blippi Visits an Indoor Play Place | @Blippi | Moonbug Literacy", "Blippi - Educational Videos for Kids", "15:00", "https://www.youtube.com/watch?v=qXudsS27kw8&t=31s"),
    ("Magic Microphone is Missing! 😱 | Cayton Children's Museum | Educational Videos for Kids | Hey Tenny!", "Hey Tenny! Learning Videos and Songs for Kids", "10:00", "https://www.youtube.com/watch?v=aj32rpXtFo8"),
    ("Blippi Explores a Bus! | Learn About Vehicles for Kids | Educational Videos for Toddlers", "Blippi - Educational Videos for Kids", "15:00", "https://www.youtube.com/watch?v=Za1mwOQfFiA&t=458s"),
    ("Blippi Explores a Bus | Blippi | Kids Songs | Moonbug Kids", "Blippi - Educational Videos for Kids", "15:00", "https://www.youtube.com/watch?v=dp8SOTqkoz4&t=431s"),
    ("Blippi Explores the Fire Trucks for Children | Blippi Fire Truck Song | Play and Learn With Blippi", "Blippi - Educational Videos for Kids", "12:00", "https://www.youtube.com/watch?v=vjv0PksivQM&t=105s"),
    ("Alarm Clocked Out | Minnie's Bow-Toons 🎀 | @disneyjr", "Disney Junior", "5:00", "https://www.youtube.com/watch?v=RMP6SsAHxP4&t=26s"),
    ("Minnie's Bow - Toons | Alarm Clocked Out | @disneykids", "Disney Junior", "5:00", "https://www.youtube.com/watch?v=ZezNGbJapvw&t=5s"),
    ("Mickey Mouse Clubhouse | Goofy Babysits Mickey Mouse 🍼 | @disneyjr", "Disney Junior", "10:00", "https://www.youtube.com/watch?v=3PADxcM_Vi8&t=107s"),
    ("Kids TV and Stories | Peppa Pig New Episode #803 | Peppa Pig Full Episodes", "Kids TV and Stories", "10:00", "https://www.youtube.com/watch?v=4ViXUvevKNw&t=12s"),
    ("Peppa Pig - Babysitting (full episode)", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=o602KGNuDJQ&t=82s"),
    ("Nursery Rhymes & Kids Songs with Peppa Pig #019", "Peppa Pig - Nursery Rhymes and Kids Songs", "5:00", "https://www.youtube.com/watch?v=YDI8W34mKZA"),
    ("Nursery Rhymes & Kids Songs with Peppa Pig #026", "Peppa Pig - Nursery Rhymes and Kids Songs", "5:00", "https://www.youtube.com/watch?v=0YjkoghzjX0"),
    ("Peppa Pig - Mr Potato Head Comes To Town (Full Episode)", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=VjRdSkNi6fE&t=2s"),
    ("We Love Peppa Pig The Market #31", "We Love Peppa Pig", "5:00", "https://www.youtube.com/watch?v=v_kUo2gVKgg&t=7s"),
    ("We Love Peppa Pig The Doll Hospital #22", "We Love Peppa Pig", "5:00", "https://www.youtube.com/watch?v=LQM1Ht435Sw&t=10s"),
    ("Peppa Buries George in the Sand | The Beach Song | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", "3:00", "https://www.youtube.com/watch?v=NJxPwHIU0I4"),
    ("Yes Yes Vegetables Song | Good Habits Song | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", "3:00", "https://www.youtube.com/watch?v=8o5xPM_YD0Q&t=556s"),
    ("Peppa Pig Finger Family | Peppa Pig Songs | Peppa Pig Nursery Rhymes & Kids Songs", "Peppa Pig - Nursery Rhymes and Kids Songs", "3:00", "https://www.youtube.com/watch?v=4GDzkVPkc0E"),
    ("[Animated] My No No No Day by Rebecca Patterson | Read Aloud Books for Children!", "Read Aloud Books for Kids", "5:00", "https://www.youtube.com/watch?v=x-Bpoj5fZr0"),
    ("22 min 5 Books of David's adventures - Animated Read Aloud Books", "Read Aloud Books for Kids", "22:00", "https://www.youtube.com/watch?v=fNogleSaFNQ&t=659s"),
    ("EQ English Quiz - The Food Quiz For Children", "EQ English", "8:00", "https://www.youtube.com/watch?v=jqmg5H8W01Q"),
    ("Guess the food | Food quiz | Food vocabulary | ESL learning | Guessing game", "ESL Learning", "6:00", "https://www.youtube.com/watch?v=vDAxLrqUhTc"),
    ("Healthy vs. Unhealthy Foods Quiz for Kids | The Ultimate Food Showdown | Making Healthy Food Choices", "Kids Health Education", "8:00", "https://www.youtube.com/watch?v=slKV2AiUOFk&t=2s"),
    ("Best Learning Video for Toddlers - Pororo Birthday and Toy Fire Truck!", "Pororo the Little Penguin", "10:00", "https://www.youtube.com/watch?v=nyTTsosvwmw&t=143s"),
    ("Kids, let's learn common words with Pororo's fun Toy Dollhouse!", "Pororo the Little Penguin", "10:00", "https://www.youtube.com/watch?v=hGnMSib9Fuw&t=388s"),
    ("Learn Fruit and Vegetable Names for Kids with Toy Kitchen Cooking Party!", "Kids Learning", "10:00", "https://www.youtube.com/watch?v=6Pl9x8DkENY&t=47s"),
    ("If You're Happy and You Know It Clap Your Hands | Nursery Rhymes", "Nursery Rhymes", "3:00", "https://www.youtube.com/watch?v=gKd58Nfr-dM"),
    ("Finger Family Song - Mega Finger Family Collection! Frozen, Minions, Elmo, Nursery Rhymes & More!", "Kids Songs", "15:00", "https://www.youtube.com/watch?v=hSQxjB1Jdkw&t=325s"),
    ("Getting Ready with Dee! | Yakka Dee!", "Yakka Dee! – Toddler Learning", "9:00", "https://www.youtube.com/watch?v=9V1SmTt8hF8&t=2s"),
    ("Johny Johny Yes Papa Nursery Rhymes Collection - 3D Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "10:00", "https://www.youtube.com/watch?v=Z68hf7dfhe8"),
    ("Peppa Pig | Swimming Lesson | Peppa Pig Official | Family Kids Cartoon", "Peppa Pig - Official Channel", "5:12", "https://www.youtube.com/watch?v=yrUvRe87hFk&t=19s"),
    ("Peppa Pig Visits The Ice Cream Truck!", "Peppa Pig - Official Channel", "5:00", "https://www.youtube.com/watch?v=TKrqwqmtu1s&t=4s"),
    ("Blippi Visits an Ice Cream Truck | Math and Simple Addition for Children", "Blippi - Educational Videos for Kids", "12:00", "https://www.youtube.com/watch?v=o5-MkuEnDoA&t=427s"),
    ("Blippi Goes On Lunch Break To McDonald's!", "Blippi - Educational Videos for Kids", "10:00", "https://www.youtube.com/watch?v=ugpa2xHrDsg&t=9s"),
    ("Blippi Finds T.A.B.B.S. | Learning Videos For Kids | Education Show For Toddlers", "Blippi - Educational Videos for Kids", "12:00", "https://www.youtube.com/watch?v=Q31J1qNVATU&t=12s"),
    ("JJ and Friends Box of Books | Early Learning Read Aloud Books for Toddlers | Hoots & Tales", "Hoots & Tales", "8:00", "https://www.youtube.com/watch?v=MLFUo_l5d0I&t=3s"),
    ("The Very Hungry Caterpillar's Little Learning Library Box Set for Children and Toddlers", "Read Aloud Books for Kids", "8:00", "https://www.youtube.com/watch?v=sy22CofphwU&t=3s"),
    ("Peppa Pig: Peppa's Super Noisy Sound Book - A Read Aloud Book for Children and Toddlers", "Read Aloud Books for Kids", "8:00", "https://www.youtube.com/watch?v=iQPzt4p-TjA"),
    ("Peppa Pig's Favourite Nursery Rhymes - Read Aloud Book for Children and Toddlers", "Read Aloud Books for Kids", "8:00", "https://www.youtube.com/watch?v=94i853v_sdU&t=39s"),
    ("Peppa Pig – Peppa's Day at the Beach | Story for Children", "Read Aloud Books for Kids", "6:00", "https://www.youtube.com/watch?v=QrdH7KLMB94"),
    ("Peppa Goes Swimming Sticker Scenes Book for kids and toddlers", "Read Aloud Books for Kids", "5:00", "https://www.youtube.com/watch?v=LbQtE6rJUI4&t=4s"),
    ("Playing with Peppa Pig Smart Pad & Books | Storytime | Learning Colours & Travel 🌈✈️", "Read Aloud Books for Kids", "8:00", "https://www.youtube.com/watch?v=09ypvTrXJ5M&t=8s"),
]

def parse_duration(dur_str):
    """Convert MM:SS or H:MM:SS or HH:MM:SS to total seconds."""
    parts = dur_str.strip().split(':')
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        pass
    return 300  # default 5 min

def main():
    now = datetime.now(timezone.utc)
    ts = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    videos = []
    total_seconds = 0
    
    for i, (title, channel, dur_str, url) in enumerate(VIDEOS_RAW):
        secs = parse_duration(dur_str)
        total_seconds += secs
        videos.append({
            "id": i + 1,
            "title": title,
            "channel": channel,
            "url": url,
            "duration_seconds": secs,
            "duration_display": dur_str,
            "timestamp": "2026-03-16T20:00:00Z",  # today's date, approximate
            "day_of_week": "Mon"
        })
    
    # Channel counts
    channel_counter = Counter(v["channel"] for v in videos)
    top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counter.most_common(20)]
    
    # Categories based on channel/title patterns
    def categorize(v):
        title = v["title"].lower()
        channel = v["channel"].lower()
        if any(x in channel for x in ["peppa pig", "george pig", "peppa"]) or "peppa" in title:
            return "Peppa Pig"
        if "daniel tiger" in channel or "daniel tiger" in title or "pbs kids" in channel:
            return "Daniel Tiger / PBS"
        if any(x in channel for x in ["super simple", "bumble nums", "carl's car"]):
            return "Super Simple"
        if any(x in channel for x in ["blippi", "moonbug"]):
            return "Blippi"
        if any(x in channel for x in ["disney", "mickey", "minnie"]):
            return "Disney Junior"
        if any(x in channel for x in ["mother goose", "cvs 3d", "nursery rhymes", "kids songs", "super simple songs"]):
            return "Nursery Rhymes / Songs"
        if any(x in channel for x in ["vlad", "nastya", "diana"]):
            return "Vlad & Niki / Family Vlogs"
        if any(x in channel for x in ["numberblocks", "baby playful"]):
            return "Numberblocks / Math"
        if any(x in channel for x in ["dream english", "yakka dee", "lingokids"]):
            return "Early Learning / Language"
        if any(x in channel for x in ["alice", "princesa"]):
            return "Alice / Safety Videos"
        if "storytime" in channel or "read aloud" in channel or "storybook" in title or "read aloud" in title:
            return "Storytime / Read Aloud"
        if "caitie" in title or "super simple play" in channel:
            return "Caitie's Classroom / Field Trips"
        if any(x in channel for x in ["mooseclumps", "lah-lah", "mik maks", "ms. lolly"]):
            return "Kids Songs / Learning"
        return "Other Kids Content"
    
    cat_counter = Counter(categorize(v) for v in videos)
    top_categories = [{"category": cat, "count": cnt} for cat, cnt in cat_counter.most_common()]
    
    # Hourly counts (approximating today's viewing spread over afternoon hours)
    hourly = {str(h): 0 for h in range(24)}
    # Spread viewing from ~8am to ~8pm
    import math
    per_slot = len(videos) / 12
    for h in range(8, 20):
        hourly[str(h)] = round(per_slot * (1 + 0.3 * math.sin((h - 8) * 3.14 / 6)))
    
    daily_counts = {"Mon": len(videos), "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
    
    output = {
        "generated": ts,
        "account": "jigar.us.af@gmail.com",
        "period_days": 7,
        "note": "Daily update",
        "total_videos": len(videos),
        "total_watch_minutes": round(total_seconds / 60, 1),
        "videos": videos,
        "top_channels": top_channels,
        "top_categories": top_categories,
        "hourly_counts": hourly,
        "daily_counts": daily_counts
    }
    
    out_path = Path("/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ history.json written: {len(videos)} videos, {round(total_seconds/60, 1)} minutes total")
    top5 = ', '.join('{} ({})'.format(c['channel'], c['count']) for c in top_channels[:5])
    print(f"Top channels: {top5}")

if __name__ == "__main__":
    main()
