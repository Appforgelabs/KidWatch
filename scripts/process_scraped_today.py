#!/usr/bin/env python3
"""Process scraped YouTube history data into history.json format - 2026-03-17."""
import json
import re
from datetime import datetime, timezone
from collections import Counter

SCRAPED_VIDEOS = [
{"title":"Let's Blow A Bubble | Bubbles Song for Kids | Rhymington Square","channel":"Rhymington Square - Songs & Rhymes for Kids!","duration":"2:33","url":"https://www.youtube.com/watch?v=1Xpfyifb5lI"},
{"title":"There's A Monster In My Tummy #2 | Fun Food Song for Kids! | Rhymington Square","channel":"Rhymington Square - Songs & Rhymes for Kids!","duration":"2:34","url":"https://www.youtube.com/watch?v=qqblIOqoVJE"},
{"title":"There's A Monster In My Tummy | Hungry Kids Song | Rhymington Square","channel":"Rhymington Square - Songs & Rhymes for Kids!","duration":"2:35","url":"https://www.youtube.com/watch?v=Lx4ZB7RgzpY"},
{"title":"Making A Card For My Valentine | Monster Song for Kids | Rhymington Square","channel":"Rhymington Square - Songs & Rhymes for Kids!","duration":"2:56","url":"https://www.youtube.com/watch?v=sLOOrLeYd_w"},
{"title":"Let's Go For A Walk Outside | Kids Song | Rhymington Square","channel":"Rhymington Square - Songs & Rhymes for Kids!","duration":"4:20","url":"https://www.youtube.com/watch?v=7sdocMe5DV4"},
{"title":"Apples And Bananas | Monster Song for Kids | Rhymington Square","channel":"Rhymington Square - Songs & Rhymes for Kids!","duration":"3:07","url":"https://www.youtube.com/watch?v=Ir_aVUKUCQs"},
{"title":"Alarm Clocked Out | Minnie's Bow-Toons | @disneyjr","channel":"Disney Jr.","duration":"3:01","url":"https://www.youtube.com/watch?v=RMP6SsAHxP4"},
{"title":"Tres Gatitos (Three Little Kittens) | Canciones infantiles en Español | ChuChu TV","channel":"ChuChuTV Español","duration":"4:14","url":"https://www.youtube.com/watch?v=DzldmZvyBhQ"},
{"title":"Let's Make a Pizza | NEW TASTY VIDEO | Mother Goose Club Phonics Songs","channel":"Mother Goose Club","duration":"2:52","url":"https://www.youtube.com/watch?v=L6nalE3OwxA"},
{"title":"Chiku Saves A Spot + More Good Habits Bedtime Stories & Moral Stories for Kids – ChuChu TV Storytime","channel":"ChuChuTV Storytime for Kids","duration":"13:53","url":"https://www.youtube.com/watch?v=-M-m9oJIzFQ"},
{"title":"Johny Johny Yes Papa Healthy Food plus More Nursery Rhymes & Kids Songs - ChuChuTV Funzone","channel":"Jumblikans by ChuChuTV - Learning Videos for Kids and ChuChu TV Nursery Rhymes & Kids Songs","duration":"31:15","url":"https://www.youtube.com/watch?v=fXLeJjbGitU"},
{"title":"Johny Johny Yes Papa Sports & Games Nursery Rhyme - 3D Rhymes & Songs for Children","channel":"CVS 3D Rhymes & Kids Songs","duration":"3:03","url":"https://www.youtube.com/watch?v=KVVdJUrKoMA"},
{"title":"Johny Johny Yes Papa Nursery Rhyme | Part 3 - 3D Animation Rhymes & Songs for Children","channel":"CVS 3D Rhymes & Kids Songs","duration":"3:07","url":"https://www.youtube.com/watch?v=EA_fbT6oN2k"},
{"title":"ABC Song | Wendy Pretend Play Learning Alphabet w/ Toys & Nursery Rhyme Songs","channel":"Toys and Colors","duration":"6:33","url":"https://www.youtube.com/watch?v=BNTCpF_n6J4"},
{"title":"Color song for kids and toddlers | learn color names | #colorsong #learncolors","channel":"Little Learners Station","duration":"2:22","url":"https://www.youtube.com/watch?v=8nPPiflAejo"},
{"title":"The Colors Song ~ Learn the Colors / Colours ~ LEARN ENGLISH with Natural English","channel":"Natural English","duration":"2:58","url":"https://www.youtube.com/watch?v=pUPM3DtK9so"},
{"title":"Ms. Rachel: 100 First Words - Read Aloud Ms. Rachel for Littles - Children and Toddlers","channel":"Conductor Jack - Kids Songs and Learning","duration":"5:11","url":"https://www.youtube.com/watch?v=r4I9tn5PFR4"},
{"title":"Peekaboo, Where Are You? | A Super Simple Storybook","channel":"Super Simple Storytime","duration":"8:00","url":"https://www.youtube.com/watch?v=k2Bl-YnZXNE"},
{"title":"Peppa Pig Full Episodes | Meet Peppa Pig's family and friends!","channel":"Peppa's Best Bites","duration":"6:07","url":"https://www.youtube.com/watch?v=kyhLMS8sSjM"},
{"title":"Adventure at Children's Museum | Educational Videos for Kids | Hey Tenny!","channel":"Hey Tenny! Learning Videos and Songs for Kids","duration":"11:23","url":"https://www.youtube.com/watch?v=7h2xTbKzUlY"},
{"title":"Learn Colors with Nuts Song 5 | Nursery Rhymes & Kids Songs","channel":"Johny FamilyShow","duration":"2:50","url":"https://www.youtube.com/watch?v=FXBlbrvagPM"},
{"title":"Yes Papa 2 (Colors and Brush Your Teeth Song)","channel":"Ashlynn FAM JAM","duration":"3:23","url":"https://www.youtube.com/watch?v=ynl7O3eyrKM"},
{"title":"Ms. Rachel: Potty Time With Bean - Read Aloud Ms. Rachel for Littles - Children and Toddlers","channel":"Conductor Jack - Kids Songs and Learning","duration":"4:21","url":"https://www.youtube.com/watch?v=2ykFDpIdcmY"},
{"title":"Toddler Language Development: Learning Animals Names, Colors & ABCs with Confidence with Ms. Rachel","channel":"Learn & Play with Jayli-Toddler Learning Videos","duration":"33:37","url":"https://www.youtube.com/watch?v=nmEOdnNGRok"},
{"title":"Peppa Pig Official Channel | Peppa Pig and Suzy Sheep are Best Friends","channel":"Peppa Pig's Big Adventures","duration":"13:51","url":"https://www.youtube.com/watch?v=xCxku3tfOCw"},
{"title":"Johny Johny Yes Papa Nursery Rhymes Collection - 3D Rhymes & Songs for Children","channel":"CVS 3D Rhymes & Kids Songs","duration":"8:54","url":"https://www.youtube.com/watch?v=Z68hf7dfhe8"},
{"title":"Best Peppa Pig Learning Video for Kids - George's Birthday Party Adventure!","channel":"Genevieve's Playhouse - Learning Videos for Kids","duration":"11:24","url":"https://www.youtube.com/watch?v=rmwENNtC9RU"},
{"title":"Cocomelon Outro Logo Super Effect Sponsored By Preview 2 Effect","channel":"Krish Effects 5M","duration":"2:23","url":"https://www.youtube.com/watch?v=manHOf05mhE"},
{"title":"Jugando peppa pig roleplay me agarre un carro de un vídeo de @EdrezLalf","channel":"Carlos Yael Serna Contrerass","duration":"5:29","url":"https://www.youtube.com/watch?v=9VDHJ4VPar8"},
{"title":"peppa the fat belly go to the bus Season 1 episode 1","channel":"Miss Kandice","duration":"13:06","url":"https://www.youtube.com/watch?v=WY8t55anmHk"},
{"title":"Bumble nums collect some grapes games","channel":"Ibrahim","duration":"6:16","url":"https://www.youtube.com/watch?v=CqxeSrx5-I8"},
{"title":"Tdgwvsc","channel":"Kaan","duration":"12:34","url":"https://www.youtube.com/watch?v=lKRLav5lj80"},
{"title":"Diana and Roma intro Effects 60PFS ( Sponsored By: Preview 2 effects ) iL Vocodex","channel":"Yupen Pro Editor","duration":"3:07","url":"https://www.youtube.com/watch?v=VTFu7JKvdHc"},
{"title":"Alice Princess Logo Super Effects (Sponsored By Preview 2 Effects)","channel":"MSC PRO EDIT","duration":"2:09","url":"https://www.youtube.com/watch?v=yOe_5QArWEQ"},
{"title":"Walmart do you like","channel":"Catherine Azez","duration":"2:36","url":"https://www.youtube.com/watch?v=Y_gPif9-k3g"},
{"title":"do you like songs","channel":"SM Store and sm markets tv","duration":"2:48","url":"https://www.youtube.com/watch?v=D5Z2Q19nUYU"},
{"title":"Learn Colours With Tayo The Little Bus ( Inspired By Preview 2 Effects) pt2","channel":"MSC PRO EDIT","duration":"2:50","url":"https://www.youtube.com/watch?v=Olcmq6rgCF8"},
{"title":"BEBEFINN Subscribe Logo Super Effects (Sponsored By Preview 2 Effects)","channel":"MSC PRO EDIT","duration":"4:28","url":"https://www.youtube.com/watch?v=gge16giNAug"},
{"title":"GIANT cocomelon baa baa black sheep clay cracking making 2","channel":"Clay Adventure","duration":"1:58","url":"https://www.youtube.com/watch?v=MULwBb8ZY70"},
{"title":"The roundabouts super simple songs 9 minutes","channel":"king McDonald","duration":"3:22","url":"https://www.youtube.com/watch?v=D-P3vfBUWjc"},
{"title":"Guess The Streaming Logo Sound Netflix, Disney+, HBO, Hulu | Logo Quiz 2025","channel":"Drynox","duration":"5:46","url":"https://www.youtube.com/watch?v=L8Mstg2zw2w"},
{"title":"Visit A Bakery & Make Delicious Cookies! | Caitie's Classroom Field Trip | Food Video for Kids","channel":"Super Simple Play with Caitie!","duration":"5:52","url":"https://www.youtube.com/watch?v=bAJfCfWdFJQ"},
{"title":"Gracie's Corner LIVE Wheels on the Bus, Veggie Dance + More Fun Kids Songs + Nursery Rhymes","channel":"LIVE","duration":"","url":"https://www.youtube.com/watch?v=gm6Mkup8OnM"},
{"title":"Clean Up Song | Gracie's Corner | Kids Songs + Nursery Rhymes","channel":"Gracie's Corner","duration":"2:41","url":"https://www.youtube.com/watch?v=llppYxsVzlE"},
{"title":"Sesame Street: What's Your Name? | Summer Camp Song with @SuperSimpleSongs","channel":"Sesame Street","duration":"1:29","url":"https://www.youtube.com/watch?v=cDbZopIt5Rs"},
{"title":"CoComelon Busy Book Reading And Toy Play | JJ & Friends Figures","channel":"Read Along With Millie's Mummy","duration":"9:17","url":"https://www.youtube.com/watch?v=V73SEwa_JmE"},
{"title":"Ben and Holly's Little Kingdom - Christmas at the North Pole","channel":"Big Ted Storytime","duration":"3:40","url":"https://www.youtube.com/watch?v=X602PMS3wjw"},
{"title":"Peppa Pig Goes To The Theatre | Cartoons for Kids | Full Episode","channel":"Peppa Pig's Big Adventures","duration":"31:30","url":"https://www.youtube.com/watch?v=Ox4zs3Bjbiw"},
{"title":"Fun Kids Music with Cool Instruments!","channel":"Joe Porter","duration":"1:32","url":"https://www.youtube.com/watch?v=_-uhOwIoNl4"},
{"title":"Guess the 2000's Preschool TV Show by the Theme Song","channel":"The Quiz Show","duration":"9:50","url":"https://www.youtube.com/watch?v=PJOZ43H6-nk"},
{"title":"Guess The Household Item Sounds For Kids | 4K","channel":"Little Dreamers Education","duration":"8:31","url":"https://www.youtube.com/watch?v=1ZPStTtE7JI"},
{"title":"Guess The Logo Sound Challenge | McDonald's, TikTok, Netflix, KFC, Pepsi | Logo Quiz 2024","channel":"WhizQuizz","duration":"11:19","url":"https://www.youtube.com/watch?v=H-uYy69qPcQ"},
{"title":"Guess Cartoon tv channel logo by its Sound / Cartoon tv logo Sound / logo quiz","channel":"Empire of Quiz","duration":"8:36","url":"https://www.youtube.com/watch?v=O_OJ2NUJTW0"},
{"title":"Guess logo by Sound / logo theme Sound / logo quiz","channel":"Empire of Quiz and Quiz Jockey","duration":"9:57","url":"https://www.youtube.com/watch?v=5b1_wfYqYi4"},
{"title":"Izzy is going to a birthday party","channel":"Bella!!","duration":"17:11","url":"https://www.youtube.com/watch?v=zpwu0KhRKoU"},
{"title":"Super Simple Songs Playing With My Car Destroyed | Sponsored By: Preview 2 Mokou Deep Fake","channel":"Custom Effects","duration":"3:03","url":"https://www.youtube.com/watch?v=pSh8dQRpbYM"},
{"title":"Happy Kids 10th Birthday Logo Ultimate Effect Edit!","channel":"StejarEffects2004","duration":"1:23","url":"https://www.youtube.com/watch?v=uUb4_2r6oLU"},
{"title":"Super Simple Songs Days Of The Week Intro Logo Sponsored By: Klasky Csupo 2001 Effects","channel":"IApple1234","duration":"4:49","url":"https://www.youtube.com/watch?v=HwKP9h9o7jA"},
{"title":"Super Simple Songs Count Down Stinky Farts Intro Logo | Sponsored By: Gamavision Csupo Effects","channel":"Custom Effects","duration":"4:13","url":"https://www.youtube.com/watch?v=-H1Z_-cK--A"},
{"title":"Super Simple Songs What's Your Name Power Slap Intro Logo | Sponsored By: Gamavision Csupo Effects","channel":"Gintoy Csupo","duration":"4:07","url":"https://www.youtube.com/watch?v=WzScrq4P-y4"},
{"title":"Super Simple Songs Mary Had A Little Lamb Intro Logo Sponsored By: Preview 2 Mokou Deepfake Effects","channel":"IApple1234","duration":"4:19","url":"https://www.youtube.com/watch?v=W-t277uEmYA"},
{"title":"Why Cocomelon Moved From Netflix To Disney+?","channel":"What's On Disney Plus","duration":"2:35","url":"https://www.youtube.com/watch?v=EaNhzUU1XBM"},
{"title":"PinkFong Subscribe Intro Logo Effect Sponsored By Preview 2 Effect","channel":"Krish Effects 5M","duration":"3:19","url":"https://www.youtube.com/watch?v=V-dQZHeK2Qk"},
{"title":"10th Birthday Happy Kids Logo Sponsored By Preview 2 Effects | Inverted","channel":"EuEffectsz","duration":"1:35","url":"https://www.youtube.com/watch?v=1vDahM3SCTc"},
{"title":"Bluey theme song on a lot of instruments!","channel":"Emstepko","duration":"1:42","url":"https://www.youtube.com/watch?v=kOxMvWZOwJo"},
{"title":"Big family winter trip to new york *WITH VOICE* (Jellycat store!) || Toca boca Roleplay","channel":"Toca kitty","duration":"18:07","url":"https://www.youtube.com/watch?v=ei07BXwMeeE"},
{"title":"Goldfish Jingle with A LOT of Cool Instruments!","channel":"Joe Porter","duration":"2:14","url":"https://www.youtube.com/watch?v=Ht7L9xXaD-k"},
{"title":"Marble Plays Famous Songs on new Different Instruments!! | Compilation","channel":"Marble Music by Shaysik","duration":"3:28","url":"https://www.youtube.com/watch?v=dwmyefmvcH8"},
{"title":"Cocomelon theme on a lot of different instruments!","channel":"Emstepko","duration":"1:45","url":"https://www.youtube.com/watch?v=nCVSMnwCVwA"},
{"title":"GORGIE PIG IS A BAD GIRL","channel":"Lemon Liliana","duration":"5:34","url":"https://www.youtube.com/watch?v=cAvQJG8tQYM"},
{"title":"TOCA BOCA HAVALIMANI YOLCULUK YAPTIKK","channel":"Ilkim Gece","duration":"6:36","url":"https://www.youtube.com/watch?v=3qMJILYkMd4"},
{"title":"New Bluey Episodes Coming To Disney+ In 2024 | Disney Plus News","channel":"What's On Disney Plus","duration":"1:55","url":"https://www.youtube.com/watch?v=4IBrg4RJkJc"},
{"title":"Sesame Street: Cookie Monster Mysteries Trailer (2026 Ambies Award Winner)","channel":"Great Pods","duration":"0:49","url":"https://www.youtube.com/watch?v=c1lrIdKA8aE"},
{"title":"Ready, Set, Ride with Elmo Trailer","channel":"Great Pods","duration":"1:04","url":"https://www.youtube.com/watch?v=DwP7PS1Ik-U"},
{"title":"Blippi & Meekah's Road Trip Trailer","channel":"Great Pods","duration":"2:04","url":"https://www.youtube.com/watch?v=GMk00rRWoEk"},
{"title":"Kids songs on fun & weird instruments!","channel":"Emstepko","duration":"1:30","url":"https://www.youtube.com/watch?v=wYbudacdjf4"},
{"title":"Donald and the Frog Prince | Mickey Mouse Clubhouse Full Episode | S1 E8 | @disneyjr","channel":"Disney Jr.","duration":"24:02","url":"https://www.youtube.com/watch?v=2Edh5QqciIQ"},
{"title":"Peppa Celebrates MOTHER'S Day | Peppa Pig Full Episodes | 2 Hours of Kids Cartoons","channel":"Peppa Pig - Official Channel","duration":"45:50","url":"https://www.youtube.com/watch?v=YgYVjj0AMKw"},
{"title":"Peppa Pig: Evie | Peppa Pig Read Aloud Story for Toddlers","channel":"Read Along With Millie's Mummy","duration":"3:02","url":"https://www.youtube.com/watch?v=lKQwZOiP54U"},
{"title":"Peppa pig Peppa's first glasses","channel":"Happily ever after storytime","duration":"4:02","url":"https://www.youtube.com/watch?v=6xR_9eJAEQg"},
{"title":"Peppa Pig and the Great Vacation","channel":"KB00KIE","duration":"4:49","url":"https://www.youtube.com/watch?v=Ng-nXlRJ0qY"},
{"title":"Peppa va a la biblioteca","channel":"la tete dans les livres","duration":"4:35","url":"https://www.youtube.com/watch?v=RYjAHPy56fw"},
{"title":"Peppa Pig and the Easter Rainbow","channel":"KB00KIE","duration":"3:00","url":"https://www.youtube.com/watch?v=MdoyCABdYb0"},
{"title":"Happy Birthday To You Song | Good Habits | Peppa Pig Nursery Rhymes & Kids Songs","channel":"Peppa Pig - Nursery Rhymes and Kids Songs","duration":"4:11","url":"https://www.youtube.com/watch?v=SonIS1EjsmI"},
{"title":"Peppa Buries George in the Sand | The Beach Song | Peppa Pig Nursery Rhymes & Kids Songs","channel":"Peppa Pig - Nursery Rhymes and Kids Songs","duration":"4:09","url":"https://www.youtube.com/watch?v=NJxPwHIU0I4"},
{"title":"Doctor Daisy, MD | S1 E25 | Full Episode | Mickey Mouse Clubhouse | @disneyjr","channel":"Disney Jr.","duration":"24:01","url":"https://www.youtube.com/watch?v=e0O6lW38ew4"},
{"title":"Minnie Red Riding Hood | S1 E18 | Full Episode | Mickey Mouse Clubhouse | @disneyjr","channel":"Disney Jr.","duration":"24:01","url":"https://www.youtube.com/watch?v=oOy9ykjLhnk"},
{"title":"Mickey Mouse Clubhouse Halloween Mickey's Treat Full Episode | S1 E17 | @disneyjr","channel":"Disney Jr.","duration":"24:01","url":"https://www.youtube.com/watch?v=i6bORQh_9LQ"},
{"title":"Let's Make a Pizza + More | Mother Goose Club Nursery Rhymes","channel":"Mother Goose Club","duration":"20:46","url":"https://www.youtube.com/watch?v=3RXZpCQ0FOI"},
{"title":"Kids Music with Cool Musical Instruments!","channel":"Joe Porter","duration":"1:37","url":"https://www.youtube.com/watch?v=Vaw3rRdWzZg"},
{"title":"Mickey Mouse Clubhouse Goofy's Bird Full Episode | S1 E3 | @disneyjr","channel":"Disney Jr.","duration":"24:02","url":"https://www.youtube.com/watch?v=4BcnPdCimAk"},
{"title":"Pete the Cat Compilation | I Love My White Shoes | Rocking in My School Shoes | Four Groovy Buttons","channel":"Cupcake Storytime and Chirpy Learners","duration":"15:43","url":"https://www.youtube.com/watch?v=Tl6jX9W1t70"},
{"title":"Pete the Cat I Love My White Shoes | Animated Book | Read aloud","channel":"LolliPop Animated Book","duration":"3:57","url":"https://www.youtube.com/watch?v=-GSnmRZlgc4"},
{"title":"Read With Me: 100 Words to Say I Love You | Gentle Story Read Aloud for Toddlers","channel":"Cozy Nest Reading","duration":"6:15","url":"https://www.youtube.com/watch?v=S67gjxFvuRs"},
{"title":"Can You Say... Banana, Dog, Book, Boots, Bike | Learn with Yakka Dee! | FULL EPISODES | BBC Kids","channel":"BBC Kids and Yakka Dee! - Toddler Learning","duration":"25:42","url":"https://www.youtube.com/watch?v=_WQttIwdetU"},
{"title":"Learn Colors with Nuts Song 2 | Nursery Rhymes & Kids Songs","channel":"Johny FamilyShow","duration":"2:51","url":"https://www.youtube.com/watch?v=O3TgmBdabiM"},
{"title":"Learn Colors with Nuts Song 3 | Nursery Rhymes & Kids Songs","channel":"Johny FamilyShow","duration":"2:53","url":"https://www.youtube.com/watch?v=wSEw3KpbR60"},
{"title":"Oliver Diana and Roma show the Safety Rules on board the Airplane","channel":"OLIVER SHOW","duration":"4:36","url":"https://www.youtube.com/watch?v=Lcl2duHV1KE"},
{"title":"Lego School Adventure for Kids!","channel":"Vlad and Niki ESP","duration":"17:08","url":"https://www.youtube.com/watch?v=sQEFIH8V9d8"},
{"title":"Kids Dress Up as Superheroes - A Christmas Toy Story for Kids","channel":"Vlad and Niki","duration":"16:09","url":"https://www.youtube.com/watch?v=o27-ifHcvNE"},
{"title":"Alice and her aunt pack a suitcase and go on a trip.","channel":"Alice_Princesa","duration":"15:19","url":"https://www.youtube.com/watch?v=dSImVYSSGNo"},
{"title":"Alice and story about helping new friends","channel":"Alice","duration":"16:14","url":"https://www.youtube.com/watch?v=RNSsKunKK8U"},
{"title":"Kids & Mall Adventures Safety Rules from Dad","channel":"Vani Mani","duration":"21:16","url":"https://www.youtube.com/watch?v=MO32xvcJsTg"},
{"title":"Children learn safety rules in the mall - useful stories with Chris","channel":"Vlad and Niki ESP","duration":"12:50","url":"https://www.youtube.com/watch?v=VKwqYgcUm08"},
{"title":"Alice's Adventures and the Mall Escalator - Safety Lessons for Kids","channel":"Alice Putri","duration":"12:30","url":"https://www.youtube.com/watch?v=3RqLHzLJ4KA"},
{"title":"Nat and Essie Playfully and Peppa Pig's School Classroom Set","channel":"Nat and Essie","duration":"4:50","url":"https://www.youtube.com/watch?v=Ada91JqNc6A"},
{"title":"Peppa Pig Dress Up Challenge | Find the Real Character!","channel":"Kids DingDong","duration":"3:05","url":"https://www.youtube.com/watch?v=FrpYYmXUJO4"},
{"title":"Baby Shark Huge St. Patrick's Day Tantrum At SpongeBob Burger King","channel":"Storytime with Sonia Panda","duration":"4:51","url":"https://www.youtube.com/watch?v=_RKpRNKDK5Q"},
{"title":"Nastya and dad - the story of how important it is to wash hands","channel":"Like Nastya","duration":"4:05","url":"https://www.youtube.com/watch?v=0dMcuLi0RV0"},
{"title":"Diana and Roma fun play at the theme park Peppa Pig","channel":"Kids Diana Show","duration":"6:39","url":"https://www.youtube.com/watch?v=3CvdLQnqmF4"},
{"title":"Peppa Pig Jumps to the Sky | Family Kids Cartoon","channel":"Peppa Pig - Official Channel","duration":"14:32","url":"https://www.youtube.com/watch?v=K6SxdYVqZxk"},
{"title":"Peppa pig: All instances where one or more characters say Hooray","channel":"T1 Account","duration":"2:16","url":"https://www.youtube.com/watch?v=efNm1Db0dOM"},
{"title":"Airplane challenge with Vlad and Niki","channel":"Vlad and Niki","duration":"5:18","url":"https://www.youtube.com/watch?v=q-GDy0sd77M"},
{"title":"Diana and Roma show the Safety Rules on board the Airplane","channel":"Kids Diana Show","duration":"9:00","url":"https://www.youtube.com/watch?v=NifKNSpp0_4"},
{"title":"Challenge the plane with Vlad and Niki and other fun adventures for kids","channel":"Vlad and Niki ARA Collection","duration":"10:49","url":"https://www.youtube.com/watch?v=nkynCUiIDnU"},
{"title":"Nastya and dad play with lego","channel":"Like Nastya","duration":"4:52","url":"https://www.youtube.com/watch?v=9TkR9226c6o"},
{"title":"Learn Colors with Vegetable Song | Nursery Rhymes & Kids Songs","channel":"Sunny Kids Show","duration":"2:51","url":"https://www.youtube.com/watch?v=M_dRWprVKbM"},
{"title":"Noodle and pals: the wheels on the bus and more!","channel":"Red studios 10","duration":"8:42","url":"https://www.youtube.com/watch?v=zdSRpP4wlu4"},
{"title":"happy new year 2024 put on your shoes noddle and pals vs super simple songs","channel":"Mario 64 and Logan Orozco The Object Thingy OSL","duration":"3:08","url":"https://www.youtube.com/watch?v=HZFcK3hFWzk"},
{"title":"Noodle and Pals - If You're Happy English vs Spanish","channel":"Shawna Stehman","duration":"1:49","url":"https://www.youtube.com/watch?v=2EYis5yAgY8"},
{"title":"Roma and Diana visit Oliver's Cafe","channel":"Kids Roma Show","duration":"5:05","url":"https://www.youtube.com/watch?v=FESRSBaXLQ8"},
{"title":"four songs do you like disgusting food super simple songs","channel":"SM Store and sm markets tv","duration":"2:28","url":"https://www.youtube.com/watch?v=0RPs6Z9SBGw"},
{"title":"Do You Like Super Simple Songs Quadparison (Portuguese) (Most Popular Video)","channel":"JOSEFINA PONCE (DO NOT HACK)","duration":"2:36","url":"https://www.youtube.com/watch?v=dXSPon2PLbw"},
{"title":"Peppa Pig theme on 30 TEMU instruments","channel":"Emstepko","duration":"1:42","url":"https://www.youtube.com/watch?v=9MTDde8WGM0"},
{"title":"Cocomelon ant piracy screen (real) @cocomelon anti piracy","channel":"Lori Belardinella","duration":"2:43","url":"https://www.youtube.com/watch?v=NF46bAbqRnc"},
{"title":"Caillou Gets A Job At Chuck E Cheese's / Ungrounded","channel":"Abel The GoAnimator Extras!","duration":"1:39","url":"https://www.youtube.com/watch?v=gsSk315PDZY"},
{"title":"Absolute cinema","channel":"Gilbert","duration":"12:12","url":"https://www.youtube.com/watch?v=nLqy5l-VtgU"},
{"title":"Peppa and george & the 15 seconds!","channel":"mickyfan productions","duration":"15:24","url":"https://www.youtube.com/watch?v=WUdnGveMmps"},
{"title":"ITS TO SLIPPERY","channel":"Lemon Liliana","duration":"3:40","url":"https://www.youtube.com/watch?v=-tUtIm5Q-UA"},
{"title":"Oh no! Polly Parrot dropped her balloon!","channel":"Lemon Liliana","duration":"3:13","url":"https://www.youtube.com/watch?v=yT4B-bzLa8Y"},
{"title":"Wat happened daddy?!","channel":"Lemon Liliana","duration":"3:53","url":"https://www.youtube.com/watch?v=6GbbirFAuyo"},
{"title":"New Cocomelon Outro Over 1 Million times","channel":"Sorry Ear","duration":"2:52","url":"https://www.youtube.com/watch?v=0TZTHn3KyR4"},
{"title":"Cocomelon Outro Logo Effect Sponsored By Preview 2 Effect","channel":"Krish Effects 5M","duration":"2:23","url":"https://www.youtube.com/watch?v=mwpJ6dIJArk"},
{"title":"Cocomelon Outro Logo Effects Sponsored By Klasky Csupo 2001 Effects | Inverted","channel":"EuEffectsz","duration":"3:00","url":"https://www.youtube.com/watch?v=L1oinDpPeG0"},
{"title":"Peppa ! Come On Boys ! Pull ! - Effects (Sponsored By: Preview 2 Effects)","channel":"Capculacayyy","duration":"3:51","url":"https://www.youtube.com/watch?v=eIu0aPVRpdc"},
{"title":"Peppa pig story","channel":"I love Gravy (Sydney's Version)","duration":"6:16","url":"https://www.youtube.com/watch?v=o8N7kjobf8g"},
{"title":"Peppa Pig skips school going to join London Fire Brigade","channel":"Hundmann Aviation and Transit Fan","duration":"5:06","url":"https://www.youtube.com/watch?v=wivMniVFbpU"},
{"title":"Gorge esta solo...","channel":"Dead rails tips","duration":"9:17","url":"https://www.youtube.com/watch?v=c-artEQ9rkI"},
{"title":"Peppa Pig Plays Minecraft in Real Life. Cartoon parody.","channel":"Mushroom Rain","duration":"2:13","url":"https://www.youtube.com/watch?v=ZRyf6rrlvtQ"},
{"title":"Peppa Pig skips school going to Disney World (Mega Grounded)","channel":"Dog Man Network","duration":"2:28","url":"https://www.youtube.com/watch?v=3AYdob_MMFo"},
{"title":"DJ Played Peppa Pig Roleplay On Roblox","channel":"Jacqueline","duration":"15:00","url":"https://www.youtube.com/watch?v=0z1KtVDwI6Y"},
{"title":"peppa the fat belly go to the bus Season 1 episode 2","channel":"Miss Kandice","duration":"13:19","url":"https://www.youtube.com/watch?v=dtRS_dmfik4"},
{"title":"Peppa Pig and Daddy Pig playing Minecraft in real life. Cartoon parody.","channel":"Mushroom Rain","duration":"3:00","url":"https://www.youtube.com/watch?v=WOZiDD7Pn7s"},
{"title":"David Goes To School ANIMATED VIDEO","channel":"Storytime with Sonia Panda","duration":"5:01","url":"https://www.youtube.com/watch?v=16EpghdisvE"},
{"title":"That's Not Funny David Animated Video","channel":"Storytime with Sonia Panda","duration":"4:20","url":"https://www.youtube.com/watch?v=wxVoO0wYPkA"},
{"title":"No, David Funny Animated Video","channel":"Storytime with Sonia Panda","duration":"3:53","url":"https://www.youtube.com/watch?v=FBumlcEqxJA"},
{"title":"David goes to school! - Animated Children's Books | Kids Books Read Aloud","channel":"Leho Lee","duration":"3:37","url":"https://www.youtube.com/watch?v=jIj2aEE2SdM"},
{"title":"David Gets In Trouble","channel":"Storytime with Sonia Panda","duration":"10:04","url":"https://www.youtube.com/watch?v=r00N3Krrhl4"},
{"title":"Caillou dancing","channel":"single word","duration":"2:52","url":"https://www.youtube.com/watch?v=BKwTFpwF91I"},
{"title":"MY MORNING ROUTINE | * With Voice * |","channel":"Bella!!","duration":"20:53","url":"https://www.youtube.com/watch?v=-H4zPClYQ30"},
{"title":"Big family aesthetic morning routine *WITH VOICE* || Toca boca Roleplay","channel":"Toca kitty","duration":"12:08","url":"https://www.youtube.com/watch?v=X7YrdJvdorU"},
{"title":"TOCA WORLD STORIES!!!","channel":"toca_sireen","duration":"12:10","url":"https://www.youtube.com/watch?v=1mC-CR8AtrA"},
{"title":"Morning routine! (Tysm for blowing this vid up!!)","channel":"Dragonz","duration":"10:21","url":"https://www.youtube.com/watch?v=Cyo5UbnXGcQ"},
{"title":"single mom with twins fall aesthetic morning routine *WITH VOICE* II Toca boca roleplay","channel":"Toca kitty","duration":"11:24","url":"https://www.youtube.com/watch?v=ofYliuUwq_o"},
{"title":"First day of kindergarten!! *WITH VOICE* II Toca boca Roleplay","channel":"Toca kitty","duration":"15:28","url":"https://www.youtube.com/watch?v=IVglTQpWSm0"},
{"title":"Single mom with twins aesthetic night routine ~ *WITH VOICE* Toca boca roleplay","channel":"Toca kitty","duration":"10:51","url":"https://www.youtube.com/watch?v=-tqeKEnKUOU"},
{"title":"First day of school! *GONE WRONG* (WITH VOICE) || Toca Boca Roleplay","channel":"Toca kitty","duration":"19:21","url":"https://www.youtube.com/watch?v=yz5tkGDJJVc"},
{"title":"Toca Boca","channel":"Adalyn S","duration":"4:20","url":"https://www.youtube.com/watch?v=7gpBDiZ4YS0"},
{"title":"super simple songs clay cracking ASMR 3 #38 - stress relief , satisfying video","channel":"FUNNY CRISPY ASMR","duration":"1:50","url":"https://www.youtube.com/watch?v=ykXv6YpdkwA"},
{"title":"The Feelings Song","channel":"Miss Molly","duration":"5:05","url":"https://www.youtube.com/watch?v=-J7HcVLsCrY"},
{"title":"Tales From The Trunk | Pete The Cat & His Four Groovy Buttons by Eric Litwin | Story Book For Kids","channel":"CC Kids TV","duration":"3:40","url":"https://www.youtube.com/watch?v=00GmvoktQuA"},
{"title":"Seasons Song","channel":"Have Fun Teaching","duration":"4:06","url":"https://www.youtube.com/watch?v=8ZjpI6fgYSY"},
{"title":"Goldilocks and the Three Bears Song | Fairy Tales | Story Time for Kids by The Learning Station","channel":"TheLearningStation - Kids Songs and Nursery Rhymes","duration":"5:59","url":"https://www.youtube.com/watch?v=PGI-4MrC_b8"},
{"title":"More Real Life Funny Food Combinations, Do You Like Broccoli Ice Cream Song","channel":"Bella & Beans TV","duration":"1:55","url":"https://www.youtube.com/watch?v=lA7Cju_wQLc"},
{"title":"Chicka Chicka Boom Boom | Storytime Delight: Picture Book Read Aloud","channel":"WizmetMedia","duration":"2:25","url":"https://www.youtube.com/watch?v=XgcK8U3ua24"},
{"title":"Teacher Lupe reads book with animated video chicka chicka boom boom","channel":"Lupe koehler","duration":"4:55","url":"https://www.youtube.com/watch?v=DC2J_-vpju8"},
{"title":"How to make Chu Chu Tv Characters in Avatar World!!!","channel":"Angelic World AW","duration":"5:32","url":"https://www.youtube.com/watch?v=GONlNDUzINE"},
{"title":"3 Little Pigs | Bedtime Stories for Kids in English | Storytime","channel":"Fairy Tales and Stories for Kids","duration":"26:16","url":"https://www.youtube.com/watch?v=-9NXxlFnZcU"},
{"title":"Super Simple Songs Intro over One Million Times","channel":"The Testing Hut and Quality testing","duration":"2:02","url":"https://www.youtube.com/watch?v=nzA_QomycUk"},
{"title":"Super simple songs the ants go marching reversed","channel":"harry clarke","duration":"3:46","url":"https://www.youtube.com/watch?v=gR2y2L0sXqo"},
{"title":"CoComelon JJ's Animal Time Outro, Bluka Bluka Blah and ABC KIDS TV Logo Intro Over 1 Million Times","channel":"Sorry Ear","duration":"3:23","url":"https://www.youtube.com/watch?v=Dz_sxbUFUt0"},
{"title":"Peppa Pig and ABC KIDS TV Logo Intro Over 1 Million Times","channel":"Sorry Ear","duration":"2:39","url":"https://www.youtube.com/watch?v=dK9797O1arE"},
{"title":"Splash Song Intro Logo Sponsored By Klasky Csupo 2001 Effects","channel":"GIGIEffects","duration":"4:06","url":"https://www.youtube.com/watch?v=HOjwBOuS11k"},
{"title":"Super Simple Songs Let's Count Down! Intro Logo Sponsored By: Preview 2 Frank V2 Effects","channel":"IApple1234","duration":"4:07","url":"https://www.youtube.com/watch?v=oP0HhAt3mKo"},
{"title":"New Cocomelon Outro 2025, Dave and Ava Intro and Too too boy Logo Intro Over 1 Million Times","channel":"Sorry Ear","duration":"3:19","url":"https://www.youtube.com/watch?v=cwdmZIde9TQ"},
{"title":"Super Simple Songs Let's Count Down! Intro Logo Sponsored By Preview 2 Frank V2 Effects","channel":"GIGIEffects","duration":"4:07","url":"https://www.youtube.com/watch?v=xSWM1FyLGWU"},
{"title":"Super Simple Songs Let's Wash Our Face! Intro Logo Sponsored By: Gamavision Csupo Effects","channel":"IApple1234","duration":"3:38","url":"https://www.youtube.com/watch?v=3lnyvq8e1nU"},
{"title":"Peppa Pig Plays Minecraft in Real Life. All parts. (Complete)","channel":"Mushroom Rain","duration":"8:27","url":"https://www.youtube.com/watch?v=--k9QH82pH8"},
{"title":"PEPPA PIG IN Avatar World / Game World / Toca Boca / The Noisy Night","channel":"Kostya World","duration":"4:56","url":"https://www.youtube.com/watch?v=C-KVnTiuMU8"},
{"title":"Getting the mega bundle in Toca boca","channel":"EIKO TV","duration":"4:17","url":"https://www.youtube.com/watch?v=OrPYdKSpPQk"},
{"title":"Cocomelon intro effect with real instruments!","channel":"Emstepko","duration":"1:29","url":"https://www.youtube.com/watch?v=FpYUobcdQdg"},
{"title":"Merry Christmas","channel":"Bella!!","duration":"14:49","url":"https://www.youtube.com/watch?v=Nq2x87JqIvs"},
{"title":"PBS KIDS STATION ID COMPILATION 2013 2015 IN REVERSED","channel":"Rickety Roc 3","duration":"7:06","url":"https://www.youtube.com/watch?v=M1LAnDoURuM"},
{"title":"PBS KIDS Station ID Compilation (2013-2015) In G Major Effects (1-100)","channel":"linda m","duration":"7:06","url":"https://www.youtube.com/watch?v=MyEWIupnRtg"},
{"title":"PBS Kids ID / System Cue Compilation (1999-2022)","channel":"Peeebs","duration":"5:37","url":"https://www.youtube.com/watch?v=2sQ1JQKrOe4"},
{"title":"PBS Kids ID (I Voice Del, Dee & Dot)","channel":"Tye The Cool Guy","duration":"7:06","url":"https://www.youtube.com/watch?v=l3H5Jqcp-1Q"},
{"title":"Super Simple Songs Let's Count Down! Intro Logo Sponsored By: Preview 2 Effects","channel":"IApple1234","duration":"3:58","url":"https://www.youtube.com/watch?v=KDAKOSAivLU"},
{"title":"ABC Kid TV FAST CHASE in Liminal Hotel | Gmod Nextbots","channel":"OreoOne","duration":"4:07","url":"https://www.youtube.com/watch?v=-wc0LiVzj2M"},
{"title":"Super Simple Songs Playing With My Car Destroyed Intro Logo | Sponsored By: Preview 2 Effects","channel":"Custom Effects","duration":"2:59","url":"https://www.youtube.com/watch?v=EJNsQTFuuhU"},
{"title":"Super Simple Songs Driving Very Slow Crash! Intro Logo Sponsored By: Preview 2 Effects","channel":"IApple1234","duration":"3:13","url":"https://www.youtube.com/watch?v=wogGPIO5COw"},
{"title":"Netflix, Miniyo and CoComelon Playdates Logo Intro Over 1 Million Times","channel":"Sorry Ear","duration":"3:44","url":"https://www.youtube.com/watch?v=wS-g-9WYY-I"},
{"title":"Guess the logo Sound - MacDonald's, Tiktok, Netflix, Pepsi / logoQuiz 2025","channel":"Empire of Quiz","duration":"8:52","url":"https://www.youtube.com/watch?v=RjZmP_ROmJI"},
{"title":"Meekah Logo Intro Super Effects (Sponsored By Preview 2 Effects)","channel":"MSC PRO EDIT","duration":"3:11","url":"https://www.youtube.com/watch?v=ODhvakzX9Nc"},
{"title":"Peppa Pigs Play Along Podcast Intro Trailer","channel":"Great Pods","duration":"0:50","url":"https://www.youtube.com/watch?v=13r_pM1CDQg"},
{"title":"Gasp! | A Mickey Mouse Cartoon | Disney Shows | @disneykids","channel":"Disney Kids","duration":"3:51","url":"https://www.youtube.com/watch?v=8k1axb8PPqQ"}
]

def duration_to_seconds(d):
    if not d or d in ('LIVE', '', 'unknown'):
        return 0
    parts = d.strip().split(':')
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        return 0
    return 0

def categorize(title, channel):
    title_lower = title.lower()
    channel_lower = channel.lower()

    if any(k in title_lower for k in ['abc', 'alphabet', 'phonics', 'learn', 'read', 'word family', 'educational', 'colors', 'colour', 'numbers', 'seasons', 'feelings', 'animals', 'toddler language', 'speech', 'ms. rachel', 'yakka dee']):
        return 'Educational / Learning'
    if any(k in title_lower for k in ['nursery rhyme', 'kids song', 'children song', 'toddler song', 'baby song', 'preschool music', 'lullaby']):
        return 'Nursery Rhymes / Songs'
    if any(k in title_lower for k in ['peppa', 'mickey mouse', 'minnie', 'disney', 'bluey', 'paw patrol', 'cocomelon', 'chuchu', 'noodle']):
        return 'Kids Cartoons'
    if any(k in channel_lower for k in ['noodle', 'super simple', 'yakka dee', 'rhymington', 'chuchu', 'blippi', 'mother goose', 'sesame street', 'have fun teaching']):
        return 'Educational / Learning'
    if any(k in title_lower for k in ['toca boca', 'toca world', 'toca life', 'roleplay', 'roblox']):
        return 'Gaming / Roleplay'
    if any(k in title_lower for k in ['logo effect', 'logo intro', 'logo super', 'sponsored by preview', 'sponsored by klasky', 'over 1 million times', 'csupo effects', 'g major', 'reversed', 'pbs kids station id']):
        return 'Logo Effects / Fan Content'
    if any(k in title_lower for k in ['stinky farts', 'power slap', 'fat belly', 'gone wrong', 'mega grounded', 'skip school', 'bad girl', 'absolute cinema']):
        return 'Questionable Content'
    if any(k in title_lower for k in ['sing', 'song', 'music', 'instrument']):
        return 'Nursery Rhymes / Songs'
    if any(k in title_lower for k in ['story', 'read aloud', 'storytime', 'storybook', 'book']):
        return 'Storytime / Read Aloud'
    return 'Kids Entertainment'

def safety_score(title, channel, category):
    title_lower = title.lower()
    flags = []
    positive_signals = []
    score = 5

    # Positive signals
    if any(k in title_lower for k in ['abc', 'alphabet', 'phonics', 'learn to read', 'educational', 'toddler language', 'ms. rachel', 'yakka dee']):
        positive_signals.append('educational_content')
        score += 2
    if any(k in title_lower for k in ['nursery', 'toddler', 'preschool', 'kids song']):
        positive_signals.append('age_appropriate')
        score += 1
    if any(k in title_lower for k in ['good habits', 'sharing', 'safety rules', 'wash hands', 'brush teeth', 'manners', 'bedtime', 'story', 'read aloud']):
        positive_signals.append('positive_values')
        score += 2

    # Negative / concerning signals
    if any(k in title_lower for k in ['stinky farts', 'power slap', 'fat belly', 'mega grounded', 'bad girl', 'single mom']):
        flags.append('inappropriate_content')
        score -= 4
    if any(k in title_lower for k in ['gone wrong', '*gone wrong*']):
        flags.append('drama_content')
        score -= 2
    if any(k in title_lower for k in ['skip school', 'skips school']):
        flags.append('negative_behavior_modeling')
        score -= 3
    if any(k in title_lower for k in ['absolute cinema', 'caillou dancing', 'tdgwvsc']):
        flags.append('unclear_content')
        score -= 1
    if 'gorge esta solo' in title_lower or 'svinka peppa v robloks' in title_lower:
        flags.append('foreign_unflagged')
        score -= 1
    if any(k in title_lower for k in ['logo effect', 'sponsored by preview', 'sponsored by klasky', 'csupo effects', 'over 1 million times', 'g major', 'reversed']):
        flags.append('logo_effect_spam')
        score -= 2
    if any(k in title_lower for k in ['aesthetic', 'morning routine', 'night routine']) and any(k in title_lower for k in ['mom', 'twin', 'toca boca', 'with voice']):
        flags.append('adult_lifestyle_content')
        score -= 2
    if 'roblox' in title_lower or 'minecraft' in title_lower:
        flags.append('gaming_content')
        score -= 1

    score = max(1, min(10, score))

    if score >= 7:
        rating = 'good'
        badge = '✅'
    elif score >= 4:
        rating = 'review'
        badge = '⬜'
    else:
        rating = 'flag'
        badge = '🚩'

    return score, rating, badge, flags, positive_signals

now = datetime.now(timezone.utc)
processed = []
total_seconds = 0

for v in SCRAPED_VIDEOS:
    dur_secs = duration_to_seconds(v['duration'])
    total_seconds += dur_secs
    category = categorize(v['title'], v['channel'])
    score, rating, badge, flags, positives = safety_score(v['title'], v['channel'], category)
    is_live = v['duration'] in ('LIVE', '')
    is_short = '/shorts/' in v['url']

    processed.append({
        'title': v['title'],
        'channel': v['channel'],
        'url': v['url'],
        'duration': v['duration'] if v['duration'] else 'unknown',
        'duration_seconds': dur_secs,
        'timestamp': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'category': category,
        'is_short': is_short,
        'is_live': is_live,
        'safety_score': score,
        'safety_rating': rating,
        'safety_badge': badge,
        'flags': flags,
        'positive_signals': positives
    })

channel_counter = Counter(v['channel'] for v in processed)
top_channels = [{'channel': ch, 'count': cnt} for ch, cnt in channel_counter.most_common(10)]

cat_counter = Counter(v['category'] for v in processed)
top_categories = [{'category': cat, 'count': cnt} for cat, cnt in cat_counter.most_common()]

good = sum(1 for v in processed if v['safety_rating'] == 'good')
review = sum(1 for v in processed if v['safety_rating'] == 'review')
flag = sum(1 for v in processed if v['safety_rating'] == 'flag')

output = {
    'generated': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
    'account': 'jigar.us.af@gmail.com',
    'period_days': 7,
    'note': 'Daily update',
    'total_videos': len(processed),
    'total_watch_minutes': round(total_seconds / 60, 1),
    'videos': processed,
    'top_channels': top_channels,
    'top_categories': top_categories,
    'hourly_counts': {str(h): 0 for h in range(24)},
    'daily_counts': {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0},
    'safety': {
        'good': good,
        'review': review,
        'flag': flag,
        'flagged_channels': list(set(v['channel'] for v in processed if v['safety_rating'] == 'flag'))
    }
}

output_path = '/Users/sgtclaw/.openclaw/workspace/KidWatch/data/history.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Saved {len(processed)} videos to {output_path}")
print(f"Total watch time: {round(total_seconds/60, 1)} minutes")
print(f"Good: {good} | Review: {review} | Flag: {flag}")
flagged = [v for v in processed if v['safety_rating'] == 'flag']
if flagged:
    print(f"Flagged videos ({len(flagged)}):")
    for v in flagged:
        print(f"  - {v['title'][:60]} [{v['channel']}] flags={v['flags']}")
flagged_channels = list(set(v['channel'] for v in processed if v['safety_rating'] == 'flag'))
print(f"Flagged channels: {flagged_channels}")
