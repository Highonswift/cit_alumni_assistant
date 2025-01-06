import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

def process_images(image_path='CIT_Alumni.jpg'):
    # Check if the image file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    
    image = Image.open(image_path)  # Open the image file
    return [image]

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv('API_KEY'))

def main():
    # Process the image file located at 'CIT_Alumni.jpg'
    content = process_images('CIT_Alumni.jpg')

    model = genai.GenerativeModel("gemini-1.5-flash")
    user_prompt = input("Enter your prompt: ")
    
    # For images, send the image along with the user prompt
    response = model.generate_content([user_prompt] + content)
    
    print(response.text)

if __name__ == "__main__":
    main()

