#!/usr/bin/env python3
"""
Simplified Car Rental Agent Executor
Uses the simple car agent without LangGraph dependencies.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from simple_car_agent import get_car_rental_agent

app = FastAPI(title="Car Rental Agent", version="1.0.0")

# Initialize the car rental agent
car_rental_agent = get_car_rental_agent()

class CarRentalRequest(BaseModel):
    """Request model for car rental."""
    message: str

@app.post("/chat")
async def chat(request: CarRentalRequest):
    """Handle car rental requests."""
    try:
        response = car_rental_agent.process_request(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Car_Rental_Agent"}

@app.get("/")
async def root():
    """Root endpoint with agent information."""
    return {
        "agent": "Car_Rental_Agent",
        "description": "Car rental agent using simplified implementation with Groq LLM",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        },
        "features": [
            "Car rental search using SerperAPI",
            "Car rental booking simulation",
            "Groq LLM for request processing",
            "No LangGraph dependencies"
        ]
    }

if __name__ == "__main__":
    print("🚗 Starting Simplified Car Rental Agent")
    print("📍 Server will be available at: http://localhost:10003")
    print("🔗 Health check: http://localhost:10003/health")
    print("💬 Chat endpoint: http://localhost:10003/chat")
    print("🧠 Using Groq LLM (no LangGraph dependencies)")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=10003)
