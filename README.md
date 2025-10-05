# Travel-_Planner_Using_A2A_AG_UI
Creating a Travel Planner Multi agent system using A2A, AG-UI, Crewwai,Google ADK and Langgraph

<img width="1597" height="866" alt="image" src="https://github.com/user-attachments/assets/dc2951bf-4d7d-4da9-9379-60de30201608" />


<img width="1562" height="866" alt="image" src="https://github.com/user-attachments/assets/35b5b556-f3e4-4e98-94a2-8d537e28399a" />


<img width="1527" height="747" alt="image" src="https://github.com/user-attachments/assets/6316b96c-1d4c-4777-926e-0af678dc49d8" />



```
Travel-Planner-Multi-Agent-A2A/
└── travel_planning_system/
    ├── 📋 **Core System Files**
    │   ├── README.md                           # Main system documentation
    │   ├── ARCHITECTURE.md                     # System architecture overview
    │   ├── ARCHITECTURE_DIAGRAM.md             # Mermaid architecture diagrams
    │   ├── WORKFLOW.md                         # Complete A2A workflow documentation
    │   ├── A2A_IMPLEMENTATION_README.md        # A2A protocol implementation guide
    │   ├── COMPLETE_WORKFLOW_DIAGRAM.md        # Complete workflow diagrams
    │   ├── DETAILED_WORKFLOW.md                # Detailed workflow documentation
    │   └── QUICK_REFERENCE.md                  # Quick reference guide
    │
    ├── 🚀 **AG-UI System (Port 8000)**
    │   ├── ag_ui_travel_server.py              # Main AG-UI FastAPI server
    │   ├── ag_ui_config.py                     # AG-UI configuration settings
    │   ├── ag_ui_requirements.txt              # AG-UI dependencies
    │   ├── start_ag_ui_server.py               # AG-UI startup script
    │   ├── AG_UI_README.md                     # AG-UI documentation
    │   └── AG_UI_IMPLEMENTATION_SUMMARY.md     # AG-UI implementation summary
    │
    ├── 🧠 **Travel Planner Agent (Google ADK - Port 10001)**
    │   └── travel_planner_agent_adk/
    │       ├── 📁 **Core Agent Files**
    │       │   ├── simple_executor.py          # Main FastAPI executor
    │       │   ├── simple_a2a_executor.py      # A2A protocol executor
    │       │   ├── simple_a2a_agent.py         # A2A agent implementation
    │       │   ├── simple_travel_planner.py     # Simplified travel planner
    │       │   └── simple_executor_with_logging.py # Logging-enabled executor
    │       │
    │       ├── 📁 **Advanced Agent (travel_planner/)**
    │       │   ├── __init__.py                  # Package initialization
    │       │   ├── agent.py                     # Google ADK Travel Planner Agent
    │       │   └── remote_agent_connection.py   # A2A connection management
    │       │
    │       ├── 📁 **Configuration & Dependencies**
    │       │   ├── pyproject.toml               # Project configuration
    │       │   ├── requirements.txt             # Python dependencies
    │       │   ├── uv.lock                      # UV lock file
    │       │   └── create_env_file.py           # Environment setup
    │       │
    │       ├── 📁 **Testing & Logging**
    │       │   ├── test_travel_planner.py       # Agent testing
    │       │   ├── test_logging.py              # Logging tests
    │       │   └── agent_communication_log.json # A2A communication logs
    │       │
    │       └── 📁 **Version Directories**
    │           ├── 0.2.0/                      # Version 0.2.0 dependencies
    │           ├── 0.3.0/                      # Version 0.3.0 dependencies
    │           ├── 1.2.1/                      # Version 1.2.1 dependencies
    │           └── 1.6.0/                      # Version 1.6.0 dependencies
    │
    ├── 🏨 **Hotel Booking Agent (CrewAI - Port 10002)**
    │   └── hotel_booking_agent_crewai/
    │       ├── 📁 **Core Agent Files**
    │       │   ├── agent.py                     # CrewAI Hotel Booking Agent
    │       │   ├── simple_hotel_agent.py        # Simplified hotel agent
    │       │   ├── simple_hotel_executor.py   # Simplified executor
    │       │   ├── a2a_hotel_executor.py       # A2A protocol executor
    │       │   └── simple_hotel_agent_with_logging.py # Logging-enabled agent
    │       │
    │       ├── 📁 **MCP Servers (servers/)**
    │       │   ├── hotel_search_mcp_server.py  # Hotel search MCP server
    │       │   ├── hotel_booking_mcp_server.py # Hotel booking MCP server
    │       │   └── serper_config.py            # SerperAPI configuration
    │       │
    │       ├── 📁 **Configuration & Dependencies**
    │       │   ├── pyproject.toml               # Project configuration
    │       │   ├── requirements.txt             # Python dependencies
    │       │   ├── uv.lock                      # UV lock file
    │       │   └── create_env_file.py           # Environment setup
    │       │
    │       ├── 📁 **Testing & Utilities**
    │       │   ├── test_hotel_agent.py          # Hotel agent testing
    │       │   ├── test_hotel_search.py         # Hotel search testing
    │       │   ├── test_tools_direct.py         # Direct tool testing
    │       │   ├── test_location_fix.py         # Location fix testing
    │       │   ├── quick_test.py                # Quick functionality test
    │       │   └── agent_executor.py            # Agent executor
    │       │
    │       └── 📁 **Version Directories**
    │           ├── 0.2.0/                      # Version 0.2.0 dependencies
    │           ├── 0.3.0/                      # Version 0.3.0 dependencies
    │           └── 0.70.0/                     # Version 0.70.0 dependencies
    │
    ├── 🚗 **Car Rental Agent (LangGraph - Port 10003)**
    │   └── car_rental_agent_langgraph/
    │       ├── 📁 **Core Agent Files**
    │       │   ├── simple_car_agent.py          # Simplified car agent
    │       │   ├── a2a_car_executor.py          # A2A protocol executor
    │       │   └── car_rental_agent.log         # Agent execution logs
    │       │
    │       ├── 📁 **App Directory (app/)**
    │       │   ├── __init__.py                  # Package initialization
    │       │   ├── __main__.py                  # Main entry point
    │       │   ├── agent.py                     # LangGraph Car Rental Agent
    │       │   ├── agent_executor.py            # Agent executor
    │       │   ├── simple_car_agent.py         # Simplified car agent
    │       │   ├── simple_car_executor.py       # Simplified executor
    │       │   └── simple_executor.py           # Main executor
    │       │
    │       ├── 📁 **Configuration & Dependencies**
    │       │   ├── pyproject.toml               # Project configuration
    │       │   ├── requirements.txt             # Python dependencies
    │       │   ├── uv.lock                      # UV lock file
    │       │   └── create_env_file.py           # Environment setup
    │       │
    │       ├── 📁 **Testing & Debugging**
    │       │   ├── test_agent_direct.py         # Direct agent testing
    │       │   ├── test_car_agent.py            # Car agent testing
    │       │   ├── test_endpoints.py            # Endpoint testing
    │       │   ├── test_without_search.py       # Testing without search
    │       │   ├── check_dependencies.py        # Dependency checking
    │       │   └── debug_env.py                 # Environment debugging
    │       │
    │       └── 📁 **Version Directories**
    │           ├── 0.2.0/                      # Version 0.2.0 dependencies
    │           ├── 0.3.0/                      # Version 0.3.0 dependencies
    │           ├── 0.5.0/                      # Version 0.5.0 dependencies
    │           └── 2.0.0/                      # Version 2.0.0 dependencies
    │
    ├── 🛠️ **System Management & Setup**
    │   ├── start_complete_system.py             # Complete system startup
    │   ├── start_a2a_agents.py                  # A2A agents startup
    │   ├── start_a2a_agents_fixed.bat           # Windows batch startup
    │   ├── start_agents_manually.py             # Manual agent startup
    │   ├── start_all_agents.bat                 # All agents batch startup
    │   ├── install_dependencies.py              # Dependency installation
    │   ├── install_dependencies.bat             # Windows batch installation
    │   ├── setup_env.py                         # Environment setup
    │   ├── setup_uv_environments.py             # UV environment setup
    │   ├── quick_fix.py                         # Quick system fixes
    │   └── logging_config.py                    # Logging configuration
    │
    ├── 🧪 **Testing & Debugging**
    │   ├── test_ag_ui_integration.py            # AG-UI integration testing
    │   ├── test_api_key_direct.py               # API key testing
    │   ├── test_serper_fix.py                   # SerperAPI testing
    │   ├── debug_serper_api.py                  # SerperAPI debugging
    │   └── streamlit_travel_app.py              # Streamlit test app
    │
    ├── 📚 **Documentation & References**
    │   ├── INSTALLATION.md                      # Installation guide
    │   ├── QUICK_START.md                       # Quick start guide
    │   ├── UV_SETUP.md                          # UV setup guide
    │   ├── Multi-Agent Travel Planner.pdf       # PDF documentation
    │   └── Multi-Agent Travel Planner1.pdf     # Additional PDF docs
    │
    ├── 📦 **Dependencies & Configuration**
    │   ├── streamlit_requirements.txt           # Streamlit dependencies
    │   └── __pycache__/                         # Python cache files
    │
    └── 📄 **System Logs & Data**
        └── agent_communication_log.json         # A2A communication logs

```
