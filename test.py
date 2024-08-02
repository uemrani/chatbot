import streamlit as st
import openai
import os
import pickle
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, Settings

st.set_page_config(
    page_title="Chatbot mit LlamaIndex",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Datenvalidierung für Chatbot 💬")
st.info("Überprüfe, ob die Dokumente korrekt geladen wurden.", icon="📚")

# API-Schlüssel einstellen
openai.api_key = st.secrets.get("openai", {}).get("openai_api_key")

# Pfade zu den einzelnen PDF-Dokumenten
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

# Funktion zum Laden der Dokumente
@st.cache_resource(show_spinner=False)
def load_documents(paths):
    reader = SimpleDirectoryReader(input_files=paths)
    docs = reader.load_data()
    return docs

# Dokumente laden
documents = load_documents(pdf_paths)

# Funktion zum Anzeigen von Beispiel-Dokumenten
def display_sample_docs(docs, num_samples=5):
    for i, doc in enumerate(docs[:num_samples]):
        st.write(f"### Dokument {i + 1}")
        st.write(f"**Pfad:** {pdf_paths[i]}")
        st.write(f"**Inhalt (Auszug):** {doc.text[:500]}...")  # Zeige die ersten 500 Zeichen des Dokuments an
        st.write("---")

# Anzahl der geladenen Dokumente anzeigen
st.write(f"Anzahl der geladenen Dokumente: {len(documents)}")

# Dokumente stichprobenartig anzeigen
if st.button("Zeige Beispiel-Dokumente"):
    display_sample_docs(documents, num_samples=5)
else:
    st.write("Klicke auf den Button, um einige Beispiel-Dokumente anzuzeigen.")
