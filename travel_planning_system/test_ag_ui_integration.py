#!/usr/bin/env python3
"""
Test script for AG-UI Travel Planner integration.
This script tests the complete system integration.
"""

import requests
import json
import time
from typing import Dict, Any

class AGUITestClient:
    """Test client for AG-UI Travel Planner system."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_server_health(self) -> bool:
        """Test if the AG-UI server is running."""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_system_status(self) -> Dict[str, Any]:
        """Test system status endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/api/status", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def test_travel_planning(self, test_request: Dict[str, Any]) -> Dict[str, Any]:
        """Test travel planning endpoint."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/plan-trip",
                json=test_request,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def test_request_history(self) -> Dict[str, Any]:
        """Test request history endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/api/history", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

def run_integration_tests():
    """Run comprehensive integration tests."""
    print("🧪 AG-UI Travel Planner Integration Tests")
    print("=" * 60)
    
    client = AGUITestClient()
    
    # Test 1: Server Health
    print("1. Testing AG-UI Server Health...")
    if client.test_server_health():
        print("   ✅ AG-UI Server is running")
    else:
        print("   ❌ AG-UI Server is not responding")
        print("   Please start the server with: python start_ag_ui_server.py")
        return False
    
    # Test 2: System Status
    print("\n2. Testing System Status...")
    status = client.test_system_status()
    if "error" in status:
        print(f"   ❌ System status error: {status['error']}")
    else:
        print("   ✅ System status retrieved successfully")
        print(f"   Travel Planner: {status.get('travel_planner', 'unknown')}")
        print(f"   Hotel Agent: {status.get('hotel_agent', 'unknown')}")
        print(f"   Car Rental Agent: {status.get('car_rental_agent', 'unknown')}")
        print(f"   Total Requests: {status.get('total_requests', 0)}")
        print(f"   Active Connections: {status.get('active_connections', 0)}")
    
    # Test 3: Travel Planning Request
    print("\n3. Testing Travel Planning Request...")
    test_request = {
        "destination": "Paris",
        "check_in": "2024-02-15",
        "check_out": "2024-02-20",
        "budget": "mid-range",
        "guests": 2,
        "car_needed": True,
        "preferences": "Near city center, family-friendly"
    }
    
    print(f"   Sending test request: {test_request['destination']} trip")
    result = client.test_travel_planning(test_request)
    
    if "error" in result:
        print(f"   ❌ Travel planning error: {result['error']}")
    else:
        print("   ✅ Travel planning request processed")
        if result.get("success"):
            print(f"   Processing time: {result.get('processing_time', 0):.2f}s")
            if result.get("result"):
                res = result["result"]
                if res.get("hotel_recommendations"):
                    print("   ✅ Hotel recommendations received")
                if res.get("car_rental_options"):
                    print("   ✅ Car rental options received")
                if res.get("travel_plan"):
                    print("   ✅ AI-generated travel plan created")
        else:
            print(f"   ❌ Request failed: {result.get('error', 'Unknown error')}")
    
    # Test 4: Request History
    print("\n4. Testing Request History...")
    history = client.test_request_history()
    if "error" in history:
        print(f"   ❌ History error: {history['error']}")
    else:
        print("   ✅ Request history retrieved successfully")
        history_count = len(history.get("history", []))
        print(f"   History entries: {history_count}")
    
    print("\n" + "=" * 60)
    print("🎉 Integration tests completed!")
    print("\n📖 Next Steps:")
    print("   1. Open http://localhost:8000 in your browser")
    print("   2. Try the travel planning interface")
    print("   3. Monitor agent status in real-time")
    print("   4. Test different destinations and preferences")
    
    return True

def test_individual_agents():
    """Test individual agent endpoints."""
    print("\n🔍 Testing Individual Agent Endpoints")
    print("=" * 60)
    
    agents = {
        "Travel Planner": "http://localhost:10001",
        "Hotel Agent": "http://localhost:10002",
        "Car Rental Agent": "http://localhost:10003"
    }
    
    for name, url in agents.items():
        print(f"\nTesting {name}...")
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name} is healthy")
            else:
                print(f"   ❌ {name} returned status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name} is not reachable: {e}")

if __name__ == "__main__":
    print("🚀 AG-UI Travel Planner Integration Test Suite")
    print("=" * 60)
    
    # Test individual agents first
    test_individual_agents()
    
    # Run integration tests
    success = run_integration_tests()
    
    if not success:
        print("\n❌ Integration tests failed")
        print("Please ensure all agents are running before testing")
        exit(1)
    else:
        print("\n✅ All tests passed!")
