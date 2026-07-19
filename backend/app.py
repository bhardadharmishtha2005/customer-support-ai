import os
import json
import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from rag.query import generate_support_response

# Configure Logging for a professional audit trail
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CustomerSupportAPI")

app = FastAPI(
    title="Multi-Agent AI Customer Support Assistant API",
    description="Production-grade RAG and Multi-Agent system handling automated policy queries and ticket routing.",
    version="1.0.0"
)

# --- Pydantic Schemas for Strict Request/Response Data Validation ---
class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender ('user' or 'assistant')")
    content: str = Field(..., description="The text content of the message")

class SupportRequest(BaseModel):
    question: str = Field(..., examples=["Hi, I bought something a couple of weeks ago but it arrived broken. Can I get my money back?"])
    history: List[ChatMessage] = Field(default=[], description="Previous conversation history for memory simulation")

class SupportResponse(BaseModel):
    status: str = Field(..., description="Success or failure status")
    active_agent: str = Field(..., description="The specific specialized agent assigned to this task")
    reply: str = Field(..., description="The generated response from the agent/RAG pipeline")
    error_details: Optional[str] = None

# --- Intent Router Logic ---
def route_intent(question: str) -> str:
    """Simulates the router.py behavior to classify which specialized agent handles the work."""
    q_low = question.lower()
    if any(word in q_low for word in ["charge", "invoice", "money", "refund", "billing", "payment", "paid"]):
        return "Billing Agent"
    elif any(word in q_low for word in ["broken", "damaged", "error", "wifi", "app", "login", "technical", "fail"]):
        return "Technical Support Agent"
    elif any(word in q_low for word in ["complaint", "worst", "terrible", "bad service", "angry"]):
        return "Complaint Escalation Agent"
    else:
        return "General FAQ/Policy Agent"

# --- API Endpoints ---
@app.post(
    "/api/v1/chat", 
    response_model=SupportResponse, 
    status_code=status.HTTP_200_OK,
    summary="Process customer queries through the Multi-Agent RAG pipeline"
)
async def process_customer_query(request: SupportRequest):
    # 1. Edge Case: Empty Request Validation
    if not request.question.strip():
        logger.warning("Received an empty question string.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="The customer question cannot be empty or whitespace only."
        )
    
    # 2. Intent Routing Identification
    assigned_agent = route_intent(request.question)
    logger.info(f"Routing query to: [{assigned_agent}]")

    try:
        # 3. Core RAG Execution Loop
        ai_reply = generate_support_response(request.question)
        
        # 4. Success Response Generation
        return SupportResponse(
            status="success",
            active_agent=assigned_agent,
            reply=ai_reply
        )

    except Exception as e:
        # 5. Global Fail-Safe Error Handling
        logger.error(f"Error encountered during RAG generation: {str(e)}")
        return SupportResponse(
            status="failed",
            active_agent=assigned_agent,
            reply="We are currently experiencing technical difficulties handling this request. Our systems are working to restore balance.",
            error_details=str(e)
        )

@app.get("/health", summary="API Infrastructure Health Check")
async def health_check():
    return {"status": "healthy", "engine": "Gemini RAG Matrix Active"}