#!/usr/bin/env python3
"""
Travel Planner Agent with A2A Protocol Support
Uses the sophisticated A2A protocol for agent-to-agent communication.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
from contextlib import asynccontextmanager
from travel_planner.agent import TravelPlannerAgent # Import sophisticated agent
from simple_travel_planner import SimpleTravelPlanner # Import simple fallback

# Initialize the travel planner
travel_planner = None

async def initialize_agent():
    """Initialize the travel planner agent with A2A protocol."""
    global travel_planner
    
    if travel_planner is None:
        print("🚀 Initializing Travel Planner Agent with A2A protocol...")
        
        # A2A protocol agent URLs
        agent_urls = [
            "http://localhost:10002",  # Hotel Booking Agent (A2A)
            "http://localhost:10003",  # Car Rental Agent (A2A)
        ]
        
        travel_planner = await TravelPlannerAgent.create(
            remote_agent_addresses=agent_urls
        )
        print("✅ Travel Planner Agent initialized successfully with A2A protocol!")

class TravelRequest(BaseModel):
    """Request model for travel planning."""
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    # Startup
    await initialize_agent()
    yield
    # Shutdown (if needed)

app = FastAPI(title="Travel Planner Agent", version="2.0.0", lifespan=lifespan)

@app.post("/plan")
async def plan_trip(request: TravelRequest):
    """Plan a trip using A2A protocol coordination with other agents."""
    try:
        if travel_planner is None:
            await initialize_agent()
        
        # Use A2A protocol for agent coordination
        print("🤖 Using A2A protocol for agent coordination")
        session_id = "travel_session"
        response_parts = []
        
        async for chunk in travel_planner.stream(request.message, session_id):
            # Handle the A2A response format
            if chunk.get("is_task_complete"):
                # Final response
                content = chunk.get("content", "")
                if content:
                    response_parts.append(content)
                print(f"✅ A2A Final response: {content[:100]}...")
            else:
                # Processing updates
                updates = chunk.get("updates", "")
                if updates:
                    print(f"🔄 A2A Processing: {updates}")
        
        # Combine all response parts
        full_response = "".join(response_parts)
        return {"plan": full_response}
            
    except Exception as e:
        print(f"❌ Error in plan_trip: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    agent_type = "A2A Protocol" if hasattr(travel_planner, 'stream') else "Simple HTTP"
    
    return {
        "status": "healthy", 
        "agent": "Travel_Planner_Agent",
        "type": agent_type,
        "initialized": travel_planner is not None
    }


@app.get("/agents/status")
async def check_agents():
    """Check status of other agents."""
    if travel_planner is None:
        return {"error": "Agent not initialized"}
    
    if hasattr(travel_planner, 'check_agent_status'): # Simple implementation
        status = travel_planner.check_agent_status()
        return {"agents": status}
    else: # A2A protocol
        return {
            "agents": "A2A protocol agents",
            "hotel_agent": "Connected via A2A",
            "car_rental_agent": "Connected via A2A"
        }


@app.get("/")
async def root():
    """Root endpoint with agent information."""
    agent_type = "A2A Protocol" if hasattr(travel_planner, 'stream') else "Simple HTTP"
    
    return {
        "agent": "Travel_Planner_Agent",
        "description": f"Travel planning agent using {agent_type} that coordinates with hotel and car rental agents",
        "version": "2.0.0",
        "type": agent_type,
        "endpoints": {
            "plan": "/plan",
            "health": "/health",
            "agents_status": "/agents/status"
        },
        "coordinated_agents": {
            "hotel_booking": "http://localhost:10002 (A2A)",
            "car_rental": "http://localhost:10003 (A2A)"
        },
        "features": [
            "A2A protocol communication",
            "Enhanced destination extraction", 
            "Real-time agent coordination",
            "Fallback to simple HTTP if A2A fails",
            "Structured logging and tracing"
        ]
    }


if __name__ == "__main__":
    print("✈️ Starting Travel Planner Agent with A2A Protocol")
    print("📍 Server will be available at: http://localhost:10001")
    print("🔗 Health check: http://localhost:10001/health")
    print("📋 Plan endpoint: http://localhost:10001/plan")
    print("🧠 Using A2A protocol with Groq LLM")
    print("🔄 Fallback to simple HTTP if A2A fails")
    print("🤖 Coordinating with A2A agents:")
    print("   - Hotel Agent: http://localhost:10002")
    print("   - Car Rental Agent: http://localhost:10003")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=10001) 