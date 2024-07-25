import streamlit as st
from streamlit_chat import message
import base64

def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        encoded_string = base64.b64encode(video_file.read()).decode()
        return encoded_string

# Pfad zu deinem lokalen Video
video_path = "imgs/hintergrund.mp4"
base64_video = video_to_base64(video_path)

st.set_page_config(layout="wide")

# HTML und CSS für das Hintergrundvideo
video_html = f"""
<style>
#myVideo {{
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%; 
  min-height: 100%;
  z-index: -1;
}}

.content {{
  position: relative;
  z-index: 1;
}}
</style>
<video autoplay muted loop id="myVideo">
  <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
  Your browser does not support HTML5 video.
</video>
"""

# Einfügen des HTML/CSS in die Streamlit-App
st.markdown(video_html, unsafe_allow_html=True)

# Rest der Streamlit-App
st.title("Chatbot 💬")
st.markdown("Dieser Text wird über dem Hintergrundvideo angezeigt! 😁")

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
        'content': "Das ist eine Antwort auf: " + prompt
    })

    # Nachrichten aktualisieren
    st.experimental_rerun()
