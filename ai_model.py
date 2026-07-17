import os
import time
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

def answer_question(question, lecture_chunks):

    contexts = []

    for count, chunk in enumerate(lecture_chunks, start=1):
          contexts.append(
        f"""Context [{count}]
        File: {chunk["filename"]}
        Page: {chunk["page"]}

        {chunk["text"]}
    """
    )
          
    lecture_notes = "\n\n".join(contexts)

    prompt = f"""
You are an AI study assistant.

Answer the student's question using ONLY the contexts below.

Every factual statement should include at least one citation.

Do not cite contexts that were not used.

Only use citation numbers that exist in the provided contexts.

Whenever you use information from a context, cite it using its context number like [1] or [2].

If multiple contexts support the same answer, you may cite multiple numbers like [1][3].

If the answer cannot be found in the provided contexts, say that the information is not available rather than making something up.

Contexts:

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
                
# ... inside your try block
                print(f"Success using {model_name}!")
                
                answer = response.text
                sources = "\n\nSources:\n"
                sources_added = False

                for number, chunk in enumerate(lecture_chunks, start=1):

                    if f"[{number}]" in answer:

                        sources += f"[{number}] {chunk['filename']} (Page {chunk['page']})\n"

                        sources_added = True

                if sources_added:
                    return answer + sources
                else:
                    return answer

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