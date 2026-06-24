
import streamlit as st
import importlib
from sheets import save_response

# ------------------------------------------------------------
# Which circle's config to load is set by Streamlit secrets.
# Locally it defaults to "active". On deploy, each app sets its own.
# ------------------------------------------------------------
circle_key = st.secrets.get("CIRCLE", "active")
cfg = importlib.import_module(f"config_{circle_key}")
WEBAPP_URL = st.secrets["WEBAPP_URL"]

# --- Page setup & branding ---
st.set_page_config(page_title=cfg.CIRCLE_NAME, page_icon="📝")

# Apply brand color to buttons via a little CSS
st.markdown(
    f"<style>div.stButton > button {{ background-color: {cfg.BRAND_COLOR}; color: white; border: none; }}</style>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# SESSION STATE: this is how Streamlit remembers progress
# across reruns. We set up our memory the first time only.
# ------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0            # 0 = welcome, then 1..N = questions
    st.session_state.answers = [""] * len(cfg.QUESTIONS)
    st.session_state.submitted = False

# Show the logo if it exists
import os
if os.path.exists(cfg.LOGO_FILE):
    st.image(cfg.LOGO_FILE, width=180)

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
# PAGES 1..N: one question each
# ------------------------------------------------------------
elif 1 <= st.session_state.page <= total_pages:
    i = st.session_state.page - 1   # index into the questions list
    st.subheader(f"Question {st.session_state.page} of {total_pages}")
    st.write(cfg.QUESTIONS[i])

    # The text box. Its value is tied to session_state so it persists.
    st.session_state.answers[i] = st.text_area(
        "Your answer",
        value=st.session_state.answers[i],
        max_chars=3000,
        height=200,
        key=f"q{i}",
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
# CONTACT PAGE (after the last question)
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
                WEBAPP_URL,
                cfg.CIRCLE_NAME,
                st.session_state.answers,
                name, phone, email,
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
