"""Helpful guide articles (answer-first, for SEO / AEO / GEO).

Each guide: slug, title, description, answer (the direct 1–3 sentence answer
shown first and used in schema), sections [(heading, [paragraphs or ("ul", [items])])],
faqs [(q, a)], related service slugs.
"""

GUIDES = [
    {
        "slug": "how-often-to-change-watch-battery",
        "title": "How Often Should You Change a Watch Battery?",
        "description": "How long a quartz watch battery lasts, the signs it's running out, and why you shouldn't leave a dead cell inside your watch.",
        "answer": "Most quartz watch batteries last about 1.5 to 3 years. Watches with lights, alarms, chronographs or digital displays usually need a new battery sooner. Replace a dead battery quickly, because an old cell can leak and damage the movement.",
        "sections": [
            ("Signs your watch battery is running low", [
                ("ul", [
                    "The seconds hand jumps 2–5 seconds at a time instead of every second (many quartz watches do this as a low-battery warning).",
                    "The watch starts losing time.",
                    "A digital display looks faded or the backlight is weak.",
                    "The watch stops completely.",
                ]),
            ]),
            ("What affects battery life?", [
                "Battery life depends on the movement, the battery size and the features. A simple three-hand analog watch can run for years on one cell. A watch that uses an alarm, a light or a stopwatch every day uses more power.",
                "Storing a watch in a very hot place, such as a car dashboard in an Ahmedabad summer, can also shorten battery life.",
            ]),
            ("Why you shouldn't leave a dead battery inside", [
                "An old battery can leak. The leak is corrosive and can damage the circuit and movement, which turns a cheap battery change into an expensive repair. If your watch has stopped and you're not going to use it soon, have the battery replaced or removed.",
            ]),
            ("Battery replacement in Chandkheda", [
                "At Jay Santoshi Watch, battery replacement is usually done in a few minutes while you wait. We use the correct cell for your watch, check the gasket and close the back properly.",
            ]),
        ],
        "faqs": [
            ("Can I change a watch battery myself?",
             "You can, but it's easy to scratch the case, damage the gasket or fit the wrong cell. A watch shop has the right tools and batteries and usually does it in minutes."),
            ("Does a new battery affect water resistance?",
             "Opening the back can affect water resistance if the gasket isn't checked and refitted properly. Ask the shop to check the gasket, and avoid swimming with older watches."),
        ],
        "related": ["watch-battery-replacement", "watch-repair"],
    },
    {
        "slug": "watch-stopped-working-what-to-do",
        "title": "Watch Stopped Working? 7 Common Causes and What to Do",
        "description": "Why a watch stops, from a dead battery to moisture and a pulled-out crown, and which problems need a repair shop.",
        "answer": "The most common reason a quartz watch stops is a dead battery. Other causes are a crown left pulled out, moisture inside, a damaged movement, or loose hands catching each other. Check the crown first. If the watch still doesn't run, get the battery and movement checked at a watch repair shop.",
        "sections": [
            ("7 common causes", [
                ("ul", [
                    "Dead battery: the number one cause for quartz watches.",
                    "Crown pulled out: in the time-setting position the watch stops. Push it fully in.",
                    "Moisture or water inside: you may see fog under the glass. Get it checked quickly.",
                    "Loose or bent hands catching each other.",
                    "Magnetism: phones, speakers and magnetic clasps can affect some watches.",
                    "A knock or fall that damaged the movement.",
                    "Automatic watch not worn enough: it may simply need winding or wearing.",
                ]),
            ]),
            ("What you can check at home", [
                "Push the crown fully in. For an automatic watch, wind it gently or wear it for a day. Look for fog or water drops under the glass. If you see moisture, don't wait. Bring the watch to a repair shop as soon as possible.",
            ]),
            ("When to visit a watch repair shop", [
                "If the watch still doesn't run after these checks, it needs a professional look. At Jay Santoshi Watch in Chandkheda we check it in front of you and tell you whether it needs a battery, a repair or a new movement, and what it costs, before doing any work.",
            ]),
        ],
        "faqs": [
            ("My watch stopped even after a new battery. What now?",
             "The movement may be dirty, damaged or worn out, or there may be moisture inside. A repair shop can clean it, repair it or replace the movement."),
            ("Is it worth repairing an old watch?",
             "Often, yes, especially if it has sentimental value. A movement replacement or cleaning can bring many old watches back to life."),
        ],
        "related": ["watch-repair", "watch-battery-replacement", "watch-servicing"],
    },
    {
        "slug": "watch-strap-size-guide",
        "title": "Watch Strap Size Guide: How to Find the Right Width and Fit",
        "description": "How to measure a watch strap's lug width, choose between leather, silicone and metal, and get a metal chain resized correctly.",
        "answer": "Strap width is the distance between the watch's lugs, in millimetres. Common sizes are 16, 18, 20 and 22 mm. Pick a strap that matches the lug width exactly. For metal chains, a shop can remove or add links so the watch sits comfortably, with about one finger's space under it.",
        "sections": [
            ("How to measure lug width", [
                "Measure the inside gap between the two lugs (the horns that hold the strap) with a ruler. Many straps also have the width printed on the inside. Most men's watches use 18–22 mm and most women's watches use 12–18 mm.",
            ]),
            ("Leather vs silicone vs metal", [
                ("ul", [
                    "Leather: classic and comfortable for office wear. Keep it away from water and heavy sweat.",
                    "Silicone / rubber: good for sports, gym and Ahmedabad's hot, humid months. Easy to wash.",
                    "Stainless steel: long-lasting and smart. Needs correct link sizing for comfort.",
                ]),
            ]),
            ("Getting a metal chain resized", [
                "A chain that's too loose slides and scratches. One that's too tight is uncomfortable. A watch shop removes links evenly from both sides so the clasp stays centred. Keep the spare links in case your wrist size changes.",
            ]),
        ],
        "faqs": [
            ("Can I put a 20 mm strap on an 18 mm watch?",
             "No. The strap must match the lug width, or it won't fit or will look loose. Get the exact size."),
            ("How tight should a watch be?",
             "Snug but comfortable. You should be able to slide one finger between the strap and your wrist."),
        ],
        "related": ["watch-strap-replacement", "watch-accessories"],
    },
    {
        "slug": "watch-water-resistance-explained",
        "title": "Watch Water Resistance Explained: 30m, 50m, 100m and What They Really Mean",
        "description": "What 3 ATM / 30m, 5 ATM / 50m and 10 ATM / 100m mean in real life, and how to keep your watch safe from water and monsoon humidity.",
        "answer": "Water-resistance ratings are lab test pressures, not safe diving depths. 30m (3 ATM) means splash-resistant only. 50m (5 ATM) is fine for hand-washing and light rain. 100m (10 ATM) is suitable for swimming. Water resistance weakens with age and after the back is opened, so have the gaskets checked.",
        "sections": [
            ("What each rating means", [
                ("ul", [
                    "Water Resistant / 30m / 3 ATM: splashes and rain only. Don't swim or shower with it.",
                    "50m / 5 ATM: hand-washing, rain and light water contact. Not ideal for swimming.",
                    "100m / 10 ATM: swimming and surface water sports.",
                    "200m / 20 ATM and above: snorkelling and serious water sports.",
                ]),
            ]),
            ("Tips for monsoon and humid weather", [
                "Keep the crown pushed in, avoid hot showers with your watch (heat and steam affect the seals), and wipe the watch dry after rain. If you see fog under the glass, get the watch checked straight away.",
            ]),
        ],
        "faqs": [
            ("Is my watch still water-resistant after a battery change?",
             "Only if the gasket is in good condition and the back is closed properly. Ask the shop to check it. Old gaskets should be replaced."),
            ("There's fog inside my watch. What should I do?",
             "Remove the watch from water and heat and bring it to a repair shop soon. Moisture inside can rust the movement and damage the dial."),
        ],
        "related": ["watch-repair", "watch-servicing", "watch-battery-replacement"],
    },
    {
        "slug": "quartz-vs-automatic-watches",
        "title": "Quartz vs Automatic Watches: Which Should You Buy?",
        "description": "A simple comparison of quartz and automatic (mechanical) watches: accuracy, maintenance, cost and which suits you.",
        "answer": "Quartz watches run on a battery, are very accurate, low-maintenance and usually more affordable. Automatic watches are mechanical, wind themselves as you wear them, need no battery, but are less accurate and need periodic servicing. For daily, worry-free use choose quartz. For craftsmanship and character choose automatic.",
        "sections": [
            ("Quick comparison", [
                ("ul", [
                    "Power: quartz uses a battery. Automatic winds from your wrist movement.",
                    "Accuracy: quartz is typically within seconds per month. Automatic is typically within seconds per day.",
                    "Maintenance: quartz needs a battery change every few years. Automatic needs a service every few years.",
                    "Price: quartz is generally more affordable.",
                ]),
            ]),
            ("Which is right for you?", [
                "If you want a reliable watch for office, college or daily use, a quartz watch is usually the best choice. If you love the feel of a mechanical movement and don't mind adjusting the time now and then, an automatic watch is a great choice.",
                "Visit Jay Santoshi Watch in Chandkheda to see and try different styles before you decide.",
            ]),
        ],
        "faqs": [
            ("Does an automatic watch need a battery?",
             "No. An automatic watch is powered by a spring that winds as you move your wrist. If you don't wear it for a day or two, it stops and needs winding."),
        ],
        "related": ["wrist-watches", "watch-servicing"],
    },
    {
        "slug": "wall-clock-buying-guide",
        "title": "Wall Clock Buying Guide: Size, Style and Silent Clocks",
        "description": "How to choose a wall clock for your living room, bedroom, kitchen or office, and why silent (sweep) movements are popular.",
        "answer": "Choose a wall clock by room size and use. Large, bold clocks suit living rooms. Simple, easy-to-read clocks suit kitchens and offices. Silent sweep-movement clocks suit bedrooms and study rooms. Check that the numbers are readable from across the room and that the style matches your decor.",
        "sections": [
            ("Choosing the right size", [
                "For a large living-room wall, a bigger clock or a decorative design makes a statement. For kitchens, offices and shops, pick a clear dial that's easy to read from a distance.",
            ]),
            ("Silent vs ticking clocks", [
                "Standard quartz clocks tick every second. Sweep-movement clocks move smoothly and silently, which is why people like them for bedrooms, study rooms and meditation spaces.",
            ]),
            ("Clocks as gifts", [
                "Wall clocks are a popular housewarming and office-opening gift in Gujarat. Pick a neutral, elegant design that will suit most homes.",
            ]),
            ("Old clock stopped working?", [
                "A stopped quartz wall clock can often be fixed by replacing its movement (machine), keeping the original dial and frame. Jay Santoshi Watch in Chandkheda does this regularly.",
            ]),
        ],
        "faqs": [
            ("Why does my wall clock stop even with a new battery?",
             "The quartz movement may be worn out, or the hands may be touching each other or the glass. A clock repair shop can replace the movement or adjust the hands."),
        ],
        "related": ["wall-clocks", "wall-clock-repair", "gift-watches"],
    },
    {
        "slug": "watch-care-tips",
        "title": "Watch Care Tips: 10 Simple Ways to Make Your Watch Last Longer",
        "description": "Practical tips to protect your watch from heat, sweat, water, magnets and knocks, written for Ahmedabad's climate.",
        "answer": "Keep your watch away from heat, water it isn't rated for, magnets and hard knocks. Wipe off sweat after use, keep the crown pushed in, replace dead batteries quickly, and have the watch checked whenever the battery is changed. These simple habits can add years to a watch's life.",
        "sections": [
            ("10 simple tips", [
                ("ul", [
                    "Wipe the watch and strap after sweating, especially in summer.",
                    "Don't leave it in a hot car or in direct sunlight.",
                    "Keep the crown fully pushed in.",
                    "Don't press chronograph buttons under water.",
                    "Keep it away from strong magnets such as speakers and magnetic phone cases.",
                    "Take it off for heavy work, gym lifting and sports where it can be knocked.",
                    "Replace a dead battery quickly to avoid leakage.",
                    "Let leather straps dry naturally, away from heat.",
                    "Store it in a box or soft pouch, not loose in a drawer.",
                    "Have it checked or serviced every time the battery is changed.",
                ]),
            ]),
        ],
        "faqs": [
            ("How do I clean my watch at home?",
             "Wipe the case and metal chain with a soft, slightly damp cloth and dry it immediately. Don't soak non-water-resistant watches or leather straps."),
        ],
        "related": ["watch-servicing", "watch-strap-replacement", "watch-battery-replacement"],
    },
    {
        "slug": "watch-gift-ideas",
        "title": "Watch Gift Ideas for Birthdays, Weddings, Raksha Bandhan and Diwali",
        "description": "How to choose the right watch or clock as a gift for him, her, kids, couples and corporate gifting.",
        "answer": "For a watch gift, match the style to the person: classic analog for office wear, sporty digital for students and active people, slim bracelet watches for women, couple watches for weddings and anniversaries, and wall clocks for housewarmings. Set a budget, know their wrist size if possible, and buy from a shop that offers after-sales help.",
        "sections": [
            ("Gift ideas by occasion", [
                ("ul", [
                    "Birthday: a stylish analog or digital watch in their favourite colour.",
                    "Wedding or anniversary: a matching couple watch set.",
                    "Raksha Bandhan: smart analog watches for brothers, elegant watches for sisters.",
                    "Diwali and corporate gifts: watches or desk/wall clocks in bulk.",
                    "Housewarming: a decorative wall clock.",
                    "Kids: colourful, easy-to-read digital or analog watches.",
                ]),
            ]),
            ("Tips before you buy", [
                "Know your budget, think about where they'll wear it (office, college, sports), and if possible find out their wrist size so the strap can be adjusted before you gift it.",
            ]),
        ],
        "faqs": [
            ("Can I exchange a watch gift if the size doesn't fit?",
             "Metal chains can usually be resized at the shop. For exchange policies, ask at the time of purchase."),
        ],
        "related": ["gift-watches", "wrist-watches", "wall-clocks"],
    },
]
