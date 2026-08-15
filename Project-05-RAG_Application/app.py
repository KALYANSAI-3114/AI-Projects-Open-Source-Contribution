import os
import hashlib
from io import BytesIO

import chromadb
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.1-8b-instant"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_documents"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RAG PDF Assistant",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# INITIALIZE GROQ
# ============================================================

@st.cache_resource
def get_groq_client():
    if not GROQ_API_KEY:
        return None

    return Groq(api_key=GROQ_API_KEY)


groq_client = get_groq_client()


# ============================================================
# INITIALIZE CHROMADB
# ============================================================

@st.cache_resource
def get_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


collection = get_chroma_collection()


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_file):
    """
    Extract text from every page of the uploaded PDF.
    """

    pdf_bytes = pdf_file.getvalue()

    reader = PdfReader(BytesIO(pdf_bytes))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            pages.append(
                {
                    "page": page_number,
                    "text": text.strip()
                }
            )

    return pages


# ============================================================
# TEXT CHUNKING
# ============================================================

def create_chunks(pages):
    """
    Split PDF text into overlapping chunks.
    """

    chunks = []

    for page_data in pages:

        text = page_data["text"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append(
                    {
                        "text": chunk_text,
                        "page": page_data["page"]
                    }
                )

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ============================================================
# CREATE DOCUMENT ID
# ============================================================

def create_document_id(pdf_file):
    """
    Create a unique ID based on the uploaded PDF.
    """

    pdf_bytes = pdf_file.getvalue()

    return hashlib.md5(pdf_bytes).hexdigest()


# ============================================================
# STORE DOCUMENT IN CHROMADB
# ============================================================

def store_document(chunks, document_id, filename):
    """
    Store document chunks in ChromaDB.

    ChromaDB automatically creates embeddings for the
    documents using its configured/default embedding function.
    """

    # Delete old chunks belonging to this document
    try:

        collection.delete(
            where={
                "document_id": document_id
            }
        )

    except Exception:
        pass

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        f"{document_id}_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return len(chunks)


# ============================================================
# RETRIEVE RELEVANT CONTEXT
# ============================================================

def retrieve_context(question, document_id):
    """
    Search ChromaDB for chunks relevant to the question.
    """

    results = collection.query(
        query_texts=[question],
        n_results=TOP_K,
        where={
            "document_id": document_id
        }
    )

    documents = results.get("documents", [[]])[0]

    metadatas = results.get("metadatas", [[]])[0]

    retrieved_context = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        retrieved_context.append(
            {
                "text": document,
                "filename": metadata.get(
                    "filename",
                    "Unknown"
                ),
                "page": metadata.get(
                    "page",
                    "Unknown"
                )
            }
        )

    return retrieved_context


# ============================================================
# GENERATE ANSWER USING GROQ
# ============================================================

def generate_answer(question, retrieved_context):
    """
    Generate an answer using the retrieved document context.
    """

    if groq_client is None:

        raise ValueError(
            "GROQ_API_KEY was not found. "
            "Please check your .env file."
        )

    context_parts = []

    for index, item in enumerate(
        retrieved_context,
        start=1
    ):

        context_parts.append(
            f"""
Source {index}
File: {item['filename']}
Page: {item['page']}

{item['text']}
"""
        )

    context = "\n".join(context_parts)

    system_prompt = """
You are a helpful Retrieval-Augmented Generation assistant.

Answer the user's question using ONLY the provided document context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not available in the context,
   say that the answer could not be found in the uploaded document.
4. Give a clear and concise answer.
5. Use the source information provided in the context.
"""

    user_prompt = f"""
DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

Answer the question using only the document context.
"""

    response = groq_client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.2,

        max_tokens=800
    )

    return response.choices[0].message.content


# ============================================================
# SESSION STATE
# ============================================================

if "document_id" not in st.session_state:

    st.session_state.document_id = None


if "filename" not in st.session_state:

    st.session_state.filename = None


if "document_ready" not in st.session_state:

    st.session_state.document_ready = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    st.write(
        f"**LLM:** {GROQ_MODEL}"
    )

    st.write(
        "**Vector Database:** ChromaDB"
    )

    st.write(
        "**Embeddings:** ChromaDB"
    )

    st.write(
        f"**Top K:** {TOP_K}"
    )

    st.write(
        f"**Chunk Size:** {CHUNK_SIZE}"
    )

    st.divider()

    if GROQ_API_KEY:

        st.success(
            "Groq API key loaded"
        )

    else:

        st.error(
            "Groq API key not found"
        )


# ============================================================
# MAIN TITLE
# ============================================================

st.title("📚 RAG PDF Assistant")

st.write(
    """
Upload a PDF and ask questions about its contents.
The application retrieves relevant information from
your document and uses Groq to generate an answer.
"""
)

st.divider()


# ============================================================
# PDF UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📄 Upload a PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    document_id = create_document_id(
        uploaded_file
    )

    # Process only when a new PDF is uploaded
    if document_id != st.session_state.document_id:

        st.session_state.document_id = document_id

        st.session_state.filename = (
            uploaded_file.name
        )

        st.session_state.document_ready = False

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        with st.spinner(
            "📖 Extracting text from PDF..."
        ):

            pages = extract_text_from_pdf(
                uploaded_file
            )

        if not pages:

            st.error(
                """
                No readable text was found in this PDF.

                Please upload a text-based PDF.
                """
            )

        else:

            st.success(
                f"Extracted text from "
                f"{len(pages)} page(s)."
            )

            # ------------------------------------------------
            # Create chunks
            # ------------------------------------------------

            with st.spinner(
                "✂️ Splitting document into chunks..."
            ):

                chunks = create_chunks(
                    pages
                )

            st.info(
                f"Created {len(chunks)} text chunks."
            )

            # ------------------------------------------------
            # Store vectors
            # ------------------------------------------------

            with st.spinner(
                "🧠 Creating embeddings and storing vectors..."
            ):

                number_of_chunks = store_document(
                    chunks,
                    document_id,
                    uploaded_file.name
                )

            st.session_state.document_ready = True

            st.success(
                f"✅ Document ready! "
                f"{number_of_chunks} chunks stored in ChromaDB."
            )


# ============================================================
# QUESTION ANSWERING
# ============================================================

if st.session_state.document_ready:

    st.divider()

    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Enter your question:",
        placeholder=(
            "Example: What is the main objective "
            "of this document?"
        )
    )

    ask_button = st.button(
        "🔍 Ask Question",
        type="primary"
    )

    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            # ------------------------------------------------
            # Retrieve context
            # ------------------------------------------------

            with st.spinner(
                "🔎 Searching the document..."
            ):

                retrieved_context = (
                    retrieve_context(
                        question,
                        st.session_state.document_id
                    )
                )

            if not retrieved_context:

                st.warning(
                    "No relevant information was found."
                )

            else:

                # ------------------------------------------------
                # Generate answer
                # ------------------------------------------------

                with st.spinner(
                    "🤖 Generating answer..."
                ):

                    try:

                        answer = generate_answer(
                            question,
                            retrieved_context
                        )

                        st.subheader(
                            "🤖 Answer"
                        )

                        st.write(answer)

                    except Exception as error:

                        st.error(
                            f"Error generating answer: {error}"
                        )

                # ------------------------------------------------
                # Display sources
                # ------------------------------------------------

                st.subheader(
                    "📚 Retrieved Sources"
                )

                for index, source in enumerate(
                    retrieved_context,
                    start=1
                ):

                    with st.expander(
                        f"Source {index} — Page {source['page']}"
                    ):

                        st.write(
                            f"**File:** "
                            f"{source['filename']}"
                        )

                        st.write(
                            f"**Page:** "
                            f"{source['page']}"
                        )

                        st.write(
                            source["text"]
                        )

else:

    st.info(
        "👆 Upload a PDF above to begin."
    )