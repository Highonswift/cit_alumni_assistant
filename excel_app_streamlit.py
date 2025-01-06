import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import streamlit as st

# Function to process specific sheets from an Excel file
def process_excel(file_path='cit_alumni_master.xlsx'):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    try:
        # Read the specific sheets
        # sheet_names = ["LTM Nos", "Batchwise Alphabetically"]
        sheet_names = ["Yearwise Alphabetically"]
        excel_data = pd.read_excel(file_path, sheet_name=sheet_names, engine='openpyxl')
        text = ""
        for sheet_name, sheet_data in excel_data.items():
            text += f"\n\nSheet: {sheet_name}\n"
            text += sheet_data.to_string(index=False)
        return text
    except Exception as e:
        return f"Error processing Excel file: {str(e)}"

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv('API_KEY'))

# Streamlit setup
st.set_page_config(page_title="CIT Alumni Assistant", page_icon="📊", layout="wide")
st.title("CIT Alumni Assistant")
st.markdown("Ask me anything about CIT Alumni!")


# Define a session state to track chat history
if 'messages' not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you with CIT Alumni information today?"}
    ]

# Static Excel path for the CIT Alumni Selection document
excel_path = 'cit_alumni_master.xlsx'

# Process the Excel content
if os.path.exists(excel_path):
    content = process_excel(excel_path)
else:
    content = "Excel file not found."

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
