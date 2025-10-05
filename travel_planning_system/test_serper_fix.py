#!/usr/bin/env python3
"""
Test script to verify the Serper API fix works.
This uses the exact format from the working Serper playground.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_serper_playground_format():
    """Test using the exact format from Serper playground."""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("❌ SERPER_API_KEY not found")
        return False
    
    print(f"🔑 Using API key: {serper_api_key[:10]}...")
    
    # Use the exact format from Serper playground
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": "Budget friendly hotels in PARIS from 11-11-2025 to 12-11-2025"
    })
    
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    
    print("🧪 Testing with Serper playground format...")
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! API call worked")
            print(f"📊 Results found: {len(data.get('organic', []))}")
            
            # Show first result
            if data.get('organic'):
                first_result = data['organic'][0]
                print(f"🏨 First hotel: {first_result.get('title', 'No title')}")
                print(f"🔗 Link: {first_result.get('link', 'No link')}")
            
            return True
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mcp_server_format():
    """Test using the MCP server format."""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("❌ SERPER_API_KEY not found")
        return False
    
    print(f"\n🧪 Testing with MCP server format...")
    
    url = "https://google.serper.dev/search"
    
    # MCP server format (Python dict)
    payload = {
        "q": "Budget friendly hotels in PARIS from 11-11-2025 to 12-11-2025",
        "num": 10
    }
    
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Use the fixed format (data=json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! MCP server format works")
            print(f"📊 Results found: {len(data.get('organic', []))}")
            return True
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function."""
    print("🔍 Testing Serper API Fix")
    print("=" * 50)
    
    # Test 1: Serper playground format
    print("Test 1: Serper Playground Format")
    playground_success = test_serper_playground_format()
    
    # Test 2: MCP server format
    print("\nTest 2: MCP Server Format")
    mcp_success = test_mcp_server_format()
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results:")
    print(f"Serper Playground Format: {'✅ PASS' if playground_success else '❌ FAIL'}")
    print(f"MCP Server Format: {'✅ PASS' if mcp_success else '❌ FAIL'}")
    
    if mcp_success:
        print("\n🎉 The MCP server fix works! Your 403 error should be resolved.")
    else:
        print("\n❌ The MCP server still has issues. Check your API key and account status.")
    
    return mcp_success

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All tests passed! Your Serper API is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check your API key and account status.")
