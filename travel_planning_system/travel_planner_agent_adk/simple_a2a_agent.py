"""
Simple A2A Travel Planner Agent
A minimal implementation focused on A2A protocol communication.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List
import httpx


class SimpleA2ATravelPlanner:
    """Simple A2A Travel Planner Agent that coordinates with other agents."""
    
    def __init__(self):
        self.agent_name = "Travel_Planner_Agent"
        self.hotel_agent_url = "http://localhost:10002"
        self.car_agent_url = "http://localhost:10003"
        self.log_file = "agent_communication_log.json"
        self.ensure_log_file()
    
    def ensure_log_file(self):
        """Ensure the log file exists with proper structure."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump({"communications": []}, f, indent=2)
    
    def log_agent_communication(self, session_id: str, agent_name: str, request: str, response: Dict[str, Any], status: str):
        """Log agent communication details."""
        try:
            # Read existing log
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            # Add new communication entry
            communication_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "agent_name": agent_name,
                "request": request,
                "response": response,
                "status": status
            }
            
            log_data["communications"].append(communication_entry)
            
            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error logging communication: {e}")
    
    def extract_destination(self, query: str) -> str:
        """Extract destination from user query."""
        # Simple destination extraction
        query_lower = query.lower()
        
        # Common destinations
        destinations = {
            "new york": "New York",
            "paris": "Paris", 
            "london": "London",
            "tokyo": "Tokyo",
            "bhubaneswar": "Bhubaneswar",
            "delhi": "New Delhi",
            "mumbai": "Mumbai",
            "bangalore": "Bangalore"
        }
        
        for key, value in destinations.items():
            if key in query_lower:
                return value
                
        # Default fallback
        return "Unknown Destination"
    
    async def check_agent_status(self) -> Dict[str, Any]:
        """Check status of other agents via A2A protocol."""
        status = {
            "hotel_agent": {"status": "unknown", "url": self.hotel_agent_url},
            "car_agent": {"status": "unknown", "url": self.car_agent_url}
        }
        
        # Check Hotel Agent
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.hotel_agent_url}/.well-known/agent.json", timeout=5.0)
                if response.status_code == 200:
                    status["hotel_agent"]["status"] = "active"
                    status["hotel_agent"]["info"] = response.json()
        except Exception as e:
            print(f"❌ Hotel Agent A2A check failed: {e}")
            
        # Check Car Agent  
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.car_agent_url}/.well-known/agent.json", timeout=5.0)
                if response.status_code == 200:
                    status["car_agent"]["status"] = "active"
                    status["car_agent"]["info"] = response.json()
        except Exception as e:
            print(f"❌ Car Agent A2A check failed: {e}")
            
        return status
    
    async def send_a2a_message(self, agent_url: str, message: str) -> Dict[str, Any]:
        """Send A2A message to another agent."""
        try:
            async with httpx.AsyncClient() as client:
                # Format message in proper A2A format with all required fields
                message_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                context_id = f"ctx_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                payload = {
                    "message": {
                        "role": "user",
                        "messageId": message_id,
                        "taskId": task_id,
                        "contextId": context_id,
                        "parts": [
                            {
                                "type": "text",
                                "text": message
                            }
                        ]
                    }
                }
                response = await client.post(f"{agent_url}/a2a/message", json=payload, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": f"A2A communication failed: {str(e)}"}
    
    async def stream(self, query: str, session_id: str):
        """Stream A2A response for travel planning."""
        destination = self.extract_destination(query)
        
        # Yield initial processing message
        yield {
            "is_task_complete": False,
            "updates": f"🤖 A2A Travel Planner: Processing request for {destination}..."
        }
        
        # Check agent status
        yield {
            "is_task_complete": False, 
            "updates": "🔍 Checking A2A agent status..."
        }
        
        agent_status = await self.check_agent_status()
        
        # Contact Hotel Agent
        yield {
            "is_task_complete": False,
            "updates": f"🏨 Contacting Hotel Agent via A2A for {destination}..."
        }
        
        hotel_message = f"Find budget-friendly hotels in {destination} for the requested dates"
        hotel_response = await self.send_a2a_message(self.hotel_agent_url, hotel_message)
        
        # Log hotel agent communication
        self.log_agent_communication(
            session_id=session_id,
            agent_name="Hotel_Booking_Agent",
            request=hotel_message,
            response=hotel_response,
            status="success" if "error" not in hotel_response else "error"
        )
        
        # Contact Car Agent
        yield {
            "is_task_complete": False,
            "updates": f"🚗 Contacting Car Rental Agent via A2A for {destination}..."
        }
        
        car_message = f"Find car rental options in {destination} for the requested dates"
        car_response = await self.send_a2a_message(self.car_agent_url, car_message)
        
        # Log car agent communication
        self.log_agent_communication(
            session_id=session_id,
            agent_name="Car_Rental_Agent",
            request=car_message,
            response=car_response,
            status="success" if "error" not in car_response else "error"
        )
        
        # Compile final response
        yield {
            "is_task_complete": False,
            "updates": "📋 Compiling A2A travel plan..."
        }
        
        # Extract content from agent responses
        hotel_content = ""
        car_content = ""
        
        if hotel_response and "error" not in hotel_response:
            if "result" in hotel_response and "content" in hotel_response["result"]:
                hotel_content = hotel_response["result"]["content"]
        
        if car_response and "error" not in car_response:
            if "result" in car_response and "content" in car_response["result"]:
                car_content = car_response["result"]["content"]
        
        # Create comprehensive response with extracted content
        response = f"""# A2A Travel Plan for {destination}

## 🎯 Destination: {destination}
**Query:** {query}
**Date:** {datetime.now().strftime("%Y-%m-%d")}

## 📋 Travel Recommendations

### 🏨 Hotel Recommendations
{hotel_content if hotel_content else "*Hotel agent communication failed or no content available*"}

### 🚗 Car Rental Options
{car_content if car_content else "*Car rental agent communication failed or no content available*"}

## 🔗 A2A Protocol Status
- ✅ Travel Planner Agent: Active
- {'✅' if agent_status['hotel_agent']['status'] == 'active' else '❌'} Hotel Agent: {agent_status['hotel_agent']['status']}
- {'✅' if agent_status['car_agent']['status'] == 'active' else '❌'} Car Agent: {agent_status['car_agent']['status']}

---
*This response was generated using A2A (Agent-to-Agent) protocol for multi-agent coordination.*
*Agent communication details have been logged to agent_communication_log.json*
"""
        
        # Final response
        yield {
            "is_task_complete": True,
            "content": response
        }


# Global instance
travel_planner = None

async def initialize_agent():
    """Initialize the A2A Travel Planner Agent."""
    global travel_planner
    if travel_planner is None:
        travel_planner = SimpleA2ATravelPlanner()
        print("✅ Simple A2A Travel Planner Agent initialized!")
    return travel_planner
