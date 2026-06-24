
import requests

# Your Apps Script web app URL (ends in /exec).
# In deployment we'll store this in Streamlit secrets, not hardcoded.
def save_response(webapp_url, circle_name, answers, name, phone, email):
    """Send one respondent's data to the Google Sheet via Apps Script."""

    # answers is a list of varying length (1 to 4).
    # Pad it to 4 so the keys always line up with the sheet columns.
    padded = answers + [""] * (4 - len(answers))

    payload = {
        "circle":  circle_name,
        "answer1": padded[0],
        "answer2": padded[1],
        "answer3": padded[2],
        "answer4": padded[3],
        "name":    name,
        "phone":   phone,
        "email":   email,
    }

    response = requests.post(webapp_url, json=payload)
    return response.ok   # True if it worked
