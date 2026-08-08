"""
Harry Potter Character & Sorting Hub
A Streamlit app with:
  1. Character Search & Information Hub (local DB + fallback)
  2. Hogwarts House & Patronus Quiz
  3. Custom wizarding-themed CSS
"""

import random
import streamlit as st

# --------------------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Harry Potter Character & Sorting Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------------------
# CUSTOM CSS — dark parchment / starry night, gold headings, house badges, cards
# --------------------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@400;600&family=EB+Garamond:wght@400;500;600&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(255,255,255,0.06) 0%, transparent 3%),
        radial-gradient(circle at 80% 10%, rgba(255,255,255,0.05) 0%, transparent 2%),
        radial-gradient(circle at 60% 70%, rgba(255,255,255,0.05) 0%, transparent 2%),
        radial-gradient(circle at 30% 85%, rgba(255,255,255,0.04) 0%, transparent 2%),
        radial-gradient(circle at 90% 60%, rgba(255,255,255,0.05) 0%, transparent 2%),
        linear-gradient(180deg, #0b0c1a 0%, #14152b 40%, #1c1a2e 70%, #241f2e 100%);
    color: #e9dfc8;
    font-family: 'EB Garamond', serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1425 0%, #241a1f 100%);
    border-right: 2px solid #c9a24b;
}
section[data-testid="stSidebar"] * { color: #e9dfc8 !important; }

h1, h2, h3 {
    font-family: 'Cinzel Decorative', 'Cinzel', serif !important;
    color: #d4af37 !important;
    text-shadow: 0 0 12px rgba(212,175,55,0.35);
    letter-spacing: 1px;
}
h4, h5, h6 { font-family: 'Cinzel', serif !important; color: #e6c66b !important; }

p, li, span, label, div { font-family: 'EB Garamond', serif; }

.hp-card {
    background: linear-gradient(160deg, rgba(40,32,24,0.85) 0%, rgba(25,20,30,0.9) 100%);
    border: 1px solid #c9a24b;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.45), inset 0 0 40px rgba(201,162,75,0.05);
}

.hp-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a24b, transparent);
    margin: 14px 0;
}

.house-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 1px;
    border: 1px solid rgba(255,255,255,0.25);
    margin-right: 8px;
}
.badge-gryffindor { background: linear-gradient(135deg,#740001,#ae0001); color:#eeba30; }
.badge-slytherin  { background: linear-gradient(135deg,#1a472a,#2a623d); color:#aaaaaa; }
.badge-ravenclaw  { background: linear-gradient(135deg,#0e1a40,#222f5b); color:#946b2d; }
.badge-hufflepuff { background: linear-gradient(135deg,#ecb939,#f0c75e); color:#372e29; }
.badge-unknown    { background: linear-gradient(135deg,#3a3a3a,#555555); color:#eee; }

.stButton>button {
    background: linear-gradient(135deg, #2a223a, #14101e);
    color: #d4af37;
    border: 1px solid #c9a24b;
    border-radius: 10px;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.5px;
    padding: 8px 20px;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #3a2f52, #201a30);
    color: #f0d878;
    border-color: #f0d878;
    box-shadow: 0 0 12px rgba(212,175,55,0.5);
}

.stTextInput>div>div>input, .stSelectbox>div>div {
    background-color: rgba(20,16,26,0.85) !important;
    color: #e9dfc8 !important;
    border: 1px solid #c9a24b !important;
    border-radius: 8px !important;
}

.stRadio > label { font-family: 'Cinzel', serif; color: #d4af37 !important; }

hr { border-color: #c9a24b33; }

.quiz-question {
    font-family: 'Cinzel', serif;
    color: #f0d878;
    font-size: 1.15rem;
    margin-top: 10px;
}

.result-hero {
    text-align: center;
    padding: 30px;
    border-radius: 16px;
    border: 2px solid #d4af37;
    margin-top: 10px;
}

::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #14101e; }
::-webkit-scrollbar-thumb { background: #6b5a2e; border-radius: 10px; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# HOUSE METADATA
# --------------------------------------------------------------------------------------
HOUSES = {
    "Gryffindor": {
        "colors": "Scarlet & Gold",
        "badge_class": "badge-gryffindor",
        "traits": "courage, daring, nerve, and chivalry",
        "animal": "Lion",
        "patronus_pool": ["Stag", "Lion", "Phoenix", "Jack Russell Terrier"],
        "founder": "Godric Gryffindor",
        "element_desc": "Gryffindors walk toward danger rather than away from it, guided by "
                         "a burning sense of what is right.",
    },
    "Slytherin": {
        "colors": "Emerald & Silver",
        "badge_class": "badge-slytherin",
        "traits": "ambition, cunning, leadership, and resourcefulness",
        "animal": "Serpent",
        "patronus_pool": ["Silver Serpent", "Fox", "Eagle", "Doe"],
        "founder": "Salazar Slytherin",
        "element_desc": "Slytherins are strategists who value resourcefulness and are "
                         "unafraid to do what it takes to achieve their goals.",
    },
    "Ravenclaw": {
        "colors": "Blue & Bronze",
        "badge_class": "badge-ravenclaw",
        "traits": "intelligence, wit, wisdom, and creativity",
        "animal": "Eagle",
        "patronus_pool": ["Eagle", "Swan", "Cat", "Otter"],
        "founder": "Rowena Ravenclaw",
        "element_desc": "Ravenclaws prize learning and originality above almost anything else, "
                         "forever chasing the next great idea.",
    },
    "Hufflepuff": {
        "colors": "Yellow & Black",
        "badge_class": "badge-hufflepuff",
        "traits": "loyalty, patience, fairness, and hard work",
        "animal": "Badger",
        "patronus_pool": ["Badger", "Otter", "Dog", "Rabbit"],
        "founder": "Helga Hufflepuff",
        "element_desc": "Hufflepuffs are steady, loyal, and endlessly hardworking — the "
                         "friends who never abandon you.",
    },
}

# --------------------------------------------------------------------------------------
# CHARACTER DATABASE
# --------------------------------------------------------------------------------------
CHARACTERS = {
    "harry potter": {
        "full_name": "Harry James Potter",
        "overview": "The Boy Who Lived. Orphaned as an infant after Lord Voldemort murdered "
                    "his parents, Harry was raised by his unpleasant Muggle relatives, the "
                    "Dursleys, until he learned on his eleventh birthday that he was a wizard. "
                    "He attended Hogwarts School of Witchcraft and Wizardry, where he became "
                    "famous for surviving the Killing Curse and eventually for defeating "
                    "Voldemort once and for all during the Battle of Hogwarts.",
        "wand": {"wood": "Holly", "core": "Phoenix feather (Fawkes)", "length": "11 inches",
                  "rigidity": "Reasonably supple"},
        "house": "Gryffindor",
        "patronus": "Stag",
        "allies": ["Ron Weasley", "Hermione Granger", "Albus Dumbledore", "Sirius Black",
                    "Remus Lupin", "Order of the Phoenix", "Dumbledore's Army"],
        "relatives": ["James Potter (father)", "Lily Potter (mother)", "Petunia Dursley (aunt)",
                       "Vernon Dursley (uncle)", "Ginny Weasley (wife)", "James Sirius, Albus "
                       "Severus & Lily Luna Potter (children)"],
        "achievements": [
            "Survived the Killing Curse as an infant, becoming 'The Boy Who Lived'",
            "Founded and led Dumbledore's Army",
            "Destroyed multiple Horcruxes",
            "Defeated Lord Voldemort in the Battle of Hogwarts (1998)",
            "Became Head of the Auror Office in later life",
        ],
    },
    "hermione granger": {
        "full_name": "Hermione Jean Granger",
        "overview": "Widely regarded as the brightest witch of her age, Hermione was born to "
                    "Muggle parents and discovered her magical ability before receiving her "
                    "Hogwarts letter. Fiercely intelligent, principled, and loyal, she became "
                    "one third of the 'Golden Trio' alongside Harry Potter and Ron Weasley, "
                    "and was instrumental in nearly every major victory against Voldemort.",
        "wand": {"wood": "Vine", "core": "Dragon heartstring", "length": "10¾ inches",
                  "rigidity": "Reasonably supple"},
        "house": "Gryffindor",
        "patronus": "Otter",
        "allies": ["Harry Potter", "Ron Weasley", "Ginny Weasley", "Order of the Phoenix",
                    "Dumbledore's Army"],
        "relatives": ["Mr. Granger (father)", "Mrs. Granger (mother)", "Ron Weasley (husband)",
                       "Rose and Hugo Granger-Weasley (children)"],
        "achievements": [
            "Founded S.P.E.W. (Society for the Promotion of Elfish Welfare)",
            "Used a Time-Turner in her third year to attend extra classes",
            "Devised the plan to destroy Horcruxes with Basilisk fangs",
            "Became a key figure in post-war magical law reform",
            "Later served as Minister for Magic",
        ],
    },
    "ron weasley": {
        "full_name": "Ronald Bilius Weasley",
        "overview": "The youngest Weasley son, Ron grew up in a loving but financially modest "
                    "wizarding family. Loyal and brave despite frequent bouts of insecurity "
                    "living in the shadow of his accomplished siblings, Ron became Harry "
                    "Potter's best friend and an essential member of the trio that defeated "
                    "Voldemort.",
        "wand": {"wood": "Willow (originally), later Ash", "core": "Unicorn hair",
                  "length": "14 inches", "rigidity": "Unyielding"},
        "house": "Gryffindor",
        "patronus": "Jack Russell Terrier",
        "allies": ["Harry Potter", "Hermione Granger", "Ginny Weasley", "Order of the Phoenix",
                    "Dumbledore's Army"],
        "relatives": ["Arthur Weasley (father)", "Molly Weasley (mother)", "Bill, Charlie, "
                      "Percy, Fred, George & Ginny Weasley (siblings)", "Hermione Granger "
                      "(wife)", "Rose and Hugo Granger-Weasley (children)"],
        "achievements": [
            "Sacrificed himself as a chess piece in first-year Wizard's Chess",
            "Became a Prefect and Gryffindor Quidditch Keeper",
            "Destroyed the locket Horcrux with the Sword of Gryffindor",
            "Fought in the Battle of Hogwarts",
            "Became a senior Auror alongside Harry",
        ],
    },
    "albus dumbledore": {
        "full_name": "Albus Percival Wulfric Brian Dumbledore",
        "overview": "Widely considered the greatest wizard of his generation, Dumbledore "
                    "served as Headmaster of Hogwarts, Supreme Mugwump of the International "
                    "Confederation of Wizards, and Chief Warlock of the Wizengamot. A brilliant "
                    "and enigmatic mentor to Harry Potter, his past was shadowed by his "
                    "complicated relationship with Gellert Grindelwald and his sister Ariana's "
                    "death.",
        "wand": {"wood": "Elder", "core": "Thestral tail hair", "length": "15 inches",
                  "rigidity": "Unyielding (the Elder Wand)"},
        "house": "Gryffindor",
        "patronus": "Phoenix",
        "allies": ["Minerva McGonagall", "Order of the Phoenix", "Harry Potter",
                    "Fawkes (his phoenix)"],
        "relatives": ["Percival Dumbledore (father)", "Kendra Dumbledore (mother)",
                       "Aberforth Dumbledore (brother)", "Ariana Dumbledore (sister)"],
        "achievements": [
            "Defeated the dark wizard Gellert Grindelwald in 1945",
            "Founded the Order of the Phoenix",
            "Discovered the twelve uses of dragon's blood",
            "Served as Headmaster of Hogwarts for decades",
            "Mentored Harry Potter and orchestrated the downfall of Voldemort's Horcruxes",
        ],
    },
    "severus snape": {
        "full_name": "Severus Snape",
        "overview": "A brilliant but embittered Potions Master (and later Defence Against the "
                    "Dark Arts teacher and Headmaster), Snape spent nearly two decades as a "
                    "double agent for the Order of the Phoenix out of enduring love for Lily "
                    "Potter. Outwardly cold and cruel, especially toward Harry, his true "
                    "loyalties and sacrifices were only revealed after his death.",
        "wand": {"wood": "Ebony", "core": "Unknown", "length": "Approximately 13 inches",
                  "rigidity": "Unyielding"},
        "house": "Slytherin",
        "patronus": "Doe",
        "allies": ["Albus Dumbledore", "Order of the Phoenix (secretly)", "Lily Potter "
                    "(in his youth)"],
        "relatives": ["Tobias Snape (father)", "Eileen Prince (mother)"],
        "achievements": [
            "Invented multiple original spells, including Sectumsempra",
            "Served as a double agent against Voldemort for ~17 years",
            "Protected Harry Potter throughout his time at Hogwarts, often unseen",
            "Delivered crucial memories revealing Harry had to die and be resurrected",
            "Became Headmaster of Hogwarts under duress during the Second Wizarding War",
        ],
    },
    "draco malfoy": {
        "full_name": "Draco Lucius Malfoy",
        "overview": "Born into a wealthy pure-blood family steeped in Voldemort's ideology, "
                    "Draco was Harry Potter's chief rival throughout their years at Hogwarts. "
                    "Pressured into becoming a Death Eater as a teenager, he ultimately proved "
                    "unwilling to kill and, by the war's end, quietly turned away from his "
                    "family's dark allegiances.",
        "wand": {"wood": "Hawthorn", "core": "Unicorn hair", "length": "10 inches",
                  "rigidity": "Reasonably supple"},
        "house": "Slytherin",
        "patronus": "Unknown/Non-corporeal",
        "allies": ["Crabbe & Goyle", "Pansy Parkinson", "Blaise Zabini"],
        "relatives": ["Lucius Malfoy (father)", "Narcissa Malfoy (mother)", "Astoria Greengrass "
                      "(wife)", "Scorpius Malfoy (son)"],
        "achievements": [
            "Became a Death Eater at sixteen under Voldemort's command",
            "Tasked with assassinating Dumbledore, but ultimately could not go through with it",
            "Lowered his wand rather than identify Harry to Death Eaters at Malfoy Manor",
            "Distanced himself and his family from Voldemort's ideology after the war",
        ],
    },
    "luna lovegood": {
        "full_name": "Luna Lovegood",
        "overview": "The dreamy, unconventional daughter of Xenophilius Lovegood, editor of "
                    "The Quibbler, Luna became a devoted member of Dumbledore's Army and one "
                    "of Harry's most steadfast friends. Her eccentricity masked a rare wisdom "
                    "and unshakeable kindness that endeared her to those who looked past first "
                    "impressions.",
        "wand": {"wood": "Unknown", "core": "Unknown", "length": "Unknown", "rigidity": "Unknown"},
        "house": "Ravenclaw",
        "patronus": "Hare",
        "allies": ["Harry Potter", "Ginny Weasley", "Neville Longbottom", "Dumbledore's Army"],
        "relatives": ["Xenophilius Lovegood (father)", "Pandora Lovegood (mother, deceased)",
                       "Rolf Scamander (husband)"],
        "achievements": [
            "Could see Thestrals, having witnessed her mother's death",
            "Helped Harry find the lost Ravenclaw diadem Horcrux",
            "Fought in the Battle of the Department of Mysteries and Battle of Hogwarts",
            "Became a celebrated magizoologist",
        ],
    },
    "neville longbottom": {
        "full_name": "Neville Longbottom",
        "overview": "Initially timid and forgetful, Neville grew into one of the bravest "
                    "wizards of his generation. Raised by his grandmother after his parents "
                    "were tortured into insanity by Death Eaters, he became a stalwart member "
                    "of Dumbledore's Army and ultimately struck the killing blow against "
                    "Nagini, Voldemort's final Horcrux.",
        "wand": {"wood": "Cherry (originally his father's), later his own",
                  "core": "Unicorn hair", "length": "13 inches", "rigidity": "Unyielding"},
        "house": "Gryffindor",
        "patronus": "None known/non-corporeal in canon",
        "allies": ["Harry Potter", "Luna Lovegood", "Ginny Weasley", "Dumbledore's Army"],
        "relatives": ["Frank Longbottom (father)", "Alice Longbottom (mother)",
                       "Augusta Longbottom (grandmother)"],
        "achievements": [
            "Led Dumbledore's Army resistance at Hogwarts in Harry's absence",
            "Pulled the Sword of Gryffindor from the Sorting Hat",
            "Beheaded Nagini, destroying Voldemort's final Horcrux",
            "Later became Hogwarts' Herbology professor",
        ],
    },
    "ginny weasley": {
        "full_name": "Ginevra Molly Weasley",
        "overview": "The youngest of the Weasley children and the only Weasley daughter in "
                    "generations, Ginny grew from a shy admirer of Harry Potter into a fierce, "
                    "talented witch in her own right — a gifted Quidditch player and committed "
                    "member of Dumbledore's Army who later married Harry.",
        "wand": {"wood": "Yew", "core": "Unknown", "length": "Unknown", "rigidity": "Unknown"},
        "house": "Gryffindor",
        "patronus": "Horse",
        "allies": ["Harry Potter", "Hermione Granger", "Luna Lovegood", "Dumbledore's Army"],
        "relatives": ["Arthur Weasley (father)", "Molly Weasley (mother)", "Bill, Charlie, "
                      "Percy, Fred, George & Ron Weasley (brothers)", "Harry Potter (husband)",
                       "James Sirius, Albus Severus & Lily Luna Potter (children)"],
        "achievements": [
            "Survived possession by Tom Riddle's diary Horcrux in her first year",
            "Became a formidable Chaser, later playing professionally for the Holyhead Harpies",
            "Co-led Dumbledore's Army during Harry's absence in his sixth/seventh year",
            "Fought in the Battle of Hogwarts",
        ],
    },
    "voldemort": {
        "full_name": "Tom Marvolo Riddle (Lord Voldemort)",
        "overview": "Born to a Muggle father and a witch descended from Salazar Slytherin, "
                    "Tom Riddle grew into the most feared Dark Wizard of the age. Obsessed "
                    "with immortality and blood purity, he split his soul into seven Horcruxes "
                    "and waged two wars against the wizarding world before being finally "
                    "destroyed by Harry Potter.",
        "wand": {"wood": "Yew", "core": "Phoenix feather (Fawkes, twin to Harry's wand)",
                  "length": "13½ inches", "rigidity": "Unyielding"},
        "house": "Slytherin",
        "patronus": "None — incapable of casting a Patronus",
        "allies": ["Death Eaters", "Bellatrix Lestrange", "Lucius Malfoy", "Nagini"],
        "relatives": ["Tom Riddle Sr. (father)", "Merope Gaunt (mother)",
                       "Marvolo Gaunt (grandfather)"],
        "achievements": [
            "Opened the Chamber of Secrets as a student",
            "Created seven Horcruxes to achieve immortality",
            "Took control of the Ministry of Magic during the Second Wizarding War",
            "Defeated in the Battle of Hogwarts (1998)",
        ],
    },
}

# alias mapping for common nicknames / alternate spellings
ALIASES = {
    "the boy who lived": "harry potter",
    "voldemort": "voldemort",
    "tom riddle": "voldemort",
    "lord voldemort": "voldemort",
    "you-know-who": "voldemort",
    "snape": "severus snape",
    "professor snape": "severus snape",
    "dumbledore": "albus dumbledore",
    "professor dumbledore": "albus dumbledore",
    "hermione": "hermione granger",
    "ron": "ron weasley",
    "ronald weasley": "ron weasley",
    "draco": "draco malfoy",
    "malfoy": "draco malfoy",
    "luna": "luna lovegood",
    "neville": "neville longbottom",
    "ginny": "ginny weasley",
    "harry": "harry potter",
}

# --------------------------------------------------------------------------------------
# QUIZ DATA
# --------------------------------------------------------------------------------------
QUIZ_QUESTIONS = [
    {
        "question": "You find a locked door in an abandoned corridor at Hogwarts. What do you do?",
        "options": {
            "Pick the lock and go exploring immediately — adventure calls!": "Gryffindor",
            "Study the lock's enchantment first to understand how it works": "Ravenclaw",
            "Find a clever way around it that no one else would think of": "Slytherin",
            "Look for a professor or friend to explore it together, safely": "Hufflepuff",
        },
    },
    {
        "question": "A friend is struggling with a difficult class. How do you help?",
        "options": {
            "Charge in and confront whoever is making it hard for them": "Gryffindor",
            "Quietly tutor them for as long as it takes, no complaints": "Hufflepuff",
            "Give them a clever trick or shortcut to master it fast": "Ravenclaw",
            "Help them if it also benefits you somehow — mutual gain": "Slytherin",
        },
    },
    {
        "question": "Which quality do you value most in yourself?",
        "options": {
            "Bravery": "Gryffindor",
            "Loyalty": "Hufflepuff",
            "Ambition": "Slytherin",
            "Wisdom": "Ravenclaw",
        },
    },
    {
        "question": "The Sorting Hat is about to be placed on your head. What are you secretly hoping for?",
        "options": {
            "Somewhere I can prove my courage": "Gryffindor",
            "Somewhere I'll always belong, no matter what": "Hufflepuff",
            "Somewhere that will challenge my mind": "Ravenclaw",
            "Somewhere that will help me achieve greatness": "Slytherin",
        },
    },
    {
        "question": "Choose a class you'd most want to excel in:",
        "options": {
            "Defence Against the Dark Arts": "Gryffindor",
            "Herbology": "Hufflepuff",
            "Charms": "Ravenclaw",
            "Potions": "Slytherin",
        },
    },
    {
        "question": "Your worst fear (a Boggart) would most likely take the shape of:",
        "options": {
            "Being seen as a coward": "Gryffindor",
            "Losing the people you love": "Hufflepuff",
            "Never learning the truth about something important": "Ravenclaw",
            "Failure — falling short of your ambitions": "Slytherin",
        },
    },
]

# --------------------------------------------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------------------------------------------
def init_state():
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_result" not in st.session_state:
        st.session_state.quiz_result = None
    if "last_search" not in st.session_state:
        st.session_state.last_search = ""
    if "search_history" not in st.session_state:
        st.session_state.search_history = []


init_state()

# --------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------------------------------------------
def normalize(name: str) -> str:
    return name.strip().lower()


def lookup_character(query: str):
    key = normalize(query)
    if not key:
        return None
    if key in CHARACTERS:
        return CHARACTERS[key]
    if key in ALIASES:
        return CHARACTERS.get(ALIASES[key])
    # partial/fuzzy fallback: match if query is substring of any known name
    for name, data in CHARACTERS.items():
        if key in name or name in key:
            return data
    for alias, target in ALIASES.items():
        if key in alias or alias in key:
            return CHARACTERS.get(target)
    return None


def render_house_badge(house_name: str):
    house = HOUSES.get(house_name)
    if house:
        st.markdown(
            f'<span class="house-badge {house["badge_class"]}">{house_name}</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<span class="house-badge badge-unknown">{house_name}</span>',
            unsafe_allow_html=True,
        )


def render_character_card(name_display: str, data: dict):
    st.markdown('<div class="hp-card">', unsafe_allow_html=True)
    st.markdown(f"### {data.get('full_name', name_display.title())}")
    render_house_badge(data.get("house", "Unknown"))
    st.markdown(f"**Patronus:** {data.get('patronus', 'Unknown')}")
    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

    st.markdown("#### 📖 Biography / Overview")
    st.write(data.get("overview", "No overview available."))
    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

    st.markdown("#### 🪄 Wand Details")
    wand = data.get("wand", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"**Wood**\n\n{wand.get('wood', 'Unknown')}")
    c2.markdown(f"**Core**\n\n{wand.get('core', 'Unknown')}")
    c3.markdown(f"**Length**\n\n{wand.get('length', 'Unknown')}")
    c4.markdown(f"**Rigidity**\n\n{wand.get('rigidity', 'Unknown')}")
    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🤝 Inner Circle — Allies & Friends")
        allies = data.get("allies", [])
        st.write(", ".join(allies) if allies else "Unknown")
    with col_b:
        st.markdown("#### 👪 Relatives")
        relatives = data.get("relatives", [])
        st.write(", ".join(relatives) if relatives else "Unknown")
    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

    st.markdown("#### 🏆 Notable Achievements / Key Lore")
    for achievement in data.get("achievements", []):
        st.markdown(f"- {achievement}")

    st.markdown("</div>", unsafe_allow_html=True)


def render_fallback_card(query: str):
    st.markdown('<div class="hp-card">', unsafe_allow_html=True)
    st.markdown(f"### {query.title()}")
    render_house_badge("Unknown")
    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)
    st.warning(
        f"**\"{query.title()}\"** was not found in our local archive of major characters. "
        "This wizard or witch may be a lesser-known figure, or the name may be misspelled."
    )
    st.markdown("#### 📖 Suggestions")
    st.write(
        "- Double-check the spelling of the character's name.\n"
        "- Try searching using their most common name (e.g., 'Snape' instead of "
        "'Severus Tobias Snape').\n"
        "- Browse the characters listed in the sidebar for full profiles.\n"
        "- Full names, nicknames, and common aliases (like 'You-Know-Who') are supported "
        "for major characters."
    )
    st.markdown("</div>", unsafe_allow_html=True)


def score_quiz(answers: dict) -> str:
    tally = {house: 0 for house in HOUSES}
    for house in answers.values():
        if house in tally:
            tally[house] += 1
    max_score = max(tally.values())
    winners = [h for h, s in tally.items() if s == max_score]
    return random.choice(winners)


# --------------------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------------------------------------------
st.sidebar.markdown("## ⚡ Navigation")
page = st.sidebar.radio(
    "Choose a section:",
    ["🔍 Character Search", "🎩 Sorting Quiz"],
    label_visibility="collapsed",
)

st.sidebar.markdown('<hr class="hp-divider">', unsafe_allow_html=True)
st.sidebar.markdown("### 📚 Characters in Archive")
for name in sorted(CHARACTERS.keys()):
    st.sidebar.markdown(f"- {CHARACTERS[name]['full_name']}")

if st.session_state.search_history:
    st.sidebar.markdown('<hr class="hp-divider">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🕰️ Recent Searches")
    for h in st.session_state.search_history[-5:][::-1]:
        st.sidebar.markdown(f"- {h}")

# --------------------------------------------------------------------------------------
# MAIN TITLE
# --------------------------------------------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;'>⚡ Harry Potter Character & Sorting Hub ⚡</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; font-style:italic; color:#c9b98a;'>"
    "\"It is our choices, Harry, that show what we truly are, far more than our abilities.\""
    "</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# PAGE 1 — CHARACTER SEARCH
# --------------------------------------------------------------------------------------
if page == "🔍 Character Search":
    st.markdown("## 🔍 Character Search & Information Hub")
    st.write(
        "Search for any Harry Potter character by name — full name, first name, or common "
        "nickname all work for characters in our archive."
    )

    search_col, button_col = st.columns([4, 1])
    with search_col:
        query = st.text_input(
            "Enter a character name",
            value=st.session_state.last_search,
            placeholder="e.g., Harry Potter, Snape, Draco...",
            label_visibility="collapsed",
        )
    with button_col:
        search_clicked = st.button("🔎 Search", use_container_width=True)

    if search_clicked and query.strip():
        st.session_state.last_search = query
        if query.strip().title() not in st.session_state.search_history:
            st.session_state.search_history.append(query.strip().title())

    if st.session_state.last_search.strip():
        result = lookup_character(st.session_state.last_search)
        if result:
            render_character_card(st.session_state.last_search, result)
        else:
            render_fallback_card(st.session_state.last_search)
    else:
        st.info("Enter a character name above and press **Search** to view their profile.")

    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)
    st.markdown("### ✨ Quick Picks")
    quick_cols = st.columns(5)
    quick_names = ["Harry Potter", "Hermione Granger", "Severus Snape", "Draco Malfoy",
                   "Voldemort"]
    for col, name in zip(quick_cols, quick_names):
        with col:
            if st.button(name, use_container_width=True, key=f"quick_{name}"):
                st.session_state.last_search = name
                if name not in st.session_state.search_history:
                    st.session_state.search_history.append(name)
                st.rerun()

# --------------------------------------------------------------------------------------
# PAGE 2 — SORTING QUIZ
# --------------------------------------------------------------------------------------
elif page == "🎩 Sorting Quiz":
    st.markdown("## 🎩 Hogwarts House & Patronus Quiz")
    st.write(
        "Answer honestly — the Sorting Hat sees through bluffing! Answer all questions, "
        "then click **Reveal My House** below."
    )
    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

    for idx, q in enumerate(QUIZ_QUESTIONS):
        st.markdown(f'<p class="quiz-question">{idx + 1}. {q["question"]}</p>',
                     unsafe_allow_html=True)
        options = list(q["options"].keys())
        current_answer = st.session_state.quiz_answers.get(idx)
        default_index = options.index(current_answer) if current_answer in options else None
        choice = st.radio(
            f"Question {idx + 1}",
            options,
            index=default_index,
            key=f"quiz_q_{idx}",
            label_visibility="collapsed",
        )
        if choice:
            st.session_state.quiz_answers[idx] = q["options"][choice]
        st.markdown("")

    st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)

    all_answered = len(st.session_state.quiz_answers) == len(QUIZ_QUESTIONS)
    reveal_col1, reveal_col2 = st.columns([1, 1])
    with reveal_col1:
        if st.button("🎩 Reveal My House", disabled=not all_answered, use_container_width=True):
            house = score_quiz(st.session_state.quiz_answers)
            patronus = random.choice(HOUSES[house]["patronus_pool"])
            st.session_state.quiz_result = {"house": house, "patronus": patronus}
            st.session_state.quiz_submitted = True
    with reveal_col2:
        if st.button("🔄 Retake Quiz", use_container_width=True):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_result = None
            st.rerun()

    if not all_answered:
        st.caption(
            f"Answer all {len(QUIZ_QUESTIONS)} questions to unlock your result "
            f"({len(st.session_state.quiz_answers)}/{len(QUIZ_QUESTIONS)} answered)."
        )

    if st.session_state.quiz_submitted and st.session_state.quiz_result:
        house = st.session_state.quiz_result["house"]
        patronus = st.session_state.quiz_result["patronus"]
        house_info = HOUSES[house]

        house_bg = {
            "Gryffindor": "linear-gradient(160deg,#3a0002,#5c0001)",
            "Slytherin": "linear-gradient(160deg,#0b2416,#173b26)",
            "Ravenclaw": "linear-gradient(160deg,#070d24,#101a3a)",
            "Hufflepuff": "linear-gradient(160deg,#4a3b12,#6b5418)",
        }[house]

        st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)
        st.balloons()
        st.markdown(
            f"""
            <div class="result-hero" style="background:{house_bg};">
                <h2>🎉 You belong in {house}! 🎉</h2>
                <p style="font-size:1.1rem; color:#e9dfc8;">
                    Founded by {house_info['founder']} — colors: {house_info['colors']}
                </p>
                <p style="font-size:1.05rem; color:#e9dfc8; max-width:600px; margin:10px auto;">
                    {house_info['element_desc']}
                </p>
                <p style="font-size:1.2rem; margin-top:16px;">
                    🦌 <strong>Your Patronus:</strong> {patronus}
                </p>
                <p style="color:#c9b98a; font-style:italic;">
                    Your defining traits: {house_info['traits']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="hp-divider">', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#8a7a5c; font-size:0.85rem;'>"
    "Built with Streamlit • Fan-made project, unaffiliated with J.K. Rowling or Warner Bros."
    "</p>",
    unsafe_allow_html=True,
)
