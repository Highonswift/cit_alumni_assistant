import os
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2

def process_file(file_path):
    _, extension = os.path.splitext(file_path)
    if extension.lower() == '.pdf':
        return process_pdf(file_path)
    else:
        raise ValueError("Unsupported file format")

def process_pdf(file_path):
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

def main():
    # Process the PDF file located at 'CIT_Alumni_Selection.pdf'
    content = process_file('CIT_Alumni_Selection.pdf')

    model = genai.GenerativeModel("gemini-1.5-flash")
    user_prompt = input("Enter your prompt: ")
    
    # For PDF, send the text extracted from the PDF along with the user prompt
    response = model.generate_content([user_prompt, content])
    
    print(response.text)

if __name__ == "__main__":
    main()
