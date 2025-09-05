"""
FastAPI server for CrewAI Editorial Assistant
REST API interface for the real CrewAI implementation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.application.use_cases.real_crewai_editorial_assistant import RealCrewAIEditorialAssistant

app = FastAPI(title="CrewAI Editorial Assistant API", version="1.0.0")

# Initialize the assistant
assistant = RealCrewAIEditorialAssistant()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
async def root():
    """API status endpoint"""
    return {
        "message": "CrewAI Editorial Assistant API", 
        "status": "running",
        "features": [
            "Real CrewAI agents and tasks",
            "Book details and store locations", 
            "Customer support tickets",
            "Session context management"
        ]
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with CrewAI processing"""
    try:
        # Get or create session
        session_id = assistant.get_session_id(request.session_id)
        
        # Process with real CrewAI
        response = assistant.process(request.message, session_id)
        
        return ChatResponse(response=response, session_id=session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "assistant": "ready"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
