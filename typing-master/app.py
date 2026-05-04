import streamlit as st
import time

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Typing Master ❤️", layout="centered")

# ---------------------------
# CUSTOM CSS (PREMIUM UI)
# ---------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ff758c, #ff7eb3);
}
.main {
    background: rgba(0,0,0,0.7);
    padding: 30px;
    border-radius: 20px;
}
h1 {
    text-align: center;
    color: white;
}
.quote {
    font-size: 20px;
    color: #fff;
    margin-bottom: 15px;
}
.result {
    font-size: 18px;
    color: #00ffcc;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# DATA
# ---------------------------
quotes = [
    "Love is composed of a single soul inhabiting two bodies.",
    "You are my today and all of my tomorrows.",
    "I saw that you were perfect, and so I loved you.",
    "Every love story is beautiful, but ours is my favorite.",
    "I love you more than yesterday but less than tomorrow."
]

# ---------------------------
# SESSION STATE
# ---------------------------
if "level" not in st.session_state:
    st.session_state.level = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ---------------------------
# UI
# ---------------------------
st.title("💻 Typing Master ❤️")

st.subheader(f"Level {st.session_state.level + 1}")

current_quote = quotes[st.session_state.level]

st.markdown(f"<div class='quote'>{current_quote}</div>", unsafe_allow_html=True)

user_input = st.text_area("Start typing here...")

col1, col2 = st.columns(2)

# ---------------------------
# START BUTTON
# ---------------------------
with col1:
    if st.button("Start"):
        st.session_state.start_time = time.time()

# ---------------------------
# SUBMIT BUTTON
# ---------------------------
with col2:
    if st.button("Submit"):
        if st.session_state.start_time is None:
            st.warning("Click Start first!")
        else:
            end_time = time.time()
            time_taken = end_time - st.session_state.start_time

            words = len(user_input.split())
            wpm = int((words / time_taken) * 60)

            correct_chars = sum(
                1 for i in range(min(len(user_input), len(current_quote)))
                if user_input[i] == current_quote[i]
            )

            accuracy = int((correct_chars / len(current_quote)) * 100)

            st.write(f"⏱ Time: {int(time_taken)} sec")
            st.write(f"⚡ WPM: {wpm}")
            st.write(f"🎯 Accuracy: {accuracy}%")

            if accuracy > 80:
                st.markdown(
                    f"<div class='result'>💖 Level Completed!<br>{current_quote}</div>",
                    unsafe_allow_html=True
                )
                st.session_state.level += 1

                if st.session_state.level >= len(quotes):
                    st.success("🎉 You completed all levels!")
                    st.session_state.level = 0
            else:
                st.error("❌ Try Again!")

# ---------------------------
# PROGRESS BAR
# ---------------------------
progress = (st.session_state.level) / len(quotes)
st.progress(progress)
