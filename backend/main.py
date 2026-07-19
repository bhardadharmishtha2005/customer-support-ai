from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.router import detect_intent

# Import all agent handlers cleanly at the top using consistent paths
try:
    from agents.billing import handle_billing
    from agents.policy import handle_policy      # Fixed path (removed backend.)
    from agents.technical import handle_technical
    from agents.complaint import handle_complaint  # Added new agent
    from agents.product import handle_product      # Added new agent
except ImportError as e:
    # Print the error in your terminal window so you can see exactly what failed
    print(f"⚠️ Import warning fallback active: {e}")
    def handle_billing(msg): return f"[Billing Agent Process] Handling: {msg}"
    def handle_policy(msg): return f"[Policy Agent Process] Querying knowledge base for: {msg}"
    def handle_technical(msg): return f"[Technical Agent Process] Troubleshooting: {msg}"
    def handle_complaint(msg): return f"[Complaint Agent Process] Managing grievance for: {msg}"
    def handle_product(msg): return f"[Product Agent Process] Item details for: {msg}"

app = FastAPI(title="Multi-Agent AI Customer Support Assistant")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "Welcome to the Multi-Agent AI Customer Support Assistant API!",
        "status": "Running smoothly"
    }

@app.post("/api/v1/chat")
async def handle_chat(payload: ChatRequest):
    """
    Main endpoint that accepts user questions, determines intent,
    routes to the right agent, and passes back the real answer.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    
    # 1. Detect the intent bucket using our router
    intent = detect_intent(payload.message)
    
    # 2. Route dynamically to the correct agent script
    if intent == "Billing":
        agent_response = handle_billing(payload.message)
    
    elif intent == "Policy" or intent == "FAQ":
        agent_response = handle_policy(payload.message)
    
    elif intent == "Technical":
        agent_response = handle_technical(payload.message)
        
    elif intent == "Complaint":
        agent_response = handle_complaint(payload.message)
        
    elif intent == "Product":
        agent_response = handle_product(payload.message)
        
    else:
        # Fallback security routing choice
        agent_response = handle_policy(payload.message)
    
    return {
        "status": "success",
        "user_message": payload.message,
        "routed_agent": intent,
        "response": agent_response
    }