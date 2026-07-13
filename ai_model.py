import os
import time
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

def answer_question(question, lecture_chunks):
    lecture_notes = "\n\n".join(lecture_chunks)

    prompt = f"""
You are an AI study assistant.

Answer the student's question using ONLY the lecture notes below.

If the lecture notes do not contain enough information to answer the question, say so instead of making something up.

Lecture Notes:
{lecture_notes}

Student Question:
{question}
"""

    models_to_try = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]
    max_retries_per_model = 3

    for model_name in models_to_try:
        wait_time = 2  
        
        for attempt in range(max_retries_per_model):
            try:
                print(f"Attempting to call {model_name} (Attempt {attempt + 1}/{max_retries_per_model})...")
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                print(f"Success using {model_name}!")
                return response.text

            except Exception as error:
                error_str = str(error)
                
                if "503" in error_str or "UNAVAILABLE" in error_str or "busy" in error_str.lower():
                    print(f"503 Error on {model_name}. Server overloaded. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    wait_time *= 2  
                else:

                    print(f"Different error encountered: {error}")
                    return f"An error occurred: {error}"

    return "Sorry, all available free Gemini models are currently experiencing high demand. Please try again in a few moments."