import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API key
api_key = os.getenv("GOOGLE_API_KEY", st.secrets.get("GOOGLE_API_KEY", None))
if not api_key:
    st.error("Google API key not found. Please add it to .env or Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Define supported languages
LANGUAGES = ["Python", "Java", "C++", "Go"]

# System prompt for multi-language code review
SYS_PROMPT = ("You are an expert AI Code Reviewer.\n"
              "When a user submits code in Python, Java, C++, or Go, you will:\n"
              "1. Analyze the logic, structure, and code style.\n"
              "2. Identify potential bugs, errors, or improvements.\n"
              "3. Suggest a corrected or optimized version of the code.\n\n"
              "Format your response like this:\n"
              "**Code Review:**\n[Detailed review here]\n\n"
              "**Bug Report:**\n[List of detected bugs or issues]\n\n"
              "**Fixed Code:**\n```<language>\n[Corrected code here]\n```")

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=SYS_PROMPT)

# Streamlit UI
st.title("AI Multi-Language Code Reviewer")

# Sidebar for history
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Review History")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Review #{len(st.session_state.history) - idx}"):
                st.code(item['code'][:120] + "...", language=item['lang'].lower())
                if st.button(f"Load Review #{len(st.session_state.history) - idx}", key=f"load_{idx}"):
                    st.session_state.current_code = item['code']
                    st.session_state.current_review = item['review']
                    st.session_state.current_lang = item['lang']
                    st.rerun()
    else:
        st.info("No reviews yet.")

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Your Code")
    language = st.selectbox("Select Language", LANGUAGES, index=0)
    user_code = st.text_area(
        "Enter your code here:",
        height=400,
        value=st.session_state.get('current_code', ''),
        placeholder="# Paste your code here"
    )

with col2:
    st.subheader("AI Review")
    review_container = st.container()

# Generate review button
if st.button("Generate Review", type="primary"):
    if user_code.strip():
        try:
            with st.spinner("Analyzing your code..."):
                response = model.generate_content(f"Language: {language}\n\nCode:\n{user_code}")
                review = response.text

                st.session_state.history.append({
                    'lang': language,
                    'code': user_code,
                    'review': review
                })
                st.session_state.current_review = review

            with review_container:
                st.markdown(review)

                st.download_button(
                    label="Download Review",
                    data=f"# Code Review\n\n## Language: {language}\n\n## Original Code:\n```{language.lower()}\n{user_code}\n```\n\n## Review:\n{review}",
                    file_name="code_review.md",
                    mime="text/markdown"
                )

            st.success("Review complete.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please verify your API key or internet connection.")
    else:
        st.warning("Please enter code before generating a review.")

elif 'current_review' in st.session_state:
    with review_container:
        st.markdown(st.session_state.current_review)
        st.download_button(
            label="Download Review",
            data=f"# Code Review\n\n## Original Code:\n```{language.lower()}\n{user_code}\n```\n\n## Review:\n{st.session_state.current_review}",
            file_name="code_review.md",
            mime="text/markdown"
        )
