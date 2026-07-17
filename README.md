# AI Study Assistant

A full-stack Retrieval-Augmented Generation (RAG) web application designed to help students upload academic PDFs, automatically process lecture notes, and ask natural language questions against their documents using semantic search and generative AI.

The system combines document processing, vector embeddings, FAISS similarity search, and Google's Gemini LLM to retrieve relevant sections of uploaded lecture notes and generate accurate answers with source citations.

## Features (Current Milestone)

* **PDF Text Extraction & Cleaning:** Extracts text from user-uploaded PDF files while removing unnecessary formatting noise, redundant spacing, and irrelevant page number artifacts.

* **Page-Aware Sentence Chunking:** Splits documents into sentence-aware chunks without cutting sentences in half. Each chunk stores additional metadata including:
  - Original PDF filename
  - Page number
  - Extracted text content

* **Semantic Vector Search:** Converts document chunks into embeddings using the `all-MiniLM-L6-v2` Sentence-Transformer model and stores them in a FAISS vector index for efficient similarity-based retrieval.

* **Citation-Aware RAG Pipeline:** Retrieved chunks maintain their original document metadata, allowing generated answers to reference the exact PDF and page number used as supporting evidence.

* **Gemini AI Integration:** Uses the Google GenAI SDK (`gemini-3.5-flash`) to generate natural explanations based only on retrieved lecture material, reducing hallucinations by restricting responses to provided context.

* **Fault-Tolerant API Handling:** Implements exponential backoff retries and automatic model fallback handling to gracefully manage temporary Gemini API availability issues.

* **Multiple PDF Support:** Allows users to upload multiple PDFs within the same session. New documents are processed and added alongside existing uploaded material instead of replacing previous data.

* **Flask Backend Integration:** A lightweight modular Flask backend connects the frontend interface with the complete document processing and AI pipeline.

## How It Works

1. User uploads one or more PDF lecture documents.
2. PDF text is extracted page-by-page and cleaned.
3. The text is split into smaller sentence-aware chunks.
4. Each chunk is stored with metadata:
   - Document filename
   - Page number
   - Chunk content
5. Chunks are converted into numerical embeddings.
6. FAISS searches for the most relevant chunks based on the user's question.
7. The retrieved context is sent to Gemini.
8. Gemini generates an answer with references to the supporting sources.

## Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript
* **Backend:** Python, Flask
* **Vector Database & Embeddings:** FAISS (cosine similarity search), Sentence-Transformers (`all-MiniLM-L6-v2`)
* **LLM API:** Google GenAI SDK (`gemini-3.5-flash`, `gemini-3.1-flash-lite`)
* **Data Processing:** `pypdf`, Regular Expressions (Regex), NumPy

## Project Structure

* `app.py` — Main Flask application handling routes, PDF uploads, session storage, and connecting the document pipeline together.

* `ai_model.py` — Handles Gemini API communication, prompt construction, context formatting, citation instructions, and retry logic.

* `vector_store.py` — Creates embeddings using Sentence-Transformers, builds the FAISS vector index, and performs similarity searches.

* `pdf_reader.py` — Handles PDF extraction, text cleaning, page tracking, and sentence-aware chunk generation with metadata.

* `static/` & `templates/` — Frontend styling, HTML templates, and user interface components.

## Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/TheRedSea510/AI_Study_Assistant.git
cd AI_Study_Assistant