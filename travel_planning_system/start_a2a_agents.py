#!/usr/bin/env python3
"""
Start all agents with A2A protocol support.
"""

import subprocess
import time
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["GROQ_API_KEY", "SERPER_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        return False
    
    print("✅ All required environment variables are set")
    return True

def start_agent(agent_name, script_path, port):
    """Start an agent in a separate process."""
    print(f"🚀 Starting {agent_name} on port {port}...")
    try:
        process = subprocess.Popen([
            sys.executable, script_path
        ], cwd=os.path.dirname(script_path))
        print(f"✅ {agent_name} started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Failed to start {agent_name}: {e}")
        return None

def main():
    """Start all A2A agents."""
    print("🤖 A2A Travel Planner System Startup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Agent configurations
    agents = [
        {
            "name": "Hotel Booking Agent (A2A)",
            "script": "hotel_booking_agent_crewai/a2a_hotel_executor.py",
            "port": 10002
        },
        {
            "name": "Car Rental Agent (A2A)", 
            "script": "car_rental_agent_langgraph/a2a_car_executor.py",
            "port": 10003
        },
        {
            "name": "Travel Planner Agent (A2A)",
            "script": "travel_planner_agent_adk/simple_executor.py",
            "port": 10001
        }
    ]
    
    processes = []
    
    try:
        # Start all agents
        for agent in agents:
            process = start_agent(agent["name"], agent["script"], agent["port"])
            if process:
                processes.append((agent["name"], process))
            time.sleep(2)  # Give each agent time to start
        
        print("\n🎉 All A2A agents started successfully!")
        print("\n📋 Agent Status:")
        for name, process in processes:
            status = "✅ Running" if process.poll() is None else "❌ Stopped"
            print(f"   {name}: {status}")
        
        print("\n🌐 Available Endpoints:")
        print("   Travel Planner: http://localhost:10001")
        print("   Hotel Agent: http://localhost:10002")
        print("   Car Rental Agent: http://localhost:10003")
        print("\n🤖 A2A Protocol Endpoints:")
        print("   Hotel Agent Card: http://localhost:10002/.well-known/agent.json")
        print("   Car Rental Agent Card: http://localhost:10003/.well-known/agent.json")
        
        print("\n⏳ Waiting for agents to initialize...")
        time.sleep(5)
        
        print("\n✅ A2A Travel Planner System is ready!")
        print("Press Ctrl+C to stop all agents")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping all A2A agents...")
        for name, process in processes:
            try:
                process.terminate()
                print(f"✅ {name} stopped")
            except:
                print(f"❌ Failed to stop {name}")
        
        print("✅ All agents stopped")

if __name__ == "__main__":
    main()
