import streamlit as st
from database import connect, get_all_books, get_book_content_from_db
from integration import chat_with_openai
from style import get_css, user_avatar, bot_avatar  # Importiere die benötigten Variablen und Funktionen

st.markdown(get_css(), unsafe_allow_html=True)

st.title("Chatbot 💬")
st.write("bla bla")

openai_api_key = st.secrets.get("openai", {}).get("openai_api_key")
if not openai_api_key:
    st.warning("OpenAI API key not found in secrets.toml. Please add it to continue.", icon="🗝️")

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

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

def is_question_about_books(prompt):
    keywords = ["book", "books", "content", "information", "detail", "details", "chapter", "chapters", "author", "title", "summary", "summaries"]
    return any(keyword in prompt.lower() for keyword in keywords)

def send_message():
    prompt = st.session_state.chat_input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(f"""
            <div class="chat-message chat-message-user">
                <div class="chat-message-content chat-message-content-user">{prompt}</div>
                <img src="data:image/png;base64,{user_avatar}" class="chat-message-avatar chat-message-avatar-user">
            </div>
            """, unsafe_allow_html=True)

        response = ""
        if openai_api_key:
            if is_question_about_books(prompt):
                conn = connect()
                if conn:
                    all_books = get_all_books(conn)
                    book_contents = [get_book_content_from_db(conn, book) for book in all_books]
                    conn.close()

                    book_content_summary = "\n\n".join([f"Inhalt von {book}:\n{content}" for book, content in zip(all_books, book_contents)])
                    messages = st.session_state.messages.copy()
                    messages.append({"role": "system", "content": f"Hier sind die Inhalte der Bücher:\n{book_content_summary}"})
                    response = chat_with_openai(openai_api_key, messages)
                else:
                    response = "Fehler bei der Verbindung zur Datenbank."
            else:
                response = chat_with_openai(openai_api_key, st.session_state.messages)
        else:
            response = "Bitte füge dein API key in die Datei secrets.toml hinzu."

        st.session_state.messages.append({"role": "assistant", "content": response})
        with chat_container:
            st.markdown(f"""
            <div class="chat-message chat-message-bot">
                <div class="chat-message-content chat-message-content-bot">{response}</div>
                <img src="data:image/png;base64,{bot_avatar}" class="chat-message-avatar chat-message-avatar-bot">
            </div>
            """, unsafe_allow_html=True)

        st.session_state.chat_input = ""  # Clear the input field after sending

chat_input_container = st.container()
with chat_input_container:
    input_col1, input_col2 = st.columns([10, 1])
    with input_col1:
        st.text_input("Chat Input", key="chat_input", placeholder="Type your message here...", max_chars=500, help="Enter your message here", on_change=send_message, label_visibility="collapsed")
    with input_col2:
        if st.button("➤", key="send_button"):
            send_message()

st.markdown("<script>document.getElementById('chat_input').focus();</script>", unsafe_allow_html=True)
