import streamlit as st
import importlib
import os
from sheets import save_response

os.environ["WEBAPP_URL"] = "https://script.google.com/macros/s/AKfycbw-RgZsvwhHkrzeV2DUWmGeE5VOCL2jPoC9jPSNgYkCCU_0kczBaly2KWCqClR-1pMK/exec"

circle_key = st.secrets.get("CIRCLE", "active")
cfg = importlib.import_module(f"config_{circle_key}")
WEBAPP_URL = os.environ["WEBAPP_URL"]

st.set_page_config(page_title=cfg.CIRCLE_NAME, page_icon="\U0001F338")

st.markdown('''
<style>
...
/* Action buttons */
div.stButton > button {
    background-color: #DF577B;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 0.55rem 1.4rem;
    font-family: 'Nunito Sans', sans-serif;
    font-weight: 700;
    transition: background-color 0.15s ease;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #C8456A;
    color: #FFFFFF;
}
div.stButton > button:active {
    transform: scale(0.98);
}

/* Wider buttons and closer spacing */
div[data-testid="stHorizontalBlock"] {
    gap: 0.5rem;
}
div[data-testid="stHorizontalBlock"] button {
    width: 100%;
}

/* Question number color */
.q-num {
    color: #DF577B;
    font-weight: 600;
    margin-right: 0.4rem;
}
...
</style>
''', unsafe_allow_html=True)

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
    st.subheader("Almost done")
    st.write(cfg.CONTACT_INTRO)

    name = st.text_input("Name", key="name", placeholder="Your name")

    phone = st.text_input("Phone", key="phone", placeholder="Your phone number")

    email = st.text_input("Email", key="email", placeholder="you@example.com")

    c1, c2, c3 = st.columns([1, 1, 4])
    with c1:
        if st.button("Back"):
            st.session_state.page -= 1
            st.rerun()
    with c2:
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
