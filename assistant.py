import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import PyPDF2

def process_images(image_path='CIT_Alumni.jpg'):
    # Check if the image file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    
    image = Image.open(image_path)  # Open the image file
    return [image]

def process_file(file_path):
    _, extension = os.path.splitext(file_path)
    if extension.lower() == '.pdf':
        return process_pdf(file_path)
    else:
        return process_text(file_path)

def process_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

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
    file_type = input("Enter file type (image/file): ").lower()

    if file_type == "image":
        # Process the image file located at 'CIT_Alumni.jpg'
        content = process_images('CIT_Alumni.jpg')
    elif file_type == "file":
        # Process the PDF file located at 'CIT_Alumni_Selection.pdf'
        content = process_file('CIT_Alumni_Selection.pdf')
    else:
        raise ValueError("Invalid file type. Please choose 'image' or 'file'.")

    model = genai.GenerativeModel("gemini-1.5-flash")
    user_prompt = input("Enter your prompt: ")
    
    if file_type == "image":
        # For images, send the image along with the user prompt
        response = model.generate_content([user_prompt] + content)
    else:
        # For PDF, send the text extracted from the PDF along with the user prompt
        response = model.generate_content([user_prompt, content])
    
    print(response.text)

if __name__ == "__main__":
    main()
