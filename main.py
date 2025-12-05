import streamlit as st
import time

st.set_page_config(page_title="Game", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        color: #f5f5f5;
    }
    [data-testid="stHeader"] {
        background: rgba(5, 5, 5, 0.9);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    p, span, label {
        color: #d0d0d0;
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 600px;
    }
    .stTextInput > div > div > input {
        background-color: #0a0a0a;
        border: 1px solid #333333;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
        outline: none;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0f0f0f, #050505);
        border: 1px solid #333333;
        color: #ffffff;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-size: 1rem;
        transition: all 0.2s ease;
       
    }
    .stButton > button:hover {
        border-color: #ffffff;
        background: #000000;
        transform: scale(0.97);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }
    .stButton > button:active {
        transform: scale(0.93);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2rem;
    }
    [data-testid="stMetricLabel"] {
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "current_level" not in st.session_state:
    st.session_state.current_level = 1
if "lives" not in st.session_state:
    st.session_state.lives = 7
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "completed_levels" not in st.session_state:
    st.session_state.completed_levels = []
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "hint_shown" not in st.session_state:
    st.session_state.hint_shown = {}

LEVEL_ANSWERS = {
    1: {"type": "range", "range": (7.0, 7.3)},
    2: {"type": "text", "value": "11221"},
    3: {"type": "text", "value": "1.2x+2.2"},
    4: {"type": "integer", "value": "20922287"},
    5: {"type": "integer", "value": 169},
    6: {"type": "text", "value": "mission complete"}
}

LEVEL_DESCRIPTIONS = {
    1: "Measure the velocity of the ball falling down the slope",
    2: "Look more closely at the tiles. What is code?",
    3: "Correclty complete the pH test.",
    4: "Identify the number for each letter in the 'caution' sign ",
    5: "Assemble the logic circuit and complete the truth table. X is the denary value of the output.",
    6: "Type the final mission codeword"
}

LEVEL_TITLES = {
    1: "PHYSICS",
    2: "BIOLOGY (1)",
    3: "BIOLOGY (2)",
    4: "CHEMISTRY",
    5: "COMPUTER SCIENCE",
    6: "FINAL"
}

LEVEL_NUMBERS_MEMORISE = {
    1: "4",
    2: "8",
    3: "1",
    4: "3",
    5: "486"

}
def check_answer(level, answer):
    config = LEVEL_ANSWERS.get(level)
    if not config:
        return False, None

    answer_type = config.get("type", "text")
    raw_value = answer.strip()

    if answer_type == "text":
        expected = str(config.get("value", "")).strip().lower()
        return raw_value.lower() == expected, None

    if answer_type == "integer":
        try:
            user_value = int(raw_value)
        except ValueError:
            return False, "Please enter an integer value."
        expected = int(config.get("value", 0))
        return user_value == expected, None

    if answer_type == "float":
        try:
            user_value = float(raw_value)
        except ValueError:
            return False, "Please enter a real number."
        expected = float(config.get("value", 0.0))
        tolerance = float(config.get("tolerance", 0.0))
        return abs(user_value - expected) <= tolerance, None

    if answer_type == "range":
        try:
            user_value = float(raw_value)
        except ValueError:
            return False, "Please enter a real number."
        lower, upper = config.get("range", (None, None))
        if lower is None or upper is None:
            return False, None
        return lower <= user_value <= upper, None

    return False, "Unsupported answer type."

def reset_game():
    st.session_state.current_level = 1
    st.session_state.lives = 7
    st.session_state.game_over = False
    st.session_state.completed_levels = []
    st.session_state.user_answer = ""
    st.session_state.hint_shown = {}

if st.session_state.game_over or st.session_state.lives <= 0:
    st.title("Game Over")
    st.markdown("---")
    st.markdown(f"### You ran out of lives!")
    st.markdown(f"**Levels completed:** {len(st.session_state.completed_levels)}/6")
    
    if st.button("Restart Game", use_container_width=True):
        reset_game()
        st.rerun()
    st.stop()

if st.session_state.current_level > 6:
    st.title("🎉 Victory!")
    st.markdown("---")
    st.markdown("### Congratulations! You completed all levels!")
    st.markdown(f"**Lives remaining:** {st.session_state.lives}")
    
    if st.button("Play Again", use_container_width=True):
        reset_game()
        st.rerun()
    st.stop()

current_level = st.session_state.current_level

col1, col2 = st.columns(2)
with col1:
    st.metric("Level", f"{current_level}/6")
with col2:
    st.metric("Lives", st.session_state.lives)

st.markdown("---")

st.markdown(f"# Level {current_level} - <u>{LEVEL_TITLES[current_level]}</u>", unsafe_allow_html=True)

hint_shown_for_level = st.session_state.hint_shown.get(current_level, False)

if not hint_shown_for_level:
    hint_button_disabled = st.session_state.lives <= 0
    if st.button("Get Hint", use_container_width=True, type="secondary", disabled=hint_button_disabled):
        if st.session_state.lives > 0:
            st.session_state.lives -= 1
            st.session_state.hint_shown[current_level] = True
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
            st.rerun()
    if hint_button_disabled:
        st.caption("⚠️ No lives remaining - cannot get hint")
else:
    st.markdown(f"###### <u>HINT</u>: {LEVEL_DESCRIPTIONS[current_level]}", unsafe_allow_html=True)

st.text("")

user_answer = st.text_input(
    "Your Answer",
    value=st.session_state.user_answer,
    key=f"answer_input_{current_level}",
    label_visibility="visible"
)

st.text("")
submit_button = st.button("Submit Answer", use_container_width=True, type="primary")

if submit_button:
    with st.spinner("Checking answer..."):
        time.sleep(2.5)
    if user_answer.strip():
        is_correct, feedback = check_answer(current_level, user_answer)
        if feedback:
            st.warning(feedback)
        elif is_correct:
            st.toast(f"TASK: MEMORISE NUMBER: '{LEVEL_NUMBERS_MEMORISE[current_level]}'", icon="💡")
            st.success("✓ Correct! Moving to next level...")
            time.sleep(3)
            st.session_state.completed_levels.append(current_level)
            st.session_state.current_level += 1
            if st.session_state.current_level == 6:
                st.session_state.lives = 2
            st.session_state.user_answer = ""
            st.rerun()
        else:
            st.session_state.lives -= 1
            st.error(f"✗ Incorrect! You have {st.session_state.lives} lives remaining.")
            time.sleep(3)
            st.session_state.user_answer = ""
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
                st.rerun()
            st.rerun()
    else:
        st.warning("Please enter an answer before submitting.")
