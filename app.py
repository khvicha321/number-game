import streamlit as st
import random

st.title("🎮 გამოიცანი საიდუმლო რიცხვი (1-50)")

# პირველად რომ ჩაირთოს
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 50)
    st.session_state.attempts = 0
    st.session_state.max_attempts = 7   # ცოტათი გავზარდეთ მცდელობა
    st.session_state.game_over = False

guess = st.number_input("შეიყვანე რიცხვი (1-50):",
                        min_value=1,
                        max_value=50,
                        step=1)

if st.button("ცდა") and not st.session_state.game_over:
    st.session_state.attempts += 1

    if guess == st.session_state.secret:
        st.success("გილოცავ! სწორად გამოიცანი 🎉")
        st.session_state.game_over = True

    elif st.session_state.attempts >= st.session_state.max_attempts:
        st.error(f"წააგე 😢 საიდუმლო რიცხვი იყო {st.session_state.secret}")
        st.session_state.game_over = True

    elif guess > st.session_state.secret:
        st.warning("ძალიან დიდი რიცხვია 📉")

    else:
        st.warning("ძალიან პატარა რიცხვია 📈")

st.write("დარჩენილი მცდელობა:",
         st.session_state.max_attempts - st.session_state.attempts)

if st.button("ახალი თამაში"):
    st.session_state.secret = random.randint(1, 50)
    st.session_state.attempts = 0
    st.session_state.game_over = False