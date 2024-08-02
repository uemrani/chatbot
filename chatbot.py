import streamlit as st
import openai
import os
import pickle
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from styles.style import get_css, user_avatar, bot_avatar

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

# PDF-Pfade zu den einzelnen Dokumenten
pdf_paths = [
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\ACT100.23.EN-US.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\ACT200.23.EN-US.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP1.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP2.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP3.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP4.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP5.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP6.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP7.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERP8.pdf",
    r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\Result_ERPPREP_TS_2024_05_17.pdf"
]

@st.cache_resource(show_spinner=False)
def load_data():
    index_path = "index.pkl"
    reader = SimpleDirectoryReader(input_files=pdf_paths)
    docs = reader.load_data()

    if os.path.exists(index_path):
        with open(index_path, "rb") as f:
            index = pickle.load(f)
    else:
        Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            system_prompt=(
                "You are an SAP consultant with over 15 years of experience and specialize in accessing and analyzing "
                "SAP Activate certification data, question catalogs, and related eBooks to answer user queries efficiently "
                "and accurately. You provide short, data-driven responses based on the information retrieved from SAP Activate "
                "certification PDFs, eBooks, and question catalogs. Clarify any ambiguous requests to ensure precise answers. "
                "Maintain focus on delivering clear and concise information from the SAP Activate certification data. "
                "All responses must include the page number and the book or document from which the information is sourced so that "
                "users can verify in their own books or documents. The primary sources of information are the uploaded eBooks: "
                "ACT200.23.EN-US.pdf, ACT100.23.EN-US.pdf, and the question catalogs Result_ERPPREP_TS_2024_05_17.pdf, Result_ERP1.pdf, "
                "Result_ERP2.pdf, Result_ERP3.pdf, Result_ERP4.pdf, Result_ERP5.pdf, Result_ERP6.pdf, Result_ERP7.pdf, and Result_ERP8.pdf."
            ),
        )

        index = VectorStoreIndex.from_documents(docs)
        with open(index_path, "wb") as f:
            pickle.dump(index, f)
    return index, docs

def display_sample_docs(docs, num_samples=5):
    for i, doc in enumerate(docs[:num_samples]):
        st.write(f"### Dokument {i + 1}")
        st.write(f"**Pfad:** {pdf_paths[i]}")
        st.write(f"**Inhalt (Auszug):** {doc.text[:500]}...")  # Zeige die ersten 500 Zeichen des Dokuments an
        st.write("---")

index, documents = load_data()

if st.button("Zeige Beispiel-Dokumente"):
    display_sample_docs(documents)
else:
    st.write("Klicke auf den Button, um einige Beispiel-Dokumente anzuzeigen.")

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response_stream = st.session_state.chat_engine.stream_chat(prompt)
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

    if hasattr(response_stream, 'source_documents'):
        st.write("### Quellenangaben:")
        for doc in response_stream.source_documents:
            st.write(f"**Dokument:** {doc.title}")
            st.write(f"**Seite:** {doc.page_number}")
            st.write(f"**Auszug:** {doc.text[:200]}...")
            st.write("---")

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