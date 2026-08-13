# 📚 RAG PDF Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents.

The application extracts text from PDFs, splits the text into chunks, stores the chunks in ChromaDB, retrieves relevant information based on the user's question, and uses Groq to generate an answer.

## 🚀 Features

- Upload PDF documents
- Extract text from PDFs
- Split documents into smaller chunks
- Generate and store document embeddings
- Retrieve relevant document sections
- Ask questions about uploaded documents
- Generate answers using Groq
- Display retrieved sources and page numbers
- Streamlit web interface

## 🛠️ Technologies Used

- Python
- Streamlit
- PyPDF
- ChromaDB
- Groq
- python-dotenv

## 📂 Project Structure

```text
Project-05-RAG_Application/
│
├── README.md
├── .gitignore
├── project.ipynb
├── app.py
└── requirements.txt
```

## ⚙️ Installation

Clone the repository and enter the project directory:

```bash
cd Project-05-RAG_Application
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project directory:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Never commit your real API key to GitHub.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 RAG Pipeline

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
Groq LLM
    ↓
Generated Answer
    ↓
Retrieved Sources
```

## 📓 Jupyter Notebook

The `project.ipynb` notebook demonstrates the RAG pipeline step by step, including:

1. PDF text extraction
2. Document chunking
3. ChromaDB storage
4. Similarity retrieval
5. Context construction
6. Groq answer generation
7. Source display

## ⚠️ Notes

- A valid Groq API key is required.
- Do not upload or commit `.env` files containing API keys.
- The application works best with text-based PDFs.

## 👨‍💻 Contribution

This project was developed as part of the AI Open Source Beginner Projects repository.