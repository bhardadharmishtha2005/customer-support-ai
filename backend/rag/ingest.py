import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize the official client using your environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

KB_DIR = "../knowledge_base"
DB_FAISS_PATH = "vectorstore/mock_db.json"  

def get_google_embedding(text):
    # Using the universally supported active model identifier
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

def build_vector_db():
    policy_file = os.path.join(KB_DIR, "company_policy.txt")
    if not os.path.exists(policy_file):
        print("Error: company_policy.txt not found.")
        return

    with open(policy_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    chunks = [chunk.strip() for chunk in text_content.split("\n\n") if chunk.strip()]
    print(f"Loaded {len(chunks)} chunks from policy file.")

    database = []
    print("Generating embeddings via official Google GenAI SDK...")
    for chunk in chunks:
        vector = get_google_embedding(chunk)
        database.append({"text": chunk, "embedding": vector})

    os.makedirs("vectorstore", exist_ok=True)
    with open(DB_FAISS_PATH, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4)
        
    print(f"Success! Data saved locally at: {DB_FAISS_PATH}")

if __name__ == "__main__":
    build_vector_db()