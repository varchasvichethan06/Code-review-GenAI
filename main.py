import streamlit as st
import google.generativeai as genai

#1. Configure your Gemini API key here
genai.configure(api_key="YOUR_API_KEY_HERE")

#2. Define the system prompt
sys_prompt = """
You are a helpful AI Python Code Reviewer. 
When students provide Python code, you will:
1. Provide a detailed **Code Review** of the code.
2. Highlight any issues or errors in a section labeled **Bug Report**.
3. Provide a corrected version of the code in a section labeled **Fixed Code**.

Always format your response exactly like this:
- **Code Review:**
  [Your review here]

- **Bug Report:**
  [List of bugs here]

- **Fixed Code:**
  [Corrected Python code here]

If there are no bugs, clearly state that in the Bug Report section and still provide a reviewed version of the code in Fixed Code.

Do not respond to anything unrelated to Python code.
"""

#3. Use a valid model that your account supports
# If "gemini-1.5-flash" gives a 404, switch to "models/gemini-1.5-pro"
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro",
    system_instruction=sys_prompt
)

#4. Streamlit UI
st.title("PYTHON-CODE_REVIEW-GENAI")

human_prompt = st.text_area("Enter your Python code here ...")

if st.button("Generate"):
    if human_prompt.strip():
        response = model.generate_content(human_prompt)
        response_text = response.text
        st.markdown(response_text)
    else:
        st.warning("Please enter Python code before clicking Generate.")
