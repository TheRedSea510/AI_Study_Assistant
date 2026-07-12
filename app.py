import os

from flask import Flask, render_template, request

from pdf_reader import get_pdf_text, split_into_chunks

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Make sure the upload folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
# Define the home route that renders the index.html template
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
# Define the upload route that handles PDF file uploads and processing
def upload_file():

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
    lecture_notes = get_pdf_text(file_location)

    # Split the extracted lecture notes into chunks of a specified maximum size
    lecture_chunks = split_into_chunks(lecture_notes)

    # Return a success message to show that the file has been uploaded and processed successfully
    return "PDF uploaded and processed successfully"




if __name__ == "__main__":
    app.run(debug=True)