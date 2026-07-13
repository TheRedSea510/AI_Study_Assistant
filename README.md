# AI Study Assistant

A full-stack Retrieval-Augmented Generation (RAG) web application designed to help students upload academic PDFs, automatically chunk the text, and ask natural language questions against their lecture notes using vector search and generative AI.

## Features (Current Milestone)
* **PDF Text Extraction:** Extracts raw text from user-uploaded PDF files, automatically clearing layout noise, redundant spacing, and page number formatting.
* **Smart Sentence-Aware Chunking:** Utilizes a custom punctuation-based regex splitter to cluster text into clean, length-restricted semantic windows without cutting sentences in half.
* **Local Vector Storage:** Embeds extracted chunks locally using the `all-MiniLM-L6-v2` Sentence-Transformer and indexes them with a high-performance **FAISS** (Facebook AI Similarity Search) database.
* **Fault-Tolerant Gemini Integration:** Connected to the Google GenAI SDK (`gemini-3.5-flash`) with built-in **exponential backoff retries** and automatic model failovers to gracefully bypass free-tier `503 Service Unavailable` errors.
* **Flask Backend Integration:** A lightweight, modular Python/Flask server driving the data pipeline and exposing intuitive endpoints for front-end templates.

## Tech Stack
* **Frontend:** HTML5, CSS3, JavaScript
* **Backend:** Python, Flask
* **Vector Database & Embeddings:** FAISS (FlatL2), Sentence-Transformers (`all-MiniLM-L6-v2`)
* **LLM API:** Google GenAI SDK (`gemini-3.5-flash`, `gemini-3.1-flash-lite`)
* **Data Processing:** PyPDF, Regular Expressions (Regex), NumPy

## Project Structure
* `app.py` — Main Flask application orchestrating the upload routes, document pipeline, and similarity search queries.
* `ai_model.py` — Handles connection to the Gemini API, prompt configuration, and resilient retry-logic handling server load.
* `vector_store.py` — Manages local embedding generation via Sentence-Transformers and handles the FAISS similarity index.
* `pdf_reader.py` — Core text extraction, formatting cleanup, and custom sentence-aware chunking logic.
* `static/` & `templates/` — UI web styling, layout configurations, and user templates.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/TheRedSea510/AI_Study_Assistant.git](https://github.com/TheRedSea510/AI_Study_Assistant.git)
   cd AI_Study_Assistant