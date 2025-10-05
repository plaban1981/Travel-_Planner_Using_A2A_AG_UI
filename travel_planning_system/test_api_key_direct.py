#!/usr/bin/env python3
"""
Direct test of the Serper API key to verify it works.
"""

import requests
import json

def test_api_key_direct():
    """Test the API key directly without any environment variables."""
    
    # Use the exact API key from your working Serper playground
    api_key = "40005d9f557bfcecfbb4ed60a9b6ba6b2973e3a6"
    
    print(f"🔑 Testing API key: {api_key[:10]}...")
    
    url = "https://google.serper.dev/search"
    
    # Use the exact format from your working Serper playground
    payload = json.dumps({
        "q": "Budget friendly hotels in PARIS from 11-11-2025 to 12-11-2025"
    })
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    print(f"🌐 URL: {url}")
    print(f"📋 Headers: {headers}")
    print(f"📦 Payload: {payload}")
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! API key works")
            print(f"📊 Results found: {len(data.get('organic', []))}")
            
            # Show first result
            if data.get('organic'):
                first_result = data['organic'][0]
                print(f"🏨 First hotel: {first_result.get('title', 'No title')}")
                print(f"🔗 Link: {first_result.get('link', 'No link')}")
            
            return True
        else:
            print(f"❌ FAILED with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Direct API Key Test")
    print("=" * 50)
    
    success = test_api_key_direct()
    
    if success:
        print("\n✅ API key works! The issue is with the MCP environment.")
        print("💡 Try using the debug MCP server: hotel_search_mcp_server_debug.py")
    else:
        print("\n❌ API key doesn't work. Check your Serper account status.")
