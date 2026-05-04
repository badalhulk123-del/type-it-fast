import streamlit as st
import time
import random
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Typing Master", layout="wide")

# ---------------- CSS ANIMATIONS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
}

.quote {
    font-size: 24px;
    color: white;
    padding: 15px;
    border-left: 6px solid #ff4d6d;
    animation: fadeIn 1s ease-in-out;
}

.correct { color: #00ff9f; }
.wrong { color: #ff4d4d; }

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

.glow {
    color: #fff;
    text-shadow: 0 0 10px #ff4d6d, 0 0 20px #ff4d6d;
}

.metric-card {
    padding: 10px;
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- QUOTES ----------------
easy_quotes = [
    "Love is beautiful.",
    "You are my world.",
    "I miss you."
]

medium_quotes = [
    "You are my today and all of my tomorrows.",
    "Every love story is beautiful but ours is my favorite."
]

hard_quotes = [
    "Love is composed of a single soul inhabiting two bodies.",
    "I love you more than yesterday but less than tomorrow."
]

# ---------------- SESSION ----------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "started" not in st.session_state:
    st.session_state.started = False

if "quote" not in st.session_state:
    st.session_state.quote = random.choice(easy_quotes)

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"

if "best_wpm" not in st.session_state:
    st.session_state.best_wpm = 0

# ---------------- AI DIFFICULTY ----------------
def get_next_quote(wpm):
    if wpm < 30:
        st.session_state.difficulty = "Easy"
        return random.choice(easy_quotes)
    elif wpm < 60:
        st.session_state.difficulty = "Medium"
        return random.choice(medium_quotes)
    else:
        st.session_state.difficulty = "Hard"
        return random.choice(hard_quotes)

# ---------------- HIGHLIGHT ----------------
def highlight_text(target, typed):
    result = ""
    for i in range(len(target)):
        if i < len(typed):
            if target[i] == typed[i]:
                result += f"<span class='correct'>{target[i]}</span>"
            else:
                result += f"<span class='wrong'>{target[i]}</span>"
        else:
            result += target[i]
    return result

# ---------------- SUBMIT ----------------
def submit_test(text):
    end = time.time()
    total_time = end - st.session_state.start_time

    words = len(text.split())
    wpm = int((words / total_time) * 60)

    correct = sum(
        1 for i in range(min(len(text), len(st.session_state.quote)))
        if text[i] == st.session_state.quote[i]
    )

    accuracy = int((correct / len(st.session_state.quote)) * 100)

    # Update best score
    if wpm > st.session_state.best_wpm:
        st.session_state.best_wpm = wpm

    # AI next level
    st.session_state.quote = get_next_quote(wpm)

    st.session_state.started = False
    st.session_state.input_text = ""

    return total_time, wpm, accuracy

# ---------------- INPUT HANDLER ----------------
def handle_input():
    text = st.session_state.input_text

    if not st.session_state.started:
        st.session_state.started = True
        st.session_state.start_time = time.time()
        return

    if text.endswith("\n"):
        result = submit_test(text.strip())
        st.session_state.result = result

# ---------------- UI ----------------
st.title("💻 Typing Master")

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(
        f"<div class='quote glow'>{st.session_state.quote}</div>",
        unsafe_allow_html=True
    )

    st.text_area(
        "Type here (Enter = Start/Submit)",
        key="input_text",
        height=150,
        on_change=handle_input
    )

    typed = st.session_state.get("input_text", "")
    st.markdown(highlight_text(st.session_state.quote, typed), unsafe_allow_html=True)

# ---------------- SIDEBAR LIVE STATS ----------------
with col2:
    st.subheader("⚡ Live Stats")

    if st.session_state.started:
        elapsed = time.time() - st.session_state.start_time
        words = len(st.session_state.get("input_text","").split())
        live_wpm = int((words / elapsed) * 60) if elapsed > 0 else 0

        st.markdown(f"<div class='metric-card'>⏱ Time: {int(elapsed)} sec</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'>⚡ WPM: {live_wpm}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='metric-card'>🎯 Difficulty: {st.session_state.difficulty}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-card'>🏆 Best WPM: {st.session_state.best_wpm}</div>", unsafe_allow_html=True)

# ---------------- RESULT ----------------
if "result" in st.session_state:
    t, wpm, acc = st.session_state.result
    st.success(f"⏱ {int(t)} sec | ⚡ {wpm} WPM | 🎯 {acc}% Accuracy")
