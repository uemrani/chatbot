import streamlit as st
#from chatbot import chatbot_page  # Importiere die Chatbot-Seite aus der chatbot.py
from test.chatbot_api import chatbot_page
# set_page_config nur einmal hier aufrufen

st.set_page_config(layout="wide")

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Chatbot", "Quiz"])

    if selection == "Home":
        home()
    elif selection == "Chatbot":
        chatbot_page()  # Verweise auf die Funktion in der chatbot.py
    elif selection == "Quiz":
        quiz()

def home():
    st.title("Home Page")
    st.write("Welcome to the homepage! Here you'll find all the information you need about our app.")

def quiz():
    st.title("Quiz")
    st.write("This is the Quiz page. Here you can take a quiz.")

    question = "What is the capital of France?"
    options = ["Berlin", "London", "Paris", "Rome"]
    answer = "Paris"

    st.write(question)
    user_answer = st.radio("Select an answer:", options)
    
    if st.button("Submit"):
        if user_answer == answer:
            st.success("Correct!")
        else:
            st.error("Incorrect!")

if __name__ == "__main__":
    main()
