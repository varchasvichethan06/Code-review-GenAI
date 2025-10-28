# 🧠 AI Code Reviewer

A Streamlit-based web app that uses **Google Gemini** models to automatically review code written in **Python, Java, C++**, and **Go**. It provides detailed feedback, detects bugs, and suggests corrected code versions — all within an intuitive UI.

---
## 🚀 Features
- 🧩 Supports **Python, Java, C++**, and **Go** code
- 🤖 Uses **Gemini 1.5 Flash** for fast AI-powered code review
- 🪄 Provides structured feedback:
  - Code Review
  - Bug Report
  - Fixed Code
- 💾 Maintains review history within the session
- 📥 Download AI review as Markdown
- 🔐 Supports both `.env` and Streamlit Cloud `secrets.toml` for secure API key management
---
## 🛠️ Installation
### 1. Clone this repository
```
git clone https://github.com/yourusername/multi-lang-code-reviewer.git
cd multi-lang-code-reviewer
```
### 2. Create a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate    # Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
**requirements.txt:**
```
streamlit>=1.36.0
google-generativeai>=0.8.0
python-dotenv>=1.0.1
```

---
## 🔑 Setup API Key
### Option 1: Using `.env` file (for local development)
Create a `.env` file in your project root:
```
GOOGLE_API_KEY=your_api_key_here
```
### Option 2: Using Streamlit Secrets (for Streamlit Cloud)
In `.streamlit/secrets.toml`:
```
GOOGLE_API_KEY = "your_api_key_here"
```
Get your key from **[Google AI Studio](https://aistudio.google.com/)**.

---
## 🧾 Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to the local URL shown (usually `http://localhost:8501`).
1. Choose your programming language.
2. Paste your code in the text box.
3. Click **Generate Review**.
4. View AI feedback under the **AI Review** tab.
5. Download the review as a `.md` file if needed.

---
## 🧩 Folder Structure
```
project/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # Dependencies
├── .env                     # (optional) Local API key storage
├── .streamlit/
│   └── secrets.toml         # Streamlit Cloud secrets
└── README.md                # Documentation
```

---
## 🧠 Model Used
- **Model:** `gemini-1.5-flash`
- **Provider:** Google Generative AI API
---
## 💡 Future Improvements
- Add syntax highlighting for fixed code
- Enable multi-file uploads
- Export reviews as PDF
- Integrate version control comments (e.g., GitHub PR)
---
