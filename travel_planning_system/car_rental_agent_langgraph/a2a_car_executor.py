#!/usr/bin/env python3
"""
Car Rental Agent with A2A Protocol Support
Implements both HTTP REST API and A2A protocol endpoints.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uvicorn
import json
import uuid
from datetime import datetime
from simple_car_agent import get_car_rental_agent

app = FastAPI(title="Car Rental Agent with A2A", version="2.0.0")

# Initialize the car rental agent
car_rental_agent = get_car_rental_agent()

# A2A Protocol Models
class A2AMessagePart(BaseModel):
    type: str = "text"
    text: str

class A2AMessage(BaseModel):
    role: str
    parts: List[A2AMessagePart]
    messageId: str
    taskId: str
    contextId: str

class A2AMessageRequest(BaseModel):
    message: A2AMessage

class A2AMessageResponse(BaseModel):
    id: str
    result: Dict[str, Any]
    status: str = "success"

class A2AAgentCard(BaseModel):
    name: str
    description: str
    capabilities: Dict[str, Any]
    defaultInputModes: List[str]
    defaultOutputModes: List[str]
    skills: List[str]
    url: str
    version: str
    status: str = "active"

# HTTP REST API Models
class CarRentalRequest(BaseModel):
    message: str

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """A2A Protocol: Agent Card Discovery endpoint."""
    return A2AAgentCard(
        name="Car Rental Agent",
        description="Specialized agent for car rental search and booking using SerperAPI and Groq LLM",
        capabilities={
            "car_rental_search": "Search for car rentals using SerperAPI",
            "car_booking": "Book car rental reservations",
            "price_comparison": "Compare car rental prices",
            "car_recommendations": "Provide car rental recommendations",
            "vehicle_type_analysis": "Analyze vehicle type requirements"
        },
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        skills=["car_rental_search", "car_booking", "price_comparison"],
        url="http://localhost:10003",
        version="2.0.0"
    )

@app.post("/a2a/message")
async def a2a_message(request: A2AMessageRequest):
    """A2A Protocol: Message exchange endpoint."""
    try:
        # Extract the message text from A2A format
        message_text = ""
        for part in request.message.parts:
            if part.type == "text":
                message_text += part.text + " "
        
        message_text = message_text.strip()
        
        # Process the message using the car rental agent
        response = car_rental_agent.process_request(message_text)
        
        # Format response in A2A format
        a2a_response = A2AMessageResponse(
            id=request.message.messageId,
            result={
                "type": "text",
                "content": response,
                "metadata": {
                    "agent": "car_rental_agent",
                    "timestamp": datetime.now().isoformat(),
                    "capabilities_used": ["car_rental_search", "llm_processing"]
                }
            }
        )
        
        return a2a_response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"A2A message processing error: {str(e)}"
        )

@app.post("/chat")
async def chat(request: CarRentalRequest):
    """HTTP REST API: Handle car rental requests."""
    try:
        response = car_rental_agent.process_request(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "agent": "Car_Rental_Agent",
        "protocol": "A2A + HTTP REST",
        "capabilities": [
            "car_rental_search",
            "car_booking",
            "price_comparison", 
            "car_recommendations"
        ]
    }

@app.get("/")
async def root():
    """Root endpoint with agent information."""
    return {
        "agent": "Car_Rental_Agent",
        "description": "Car rental agent with A2A protocol support using Groq LLM",
        "version": "2.0.0",
        "protocols": ["A2A", "HTTP REST"],
        "endpoints": {
            "agent_card": "/.well-known/agent.json",
            "a2a_message": "/a2a/message",
            "chat": "/chat",
            "health": "/health"
        },
        "capabilities": [
            "car_rental_search",
            "car_booking",
            "price_comparison", 
            "car_recommendations",
            "vehicle_type_analysis"
        ],
        "features": [
            "A2A protocol compliance",
            "HTTP REST API compatibility",
            "SerperAPI integration",
            "Groq LLM processing",
            "Structured logging"
        ]
    }

if __name__ == "__main__":
    print("🚗 Starting Car Rental Agent with A2A Protocol")
    print("📍 Server will be available at: http://localhost:10003")
    print("🔗 Health check: http://localhost:10003/health")
    print("💬 Chat endpoint: http://localhost:10003/chat")
    print("🤖 A2A Agent Card: http://localhost:10003/.well-known/agent.json")
    print("📨 A2A Message: http://localhost:10003/a2a/message")
    print("🧠 Using Groq LLM with SerperAPI")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=10003)
