import streamlit as st
import importlib
import os
from sheets import save_response

circle_key = st.secrets.get("CIRCLE", "active")
cfg = importlib.import_module(f"config_{circle_key}")
WEBAPP_URL = st.secrets["WEBAPP_URL"]

st.set_page_config(page_title=cfg.CIRCLE_NAME, page_icon="\U0001F338")

st.markdown('''
<style>
...
</style>
''', unsafe_allow_html=True)

COUNTRY_CODES = [...]

if "page" not in st.session_state:
    st.session_state.page = 1
    st.session_state.answers = [""] * len(cfg.QUESTIONS)

if os.path.exists(cfg.LOGO_FILE):
    st.image(cfg.LOGO_FILE, use_container_width=True)

total_pages = len(cfg.QUESTIONS)

# ------------------------------------------------------------
# PAGES 1..N: one question each (numbered, with optional helper)
# ------------------------------------------------------------
if 1 <= st.session_state.page <= total_pages:
    i = st.session_state.page - 1
    question = cfg.QUESTIONS[i]

    st.markdown(
        f'<p class="q-line"><span class="q-num">{st.session_state.page}.</span>{question["q"]}</p>',
        unsafe_allow_html=True,
    )
    if question.get("helper"):
        st.markdown(f'<p class="q-help">{question["helper"]}</p>', unsafe_allow_html=True)

    st.session_state.answers[i] = st.text_area(
        "Your answer",
        value=st.session_state.answers[i],
        max_chars=3000,
        height=200,
        key=f"q{i}",
        label_visibility="collapsed",
        placeholder="Type your answer here...",
    )

    if st.session_state.page > 1:
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            if st.button("Back"):
                st.session_state.page -= 1
                st.rerun()
        with c2:
            if st.button("Next"):
                st.session_state.page += 1
                st.rerun()
    else:
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("Next"):
                st.session_state.page += 1
                st.rerun()

# ------------------------------------------------------------
# CONTACT PAGE
# ------------------------------------------------------------
elif st.session_state.page == total_pages + 1:
    ...

# ------------------------------------------------------------
# THANK YOU PAGE
# ------------------------------------------------------------
else:
    ...
