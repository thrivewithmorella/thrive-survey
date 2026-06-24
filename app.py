
import streamlit as st
import importlib
import os
from sheets import save_response

# ------------------------------------------------------------
# Load this app's circle config from Streamlit secrets.
# ------------------------------------------------------------
circle_key = st.secrets.get("CIRCLE", "active")
cfg = importlib.import_module(f"config_{circle_key}")
WEBAPP_URL = st.secrets["WEBAPP_URL"]

st.set_page_config(page_title=cfg.CIRCLE_NAME, page_icon="🌸")

# ------------------------------------------------------------
# BRAND STYLING
# Palette: Ivory #FAF7F2 / Charcoal #2E2A2B / Watermelon #DF577B / Stone #D8D1C8
# Fonts:  Fraunces (headings) + Nunito Sans (body)
# ------------------------------------------------------------
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Nunito+Sans:wght@400;600;700&display=swap');

/* Page background + body font */
.stApp { background-color: #FAF7F2; }
html, body, [class*="css"] { font-family: 'Nunito Sans', sans-serif; color: #2E2A2B; }

/* Headings in Fraunces */
h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #2E2A2B !important; font-weight: 500; }

/* Center the logo */
div[data-testid="stImage"] { display: flex; justify-content: center; }
div[data-testid="stImage"] img { margin: 0 auto; }

/* Rounded answer box */
.stTextArea textarea, .stTextInput input {
    border-radius: 12px !important;
    border: 1px solid #D8D1C8 !important;
    background-color: #FFFFFF !important;
    padding: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    color: #2E2A2B !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #DF577B !important;
    box-shadow: 0 0 0 2px rgba(223,87,123,0.18) !important;
}

/* Accent buttons */
div.stButton > button {
    background-color: #DF577B;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 0.55rem 1.4rem;
    font-family: 'Nunito Sans', sans-serif;
    font-weight: 700;
    transition: background-color 0.15s ease;
}
div.stButton > button:hover { background-color: #C8456A; color: #FFFFFF; }
div.stButton > button:active { transform: scale(0.98); }

/* Hide Streamlit's default chrome for a cleaner, less-"Streamlit" look */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
''', unsafe_allow_html=True)

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.answers = [""] * len(cfg.QUESTIONS)

# Logo (skipped gracefully if missing)
if os.path.exists(cfg.LOGO_FILE):
    st.image(cfg.LOGO_FILE, width=200)

total_pages = len(cfg.QUESTIONS)

# ------------------------------------------------------------
# PAGE 0: Welcome
# ------------------------------------------------------------
if st.session_state.page == 0:
    st.title(cfg.WELCOME_TITLE)
    st.write(cfg.WELCOME_TEXT)
    if st.button("Start"):
        st.session_state.page = 1
        st.rerun()

# ------------------------------------------------------------
# PAGES 1..N: one question each (no counter heading)
# ------------------------------------------------------------
elif 1 <= st.session_state.page <= total_pages:
    i = st.session_state.page - 1
    st.write(cfg.QUESTIONS[i])

    st.session_state.answers[i] = st.text_area(
        "Your answer",
        value=st.session_state.answers[i],
        max_chars=3000,
        height=200,
        key=f"q{i}",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.page > 1:
            if st.button("Back"):
                st.session_state.page -= 1
                st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state.page += 1
            st.rerun()

# ------------------------------------------------------------
# CONTACT PAGE
# ------------------------------------------------------------
elif st.session_state.page == total_pages + 1:
    st.subheader("Almost done")
    st.write(cfg.CONTACT_INTRO)

    name  = st.text_input("Name",  key="name")
    phone = st.text_input("Phone", key="phone")
    email = st.text_input("Email", key="email")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page -= 1
            st.rerun()
    with col2:
        if st.button("Submit"):
            ok = save_response(
                WEBAPP_URL, cfg.CIRCLE_NAME,
                st.session_state.answers, name, phone, email,
            )
            if ok:
                st.session_state.page = total_pages + 2
                st.rerun()
            else:
                st.error("Something went wrong sending your response. Please try again.")

# ------------------------------------------------------------
# THANK YOU PAGE
# ------------------------------------------------------------
else:
    st.title(cfg.THANKYOU_TITLE)
    st.write(cfg.THANKYOU_TEXT)
    st.markdown(f"[Visit our website]({cfg.WEBSITE_URL})")
    st.markdown(f"[Follow us]({cfg.SOCIAL_URL})")
