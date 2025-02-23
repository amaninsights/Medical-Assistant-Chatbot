import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image  # For image processing
import pytesseract  # For OCR (Make sure Tesseract OCR is installed)

# Load environment variables from .env file
load_dotenv()

# Ensure Google API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found. Please set it in your .env file.")
    st.stop()

# Configure Gemini with the API key
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System prompts for the Gemini model
system_prompts = """
You are a domain expert in medical analysis. Your task is to analyze text or image inputs to identify diseases, provide detailed reports, and suggest treatments.

Your responsibilities:
1. **Detailed Analysis**: Thoroughly examine the input for abnormalities or symptoms.
2. **Analysis Report**: Document findings in a structured format.
3. **Recommendations**: Suggest remedies, tests, or treatments.
4. **Treatments**: Provide detailed treatment plans for faster recovery.
5. **Differential Diagnosis**: List possible conditions based on the input.
6. **Follow-Up Steps**: Suggest next steps for monitoring and further evaluation.
7. **Red Flags & Urgency**: Highlight any urgent conditions or red flags.
8. **User-Friendly Language**: Ensure the report is easy to understand for users who may not be familiar with medical terms.

Important Notes:
1. Only respond to human health-related inputs.
2. If the input is unclear, note: "Unable to determine based on the provided input."
3. Always include the disclaimer: "Consult with a Doctor before making any decisions."

Provide the final response under these headings: 
- **Detailed Analysis**  
- **Analysis Report**  
- **Recommendations**  
- **Treatments**
- **Based on the detected condition, the model suggests the appropriate specialist(s)**  
- **Differential Diagnosis**  
- **Follow-Up Steps**  
- **Red Flags & Urgency**  
"""

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Function to process image and extract text using OCR
def process_image(image_file):
    """Process the uploaded image file and extract text using OCR."""
    try:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        text = pytesseract.image_to_string(image)
        if not text.strip():
            return "No readable text found in the image."
        return text
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Medical Assistant", page_icon="🩺", layout="wide")
st.title("🩺 Medical Assistant Chatbot")

# Input options
st.write("You can provide text, an image, or both for analysis.")

# Collect additional user information for personalization
col1, col2 = st.columns(2)
with col1:
    age = st.slider("Enter your age:", min_value=0, max_value=120, value=25)
with col2:
    weight = st.slider("Enter your weight (kg):", min_value=0.0, max_value=200.0, value=70.0, step=0.1)

medical_history = st.text_area("Enter your medical history (optional):")

# Text input
user_input = st.text_area("Enter your symptoms or condition:")

# Image input
image_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])

# Generate analysis
if st.button("Generate Analysis"):
    response_text = None  # Initialize response

    combined_input = system_prompts
    combined_input += f"\nUser Information: Age: {age}, Weight: {weight} kg, Medical History: {medical_history}"

    if user_input:
        combined_input += f"\nUser Input (Text): {user_input}"

    if image_file:
        extracted_text = process_image(image_file)
        if extracted_text:
            combined_input += f"\nUser Input (Image): {extracted_text}"

    if user_input or image_file:
        response = model.generate_content(combined_input)
        response_text = response.text
    else:
        st.error("Please provide valid input.")

    # Display the response
    if response_text:
        st.subheader("🔍 Medical Analysis Report")
        st.markdown(response_text)
        st.warning("⚠️ Disclaimer: Consult with a Doctor before making any medical decisions.")

