# Medical Assistant Chatbot

This project is a Medical Assistant Chatbot that uses AI to analyze text and image inputs to identify diseases, provide detailed reports, and suggest treatments. The chatbot is built using Streamlit for the user interface and Google Generative AI for the analysis.

This `README.md` file provides an overview of the project, installation instructions, usage guidelines, dependencies, license information, and a disclaimer.

## Features

- **Personalization**: Collects user information (age, weight, medical history) to provide tailored recommendations.
- **Text and Image Analysis**: Processes text and image inputs to extract relevant information.
- **User-Friendly Reports**: Generates reports that are easy to understand for users who may not be familiar with medical terms.
- **Red Flags & Urgency**: Highlights urgent conditions and red flags in the report.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/Medical-Assistant-Chatbot.git
   cd Medical-Assistant-Chatbot
   ```
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a .env file in the project directory and add your Google API key:**:
   ```sh
   GOOGLE_API_KEY=your_google_api_key
   ```
5. **Run the application**:
   ```sh
   streamlit run app.py
   ```


