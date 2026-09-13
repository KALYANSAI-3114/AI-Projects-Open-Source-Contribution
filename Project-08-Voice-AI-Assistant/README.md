```markdown
# 🚀 Voice AI Assistant

A Voice AI Assistant capable of answering user queries using speech. It records audio from the user, transcribes it to text, generates an intelligent response using an LLM, and speaks the response back.

## ✨ Features
- **Voice Input (Speech-to-Text):** Uses `faster-whisper` to transcribe user voice input locally.
- **Voice Output (Text-to-Speech):** Uses `gTTS` to convert AI text responses into spoken audio.
- **AI Responses (LLM):** Uses `Groq` API for fast, intelligent, and accurate conversational responses.
- **Conversation History:** Remembers chat context during the session using Streamlit's session state.
- **Streamlit Frontend:** Built with Streamlit, featuring a microphone input and a clean chat UI.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Speech-to-Text:** Faster-Whisper
- **Text-to-Speech:** gTTS
- **LLM:** Groq API

## 📋 Prerequisites
- Python 3.8+
- A Groq API Key (Get it free from [console.groq.com](https://console.groq.com/))
- `ffmpeg` installed on your system (required by faster-whisper).

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API Key:**
   Create a file named `.env` in the root directory and add your Groq API key:
   ```text
   GROQ_API_KEY=your_api_key_here
   ```

## 🚀 Running the App

Start the Streamlit web app by running:
```bash
streamlit run app.py
```
Click the "Record your question" button, speak, and hear the AI respond!

## 📁 Project Structure
```text
├── voice_ai/
│   ├── __init__.py
│   ├── stt.py              # Speech to text logic
│   ├── tts.py              # Text to speech logic
│   └── llm.py              # LLM logic
├── app.py                  # Streamlit frontend
├── project.ipynb           # Jupyter notebook for testing
├── requirements.txt        # Dependencies
├── .gitignore              # Files to ignore in git
├── README.md               # Documentation
└── .env                    # API keys (Not included in git)
```
```