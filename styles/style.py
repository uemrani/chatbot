import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

user_avatar = image_to_base64("imgs/cat.jpg")
bot_avatar = image_to_base64("imgs/ai.png")
background_image_path = "imgs/background1.png"
base64_background_image = image_to_base64(background_image_path)

background_image = f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{base64_background_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    margin: 0;
}}
</style>
"""

chat_css = f"""
<style>
/* General text color */
body, .css-1v3fvcr, .css-1m8ydn5 {{
    color: black !important;
}}

/* Title style */
h1, h2, h3, h4, h5, h6 {{
    color: black !important;
}}

/* Input field container style */
.chat-input-container {{
    display: flex;
    align-items: center;
    position: fixed;
    bottom: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0); /* Transparent background */
    border-top: 1px solid #ddd;
    padding: 10px;
    box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
    z-index: 10;
}}

/* Input field style */
.chat-input {{
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 10px;
    margin-right: 10px;
    background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent background */
}}

/* Send button style */
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

/* Chat container style */
.chat-container {{
    display: flex;
    flex-direction: column-reverse;
    height: calc(100vh - 90px);
    overflow-y: auto;
    padding: 10px;
    box-sizing: border-box;
}}

/* Custom style for chat messages */
.chat-message {{
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
}}

.chat-message-user {{
    display: flex;
    justify-content: flex-end;
}}

.chat-message-bot {{
    display: flex;
    justify-content: flex-start;
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
    background: #ADD8E6;
    color: black;
    border-bottom-right-radius: 0;
}}

.chat-message-content-bot {{
    background: #f1f1f1;
    border-bottom-left-radius: 0;
}}

.chat-message-avatar-user {{
    margin-left: 10px;
}}

.chat-message-avatar-bot {{
    margin-right: 10px;
}}
</style>
"""

def get_css():
    return background_image + chat_css
