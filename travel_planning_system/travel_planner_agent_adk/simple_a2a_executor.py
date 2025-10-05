"""
Simple A2A Travel Planner Executor
A minimal FastAPI server that implements pure A2A protocol communication.
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from simple_a2a_agent import SimpleA2ATravelPlanner, initialize_agent

# Global agent instance
travel_planner = None

class TravelRequest(BaseModel):
    message: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    # Startup
    global travel_planner
    travel_planner = await initialize_agent()
    print("🚀 Simple A2A Travel Planner Agent Started")
    print("📍 Server will be available at: http://localhost:10001")
    print("🔗 Health check: http://localhost:10001/health")
    print("📋 Plan endpoint: http://localhost:10001/plan")
    print("🤖 Using Pure A2A Protocol")
    print("=" * 60)
    yield
    # Shutdown (if needed)

app = FastAPI(title="Simple A2A Travel Planner Agent", version="1.0.0", lifespan=lifespan)

@app.post("/plan")
async def plan_trip(request: TravelRequest):
    """Plan a trip using pure A2A protocol coordination."""
    try:
        if travel_planner is None:
            raise HTTPException(status_code=500, detail="Agent not initialized")
        
        print(f"🤖 A2A Travel Planner received: {request.message}")
        
        # Use A2A protocol for agent coordination
        session_id = "a2a_session"
        response_parts = []
        
        async for chunk in travel_planner.stream(request.message, session_id):
            if chunk.get("is_task_complete"):
                content = chunk.get("content", "")
                if content:
                    response_parts.append(content)
                    print(f"✅ A2A Final response: {content[:100]}...")
            else:
                updates = chunk.get("updates", "")
                if updates:
                    print(f"🔄 A2A Processing: {updates}")
        
        # Combine all response parts
        full_response = "".join(response_parts)
        return {"plan": full_response}
        
    except Exception as e:
        print(f"❌ A2A Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"A2A Error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "agent": "Simple_A2A_Travel_Planner",
        "protocol": "A2A",
        "initialized": travel_planner is not None
    }

@app.get("/agents/status")
async def check_agents():
    """Check status of other agents via A2A protocol."""
    if travel_planner is None:
        return {"error": "Agent not initialized"}
    
    try:
        status = await travel_planner.check_agent_status()
        return {
            "a2a_protocol": True,
            "agents": status
        }
    except Exception as e:
        return {"error": f"A2A status check failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10001)
