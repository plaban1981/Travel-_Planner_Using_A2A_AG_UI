#!/usr/bin/env python3
"""
Test script to verify location handling in hotel search MCP server
"""

import json
import sys
import os

# Add the servers directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'servers'))

def test_hotel_search():
    """Test the hotel search function directly"""
    try:
        from hotel_search_mcp_server import search_hotels
        
        print("🧪 Testing Hotel Search Location Fix")
        print("=" * 50)
        
        # Test New York search
        print("\n🏙️ Testing New York search:")
        result = search_hotels("New York", "2025-10-06", "2025-10-08", "budget")
        data = json.loads(result)
        
        print(f"📊 Found {len(data)} results")
        for i, hotel in enumerate(data[:3], 1):
            print(f"{i}. {hotel.get('name', 'N/A')[:50]}...")
            print(f"   Location: {hotel.get('location', 'N/A')}")
            print(f"   Price: {hotel.get('estimated_cost_usd', 'N/A')}")
            print()
        
        # Test Paris search for comparison
        print("\n🗼 Testing Paris search:")
        result = search_hotels("Paris", "2025-10-06", "2025-10-08", "budget")
        data = json.loads(result)
        
        print(f"📊 Found {len(data)} results")
        for i, hotel in enumerate(data[:3], 1):
            print(f"{i}. {hotel.get('name', 'N/A')[:50]}...")
            print(f"   Location: {hotel.get('location', 'N/A')}")
            print(f"   Price: {hotel.get('estimated_cost_usd', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hotel_search()
