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

st.set_page_config(page_title=cfg.CIRCLE_NAME, page_icon="\U0001F338")

# ------------------------------------------------------------
# BRAND STYLING
# Palette: Ivory #FAF7F2 / Charcoal #2E2A2B / Watermelon #DF577B / Stone #D8D1C8
# Fonts:  Fraunces (headings) + Nunito Sans (body)
# ------------------------------------------------------------
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Nunito+Sans:wght@400;600;700&display=swap');

.stApp { background-color: #FAF7F2; }
html, body, [class*="css"] { font-family: 'Nunito Sans', sans-serif; color: #2E2A2B; }
h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #2E2A2B !important; font-weight: 500; }

/* Center the logo */
div[data-testid="stImage"] { display: flex; justify-content: center; }
div[data-testid="stImage"] img { margin: 0 auto; }

/* Numbered question line */
.q-line { font-family: 'Fraunces', serif; font-size: 1.5rem; color: #2E2A2B; line-height: 1.3; margin: 0.5rem 0 0.25rem; }
.q-num  { color: #DF577B; font-weight: 600; margin-right: 0.4rem; }
.q-help { font-family: 'Nunito Sans', sans-serif; font-size: 0.92rem; color: #8A7F82; line-height: 1.5; margin: 0 0 0.5rem; }

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
    width: 100%;
}
div.stButton > button:hover { background-color: #C8456A; color: #FFFFFF; }
div.stButton > button:active { transform: scale(0.98); }

/* Tighten the gap between the Back/Next columns */
div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }

/* Hide Streamlit default chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
''', unsafe_allow_html=True)

# ------------------------------------------------------------
# A small list of country dialing codes for the phone field.
# ------------------------------------------------------------
COUNTRY_CODES = [
    "+57 Colombia", "+58 Venezuela", "+1 USA/Canada", "+52 Mexico",
    "+54 Argentina", "+56 Chile", "+51 Peru", "+593 Ecuador",
    "+34 Spain", "+44 UK", "+55 Brazil", "+507 Panama",
    "+506 Costa Rica", "+502 Guatemala", "+503 El Salvador",
    "+591 Bolivia", "+598 Uruguay", "+595 Paraguay", "+809 Dominican Rep.",
    "Other",
]

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
    st.session_state.answers = [""] * len(cfg.QUESTIONS)

# Banner (skipped gracefully if missing)
if os.path.exists(cfg.LOGO_FILE):
    st.image(cfg.LOGO_FILE, use_container_width=True)

total_pages = len(cfg.QUESTIONS)

# ------------------------------------------------------------
# PAGES 1..N: one question each (numbered, with optional helper)
# ------------------------------------------------------------
elif 1 <= st.session_state.page <= total_pages:
    i = st.session_state.page - 1
    question = cfg.QUESTIONS[i]

    # Numbered question line (number in watermelon)
    st.markdown(
        f'<p class="q-line"><span class="q-num">{st.session_state.page}.</span>{question["q"]}</p>',
        unsafe_allow_html=True,
    )
    # Optional smaller helper text
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

    # Back/Next sit in narrow columns near each other (not full width)
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

    # Phone: country code selector + number box, side by side
    st.markdown('<p style="margin-bottom:0.2rem;">Phone</p>', unsafe_allow_html=True)
    pcol1, pcol2 = st.columns([2, 3])
    with pcol1:
        country = st.selectbox("Country code", COUNTRY_CODES, label_visibility="collapsed")
    with pcol2:
        phone_number = st.text_input(
            "Phone number", key="phone_num",
            label_visibility="collapsed", placeholder="Phone number",
        )
    # Combine code + number; keep just the dialing code part (e.g. "+57")
    dial = country.split(" ")[0] if country != "Other" else ""
    phone = f"{dial} {phone_number}".strip()

    email = st.text_input("Email", key="email", placeholder="you@example.com")

    if st.session_state.page > 1:
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
