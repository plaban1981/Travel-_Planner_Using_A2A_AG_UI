#!/usr/bin/env python3
"""
Startup script for AG-UI Travel Planner Server.
This script starts the AG-UI server and provides instructions for running the complete system.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_agent_status(agent_name, url, timeout=5):
    """Check if an agent is running."""
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except:
        return False

def start_ag_ui_server():
    """Start the AG-UI Travel Planner Server."""
    print("🚀 Starting AG-UI Travel Planner Server...")
    print("=" * 60)
    
    # Check if required environment variables are set
    required_env_vars = ["GROQ_API_KEY", "SERPER_API_KEY"]
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables before running the server.")
        print("You can create a .env file with:")
        for var in missing_vars:
            print(f"   {var}=your_api_key_here")
        return False
    
    # Check agent status
    print("🔍 Checking agent status...")
    agents = {
        "Travel Planner": "http://localhost:10001",
        "Hotel Agent": "http://localhost:10002", 
        "Car Rental Agent": "http://localhost:10003"
    }
    
    agent_status = {}
    for name, url in agents.items():
        status = check_agent_status(name, url)
        agent_status[name] = "✅ Running" if status else "❌ Not running"
        print(f"   {name}: {agent_status[name]}")
    
    print("\n📋 System Status:")
    print("   AG-UI Server: Starting...")
    for name, status in agent_status.items():
        print(f"   {name}: {status}")
    
    if not any("✅" in status for status in agent_status.values()):
        print("\n⚠️  Warning: No agents are currently running.")
        print("   The AG-UI server will start but may not function properly.")
        print("   Please start the required agents:")
        print("   1. Travel Planner Agent (port 10001)")
        print("   2. Hotel Booking Agent (port 10002)")
        print("   3. Car Rental Agent (port 10003)")
    
    print("\n🌐 Starting AG-UI Server...")
    print("   Server will be available at: http://localhost:8000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the AG-UI server
        from ag_ui_travel_server import ag_ui_travel_server, settings
        import uvicorn
        
        uvicorn.run(
            ag_ui_travel_server.app,
            host=settings.ag_ui_host,
            port=settings.ag_ui_port,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 AG-UI Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting AG-UI Server: {e}")
        return False
    
    return True

def print_usage_instructions():
    """Print usage instructions for the complete system."""
    print("\n" + "=" * 60)
    print("📖 AG-UI Travel Planner System - Usage Instructions")
    print("=" * 60)
    print("\n1. 🚀 Starting the Complete System:")
    print("   a) Start the individual agents first:")
    print("      - Travel Planner Agent: python travel_planner_agent_adk/simple_executor.py")
    print("      - Hotel Agent: python hotel_booking_agent_crewai/simple_executor.py") 
    print("      - Car Rental Agent: python car_rental_agent_langgraph/simple_executor.py")
    print("\n   b) Start the AG-UI Server:")
    print("      - python start_ag_ui_server.py")
    print("\n2. 🌐 Access the System:")
    print("   - Open your browser and go to: http://localhost:8000")
    print("   - Fill in the travel planning form")
    print("   - Submit to get AI-powered travel recommendations")
    print("\n3. 🔧 Configuration:")
    print("   - Make sure you have GROQ_API_KEY and SERPER_API_KEY in your .env file")
    print("   - All agents should be running on their respective ports")
    print("\n4. 🐛 Troubleshooting:")
    print("   - Check agent status in the AG-UI interface")
    print("   - Ensure all required environment variables are set")
    print("   - Verify all agents are running and accessible")
    print("=" * 60)

if __name__ == "__main__":
    print("🤖 AG-UI Travel Planner Server Startup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("ag_ui_travel_server.py").exists():
        print("❌ Error: ag_ui_travel_server.py not found in current directory")
        print("   Please run this script from the travel_planning_system directory")
        sys.exit(1)
    
    # Start the server
    success = start_ag_ui_server()
    
    if success:
        print_usage_instructions()
    else:
        print("\n❌ Failed to start AG-UI server")
        sys.exit(1)
