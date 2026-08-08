# ⚡ Harry Potter Character & Sorting Hub

A wizarding-themed Streamlit web app that lets you look up Harry Potter characters and take an interactive Hogwarts Sorting Quiz to discover your House and Patronus.

## 🌐 Live Demo

👉 **[harrypotter7.streamlit.app](https://harrypotter7.streamlit.app)**

## ✨ Features

### 🔍 Character Search & Information Hub
- Search any Harry Potter character by full name, first name, or common nickname/alias (e.g. "Snape," "Draco," "You-Know-Who").
- Local database of 10 major characters — Harry Potter, Hermione Granger, Ron Weasley, Albus Dumbledore, Severus Snape, Draco Malfoy, Luna Lovegood, Neville Longbottom, Ginny Weasley, and Voldemort.
- Each profile includes:
  - Full biography / overview
  - Wand details (wood, core, length, rigidity)
  - Hogwarts House & Patronus
  - Inner circle (allies, relatives, close friends)
  - Notable achievements / key lore
- Fuzzy fallback matching for partial/misspelled names, plus a friendly "not found" card with search tips when a character isn't in the archive.
- Quick-pick buttons and a recent-searches list in the sidebar.

### 🎩 Hogwarts House & Patronus Quiz
- 6 Harry Potter–themed multiple-choice questions.
- Answers are scored per house (Gryffindor, Slytherin, Ravenclaw, Hufflepuff); ties are broken randomly.
- Results reveal your House with its colors, founder, personality description, defining traits, and a randomly assigned Patronus — complete with a celebratory balloon animation.
- Retake button to reset and try again.

### 🎨 Wizarding Theme
- Dark, starry-night/parchment gradient background.
- Elegant serif fonts (Cinzel / EB Garamond) with glowing gold headings.
- House-colored badges (Gryffindor, Slytherin, Ravenclaw, Hufflepuff).
- Custom card containers, dividers, and styled buttons/inputs.

### 🧠 Persistent State
- Search text, search history, and quiz answers/results are stored in `st.session_state`, so nothing resets while you navigate or interact with the app.

## 📁 Project Structure

```
.
├── app.py          # Complete Streamlit application (UI, data, logic, CSS)
└── README.md        # This file
```

Everything — the character database, quiz questions, styling, and app logic — lives in the single `app.py` file for simplicity.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher

### 1. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install streamlit
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`. If it doesn't, open that URL manually.

### 4. Stop the app
Press `Ctrl+C` in the terminal where Streamlit is running.

## 🕹️ How to Use

1. **Character Search** — Select "🔍 Character Search" in the sidebar, type a character's name into the search bar, and click **Search**. Use the Quick Picks buttons for one-click access to popular characters.
2. **Sorting Quiz** — Select "🎩 Sorting Quiz" in the sidebar, answer all 6 questions, then click **Reveal My House** to see your Hogwarts House and Patronus. Click **Retake Quiz** to start over.

## 🛠️ Customization Ideas
- Add more characters to the `CHARACTERS` dictionary in `app.py` (each entry follows the same structure: `full_name`, `overview`, `wand`, `house`, `patronus`, `allies`, `relatives`, `achievements`).
- Add more entries to `ALIASES` to support additional nicknames.
- Extend `QUIZ_QUESTIONS` with more questions, or adjust scoring logic in `score_quiz()`.
- Tweak the `CUSTOM_CSS` block to adjust colors, fonts, or layout.

## ⚠️ Disclaimer
This is an unofficial fan-made project built for educational/demonstration purposes. It is not affiliated with, endorsed by, or connected to J.K. Rowling, Warner Bros., or the official Harry Potter franchise. All character names and related content are the property of their respective owners.

## 📦 Requirements
```
streamlit
```

(Python's built-in `random` module is also used — no extra installation needed.)
