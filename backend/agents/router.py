import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def fallback_keyword_router(user_message: str) -> str:
    """
    Local keyword matching backup system.
    Runs instantly without API calls if your Gemini quota is exhausted.
    """
    msg = user_message.lower()
    
    if any(word in msg for word in ["charge", "billing", "pay", "invoice", "money", "fee", "card", "price"]):
        return "Billing"
    elif any(word in msg for word in ["login", "password", "account", "lock", "error", "bug", "app", "lag", "500"]):
        return "Technical"
    elif any(word in msg for word in ["stock", "item", "available", "product", "catalog", "size", "buy"]):
        return "Product"
    elif any(word in msg for word in ["worst", "manager", "terrible", "ruined", "bad service", "complain", "speak to"]):
        return "Complaint"
    else:
        return "Policy"

def detect_intent(user_message: str) -> str:
    prompt = f"""
    You are an expert routing assistant for a customer support network. 
    Analyze the user's message and classify it into EXACTLY ONE of these categories:
    
    - 'Billing': For issues about being charged twice, payments, invoices, fees, or pricing.
    - 'Technical': For issues about passwords, login errors, account lockouts, app bugs, or lag.
    - 'Product': For questions about stock availability, item features, sizes, or catalog specifications.
    - 'Complaint': For angry customers, poor service experiences, or demands to speak to a manager.
    - 'Policy': ONLY for general rules, terms of service, legal documentation guarantees, or shipping/return timeframes.

    User Message: {user_message}
    Output only the exact category name (e.g., Billing, Technical, Product, Complaint, Policy), nothing else. Do not use punctuation.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0
            )
        )
        category = response.text.strip().capitalize()
        return category

    except Exception as e:
        # If we hit a 429 Quota issue, print a clean warning and switch to the local rule parser
        print(f"⚠️ API Quota limit or connection issue encountered ({e}). Switching to local keyword router.")
        return fallback_keyword_router(user_message)

if __name__ == "__main__":
    test_queries = [
        "I was charged twice on my card yesterday, please give my money back!",
        "The login page keeps throwing a 500 server error when I input my email.",
        "Is this item available in stock right now?",
        "This is the worst customer service experience I have ever had. Let me speak to your manager."
    ]
    
    print("--- Testing Agent Router Classification ---")
    for query in test_queries:
        detected = detect_intent(query)
        print(f"Query: '{query}' \n➡️ Detected Intent: {detected}\n")