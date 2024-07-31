import streamlit as st
import openai
import os
import pickle
import faiss
import redis
import numpy as np
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage
from style import get_css, user_avatar, bot_avatar

# Streamlit configuration
st.set_page_config(page_title="Chatbot mit LangChain", page_icon="💬", layout="centered")
st.title("Chatbot 💬")
st.info("Frage mich etwas über die Inhalte der Bücher.", icon="📚")

# API key from OpenAI
openai_api_key = st.secrets.get("openai", {}).get("openai_api_key")
if openai_api_key is None:
    st.error("OPENAI_API_KEY nicht gefunden. Bitte setzen Sie den API-Schlüssel in den Streamlit Secrets.")
    st.stop()

openai.api_key = openai_api_key

# Session initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Frage mich etwas über die Inhalte der Bücher."}
    ]

# Redis configuration (Optional, if needed)
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

# Function to read file with multiple encodings
def read_file_with_encodings(file_path, encodings=["utf-8", "latin-1", "iso-8859-1"]):
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError(f"Cannot read file {file_path} with given encodings.")

# Loading data from local directory
@st.cache_resource(show_spinner=False)
def load_data():
    local_directory = "C:\\Users\\602648\\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\\Bachelor\\books - for code"
    documents = []

    for filename in os.listdir(local_directory):
        if filename.endswith(".txt") or filename.endswith(".pdf"):  # Adjust as needed for your file types
            file_path = os.path.join(local_directory, filename)
            text = read_file_with_encodings(file_path)
            documents.append({"page_content": text})

    if not documents:
        st.error("Keine Dokumente im angegebenen Verzeichnis gefunden.")
        return None, None

    # Splitting documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    split_documents = []
    for doc in documents:
        split_texts = text_splitter.split_text(doc["page_content"])
        split_documents.extend([{"page_content": text} for text in split_texts])

    # Embeddings and FAISS Index creation
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    document_texts = [doc["page_content"] for doc in split_documents]
    document_embeddings = [embeddings.embed_query(text) for text in document_texts]

    dimension = len(document_embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(document_embeddings))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=None,  # Add appropriate docstore here
        index_to_docstore_id={i: i for i in range(len(split_documents))}
    )
    
    return vector_store, split_documents

vector_store, documents = load_data()
if vector_store is None or documents is None:
    st.stop()

# Additional check
if vector_store.index_to_docstore_id is None:
    st.error("index_to_docstore_id is not initialized correctly.")
    st.stop()

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

# Initialize memory tool
memory = ConversationBufferMemory()

# Define system prompt
system_prompt = """
You are an SAP consultant with over 15 years of experience and an expert in your field. 
You are very knowledgeable about SAP Activate and the related books. 
You are friendly and helpful. Answer technical questions based on the contents of the books provided, 
and feel free to engage in small talk as well.
"""

# Create prompt template
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    HumanMessage(content="{context}\n\n{question}")
])

# Create retriever
retriever = vector_store.as_retriever()

# Define retrieval chain creation function
def create_retrieval_chain(query):
    try:
        retrieved_docs = retriever.get_relevant_documents(query)
        if not retrieved_docs:
            st.error("No documents found for the given query.")
            return {"text": "Sorry, I couldn't find any relevant documents."}
        
        # Ensure that each retrieved document has the attribute 'page_content'
        context = "\n\n".join([doc["page_content"] for doc in retrieved_docs])
        
        # Format messages using the context and query
        formatted_messages = prompt_template.format_messages(context=context, question=query)
        
        # Ensure formatted_messages is a list of BaseMessage
        if not isinstance(formatted_messages, list):
            raise ValueError("Formatted messages should be a list of BaseMessage objects")
        
        # Get response from the language model
        response = llm(formatted_messages)
        return response
    except Exception as e:
        st.error(f"Error in create_retrieval_chain: {e}")
        return {"text": "An error occurred while processing your request."}

# Initialize chat engine
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = create_retrieval_chain

# User query
if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add assistant response
    response = st.session_state.chat_engine(prompt)
    if response and hasattr(response, "choices") and response.choices:
        response_content = response.choices[0].text
    else:
        response_content = "An error occurred while processing your request."
    st.session_state.messages.append({"role": "assistant", "content": response_content})

# Display messages
for message in st.session_state.messages:
    avatar = user_avatar if message["role"] == "user" else bot_avatar
    alignment = "flex-end" if message["role"] == "user" else "flex-start"
    background_color = "#ADD8E6" if message["role"] == "user" else "#f1f1f1"
    text_color = "black"
    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-start; justify-content: {alignment}; margin-bottom: 10px;">
            <img src="{avatar}" width="40" style="border-radius: 50%; margin-right: 10px;">
            <div style="background: {background_color}; color: {text_color}; padding: 10px; border-radius: 10px; max-width: 70%;">
                {message["content"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
