import streamlit as st
from PIL import Image
import easyocr
import pyttsx3
import os
import google.generativeai as genai

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = 'AIzaSyBTUCKap7B6jgX_ZAIckTaRBVlSPYa2z18'  # Replace with your valid API key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Streamlit Page Configuration
st.set_page_config(page_title="Pixscribe App", layout="wide", page_icon="📸")

# CSS Style
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f7fa;
    }
    .main-title {
        font-size: 50px;
        font-weight: 800;
        color: #303952;
        text-align: center;
        margin: 10px 0 20px;
    }
    .subtitle {
        font-size: 18px;
        color: #57606f;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-header {
        font-size: 22px;
        color: #2f3542;
        font-weight: bold;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    footer {
        text-align: center;
        color: #57606f;
        font-size: 14px;
    }
    .stButton>button {
        background: linear-gradient(to right, #6a89cc, #82ccdd);
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #4a69bd, #60a3bc);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    ### 📌 Features
    - 🔍 Describe Scene: Get AI insights about the image, including objects and suggestions.
    - 📝 Extract Text: Extract visible text using OCR.
    - 🔊 Text-to-Speech: Hear the extracted text aloud.
    - 💡 How it helps: Assists visually impaired users by providing scene descriptions, text extraction, and speech.

    ### 🤖 Powered by:
    - Google Gemini API for scene understanding.
    - EasyOCR for text extraction.
    - pyttsx3 for text-to-speech.

    ### 📜 Instructions:
    - Upload an image to start.
    - Choose a feature to interact with: Describe Scene, Extract Text, or Listen to it.

    ---
    Powered by Google Gemini API | Built with ❤️ using Streamlit
    """
)


# Functions for functionality
def extract_text_from_image(image):
    """Extracts text from the given image using EasyOCR."""
    image.save("temp_image.jpg")  # Save the image temporarily
    result = reader.readtext("temp_image.jpg", detail=0)  # Extract text without detailed coordinates
    os.remove("temp_image.jpg")  # Clean up the temporary image
    return "\n".join(result)


def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()


def generate_scene_description(input_prompt):
    """Generates a scene description using Google Generative AI."""
    response = genai.generate_text(model="gemini-1.5-pro", prompt=input_prompt)
    return response.get('text', 'Error generating description.')


def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")


# Upload Image Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    # Buttons Section
    st.markdown("<h3 class='feature-header'>⚙ Features</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    scene_button = col1.button("🔍 Describe Scene")
    ocr_button = col2.button("📝 Extract Text")
    tts_button = col3.button("🔊 Text-to-Speech")

    # Input Prompt for Scene Understanding
    input_prompt = """
    You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
    1. List of items detected in the image with their purpose.
    2. Overall description of the image.
    3. Suggestions for actions or precautions for the visually impaired.
    """

    # Process user interactions
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)

        if scene_button:
            with st.spinner("Generating scene description..."):
                response = generate_scene_description(input_prompt)
                st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
                st.write(response)

        if ocr_button:
            with st.spinner("Extracting text from the image..."):
                text = extract_text_from_image(image)
                st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
                st.text_area("Extracted Text", text, height=150)

        if tts_button:
            with st.spinner("Converting text to speech..."):
                text = extract_text_from_image(image)
                if text.strip():
                    text_to_speech(text)
                    st.success("✅ Text-to-Speech Conversion Completed!")
                else:
                    st.warning("No text found to convert.")

    # Footer
    st.markdown(
        """
        <hr>
        <footer>
            <p>Powered by <strong>Google Gemini API</strong> | Built with ❤️ using Streamlit</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )