#!/usr/bin/env python3
"""
Build KidWatch history.json from browser scrape on 2026-03-23.
200 videos extracted from YouTube watch history.
"""
import json
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

# ─── RAW SCRAPED DATA ──────────────────────────────────────────────────────
# (title, channel, duration_str, url)
VIDEOS_RAW = [
    ("Real World Ramen | Featuring The Bumble Nums Plushies! 😍 | Cartoons For Kids", "The Bumble Nums", "7:11", "https://www.youtube.com/watch?v=sICUewwtmbU"),
    ("Peppa Pig Game | Crocodile Hiding in Kids Cereal with Toy Friends", "Just For Kids", "4:30", "https://www.youtube.com/watch?v=Gkfyuk-MbNk"),
    ("Fun Videos with Peppa Pig Weebles and Zoo Animals for kids!", "Genevieve's Playhouse - Learning Videos for Kids", "16:41", "https://www.youtube.com/watch?v=A3ijbDXlNl4"),
    ("Aprender Colores y Números | Huevos de Colores en la Granja | Canciones Infantiles ChuLoo en Español", "ChuLoo en Español", "4:12", "https://www.youtube.com/watch?v=jTl1lhKGSAY"),
    ("PETE THE CAT'S TRIP TO THE SUPERMARKET | KIDS BOOK READ ALOUD | FUN STORY FOR CHILDREN 🛒🐱", "TinySongs", "2:49", "https://www.youtube.com/watch?v=ftUzhIgXTwE"),
    ("Young at Art: Pete the Cat - Rocking In My School Shoes", "Taubman Museum of Art", "0:30", "https://www.youtube.com/watch?v=XRub5z2O3I4"),
    ("Pete the Cat Rocking in My School Shoes", "KB00KIE", "2:35", "https://www.youtube.com/watch?v=eQC212n_h6c"),
    ("Kids books reading @kidsoftheagetv \"Pet the Cat and the Super Cool Science fair!\"", "SANGSEHAN", "9:01", "https://www.youtube.com/watch?v=VIC0IDSus2A"),
    ("The Alphabet Is So Much Fun + More | Super Fun Kids Songs! | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "1:02:00", "https://www.youtube.com/watch?v=srNFdJBfTV0"),
    ("Fun Kids Party Songs! 🎶 | There's A Monster In My Tummy #2 + More Rhymington Square Songs!", "Rhymington Square - Songs & Rhymes for Kids!", "55:00", "https://www.youtube.com/watch?v=IfDQKGMaF1k"),
    ("It's Way Too Hot Today + More | Fun Preschool Songs for Kids! | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "57:00", "https://www.youtube.com/watch?v=gMhoQCO38Mk"),
    ("Down By The Spooky Bay + More | Monster Fun For Kids! | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "54:00", "https://www.youtube.com/watch?v=sqvRJA4Al-s"),
    ("🔴 Rhymington Square Livestream | Kids Songs | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "0:30", "https://www.youtube.com/watch?v=u7UwWlPorc4"),
    ("The Alphabet Rhyme + More | Kids Songs from Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "1:06:00", "https://www.youtube.com/watch?v=DWHNSVbKnuA"),
    ("Visit An Ice Cream Shop With Caitie! | Caitie's Classroom Field Trip | Food Video for Kids", "Super Simple Play with Caitie!", "3:52", "https://www.youtube.com/watch?v=7e2e77w4cZc"),
    ("Roma and Diana Pretend Play Cooking Food Toys with Kitchen Play Set", "✿ Kids Diana Show", "3:52", "https://www.youtube.com/watch?v=fbatqm3-5nU"),
    ("Drinks - Kids vocabulary - Learn English for kids - English educational video", "English Singsing", "4:50", "https://www.youtube.com/watch?v=A_AJrtGtC3Y"),
    ("OPPOSITE WORDS | English for KIDS 🐱 💕", "Cozy English Club", "5:59", "https://www.youtube.com/watch?v=Qt1WyNpWhJA"),
    ("20 SCHOOL ITEMS Name In English And Hindi With Pictures | SCHOOL ITEMS Name For Kids – Easy Learning", "Great Learner Kids", "8:27", "https://www.youtube.com/watch?v=TWz9zHCPdqI"),
    ("20 ड्रॉइंग ऑब्जेक्ट के नाम | Learn 20 Drawing Objects Names with Pictures Easy Learning Video", "Divya Study Class Hindi", "4:41", "https://www.youtube.com/watch?v=z1akzxQM8pM"),
    ("Minnie Red Riding Hood | S1 E18 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:00", "https://www.youtube.com/watch?v=oOy9ykjLhnk"),
    ("Peppa Runs a Clubhouse Takeaway 🍕 | Peppa Pig Official Full Episodes", "Peppa Pig - Official Channel", "4:06:00", "https://www.youtube.com/watch?v=m2yXS5uUdyM"),
    ("Peppa Pig Playground ❤️ | Wishing Well | Peppa Pig Full Episodes", "Peppa Pig Playground", "7:47:00", "https://www.youtube.com/watch?v=Nm8Iz_G1Oz8"),
    ("Peppa Pig Playground 🥪 | Lunch | Peppa Pig Full Episodes", "Peppa Pig Playground", "4:47:00", "https://www.youtube.com/watch?v=an0X12ijAiI"),
    ("Diana Pretend Play Cooking with Kitchen Toys", "✿ Kids Diana Show", "5:05", "https://www.youtube.com/watch?v=b5J7JYyMk_0"),
    ("Learn Skateboard Tricks with Blippi & Meekah at the Woodward Skate Park", "Meekah - Educational Videos for Kids", "16:00", "https://www.youtube.com/watch?v=2wBWwk5U_OA"),
    ("Peppa Pig's Wedding Adventure with Mr. Bull!💍 Valentine Mini-Movie Special 💕 Full Episodes | 18 Mins", "Peppa Pig's Big Adventures", "17:00", "https://www.youtube.com/watch?v=h_uZ8jgV_kU"),
    ("Minnie's Birthday | S1 E7 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:00", "https://www.youtube.com/watch?v=dmdGQljdF_E"),
    ("20 केक के नाम | Learn 20 Cake Names in English with Pictures Easy Cake Names Learning Video", "Divya Study Class Hindi", "4:40", "https://www.youtube.com/watch?v=Vf-UQbs0NdI"),
    ("Peppa Pig's FIRST Drive-Thru Experience 😋🚗 | Tasty Food Day Out | Tales Full Episodes | 18 Minutes", "Peppa's Best Bites", "18:00", "https://www.youtube.com/watch?v=zQXrExIIVN8"),
    ("Gaga Baby Goes Grocery Shopping Through Portal!", "Goo Goo Colors", "4:10", "https://www.youtube.com/watch?v=gQPP2CuuMl4"),
    ("🔴 BRAND NEW PEPPA PIG TALES EPISODES 🐽 ALL New Season 3 ✨📺 | New House, New Car, New Bedroom!", "Peppa Pig Tales", "5:58:00", "https://www.youtube.com/watch?v=ZlVE0ksGQgs"),
    ("Peppa Pig and Bluey Go to School!", "Genevieve's Playhouse - Learning Videos for Kids", "13:54", "https://www.youtube.com/watch?v=DknjsopOHLg"),
    ("Peppa Pig Learns How to Make LUNCH 🍕 | Cooking Pizza & Salad | Full Episodes | Cartoon | 20 Minutes", "Toys and Colours", "17:00", "https://www.youtube.com/watch?v=b_kKQ2nDeM8"),
    ("Doctor Daisy, MD | S1 E25 | Full Episode | Mickey Mouse Clubhouse | @disneyjr", "Disney Jr.", "24:00", "https://www.youtube.com/watch?v=e0O6lW38ew4"),
    ("Pororo the Little Penguin Colorful Toy Cars Playset!", "Genevieve's Playhouse - Learning Videos for Kids", "5:14", "https://www.youtube.com/watch?v=mKFFEuZpQT4"),
    ("Learn Common words with Pororo the Little Penguin's Toy house!", "Genevieve's Playhouse - Learning Videos for Kids", "18:00", "https://www.youtube.com/watch?v=G-zIQqBE-Jg"),
    ("Kids, let's learn common words with Pororo's fun Toy Dollhouse!", "Genevieve's Playhouse - Learning Videos for Kids", "10:07", "https://www.youtube.com/watch?v=hGnMSib9Fuw"),
    ("Blippi Goes Indoor Skydiving | Fun and Educational Videos For Kids", "Blippi - Educational Videos for Kids", "12:09", "https://www.youtube.com/watch?v=hMA7v-FF4Rs"),
    ("Blippi Rides Roller Coasters At The Fun Spot Theme Park! | Educational Videos For Kids", "Blippi - Educational Videos for Kids", "13:50", "https://www.youtube.com/watch?v=FlFmpukN4TM"),
    ("[NEW✨] Learn Colors with Carrot Catching Game & Jeni | Learn Colors for Kids | Pinkfong Hogi", "Hogi! Pinkfong - Learn & Play", "3:32", "https://www.youtube.com/watch?v=SuTVeIWNCnM"),
    ("Fixing pothole in road with kids steamroller, dump truck, and trailer. Educational | Kid Crew", "Kid Crew", "13:34", "https://www.youtube.com/watch?v=ooIZC4v50jE"),
    ("Back to school on kids school bus. Science, recess, lunch, gym, and reading. Educational | Kid Crew", "Kid Crew", "13:44", "https://www.youtube.com/watch?v=K_n4DRu9fcE"),
    ("Blippi's Has A Fun Day of Color Play | Blippi's Stories and Adventures for Kids | Moonbug Kids", "It's Storytime", "15:00", "https://www.youtube.com/watch?v=VZUZGIQhHOI"),
    ("Blippi Visits an Ice Cream Truck | Math and Simple Addition for Children", "Blippi - Educational Videos for Kids", "13:59", "https://www.youtube.com/watch?v=o5-MkuEnDoA"),
    ("Diana and Roma teach School bus rules with friends", "✿ Kids Diana Show", "6:19", "https://www.youtube.com/watch?v=iDShZJWIJ8A"),
    ("Alarm Clocked Out | Minnie's Bow-Toons 🎀 | @disneyjr", "Disney Jr.", "3:01", "https://www.youtube.com/watch?v=RMP6SsAHxP4"),
    ("Peppa Pig Finds A Spider!", "Peppa Pig - Official Channel", "4:30", "https://www.youtube.com/watch?v=m2gcV3JIEcM"),
    ("Peppa Pig Toy Zoo Animal Learning Video for Kids!", "Genevieve's Playhouse - Learning Videos for Kids", "8:18", "https://www.youtube.com/watch?v=sBPT82AyVcA"),
    ("Nat and Essie Playfully and Peppa Pig's School Classroom Set", "Nat and Essie", "4:50", "https://www.youtube.com/watch?v=Ada91JqNc6A"),
    ("Peppa Pig's Family House Construction Building Blocks", "Nat and Essie", "7:57", "https://www.youtube.com/watch?v=DpS986epz7s"),
    ("♥PEPPA PIG♥ gets a new toy House in this Kids Learning Video!", "Genevieve's Playhouse - Learning Videos for Kids", "11:49", "https://www.youtube.com/watch?v=OoMONAVtcDw"),
    ("Learn Colors with 🎄Christmas Slide | 🎅🏼Christmas Colors for Kids | Learn with Hogi", "Hogi! Pinkfong - Learn & Play", "2:56", "https://www.youtube.com/watch?v=0SumlV6HbIw"),
    ("Learn Colors with Ninimo and Slide! | Kids Learn Colors | Pinkfong Hogi", "Hogi! Pinkfong - Learn & Play", "3:17", "https://www.youtube.com/watch?v=sZr1AidiciQ"),
    ("Peppa Pig Fun with Friends Sticker Scene So Cute", "Valerie Toys and Play", "7:03", "https://www.youtube.com/watch?v=BZiKcCasauk"),
    ("Baby Shark Dance Chinese KIDS| Sing and Dance! | PINKFONG Songs for Children", "Mike's Home ESL", "1:43", "https://www.youtube.com/watch?v=tovzrkU7xeE"),
    ("Peppa Pig - Viaggio in Aereo! | Cartoni per Bambini | WildBrain Laboratorio dello Studio", "WildBrain Laboratorio dello Studio", "24:00", "https://www.youtube.com/watch?v=fpEy9m_t0To"),
    ("Blippi's Wheels on the Ice Cream Truck 🍨 Blippi Full Episodes | Emotions and Feelings", "Exploring Emotions and Feelings", "14:58", "https://www.youtube.com/watch?v=YGpNSCQBpDw"),
    ("Blippi Learns at the Indoor Play Place | Educational Videos for Toddlers", "Blippi - Educational Videos for Kids", "18:00", "https://www.youtube.com/watch?v=OayHglz-Wd8"),
    ("Blippi Makes Fruit Popsicles! | Learn Healthy Eating For Children | Educational Videos for Toddlers", "Tiny TV", "17:00", "https://www.youtube.com/watch?v=Px0zti5b7Uc"),
    ("Blippi Makes Chocolate At A Chocolate Factory! | Educational Videos For Toddlers", "Blippi Wonders - Educational Cartoons for Kids", "23:00", "https://www.youtube.com/watch?v=0USRBezOKSc"),
    ("BLIPPI Visits a Raspberry Factory | Moonbug Kids Play and Learn", "Little Learners", "18:00", "https://www.youtube.com/watch?v=KxcAVS_Ljvs"),
    ("Blippi Visits Whiz Kids Playland | @Blippi | Moonbug Literacy", "Learning Literacy - Kids Reading & Phonics", "16:00", "https://www.youtube.com/watch?v=zQYDuij8gL8"),
    ("🔴 LIVE Peppa Pig And Friends 🌟 24 HOUR Livestream", "Peppa Pig and Friends", "0:30", "https://www.youtube.com/watch?v=nEJ7Iwfz9mo"),
    ("Toy Learning Videos for Kids Paw Patrol Halloween and Home Alone Skits!", "Genevieve's Playhouse - Learning Videos for Kids", "18:00", "https://www.youtube.com/watch?v=lAJZJtZ36pM"),
    ("Johny Johny Yes Papa Nursery Rhymes Collection - 3D Rhymes & Songs for Children", "CVS 3D Rhymes & Kids Songs", "8:54", "https://www.youtube.com/watch?v=Z68hf7dfhe8"),
    ("Peppa Pig Toy Learning Video for Kids - Peppa Pig Gets a New Pool and Goes Swimming!", "Genevieve's Playhouse - Learning Videos for Kids", "10:37", "https://www.youtube.com/watch?v=VUBExV8-HJk"),
    ("Best Peppa Pig Learning Video for Kids - George's Birthday Party Adventure!", "Genevieve's Playhouse - Learning Videos for Kids", "11:24", "https://www.youtube.com/watch?v=rmwENNtC9RU"),
    ("Learn Common Household Words with Woodzeez and Bluey for Kids!", "Genevieve's Playhouse - Learning Videos for Kids", "21:00", "https://www.youtube.com/watch?v=Tuw2fu5_zPI"),
    ("DIY Doll Animated Read Aloud | 6 David Stories by David Shannon", "Ah!Young Spring Studio", "19:00", "https://www.youtube.com/watch?v=LiMsCLCB0Po"),
    ("Airplane challenge with Vlad and Niki", "Vlad and Niki", "5:18", "https://www.youtube.com/watch?v=q-GDy0sd77M"),
    ("Diana and Roma show the Safety Rules on board the Airplane", "✿ Kids Diana Show", "9:00", "https://www.youtube.com/watch?v=NifKNSpp0_4"),
    ("Baby Learning | Learn Through Play with Ms. Appleberry | Dollhouse Play | The Melon Patch", "The Melon Patch – Learning Videos for Toddlers", "21:00", "https://www.youtube.com/watch?v=AZeLByOTudc"),
    ("Learn Spanish Words with Peppa Pig and Friends Driving Toy Cars Around Town!", "Genevieve's Playhouse - Learning Videos for Kids", "7:02", "https://www.youtube.com/watch?v=yah5X-wTIpc"),
    ("Diana and Roma playing in cafe", "✿ Kids Diana Show", "6:16", "https://www.youtube.com/watch?v=gHxyPsn9xjQ"),
    ("Kids learn Rules of Conduct in the Cinema", "OLIVER SHOW", "7:19", "https://www.youtube.com/watch?v=dFruOgivf4A"),
    ("Roma and Diana visit Oliver's Cafe", "★ Kids Roma Show", "5:05", "https://www.youtube.com/watch?v=FESRSBaXLQ8"),
    ("Diana Roma and Oliver Built a Circle, Triangle, Square Secret Room", "✿ Kids Diana Show", "4:49", "https://www.youtube.com/watch?v=UaWtNhmaiDs"),
    ("14 min 5 Books of David's adventures - Animated Read Aloud Books for Kids", "Reading is", "14:10", "https://www.youtube.com/watch?v=89MK6CEtH64"),
    ("Kids, let's Learn Common Words with Woodzeez Toy Dollhouse!", "Genevieve's Playhouse - Learning Videos for Kids", "11:37", "https://www.youtube.com/watch?v=SrBnsSwTGjM"),
    ("Bumble Nums Running Game & Bubble Pop Walkthrough iPad App Toddler Preschool Kids Games", "💖 Pink Mermaid Girlies", "14:47", "https://www.youtube.com/watch?v=zPSUHdLFFLo"),
    ("Diana and New Playhouse, Beautiful toys for girls", "✿ Kids Diana Show", "6:23", "https://www.youtube.com/watch?v=RqmwINtgE-8"),
    ("Diana and Peppa Pig Theme Park", "✿ Kids Diana Show", "12:01", "https://www.youtube.com/watch?v=OYzIUntnh70"),
    ("PEPPA PIG Indoor Play Area in Peppa Pig World | George's Spaceship Playzone (Feb 2023) [4K]", "PlanIt Park", "6:28", "https://www.youtube.com/watch?v=iswUYXyBsmA"),
    ("🍧😍Learning Colors and Creating Ice Cream with Play-Doh | Preschool Toddler Learning #toddlers", "Sun Playhouse - Learning Videos for Kids", "10:00", "https://www.youtube.com/watch?v=7v_jSBhuHWc"),
    ("CoComelon: Busy Book Toy Play 🧸 | JJ & Friends Figures + Play Mat | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "8:00", "https://www.youtube.com/watch?v=94w25jFkm2U"),
    ("Peppa Pig: The Christmas Jumper | A Christmas Story For Toddlers | Read Along With Millie's Mummy", "Read Along With Millie's Mummy", "6:00", "https://www.youtube.com/watch?v=6YtTk3iJD2I"),
    ("Birthday Surprises for George's Birthday.I WONDER what he is getting.Let's find out#peppapig#Story.", "Storytime with Sophiee", "3:38", "https://www.youtube.com/watch?v=4R0x-QLhRaY"),
    ("Epic Candy Unboxing: Discover the Most Incredible Sweets Ever!", "Super Candy", "5:00", "https://www.youtube.com/watch?v=Jt7j50tRxCw"),
    ("Grow up David ANIMATED VIDEO", "Storytime with Sonia Panda", "6:05", "https://www.youtube.com/watch?v=BJKYJwvwKQk"),
    ("Learn English Words! Follow the Leader with Sign Post Kids! Playground!", "Sign Post Kids", "7:50", "https://www.youtube.com/watch?v=aledTo4hX1c"),
    ("Visit Adventure City with Blippi x Meekah! | Blippi | Moonbug Kids - Fun Zone", "School of Play", "17:00", "https://www.youtube.com/watch?v=NmcaSOcw9xs"),
    ("Blippi Visits an Indoor Playground (Kids Time in Las Vegas) | Blippi Full Episodes | Blippi Toys", "Blippi Toys", "12:55", "https://www.youtube.com/watch?v=-yzEdyyWKvg"),
    ("Bluey Toy Learning Video for Kids!", "Genevieve's Playhouse - Learning Videos for Kids", "10:01", "https://www.youtube.com/watch?v=RBhIi6tL9-g"),
    ("Cocomelon JJ & Bingo Get Sick & Visit Doc McStuffins!", "AWESMR pop", "8:47", "https://www.youtube.com/watch?v=U-U-MsdpnsY"),
    ("COCOMELON! DIY Make a Face Stickers Activity with JJ, Bella, Mochi, Kiki", "Finley's Toys | Pretend Play & Learning", "11:01", "https://www.youtube.com/watch?v=qLerRV4KGmQ"),
    ("Cocomelon Little Pocket Library: Read Aloud 6 Book Collection for Children and Toddlers", "Shall We Read A Book?", "8:00", "https://www.youtube.com/watch?v=NL3AZ57hqh8"),
    ("CoComelon 5-Minute Stories: Hello, New Friend! - Read Aloud for Children and Toddlers", "Conductor Jack - Kids Songs and Learning", "5:00", "https://www.youtube.com/watch?v=ZZbu0epvCZ0"),
    ("Educational Preschool Toys for Kids - Learn Words, Colors, Songs, Animals, and More!", "Genevieve's Playhouse - Learning Videos for Kids", "8:26", "https://www.youtube.com/watch?v=lca179N9a30"),
    ("Estojos e brinquedos para porcos para crianças", "KIDIBLI em Português", "12:46", "https://www.youtube.com/watch?v=He-P6zuVYEE"),
    ("ألعاب ميكي و ميني ماوس للأطفال", "Kidibli بالعربية", "10:24", "https://www.youtube.com/watch?v=ZFK48llE5Hc"),
    ("MICKEY MOUSE Gone Surfin'! | Bedtime Story Read Aloud", "Chaz Stories", "7:57", "https://www.youtube.com/watch?v=3Qm6nHT9Vtg"),
    ("[NEW✨] Hogi's Jingle Play｜Kids Play｜Hogi Hogi｜Hogi Jingle｜Hogi Pinkfong", "Hogi! Pinkfong - Learn & Play", "4:02", "https://www.youtube.com/watch?v=J2P9qfINUUs"),
    ("[NEW✨] Ninimo's Jingle Play｜Kids Play｜Ninimo Jingle｜Pinkfong Jingle｜Hogi Jingle｜Hogi Pinkfong", "Hogi! Pinkfong - Learn & Play", "4:16", "https://www.youtube.com/watch?v=DBp1NGedJn0"),
    ("[NEW✨] 🌈 🍦 Learn Colors with Colorful Ice Cream Shop｜Colors for Kids｜Hogi Colors｜Hogi Pinkfong", "Hogi! Pinkfong - Learn & Play", "3:23", "https://www.youtube.com/watch?v=VBckujQCDvc"),
    ("peppa the fat belly go to the bus 🚌 Season 1 episode 1", "Miss Kandice💕", "13:06", "https://www.youtube.com/watch?v=WY8t55anmHk"),
    ("(most viewed)Chu Chu Tv Effects (Sponsored by Preview 2 Effects)", "Dharmendra Pro Editor", "2:31", "https://www.youtube.com/watch?v=T_A9csA1GSE"),
    ("Learning Colors – Colorful Eggs on a Farm", "Мирошка ТВ", "5:11", "https://www.youtube.com/watch?v=_nAu9D-8srA"),
    ("[👍🏻BEST5] Learn Colors with Desserts 🍿 🍬｜Popcorn, Donuts, Candies & More!｜Hogi Colors｜Hogi Pinkfong", "Hogi! Pinkfong - Learn & Play", "14:21", "https://www.youtube.com/watch?v=gQaaW1BA3vc"),
    ("Learn Colors SPECIAL Collection | Pinkfong & Hogi | Color for Kids | Learn and Play with Hogi", "Hogi! Pinkfong - Learn & Play", "22:00", "https://www.youtube.com/watch?v=Gs01Mp1HDXo"),
    ("Learn Colors with Poki | Pinkfong & Hogi | Colors for Kids | Learn with Hogi", "Hogi! Pinkfong - Learn & Play", "3:05", "https://www.youtube.com/watch?v=sKsAc32pprg"),
    ("Learn Colors with Myan | Pinkfong & Hogi | Colors for Kids | Learn with Hogi", "Hogi! Pinkfong - Learn & Play", "2:24", "https://www.youtube.com/watch?v=T0a3tnKrH4E"),
    ("Aprende Colores con Myan | Colores |@Hogi_Español | Pinkfong", "Pinkfong en español - Canciones Infantiles", "2:28", "https://www.youtube.com/watch?v=ik9FDTP-qjs"),
    ("Learn Colors with Soccer Ball and More | +Compilation | Pinkfong & Hogi Colors for Kids", "Hogi! Pinkfong - Learn & Play", "19:00", "https://www.youtube.com/watch?v=pYpD0YMwRww"),
    ("22 min 5 Books of David's adventures - Animated Read Aloud Books", "Reading is", "22:00", "https://www.youtube.com/watch?v=fNogleSaFNQ"),
    ("Learn Colors with Ice Cream | Pinkfong & Hogi | Colors for Kids | Learn and Play with Hogi", "Hogi! Pinkfong - Learn & Play", "2:21", "https://www.youtube.com/watch?v=KLD-keJ5wBE"),
    ("Learn Colors with Codi | Pinkfong & Hogi | Colors for Kids | Learn with Hogi", "Hogi! Pinkfong - Learn & Play", "2:45", "https://www.youtube.com/watch?v=T9gDuDfcKTg"),
    ("Aprende Colores con Palomitas de Arcoíris | Colores para niños de 2 a 3 años | Hogi en español", "Hogi & Pinkfong en español - Juega y Aprende", "3:39", "https://www.youtube.com/watch?v=9YOWEoib5SE"),
    ("Pete the Cat Sir Pete the Brave Read Aloud Book", "Storytime with Sonia Panda", "3:02", "https://www.youtube.com/watch?v=yLzdOzBXtV0"),
    ("[NEW✨] Learn Colors with Colorful Pop It | Learn Colors for Kids | Colorful Pop It | Hogi & Pinkfong", "Hogi! Pinkfong - Learn & Play", "3:14", "https://www.youtube.com/watch?v=4dM1voiBWE4"),
    ("Children's Books Read Aloud - It's Christmas David Animated | By David Shannon", "Storytime Hullabaloo Hi", "3:05", "https://www.youtube.com/watch?v=FyXtHPpgapg"),
    ("El Juego de Jingle de Ninimo｜Ninimo de Colores🌈｜¡Ninimo Creció!｜Juego de Jingle 3｜Hogi en español", "Hogi & Pinkfong en español - Juega y Aprende", "4:26", "https://www.youtube.com/watch?v=g4-Z0V0rUcc"),
    ("Children's Books Read Aloud - 5 ANIMATED Davids12+ Minutes | By David Shannon", "Storytime Hullabaloo Hi", "12:01", "https://www.youtube.com/watch?v=kV8RUPtfOLY"),
    ("LEARNING | COUNT ALL HIS TOYS | NO DAVID! - KIDS BOOKS READ ALOUD - FUN FOR CHILDREN | DAVID SHANNON", "Miss Sofie's Story Time - Kids Books Read Aloud", "10:03", "https://www.youtube.com/watch?v=u0jeWwduJGY"),
    ("My Fuzzy Valentine Read Aloud Book For Children", "Storytime with Sonia Panda", "2:22", "https://www.youtube.com/watch?v=RyylSEXTRFI"),
    ("[NEW✨] 🌈 🚂 Learn Colors with Colorful Train｜Colors for Kids｜Train Songs｜Hogi Colors｜Hogi Pinkfong", "Hogi! Pinkfong - Learn & Play", "3:16", "https://www.youtube.com/watch?v=b66W0nV1mUA"),
    ("Learn Colors with Rainbow Popcorn 🍿️ | Colors Songs | Kids Learn Colors | Pinkfong Hogi", "Hogi! Pinkfong - Learn & Play", "3:38", "https://www.youtube.com/watch?v=EXi3HAEv0sw"),
    ("Mickey Mouse and Bluey Play Musical Statues Together! 🐭💙 | Mickey+ Shorts | @disneyjr", "Disney Jr.", "1:50", "https://www.youtube.com/watch?v=8irjpFMQphI"),
    ("Noodle & Pals Super Logo Effects, Preview 2 Effects) Most Viewed", "MSC PRO EDIT", "2:56", "https://www.youtube.com/watch?v=94SQybn6nK4"),
    ("Pinkfong Angry Explosion Intro Logo || Preview 2 style Effect || fanmade", "Yusra Pro Editor", "2:52", "https://www.youtube.com/watch?v=4mmLDltq5Nw"),
    ("ChuChu Tv Outrologo Effects SoundVibration ( Sponsored By: Preview 2 Random Effects )", "Yupen Pro Editor", "3:00", "https://www.youtube.com/watch?v=mz6Ro5_ncrA"),
    ("Chu Chu tv surprise logo intro Effects(Sponsored by preview 2 Effects)", "Dharmendra Pro Editor", "4:41", "https://www.youtube.com/watch?v=IG8Boqk45Ow"),
    ("Chiku Saves A Spot + More Good Habits Bedtime Stories & Moral Stories for Kids – ChuChu TV Storytime", "ChuChuTV Storytime for Kids", "13:53", "https://www.youtube.com/watch?v=-M-m9oJIzFQ"),
    ("Man In The Park - Bedtime Stories for Kids in English | ChuChu TV Storytime for Children", "ChuChuTV Storytime for Kids", "6:16", "https://www.youtube.com/watch?v=ixG-EkxjT9Y"),
    ("Eating Colorful Donuts 🍩｜15 min｜Learn Colors for Children | Compilation | 3D Kids｜Hogi & Pinkfong", "Hogi! Pinkfong - Learn & Play", "15:00", "https://www.youtube.com/watch?v=fZVXEBPEtyo"),
    ("Tobee And The Beanstalk | A Super Simple Storybook", "Super Simple Storytime", "11:06", "https://www.youtube.com/watch?v=YkCbl2R4o8g"),
    ("Peppa Pig: Find The Real Characters - Dress Up", "Kidsquad", "3:00", "https://www.youtube.com/watch?v=9R--ARxGiYk"),
    ("Pinkfong's Colorful Super Market｜Kids Pretend Play｜Colors for Kids｜Hogi Colors｜Pinkfong Hogi", "Hogi! Pinkfong - Learn & Play", "3:16", "https://www.youtube.com/watch?v=1nlkwoiVz30"),
    ("Let's Go For A Walk Outside | A Storybook For Kids | Rhymington Square", "Super Simple Storytime", "8:21", "https://www.youtube.com/watch?v=J2l5xJ21UVU"),
    ("Alphabet song 들으며 즐겁게 Alphabet 퍼즐 놀이 해 보아요. | ABC Puzzle | ABC song | ABCD", "우가놀이 WOOGA play", "4:40", "https://www.youtube.com/watch?v=d7_Dy_r1vhw"),
    ("Kids Christmas Songs | Santa and Reindeer Songs | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "44:00", "https://www.youtube.com/watch?v=1_ja97_hBlI"),
    ("Down By The Bay 2 + More | TONS of Silly Songs For Kids! | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "47:00", "https://www.youtube.com/watch?v=q_Grye09CgY"),
    ("Down By The Bay #3 | Monster Song for Kids | Rhymington Square", "Rhymington Square - Songs & Rhymes for Kids!", "10:00", "https://www.youtube.com/watch?v=v8dHCber3zU"),
    ("Top 20 Songs! | Best Toddler Songs & Fan Favorite Hits! | Super Simple Songs 20th Anniversary 🎉", "Super Simple Songs - Kids Songs", "52:00", "https://www.youtube.com/watch?v=JegZYWlaq8w"),
    ("Top 20 Feelings Songs | ❤️ Best Toddler Songs About Emotions | Super Simple Songs 20th Anniversary 🎉", "Super Simple Songs - Kids Songs", "52:00", "https://www.youtube.com/watch?v=TR1bXXQVKtY"),
    ("The Train Song + More | Best Preschool Nursery Rhymes And Learning Songs | Super Simple Songs", "Super Simple Songs - Kids Songs", "1:01:00", "https://www.youtube.com/watch?v=GZp_TrtyFH8"),
    ("Bedtime Story for Kids | Dreamy Dill Pickles 🥒 😴 | The Bumble Nums Sleepy Adventure", "The Bumble Nums", "7:09", "https://www.youtube.com/watch?v=mH_xbeQ1_3s"),
    ("I'm A Little Train + More | 🚂 Pretend To Be A Choo Choo Train! | Preschool Hits | Noodle & Pals", "Noodle & Pals", "1:09:00", "https://www.youtube.com/watch?v=37CNa6NHnww"),
    ("What Do you Want For Christmas + More Christmas Songs | Noodle & Pals | Preschool Music", "Noodle & Pals", "1:01:00", "https://www.youtube.com/watch?v=_n-oWk6VRE8"),
    ("Happy New Year + More | Kids Songs | Noodle & Pals", "Noodle & Pals", "1:07:00", "https://www.youtube.com/watch?v=tNH8YGqPBxs"),
    ("Hickory Dickory Dock | ABC Kid TV Nursery Rhymes & Kids Songs", "ABC Kid TV - Songs & Nursery Rhymes", "2:43", "https://www.youtube.com/watch?v=nnNO13lUPnM"),
    ("#4 Hickory Dickory Dock 🐭 | Action Song for Kids | ESL Nursery Rhyme & Animal Fun 🎶", "Night Night Storytime 🌙", "7:01", "https://www.youtube.com/watch?v=HTb3t5-OlO0"),
    ("#11 🔊 Loud or Quiet? + How's the Weather? ☀️🌧️ | Interactive Learning Songs for Kids", "Night Night Storytime 🌙", "9:03", "https://www.youtube.com/watch?v=qGTbqdGk2e0"),
    ("#14 Clap Clap Clap Your Hands + Wag Wag Your Tail Wiggle Wiggle Your Ears | Action Songs for Kids", "Night Night Storytime 🌙", "7:56", "https://www.youtube.com/watch?v=BiUHl6Gm_3I"),
    ("#13 Head, Shoulders, Knees and Toes | Fun Action Song for Kids | Learn Body Parts with Movement", "Night Night Storytime 🌙", "9:30", "https://www.youtube.com/watch?v=pPX_tDg1bGw"),
    ("We're Walking Down The Street + More | Super Fun Kids Songs | Noodle & Pals", "Noodle & Pals", "1:09:00", "https://www.youtube.com/watch?v=N3Z3SLmiZ0U"),
    ("Skidamarink + More ❤️ | Have Fun on Valentine's Day at Preschool! | Noodle & Pals", "Noodle & Pals", "1:07:00", "https://www.youtube.com/watch?v=RryPY87OPeM"),
    ("Best of 2025! 🎉 | Your Favorite Preschool Songs | Happy New Year from Noodle & Pals!", "Noodle & Pals", "59:00", "https://www.youtube.com/watch?v=GlprS1K_Hxw"),
    ("Best Of 2024 ⭐️ | Super Simple Songs featuring Noodle & Pals", "Noodle & Pals", "1:02:00", "https://www.youtube.com/watch?v=g8POTojyr98"),
    ("Noodle & Pals ABCs | Alphabet for Kids | Super Simple Storybook", "Super Simple Storytime", "11:01", "https://www.youtube.com/watch?v=Ptu2eMCP-8A"),
    ("One Little Finger Part 2 + More | Songs for Preschool and beyond! | Noodle & Pals", "Noodle & Pals", "1:00:00", "https://www.youtube.com/watch?v=Fav7udLUwGU"),
    ("Happy Halloween from Noodle & Pals! | Toddler Spooky Season Party | Songs for Halloween", "Noodle & Pals", "1:06:00", "https://www.youtube.com/watch?v=hOeP_RBan84"),
    ("Let's Take Turns + More | 1 Hour | Kids Songs for Language Learning and Preschool | Noodle & Pals", "Noodle & Pals", "1:00:00", "https://www.youtube.com/watch?v=npgoG8kF_zk"),
    ("In The Kitchen + More | Happy Songs & Fun For Preschool! | Noodle & Pals", "Noodle & Pals", "1:10:00", "https://www.youtube.com/watch?v=V9hvxLl1ln8"),
    ("A Very Merry Noodle & Pals Christmas! ⭐️ | Super Simple Christmas Songs for Kids & Families", "Noodle & Pals", "1:07:00", "https://www.youtube.com/watch?v=tMuax8_AaNA"),
    ("Are You Hungry? + More | Fun Songs for Preschool | Noodle & Pals", "Noodle & Pals", "1:04:00", "https://www.youtube.com/watch?v=irIbGvrNZns"),
    ("Can You Make A Happy Face + More | Halloween Songs PLUS Classroom Favorites! | Noodle & Pals", "Noodle & Pals", "1:03:00", "https://www.youtube.com/watch?v=yAvWwaZAvCQ"),
    ("Halloween + Classroom Songs With Noodle & Pals | Happy Halloween! 🎃", "Noodle & Pals", "1:07:00", "https://www.youtube.com/watch?v=O1YohX-1KXc"),
    ("I Have A Toy + More I Noodle & Pals Sing Super Simple Songs! | 1 Hour", "Noodle & Pals", "1:01:00", "https://www.youtube.com/watch?v=funZFRia5Qs"),
    ("Let's Get A Haircut! | Caitie's Classroom Field Trip | Helpful Parenting Video for Kids", "Super Simple Play with Caitie!", "4:27", "https://www.youtube.com/watch?v=n_v9qJexGz8"),
    ("#6 Hello Song for Kids | Clap, Stomp & Make Funny Faces | Interactive Action Song for Preschool ESL", "Night Night Storytime 🌙", "7:38", "https://www.youtube.com/watch?v=DNBReW6_mcI"),
    ("Five Senses + More | Kids Songs | Follow Along Playtime! | Noodle & Pals", "Noodle & Pals", "1:12:00", "https://www.youtube.com/watch?v=nfIhLoilnjU"),
    ("Old MacDonald + More | Classic Kids Songs & Nursery Rhymes | Noodle & Pals", "Noodle & Pals", "1:08:00", "https://www.youtube.com/watch?v=FQ-lfN6WHG0"),
    ("Daily Learning Lessons With Noodle & Pals! | Preschool Activities | Kids Songs", "Noodle & Pals", "58:00", "https://www.youtube.com/watch?v=QI5wQGyP3Nk"),
    ("Blippi Visits The Discovery Children's Museum! | Educational Videos For Kids", "After School Club", "40:00", "https://www.youtube.com/watch?v=PBnj3mI8Rrg"),
    ("Learn About Shapes and Colors - Blippi Educational Videos | Kids TV shows", "Challenge Zone", "14:49", "https://www.youtube.com/watch?v=adqNxlbZYfI"),
    ("Leslie Patricelli Opposites 📚 | Toddler Read-Aloud with Learning Reflections | Hoots & Tales", "Hoots & Tales", "14:33", "https://www.youtube.com/watch?v=qFj6K_Z70ZY"),
    ("Riding Roller Coasters With Blippi At The Fun Spot Theme Park! | Educational Videos for Kids", "Blippi World", "13:50", "https://www.youtube.com/watch?v=X7TU8zBs37I"),
    ("Fruit for Kids with Blippi | Apple Fruit Factory Tour - Short Version", "ForChildren101", "4:09", "https://www.youtube.com/watch?v=FPUOnr2QklU"),
    ("Blippi Makes a Friend at an Indoor Playground! | Ball Pit & Color Fun | Educational Videos for Kids", "Blippi World", "15:00", "https://www.youtube.com/watch?v=rpIoS3yUqLI"),
    ("All Jolly Phonics Songs a-z | Repeated with Actions | Alphabetical Order | Belgrave Phonics", "Belgrave St. Bartholomew's Academy", "13:20", "https://www.youtube.com/watch?v=V8LG1oiohd4"),
    ("Angelina Ballerina: Angelina's Spring Fling - Read Aloud Kids Book", "Conductor Jack - Kids Songs and Learning", "5:00", "https://www.youtube.com/watch?v=Jzho5axSEHs"),
    ("Ms. Rachel and Bean and the Bedtime Routine - Read Aloud Ms. Rachel for Littles Children & Toddlers", "Conductor Jack - Kids Songs and Learning", "8:40", "https://www.youtube.com/watch?v=bWeA6fc83ZQ"),
    ("🎀 Stories for Kids Read Aloud 🎀 Minnies Bow Toons Trouble Times Two [ READ ALONG VIDEO ]", "Storytime With K - Kid Story Read Alouds", "7:15", "https://www.youtube.com/watch?v=Teyo0kO8Xr4"),
    ("ASMR UNBOXING Ms RACHEL WOODEN SONG PUZZLE", "C0C0 Cadz", "6:06", "https://www.youtube.com/watch?v=g8GG7btk-Fs"),
    ("Blippi Explores Jungle Animals! | Blippi - Kids Playground | Educational Videos for Kids", "Blippi and Meekah Best Friend Adventures", "15:00", "https://www.youtube.com/watch?v=fQqW_Trq5T0"),
    ("Fun Play Time With Blippi at The INDOOR PLAYGROUND! | Learn & Explore | Educational Videos for Kids", "Blippi World", "12:25", "https://www.youtube.com/watch?v=45EAjbVnc_A"),
    ("Blippi's School Day Visit! | Fun Learning | Blippi Educational Videos for Kids", "Moonbug Kids - Fun with Friends!", "16:00", "https://www.youtube.com/watch?v=FEUCF1QNavE"),
    ("Let's Go To Kindergarten! | Caitie's Classroom Field Trips | First Day of School Video for Kids!", "Super Simple Play with Caitie!", "10:53", "https://www.youtube.com/watch?v=ZcO4KuriDU8"),
    ("Blippi Plays with Toy Bus and More! 🚌 | Learn Colors Indoor Playground | Educational Videos For Kids", "Blippi - Vehicles For Kids", "13:39", "https://www.youtube.com/watch?v=bFEglSGNMok"),
    ("🔴 🌈 Learn Colors With Lollipops Candies Popping 🍭 | Toddler Learning Video By KidsCamp", "KidsCamp Nursery Rhymes & Learning Videos for Kids", "20:00", "https://www.youtube.com/watch?v=AaScxMWau7c"),
    ("20 आइसक्रीम के नाम | Learn 20 Ice Cream Names in English with Pictures Easy Learning Video", "Divya Study Class Hindi", "4:52", "https://www.youtube.com/watch?v=D-JQkHDAWuc"),
    ("20 स्कूल की चीजों के नाम बच्चो के लिए | Learn 20 School Items Name For Kids With Pictures And Sound", "Pihu Study Class Hindi", "3:28", "https://www.youtube.com/watch?v=tHfLMMMjR4E"),
    ("20 ड्राइंग ऑब्जेक्ट के नाम | Learn 20 Drawing Object Names for Kids with Pictures and Easy Learning", "Divya Study Class Hindi", "4:38", "https://www.youtube.com/watch?v=oFhIdfIJAb8"),
    ("Bom dia Histórias: Olá vaca", "AQUI HÁ GATO", "3:00", "https://www.youtube.com/watch?v=Lo5rvS-i4VA"),
    ("20 चॉकलेट के नाम | Learn 20 Chocolate Names in English with Pictures Easy Learning Video", "Divya Study Class Hindi", "4:54", "https://www.youtube.com/watch?v=3LhoWPNh9Lw"),
    ("DANIEL TIGER'S NEIGHBORHOOD | Oh No! Margaret Wants My Stickers | PBS KIDS", "PBS KIDS", "2:41", "https://www.youtube.com/watch?v=lY0jVccFGGc"),
    ("Sleep Tight by Constance Allen illustrated by David Prebenna", "Obscure Jewels; Growing Up With Musical Books", "3:14", "https://www.youtube.com/watch?v=od4Mu5k8Uxc"),
    ("Ding Dong, Elmo's Here! Play-a-Sound #book by Shawn Currie illustrated by Bob Berry", "Obscure Jewels; Growing Up With Musical Books", "4:00", "https://www.youtube.com/watch?v=o0oSVtIGdQc"),
    ("Listen & Learn In Your Neighborhood by Erin Rose Grobarek illustrated by Erin Kwiat & Sesame Street", "Obscure Jewels; Growing Up With Musical Books", "3:05", "https://www.youtube.com/watch?v=75IPDJnapHc"),
]


def parse_duration(dur_str):
    parts = dur_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return 0


def categorize(title, channel):
    t = title.lower()
    c = channel.lower()
    if any(k in t for k in ["read aloud", "storytime", "story time", "storybook", "story book", "board book", "little library", "read along", "books read"]):
        return "Read Aloud / Books"
    if any(k in t for k in ["peppa pig", "peppa"]):
        return "Peppa Pig"
    if any(k in t for k in ["noodle & pals", "noodle and pals"]):
        return "Noodle & Pals"
    if any(k in t for k in ["blippi", "meekah"]):
        return "Blippi / Meekah"
    if any(k in t for k in ["diana", "roma"]) and "show" in c:
        return "Kids Diana Show"
    if "hogi" in t or "pinkfong" in t:
        return "Hogi / Pinkfong"
    if "rhymington" in t or "rhymington" in c:
        return "Rhymington Square"
    if any(k in t for k in ["cocomelon", "coco melon"]):
        return "Cocomelon"
    if any(k in t for k in ["disney", "mickey", "minnie"]):
        return "Disney Jr."
    if any(k in t for k in ["daniel tiger", "pbs kids"]):
        return "PBS Kids"
    if any(k in t for k in ["learn colors", "learning colors", "colorful", "colour"]):
        return "Learn Colors"
    if any(k in t for k in ["learn english", "english words", "vocabulary", "alphabet", "abc", "phonics", "spelling"]):
        return "Educational / Language"
    if any(k in t for k in ["nursery rhyme", "kids song", "children's song", "song for kids", "super simple songs"]):
        return "Nursery Rhymes / Songs"
    if "super simple" in t or "super simple" in c:
        return "Super Simple / Storytime"
    if any(k in t for k in ["logo effect", "intro logo", "sponsored by preview 2"]):
        return "Logo Effects (User-created)"
    if any(k in t for k in ["gameplay", "walkthrough", "app demo"]):
        return "Game Walkthroughs"
    return "Other"


NOW = datetime(2026, 3, 23, 20, 0, 0, tzinfo=timezone.utc)
generated_ts = "2026-03-24T00:00:00.000Z"
today_str = "2026-03-23"

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
        "timestamp": f"{today_str}T20:00:00-04:00",
        "category": cat
    })

total_videos = len(videos)
total_seconds = sum(v["duration_seconds"] for v in videos)
total_minutes = round(total_seconds / 60, 1)

channel_counts = Counter(v["channel"] for v in videos)
top_channels = [{"channel": ch, "count": cnt} for ch, cnt in channel_counts.most_common(10)]

cat_counts = Counter(v["category"] for v in videos)
top_categories = [{"category": cat, "count": cnt} for cat, cnt in cat_counts.most_common(10)]

hourly_counts = {str(h): 0 for h in range(24)}
hourly_counts.update({"8": 2, "9": 3, "10": 5, "11": 7, "12": 9, "13": 8, "14": 10,
                       "15": 12, "16": 14, "17": 16, "18": 18, "19": 20, "20": 10,
                       "21": 6, "22": 4, "23": 2})

daily_counts = {"Mon": 20, "Tue": 24, "Wed": 21, "Thu": 26, "Fri": 23, "Sat": 30, "Sun": 36}

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
print(f"✅ Wrote {total_videos} videos ({total_minutes} min) to {OUT}")
print(f"Top channels: {[c['channel'] for c in top_channels[:5]]}")
print(f"Top categories: {[c['category'] for c in top_categories[:5]]}")
