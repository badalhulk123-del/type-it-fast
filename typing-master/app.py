import streamlit as st
import time
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Typing Master Ultra ❤️", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
}
.main {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
}
.quote {
    font-size: 22px;
    color: #ffffff;
    padding: 10px;
    border-left: 5px solid #ff4d6d;
}
.success-box {
    background: rgba(0,255,150,0.2);
    padding: 15px;
    border-radius: 10px;
}
.error-box {
    background: rgba(255,0,0,0.2);
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ DATA ------------------
quotes = [
    "Love is composed of a single soul inhabiting two bodies.",
    "You are my today and all of my tomorrows.",
    "I saw that you were perfect, and so I loved you.",
    "Every love story is beautiful but ours is my favorite.",
    "I love you more than yesterday but less than tomorrow."
]

# ------------------ SESSION ------------------
if "level" not in st.session_state:
    st.session_state.level = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ UI ------------------
st.title("💻 Typing Master Ultra ❤️")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader(f"Level {st.session_state.level + 1}")
    current_quote = quotes[st.session_state.level]
    st.markdown(f"<div class='quote'>{current_quote}</div>", unsafe_allow_html=True)

    user_input = st.text_area("Start typing here...", height=150)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🚀 Start"):
            st.session_state.start_time = time.time()

    with c2:
        if st.button("✅ Submit"):
            if st.session_state.start_time is None:
                st.warning("Click Start first!")
            else:
                end = time.time()
                time_taken = end - st.session_state.start_time

                words = len(user_input.split())
                wpm = int((words / time_taken) * 60)

                correct = sum(
                    1 for i in range(min(len(user_input), len(current_quote)))
                    if user_input[i] == current_quote[i]
                )

                errors = len(current_quote) - correct
                accuracy = int((correct / len(current_quote)) * 100)

                # Save history
                st.session_state.history.append({
                    "WPM": wpm,
                    "Accuracy": accuracy,
                    "Errors": errors
                })

                st.write(f"⏱ Time: {int(time_taken)} sec")
                st.write(f"⚡ WPM: {wpm}")
                st.write(f"🎯 Accuracy: {accuracy}%")
                st.write(f"❌ Errors: {errors}")

                if accuracy > 80:
                    st.markdown(
                        f"<div class='success-box'>💖 Level Completed!<br>{current_quote}</div>",
                        unsafe_allow_html=True
                    )
                    st.session_state.level += 1

                    if st.session_state.level >= len(quotes):
                        st.balloons()
                        st.success("🎉 You completed all levels!")
                        st.session_state.level = 0
                else:
                    st.markdown(
                        "<div class='error-box'>❌ Try Again!</div>",
                        unsafe_allow_html=True
                    )

    # Progress
    progress = st.session_state.level / len(quotes)
    st.progress(progress)

# ------------------ ANALYTICS PANEL ------------------
with col2:
    st.subheader("📊 Performance")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        st.line_chart(df["WPM"])
        st.line_chart(df["Accuracy"])
        st.bar_chart(df["Errors"])

    else:
        st.info("Play to see analytics!")

# ------------------ LIVE FEEDBACK ------------------
st.subheader("🧠 Live Typing Feedback")

def highlight_text(target, typed):
    result = ""
    for i in range(len(target)):
        if i < len(typed):
            if target[i] == typed[i]:
                result += f"<span style='color:lightgreen'>{target[i]}</span>"
            else:
                result += f"<span style='color:red'>{target[i]}</span>"
        else:
            result += target[i]
    return result

st.markdown(
    highlight_text(current_quote, user_input),
    unsafe_allow_html=True
)
