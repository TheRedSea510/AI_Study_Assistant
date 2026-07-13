import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(text_chunks):

    vectors = embedding_model.encode(text_chunks)

    return vectors

def build_vector_database(chunk_vectors):
    dimension = chunk_vectors.shape[1]  
    index = faiss.IndexFlatL2(dimension)
    index.add(chunk_vectors.astype("float32"))

    return index

def search_notes(user_question, index, lecture_chunks, results=3):
    question_vector = embedding_model.encode([user_question])
    question_vector = question_vector.astype("float32")

    distances, positions = index.search(question_vector, results)

    matching_chunks = []

    for position in positions[0]:
        matching_chunks.append(lecture_chunks[position])

    return matching_chunks
