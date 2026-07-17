import os
import numpy as np
from flask import Flask, render_template, request

from ai_model import answer_question
from pdf_reader import get_pdf_text, split_into_chunks
from vector_store import build_vector_database, create_embeddings, search_notes

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Make sure the upload folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

stored_chunks = None
stored_embeddings = None
stored_index = None


@app.route("/")
# Define the home route that renders the index.html template
def home():
    return render_template("index.html", upload_message=None, ai_answer=None)


@app.route("/upload", methods=["POST"])
# Define the upload route that handles PDF file uploads and processing
def upload_file():

    global stored_chunks
    global stored_embeddings
    global stored_index

    # Check if a "pdf" file is present in the request.files dictionary
    if "pdf" not in request.files:
        return "No file uploaded", 400

    # Get the uploaded PDF file from the request
    uploaded_pdf = request.files["pdf"]

    # Check if the uploaded file has a valid filename and is a PDF file
    if uploaded_pdf.filename == "":
        return "No file selected", 400

    # Check if the uploaded file has a valid PDF extension
    if not uploaded_pdf.filename.endswith(".pdf"):
        return "Only PDF files are allowed", 400

    # Save the uploaded PDF file to the "UPLOAD_FOLDER" folder and get the file location
    save_folder = app.config["UPLOAD_FOLDER"]

    file_location = os.path.join(save_folder, uploaded_pdf.filename) # type: ignore

    # Save the uploaded PDF file to the specified file location
    uploaded_pdf.save(file_location)

    # Get the text from the uploaded PDF file
    lecture_pages = get_pdf_text(file_location)

    # Split the extracted lecture notes into chunks of a specified maximum size
    new_chunks = split_into_chunks(lecture_pages, uploaded_pdf.filename)

    print(new_chunks[0])

    if stored_chunks is None:
        stored_chunks = new_chunks
    else:
        stored_chunks.extend(new_chunks)

    new_embeddings = create_embeddings(new_chunks)

    stored_embeddings = np.vstack([stored_embeddings, new_embeddings]) if stored_embeddings is not None else new_embeddings

    stored_index = build_vector_database(stored_embeddings)

    # Return a success message to show that the file has been uploaded and processed successfully
    return render_template("index.html", upload_message="File uploaded and processed successfully!", ai_answer=None)

@app.route("/ask", methods=["POST"])
def ask_question():
    question = request.form.get("question")

    if stored_chunks is None or stored_index is None:
        print("Chunks:", stored_chunks is None)
        print("Index:", stored_index is None)
        return "No lecture notes available. Please upload a PDF first.", 400
    
    matching_chunks = search_notes(question, stored_index, stored_chunks)
    ai_response = answer_question(question, matching_chunks)
    print("\nRetrieved chunks:")

    for chunk in matching_chunks:
        print("----------------")
        print("File:", chunk["filename"])
        print("Page:", chunk["page"])
        print("Text:", chunk["text"])

    return render_template("index.html", upload_message=None, ai_answer=ai_response)



if __name__ == "__main__":
    app.run(debug=True)