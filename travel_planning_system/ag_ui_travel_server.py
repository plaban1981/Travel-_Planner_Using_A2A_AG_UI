"""
AG-UI (Agent User Interface) Server for Travel Planner Multi-Agent System.
Provides a user-friendly interface for interacting with the travel planning agents.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

from ag_ui_config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class TravelRequest(BaseModel):
    destination: str
    check_in: str
    check_out: str
    budget: str = "any"
    guests: int = 2
    car_needed: bool = True
    preferences: Optional[str] = None

class UserResponse(BaseModel):
    request_id: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float
    timestamp: datetime

class AgentStatus(BaseModel):
    agent_id: str
    status: str
    capabilities: List[str]
    last_activity: datetime

class SystemStatus(BaseModel):
    travel_planner: str
    hotel_agent: str
    car_rental_agent: str
    agents: List[AgentStatus]
    total_requests: int
    active_connections: int

# AG-UI Travel Server class
class AGUITravelServer:
    def __init__(self):
        self.app = FastAPI(title="AG-UI Travel Planner Server", version="1.0.0")
        self.setup_middleware()
        self.setup_routes()
        
        # Connection management
        self.connected_clients: List[WebSocket] = []
        self.active_requests: Dict[str, TravelRequest] = {}
        self.request_history: List[UserResponse] = []
        
        # Statistics
        self.total_requests = 0
        self.successful_requests = 0
    
    def setup_middleware(self):
        """Setup CORS middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def root(request: Request):
            """Serve the main travel planning UI."""
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Multi-Agent Travel Planning System</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                    .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .header { text-align: center; margin-bottom: 30px; }
                    .header h1 { color: #333; margin-bottom: 10px; }
                    .header p { color: #666; }
                    .form-section { margin-bottom: 30px; }
                    .form-group { margin-bottom: 15px; }
                    .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
                    .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
                    .form-group textarea { height: 100px; resize: vertical; }
                    .form-row { display: flex; gap: 15px; }
                    .form-row .form-group { flex: 1; }
                    .btn { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                    .btn:hover { background-color: #0056b3; }
                    .btn:disabled { background-color: #ccc; cursor: not-allowed; }
                    .response-section { margin-top: 30px; }
                    .response-box { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin-top: 10px; }
                    .status-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
                    .status-online { background-color: #28a745; }
                    .status-offline { background-color: #dc3545; }
                    .status-processing { background-color: #ffc107; }
                    .agent-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
                    .agent-card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; }
                    .agent-card h3 { margin: 0 0 10px 0; color: #333; }
                    .agent-card p { margin: 5px 0; color: #666; }
                    .loading { text-align: center; padding: 20px; }
                    .error { color: #dc3545; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 10px; margin-top: 10px; }
                    .success { color: #155724; background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; padding: 10px; margin-top: 10px; }
                    .travel-plan { background: #e3f2fd; border: 1px solid #bbdefb; border-radius: 5px; padding: 15px; margin-top: 10px; }
                    .hotel-option, .car-option { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 10px; margin: 5px 0; }
                    .option-name { font-weight: bold; color: #333; }
                    .option-price { color: #28a745; font-weight: bold; }
                    .option-link { color: #007bff; text-decoration: none; }
                    .option-link:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>✈️ Multi-Agent Travel Planning System</h1>
                        <p>Plan your perfect trip with AI-powered travel agents</p>
                    </div>
                    
                    <div class="form-section">
                        <h3>📋 Plan Your Trip</h3>
                        <form id="travelForm">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="destination">Destination:</label>
                                    <input type="text" id="destination" placeholder="e.g., Paris, Tokyo, New York" required>
                                </div>
                                <div class="form-group">
                                    <label for="budget">Budget Range:</label>
                                    <select id="budget">
                                        <option value="any">Any Budget</option>
                                        <option value="budget">Budget</option>
                                        <option value="mid-range">Mid-Range</option>
                                        <option value="luxury">Luxury</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="checkIn">Check-in Date:</label>
                                    <input type="date" id="checkIn" required>
                                </div>
                                <div class="form-group">
                                    <label for="checkOut">Check-out Date:</label>
                                    <input type="date" id="checkOut" required>
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="guests">Number of Guests:</label>
                                    <input type="number" id="guests" min="1" max="10" value="2" required>
                                </div>
                                <div class="form-group">
                                    <label for="carNeeded">Need Car Rental:</label>
                                    <select id="carNeeded">
                                        <option value="true">Yes</option>
                                        <option value="false">No</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label for="preferences">Special Preferences:</label>
                                <textarea id="preferences" placeholder="e.g., Near city center, family-friendly, accessible rooms, etc."></textarea>
                            </div>
                            
                            <button type="submit" class="btn">🚀 Plan My Trip</button>
                        </form>
                    </div>
                    
                    <div class="response-section">
                        <h3>📋 Your Travel Plan</h3>
                        <div id="responseBox" class="response-box" style="display: none;">
                            <div id="responseContent"></div>
                        </div>
                    </div>
                    
                    <div class="agent-status">
                        <h3>🤖 Agent Status</h3>
                        <div id="agentStatus" class="agent-grid">
                            <div class="loading">Loading agent status...</div>
                        </div>
                    </div>
                </div>
                
                <script>
                    let ws = null;
                    let currentRequestId = null;
                    
                    // Initialize WebSocket connection
                    function initWebSocket() {
                        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                        const wsUrl = `${protocol}//${window.location.host}/ws`;
                        
                        ws = new WebSocket(wsUrl);
                        
                        ws.onopen = function() {
                            console.log('WebSocket connected');
                            loadAgentStatus();
                        };
                        
                        ws.onmessage = function(event) {
                            const data = JSON.parse(event.data);
                            handleWebSocketMessage(data);
                        };
                        
                        ws.onclose = function() {
                            console.log('WebSocket disconnected');
                            setTimeout(initWebSocket, 5000);
                        };
                    }
                    
                    // Handle WebSocket messages
                    function handleWebSocketMessage(data) {
                        if (data.type === 'response' && data.request_id === currentRequestId) {
                            displayResponse(data);
                        } else if (data.type === 'status_update') {
                            updateAgentStatus(data.agents);
                        }
                    }
                    
                    // Handle form submission
                    document.getElementById('travelForm').addEventListener('submit', async function(e) {
                        e.preventDefault();
                        
                        const destination = document.getElementById('destination').value.trim();
                        const checkIn = document.getElementById('checkIn').value;
                        const checkOut = document.getElementById('checkOut').value;
                        const budget = document.getElementById('budget').value;
                        const guests = parseInt(document.getElementById('guests').value);
                        const carNeeded = document.getElementById('carNeeded').value === 'true';
                        const preferences = document.getElementById('preferences').value.trim();
                        
                        if (!destination || !checkIn || !checkOut) {
                            alert('Please fill in all required fields');
                            return;
                        }
                        
                        if (new Date(checkOut) <= new Date(checkIn)) {
                            alert('Check-out date must be after check-in date');
                            return;
                        }
                        
                        const btn = document.querySelector('.btn');
                        btn.disabled = true;
                        btn.textContent = 'Planning...';
                        
                        try {
                            const response = await fetch('/api/plan-trip', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    destination,
                                    check_in: checkIn,
                                    check_out: checkOut,
                                    budget,
                                    guests,
                                    car_needed: carNeeded,
                                    preferences: preferences || null
                                })
                            });
                            
                            const result = await response.json();
                            
                            if (result.success) {
                                currentRequestId = result.request_id;
                                displayResponse(result);
                            } else {
                                displayError(result.error);
                            }
                        } catch (error) {
                            displayError('Request failed: ' + error.message);
                        } finally {
                            btn.disabled = false;
                            btn.textContent = '🚀 Plan My Trip';
                        }
                    });
                    
                    // Display response
                    function displayResponse(data) {
                        const responseBox = document.getElementById('responseBox');
                        const responseContent = document.getElementById('responseContent');
                        
                        responseBox.style.display = 'block';
                        
                        if (data.success && data.result) {
                            const result = data.result;
                            let html = `
                                <div class="success">
                                    <h4>✅ Travel Plan Generated Successfully</h4>
                                    <p><strong>Processing Time:</strong> ${data.processing_time.toFixed(2)}s</p>
                                </div>
                            `;
                            
                            if (result.hotel_recommendations) {
                                html += '<div class="travel-plan"><h4>🏨 Hotel Recommendations</h4>';
                                if (Array.isArray(result.hotel_recommendations)) {
                                    result.hotel_recommendations.forEach(hotel => {
                                        html += `
                                            <div class="hotel-option">
                                                <div class="option-name">${hotel.name || 'Hotel'}</div>
                                                <div>${hotel.description || ''}</div>
                                                <div class="option-price">${hotel.estimated_cost_usd || 'Price N/A'}</div>
                                                ${hotel.link ? `<a href="${hotel.link}" target="_blank" class="option-link">View Details</a>` : ''}
                                            </div>
                                        `;
                                    });
                                } else {
                                    html += `<div>${result.hotel_recommendations}</div>`;
                                }
                                html += '</div>';
                            }
                            
                            if (result.car_rental_options) {
                                html += '<div class="travel-plan"><h4>🚗 Car Rental Options</h4>';
                                if (Array.isArray(result.car_rental_options)) {
                                    result.car_rental_options.forEach(car => {
                                        html += `
                                            <div class="car-option">
                                                <div class="option-name">${car.name || 'Car Rental'}</div>
                                                <div>${car.description || ''}</div>
                                                <div class="option-price">${car.estimated_cost_usd || 'Price N/A'}</div>
                                                ${car.link ? `<a href="${car.link}" target="_blank" class="option-link">View Details</a>` : ''}
                                            </div>
                                        `;
                                    });
                                } else {
                                    html += `<div>${result.car_rental_options}</div>`;
                                }
                                html += '</div>';
                            }
                            
                            if (result.travel_plan) {
                                html += `<div class="travel-plan"><h4>📝 AI-Generated Travel Plan</h4><div>${result.travel_plan.replace(/\\n/g, '<br>')}</div></div>`;
                            }
                            
                            responseContent.innerHTML = html;
                        } else {
                            responseContent.innerHTML = `
                                <div class="error">
                                    <h4>❌ Request Failed</h4>
                                    <p>${data.error || 'Unknown error occurred'}</p>
                                </div>
                            `;
                        }
                    }
                    
                    // Display error
                    function displayError(message) {
                        const responseBox = document.getElementById('responseBox');
                        const responseContent = document.getElementById('responseContent');
                        
                        responseBox.style.display = 'block';
                        responseContent.innerHTML = `
                            <div class="error">
                                <h4>❌ Error</h4>
                                <p>${message}</p>
                            </div>
                        `;
                    }
                    
                    // Load agent status
                    async function loadAgentStatus() {
                        try {
                            const response = await fetch('/api/status');
                            const status = await response.json();
                            updateAgentStatus(status.agents);
                        } catch (error) {
                            console.error('Failed to load agent status:', error);
                        }
                    }
                    
                    // Update agent status display
                    function updateAgentStatus(agents) {
                        const agentStatus = document.getElementById('agentStatus');
                        
                        if (!agents || agents.length === 0) {
                            agentStatus.innerHTML = '<div class="loading">No agents available</div>';
                            return;
                        }
                        
                        agentStatus.innerHTML = agents.map(agent => `
                            <div class="agent-card">
                                <h3>${agent.agent_id.replace('_', ' ').toUpperCase()}</h3>
                                <p><span class="status-indicator ${agent.status === 'active' ? 'status-online' : 'status-offline'}"></span>${agent.status}</p>
                                <p><strong>Capabilities:</strong> ${agent.capabilities.join(', ')}</p>
                                <p><strong>Last Activity:</strong> ${new Date(agent.last_activity).toLocaleString()}</p>
                            </div>
                        `).join('');
                    }
                    
                    // Initialize on page load
                    document.addEventListener('DOMContentLoaded', function() {
                        initWebSocket();
                        // Set default dates
                        const today = new Date();
                        const tomorrow = new Date(today);
                        tomorrow.setDate(tomorrow.getDate() + 1);
                        const dayAfter = new Date(tomorrow);
                        dayAfter.setDate(dayAfter.getDate() + 1);
                        
                        document.getElementById('checkIn').value = tomorrow.toISOString().split('T')[0];
                        document.getElementById('checkOut').value = dayAfter.toISOString().split('T')[0];
                    });
                </script>
            </body>
            </html>
            """
        
        @self.app.post("/api/plan-trip")
        async def plan_trip(request: TravelRequest):
            """Plan a trip using the multi-agent system."""
            try:
                request_id = str(uuid.uuid4())
                self.active_requests[request_id] = request
                self.total_requests += 1
                
                start_time = asyncio.get_event_loop().time()
                
                # Check agent status first
                agent_status = await self.check_agent_status()
                
                # Prepare request for travel planner
                travel_request = {
                    "destination": request.destination,
                    "check_in": request.check_in,
                    "check_out": request.check_out,
                    "budget": request.budget,
                    "guests": request.guests,
                    "car_needed": request.car_needed,
                    "preferences": request.preferences
                }
                
                # Try to use travel planner agent if available
                if agent_status["travel_planner"] == "active":
                    result = await self.coordinate_travel_planning(travel_request)
                else:
                    # Fallback to direct agent communication
                    result = await self.direct_agent_communication(travel_request)
                
                processing_time = asyncio.get_event_loop().time() - start_time
                
                if result.get("success", False):
                    self.successful_requests += 1
                    
                    response = UserResponse(
                        request_id=request_id,
                        success=True,
                        result=result,
                        processing_time=processing_time,
                        timestamp=datetime.now()
                    )
                else:
                    response = UserResponse(
                        request_id=request_id,
                        success=False,
                        error=result.get("error", "Unknown error occurred"),
                        processing_time=processing_time,
                        timestamp=datetime.now()
                    )
                
                # Store response
                self.request_history.append(response)
                
                # Clean up
                if request_id in self.active_requests:
                    del self.active_requests[request_id]
                
                return response.dict()
                
            except Exception as e:
                logger.error(f"Trip planning error: {str(e)}")
                return UserResponse(
                    request_id=str(uuid.uuid4()),
                    success=False,
                    error=str(e),
                    processing_time=0.0,
                    timestamp=datetime.now()
                ).dict()
        
        @self.app.get("/api/status")
        async def get_system_status():
            """Get system status including agent status."""
            try:
                agent_status = await self.check_agent_status()
                agents = []
                
                # Create agent status objects
                if agent_status["travel_planner"] == "active":
                    agents.append(AgentStatus(
                        agent_id="travel_planner",
                        status="active",
                        capabilities=settings.TRAVEL_PLANNER_CAPABILITIES,
                        last_activity=datetime.now()
                    ))
                
                if agent_status["hotel_agent"] == "active":
                    agents.append(AgentStatus(
                        agent_id="hotel_agent",
                        status="active",
                        capabilities=settings.HOTEL_AGENT_CAPABILITIES,
                        last_activity=datetime.now()
                    ))
                
                if agent_status["car_rental_agent"] == "active":
                    agents.append(AgentStatus(
                        agent_id="car_rental_agent",
                        status="active",
                        capabilities=settings.CAR_RENTAL_CAPABILITIES,
                        last_activity=datetime.now()
                    ))
                
                return SystemStatus(
                    travel_planner=agent_status["travel_planner"],
                    hotel_agent=agent_status["hotel_agent"],
                    car_rental_agent=agent_status["car_rental_agent"],
                    agents=agents,
                    total_requests=self.total_requests,
                    active_connections=len(self.connected_clients)
                ).dict()
                
            except Exception as e:
                logger.error(f"Status check error: {str(e)}")
                return SystemStatus(
                    travel_planner="unknown",
                    hotel_agent="unknown",
                    car_rental_agent="unknown",
                    agents=[],
                    total_requests=self.total_requests,
                    active_connections=len(self.connected_clients)
                ).dict()
        
        @self.app.get("/api/history")
        async def get_request_history():
            """Get request history."""
            return {"history": [req.dict() for req in self.request_history[-50:]]}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time communication."""
            await websocket.accept()
            self.connected_clients.append(websocket)
            logger.info(f"Client connected. Total clients: {len(self.connected_clients)}")
            
            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Handle client message
                    if message.get("type") == "status_request":
                        status = await get_system_status()
                        await websocket.send_text(json.dumps({
                            "type": "status_update",
                            "data": status
                        }))
            except WebSocketDisconnect:
                self.connected_clients.remove(websocket)
                logger.info(f"Client disconnected. Total clients: {len(self.connected_clients)}")
    
    async def check_agent_status(self) -> Dict[str, str]:
        """Check the status of all agents."""
        status = {
            "travel_planner": "offline",
            "hotel_agent": "offline",
            "car_rental_agent": "offline"
        }
        
        # Check travel planner agent
        try:
            response = requests.get(f"{settings.travel_planner_url}/health", timeout=5)
            if response.status_code == 200:
                status["travel_planner"] = "active"
        except:
            pass
        
        # Check hotel agent
        try:
            response = requests.get(f"{settings.hotel_agent_url}/health", timeout=5)
            if response.status_code == 200:
                status["hotel_agent"] = "active"
        except:
            pass
        
        # Check car rental agent
        try:
            response = requests.get(f"{settings.car_rental_agent_url}/health", timeout=5)
            if response.status_code == 200:
                status["car_rental_agent"] = "active"
        except:
            pass
        
        return status
    
    async def coordinate_travel_planning(self, travel_request: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate travel planning using the travel planner agent."""
        try:
            # Convert travel request to message format expected by travel planner
            message = f"Plan a trip to {travel_request['destination']} from {travel_request['check_in']} to {travel_request['check_out']} for {travel_request['guests']} guests"
            if travel_request.get('car_needed'):
                message += " with car rental"
            if travel_request.get('preferences'):
                message += f". Special preferences: {travel_request['preferences']}"
            
            print(f"🔍 DEBUG: Sending message to Travel Planner: {message}")
            print(f"📍 DEBUG: Destination from request: {travel_request['destination']}")
            
            # Use the travel planner agent to coordinate the entire process
            response = requests.post(
                f"{settings.travel_planner_url}/plan",
                json={"message": message},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                # The travel planner returns {"plan": "..."} format
                return {
                    "success": True,
                    "travel_plan": result.get("plan", ""),
                    "hotel_recommendations": "Contacted hotel agent for recommendations",
                    "car_rental_options": "Contacted car rental agent for options"
                }
            else:
                return {"success": False, "error": f"Travel planner error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": f"Travel planner communication error: {str(e)}"}
    
    async def direct_agent_communication(self, travel_request: Dict[str, Any]) -> Dict[str, Any]:
        """Directly communicate with individual agents."""
        result = {"success": True, "hotel_recommendations": "", "car_rental_options": "", "travel_plan": ""}
        
        # Get hotel recommendations
        try:
            hotel_query = f"Find top 10 budget-friendly hotels in {travel_request['destination']} for {travel_request['guests']} guests from {travel_request['check_in']} to {travel_request['check_out']}"
            if travel_request['budget'] != "any":
                hotel_query += f" with {travel_request['budget']} budget"
            
            hotel_response = requests.post(
                f"{settings.hotel_agent_url}/chat",
                json={"message": hotel_query},
                timeout=30
            )
            
            if hotel_response.status_code == 200:
                hotel_data = hotel_response.json()
                result["hotel_recommendations"] = hotel_data.get("response", "No hotel recommendations available")
        except Exception as e:
            result["hotel_recommendations"] = f"Hotel agent error: {str(e)}"
        
        # Get car rental options if needed
        if travel_request.get("car_needed", False):
            try:
                car_query = f"Find car rental options in {travel_request['destination']} from {travel_request['check_in']} to {travel_request['check_out']}"
                
                car_response = requests.post(
                    f"{settings.car_rental_agent_url}/chat",
                    json={"message": car_query},
                    timeout=30
                )
                
                if car_response.status_code == 200:
                    car_data = car_response.json()
                    result["car_rental_options"] = car_data.get("response", "No car rental options available")
            except Exception as e:
                result["car_rental_options"] = f"Car rental agent error: {str(e)}"
        
        # Generate travel plan using LLM
        try:
            from langchain_groq import ChatGroq
            import os
            
            llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
            
            plan_prompt = f"""
            You are a travel planning expert. Create a comprehensive travel plan based on the following information:
            
            Destination: {travel_request['destination']}
            Check-in: {travel_request['check_in']}
            Check-out: {travel_request['check_out']}
            Budget: {travel_request['budget']}
            Guests: {travel_request['guests']}
            Car Rental Needed: {travel_request.get('car_needed', False)}
            
            Hotel Recommendations:
            {result['hotel_recommendations']}
            
            Car Rental Options:
            {result.get('car_rental_options', 'No car rental requested')}
            
            Please create a detailed travel itinerary that includes:
            1. Summary of the trip
            2. Top hotel recommendations with prices and features
            3. Car rental options and recommendations (if requested)
            4. Estimated total cost breakdown
            5. Travel tips and recommendations
            6. Day-by-day itinerary suggestions
            
            Format the response clearly with sections, bullet points, and markdown formatting.
            """
            
            plan_response = llm.invoke(plan_prompt)
            result["travel_plan"] = plan_response.content
        except Exception as e:
            result["travel_plan"] = f"Error generating travel plan: {str(e)}"
        
        return result

# Create AG-UI travel server instance
ag_ui_travel_server = AGUITravelServer()

if __name__ == "__main__":
    uvicorn.run(
        ag_ui_travel_server.app,
        host=settings.ag_ui_host,
        port=settings.ag_ui_port,
        log_level="info"
    )
