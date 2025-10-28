Python-code-review-GenAI

----------------------
📘 Project Description:
Python-code-review-GenAI is an AI-powered Python code review web app built using Streamlit and Google’s Gemini Generative AI API.
The application analyzes Python scripts, identifies bugs, and automatically suggests corrected versions — all in a clear, structured format.

Users can simply paste their Python code into the app, and the GenAI model provides:
Code Review: A detailed analysis of code quality, readability, and logic.
Bug Report: A list of detected syntax or logical issues.
Fixed Code: A revised and improved version of the provided code.

This project demonstrates the integration of Google’s Gemini AI with an interactive Streamlit interface to create a smart educational and debugging assistant for Python learners and developers.

----------------------
⚙️ Tech Stack:
Python 3.10+
Streamlit – for the interactive UI
Google Generative AI (Gemini) – for natural language code analysis

----------------------
🚀 How It Works:
User inputs Python code into the Streamlit interface.
The system sends the input to the Gemini model along with a predefined system prompt.

The model returns a structured output containing:
Code Review
Bug Report
Fixed Code
The result is displayed neatly on the web interface.

----------------------
🔐 Environment Setup:
Add your Google API key:
export GOOGLE_API_KEY="your_api_key_here"

or create a .env file:
GOOGLE_API_KEY=your_api_key_here

Then run:
pip install streamlit google-generativeai
streamlit run app.py

----------------------
💡 Use Cases:
Automated Python code feedback for students.
AI-assisted debugging for developers.
Quick review tool for coding tutorials and workshops.
