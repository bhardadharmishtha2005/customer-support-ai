import os
import json
import math
import time
from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DB_FAISS_PATH = "vectorstore/mock_db.json"

def get_google_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if not norm_a or not norm_b:
        return 0.0
    return dot_product / (norm_a * norm_b)

def retrieve_relevant_context(query, top_k=1):
    if not os.path.exists(DB_FAISS_PATH):
        print(f"Error: Vector store file not found at {DB_FAISS_PATH}.")
        return None

    with open(DB_FAISS_PATH, "r", encoding="utf-8") as f:
        database = json.load(f)

    query_vector = get_google_embedding(query)

    scored_chunks = []
    for item in database:
        score = cosine_similarity(query_vector, item["embedding"])
        scored_chunks.append((score, item["text"]))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return scored_chunks[:top_k]

def generate_support_response(user_query):
    """Retrieves context and uses Gemini to answer, safely catching 429 string messages."""
    matches = retrieve_relevant_context(user_query, top_k=1)
    if not matches:
        return "System Error: No knowledge base data available."
    
    context_text = matches[0][1]
    
    prompt = f"""
You are a helpful and professional customer support AI assistant. 
Answer the customer's question politely and accurately using ONLY the provided company policy text below. 
If the information is not in the policy text, politely inform the customer that you cannot assist with that specific request.

Company Policy Context:
{context_text}

Customer Question:
{user_query}

AI Assistant Response:
"""

    max_retries = 3
    wait_time = 60  # Increased to 60 seconds to completely clear out the free-tier quota window

    for attempt in range(max_retries):
        try:
            # Switched to the current active stable flash model
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            return response.text
        except ClientError as e:
            error_msg = str(e).lower()
            # Safely check the string contents of the ClientError
            if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                print(f"⚠️ Rate limit hit (Attempt {attempt + 1}/{max_retries}).")
                print(f"Waiting {wait_time} seconds to let your Gemini free tier reset...")
                time.sleep(wait_time)
            else:
                raise e

    return "Error: The AI assistant is receiving too much traffic. Please run the script again in a minute."

if __name__ == "__main__":
    test_query = "Hi, I bought something a couple of weeks ago but it arrived broken. Can I get my money back?"
    print(f"Customer Question: '{test_query}'\n")
    
    print("Processing RAG Response...")
    ai_reply = generate_support_response(test_query)
    
    print("\n================ AI Support Reply ================")
    print(ai_reply)
    print("==================================================")