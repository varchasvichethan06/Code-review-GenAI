import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
import re
from dotenv import load_dotenv

# --------------------------------------------------------
# 🔧 Load environment variables
# --------------------------------------------------------
load_dotenv()

# --------------------------------------------------------
# 🔑 Configure API Key
# --------------------------------------------------------
#api_key = os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY_HERE"
api_key = "AIzaSyAoJnWj9earmDpIvo6J1Lm0UZxW9BBF5Y4"

if not api_key or api_key == "YOUR_API_KEY_HERE":
    st.error("❌ No API key found. Please set GOOGLE_API_KEY in your .env or Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --------------------------------------------------------
# 🧠 System Instruction for AI Reviewer
# --------------------------------------------------------
SYSTEM_PROMPT = """
You are a helpful AI Code Reviewer. 
When students provide code, you will:
1. Detect the programming language.
2. Provide a detailed **Code Review**.
3. Highlight issues or errors in a **Bug Report**.
4. Provide a corrected version in **Fixed Code**.

Follow this format exactly:
- **Language Detected:** [language]
- **Code Review:**
  [Review here]
- **Bug Report:**
  [List issues here]
- **Fixed Code:**
  ```[language]
  [Fixed version here]
If no bugs, say 'No issues found' and still show a clean code version.
"""

# --------------------------------------------------------
# ⚙️ Configure Model
# --------------------------------------------------------
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-pro",
    system_instruction=SYSTEM_PROMPT
)

# --------------------------------------------------------
# 🖥️ Streamlit UI Setup
# --------------------------------------------------------
st.set_page_config(page_title="GenAI Code Reviewer", page_icon="🤖", layout="wide") 
st.title("🤖 AI Code Reviewer")

# Initialize session state
if "history" not in st.session_state: 
    st.session_state.history = [] 
if "review" not in st.session_state: 
    st.session_state.review = "" 
if "code" not in st.session_state:
    st.session_state.code = ""
if "language" not in st.session_state:
    st.session_state.language = ""

# --------------------------------------------------------
# 🧭 Sidebar (History)
# --------------------------------------------------------
with st.sidebar: 
    st.header("📜 Review History") 
    if st.session_state.history: 
        for idx, item in enumerate(reversed(st.session_state.history)): 
            with st.expander(f"Review #{len(st.session_state.history) - idx} ({item['time']})"): 
                st.code(item["code"][:120] + "...")
            if st.button(f"Load #{len(st.session_state.history) - idx}", key=f"load_{idx}"): 
                st.session_state.code = item["code"] 
                st.session_state.review = item["review"]
                st.session_state.language = item.get("language", "")
                st.rerun() 
    else: 
        st.info("No reviews yet.")

    if st.button("🗑️ Clear All"): 
        st.session_state.clear() 
        st.success("Session cleared!") 
        st.rerun()

# --------------------------------------------------------
# 🧩 Tabs
# --------------------------------------------------------
tab_code, tab_review = st.tabs(["💻 Your Code", "✨ AI Review"])

# --------------------------------------------------------
# 💻 Code Input Tab
# --------------------------------------------------------
with tab_code: 
    code_input = st.text_area(
        "Enter your code:",
        value=st.session_state.code,
        height=400,
        placeholder="// Paste your code here (any language)..."
    )

    if st.button("🔍 Generate Review"): 
        if not code_input.strip(): 
            st.warning("Please enter code first.") 
        else: 
            with st.spinner("Analyzing your code..."): 
                try:
                    # Send user code to Gemini
                    response = model.generate_content([
                        {"role": "user", "parts": [code_input]}
                    ])

                    review_text = response.text.strip() if response.text else "⚠️ No review generated. Please check the API response."

                    # Detect language from review text
                    lang_match = re.search(r"(?i)\**\s*(language\s*detected|detected\s*language)\s*[:\-]\s*\**\s*([A-Za-z0-9+#\-\s]+)", review_text)
                    detected_lang = lang_match.group(2).strip() if lang_match else "Unknown"

                    # If no "Fixed Code" section, show a friendly message
                    if "Fixed Code" not in review_text:
                        review_text += "\n\n✅ It's all good! Your code looks perfect."

                    # Save session data
                    st.session_state.code = code_input 
                    st.session_state.review = review_text 
                    st.session_state.language = detected_lang
                    st.session_state.history.append({
                        "code": code_input,
                        "review": review_text,
                        "language": detected_lang,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }) 

                    st.success(f"✅ Review generated successfully! (Language: {detected_lang})") 

                except Exception as e:
                    st.error(f"Error: {e}") 
                    st.info("Check if the API key is valid and Gemini access is enabled.")

# --------------------------------------------------------
# ✨ Review Tab
# --------------------------------------------------------
with tab_review: 
    if st.session_state.review:
        if st.session_state.language:
            st.subheader(f"🌐 Language Detected: {st.session_state.language}")
        st.markdown(st.session_state.review) 
        st.download_button(
            "📥 Download Review",
            data=f"## Code Review\n\n{st.session_state.code}\n\n{st.session_state.review}",
            file_name="code_review.md",
            mime="text/markdown"
        )
    else:
        st.info("No review yet. Generate one in the first tab.")

