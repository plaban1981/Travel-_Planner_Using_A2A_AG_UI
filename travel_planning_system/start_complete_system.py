#!/usr/bin/env python3
"""
Complete System Startup Script for AG-UI Travel Planner.
This script starts all agents and the AG-UI server in the correct order.
"""

import os
import sys
import subprocess
import time
import requests
import signal
import threading
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SystemManager:
    """Manages the complete travel planner system startup and shutdown."""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.running = True
        
        # Agent configurations
        self.agents = {
            "travel_planner": {
                "name": "Travel Planner Agent",
                "script": "travel_planner_agent_adk/simple_executor.py",
                "port": 10001,
                "url": "http://localhost:10001",
                "startup_time": 10
            },
            "hotel_agent": {
                "name": "Hotel Booking Agent", 
                "script": "hotel_booking_agent_crewai/simple_executor.py",
                "port": 10002,
                "url": "http://localhost:10002",
                "startup_time": 10
            },
            "car_rental_agent": {
                "name": "Car Rental Agent",
                "script": "car_rental_agent_langgraph/app/simple_executor.py", 
                "port": 10003,
                "url": "http://localhost:10003",
                "startup_time": 10
            },
            "ag_ui_server": {
                "name": "AG-UI Server",
                "script": "start_ag_ui_server.py",
                "port": 8000,
                "url": "http://localhost:8000",
                "startup_time": 5
            }
        }
    
    def check_environment(self) -> bool:
        """Check if required environment variables are set."""
        required_vars = ["GROQ_API_KEY", "SERPER_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value or value == "your_groq_api_key_here" or value == "your_serper_api_key_here":
                missing_vars.append(var)
        
        if missing_vars:
            print("❌ Missing or invalid required environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\n🔧 To fix this, run the setup script:")
            print("   python setup_env.py")
            print("\nOr manually create a .env file with:")
            for var in missing_vars:
                print(f"   {var}=your_actual_api_key_here")
            return False
        
        return True
    
    def check_agent_health(self, agent_name: str, url: str, timeout: int = 5) -> bool:
        """Check if an agent is healthy and responding."""
        try:
            response = requests.get(f"{url}/health", timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    def start_agent(self, agent_name: str) -> bool:
        """Start a specific agent."""
        agent_config = self.agents[agent_name]
        script_path = agent_config["script"]
        
        if not Path(script_path).exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        print(f"🚀 Starting {agent_config['name']}...")
        
        try:
            # Start the agent process
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes.append(process)
            
            # Wait for agent to start up
            print(f"   Waiting for {agent_config['name']} to start...")
            time.sleep(agent_config["startup_time"])
            
            # Check if agent is healthy
            if self.check_agent_health(agent_name, agent_config["url"]):
                print(f"   ✅ {agent_config['name']} is running and healthy")
                return True
            else:
                print(f"   ❌ {agent_config['name']} failed to start or is not responding")
                return False
                
        except Exception as e:
            print(f"   ❌ Error starting {agent_config['name']}: {e}")
            return False
    
    def start_all_agents(self) -> bool:
        """Start all agents in the correct order."""
        print("🤖 Starting Multi-Agent Travel Planner System")
        print("=" * 60)
        
        # Start agents in dependency order
        agent_order = ["travel_planner", "hotel_agent", "car_rental_agent", "ag_ui_server"]
        
        for agent_name in agent_order:
            if not self.start_agent(agent_name):
                print(f"\n❌ Failed to start {self.agents[agent_name]['name']}")
                print("   Stopping all processes...")
                self.stop_all_agents()
                return False
        
        print("\n✅ All agents started successfully!")
        return True
    
    def stop_all_agents(self):
        """Stop all running agents."""
        print("\n🛑 Stopping all agents...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"   Error stopping process: {e}")
        
        self.processes.clear()
        print("✅ All agents stopped")
    
    def monitor_system(self):
        """Monitor the system and display status."""
        print("\n📊 System Status Monitor")
        print("=" * 60)
        print("Press Ctrl+C to stop the system")
        print("=" * 60)
        
        try:
            while self.running:
                print(f"\n🕐 {time.strftime('%H:%M:%S')} - System Status:")
                
                for agent_name, config in self.agents.items():
                    if agent_name == "ag_ui_server":
                        # Check if AG-UI server is responding
                        try:
                            response = requests.get(config["url"], timeout=2)
                            status = "✅ Running" if response.status_code == 200 else "❌ Not responding"
                        except:
                            status = "❌ Not reachable"
                    else:
                        # Check agent health
                        if self.check_agent_health(agent_name, config["url"]):
                            status = "✅ Healthy"
                        else:
                            status = "❌ Unhealthy"
                    
                    print(f"   {config['name']}: {status}")
                
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\n👋 Shutdown requested by user")
            self.running = False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        self.stop_all_agents()
        sys.exit(0)
    
    def run(self):
        """Run the complete system."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check environment
        if not self.check_environment():
            return False
        
        # Start all agents
        if not self.start_all_agents():
            return False
        
        # Display system information
        print("\n🌐 System Access Information:")
        print("   AG-UI Interface: http://localhost:8000")
        print("   Travel Planner API: http://localhost:10001")
        print("   Hotel Agent API: http://localhost:10002")
        print("   Car Rental Agent API: http://localhost:10003")
        print("\n📖 Usage Instructions:")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Fill in the travel planning form")
        print("   3. Submit to get AI-powered recommendations")
        print("   4. Monitor agent status in the interface")
        
        # Start monitoring
        self.monitor_system()
        
        return True

def main():
    """Main entry point."""
    print("🚀 AG-UI Travel Planner System Manager")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("ag_ui_travel_server.py").exists():
        print("❌ Error: ag_ui_travel_server.py not found")
        print("   Please run this script from the travel_planning_system directory")
        sys.exit(1)
    
    # Create and run system manager
    manager = SystemManager()
    success = manager.run()
    
    if not success:
        print("\n❌ System startup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
