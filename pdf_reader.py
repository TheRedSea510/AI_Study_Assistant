from pypdf import PdfReader
import re

# Gets the pdf text from the pdf being uploaded and the loacation of the file
def get_pdf_text(file_location):

    pdf_document = PdfReader(file_location)

    # Initialize an empty string to store the extracted text
    lecture_text = ""
 
    # Iterate through each page in the PDF document and extract text
    for page in pdf_document.pages:

        # Extract text from the current page
        page_text = page.extract_text()

        # Append the extracted text to the lecture_text string if it's not None
        if page_text:
            lecture_text += page_text + "\n"

    # Clean the extracted text by removing unnecessary whitespace and formatting
    cleaned_text = clean_text(lecture_text)

    return cleaned_text

# Function to clean the extracted text by removing unnecessary whitespace, line breaks, and page numbers
def clean_text(raw_text):

    # Remove line breaks and carriage returns
    cleaned_text = raw_text.replace("\n", " ")

    # Remove carriage returns
    cleaned_text = cleaned_text.replace("\r", " ")

    # Remove multiple spaces and replace them with a single space
    cleaned_text = " ".join(cleaned_text.split())

    # Remove page numbers (e.g., "Page 1", "Page 2", etc.)
    cleaned_text = re.sub(r"Page\s+\d+", "", cleaned_text)

    return cleaned_text

# Function to split the cleaned text into chunks of a specified max chunk size
def split_into_chunks(text, max_chunk_size=500):

    # Splits the sentences based on punctuation marks (., !, ?) followed by whitespace
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Initialize an empty list to store the chunks
    chunks = []

    # Creates an empty string to hold the current selection of sentences that will be combined into a chunk
    current_selection = ""

    # Iterate through each sentence and build chunks based on the max_chunk_size
    for sentence in sentences:

        # Create a new chunk by adding the current sentence to the current selection
        new_chunk = current_selection + sentence + " "

        # Check if the length of the new chunk is within the max_chunk_size limit
        if len(new_chunk) <= max_chunk_size:
            # If the new chunk is within the limit, update the current selection to include the new sentence
            current_selection = new_chunk

        # If the new chunk exceeds the max_chunk_size limit, finalize the current selection as a chunk and start a new selection with the current sentence
        else:
            if current_selection:
                chunks.append(current_selection.strip())

            # Start a new selection with the current sentence
            current_selection = sentence + " "

    # After iterating through all sentences, check if there is any remaining text in current_selection and add it as a final chunk
    if current_selection:
        chunks.append(current_selection.strip())

    return chunks

