import streamlit as st
from openai import OpenAI
import base64

# Funktion zum Laden eines Bildes und Umwandeln in Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Lade die Bilder und konvertiere sie in Base64
user_avatar = get_base64_image("imgs/cat.jpg")
bot_avatar = get_base64_image("imgs/stuser.png")  # Ersetze durch den Pfad deines Bot-Bildes

# Show title and description.
st.title("Chatbot 💬")
st.write("bla bla")

# Retrieve the OpenAI API key from secrets.toml
openai_api_key = st.secrets.get("openai", {}).get("openai_api_key")
if not openai_api_key:
    st.warning("OpenAI API key not found in secrets.toml. Please add it to continue.", icon="🗝️")

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Style adjustments for layout
st.markdown(f"""
<style>
.chat-container {{
    display: flex;
    flex-direction: column-reverse;
    height: calc(100vh - 100px); /* Adjust height to make space for input field */
    overflow-y: auto;
}}
.chat-input-container {{
    display: flex;
    align-items: center;
    position: fixed;
    bottom: 0;
    width: 100%;
    background: white;
    border-top: 1px solid #ddd;
    padding: 10px;
    box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
}}
.chat-input {{
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 10px;
    margin-right: 10px;
}}
.chat-input button {{
    background: #007BFF;
    border: none;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    font-size: 18px;
    padding: 10px;
    margin-left: 5px;
}}
.chat-message {{
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
}}
.chat-message-user {{
    display: flex;
    justify-content: flex-end;  /* Nachricht nach rechts verschieben */
    align-items: flex-start;
    margin-bottom: 10px;
}}
.chat-message-bot {{
    display: flex;
    justify-content: flex-start;  /* Nachricht nach links verschieben */
    align-items: flex-start;
    margin-bottom: 10px;
}}
.chat-message-avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
}}
.chat-message-content {{
    background: #f1f1f1;
    padding: 10px;
    border-radius: 10px;
    max-width: 70%;
}}
.chat-message-content-user {{
    background: #007BFF;
    color: white;
    border-bottom-right-radius: 0;
}}
.chat-message-content-bot {{
    background: #f1f1f1;
    border-bottom-left-radius: 0;
}}
.chat-message-avatar-user {{
    margin-left: 10px;  /* Abstand zwischen Text und Avatar beim Benutzer */
}}
.chat-message-avatar-bot {{
    margin-right: 10px;  /* Abstand zwischen Avatar und Text beim Bot */
}}
</style>
""", unsafe_allow_html=True)

# Create chat container for messages
chat_container = st.container()

# Display the existing chat messages
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            avatar = user_avatar
            class_name = "chat-message chat-message-user"
            content_class_name = "chat-message-content chat-message-content-user"
            avatar_class_name = "chat-message-avatar chat-message-avatar-user"
        else:
            avatar = bot_avatar
            class_name = "chat-message chat-message-bot"
            content_class_name = "chat-message-content chat-message-content-bot"
            avatar_class_name = "chat-message-avatar chat-message-avatar-bot"

        st.markdown(f"""
        <div class="{class_name}">
            <div class="{content_class_name}">{message['content']}</div>
            <img src="data:image/png;base64,{avatar}" class="{avatar_class_name}">
        </div>
        """, unsafe_allow_html=True)

# Function to send the message
def send_message():
    prompt = st.session_state.chat_input
    if prompt:
        # Store and display the current prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(f"""
            <div class="chat-message chat-message-user">
                <div class="chat-message-content chat-message-content-user">{prompt}</div>
                <img src="data:image/png;base64,{user_avatar}" class="chat-message-avatar chat-message-avatar-user">
            </div>
            """, unsafe_allow_html=True)

        if openai_api_key:
            # Generate a response using the OpenAI API
            client = OpenAI(api_key=openai_api_key)
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # Stream the response to the chat using `st.write_stream`, then store it in session state
            with chat_container:
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            # Default response if API key is not found
            default_response = "Bitte füge dein API key in die Datei secrets.toml hinzu."
            with chat_container:
                st.markdown(f"""
                <div class="chat-message chat-message-bot">
                    <div class="chat-message-content chat-message-content-bot">{default_response}</div>
                    <img src="data:image/png;base64,{bot_avatar}" class="chat-message-avatar chat-message-avatar-bot">
                </div>
                """, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": default_response})

        st.session_state.chat_input = ""  # Clear the input field after sending

# Create chat input field with send button
chat_input_container = st.container()
with chat_input_container:
    input_col1, input_col2 = st.columns([10, 1])
    with input_col1:
        st.text_input("", key="chat_input", placeholder="Type your message here...", max_chars=500, help="Enter your message here", on_change=send_message)
    with input_col2:
        if st.button("➤", key="send_button"):
            send_message()

# Ensure the chat input field is focused on load
st.markdown("<script>document.getElementById('chat_input').focus();</script>", unsafe_allow_html=True)
