# 🤖 AG-UI Travel Planner System

A comprehensive Agent User Interface (AG-UI) implementation for the Multi-Agent Travel Planning System. This system provides a modern web interface for interacting with specialized AI agents that coordinate to create personalized travel plans.

## 🌟 Features

- **Modern Web Interface**: Clean, responsive UI for travel planning
- **Real-time Agent Status**: Monitor all agents in real-time
- **Multi-Agent Coordination**: Seamless communication between specialized agents
- **AI-Powered Recommendations**: Get hotel and car rental suggestions
- **Comprehensive Travel Plans**: AI-generated itineraries with cost breakdowns
- **WebSocket Support**: Real-time updates and communication

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AG-UI Server (Port 8000)                │
│                    FastAPI + WebSocket                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐        ┌────▼────┐        ┌───▼───┐
│Travel │        │ Hotel  │        │  Car  │
│Planner│        │ Agent  │        │Agent  │
│Agent  │        │(CrewAI)│        │(LangGraph)│
│(ADK)  │        │Port10002│       │Port10003│
│Port10001│      └────────┘        └────────┘
└────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Required API keys:
  - `GROQ_API_KEY` - For LLM inference
  - `SERPER_API_KEY` - For web search

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd Travel-Planner-Multi-Agent-A2A/travel_planning_system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r ag_ui_requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

### Running the System

#### Option 1: Complete System (Recommended)
Start all agents and the AG-UI server together:
```bash
python start_complete_system.py
```

#### Option 2: Individual Components
Start agents individually:

1. **Start Travel Planner Agent:**
   ```bash
   python travel_planner_agent_adk/simple_executor.py
   ```

2. **Start Hotel Booking Agent:**
   ```bash
   python hotel_booking_agent_crewai/simple_executor.py
   ```

3. **Start Car Rental Agent:**
   ```bash
   python car_rental_agent_langgraph/simple_executor.py
   ```

4. **Start AG-UI Server:**
   ```bash
   python start_ag_ui_server.py
   ```

### Access the System

Open your browser and navigate to: **http://localhost:8000**

## 🧪 Testing

Run the integration test suite:
```bash
python test_ag_ui_integration.py
```

This will test:
- Server health
- Agent connectivity
- Travel planning functionality
- Request history
- System status monitoring

## 📋 API Endpoints

### AG-UI Server Endpoints

- `GET /` - Main web interface
- `POST /api/plan-trip` - Plan a trip
- `GET /api/status` - System status
- `GET /api/history` - Request history
- `WebSocket /ws` - Real-time communication

### Agent Endpoints

- **Travel Planner Agent** (Port 10001)
  - `GET /health` - Health check
  - `POST /api/plan-trip` - Coordinate travel planning

- **Hotel Booking Agent** (Port 10002)
  - `GET /health` - Health check
  - `POST /chat` - Hotel search and booking

- **Car Rental Agent** (Port 10003)
  - `GET /health` - Health check
  - `POST /chat` - Car rental search and booking

## 🎯 Usage Examples

### Basic Travel Planning Request

```json
{
  "destination": "Paris",
  "check_in": "2024-02-15",
  "check_out": "2024-02-20",
  "budget": "mid-range",
  "guests": 2,
  "car_needed": true,
  "preferences": "Near city center, family-friendly"
}
```

### Expected Response

```json
{
  "request_id": "uuid-here",
  "success": true,
  "result": {
    "hotel_recommendations": [
      {
        "name": "Hotel Name",
        "description": "Hotel description",
        "link": "https://booking.com/hotel",
        "estimated_cost_usd": "$150 USD"
      }
    ],
    "car_rental_options": [
      {
        "name": "Car Rental Company",
        "description": "Car description",
        "link": "https://rental.com",
        "estimated_cost_usd": "$50 USD"
      }
    ],
    "travel_plan": "AI-generated comprehensive travel plan..."
  },
  "processing_time": 15.2,
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔧 Configuration

### Agent Configuration (`ag_ui_config.py`)

```python
class Settings:
    # Server settings
    ag_ui_host: str = "localhost"
    ag_ui_port: int = 8000
    
    # Agent settings
    travel_planner_host: str = "localhost"
    travel_planner_port: int = 10001
    hotel_agent_host: str = "localhost"
    hotel_agent_port: int = 10002
    car_rental_agent_host: str = "localhost"
    car_rental_agent_port: int = 10003
```

### Environment Variables

- `GROQ_API_KEY` - Required for LLM inference
- `SERPER_API_KEY` - Required for web search
- `AG_UI_HOST` - AG-UI server host (default: localhost)
- `AG_UI_PORT` - AG-UI server port (default: 8000)

## 🐛 Troubleshooting

### Common Issues

1. **Agents not responding:**
   - Check if agents are running on correct ports
   - Verify environment variables are set
   - Check agent logs for errors

2. **API key errors:**
   - Ensure `GROQ_API_KEY` and `SERPER_API_KEY` are set
   - Verify API keys are valid and have sufficient quota

3. **Connection timeouts:**
   - Check network connectivity
   - Verify agent health endpoints
   - Increase timeout values if needed

### Debug Mode

Run with debug logging:
```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from start_ag_ui_server import start_ag_ui_server
start_ag_ui_server()
"
```

## 📊 Monitoring

### Real-time Status
- Agent health monitoring
- Request processing times
- System performance metrics
- WebSocket connections

### Logs
- Request/response logging
- Error tracking
- Performance metrics
- Agent communication logs

## 🔄 System Flow

1. **User Input** → AG-UI Interface
2. **Request Processing** → AG-UI Server
3. **Agent Coordination** → Travel Planner Agent
4. **Specialized Tasks** → Hotel & Car Rental Agents
5. **Response Aggregation** → AG-UI Server
6. **Result Display** → User Interface

## 🚀 Advanced Features

### WebSocket Communication
- Real-time status updates
- Live agent monitoring
- Instant response notifications

### Multi-Agent Coordination
- Intelligent task delegation
- Parallel processing
- Result aggregation

### AI-Powered Planning
- Natural language processing
- Context-aware recommendations
- Personalized suggestions

## 📈 Performance

### Optimization Features
- Async request processing
- Connection pooling
- Caching mechanisms
- Load balancing

### Scalability
- Horizontal scaling support
- Agent load distribution
- Resource management
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the Multi-Agent Travel Planning System and follows the same licensing terms.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review agent logs
3. Test individual components
4. Contact the development team

---

**🎉 Enjoy planning your perfect trip with AI-powered agents!**
