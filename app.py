import streamlit as st
import random


def load_pairs(filepath):
    pairs = []

    f = open(filepath, "r", encoding="utf-8")
    lines = f.readlines()
    f.close()

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        parts = line.split("|")
        if len(parts) != 2:
            continue

        country = parts[0].strip()
        capital = parts[1].strip()

        if country != "" and capital != "":
            pairs.append((country, capital))

    return pairs


def pick_pair_by_difficulty(pairs, difficulty):
    pool = []

    if difficulty == "Easy":
        for country, capital in pairs:
            if len(capital) <= 6:
                pool.append((country, capital))
        lives = 7

    elif difficulty == "Medium":
        for country, capital in pairs:
            if len(capital) <= 10:
                pool.append((country, capital))
        lives = 5

    else:
        for country, capital in pairs:
            if len(capital) > 10:
                pool.append((country, capital))
        lives = 3

    if len(pool) == 0:
        pool = pairs

    country, capital = random.choice(pool)
    return country, capital, lives


def make_mask(capital, guessed):
    masked = ""

    for ch in capital:
        if ch == " " or ch == "-":
            masked = masked + ch
        else:
            if ch.lower() in guessed:
                masked = masked + ch
            else:
                masked = masked + "_"

    return masked


def has_underscore(masked):
    for ch in masked:
        if ch == "_":
            return True
    return False


def new_game(pairs, difficulty):
    country, capital, lives = pick_pair_by_difficulty(pairs, difficulty)

    st.session_state["country"] = country
    st.session_state["capital"] = capital
    st.session_state["lives"] = lives
    st.session_state["good"] = []
    st.session_state["bad"] = []
    st.session_state["guessed"] = []
    st.session_state["status"] = "playing"


def guess(letter):
    if st.session_state["status"] != "playing":
        return

    if letter is None:
        return

    letter = letter.strip().lower()

    if len(letter) != 1:
        return

    if letter.isalpha() is False:
        return

    if letter in st.session_state["guessed"]:
        return

    st.session_state["guessed"].append(letter)

    capital = st.session_state["capital"]
    found = False

    for ch in capital:
        if ch.lower() == letter:
            found = True
            break

    if found:
        st.session_state["good"].append(letter)
    else:
        st.session_state["bad"].append(letter)
        st.session_state["lives"] = st.session_state["lives"] - 1

    masked = make_mask(capital, st.session_state["guessed"])

    if has_underscore(masked) is False:
        st.session_state["status"] = "win"

    if st.session_state["lives"] <= 0:
        st.session_state["status"] = "game_over"


st.set_page_config(page_title="Hangman - Countries & Capitals", layout="centered")
st.title("Hangman – Countries & Capitals Edition")

pairs = load_pairs("countries-and-capitals.txt")

difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

col1, col2 = st.columns(2)

with col1:
    if st.button("New game"):
        new_game(pairs, difficulty)

with col2:
    if st.button("Reset"):
        keys = list(st.session_state.keys())
        for k in keys:
            del st.session_state[k]
        st.rerun()

if "country" not in st.session_state:
    st.info("Click New game to start.")
    st.stop()

country = st.session_state["country"]
capital = st.session_state["capital"]
lives = st.session_state["lives"]
status = st.session_state["status"]

masked = make_mask(capital, st.session_state["guessed"])

st.subheader("Game")
st.write("Country:", country)
st.write("Capital:", masked)
st.write("Lives:", lives)

st.write("Correct guesses:", ", ".join(st.session_state["good"]))
st.write("Wrong guesses:", ", ".join(st.session_state["bad"]))

if status == "playing":
    letter = st.text_input("Type one letter", value="", max_chars=1)
    if st.button("Guess"):
        guess(letter)
        st.rerun()

if status == "win":
    st.success("WIN")
    st.write("Solution:", capital, "(", country, ")")

if status == "game_over":
    st.error("GAME OVER")
    st.write("Solution was:", capital, "(", country, ")")
