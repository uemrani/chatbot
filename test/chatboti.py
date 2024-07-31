import streamlit as st
from streamlit_chat import message
import base64

def chatbot_page():
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return encoded_string

    # Pfad zu deinem lokalen Bild für den Hintergrund
    background_image_path = "imgs/background1.png"  # Pfad zu deinem Hintergrundbild
    base64_background_image = image_to_base64(background_image_path)

    # Set the background image using Base64 encoding
    background_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }}
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

    # Optional: Customize the appearance of the title, text input, and all texts
    style = f"""
    <style>
    /* General text color */
    body, .css-1v3fvcr, .css-1m8ydn5 {{
        color: black !important;
    }}

    /* Title style */
    h1, h2, h3, h4, h5, h6 {{
        color: black !important;
    }}

    /* Input field style */
    input[type="text"] {{
        background-color: transparent;
    }}
    div[data-baseweb="base-input"] {{
        background-color: transparent !important;
    }}

    /* Markdown content style */
    div[data-testid="stMarkdownContainer"] {{
        color: black !important;
    }}

    /* Ensure transparency for the entire app container */
    [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}

    /* Ensure transparency for the main container */
    [data-testid="stBlock"] {{
        background: transparent !important;
    }}

    /* Ensure transparency for the vertical blocks */
    [data-testid="stVerticalBlock"] {{
        background: transparent !important;
    }}

    /* Custom style for chat messages */
    [data-testid="stChatMessage"] {{
        background: transparent !important; /* Fully transparent background */
        border: none !important; /* Remove the border */
        padding: 0 !important; /* Remove padding */
        color: black !important; /* Text color for better visibility */
    }}

    /* Make the bottom input field transparent */
    [data-testid="stBottom"] > div {{
        background: transparent !important; /* Fully transparent background */
    }}

    /* Remove avatar images */
    [data-testid="stChatMessage"] .user::before,
    [data-testid="stChatMessage"] .assistant::after {{
        content: none !important; /* Remove any existing content or image */
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    # Rest der Streamlit-App
    st.title("Chatbot 💬")
    st.markdown("Dieser Text wird über dem Hintergrundbild angezeigt! 😁")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Anzeige der Nachrichten
    for idx, msg in enumerate(st.session_state['messages']):
        message(
            msg['content'], 
            is_user=(msg['role'] == 'user'), 
            key=f"{msg['role']}_{idx}"  # Eindeutiger Schlüssel für jede Nachricht
        )

    # Chat-Eingabefeld, das automatisch unten angezeigt wird
    if prompt := st.chat_input("Schreibe eine Nachricht:"):
        st.session_state['messages'].append({
            'role': 'user',
            'content': prompt
        })
        # Hier könntest du deine Chatbot-Antwort hinzufügen
        st.session_state['messages'].append({
            'role': 'bot',
            'content': "Lass mich in Ruhe"
        })

        # Nachrichten aktualisieren
        st.experimental_rerun()