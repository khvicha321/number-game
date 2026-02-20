import streamlit as st
import random

st.set_page_config(page_title="Guess the Number", page_icon="🎮")

st.title("🎮 გამოიცანი საიდუმლო რიცხვი")
st.caption("აირჩიე სირთულე, გაქვს შეზღუდული მცდელობები და მიიღე მინიშნებები 😉")

# --- Difficulty settings ---
LEVELS = {
    "Easy (1-10, 5 მცდელობა)": {"min": 1, "max": 10, "attempts": 5},
    "Medium (1-50, 7 მცდელობა)": {"min": 1, "max": 50, "attempts": 7},
    "Hard (1-100, 10 მცდელობა)": {"min": 1, "max": 100, "attempts": 10},
}

level_name = st.selectbox("აირჩიე სირთულე:", list(LEVELS.keys()))
cfg = LEVELS[level_name]

def new_game():
    st.session_state.secret = random.randint(cfg["min"], cfg["max"])
    st.session_state.attempts = 0
    st.session_state.max_attempts = cfg["attempts"]
    st.session_state.game_over = False
    st.session_state.last_msg = ""
    st.session_state.level_name = level_name

# --- Init / reset if level changed ---
if "secret" not in st.session_state:
    new_game()
elif st.session_state.get("level_name") != level_name:
    new_game()

colA, colB = st.columns([2, 1])
with colA:
    guess = st.number_input(
        f"შეიყვანე რიცხვი ({cfg['min']}-{cfg['max']}):",
        min_value=cfg["min"],
        max_value=cfg["max"],
        step=1
    )
with colB:
    st.write("")
    st.write("")
    try_btn = st.button("ცდა ✅", use_container_width=True, disabled=st.session_state.game_over)

guess = int(guess)  # streamlit number_input ზოგჯერ float-ს აბრუნებს

# --- Game logic ---
if try_btn:
    st.session_state.attempts += 1
    secret = st.session_state.secret

    if guess == secret:
        st.session_state.last_msg = f"გილოცავ! სწორად გამოიცანი 🎉 (მცდელობები: {st.session_state.attempts})"
        st.session_state.game_over = True
    else:
        # მინიშნება: ახლოს ხარ?
        close = abs(guess - secret) <= 3

        if guess > secret:
            msg = "ძალიან დიდი რიცხვია 📉"
        else:
            msg = "ძალიან პატარა რიცხვია 📈"

        if close:
            msg += " — ძალიან ახლოს ხარ 🔥"

        st.session_state.last_msg = msg

        if st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.last_msg = f"წააგე 😢 საიდუმლო რიცხვი იყო: {secret}"
            st.session_state.game_over = True

# --- Status area ---
remaining = st.session_state.max_attempts - st.session_state.attempts
st.metric("დარჩენილი მცდელობები", remaining)

if st.session_state.last_msg:
    if "გილოცავ" in st.session_state.last_msg:
        st.success(st.session_state.last_msg)
    elif "წააგე" in st.session_state.last_msg:
        st.error(st.session_state.last_msg)
    else:
        st.warning(st.session_state.last_msg)

# --- Controls ---
col1, col2 = st.columns(2)
with col1:
    if st.button("ახალი თამაში 🔄", use_container_width=True):
        new_game()
        st.rerun()

with col2:
    show_secret = st.toggle("დამალული რიცხვის ჩვენება (მასწავლებლის რეჟიმი)")
    if show_secret:
        st.info(f"საიდუმლო რიცხვია: {st.session_state.secret}")
