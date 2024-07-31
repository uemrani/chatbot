import streamlit as st
import openai
import os
import pickle
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from style import get_css, user_avatar, bot_avatar

st.set_page_config(
    page_title="Chatbot mit LlamaIndex",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="auto"
)
openai.api_key = st.secrets.get("openai", {}).get("openai_api_key")
st.title("Chatbot 💬")
st.info("Frage mich etwas über die Inhalte der Bücher.", icon="📚")
st.markdown(get_css(), unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Frage mich etwas über die Inhalte der Bücher."}]

@st.cache_resource(show_spinner=False)
def load_data():
    index_path = "index.pkl"
    input_dir = r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code"

    if os.path.exists(index_path):
        with open(index_path, "rb") as f:
            index = pickle.load(f)
    else:
        # PDF-Dokumente laden und in Texte konvertieren
        reader = SimpleDirectoryReader(input_dir=input_dir, recursive=True, file_types=['pdf'])
        docs = reader.load_data()

        Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2,
            system_prompt=(
                "You are an SAP consultant with over 15 years of experience. You are very knowledgeable "
                "about SAP Activate and the related books. Answer technical questions based on the contents "
                "of the books provided. Keep your responses concise and always include the source file name "
                "and page number for reference. Format the source as: (Source: [Book Name], Page [Page Number])."
            ),
        )

        index = VectorStoreIndex.from_documents(docs)
        with open(index_path, "wb") as f:
            pickle.dump(index, f)
    return index

index = load_data()

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    avatar = user_avatar if message["role"] == "user" else bot_avatar
    alignment = "flex-end" if message["role"] == "user" else "flex-start"
    background_color = "#ADD8E6" if message["role"] == "user" else "#f1f1f1"
    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-start; justify-content: {alignment}; margin-bottom: 10px;">
            <img src="data:image/jpeg;base64,{avatar}" width="40" style="border-radius: 50%; margin-right: 10px;">
            <div style="background: {background_color}; color: black; padding: 10px; border-radius: 10px; max-width: 70%;">
                {message["content"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if st.session_state.messages[-1]["role"] != "assistant":
    response_stream = st.session_state.chat_engine.stream_chat(st.session_state.messages[-1]["content"])
    response_content = ''.join(chunk for chunk in response_stream.response_gen)
    st.session_state.messages.append({"role": "assistant", "content": response_content})

    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 10px;">
            <img src="data:image/jpeg;base64,{bot_avatar}" width="40" style="border-radius: 50%; margin-right: 10px;">
            <div style="background: #f1f1f1; color: black; padding: 10px; border-radius: 10px; max-width: 70%;">
                {response_content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
