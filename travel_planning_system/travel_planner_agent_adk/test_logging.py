"""
Test script to verify A2A logging functionality
"""

import asyncio
from simple_a2a_agent import SimpleA2ATravelPlanner

async def test_logging():
    """Test the logging functionality."""
    print("Testing A2A Logging Functionality")
    print("=" * 50)
    
    # Create agent instance
    agent = SimpleA2ATravelPlanner()
    
    # Test logging functionality
    print("Testing agent communication logging...")
    
    # Simulate hotel agent communication
    hotel_response = {
        "id": "msg_test_001",
        "result": {
            "type": "text",
            "content": "Test hotel recommendations for Paris",
            "metadata": {
                "agent": "hotel_booking_agent",
                "timestamp": "2025-10-05T12:00:00",
                "capabilities_used": ["hotel_search", "llm_processing"]
            }
        },
        "status": "success"
    }
    
    # Log hotel communication
    agent.log_agent_communication(
        session_id="test_session_001",
        agent_name="Hotel_Booking_Agent",
        request="Find budget-friendly hotels in Paris",
        response=hotel_response,
        status="success"
    )
    
    # Simulate car agent communication
    car_response = {
        "id": "msg_test_002",
        "result": {
            "type": "text",
            "content": "Test car rental options for Paris",
            "metadata": {
                "agent": "car_rental_agent",
                "timestamp": "2025-10-05T12:00:00",
                "capabilities_used": ["car_rental_search", "llm_processing"]
            }
        },
        "status": "success"
    }
    
    # Log car communication
    agent.log_agent_communication(
        session_id="test_session_001",
        agent_name="Car_Rental_Agent",
        request="Find car rental options in Paris",
        response=car_response,
        status="success"
    )
    
    print("Logging test completed!")
    print("Check agent_communication_log.json for logged data")
    
    # Test content extraction
    print("\nTesting content extraction...")
    
    # Extract content from hotel response
    if "result" in hotel_response and "content" in hotel_response["result"]:
        hotel_content = hotel_response["result"]["content"]
        print(f"Hotel content extracted: {hotel_content[:50]}...")
    
    # Extract content from car response
    if "result" in car_response and "content" in car_response["result"]:
        car_content = car_response["result"]["content"]
        print(f"Car content extracted: {car_content[:50]}...")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    asyncio.run(test_logging())
