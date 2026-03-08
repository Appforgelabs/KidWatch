#!/usr/bin/env python3
"""Parse YouTube history text content and build history.json"""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict

# Raw text lines from YouTube history page
RAW_TEXT = """Skip navigation
Create
Home
Shorts
Subscriptions
You
Watch history
All
Videos
Shorts
Podcasts
Music
Today
8:19
Logo Sound Quiz Cartoons 🎵 | Guess the Cartoon Channel Logo Sound Disney, CoComelon, Cartoon Network
ZIZOQUIZ
•
11K views
8:02
Guess the Kids Streaming Logo Sound 🎵📺 – Fun Cartoon & Educational Channel Quiz! 2026
ZIZOQUIZ
•
5K views
8:03
Guess The Kids TV Logo Sound 🔊 | BabyTV, CBeebies, PBS Kids, YouTube Kids & More Preschool Quiz 2026
ZIZOQUIZ
•
46K views
16:59
Guess The Logo Sound 🔥🔊 McDonald's, Tiktok, Netflix, Pepsi | Logo Quiz 2025
Quiz Rainbow
•
16M views
8:12
Guess The Educational Logo Sound!🔊📚 | BabyBus, Pinkfong, ABCmouse & More
ZIZOQUIZ
•
1.5K views
8:02
Guess The Early Learning App Logo Sound 🔊 | ABCmouse, Duolingo ABC, Khan Academy Kids & More 2026 🎵
ZIZOQUIZ
•
19K views
8:15
Guess the Logo Sound – Kids Learning Apps Quiz 🎵 | Fun Educational Sound Quiz for Kids 2026
ZIZOQUIZ
•
2.4K views
8:02
Guess the Logo Sound Challenge! 🔊You Hear These Every Day But Cant Name Them! 99% Fail
ZIZOQUIZ
•
464 views
5:53
.ೃ࿔ My afternoon routine at home🧺🧴| self care, cooking & home reset 🌸🤍✨ #avatarworld #pazu
Lili's diary🧸𐙚
•
63K views
10:01
Morning Routine In Our NEW HOUSE 🌤️ (EP 16) | Toca Life World Family RP 🌍
It's Nora
•
204K views
10:51
Single mom with twins aesthetic night routine ~ *WITH VOICE* Toca boca roleplay
Toca kitty
•
1.1M views
6:11
Cozy morning routine with Lili & Ben⛅️🧺🥯| Avatar world #avatarworld #pazu
Lili's diary🧸𐙚
•
194K views
8:29
⋆˚࿔ My Morning Routine🧋⛅️ | Pilates Class & Market run 🛒🥥#avatarworld #pazu
Lili's diary🧸𐙚
•
302K views
19:21
First day of school! 🏫 *GONE WRONG* (WITH VOICE) || Toca Boca Roleplay
Toca kitty
•
1.3M views
15:28
First day of kindergarten!! 🐯🍎 *WITH VOICE* II Toca boca Roleplay
Toca kitty
•
2.8M views
9:05
The Waterpark ACCIDENT! 🌊| With Voice 🔈 | Toca Life World Roleplay
It's Nora
•
726K views
12:44
The sleepover! *GONE WRONG* (WITH VOICE) II Toca boca roleplay
Toca kitty
•
5.8M views
10:56
Good Kid Vs Bad Kid! Which Are You?! Melody Kuromi 😈👀 Toca Life World | Toca Life Story | Toca Boca
CandyCute Channel
•
189K views
11:10
Good Babysitter VS Bad Babysitter 🍼😈 Sad Story | Toca Life Story | Toca Boca | Toca Life World
CandyCute Channel
•
862K views
10:47
Bad Daughter VS Good Daughter👧🏻😈🩷 Toca Life World | Toca Life Story | Toca Boca
CandyCute Channel
•
817K views
27:46
Rich School Teacher vs Broke School Teacher! Who's Better? | Toca Life Story | Toca Boca
Toca Moca and Toca Avatar Love
•
1.6M views
12:08
Big family aesthetic morning routine 🪴☀️ *WITH VOICE* || Toca boca Roleplay
Toca kitty
•
2.7M views
11:24
single mom with twins fall aesthetic morning routine 🤍 *WITH VOICE* II Toca boca roleplay
Toca kitty
•
1M views
12:33
Working at a bakery! (GONE WRONG) *WITH VOICE* || Toca boca roleplay
Toca kitty
•
2.1M views
16:18
Working as a babysitter! (GONE WRONG) *WITH VOICE* || Toca Boca Roleplay
Toca kitty
•
1.8M views
9:51
Good Mom VS Bad Mom 😭👱🏻‍♀️❤️ Avatar World | Toca Boca | Toca Life Story
Wendy Сandy
•
1.2M views
12:23
Good Student VS Bad Student 🌙 Night Routine | Toca Boca Life Story
CandyCute Channel
•
1.8M views
2:53
★•Rainy Night Routine 🚿🌧🧺(asmr) |living alone| @avatarworldbypazu
𖦹Adelinite
•
285K views
6:46
My Night routine as a Teacher 👩🏼‍🏫🌙 | Avatar World
isa world
•
1.9M views
8:33
Cozy snowy day routine☃️🧸✨ Relaxing Avatar world video🧺🧡
Lili's diary🧸𐙚
•
20K views
2:06
Phonics Song 3
KidsTV123
•
91M views
2:42
Phonics Song
KidsTV123
•
413M views
1:34
♪♪ Funny Animal Song | When Hedgehogs Kiss | Hooray Kids Songs & Nursery Rhymes | Love
Hooray Kids Songs & Nursery Rhymes
•
7M views
2:11
Get well soon children's song | Soon you will be fit again - Hooray kids songs & nursery rhymes
Hooray Kids Songs & Nursery Rhymes
•
35M views
2:47
Children's song Have a Haircut - Children at the Hairdresser | Hooray Kids Songs & Nursery Rhymes
Hooray Kids Songs & Nursery Rhymes
•
8.1M views
6:06
ASMR UNBOXING Ms RACHEL WOODEN SONG PUZZLE
C0C0 Cadz
•
1.9M views
15:24
Four Pete the Cat Books - By Eric Litwin | Kids Book Sing/Read Aloud - Learn To Read
Vienna's View - Toddler Learning Videos
•
956K views
2:22
Pete The Cat I Love My White Shoes
KB00KIE
•
363K views
4:54
The Rings of Unity - Full Episode | Series 8 E29 | Numberblocks
Numberblocks
•
321K views
14:12
New Words for Toddlers | House and Home Sounds | Phonics with Dee | Yakka Dee!
Yakka Dee! – Toddler Learning
•
19M views
5:39
Let's read together a Peppa Pig book. The BIGGEST Muddy Puddle in the World. Read along.
We are book buddies
•
57K views
4:29
Learn With Peppa Pig: Peppa Explores Space (Read Aloud) | Read Along With Millie's Mummy
Read Along With Millie's Mummy
•
266 views
5:06
Peppa pig Peppa loves doctors and nurses
Happily ever after storytime
•
854 views
3:00
Peppa Pig and the Easter Rainbow
KB00KIE
•
136K views
2:01
Bath Time Song | More Nursery Rhymes & Kids Songs
Peppa Pig - Nursery Rhymes and Kids Songs
•
26M views
1:37
Kids Music with Cool Musical Instruments!
Joe Porter
•
84M views
10:01
Aesthetic FAMILY FRIDGE RESTOCK! 🍎 (EP 9) | Toca Life World Family Roleplay 🌍
It's Nora
•
343K views
10:09
Our Family Goes TO WALMART 🛒 (EP 8) | Toca Life World Family Roleplay 🌍
It's Nora
•
580K views
1:05
Theme Song! 🎶| Yakka Dee!
Yakka Dee! – Toddler Learning
•
5M views
51:24
Let's Yakka Yak with Dee! | Yakka Dee Marathon! ⭐️
Yakka Dee! – Toddler Learning
•
10M views
0:57
Yakka Dee Theme Tune! | CBeebies
CBeebies
•
460K views
28:21
Morning routine !!! new role-play !!!!! Toca Boca role-play !!!!!! with voice !!!!!
Toca tot
•
662K views
4:30
Peppa Pig in Avatar World VS Toca World | George Catches a Cold 😰
Dino Avatar
•
205K views
0:07
Sad cheesey noodle and pals remake kinemaster speed speedrun logo be like
Варвара Краса
•
1.4K views
14:17
Let's Talk About Clothes! | Yakka Dee!
Yakka Dee! – Toddler Learning
•
5.5M views
8:02
Let's Talk About the Body! | Yakka Dee!
Yakka Dee! – Toddler Learning
•
43M views
15:41
Let's Talk about Things in the Kitchen ☕️ | Yakka Dee!
Yakka Dee! – Toddler Learning
•
20M views
7:07
Let's Talk about Animals that Swim! | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.2M views
14:08
Let's Talk about Travel! | Yakka Dee!
Yakka Dee! – Toddler Learning
•
4.9M views
30:10
Toddler Learning with Dee | Learn Farm, Zoo and Pet Animals | Lern to Talk | Yakka Dee!
Yakka Dee! – Toddler Learning
•
14M views
1:54
Can you say Digger? 🧱 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
26M views
8:55
BRAND NEW! Yakka Dee: Dee's Food Party! 🍕 🍦 | Toddler Words | Yakka Dee!
Yakka Dee! – Toddler Learning
•
26K views
8:55
BRAND NEW! Yakka Dee: What Can You See? | Farm Friends! 🐮🐴 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
185K views
3:02
BRAND NEW! Yakka Dee: What Can You See? | Christmas 🎄 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
276K views
3:02
BRAND NEW! Yakka Dee: What Can You See | Halloween 🎃 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
525K views
31:55
Dee's Mega Song Marathon | Yakka Dee!
Yakka Dee! – Toddler Learning
•
826K views
4:06
What Pet Should I Get? by Dr. Seuss | READ ALOUD for Kids
Little Cozy Nook
•
2.4M views
12:17
Autumn Animals 🍂 | Let's Learn with Yakka Dee| BBC Kids
BBC Kids
•
45K views
25:31
Can You Say... Nose, Bird, Bath, Monkey, Bubble | Learn with Yakka Dee! | FULL EPISODES | BBC Kids
BBC Kids and Yakka Dee! – Toddler Learning
•
16K views
25:28
Can You Say... Feet, Goat, Key, Flower, Kite | Learn with Yakka Dee! | FULL EPISODES | BBC Kids
BBC Kids and Yakka Dee! – Toddler Learning
•
53K views
25:29
Can You Say... Ball, Mouse, Beans, Car, Bed | Learn with Yakka Dee! | FULL EPISODES | BBC Kids
BBC Kids and Yakka Dee! – Toddler Learning
•
31K views
12:44
Learn Transport Words! | Toddler Learning | Car, Bike, Plane + more! | Yakka Dee!
Yakka Dee! – Toddler Learning
•
6.2M views
20:15
Learn Transport words with Dee! | Car, Bus + more! | BBC Kids
BBC Kids
•
153K views
2:11
Can you say Toothbrush? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
12M views
3:56
The Colorbubblies Song
KidsTV123
•
48M views
2:22
Colors Song 2
KidsTV123
•
44M views
1:56
Can You Say Book? 📚| Yakka Dee!
Yakka Dee! – Toddler Learning
•
703K views
1:55
Can You Say Beans? 🍽| Yakka Dee!
Yakka Dee! – Toddler Learning
•
21M views
2:54
Phonics Song 2 (new version)
KidsTV123
•
155M views
38:29
Garden Party Words! | Duck, Strawberry, Cloud | Yakka Dee!
Yakka Dee! – Toddler Learning
•
592K views
1:18:26
Learn New Words! | Star, Kite, Pasta | Yakka Dee!
Yakka Dee! – Toddler Learning
•
555K views
25:32
Can You Say... Hat, Peas, Bus, Cup, Duck | Learn with Yakka Dee! | FULL EPISODES | Yakka Dee!
Yakka Dee! – Toddler Learning
•
110K views
30:47
Scary Words 👻 | 30+ Minutes | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.4M views
27:41
Smiles All Around 💛 | Learn Happy Words | 20+ Minutes | Yakka Dee!
Yakka Dee! – Toddler Learning
•
537K views
2:03
Can You Say Rain? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.6M views
2:11
Can you say Hedgehog? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1M views
1:55
Can You Say Lion? 🦁| Yakka Dee!
Yakka Dee! – Toddler Learning
•
4.8M views
1:53
Can you say Train?🚂 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.7M views
1:53
Can you say Rocket? 🚀 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.6M views
1:53
Can You Say Apple? 🍎| Yakka Dee!
Yakka Dee! – Toddler Learning
•
30M views
1:56
Can You Say Peas? 💚| Yakka Dee!
Yakka Dee! – Toddler Learning
•
3.8M views
10:31
Transport words with Dee 🚂✈️ | Learn Travel Phonics | Trains, Bus and Bicycle words | Yakka Dee!
Yakka Dee! – Toddler Learning
•
624K views
4:53
TUBBY | Leslie Patricelli | TODDLER CONCEPTS | #storytime #parenting #esl #toddler #preschool #kids
Read Aloud Edu
•
205K views
1:44:48
🔴LIVE: The BEST of Series 2 | Yakka Dee
Yakka Dee! – Toddler Learning
•
961K views
31:30
Peppa Pig Takes Funny Pictures In The Photo Booth | Kids TV And Stories
Peppa Pig's Big Adventures
•
8M views
3:02
BRAND NEW! Yakka Dee: What Can You See? | Bedroom 🧸📚 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
146K views
LIVE
🔴 LIVE: Common Words with Dee! | Food Words for Toddlers | Yakka Dee!
Yakka Dee! – Toddler Learning
•
29 watching
10:59:42
🔴LIVE: Learning Marathon for Toddlers! | Explore new words and Sounds with Dee | Yakka Dee!
Yakka Dee! – Toddler Learning
•
970K views
14:27
Water Words for Toddlers | Bubble, Whale & More | Yakka Dee!
Yakka Dee! – Toddler Learning
•
9.4M views
45:50
Alphabet Marathon (A-Z) Words and Letters | Yakka Dee!
Yakka Dee! – Toddler Learning
•
856K views
12:11
Explore Winter With Dee! ❄️ | Toddler Words | Yakka Dee!
Yakka Dee! – Toddler Learning
•
268K views
25:24
Can You Say... Bed, Car, Beans, Mouse, Ball | Learn with Yakka Dee! | FULL EPISODES | Yakka Dee!
Yakka Dee! – Toddler Learning
•
126K views
3:02
BRAND NEW! Yakka Dee: What Can You See? | Bathroom 🦷 🫧 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
126K views
2:09
Can you say Van? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.3M views
2:06
Can you say Lemon? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.7M views
1:46
Can You Say Hair? 💇‍♀️| Yakka Dee!
Yakka Dee! – Toddler Learning
•
705K views
1:54
Can You Say Whale? 🐳| Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.6M views
1:48
Can You Say Cat? 🐈 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
3M views
1:49
Can You Say Bag? 👜 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
684K views
2:09
Can You Say Nose? 👃| Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.9M views
1:54
Can you say Donkey?🐴 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1M views
1:51
Can You Say Strawberry? 🍓 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
615K views
2:12
Can you say Bread? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.4M views
2:10
Can you say Cheese? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.4M views
2:12
Can you say Scooter? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1M views
2:10
Can you say Octopus? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.7M views
2:08
Can you say Spider? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.4M views
2:15
Can you say Blanket? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
4.4M views
1:50
Can You Say Orange? 🍊 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
406K views
1:50
Can You Say Pumpkin? 🎃 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
515K views
1:53
Can you say Raspberry? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
999K views
2:11
Can you say Grass? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.1M views
1:49
Can You Say Hand? 🖐️ | Yakka Dee!
Yakka Dee! – Toddler Learning
•
810K views
2:05
Can you say Bed? 🛌 💤 | Yakka Dee
Yakka Dee! – Toddler Learning
•
2.6M views
1:44
Yakka Dee - Book
CBeebies Asia
•
1.3M views
0:37
Yakka Dee - Top
CBeebies Asia
•
1.4M views
1:34
Yakka Dee Series 4 | Episode 2 | CBeebies
CBeebies Asia
•
478K views
1:48
Can You Say Chair? 🪑| Yakka Dee
Yakka Dee! – Toddler Learning
•
563K views
1:55
Can You Say Boots? 👢| Yakka Dee!
Yakka Dee! – Toddler Learning
•
634K views
1:54
Can you say Coat? 🧥 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
871K views
1:55
Can you say Top?👚| Yakka Dee!
Yakka Dee! – Toddler Learning
•
1M views
1:56
Can you say Shoes?🥾 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1M views
1:56
Can You Say Cup? 🥛| Yakka Dee!
Yakka Dee! – Toddler Learning
•
6.1M views
1:53
Can You Say Mouse? 🐭| Yakka Dee!
Yakka Dee! – Toddler Learning
•
649K views
1:57
Can You Say Bird? 🦜| Yakka Dee!
Yakka Dee! – Toddler Learning
•
745K views
1:58
Can You Say Monkey? 🐒| Yakka Dee!
Yakka Dee! – Toddler Learning
•
918K views
1:52
Can You Say Bath? 🛁| Yakka Dee!
Yakka Dee! – Toddler Learning
•
3.6M views
1:53
Can you say Swing? 😃 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
11M views
1:54
Can You Say Bus? 🚌| Yakka Dee!
Yakka Dee! – Toddler Learning
•
4.6M views
1:58
Can You Say Dog? 🐶| Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.3M views
2:15
Can you say Pyjamas? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
879K views
2:13
Can you say Shorts? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
941K views
2:11
Can you say Sheep? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.2M views
1:52
Can you say Cow? 🐄 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
4.4M views
1:54
Can you say Fish? 🐟 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
6.3M views
2:08
Can you say Lizard? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
7.7M views
1:55
Can you say Egg?🥚 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.8M views
1:52
Can You Say Bowl? 🥣 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.4M views
2:10
Can you say Glasses? 👓 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.1M views
2:09
Can you say Pizza? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.2M views
2:12
Can you say Plate? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
860K views
2:09
Can you say Tractor? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2.6M views
2:23
♪ ♪ Funny Cat Song – Cat Toilet | Hooray Kids Songs & Nursery Rhymes | Funny Animal Songs
Hooray Kids Songs & Nursery Rhymes
•
19M views
1:53
Can you say Plane? ✈️ | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.3M views
1:55
Can you say Mango? 🥭 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.3M views
1:52
Can You Say Flower? 🌺| Yakka Dee!
Yakka Dee! – Toddler Learning
•
611K views
1:51
Can You Say Kite? 🎏 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
685K views
1:53
Can You Say Key? 🔑| Yakka Dee!
Yakka Dee! – Toddler Learning
•
937K views
1:53
Can you say Milk?🍼 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.6M views
8:55
BRAND NEW! Yakka Dee: What Can You See? | Explore With Dee! 🔍 💚 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
90K views
13:59
Yakka Dee Transport!🚦| Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.7M views
1:41
Yakka Dee - Banana
CBeebies Asia
•
39M views
2:08
Can you say Juice? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
900K views
2:13
Can You Say Chicken 🐥 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.1M views
1:57
Can You Say Worm? 🐛| Yakka Dee!
Yakka Dee! – Toddler Learning
•
8.6M views
1:51
Can You Say Elf | Yakka Dee!
Yakka Dee! – Toddler Learning
•
297K views
1:50
Can You Say Skin? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
861K views
1:48
Can You Say Ear?👂 | Yakka Dee
Yakka Dee! – Toddler Learning
•
504K views
1:54
Can You Say Tummy? 👕| Yakka Dee!
Yakka Dee! – Toddler Learning
•
136M views
1:51
Can you say Tiger?🐅 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.3M views
1:53
Can You Say Bee? 🐝| Yakka Dee!
Yakka Dee! – Toddler Learning
•
3.6M views
2:58
Peppa's Pop-Up Dragons🐉lift-the-flap book #readaloud #bedtimestories #kidsbooks #peppapig #storytime
Wonderfu1me
•
32K views
3:38
Peppa's Great DINOSAUR Hunt**A lift-the-flap Book**Bedtimestory☆ Reading aloud☆
Wonderfu1me
•
141K views
2:41
Peppa Loves Soft Play☆A lift-the-flap Book☆Bedtimestory☆ #story #bedtimestories #peppapig #readaloud
Wonderfu1me
•
50K views
4:27
Learn Characters, Vehicles and Colors with Ben & Holly, Peppa Pig, and other toys in box for Kids
BigBAMGamer
•
19M views
3:02
BRAND NEW! Yakka Dee: What Can You See? | Kitchen 🍞 🍏 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
49K views
45:42
Even More Yakka Dee! | Yakka Dee Marathon 3 ⭐️
Yakka Dee! – Toddler Learning
•
16M views
4:17
Peppa Pig Dress Up Color Game 🌈 Peppa Pig Tales Kids Quiz with Peppa Pig & Friends | Kids DingDong
Kids DingDong
•
100K views
11:37
Kids, let's Learn Common Words with Woodzeez Toy Dollhouse!
Genevieve's Playhouse - Learning Videos for Kids
•
136M views
1:50
Can You Say Tree? 🌳| Yakka Dee!
Yakka Dee! – Toddler Learning
•
715K views
1:54
Can you say Cake? 🍰 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.2M views
1:55
Can You Say Ball? ⚽️| Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.9M views
1:54
Can You Say House? 🏠| Yakka Dee!
Yakka Dee! – Toddler Learning
•
2M views
1:57
Can You Say Hat? 🎩| Yakka Dee!
Yakka Dee! – Toddler Learning
•
2M views
1:54
Can You Say Cloud? ☁️| Yakka Dee!
Yakka Dee! – Toddler Learning
•
863K views
3:59
Let's Dance with Dee! | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.9M views
10:59:38
🔴LIVE: Songs with Dee! | Fun songs for kids | Yakka Dee!
Yakka Dee! – Toddler Learning
•
389K views
20:14
Transport Marathon with Dee | Yakka Dee!
Yakka Dee! – Toddler Learning
•
7.1M views
2:02
Learn Amazing Insects and Bugs for Kids | Kids Learning Classroom
Kids Learning Classroom
•
6.6K views
2:10
Can you say Robot? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
3.5M views
2:13
We play Opposite Day - Children's song to play and join in | Hooray Kids Songs & Nursery Rhymes
Hooray Kids Songs & Nursery Rhymes
•
2.5M views
4:21
Jay Tries to Do Grown Up Jobs | Nikhil & Jay Kids Cartoons on BBC iPlayer
Nikhil & Jay
•
1.1K views
22:22
Can you say words beginning with S? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
2M views
11:17
Feelings with Leslie Patricelli 💛 | Toddler Read-Aloud Compilation | Emotions & Empathy
Hoots & Tales
•
336K views
14:33
Leslie Patricelli Opposites 📚 | Toddler Read-Aloud with Learning Reflections | Hoots & Tales
Hoots & Tales
•
1M views
2:09
Can you say Gloves? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.1M views
1:53
Can you say Drum?🥁 | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1.3M views
2:10
Can you say Fox? | Yakka Dee!
Yakka Dee! – Toddler Learning
•
1M views
21:37
Learn Common Household Words with Woodzeez and Bluey for Kids!
Genevieve's Playhouse - Learning Videos for Kids
•
114M views
1:51
Can You Say Alien | Yakka Dee!
Yakka Dee! – Toddler Learning
•
427K views"""

# URL data extracted from the page
URL_LIST = [
    {"title": "Logo Sound Quiz Cartoons 🎵 | Guess the Cartoon Channel Logo Sound Disney, CoComelon, Cartoon Network", "url": "https://www.youtube.com/watch?v=KNVMAc6JGEg"},
    {"title": "Guess the Kids Streaming Logo Sound 🎵📺 – Fun Cartoon & Educational Channel Quiz! 2026", "url": "https://www.youtube.com/watch?v=P1lDDH4O3qA"},
    {"title": "Guess The Kids TV Logo Sound 🔊 | BabyTV, CBeebies, PBS Kids, YouTube Kids & More Preschool Quiz 2026", "url": "https://www.youtube.com/watch?v=GYNPa7gpDNA"},
    {"title": "Guess The Logo Sound 🔥🔊 McDonald's, Tiktok, Netflix, Pepsi | Logo Quiz 2025", "url": "https://www.youtube.com/watch?v=FOxIbPL3CiY"},
    {"title": "Guess The Educational Logo Sound!🔊📚 | BabyBus, Pinkfong, ABCmouse & More", "url": "https://www.youtube.com/watch?v=A1R-5aMNs6A"},
    {"title": "Guess The Early Learning App Logo Sound 🔊 | ABCmouse, Duolingo ABC, Khan Academy Kids & More 2026 🎵", "url": "https://www.youtube.com/watch?v=YFd3Y7vyEI0"},
    {"title": "Guess the Logo Sound – Kids Learning Apps Quiz 🎵 | Fun Educational Sound Quiz for Kids 2026", "url": "https://www.youtube.com/watch?v=1sv9FlaVCSw"},
    {"title": "Guess the Logo Sound Challenge! 🔊You Hear These Every Day But Cant Name Them! 99% Fail", "url": "https://www.youtube.com/watch?v=xbcwTOrHcv8"},
    {"title": ".ೃ࿔ My afternoon routine at home🧺🧴| self care, cooking & home reset 🌸🤍✨ #avatarworld #pazu", "url": "https://www.youtube.com/watch?v=MSEZEem7E6s"},
    {"title": "Morning Routine In Our NEW HOUSE 🌤️ (EP 16) | Toca Life World Family RP 🌍", "url": "https://www.youtube.com/watch?v=mjoq17Pbhuk"},
    {"title": "Single mom with twins aesthetic night routine ~ *WITH VOICE* Toca boca roleplay", "url": "https://www.youtube.com/watch?v=-tqeKEnKUOU"},
    {"title": "Cozy morning routine with Lili & Ben⛅️🧺🥯| Avatar world #avatarworld #pazu", "url": "https://www.youtube.com/watch?v=LH7gyHDcra8"},
    {"title": "⋆˚࿔ My Morning Routine🧋⛅️ | Pilates Class & Market run 🛒🥥#avatarworld #pazu", "url": "https://www.youtube.com/watch?v=3-T8KV4oI9Y"},
    {"title": "First day of school! 🏫 *GONE WRONG* (WITH VOICE) || Toca Boca Roleplay", "url": "https://www.youtube.com/watch?v=yz5tkGDJJVc"},
    {"title": "First day of kindergarten!! 🐯🍎 *WITH VOICE* II Toca boca Roleplay", "url": "https://www.youtube.com/watch?v=IVglTQpWSm0"},
    {"title": "The Waterpark ACCIDENT! 🌊| With Voice 🔈 | Toca Life World Roleplay", "url": "https://www.youtube.com/watch?v=C0R3vky7r_o"},
    {"title": "The sleepover! *GONE WRONG* (WITH VOICE) II Toca boca roleplay", "url": "https://www.youtube.com/watch?v=ddM_L1bJRKo"},
    {"title": "Good Kid Vs Bad Kid! Which Are You?! Melody Kuromi 😈👀 Toca Life World | Toca Life Story | Toca Boca", "url": "https://www.youtube.com/watch?v=-cjkprX0A0E"},
    {"title": "Good Babysitter VS Bad Babysitter 🍼😈 Sad Story | Toca Life Story | Toca Boca | Toca Life World", "url": "https://www.youtube.com/watch?v=0JWF-vl4sKQ"},
    {"title": "Bad Daughter VS Good Daughter👧🏻😈🩷 Toca Life World | Toca Life Story | Toca Boca", "url": "https://www.youtube.com/watch?v=NXJcYEtOO_g"},
    {"title": "Rich School Teacher vs Broke School Teacher! Who's Better? | Toca Life Story | Toca Boca", "url": "https://www.youtube.com/watch?v=h88W9Zzo8Lw"},
    {"title": "Big family aesthetic morning routine 🪴☀️ *WITH VOICE* || Toca boca Roleplay", "url": "https://www.youtube.com/watch?v=X7YrdJvdorU"},
    {"title": "single mom with twins fall aesthetic morning routine 🤍 *WITH VOICE* II Toca boca roleplay", "url": "https://www.youtube.com/watch?v=ofYliuUwq_o"},
    {"title": "Working at a bakery! (GONE WRONG) *WITH VOICE* || Toca boca roleplay", "url": "https://www.youtube.com/watch?v=klhqs4ovtI4"},
    {"title": "Working as a babysitter! (GONE WRONG) *WITH VOICE* || Toca Boca Roleplay", "url": "https://www.youtube.com/watch?v=jzruyuFoqdM"},
    {"title": "Good Mom VS Bad Mom 😭👱🏻‍♀️❤️ Avatar World | Toca Boca | Toca Life Story", "url": "https://www.youtube.com/watch?v=1l5x_n4LQKA"},
    {"title": "Good Student VS Bad Student 🌙 Night Routine | Toca Boca Life Story", "url": "https://www.youtube.com/watch?v=CUhhrSL7Ps0"},
    {"title": "★•Rainy Night Routine 🚿🌧🧺(asmr) |living alone| @avatarworldbypazu", "url": "https://www.youtube.com/watch?v=EYrXSYnVU6k"},
    {"title": "My Night routine as a Teacher 👩🏼‍🏫🌙 | Avatar World", "url": "https://www.youtube.com/watch?v=fMbATP1HVAA"},
    {"title": "Cozy snowy day routine☃️🧸✨ Relaxing Avatar world video🧺🧡", "url": "https://www.youtube.com/watch?v=CFkURM9m_oU"},
    {"title": "Phonics Song 3", "url": "https://www.youtube.com/watch?v=zNmh4s9un3c"},
    {"title": "Phonics Song", "url": "https://www.youtube.com/watch?v=saF3-f0XWAY"},
    {"title": "♪♪ Funny Animal Song | When Hedgehogs Kiss | Hooray Kids Songs & Nursery Rhymes | Love", "url": "https://www.youtube.com/watch?v=aIgQMKTO6UU"},
    {"title": "Get well soon children's song | Soon you will be fit again - Hooray kids songs & nursery rhymes", "url": "https://www.youtube.com/watch?v=7GtxhRH4FEo"},
    {"title": "Children's song Have a Haircut - Children at the Hairdresser | Hooray Kids Songs & Nursery Rhymes", "url": "https://www.youtube.com/watch?v=zvL9Ei6NM00"},
    {"title": "ASMR UNBOXING Ms RACHEL WOODEN SONG PUZZLE", "url": "https://www.youtube.com/watch?v=g8GG7btk-Fs"},
    {"title": "Four Pete the Cat Books - By Eric Litwin | Kids Book Sing/Read Aloud - Learn To Read", "url": "https://www.youtube.com/watch?v=Eag_WBwO61o"},
    {"title": "Pete The Cat I Love My White Shoes", "url": "https://www.youtube.com/watch?v=cQWDyzH-J54"},
    {"title": "The Rings of Unity - Full Episode | Series 8 E29 | Numberblocks", "url": "https://www.youtube.com/watch?v=UglDhUBsj0k"},
    {"title": "New Words for Toddlers | House and Home Sounds | Phonics with Dee | Yakka Dee!", "url": "https://www.youtube.com/watch?v=ZKnf4HfGGZc"},
    {"title": "Let's read together a Peppa Pig book. The BIGGEST Muddy Puddle in the World. Read along.", "url": "https://www.youtube.com/watch?v=Z5C-RbfsU_Y"},
    {"title": "Learn With Peppa Pig: Peppa Explores Space (Read Aloud) | Read Along With Millie's Mummy", "url": "https://www.youtube.com/watch?v=95kJ08icnSE"},
    {"title": "Peppa pig Peppa loves doctors and nurses", "url": "https://www.youtube.com/watch?v=O8dO0jWpq1A"},
    {"title": "Peppa Pig and the Easter Rainbow", "url": "https://www.youtube.com/watch?v=MdoyCABdYb0"},
    {"title": "Bath Time Song | More Nursery Rhymes & Kids Songs", "url": "https://www.youtube.com/watch?v=_Sp1at0H194"},
    {"title": "Kids Music with Cool Musical Instruments!", "url": "https://www.youtube.com/watch?v=Vaw3rRdWzZg"},
    {"title": "Aesthetic FAMILY FRIDGE RESTOCK! 🍎 (EP 9) | Toca Life World Family Roleplay 🌍", "url": "https://www.youtube.com/watch?v=hs926uOx0rQ"},
    {"title": "Our Family Goes TO WALMART 🛒 (EP 8) | Toca Life World Family Roleplay 🌍", "url": "https://www.youtube.com/watch?v=xajUjdVptFU"},
    {"title": "Theme Song! 🎶| Yakka Dee!", "url": "https://www.youtube.com/watch?v=4BzCW7pt37s"},
    {"title": "Let's Yakka Yak with Dee! | Yakka Dee Marathon! ⭐️", "url": "https://www.youtube.com/watch?v=buCdwl6h5Y8"},
    {"title": "Yakka Dee Theme Tune! | CBeebies", "url": "https://www.youtube.com/watch?v=YTZTwOVL14U"},
    {"title": "Morning routine !!! new role-play !!!!! Toca Boca role-play !!!!!! with voice !!!!!", "url": "https://www.youtube.com/watch?v=GZ1kp1VCPdI"},
    {"title": "Peppa Pig in Avatar World VS Toca World | George Catches a Cold 😰", "url": "https://www.youtube.com/watch?v=kkebnd4qW60"},
    {"title": "Sad cheesey noodle and pals remake kinemaster speed speedrun logo be like", "url": "https://www.youtube.com/watch?v=XS8jMUeoEfM"},
    {"title": "Let's Talk About Clothes! | Yakka Dee!", "url": "https://www.youtube.com/watch?v=WTNItrvtMvY"},
    {"title": "Let's Talk About the Body! | Yakka Dee!", "url": "https://www.youtube.com/watch?v=XIBDtp1wVf0"},
    {"title": "Let's Talk about Things in the Kitchen ☕️ | Yakka Dee!", "url": "https://www.youtube.com/watch?v=AgCUl1nQJ0Q"},
    {"title": "Let's Talk about Animals that Swim! | Yakka Dee!", "url": "https://www.youtube.com/watch?v=ac8oqoejXVc"},
    {"title": "Let's Talk about Travel! | Yakka Dee!", "url": "https://www.youtube.com/watch?v=G6DLvrRtXKg"},
    {"title": "Toddler Learning with Dee | Learn Farm, Zoo and Pet Animals | Lern to Talk | Yakka Dee!", "url": "https://www.youtube.com/watch?v=C5XeTyMvtb4"},
    {"title": "Can you say Digger? 🧱 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=eSTHctmxTLk"},
    {"title": "BRAND NEW! Yakka Dee: Dee's Food Party! 🍕 🍦 | Toddler Words | Yakka Dee!", "url": "https://www.youtube.com/watch?v=g-HUcLRX8JA"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See? | Farm Friends! 🐮🐴 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=IZZZ4vCigrU"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See? | Christmas 🎄 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=DEn6cwWXRz0"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See | Halloween 🎃 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=IMIx3AcCKAU"},
    {"title": "Dee's Mega Song Marathon | Yakka Dee!", "url": "https://www.youtube.com/watch?v=mAxqftr-XuU"},
    {"title": "What Pet Should I Get? by Dr. Seuss | READ ALOUD for Kids", "url": "https://www.youtube.com/watch?v=psCzO1TlJlU"},
    {"title": "Autumn Animals 🍂 | Let's Learn with Yakka Dee| BBC Kids", "url": "https://www.youtube.com/watch?v=AwdyfY8SNBo"},
    {"title": "Can You Say... Nose, Bird, Bath, Monkey, Bubble | Learn with Yakka Dee! | FULL EPISODES | BBC Kids", "url": "https://www.youtube.com/watch?v=ri4xkQgOwQU"},
    {"title": "Can You Say... Feet, Goat, Key, Flower, Kite | Learn with Yakka Dee! | FULL EPISODES | BBC Kids", "url": "https://www.youtube.com/watch?v=iRe08kWZnvw"},
    {"title": "Can You Say... Ball, Mouse, Beans, Car, Bed | Learn with Yakka Dee! | FULL EPISODES | BBC Kids", "url": "https://www.youtube.com/watch?v=2wnA0gjGiXg"},
    {"title": "Learn Transport Words! | Toddler Learning | Car, Bike, Plane + more! | Yakka Dee!", "url": "https://www.youtube.com/watch?v=6OnGQ8nL8Dk"},
    {"title": "Learn Transport words with Dee! | Car, Bus + more! | BBC Kids", "url": "https://www.youtube.com/watch?v=lbp8K-4rvgY"},
    {"title": "Can you say Toothbrush? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=ZWUHObYI8jA"},
    {"title": "The Colorbubblies Song", "url": "https://www.youtube.com/watch?v=s0p9P9KOQSk"},
    {"title": "Colors Song 2", "url": "https://www.youtube.com/watch?v=tQASh8bbkUY"},
    {"title": "Can You Say Book? 📚| Yakka Dee!", "url": "https://www.youtube.com/watch?v=WFJsPrEqD_g"},
    {"title": "Can You Say Beans? 🍽| Yakka Dee!", "url": "https://www.youtube.com/watch?v=H0tHDTLWIz0"},
    {"title": "Phonics Song 2 (new version)", "url": "https://www.youtube.com/watch?v=ffeZXPtTGC4"},
    {"title": "Garden Party Words! | Duck, Strawberry, Cloud | Yakka Dee!", "url": "https://www.youtube.com/watch?v=fP1O70tz83s"},
    {"title": "Learn New Words! | Star, Kite, Pasta | Yakka Dee!", "url": "https://www.youtube.com/watch?v=2obT3yQmcm4"},
    {"title": "Can You Say... Hat, Peas, Bus, Cup, Duck | Learn with Yakka Dee! | FULL EPISODES | Yakka Dee!", "url": "https://www.youtube.com/watch?v=HXR8gT1tF08"},
    {"title": "Scary Words 👻 | 30+ Minutes | Yakka Dee!", "url": "https://www.youtube.com/watch?v=ZQhndsEDQno"},
    {"title": "Smiles All Around 💛 | Learn Happy Words | 20+ Minutes | Yakka Dee!", "url": "https://www.youtube.com/watch?v=uzG5g5KpWFk"},
    {"title": "Can You Say Rain? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=nTXkraiOBXk"},
    {"title": "Can you say Hedgehog? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=hogg_V0OuAE"},
    {"title": "Can You Say Lion? 🦁| Yakka Dee!", "url": "https://www.youtube.com/watch?v=_bQKaMjwm5s"},
    {"title": "Can you say Train?🚂 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=s7omVulXuA8"},
    {"title": "Can you say Rocket? 🚀 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=EOA8Yj639sE"},
    {"title": "Can You Say Apple? 🍎| Yakka Dee!", "url": "https://www.youtube.com/watch?v=lbOvVsgxSL8"},
    {"title": "Can You Say Peas? 💚| Yakka Dee!", "url": "https://www.youtube.com/watch?v=RyNCz4zawyc"},
    {"title": "Transport words with Dee 🚂✈️ | Learn Travel Phonics | Trains, Bus and Bicycle words | Yakka Dee!", "url": "https://www.youtube.com/watch?v=IhW1naBMuYw"},
    {"title": "TUBBY | Leslie Patricelli | TODDLER CONCEPTS | #storytime #parenting #esl #toddler #preschool #kids", "url": "https://www.youtube.com/watch?v=SBpkBJY1PKA"},
    {"title": "🔴LIVE: The BEST of Series 2 | Yakka Dee", "url": "https://www.youtube.com/watch?v=HxpF-kIdlso"},
    {"title": "Peppa Pig Takes Funny Pictures In The Photo Booth | Kids TV And Stories", "url": "https://www.youtube.com/watch?v=tx2OzMdgs_Q"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See? | Bedroom 🧸📚 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=9CkomrNIztk"},
    {"title": "🔴 LIVE: Common Words with Dee! | Food Words for Toddlers | Yakka Dee!", "url": "https://www.youtube.com/watch?v=EEQYWSAfVBU"},
    {"title": "🔴LIVE: Learning Marathon for Toddlers! | Explore new words and Sounds with Dee | Yakka Dee!", "url": "https://www.youtube.com/watch?v=jN6Sqi9j_hU"},
    {"title": "Water Words for Toddlers | Bubble, Whale & More | Yakka Dee!", "url": "https://www.youtube.com/watch?v=aAG4GgbwfnQ"},
    {"title": "Alphabet Marathon (A-Z) Words and Letters | Yakka Dee!", "url": "https://www.youtube.com/watch?v=vKbgmwzrcP8"},
    {"title": "Explore Winter With Dee! ❄️ | Toddler Words | Yakka Dee!", "url": "https://www.youtube.com/watch?v=xI1c6h0Zaww"},
    {"title": "Can You Say... Bed, Car, Beans, Mouse, Ball | Learn with Yakka Dee! | FULL EPISODES | Yakka Dee!", "url": "https://www.youtube.com/watch?v=FXDDmdevF3w"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See? | Bathroom 🦷 🫧 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=iwJ6A3kpHMk"},
    {"title": "Can you say Van? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=ZdS1Mz5Nh4Q"},
    {"title": "Can you say Lemon? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=PJ2a0TmhiVE"},
    {"title": "Can You Say Hair? 💇‍♀️| Yakka Dee!", "url": "https://www.youtube.com/watch?v=DdBkdt4iAfI"},
    {"title": "Can You Say Whale? 🐳| Yakka Dee!", "url": "https://www.youtube.com/watch?v=QMnwOsI5pys"},
    {"title": "Can You Say Cat? 🐈 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=WWimpIBiU1o"},
    {"title": "Can You Say Bag? 👜 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=i4QvU1Lgyz0"},
    {"title": "Can You Say Nose? 👃| Yakka Dee!", "url": "https://www.youtube.com/watch?v=4BoPY-DWK8Y"},
    {"title": "Can you say Donkey?🐴 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Cq1Hq9w_Z5o"},
    {"title": "Can You Say Strawberry? 🍓 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=s2xFC53lwH0"},
    {"title": "Can you say Bread? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=A3gvI1U7pGE"},
    {"title": "Can you say Cheese? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=2ZCoif6MLnM"},
    {"title": "Can you say Scooter? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=9vaziM4WFTk"},
    {"title": "Can you say Octopus? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=urIa9TDosFQ"},
    {"title": "Can you say Spider? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=usR89A2qnfg"},
    {"title": "Can you say Blanket? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=JVUXUQ-hZi8"},
    {"title": "Can You Say Orange? 🍊 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=lEsZOSB6H_8"},
    {"title": "Can You Say Pumpkin? 🎃 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=_9113L1xd-M"},
    {"title": "Can you say Raspberry? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=cYiM4eB8-B8"},
    {"title": "Can you say Grass? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=acXeRVxfR3Y"},
    {"title": "Can You Say Hand? 🖐️ | Yakka Dee!", "url": "https://www.youtube.com/watch?v=OcJ7KItsQ5k"},
    {"title": "Can you say Bed? 🛌 💤 | Yakka Dee", "url": "https://www.youtube.com/watch?v=uO0kiBfhrtE"},
    {"title": "Yakka Dee - Book", "url": "https://www.youtube.com/watch?v=qOmaOijEPEM"},
    {"title": "Yakka Dee - Top", "url": "https://www.youtube.com/watch?v=w8Rdu1hz1-E"},
    {"title": "Yakka Dee Series 4 | Episode 2 | CBeebies", "url": "https://www.youtube.com/watch?v=iyQFWFFOxeU"},
    {"title": "Can You Say Chair? 🪑| Yakka Dee", "url": "https://www.youtube.com/watch?v=oRj0wBTw00A"},
    {"title": "Can You Say Boots? 👢| Yakka Dee!", "url": "https://www.youtube.com/watch?v=HBaVmad60m8"},
    {"title": "Can you say Coat? 🧥 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=C2WRRb_VL0k"},
    {"title": "Can you say Top?👚| Yakka Dee!", "url": "https://www.youtube.com/watch?v=-W_vJkGh9SY"},
    {"title": "Can you say Shoes?🥾 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=JTCTOMkQxCY"},
    {"title": "Can You Say Cup? 🥛| Yakka Dee!", "url": "https://www.youtube.com/watch?v=wu1M0Agj_hE"},
    {"title": "Can You Say Mouse? 🐭| Yakka Dee!", "url": "https://www.youtube.com/watch?v=2gAGAslcoZ0"},
    {"title": "Can You Say Bird? 🦜| Yakka Dee!", "url": "https://www.youtube.com/watch?v=Df0TK9Ql2-M"},
    {"title": "Can You Say Monkey? 🐒| Yakka Dee!", "url": "https://www.youtube.com/watch?v=N6baWdxJ0Jw"},
    {"title": "Can You Say Bath? 🛁| Yakka Dee!", "url": "https://www.youtube.com/watch?v=RtAnhHh0FTU"},
    {"title": "Can you say Swing? 😃 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Kz_6Drsx-7Y"},
    {"title": "Can You Say Bus? 🚌| Yakka Dee!", "url": "https://www.youtube.com/watch?v=XycRJKpt5ZE"},
    {"title": "Can You Say Dog? 🐶| Yakka Dee!", "url": "https://www.youtube.com/watch?v=bSaC90HFmn4"},
    {"title": "Can you say Pyjamas? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=RjkZ3f28iNo"},
    {"title": "Can you say Shorts? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=KdN2JYOhuCs"},
    {"title": "Can you say Sheep? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=FZ-3_F84yag"},
    {"title": "Can you say Cow? 🐄 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=L02MPzmb-9c"},
    {"title": "Can you say Fish? 🐟 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=O-x7AKVe-g8"},
    {"title": "Can you say Lizard? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Ns9MRB8YcYU"},
    {"title": "Can you say Egg?🥚 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Uquc6L38qXk"},
    {"title": "Can You Say Bowl? 🥣 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=oB10YeBIx-s"},
    {"title": "Can you say Glasses? 👓 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=zEWqRXNaGvc"},
    {"title": "Can you say Pizza? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=DlklPwhryJc"},
    {"title": "Can you say Plate? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=kftacIt4fug"},
    {"title": "Can you say Tractor? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Lyp9t_oYSYY"},
    {"title": "♪ ♪ Funny Cat Song – Cat Toilet | Hooray Kids Songs & Nursery Rhymes | Funny Animal Songs", "url": "https://www.youtube.com/watch?v=k9QP8-tkDvY"},
    {"title": "Can you say Plane? ✈️ | Yakka Dee!", "url": "https://www.youtube.com/watch?v=EyolcamjwgU"},
    {"title": "Can you say Mango? 🥭 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=fatEjz_x0dc"},
    {"title": "Can You Say Flower? 🌺| Yakka Dee!", "url": "https://www.youtube.com/watch?v=u5d0hauCdEo"},
    {"title": "Can You Say Kite? 🎏 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=1NM7uobvgg8"},
    {"title": "Can You Say Key? 🔑| Yakka Dee!", "url": "https://www.youtube.com/watch?v=iYQzP10nlaQ"},
    {"title": "Can you say Milk?🍼 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=j4CJyornuKM"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See? | Explore With Dee! 🔍 💚 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=zfL49PUT6jE"},
    {"title": "Yakka Dee Transport!🚦| Yakka Dee!", "url": "https://www.youtube.com/watch?v=9sb_dVdoWsU"},
    {"title": "Yakka Dee - Banana", "url": "https://www.youtube.com/watch?v=Gj12k0x_3Sw"},
    {"title": "Can you say Juice? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=NVmEp15ZOAE"},
    {"title": "Can You Say Chicken 🐥 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=_Qt8HqlfD7Y"},
    {"title": "Can You Say Worm? 🐛| Yakka Dee!", "url": "https://www.youtube.com/watch?v=LkD0Bx88Bpg"},
    {"title": "Can You Say Elf | Yakka Dee!", "url": "https://www.youtube.com/watch?v=1eLJD4VvGTg"},
    {"title": "Can You Say Skin? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=siZ10v63uK8"},
    {"title": "Can You Say Ear?👂 | Yakka Dee", "url": "https://www.youtube.com/watch?v=gjfgO6raZaM"},
    {"title": "Can You Say Tummy? 👕| Yakka Dee!", "url": "https://www.youtube.com/watch?v=BGMXpB6vE9M"},
    {"title": "Can you say Tiger?🐅 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=qO5jk0N7q40"},
    {"title": "Can You Say Bee? 🐝| Yakka Dee!", "url": "https://www.youtube.com/watch?v=9Roo_LGVYzg"},
    {"title": "Peppa's Pop-Up Dragons🐉lift-the-flap book #readaloud #bedtimestories #kidsbooks #peppapig #storytime", "url": "https://www.youtube.com/watch?v=05CRiWHevFY"},
    {"title": "Peppa's Great DINOSAUR Hunt**A lift-the-flap Book**Bedtimestory☆ Reading aloud☆", "url": "https://www.youtube.com/watch?v=6IEf3GC8RWg"},
    {"title": "Peppa Loves Soft Play☆A lift-the-flap Book☆Bedtimestory☆ #story #bedtimestories #peppapig #readaloud", "url": "https://www.youtube.com/watch?v=D99WH-k19E0"},
    {"title": "Learn Characters, Vehicles and Colors with Ben & Holly, Peppa Pig, and other toys in box for Kids", "url": "https://www.youtube.com/watch?v=gc_x_2T3tDs"},
    {"title": "BRAND NEW! Yakka Dee: What Can You See? | Kitchen 🍞 🍏 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Qw7BZmiFGFk"},
    {"title": "Even More Yakka Dee! | Yakka Dee Marathon 3 ⭐️", "url": "https://www.youtube.com/watch?v=7cLHwcD-oNE"},
    {"title": "Peppa Pig Dress Up Color Game 🌈 Peppa Pig Tales Kids Quiz with Peppa Pig & Friends | Kids DingDong", "url": "https://www.youtube.com/watch?v=EjUIBBfbhiI"},
    {"title": "Kids, let's Learn Common Words with Woodzeez Toy Dollhouse!", "url": "https://www.youtube.com/watch?v=SrBnsSwTGjM"},
    {"title": "Can You Say Tree? 🌳| Yakka Dee!", "url": "https://www.youtube.com/watch?v=zvA6heBezOY"},
    {"title": "Can you say Cake? 🍰 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=b_b5GPeZmDc"},
    {"title": "Can You Say Ball? ⚽️| Yakka Dee!", "url": "https://www.youtube.com/watch?v=lr704Bu0XYc"},
    {"title": "Can You Say House? 🏠| Yakka Dee!", "url": "https://www.youtube.com/watch?v=7c5Zctnmoxw"},
    {"title": "Can You Say Hat? 🎩| Yakka Dee!", "url": "https://www.youtube.com/watch?v=C6dvN6uX5qU"},
    {"title": "Can You Say Cloud? ☁️| Yakka Dee!", "url": "https://www.youtube.com/watch?v=dPkV6PwxglU"},
    {"title": "Let's Dance with Dee! | Yakka Dee!", "url": "https://www.youtube.com/watch?v=NgiCePyv7tY"},
    {"title": "🔴LIVE: Songs with Dee! | Fun songs for kids | Yakka Dee!", "url": "https://www.youtube.com/watch?v=gf9Q3YQrB7I"},
    {"title": "Transport Marathon with Dee | Yakka Dee!", "url": "https://www.youtube.com/watch?v=V6rYtuuAJDI"},
    {"title": "Learn Amazing Insects and Bugs for Kids | Kids Learning Classroom", "url": "https://www.youtube.com/watch?v=zDLyJoMKohY"},
    {"title": "Can you say Robot? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Q8f99Cwx78k"},
    {"title": "We play Opposite Day - Children's song to play and join in | Hooray Kids Songs & Nursery Rhymes", "url": "https://www.youtube.com/watch?v=MyBCU3hrHNs"},
    {"title": "Jay Tries to Do Grown Up Jobs | Nikhil & Jay Kids Cartoons on BBC iPlayer", "url": "https://www.youtube.com/watch?v=xvHtq-oE_i8"},
    {"title": "Can you say words beginning with S? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=_B_D6hficgU"},
    {"title": "Feelings with Leslie Patricelli 💛 | Toddler Read-Aloud Compilation | Emotions & Empathy", "url": "https://www.youtube.com/watch?v=kwrXXCAhywI"},
    {"title": "Leslie Patricelli Opposites 📚 | Toddler Read-Aloud with Learning Reflections | Hoots & Tales", "url": "https://www.youtube.com/watch?v=qFj6K_Z70ZY"},
    {"title": "Can you say Gloves? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=qCEeZvcMNfk"},
    {"title": "Can you say Drum?🥁 | Yakka Dee!", "url": "https://www.youtube.com/watch?v=Z2iSApmXmGU"},
    {"title": "Can you say Fox? | Yakka Dee!", "url": "https://www.youtube.com/watch?v=wMpcq5fhbtk"},
    {"title": "Learn Common Household Words with Woodzeez and Bluey for Kids!", "url": "https://www.youtube.com/watch?v=Tuw2fu5_zPI"},
    {"title": "Can You Say Alien | Yakka Dee!", "url": "https://www.youtube.com/watch?v=K1e3yUrdlTk"},
]

def parse_duration_to_seconds(dur_str):
    """Convert duration string to seconds"""
    dur_str = dur_str.strip()
    parts = dur_str.split(':')
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        pass
    return 0

def parse_text_to_videos():
    """Parse the raw text into video entries"""
    lines = [l.strip() for l in RAW_TEXT.strip().split('\n') if l.strip()]
    
    # Skip header lines
    skip = {'Skip navigation', 'Create', 'Home', 'Shorts', 'Subscriptions', 'You', 
            'Watch history', 'All', 'Videos', 'Shorts', 'Podcasts', 'Music', 
            'Search watch history', 'Clear all watch history', 'Pause watch history', 
            'Manage all history', 'Comments', 'Posts', 'Live chat', '•', 'Today',
            'Yesterday', 'This week', 'Last week'}
    
    duration_re = re.compile(r'^\d+:\d{2}(:\d{2})?$')
    views_re = re.compile(r'^[\d.,]+[KMB]?\s*views$|^\d+\s*watching$')
    
    videos = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line in skip:
            i += 1
            continue
        
        # Check if this is a duration line
        if duration_re.match(line) or line == 'LIVE':
            duration = line
            i += 1
            if i >= len(lines):
                break
            
            # Next should be title
            title = lines[i]
            if title in skip or duration_re.match(title) or views_re.match(title):
                i += 1
                continue
            i += 1
            
            # Next should be channel name
            channel = ''
            if i < len(lines) and lines[i] not in skip and not duration_re.match(lines[i]) and not views_re.match(lines[i]):
                channel = lines[i]
                i += 1
                # Sometimes channel has "and ..." continuation
                if i < len(lines) and lines[i].startswith('and ') and not views_re.match(lines[i]):
                    channel += ' ' + lines[i]
                    i += 1
            
            # Skip • and views
            while i < len(lines) and (lines[i] == '•' or views_re.match(lines[i])):
                i += 1
            
            # Skip description line
            if i < len(lines) and len(lines[i]) > 80 and not duration_re.match(lines[i]):
                i += 1
            
            videos.append({
                'duration_str': duration,
                'title': title,
                'channel': channel
            })
        else:
            i += 1
    
    return videos

def categorize_video(title, channel):
    """Assign category based on title/channel"""
    title_lower = title.lower()
    channel_lower = channel.lower()
    
    if any(x in title_lower for x in ['phonics', 'alphabet', 'abc', 'reading', 'learn', 'educational', 'words', 'letters']):
        return 'Educational'
    if any(x in channel_lower for x in ['yakka dee', 'kidstv123', 'numberblocks', 'cbeebies', 'bbc kids']):
        return 'Educational'
    if any(x in title_lower for x in ['peppa pig', 'peppa']):
        return 'Cartoon/Show'
    if any(x in title_lower for x in ['toca boca', 'toca life', 'avatar world', 'roleplay', 'role-play', 'role play']):
        return 'Gaming/Roleplay'
    if any(x in title_lower for x in ['nursery rhymes', 'kids songs', 'song', 'music']):
        return 'Music/Songs'
    if any(x in title_lower for x in ['read aloud', 'storytime', 'story time', 'book']):
        return 'Storytime'
    if any(x in title_lower for x in ['logo sound', 'quiz', 'guess']):
        return 'Quiz/Games'
    if 'routine' in title_lower:
        return 'Gaming/Roleplay'
    return 'Other'

def main():
    now = datetime.now(timezone.utc)
    iso_now = now.isoformat()
    
    # Parse text entries
    text_videos = parse_text_to_videos()
    
    # Create URL lookup by title (normalized)
    url_lookup = {}
    for u in URL_LIST:
        norm = u['title'][:50].strip()
        url_lookup[norm] = u['url']
    
    # Build video list
    videos = []
    total_seconds = 0
    
    for idx, tv in enumerate(text_videos):
        title = tv['title']
        channel = tv['channel']
        duration_str = tv['duration_str']
        
        # Find URL
        url = ''
        for ul in URL_LIST:
            if ul['title'][:40] == title[:40]:
                url = ul['url']
                break
        
        if not url and idx < len(URL_LIST):
            url = URL_LIST[idx]['url'] if idx < len(URL_LIST) else ''
        
        secs = parse_duration_to_seconds(duration_str) if duration_str != 'LIVE' else 0
        total_seconds += secs
        
        category = categorize_video(title, channel)
        
        videos.append({
            'title': title,
            'channel': channel,
            'timestamp': iso_now,
            'timestamp_raw': 'Today',
            'url': url,
            'duration': duration_str,
            'duration_seconds': secs,
            'category': category
        })
    
    # Channel counts
    channel_counts = defaultdict(int)
    for v in videos:
        if v['channel']:
            channel_counts[v['channel']] += 1
    
    top_channels = sorted([{'channel': c, 'count': n} for c, n in channel_counts.items()], 
                          key=lambda x: -x['count'])[:15]
    
    # Category counts
    cat_counts = defaultdict(int)
    for v in videos:
        cat_counts[v['category']] += 1
    
    top_categories = sorted([{'category': c, 'count': n} for c, n in cat_counts.items()],
                            key=lambda x: -x['count'])
    
    # Hour/day counts (approximate - all today)
    hour = now.hour
    hourly = {str(hour): len(videos)}
    daily = {'Sat': len(videos)}
    
    data = {
        'generated': iso_now,
        'account': 'jigar.us.af@gmail.com',
        'period_days': 7,
        'note': 'Daily update - Saturday March 7 2026',
        'total_videos': len(videos),
        'total_watch_minutes': round(total_seconds / 60, 1),
        'videos': videos,
        'top_channels': top_channels,
        'top_categories': top_categories,
        'hourly_counts': hourly,
        'daily_counts': daily
    }
    
    out_path = '/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(videos)} videos to history.json")
    print(f"   Total watch time: {round(total_seconds/60, 1)} minutes")
    print(f"   Top channel: {top_channels[0]['channel'] if top_channels else 'N/A'} ({top_channels[0]['count'] if top_channels else 0} videos)")
    print(f"   Top category: {top_categories[0]['category'] if top_categories else 'N/A'} ({top_categories[0]['count'] if top_categories else 0} videos)")

if __name__ == '__main__':
    main()
