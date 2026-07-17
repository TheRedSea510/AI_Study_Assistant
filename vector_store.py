import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):

    chunk_text = []

    for chunk in chunks:
        chunk_text.append(chunk["text"])

    vectors = embedding_model.encode(chunk_text)

    return vectors

def build_vector_database(chunk_vectors):
    dimension = chunk_vectors.shape[1]  

    faiss.normalize_L2(chunk_vectors.astype("float32"))  # Normalize the vectors for cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(chunk_vectors.astype("float32"))

    return index

def search_notes(user_question, index, lecture_chunks, results=3):
    question_vector = embedding_model.encode([user_question])
    
    faiss.normalize_L2(question_vector)

    question_vector = question_vector.astype("float32")

    distances, positions = index.search(question_vector, results)

    matching_chunks = []

    for position in positions[0]:
        # FIX: Ensure FAISS found a real index and it falls within your chunk range
        if position != -1 and position < len(lecture_chunks):
            matching_chunks.append(lecture_chunks[position])

    return matching_chunks
