import streamlit as st
import os
import base64

st.set_page_config(layout="wide")

# Initialize session state to track video playback status
if "video_played" not in st.session_state:
    st.session_state.video_played = False

# Function to encode file in base64
def encode_file_to_base64(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode()
    else:
        st.error(f"File not found: {file_path}")
        return None

# Paths to video and images
video_path = "imgs/video.mp4"
screenshot_path = "imgs/video.png"
logo_path = "imgs/book.png"

# Encode files to base64
encoded_video = encode_file_to_base64(video_path)
encoded_img = encode_file_to_base64(screenshot_path)
encoded_logo = encode_file_to_base64(logo_path)

# HTML and CSS for video background and content
video_html = f"""
<style>
body {{
  overflow: hidden; /* Remove scrolling for the whole page */
  margin: 0;
  padding: 0;
}}

#myVideo {{
  display: none; /* Initially hidden */
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: -1;
  background-color: black; /* Fallback color */
}}

#myImage {{
  display: none; /* Initially hidden */
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: -1;
  background-color: black; /* Fallback color */
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
  cursor: pointer; /* Change cursor to pointer for clickable links */
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
<video id="myVideo">
  <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
  Your browser does not support HTML5 video.
</video>
<img id="myImage" src="data:image/png;base64,{encoded_img}" alt="End Image">
<script>
window.onload = function() {{
  if ({str(st.session_state.video_played).lower()}) {{
    document.getElementById('myVideo').style.display = 'block';
    document.getElementById('myVideo').play();
  }}
  document.getElementById('myVideo').onended = function() {{
    document.getElementById('myVideo').style.display = 'none';
    document.getElementById('myImage').style.display = 'block';
  }};
}};
</script>
"""

# Insert the HTML/CSS into the Streamlit app
st.markdown(video_html, unsafe_allow_html=True)

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

# Function to display the KI page
def show_ki():
    st.markdown("""
    <div class="center-content">
        <h1>KI</h1>
        <p>Hier können Sie mit unserer KI interagieren. Geben Sie Ihre Anfragen ein und erhalten Sie die gewünschten Informationen.</p>
        <input type="text" style="width: 80%; padding: 10px; font-size: 16px;" placeholder="Geben Sie Ihre Anfrage ein:">
    </div>
    """, unsafe_allow_html=True)

# Function to display the About page
def show_about():
    st.markdown("""
    <div class="center-content">
        <h1>Über uns</h1>
        <p>Wir sind ein engagiertes Team, das sich darauf spezialisiert hat, Ihnen die besten KI-gestützten Lösungen anzubieten.
        Unsere Mission ist es, Ihnen zu helfen, das Beste aus den SAP Zertifikatsbüchern herauszuholen.</p>
        <p>Unsere KI ist eine leistungsstarke Lösung, die auf den Inhalten von SAP Zertifikatsbüchern basiert.
        Momentan umfasst sie den Fragekatalog und SAP Activate Bücher. Weitere Inhalte folgen bald.</p>
        <p>Nutzen Sie unsere KI, um tiefer in die Inhalte der SAP Zertifikatsbücher einzutauchen und Ihr Wissen zu erweitern.
        Kontaktieren Sie uns gerne für weitere Informationen oder Unterstützung.</p>
    </div>
    """, unsafe_allow_html=True)

# Content of pages based on navigation
query_params = st.query_params
page = query_params.get("page", ["home"])[0]

if page == "home":
    st.session_state.video_played = True
    show_home()
elif page == "ki":
    show_ki()
elif page == "about":
    show_about()
elif page == "quiz":
    # Navigate to quiz page by rerunning the app with quiz.py
    st.experimental_rerun()  # This will be used to redirect to quiz.py


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

# Footer with contact information and legal links
st.markdown("""
    <div class="footer">
        <p>Kontakt: info@example.com | <a href="#">Impressum</a></p>
    </div>
""", unsafe_allow_html=True)
