# AI Study Assistant

A full-stack web application designed to help students efficiently parse, chunk, and analyze academic PDF textbooks and notes using natural language processing. 

## Features (Current Milestone)
* **PDF Text Extraction:** Extracts and processes raw text from user-uploaded PDF files, filtering out layout noise like page numbers and redundant spacing.
* **Smart Text Chunking:** Implements a custom sentence-boundary tokenization regex to split documents by semantic punctuation, clustering text into clean, length-restricted chunks optimized for NLP models.
* **Flask Backend Integration:** A lightweight Python/Flask server connects the backend text processing pipeline to an intuitive HTML/CSS user interface.

## Tech Stack
* **Frontend:** HTML5, CSS3
* **Backend:** Python, Flask
* **Data Processing:** Regular Expressions (Regex), PDF parsing libraries

## Project Structure
* `app.py` — Main Flask application handling routes and file uploads.
* `pdf_reader.py` — Core text extraction, cleaning, and text-chunking logic.
* `static/` & `templates/` — UI styling and layout configuration.

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/TheRedSea510/AI_Study_Assistant.git](https://github.com/TheRedSea510/AI_Study_Assistant.git)