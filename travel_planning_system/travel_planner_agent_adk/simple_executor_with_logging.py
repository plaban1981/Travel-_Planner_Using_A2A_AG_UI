#!/usr/bin/env python3
"""
Simplified Travel Planner Agent Executor with comprehensive logging.
Uses the sophisticated agent with A2A protocol and fallback to simple implementation.
"""

import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from travel_planner.agent import TravelPlannerAgent # Import sophisticated agent
from simple_travel_planner import SimpleTravelPlanner # Import simple fallback
from logging_config import get_logger, TraceContext, trace_llm_call, trace_agent_communication

app = FastAPI(title="Travel Planner Agent", version="1.0.0")

# Initialize logger
logger = get_logger("travel_planner")

travel_planner = None

async def initialize_agent():
    """Initialize the travel planner agent with logging."""
    global travel_planner
    
    if travel_planner is None:
        logger.info("Initializing Travel Planner Agent with A2A protocol")
        
        agent_urls = [
            "http://localhost:10002",  # Hotel Booking Agent
            "http://localhost:10003",  # Car Rental Agent
        ]
        
        try:
            with TraceContext(logger, "agent_initialization", {"agent_urls": agent_urls}):
                travel_planner = await TravelPlannerAgent.create(
                    remote_agent_addresses=agent_urls
                )
                logger.info("Travel Planner Agent initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            logger.info("Falling back to simple implementation")
            from simple_travel_planner import SimpleTravelPlanner
            travel_planner = SimpleTravelPlanner()
            logger.info("Fallback to simple implementation completed")

class TravelRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    """Startup event with logging."""
    logger.info("Starting Travel Planner Agent server")
    await initialize_agent()

@app.post("/plan")
async def plan_trip(request: TravelRequest):
    """Plan a trip with comprehensive logging."""
    start_time = time.time()
    
    logger.info(f"Received trip planning request: {request.message[:100]}...")
    
    try:
        if travel_planner is None:
            logger.warning("Agent not initialized, attempting to initialize")
            await initialize_agent()
        
        if hasattr(travel_planner, 'stream'): # Check if it's the sophisticated agent
            logger.info("Using sophisticated agent with A2A protocol")
            
            session_id = "travel_session"
            response_parts = []
            
            with TraceContext(logger, "sophisticated_agent_planning", {
                "message": request.message,
                "session_id": session_id
            }):
                async for chunk in travel_planner.stream(request.message, session_id):
                    if chunk.get("type") == "text":
                        response_parts.append(chunk.get("text", ""))
                        logger.info(f"Received text chunk: {chunk.get('text', '')[:50]}...")
                    elif chunk.get("type") == "tool_call":
                        logger.info(f"Tool call: {chunk.get('tool_name', 'unknown')}")
                    elif chunk.get("type") == "tool_result":
                        logger.info(f"Tool result: {chunk.get('result', '')[:100]}...")
                
                full_response = "".join(response_parts)
                
                # Trace the LLM call
                duration = time.time() - start_time
                trace_llm_call(logger, "groq/llama-3.3-70b-versatile", request.message, full_response, duration)
                
                return {"plan": full_response}
        else: # Fallback to simple implementation
            logger.info("Using simple agent implementation")
            
            with TraceContext(logger, "simple_agent_planning", {
                "message": request.message
            }):
                plan = travel_planner.plan_trip(request.message)
                
                # Trace the LLM call
                duration = time.time() - start_time
                trace_llm_call(logger, "groq/llama-3.3-70b-versatile", request.message, plan, duration)
                
                return {"plan": plan}
                
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error in plan_trip: {str(e)}")
        logger.error_trace("plan_trip_error", str(e), {
            "message": request.message,
            "duration": duration
        })
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint with logging."""
    logger.info("Health check requested")
    
    agent_type = "A2A Protocol" if hasattr(travel_planner, 'stream') else "Simple HTTP"
    
    return {
        "status": "healthy", 
        "agent": "Travel_Planner_Agent",
        "type": agent_type,
        "initialized": travel_planner is not None
    }

@app.get("/agents/status")
async def check_agents():
    """Check agent status with logging."""
    logger.info("Agent status check requested")
    
    if travel_planner is None:
        logger.warning("Agent not initialized")
        return {"error": "Agent not initialized"}
    
    if hasattr(travel_planner, 'check_agent_status'): # Simple implementation
        logger.info("Checking simple agent status")
        status = travel_planner.check_agent_status()
        return {"agents": status}
    else: # Sophisticated agent
        logger.info("Using A2A protocol agents")
        return {
            "agents": "A2A protocol agents",
            "hotel_agent": "Connected via A2A",
            "car_rental_agent": "Connected via A2A"
        }

@app.get("/")
async def root():
    """Root endpoint with agent information."""
    agent_type = "A2A Protocol" if hasattr(travel_planner, 'stream') else "Simple HTTP"
    
    logger.info("Root endpoint accessed")
    
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
            "hotel_booking": "http://localhost:10002",
            "car_rental": "http://localhost:10003"
        },
        "features": [
            "Enhanced destination extraction",
            "A2A protocol communication",
            "Fallback to simple HTTP if A2A fails",
            "Real-time agent coordination",
            "Comprehensive logging and tracing"
        ]
    }

if __name__ == "__main__":
    logger.info("Starting Travel Planner Agent with comprehensive logging")
    print("✈️ Starting Travel Planner Agent")
    print("📍 Server will be available at: http://localhost:10001")
    print("🔗 Health check: http://localhost:10001/health")
    print("📋 Plan endpoint: http://localhost:10001/plan")
    print("🧠 Using A2A protocol with Groq LLM")
    print("🔄 Fallback to simple HTTP if A2A fails")
    print("📊 Comprehensive logging enabled")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=10001)
