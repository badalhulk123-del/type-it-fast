import streamlit as st
import time
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Typing Master Ultra ❤️", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.quote {
    font-size: 22px;
    color: white;
    padding: 10px;
    border-left: 5px solid #ff4d6d;
}
.correct { color: lightgreen; }
.wrong { color: red; }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
quotes = [
    "Love is composed of a single soul inhabiting two bodies.",
    "You are my today and all of my tomorrows.",
    "I saw that you were perfect and so I loved you.",
    "Every love story is beautiful but ours is my favorite.",
    "I love you more than yesterday but less than tomorrow."
]

# ---------------- SESSION ----------------
if "level" not in st.session_state:
    st.session_state.level = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "started" not in st.session_state:
    st.session_state.started = False

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- FUNCTIONS ----------------
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

def handle_typing():
    text = st.session_state.input_text

    # START on first Enter
    if not st.session_state.started:
        st.session_state.started = True
        st.session_state.start_time = time.time()
        return

    # SUBMIT on Enter again
    if text.endswith("\n"):
        submit_test(text.strip())

def submit_test(user_input):
    end = time.time()
    time_taken = end - st.session_state.start_time

    current_quote = quotes[st.session_state.level]

    words = len(user_input.split())
    wpm = int((words / time_taken) * 60)

    correct = sum(
        1 for i in range(min(len(user_input), len(current_quote)))
        if user_input[i] == current_quote[i]
    )

    errors = len(current_quote) - correct
    accuracy = int((correct / len(current_quote)) * 100)

    st.session_state.history.append({
        "WPM": wpm,
        "Accuracy": accuracy,
        "Errors": errors
    })

    st.session_state.result = {
        "time": int(time_taken),
        "wpm": wpm,
        "accuracy": accuracy,
        "errors": errors
    }

    if accuracy > 80:
        st.session_state.level += 1
        if st.session_state.level >= len(quotes):
            st.session_state.level = 0

    st.session_state.started = False
    st.session_state.input_text = ""

# ---------------- UI ----------------
st.title("💻 Typing Master Ultra ❤️")

current_quote = quotes[st.session_state.level]

st.subheader(f"Level {st.session_state.level + 1}")
st.markdown(f"<div class='quote'>{current_quote}</div>", unsafe_allow_html=True)

# INPUT BOX (ENTER DETECTION)
st.text_area(
    "Start typing (Press Enter to Start & Submit)",
    key="input_text",
    height=150,
    on_change=handle_typing
)

# ---------------- LIVE TIMER ----------------
if st.session_state.started:
    elapsed = int(time.time() - st.session_state.start_time)
    st.write(f"⏱ Live Time: {elapsed} sec")

# ---------------- LIVE HIGHLIGHT ----------------
typed = st.session_state.get("input_text", "")
st.markdown(highlight_text(current_quote, typed), unsafe_allow_html=True)

# ---------------- RESULT ----------------
if "result" in st.session_state:
    r = st.session_state.result
    st.write(f"⏱ Time: {r['time']} sec")
    st.write(f"⚡ WPM: {r['wpm']}")
    st.write(f"🎯 Accuracy: {r['accuracy']}%")
    st.write(f"❌ Errors: {r['errors']}")

# ---------------- ANALYTICS ----------------
st.subheader("📊 Performance")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df["WPM"])
    st.line_chart(df["Accuracy"])
    st.bar_chart(df["Errors"])
else:
    st.info("Start typing to see analytics!")
