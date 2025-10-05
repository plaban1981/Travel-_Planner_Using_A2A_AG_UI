#!/usr/bin/env python3
"""
Manual agent startup script for AG-UI Travel Planner System.
This script provides the exact commands to start each agent manually.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_agent_health(url, timeout=5):
    """Check if an agent is healthy."""
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except:
        return False

def start_agent_in_terminal(agent_name, script_path, port):
    """Start an agent in a new terminal window."""
    print(f"🚀 Starting {agent_name}...")
    print(f"   Script: {script_path}")
    print(f"   Port: {port}")
    
    if not Path(script_path).exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        # Start the agent process
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for startup
        print(f"   Waiting for {agent_name} to start...")
        time.sleep(10)
        
        # Check health
        if check_agent_health(f"http://localhost:{port}"):
            print(f"   ✅ {agent_name} is running and healthy")
            return True
        else:
            print(f"   ❌ {agent_name} failed to start or is not responding")
            return False
            
    except Exception as e:
        print(f"   ❌ Error starting {agent_name}: {e}")
        return False

def main():
    """Main function to start all agents."""
    print("🤖 Manual Agent Startup for AG-UI Travel Planner")
    print("=" * 60)
    
    # Check environment
    groq_key = os.getenv("GROQ_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    if not groq_key or not serper_key:
        print("❌ Missing required environment variables")
        print("Please run: python setup_env.py")
        return False
    
    print("✅ Environment variables loaded")
    
    # Agent configurations
    agents = [
        {
            "name": "Travel Planner Agent",
            "script": "travel_planner_agent_adk/simple_executor.py",
            "port": 10001
        },
        {
            "name": "Hotel Booking Agent",
            "script": "hotel_booking_agent_crewai/simple_executor.py", 
            "port": 10002
        },
        {
            "name": "Car Rental Agent",
            "script": "car_rental_agent_langgraph/app/simple_executor.py",
            "port": 10003
        }
    ]
    
    print("\n📋 Starting agents in sequence...")
    
    # Start each agent
    for agent in agents:
        success = start_agent_in_terminal(
            agent["name"], 
            agent["script"], 
            agent["port"]
        )
        
        if not success:
            print(f"\n❌ Failed to start {agent['name']}")
            print("Please check the script path and try again")
            return False
    
    print("\n✅ All agents started successfully!")
    print("\n🌐 Next steps:")
    print("1. Start the AG-UI server: python start_ag_ui_server.py")
    print("2. Open your browser to: http://localhost:8000")
    print("3. Test the travel planning interface")
    
    return True

def print_manual_commands():
    """Print the manual commands for starting agents."""
    print("\n📖 Manual Commands (if automatic startup fails):")
    print("=" * 60)
    print("Open separate terminal windows and run these commands:")
    print()
    print("Terminal 1 - Travel Planner Agent:")
    print("cd travel_planning_system/travel_planner_agent_adk")
    print("python app/simple_executor.py")
    print()
    print("Terminal 2 - Hotel Booking Agent:")
    print("cd travel_planning_system/hotel_booking_agent_crewai")
    print("python simple_executor.py")
    print()
    print("Terminal 3 - Car Rental Agent:")
    print("cd travel_planning_system/car_rental_agent_langgraph")
    print("python app/simple_executor.py")
    print()
    print("Terminal 4 - AG-UI Server:")
    print("cd travel_planning_system")
    print("python start_ag_ui_server.py")
    print()
    print("Then open: http://localhost:8000")

if __name__ == "__main__":
    print("🚀 AG-UI Travel Planner - Manual Agent Startup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("ag_ui_travel_server.py").exists():
        print("❌ Error: ag_ui_travel_server.py not found")
        print("Please run this script from the travel_planning_system directory")
        sys.exit(1)
    
    # Try automatic startup first
    success = main()
    
    if not success:
        print("\n🔄 Automatic startup failed. Here are the manual commands:")
        print_manual_commands()
        sys.exit(1)
    else:
        print("\n🎉 All agents started successfully!")
        print("You can now start the AG-UI server with: python start_ag_ui_server.py")
