import streamlit as st
import base64
import os

st.set_page_config(layout="wide")

# Function to encode file in base64
def encode_file_to_base64(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode()
    else:
        st.error(f"File not found: {file_path}")
        return None

# Paths to images
logo_path = "imgs/book.png"

# Encode logo to base64
encoded_logo = encode_file_to_base64(logo_path)

# HTML and CSS for layout and content
page_html = f"""
<style>
body {{
  overflow: hidden; /* Remove scrolling for the whole page */
  margin: 0;
  padding: 0;
}}

.content {{
  position: relative;
  z-index: 1;
  padding: 20px; /* Optional: Padding for content */
  color: black; /* Text color set to black */
  overflow-y: hidden; /* Remove scrolling in the content area */
}}

.navbar {{
  display: flex;
  justify-content: space-between; /* Align logo left, links right */
  align-items: center;
  background-color: transparent;
  padding: 10px 20px; /* Add padding for spacing */
  margin-top: 60px; /* Add more margin to move navbar down */
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}}

.navbar .logo {{
  width: 80px; /* Reduced size of the logo */
}}

.navbar div {{
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Align links to the right */
  flex-grow: 1;
  margin-right: 120px; /* Add right margin to bring links left */
}}

.navbar a {{
  margin: 0 10px; /* Adjust spacing between links */
  text-decoration: none;
  color: black; /* Text color of navigation set to black */
  font-weight: bold;
}}

.footer {{
  color: black; /* Text color of footer set to black */
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: transparent;
  text-align: center;
  padding: 10px;
  box-shadow: 0 -4px 2px -2px gray;
  z-index: 1000;
}}

.center-content {{
  display: flex;
  flex-direction: column; /* Align items vertically */
  justify-content: center;
  align-items: center;
  height: calc(100vh - 220px); /* Adjusted for new navbar position */
  color: black; /* Text color set to black */
  text-align: center;
  padding: 20px;
  box-sizing: border-box;
}}

button {{
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 18px;
  color: white;
  background-color: black;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-transform: uppercase;
}}

button:hover {{
  background-color: #333;
}}
</style>
"""

# Insert the HTML/CSS into the Streamlit app
st.markdown(page_html, unsafe_allow_html=True)

# Navigation header as tiles
st.markdown(f"""
    <div class="navbar">
        <img src='data:image/png;base64,{encoded_logo}' class='logo'>
        <div>
            <a href="?page=home" id="link-home">Home</a>
            <a href="?page=ki" id="link-ki">KI</a>
            <a href="?page=quiz" id="link-quiz">Quiz</a>
            <a href="?page=about" id="link-about">Über uns</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Function to display the home page
def show_home():
    st.markdown("""
    <div class="center-content">
        <h1>SAP AI ASSISTANT</h1>
        <button onclick="window.location.href='?page=ki';">Get Started!</button>
    </div>
    """, unsafe_allow_html=True)

# Function to display the "Under Construction" page
def show_under_construction():
    st.markdown("""
    <div class="center-content">
        <h1>Sorry, diese Seite ist momentan noch in Arbeit.</h1>
        <button onclick="window.location.href='?page=home';">Zurück zum Home</button>
    </div>
    """, unsafe_allow_html=True)

# Content of pages based on navigation
query_params = st.query_params
page = query_params.get("page", ["home"])[0]

if page == "home":
    show_home()
elif page == "ki":
    show_under_construction()  # Placeholder for KI page
elif page == "quiz":
    show_under_construction()  # Placeholder for Quiz page
elif page == "about":
    show_under_construction()  # Placeholder for About page

# Footer with contact information and legal links
st.markdown("""
    <div class="footer">
        <p>Kontakt: info@example.com | <a href="#">Impressum</a></p>
    </div>
""", unsafe_allow_html=True)

# JavaScript to support navigation
st.markdown("""
    <script>
        document.getElementById('link-home').onclick = () => {
            window.location.href = window.location.pathname + "?page=home";
        };

        document.getElementById('link-ki').onclick = () => {
            window.location.href = window.location.pathname + "?page=ki";
        };

        document.getElementById('link-quiz').onclick = () => {
            window.location.href = window.location.pathname + "?page=quiz";
        };

        document.getElementById('link-about').onclick = () => {
            window.location.href = window.location.pathname + "?page=about";
        };
    </script>
""", unsafe_allow_html=True)
