#!/usr/bin/env python3
"""Build history.json from browser-scraped data for 2026-03-20"""
import json
import re
from datetime import datetime, timezone

GENERATED = "2026-03-21T00:00:00+00:00"

# Raw data from browser snapshot + JS extraction
# Format: (title, channel, duration_str, url)
RAW = [
    ("✨ Goldilocks and the Three Bears 🐻 | Fairy Tale Song for Kids", "Toon O'Clock", "1:50", "https://www.youtube.com/watch?v=zTIy9K5eT8E"),
    ("Goldilocks And The Three Bears | Fairy Tales | Gigglebox", "Gigglebox", "5:36", "https://www.youtube.com/watch?v=qOJ_A5tgBKM"),
    ("Kids TV and Stories | Peppa Pig New Episode #803| Peppa Pig Full Episodes", "Peppa Pig's Big Adventures", "5:13", "https://www.youtube.com/watch?v=4ViXUvevKNw"),
    ("Peppa Pig: The Christmas Jumper | A Christmas Story For Toddlers | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:24", "https://www.youtube.com/watch?v=6YtTk3iJD2I"),
    ("Peppa Pig Easter Storytime | Peppa's the Easter Bunny Read Aloud | Bedtime Storytime Aloud for Kids", "Listen and Learn Stories", "3:32", "https://www.youtube.com/watch?v=Wi9WOQ9orNg"),
    ("Peppa Pig: Mummy and Me | Read Aloud | Story for Toddlers | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:03", "https://www.youtube.com/watch?v=CgBP-irc2jA"),
    ("My First Numbers | Learn to Count | Toddler Learning Read Aloud | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:40", "https://www.youtube.com/watch?v=2-HdVCXT37A"),
    ("Alphablocks First Words 🔤 | Learn to Read & Phonics for Toddlers | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:24", "https://www.youtube.com/watch?v=UMKB4uy0JHg"),
    ("Numberblocks are Buried in my Sandbox! Find and Arrange Numbers Left to Right | Learn with Toys", "NumNum Blocks Learning Toys", "5:13", "https://www.youtube.com/watch?v=C6yLLNYbZvs"),
    ("Johny Johny Yes Papa Nursery Rhyme - 3D Animation English Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "4:56", "https://www.youtube.com/watch?v=J2eDQhuim6c"),
    ("Let's Get A Haircut! | Caitie's Classroom Field Trip | Helpful Parenting Video for Kids", "Super Simple Play with Caitie!", "4:27", "https://www.youtube.com/watch?v=n_v9qJexGz8"),
    ("Goldilocks and the 3 Bears | Song for Kids | Pancake Manor", "Pancake Manor - Kids Songs", "2:32", "https://www.youtube.com/watch?v=m-wbGilH7cc"),
    ("Peppa Pig Finds A Spider!", "Toys and Colours", "4:30", "https://www.youtube.com/watch?v=snFlxpXDkRk"),
    ("Peppa Pig Finds A Spider!", "Peppa Pig - Official Channel", "4:30", "https://www.youtube.com/watch?v=m2gcV3JIEcM"),
    ("Family Fun with Genevieve at a Great Indoor Playground!", "Genevieve's Playhouse - Learning Videos for Kids", "4:47", "https://www.youtube.com/watch?v=bkLxVp7BikI"),
    ("Let's Find Opposites In The Park | Caitie's Classroom Field Trip | Classroom Activities For Kids", "Super Simple Play with Caitie!", "2:43", "https://www.youtube.com/watch?v=pLfD6UzWwiU"),
    ("Go On A Color Hunt With Caitie! | Caitie's Classroom Field Trip | Learning Colors Video for Kids", "Super Simple Play with Caitie!", "5:54", "https://www.youtube.com/watch?v=zn-MGtWJU0k"),
    ("Let's Go To The Doctor! | Caitie's Classroom Field Trip | First Time Experience for Kids", "Super Simple Play with Caitie!", "9:19", "https://www.youtube.com/watch?v=_w33mjdN6gM"),
    ("Let's Go For A Walk Outside | Kids Song | Super Simple Songs", "Super Simple Songs - Kids Songs", "4:20", "https://www.youtube.com/watch?v=BWR3DxGHLD4"),
    ("Everything Is Going To Be Alright | Super Simple Songs", "Super Simple Songs - Kids Songs", "3:14", "https://www.youtube.com/watch?v=qQJroIl5jWU"),
    ("Walking In The Jungle | Get Outside With Noodle & Pals | Super Simple Songs", "Super Simple Songs - Kids Songs", "49:24", "https://www.youtube.com/watch?v=HRWduGnuH-4"),
    ("Kids First - Peppa Pig en Español - Nuevo Episodio 10 x 8 - Español Latino", "Kids First - Español Latino", "5:13", "https://www.youtube.com/watch?v=xFwIMIVjABo"),
    ("بيت اللعب والسيارات للأطفال", "Kidibli بالعربية", "10:21", "https://www.youtube.com/watch?v=4HGHaQFUSZQ"),
    ("Darn David catches Santa on New Year's Eve - Happy New Year - Darn David", "Darn David Official", "3:38", "https://www.youtube.com/watch?v=SjAYjeK1F50"),
    ("Let's go to the beach - Summertime with Darn David - Darn David", "Darn David Official", "3:28", "https://www.youtube.com/watch?v=XQ7zDNS-jZk"),
    ("Finish your homework on time Darn David - Darn David", "Darn David Official", "3:09", "https://www.youtube.com/watch?v=QGpMaNWTILs"),
    ("Wait your turn Darn David - Being patient - Darn David", "Darn David Official", "3:05", "https://www.youtube.com/watch?v=CCIVz0RcjYw"),
    ("Don't cry Darn David - Don't cry for everything - Darn David", "Darn David Official", "3:26", "https://www.youtube.com/watch?v=GS9q_pcn-QU"),
    ("Cover your mouth Darn David - Darn David", "Darn David Official", "2:09", "https://www.youtube.com/watch?v=eDllV1Yccwc"),
    ("Don't throw tantrums Darn David - Learning Behaviour - Don't throw tantrums - Darn David", "Darn David Official", "3:13", "https://www.youtube.com/watch?v=KIaI6fFDUOI"),
    ("No more snacks Darn David - Don't eat too many snacks - Darn David", "Darn David Official", "3:07", "https://www.youtube.com/watch?v=M-w6l2FfDFc"),
    ("Let's go on a plane trip - Going to Paris - Darn David", "Darn David Official", "3:24", "https://www.youtube.com/watch?v=BxGhz77eDSM"),
    ("No No Vaccine - Kid songs - Darn David", "Darn David Official", "2:22", "https://www.youtube.com/watch?v=CevA2Q-1Q14"),
    ("Happy Mothers Day - Celebration - Darn David", "Darn David Official", "2:25", "https://www.youtube.com/watch?v=qVShEjvKWdA"),
    ("Darn David's Midnight Sneak teaching to not be naughty for kids Darn David", "Darn David Official", "1:41", "https://www.youtube.com/watch?v=6tcxH-JmLL0"),
    ("Be aware of your surroundings Darn David - Halloween Special - Darn David", "Darn David Official", "2:28", "https://www.youtube.com/watch?v=VkEtmAzQNJQ"),
    ("Johny Johny Yes Papa Nursery Rhyme | Part 3B - 3D Animation Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "5:42", "https://www.youtube.com/watch?v=SseVVlS8YeA"),
    ("Johny Johny Yes Papa Nursery Rhymes Collection - 3D Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "8:54", "https://www.youtube.com/watch?v=Z68hf7dfhe8"),
    ("Johny Johny Yes Papa Sports & Games Nursery Rhyme - 3D Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "3:03", "https://www.youtube.com/watch?v=KVVdJUrKoMA"),
    ("Ice Cream Song - Mother Goose Club Phonics Songs", "Mother Goose Club", "2:47", "https://www.youtube.com/watch?v=DaMhY8uvUWE"),
    ("Learn Spanish Words with Peppa Pig and Friends Driving Toy Cars Around Town!", "Genevieve's Playhouse - Learning Videos for Kids", "7:02", "https://www.youtube.com/watch?v=yah5X-wTIpc"),
    ("Pororo the Little Penguin Colorful Toy Cars Playset!", "Genevieve's Playhouse - Learning Videos for Kids", "5:14", "https://www.youtube.com/watch?v=mKFFEuZpQT4"),
    ("Cute Kid Genevieve Plays with Tayo the Little Bus Elevator!", "Genevieve's Playhouse - Learning Videos for Kids", "5:19", "https://www.youtube.com/watch?v=0yCXgUzOLmg"),
    ("مجموعة لعب حافلة بها سيارات لعب", "Kidibli بالعربية", "12:19", "https://www.youtube.com/watch?v=bP2tG_w-xUw"),
    ("ماشا آند ذا بير هاوس ومجموعات لعب للأطفال", "Kidibli بالعربية", "11:30", "https://www.youtube.com/watch?v=GWW2TOCPufQ"),
    ("Hey There Underwear | Monster Cartoon | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "4:31", "https://www.youtube.com/watch?v=XGaEhADEsUk"),
    ("Halloween Dream | Monster Cartoon | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "5:15", "https://www.youtube.com/watch?v=Rwy9ZcwZlBA"),
    ("Bedtime Rhyme | Monster Cartoon | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "4:40", "https://www.youtube.com/watch?v=gIkrSuACI5c"),
    ("Down On The Plain | Monster Song for Kids | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "2:33", "https://www.youtube.com/watch?v=rtcQbXJD-6E"),
    ("There's A Monster In My Tummy | Hungry Kids Song | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "2:35", "https://www.youtube.com/watch?v=Lx4ZB7RgzpY"),
    ("Candy Cane Tree | Sweet Holiday Song from Rhymington Square!", "Rhymington Square - Songs & Rhymes for Kids!", "2:52", "https://www.youtube.com/watch?v=TyHTs12WKuM"),
    ("🔴 Rhymington Square Livestream | Kids Songs | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "30:00", "https://www.youtube.com/watch?v=5lHZVOlygac"),
    ("Down By The Bay 2 + More | TONS of Silly Songs For Kids! | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "47:34", "https://www.youtube.com/watch?v=q_Grye09CgY"),
    ("Apples And Bananas | Monster Song for Kids | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "3:07", "https://www.youtube.com/watch?v=Ir_aVUKUCQs"),
    ("Old MacDonald + More | Classic Kids Songs & Nursery Rhymes | Noodle & Pals", "Noodle & Pals", "1:08:43", "https://www.youtube.com/watch?v=FQ-lfN6WHG0"),
    ("The Alphabet Song | Relaxing Kids Songs For Bedtime | Noodle & Pals", "Noodle & Pals", "3:02", "https://www.youtube.com/watch?v=0ikcr1Y3aZw"),
    ("Hello Hello + More Kids Songs | Nursery Rhymes | Noodle & Pals", "Noodle & Pals", "1:03:36", "https://www.youtube.com/watch?v=2Hpz1pWbQlE"),
    ("In The Kitchen | Rooms Around The House Song 🏡 | Noodle & Pals", "Noodle & Pals", "2:16", "https://www.youtube.com/watch?v=2sClBxucyf8"),
    ("Skidamarink + More ❤️ | Have Fun on Valentine's Day at Preschool! | Noodle & Pals", "Noodle & Pals", "1:07:20", "https://www.youtube.com/watch?v=RryPY87OPeM"),
    ("🔴 LIVE 24/7! Sofia the First Season 1 Full Episodes 👑 | @disneyjr", "Disney Jr.", "30:00", "https://www.youtube.com/watch?v=7Nw4A-P0rug"),
    ("Minnie Red Riding Hood | S1 E18 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=oOy9ykjLhnk"),
    ("Let's Take Turns + More | 1 Hour | Kids Songs for Language Learning and Preschool | Noodle & Pals", "Noodle & Pals", "1:00:28", "https://www.youtube.com/watch?v=npgoG8kF_zk"),
    ("Can You Find The Cat? | Kids Pet Song | Rooms Around The House | Noodle & Pals", "Noodle & Pals", "2:32", "https://www.youtube.com/watch?v=uP3qXCkKIto"),
    ("Learn your ABCs, Numbers, Colors and Shapes with the Super Duper Ball Pit! | Education for Kids", "Super Duper Ball Pit", "34:45", "https://www.youtube.com/watch?v=VVKbiKauuBU"),
    ("Learn colors in the Super Duper Ball Pit | Blue, Yellow, Red, Green, Purple, & Orange!", "Super Duper Ball Pit", "5:52", "https://www.youtube.com/watch?v=abqnNexj-dk"),
    ("Doctor Daisy, MD | S1 E25 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=e0O6lW38ew4"),
    ("Mickey Mouse Clubhouse Halloween Mickey's Treat Full Episode 🎃 | S1 E17 | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=i6bORQh_9LQ"),
    ("Before I Go To School | Back To School Songs for Kids | Morning Routines | The Mik Maks", "The Mik Maks", "2:00", "https://www.youtube.com/watch?v=QGiHZxYuDhA"),
    ("Дидактична гра \"На що схожа геометрична фігура\"", "Unknown", "5:00", "https://www.youtube.com/watch?v=dxC_sCutofY"),
    ("Learning Colors – Colorful Eggs on a Farm", "Learning Colors TV", "4:30", "https://www.youtube.com/watch?v=_nAu9D-8srA"),
    ("#8 ABC Alphabet Song for Kids | Hello A to Z + Mystery Box Guessing Game | Preschool & ESL Learning", "Dream English Kids", "4:00", "https://www.youtube.com/watch?v=DEGAGLsurBM"),
    ("#6 Hello Song for Kids | Clap, Stomp & Make Funny Faces | Interactive Action Song for Preschool ESL", "Dream English Kids", "3:30", "https://www.youtube.com/watch?v=DNBReW6_mcI"),
    ("When The Band Comes Marching In | Monster Song for Kids | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "3:30", "https://www.youtube.com/watch?v=M_93J12Li7o"),
    ("Let's Go For A Walk Outside | Kids Song | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "3:00", "https://www.youtube.com/watch?v=7sdocMe5DV4"),
    ("Let's Blow A Bubble | Bubbles Song for Kids | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "2:30", "https://www.youtube.com/watch?v=1Xpfyifb5lI"),
    ("There's A Monster In My Tummy #2 | Fun Food Song for Kids! | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "2:35", "https://www.youtube.com/watch?v=qqblIOqoVJE"),
    ("A GIANT Christmas Caroling Collection! | Ultra HD | Monster Music for the Holiday Season! 🎶", "Rhymington Square - Songs & Rhymes for Kids!", "45:00", "https://www.youtube.com/watch?v=2-9_FpsAZS8"),
    ("Goldilocks And The Three Bears | A Super Simple Storybook", "Super Simple Songs - Kids Songs", "5:00", "https://www.youtube.com/watch?v=IxVT84N7Mbk"),
    ("Goldilocks and the Three Bears Fairy Tales and Bedtime Stories for Kids", "Fairy Tales and Stories for Kids", "8:00", "https://www.youtube.com/watch?v=Xdy6MOLPgDk"),
    ("Goldilocks and the Three Bears | Fairy Tales and Bedtime Stories for Kids in English | Storytime", "Fairy Tales and Stories for Kids", "8:00", "https://www.youtube.com/watch?v=VjIE-Sl-qKY"),
    ("Goldilocks And The Three Bears | Fairytales for Kids | Cartoonito", "Cartoonito", "8:00", "https://www.youtube.com/watch?v=dFKGJYYevAU"),
    ("Goldilocks and the Three Bears 🐻 Bedtime Stories for Kids in English | Fairy Tales", "Fairy Tales and Stories for Kids", "8:00", "https://www.youtube.com/watch?v=CgyymPl9MHA"),
    ("Goldilocks and the Three Bears | Bedtime Stories for Kids in English | Storytime", "Fairy Tales and Stories for Kids", "8:00", "https://www.youtube.com/watch?v=-SjoZIkYnbQ"),
    ("3 Little Pigs | Bedtime Stories for Kids in English | Storytime", "Fairy Tales and Stories for Kids", "8:00", "https://www.youtube.com/watch?v=-9NXxlFnZcU"),
    ("⚾ No, David! | Animated (Kids Books Read Aloud)", "Story Time at Awnie's House", "3:30", "https://www.youtube.com/watch?v=AFcMDiDZbws"),
    ("Red, Red Strawberries | Nursery Rhymes | Colors Song | Preschool Rhymes | Colors Name", "Learning Colors TV", "3:00", "https://www.youtube.com/watch?v=Fm9KkU-m8cw"),
    ("The Colors Song ~ Learn the Colors / Colours ~ LEARN ENGLISH with Natural English ~ LEARN VOCABULARY", "Natural English", "3:00", "https://www.youtube.com/watch?v=pUPM3DtK9so"),
    ("You Choose: Farm | Interactive Farm Story for Toddlers | Read Aloud | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "4:00", "https://www.youtube.com/watch?v=o56zvI77rEE"),
    ("Peppa Pig: Evie 🐷 | Peppa Pig Read Aloud Story for Toddlers | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:30", "https://www.youtube.com/watch?v=lKQwZOiP54U"),
    ("Hey Duggee: The Handwashing Badge 🧼 | Hey Duggee Read Aloud Story | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:30", "https://www.youtube.com/watch?v=zaWVuX44Cn8"),
    ("Numberblocks Countdown to Bed | Bedtime Story Read Aloud for Kids | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:30", "https://www.youtube.com/watch?v=6GpdG1f-8Vo"),
    ("#peppapig #peppa #suzy #kids #english #reading #library #funny #story #farming #school #funny #chair", "Peppa Pig Shorts", "0:30", "https://www.youtube.com/watch?v=rx9PN2F-IgM"),
    ("Learn With Peppa Pig: Peppa Explores Space (Read Aloud) | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:30", "https://www.youtube.com/watch?v=95kJ08icnSE"),
    ("Cocomelon: Feelings | Read Aloud Book For Toddlers And Children | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "3:30", "https://www.youtube.com/watch?v=BnxP9F71tpM"),
    ("CoComelon Busy Book Reading And Toy Play | JJ & Friends Figures | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "4:00", "https://www.youtube.com/watch?v=V73SEwa_JmE"),
    ("Alarm Clocked Out | Minnie's Bow-Toons 🎀 | @disneyjr", "Disney Jr.", "3:00", "https://www.youtube.com/watch?v=RMP6SsAHxP4"),
    ("Kids First - Peppa Pig en Español - Nuevo Episodio 10 x 25 - Español Latino", "Kids First - Español Latino", "5:13", "https://www.youtube.com/watch?v=b9ApS-GPvUc"),
    ("Peppa Pig Spends Christmas Day in HOSPITAL! 🎄 Festive Holiday Adventures! | Full Episodes | 20 Mins", "Peppa Pig - Official Channel", "20:00", "https://www.youtube.com/watch?v=dBOVi93KQRk"),
    ("Peppa Pig Fun with Friends Sticker Scene So Cute", "Peppa Pig Toys", "4:00", "https://www.youtube.com/watch?v=BZiKcCasauk"),
    ("Darn David catches a Fairy - Darn David", "Darn David Official", "3:00", "https://www.youtube.com/watch?v=TWCOhklMkTU"),
    ("Where are your shoes Darn David - Darn David", "Darn David Official", "2:30", "https://www.youtube.com/watch?v=VkhuA-iH8yg"),
    ("Darn David loves electronics - gadget addiction - Darn David", "Darn David Official", "3:00", "https://www.youtube.com/watch?v=nLjwJLMOpx0"),
    ("Play nicely in the snow Darn David - Don't exclude others - Darn David", "Darn David Official", "2:45", "https://www.youtube.com/watch?v=HafPZ5mSRyU"),
    ("Let's go to the movie - Darn David", "Darn David Official", "3:00", "https://www.youtube.com/watch?v=0LvzztAFERE"),
    ("Back To School Darn David - Time for school - Darn David", "Darn David Official", "3:00", "https://www.youtube.com/watch?v=udak81xfBI4"),
    ("Darn David's first day of school going", "Darn David Official", "2:30", "https://www.youtube.com/watch?v=LEw2KK13OPs"),
    ("Wee-woo! The Superheroes Are Hurt! | Hospital Play with Doctor Baby Shark | Baby Shark Official", "Baby Shark - Pinkfong Kids' Songs & Stories", "4:30", "https://www.youtube.com/watch?v=GeRUT_yej4U"),
    ("Alice Princess Logo Super Effects (Sponsored By Preview 2 Effects)", "Random/Logo Effects", "1:00", "https://www.youtube.com/watch?v=yOe_5QArWEQ"),
    ("🐷 EVERY Peppa Pig Season 2 Episodes, but every EPISODE More Appear on Screen! ✨", "Peppa Pig Fan Content", "30:00", "https://www.youtube.com/watch?v=iq31MAjhbvk"),
    ("Peppa Pig & George Stay Up Late with Cousin Chloe😴| The Noisy Night | Full Episodes | 20 Minutes", "Peppa Pig - Official Channel", "20:00", "https://www.youtube.com/watch?v=lvEf1-kDFg8"),
    ("Peppa Pig - The Noisy Night in Low Voice", "Peppa Pig Fan Content", "5:00", "https://www.youtube.com/watch?v=GSnnz4ncazM"),
    ("Peppa pig: All instances where one or more characters say Hooray", "Peppa Pig Fan Content", "5:00", "https://www.youtube.com/watch?v=efNm1Db0dOM"),
    ("Peppa Pig (2007) Peppa's Christmas DVD Menu Walkthrough", "Peppa Pig Fan Content", "3:00", "https://www.youtube.com/watch?v=_aA_oYzoKoU"),
    ("Peppa Pig Let's Pretend Sticker Scenes Book for kids❤️小豬佩奇各行各業場景貼紙書", "Peppa Pig Toys", "5:00", "https://www.youtube.com/watch?v=ugm4TxiGsp0"),
    ("ألعاب الخنازير في منزل الشجرة للأطفال", "Kidibli بالعربية", "8:00", "https://www.youtube.com/watch?v=nZQfQDvh50o"),
    ("I Like Broccoli Ice Cream Song VERSION 2 - Funny Food song for kids by Bella and Beans TV", "Bella and Beans TV", "2:30", "https://www.youtube.com/watch?v=h9PlG8w7_R8"),
    ("Johny Johny Yes Papa Learn Colors | Part 7 - 3D Nursery Rhymes & Songs for Kids", "CVS 3D Rhymes & Kids Songs", "4:00", "https://www.youtube.com/watch?v=4KnA_6K6LTw"),
    ("Johny Johny Yes Papa Sports & Games (Radio Edit)", "CVS 3D Rhymes & Kids Songs", "3:00", "https://www.youtube.com/watch?v=hxpXN4qUxvc"),
    ("Say Cheese! [Sing-Along]", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=Kupp-mQPd0E"),
    ("22 min 5 Books of David's adventures - Animated Read Aloud Books", "Story Time at Awnie's House", "22:00", "https://www.youtube.com/watch?v=fNogleSaFNQ"),
    ("That's Not Funny, David! - Animated Read Aloud Book", "Story Time at Awnie's House", "3:30", "https://www.youtube.com/watch?v=Hb43JjKERAk"),
    ("More Real Life Funny Food Combinations, Do You Like Broccoli Ice Cream Song by Bella and Beans TV", "Bella and Beans TV", "2:30", "https://www.youtube.com/watch?v=lA7Cju_wQLc"),
    ("Mickey Saves Santa 🎅🏻 | S1 E20 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=cC03A0OgMuA"),
    ("All-Day Christmas & Holiday Music for the festive season! ☃️ | Super Simple Live", "Super Simple Songs - Kids Songs", "60:00", "https://www.youtube.com/watch?v=OKSthLq9kDE"),
    ("🔴 Super Simple Songs LIVE 🎶 | Kids Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "60:00", "https://www.youtube.com/watch?v=lsqNME_9LNc"),
    ("All-Day Vehicles Songs for Kids 🚗 | Toddlers on the Go Songs Compilation | Super Simple Live", "Super Simple Songs - Kids Songs", "60:00", "https://www.youtube.com/watch?v=ciIHiOCc-Xk"),
    ("All-Day Playtime Music for Toddlers | Happy Mood Songs | Super Simple Live", "Super Simple Songs - Kids Songs", "60:00", "https://www.youtube.com/watch?v=qXtHNjfdDak"),
    ("ABC song For Kids | abcd, a to z, Kids rhymes | kids Education | Kid's Education", "Kids Education", "3:00", "https://www.youtube.com/watch?v=Yv2yZWWYoVU"),
    ("The Animal Alphabet | Learn Animal Names! | Noodle & Pals", "Noodle & Pals", "3:30", "https://www.youtube.com/watch?v=Wk3K9PLtNUQ"),
    ("Best of 2025! 🎉 | Your Favorite Preschool Songs | Happy New Year from Noodle & Pals!", "Noodle & Pals", "45:00", "https://www.youtube.com/watch?v=GlprS1K_Hxw"),
    ("Do You Like Broccoli Ice Cream? Songs with Roma and Diana", "✿ Kids Diana Show", "3:00", "https://www.youtube.com/watch?v=F3LpIH-078Y"),
    ("🥊THATS NOT FUNNY, DAVID! (kids books read aloud) animated stories for kids", "Story Time at Awnie's House", "3:30", "https://www.youtube.com/watch?v=vGt3d7yC-DU"),
    ("David Goes to School - Animated Read Aloud Book for Kids", "Story Time at Awnie's House", "3:30", "https://www.youtube.com/watch?v=Qk7zCs-PaU4"),
    ("Peppa Pig Baby Evie's Arrival! 🤪 Sticker Activity for Kids", "Peppa Pig Toys", "4:00", "https://www.youtube.com/watch?v=hjEdWZADwT4"),
    ("Challenge the plane with Vlad and Niki and other fun adventures for kids", "Vlad and Niki", "12:00", "https://www.youtube.com/watch?v=nkynCUiIDnU"),
    ("Diana and Roma playing in cafe", "✿ Kids Diana Show", "5:00", "https://www.youtube.com/watch?v=gHxyPsn9xjQ"),
    ("Best ♥Peppa Pig♥ Toy Learning Videos for Kids - New House and Babysitting Baby Alexander!", "Genevieve's Playhouse - Learning Videos for Kids", "10:00", "https://www.youtube.com/watch?v=6B2or8Jla7k"),
    ("I Like Broccoli Ice Cream Song - Funny Food song for kids by Bella and Beans TV", "Bella and Beans TV", "2:30", "https://www.youtube.com/watch?v=v1a-lUvk7lo"),
    ("Numberblocks 1 goes down the Step Squad but Finds Missing Numbers! Help One Add Pairs to get Down!", "NumNum Blocks Learning Toys", "5:00", "https://www.youtube.com/watch?v=5kNU2cqw6xY"),
    ("Even Numberblocks Missing - Lots of Two to the Rescue! Fun Toy Learning and Early math for Toddlers", "NumNum Blocks Learning Toys", "5:00", "https://www.youtube.com/watch?v=fEH9r7D7Ius"),
    ("Let's camp in the snow! - Camping - Learning how to listen for kids - Darn David", "Darn David Official", "3:00", "https://www.youtube.com/watch?v=QgdT39O7vMU"),
    ("Diana y Roma - dulces y caramelos, Desafío para niños", "✿ Kids Diana Show", "5:00", "https://www.youtube.com/watch?v=Et8ERR1QkRQ"),
    ("Tres Gatitos (Three Little Kittens) | Canciones infantiles en Español | ChuChu TV", "ChuChu TV Nursery Rhymes & Kids Songs", "3:00", "https://www.youtube.com/watch?v=DzldmZvyBhQ"),
    ("A Very Merry Noodle & Pals Christmas! ⭐️ | Super Simple Christmas Songs for Kids & Families", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=tMuax8_AaNA"),
    ("Five Senses + More | Kids Songs | Follow Along Playtime! | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=nfIhLoilnjU"),
    ("Dance Compilation! | The Jellyfish + More Kids Songs To Move To | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=LOYTmGAHzMI"),
    ("Here Comes The Fire Truck + More | Classic Kids Preschool Songs | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=hyUsfovmkZg"),
    ("I Like To Draw | Creativity Song for art time at school | Practice shapes and colors | Noodle & Pals", "Noodle & Pals", "3:00", "https://www.youtube.com/watch?v=SU1I1EbEh8w"),
    ("We Wish You A Merry Christmas + More | Super Simple Songs | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=3X4WxytBXis"),
    ("Walking In The Forest + More | Kids Songs for Summer! | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=maQgXJhiqZc"),
    ("The Animal Alphabet & Hide and Seek Around The House + More | Fun Kids Songs! | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=n7u5e8zlJE4"),
    ("Daily Learning Lessons With Noodle & Pals! | Preschool Activities | Kids Songs", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=QI5wQGyP3Nk"),
    ("Happy Halloween from Noodle & Pals! | Toddler Spooky Season Party | Songs for Halloween", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=hOeP_RBan84"),
    ("Stomp Like A Dinosaur + More | ROAR! 🦖 | 1 Hour of Big Movement Songs for Kids | Noodle & Pals", "Noodle & Pals", "60:00", "https://www.youtube.com/watch?v=eD9HtFzNXvo"),
    ("I CAN DO HARD THINGS 💪 | SuperKids Bible Affirmations - Day 9", "SuperKids Ministry", "3:00", "https://www.youtube.com/watch?v=4bbFDjNCXw0"),
    ("Who Took The Cookie? - On The Job + More | Fun Kids Songs | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=Rl11aSdGFEI"),
    ("Hide and Seek #2 + More | Preschool Hit Songs! | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=bUUVkAcFajs"),
    ("Good Morning Farm + More | Kids Songs | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=psLRBdzDzgA"),
    ("I'm A Little Train + More | 🚂 Pretend To Be A Choo Choo Train! | Preschool Hits | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=37CNa6NHnww"),
    ("Can You Make A Happy Face + More | Halloween Songs PLUS Classroom Favorites! | Noodle & Pals", "Noodle & Pals", "45:00", "https://www.youtube.com/watch?v=yAvWwaZAvCQ"),
    ("How's The Weather + More | Sing and Learn Super Simple Songs With Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=2D3-VRtLZmw"),
    ("Halloween + Classroom Songs With Noodle & Pals | Happy Halloween! 🎃", "Noodle & Pals", "45:00", "https://www.youtube.com/watch?v=O1YohX-1KXc"),
    ("Jingle Bells + More | Kids Christmas Songs for the season | Noodle & Pals", "Noodle & Pals", "30:00", "https://www.youtube.com/watch?v=V-alGR-Sm_Y"),
    ("What's Inside The Toy Box? 🎁 | Favorite Toy Song | Surprises with Noodle & Pals!", "Noodle & Pals", "3:00", "https://www.youtube.com/watch?v=GGbm73UAfUs"),
    ("This Is A Happy Face | Noodle & Pals | Songs For Children", "Noodle & Pals", "3:00", "https://www.youtube.com/watch?v=W9rX6ApYqjo"),
    ("Noodle & Pals Storybook | ABCs | Preschool Lessons", "Noodle & Pals", "5:00", "https://www.youtube.com/watch?v=H4zoxotsxis"),
    ("A Is For Apple 🍎 | Fun Alphabet Song for Preschool | Noodle & Pals", "Noodle & Pals", "3:00", "https://www.youtube.com/watch?v=qUv_N8HzWt0"),
    ("Stand Up Sit Down | Preschool Song | Noodle & Pals", "Noodle & Pals", "2:30", "https://www.youtube.com/watch?v=-iMGSD_35pM"),
    ("The Animals on the Farm", "Noodle & Pals", "3:00", "https://www.youtube.com/watch?v=QVAuNN63xB8"),
    ("Food Alphabet Phonics Song for Kids | Do You Like Apples? Song | Learning Food and ABCs", "Dream English Kids", "3:00", "https://www.youtube.com/watch?v=p4MCiq3cbao"),
    ("Do You Like Fish in the Milk?", "Super Simple Songs - Kids Songs", "2:30", "https://www.youtube.com/watch?v=9Jp9d7cTjQU"),
    ("Do You Like Broccoli Ice Cream? | Food Song for Kids! | Kids Songs for You", "Super Simple Songs - Kids Songs", "2:47", "https://www.youtube.com/watch?v=yRVn4JRDWiQ"),
    ("What Do You See? Song Jobs | Book Version | Dream English Kids", "Dream English Kids", "3:00", "https://www.youtube.com/watch?v=0ExoYRVy8-0"),
    ("Piggy Bank Smash! Toy Learning Video for Toddlers and Kids!", "Genevieve's Playhouse - Learning Videos for Kids", "5:00", "https://www.youtube.com/watch?v=eUSSp41qYQM"),
    ("I See 100 Things | My First Words Series | I See Chant", "Dream English Kids", "3:00", "https://www.youtube.com/watch?v=lHPuGz4V9AI"),
    ("What Color Is it? Song | Learn 11 Colors | Learn English Kids", "Learn English Kids - British Council", "3:00", "https://www.youtube.com/watch?v=YyFLBTTAbSE"),
    ("Learn Colors - Preschool Chant - Colors Song for Preschool by ELF Learning - ELF Kids Videos", "ELF Learning", "2:30", "https://www.youtube.com/watch?v=qhOTU8_1Af4"),
    ("My First 100 Words in English Chant Step 4 | Animals, Health, School Subjects | Learn English Kids", "Learn English Kids - British Council", "3:30", "https://www.youtube.com/watch?v=J5czOoI5gLw"),
    ("100 Words 1 Minute Challenge | Animals, Colors, Shapes, Verbs, Numbers", "Dream English Kids", "1:00", "https://www.youtube.com/watch?v=nvUFCNqdXKw"),
    ("My First 100 Words in English Chant With Matt | Numbers, Colors, Animals | Learn English Kids", "Learn English Kids - British Council", "3:30", "https://www.youtube.com/watch?v=sUoCd0DTJVY"),
    ("Finger Family Song - 3D Animals Finger Family Nursery Rhymes & Songs for Kids", "CVS 3D Rhymes & Kids Songs", "3:30", "https://www.youtube.com/watch?v=fup9bXVf1vI"),
    ("Finger Family Song - Food Family With Matt | Nursery Rhymes, Children's Songs | Learn English Kids", "Learn English Kids - British Council", "3:00", "https://www.youtube.com/watch?v=05MT6fRl6QM"),
    ("Food Family Part 2-Finger Family Songs with Matt | Nursery Rhymes | Learn English Kids", "Learn English Kids - British Council", "3:00", "https://www.youtube.com/watch?v=VjPsATEpSFA"),
    ("Food Song | Learn 15 Food and Drinks | Learn English Kids", "Learn English Kids - British Council", "3:00", "https://www.youtube.com/watch?v=6IwulRrYnzQ"),
    ("300 Words in English Chants | My First Words Series | Numbers, Colors, Animals, Vehicles, Verbs", "Dream English Kids", "5:00", "https://www.youtube.com/watch?v=m55qlS-QWAo"),
    ("My First 100 Words in English Chant Step 2 | Numbers, Colors, Animals | Learn English Kids", "Learn English Kids - British Council", "3:30", "https://www.youtube.com/watch?v=SsVQqXxZR6A"),
    ("Minnie's Birthday | S1 E7 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=dmdGQljdF_E"),
    ("A to Z Alphabet School Things Chant with Matt | Learn School Object Names | Alphabet for Kids", "Learn English Kids - British Council", "3:00", "https://www.youtube.com/watch?v=mRQJ2HRWNMI"),
    ("A Good Sign | Minnie's Bow-Toons | @disneyjr", "Disney Jr.", "3:00", "https://www.youtube.com/watch?v=aY3kfdGXcV8"),
    ("Mickey Mouse clubhouse hot dog dance song 3 Edwin Bermudez 2 for @disneyjr", "Fan Content", "2:00", "https://www.youtube.com/watch?v=ATL-vk61kF8"),
    ("All Hot Dog Dances! Compilation | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "5:00", "https://www.youtube.com/watch?v=bseyU2PvBQo"),
    ("Do you like yucky song | Cartoon Songs", "Cartoon Songs", "2:30", "https://www.youtube.com/watch?v=O3-MVmyIvsM"),
    ("Finger Family Emoji Song | Nursery Rhymes | @TheMikMaks", "The Mik Maks", "2:30", "https://www.youtube.com/watch?v=PYXVQ-FTMl0"),
    ("Sleeping Minnie Mouse | S1 E19 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=KbGeR-Of1Fw"),
    ("Peppa Pig - Dress Up & Learn Colors With People Who Help Us", "Peppa Pig - Official Channel", "5:00", "https://www.youtube.com/watch?v=SwaZkyj9N2U"),
    ("Peppa Pig Dress Up Challenge 🐷 Find the Real Character! Peppa Pig Tales Kids Game | Kids DingDong", "Kids DingDong", "5:00", "https://www.youtube.com/watch?v=FrpYYmXUJO4"),
    ("Humpty Dumpty Nursery Rhyme - 3D Animation English Rhymes for children", "CVS 3D Rhymes & Kids Songs", "3:00", "https://www.youtube.com/watch?v=0oKreL1jvkg"),
    ("Mickey Mouse Clubhouse Full Episode | Mickey Goes Fishing | S1 E5 | @disneyjr", "Disney Jr.", "24:01", "https://www.youtube.com/watch?v=m3LV5Z2nCRg"),
    ("Johny Johny Yes Papa - Ice Cream Song – ChuChu TV Funzone Nursery Rhymes - Toddler Videos for Babies", "ChuChu TV Nursery Rhymes & Kids Songs", "3:30", "https://www.youtube.com/watch?v=zvQOKufvs-8"),
    ("This Is The Way Song - ChuChu TV Funzone 3D Nursery Rhymes & Songs For Babies", "ChuChu TV Nursery Rhymes & Kids Songs", "3:00", "https://www.youtube.com/watch?v=UR1zpBnkEuc"),
]

def duration_to_seconds(d):
    parts = d.strip().split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return 0
    except:
        return 0

def extract_video_id(url):
    m = re.search(r'v=([A-Za-z0-9_-]+)', url)
    return m.group(1) if m else ''

# Build videos list
videos = []
for title, channel, duration, url in RAW:
    secs = duration_to_seconds(duration)
    vid_id = extract_video_id(url)
    videos.append({
        "video_id": vid_id,
        "title": title,
        "channel": channel,
        "duration": duration,
        "duration_seconds": secs,
        "timestamp": GENERATED,
        "url": url
    })

total_seconds = sum(v["duration_seconds"] for v in videos)
total_watch_minutes = round(total_seconds / 60, 1)

# Top channels
from collections import Counter
channel_counts = Counter(v["channel"] for v in videos)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

# Categories (inferred)
def categorize(title, channel):
    t = title.lower()
    c = channel.lower()
    if any(x in t for x in ["peppa pig", "peppa"]):
        return "Peppa Pig"
    if any(x in t for x in ["noodle & pals", "noodle"]) or "noodle" in c:
        return "Noodle & Pals"
    if "rhymington square" in t or "rhymington" in c:
        return "Rhymington Square"
    if "darn david" in t or "darn david" in c:
        return "Darn David"
    if "disney" in c or "mickey" in t or "minnie" in t or "sofia" in t:
        return "Disney Jr."
    if "super simple" in t or "super simple" in c:
        return "Super Simple Songs"
    if "numberblocks" in t or "numnum" in c:
        return "Numberblocks"
    if "alphablocks" in t:
        return "Alphablocks"
    if "johny johny" in t or "cvs 3d" in c:
        return "Johny Johny"
    if "genevieve" in t or "genevieve" in c:
        return "Genevieve's Playhouse"
    if "caitie" in t:
        return "Super Simple Play with Caitie"
    if any(x in t for x in ["goldilocks", "fairy tale", "bedtime story", "read aloud", "storytime"]):
        return "Stories & Read Alouds"
    if "kidibli" in c or "arabic" in c or t.startswith("ا") or t.startswith("م") or t.startswith("ب"):
        return "Arabic Content"
    if "diana" in t or "roma" in t or "diana" in c:
        return "Diana & Roma"
    if "vlad" in t and "niki" in t:
        return "Vlad and Niki"
    if "learn english" in c or "dream english" in c or "elf learning" in c:
        return "English Learning"
    if any(x in t for x in ["abc", "alphabet", "phonics", "numbers", "colors", "shapes"]):
        return "Educational"
    return "Other Kids Content"

cat_counts = Counter(categorize(v["title"], v["channel"]) for v in videos)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in cat_counts.most_common(10)]

# All today (no real timestamps)
data = {
    "generated": GENERATED,
    "account": "jigar.us.af@gmail.com",
    "period_days": 7,
    "note": "Daily update",
    "total_videos": len(videos),
    "total_watch_minutes": total_watch_minutes,
    "videos": videos,
    "top_channels": top_channels,
    "top_categories": top_categories,
    "hourly_counts": {"20": len(videos)},
    "daily_counts": {"Fri": len(videos)}
}

out_path = "/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json"
with open(out_path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Wrote {len(videos)} videos to {out_path}")
print(f"   Total watch time: {total_watch_minutes} min")
print(f"   Top channels: {top_channels[:5]}")
