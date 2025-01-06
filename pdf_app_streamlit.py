import os
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
import streamlit as st

# Function to process PDF files and extract text
def process_pdf(file_path='CIT_Alumni_Selection.pdf'):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv('API_KEY'))

# Streamlit setup
st.set_page_config(page_title="CIT Alumni Assistant", page_icon="🎓", layout="wide")
st.title("CIT Alumni Assistant")
st.markdown("Ask me anything about CIT Alumni! Here's some context from the CIT Alumni Selection PDF.")

# Display instructions in the sidebar
st.sidebar.header("Instructions")
st.sidebar.write(
    """
    The CIT Alumni Assistant is ready to assist you. Below is the information extracted from the CIT Alumni Selection PDF. 
    Ask your questions based on the content of the document.
    """
)

# Define a session state to track chat history
if 'messages' not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you with CIT Alumni information today?"}
    ]

# Static PDF path for the CIT Alumni Selection document
pdf_path = 'CIT_Alumni_Selection.pdf'

# Process the PDF content
if os.path.exists(pdf_path):
    content = process_pdf(pdf_path)
else:
    content = "PDF file not found."

# Function to generate bot response
def get_bot_response(user_input, content):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([user_input, content])
    return response.text

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle User Input
if user_input := st.chat_input("Type your question here..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get bot response and add to history
    bot_response = get_bot_response(user_input, content)
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)
