#!/usr/bin/env python3
"""
Simplified Hotel Booking Agent Executor
Uses the simple hotel agent without CrewAI dependencies.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from simple_hotel_agent import get_hotel_booking_agent

app = FastAPI(title="Hotel Booking Agent", version="1.0.0")

# Initialize the hotel booking agent
hotel_booking_agent = get_hotel_booking_agent()

class HotelBookingRequest(BaseModel):
    """Request model for hotel booking."""
    message: str

@app.post("/chat")
async def chat(request: HotelBookingRequest):
    """Handle hotel booking requests."""
    try:
        response = hotel_booking_agent.process_request(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Hotel_Booking_Agent"}

@app.get("/")
async def root():
    """Root endpoint with agent information."""
    return {
        "agent": "Hotel_Booking_Agent",
        "description": "Hotel booking agent using simplified implementation with Groq LLM",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        },
        "features": [
            "Hotel search using SerperAPI",
            "Hotel booking simulation",
            "Groq LLM for request processing",
            "No CrewAI dependencies"
        ]
    }

if __name__ == "__main__":
    print("🏨 Starting Simplified Hotel Booking Agent")
    print("📍 Server will be available at: http://localhost:10002")
    print("🔗 Health check: http://localhost:10002/health")
    print("💬 Chat endpoint: http://localhost:10002/chat")
    print("🧠 Using Groq LLM (no CrewAI dependencies)")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=10002)
