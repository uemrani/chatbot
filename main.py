import streamlit as st
from scripts import chatbot  # Beispiel für Import

def main():
    st.title("Hauptseite")
    st.write("Willkommen! Wählen Sie eine Option:")
    
    if st.button('Chatbot starten'):
        chatbot.run()  # Eine Funktion in chatbot.py, die den Chatbot startet

if __name__ == "__main__":
    main()
