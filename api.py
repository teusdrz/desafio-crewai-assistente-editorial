"""
FastAPI Web Interface for the Editorial Assistant
"""

import sys
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.editorial_assistant import EditorialAssistant
from src.config import get_logger


# Pydantic models for API requests
class ChatRequest(BaseModel):
    message: str


class TicketRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str


class ChatResponse(BaseModel):
    response: str
    intent: str = None


# Initialize FastAPI app
app = FastAPI(
    title="Elo Editorial Assistant API",
    description="A multiagent editorial assistant built with CrewAI and Gemini",
    version="1.0.0"
)

# Global assistant instance
assistant: EditorialAssistant = None
logger = get_logger(__name__)


@app.on_event("startup")
async def startup_event():
    """Initialize the Editorial Assistant on startup"""
    global assistant
    try:
        logger.info("Initializing Editorial Assistant API...")
        assistant = EditorialAssistant()
        logger.info("Editorial Assistant API ready!")
    except Exception as e:
        logger.error(f"Failed to initialize Editorial Assistant: {str(e)}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Elo Editorial Group Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat - Send a message to the assistant",
            "ticket": "/ticket - Create a support ticket",
            "health": "/health - Check API health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "assistant_ready": assistant is not None
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the editorial assistant
    
    Args:
        request: ChatRequest with user message
        
    Returns:
        ChatResponse with assistant's response
    """
    if not assistant:
        raise HTTPException(status_code=503, detail="Assistant not initialized")
    
    try:
        # Detect intent for logging/analytics
        intent_data = assistant.detect_intent(request.message)
        intent = intent_data.get("intent", "unknown")
        
        # Process the request
        response = assistant.process_request(request.message)
        
        return ChatResponse(
            response=response,
            intent=intent
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing request")


@app.post("/ticket")
async def create_ticket(request: TicketRequest) -> Dict[str, Any]:
    """
    Create a support ticket
    
    Args:
        request: TicketRequest with ticket details
        
    Returns:
        Ticket creation confirmation
    """
    if not assistant:
        raise HTTPException(status_code=503, detail="Assistant not initialized")
    
    try:
        response = assistant.create_support_ticket(
            name=request.name,
            email=request.email,
            subject=request.subject,
            message=request.message
        )
        
        return {
            "success": True,
            "message": response
        }
        
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating ticket")


@app.get("/books")
async def list_books():
    """
    Get a list of available books (for reference)
    """
    try:
        import json
        catalog_path = os.path.join(os.path.dirname(__file__), "data", "mock_catalog.json")
        
        with open(catalog_path, 'r', encoding='utf-8') as file:
            catalog_data = json.load(file)
        
        books = [
            {
                "title": book["title"],
                "author": book["author"],
                "imprint": book["imprint"],
                "release_date": book["release_date"]
            }
            for book in catalog_data["books"]
        ]
        
        return {
            "total_books": len(books),
            "books": books
        }
        
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching books")


def run_api(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the FastAPI server
    
    Args:
        host: Host to bind to
        port: Port to bind to
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_api()
