import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import streamlit as st

# Function to process static images
def process_images(image_path='CIT_Alumni.jpg'):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    image = Image.open(image_path)
    return [image]

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv('API_KEY'))

# Streamlit setup
st.set_page_config(page_title="CIT Alumni ECM Assistant", page_icon="🎓", layout="wide")
st.title("CIT Alumni ECM Assistant")
st.markdown("Ask me anything about CIT Alumni ECM!")

# Define a session state to track chat history
if 'messages' not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you with CIT Alumni information today?"}
    ]

# Function to generate bot response
def get_bot_response(user_input):
    # Process the static image
    content = process_images('CIT_Alumni.jpg')  # Use the static image
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([user_input] + content)
    return response.text

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle User Input
if user_input := st.chat_input("Type your question here..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get bot response and add to history
    bot_response = get_bot_response(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)
