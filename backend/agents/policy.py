import os
from rag.query import generate_support_response

def handle_policy(message: str) -> str:
    """
    Takes the user inquiry, queries the company policy document using RAG,
    and returns a precise, human-like answer.
    """
    try:
        # Call your beautiful RAG function directly
        response = generate_support_response(message)
        return response
        
    except Exception as e:
        # Fallback security layout text if something structural changes later
        return (
            "I'm having a little trouble reading our policy files right now. "
            f"However, I noted your question regarding: '{message}'. Let me double-check our system database."
        )