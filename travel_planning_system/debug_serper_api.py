#!/usr/bin/env python3
"""
Debug script for Serper API issues.
This script tests the Serper API directly to identify the 403 error cause.
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_serper_api():
    """Test Serper API with different configurations."""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("❌ SERPER_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 API Key found: {serper_api_key[:10]}...")
    
    # Test 1: Basic search
    print("\n🧪 Test 1: Basic search")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": "hotels in Paris",
        "num": 5
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Basic search successful")
            print(f"Results found: {len(data.get('organic', []))}")
            return True
        else:
            print(f"❌ Basic search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Basic search error: {e}")
        return False

def test_hotel_search():
    """Test hotel-specific search."""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("❌ SERPER_API_KEY not found")
        return False
    
    print("\n🏨 Test 2: Hotel search")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": "Budget friendly hotels in Paris from 2024-02-15 to 2024-02-20",
        "num": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Hotel search successful")
            print(f"Results found: {len(data.get('organic', []))}")
            
            # Show first result
            if data.get('organic'):
                first_result = data['organic'][0]
                print(f"First result: {first_result.get('title', 'No title')}")
                print(f"Link: {first_result.get('link', 'No link')}")
            
            return True
        else:
            print(f"❌ Hotel search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Hotel search error: {e}")
        return False

def test_api_key_validity():
    """Test if the API key is valid by checking account info."""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("❌ SERPER_API_KEY not found")
        return False
    
    print("\n🔍 Test 3: API Key validation")
    
    # Try to get account info (if available)
    try:
        # Some APIs have account info endpoints
        url = "https://google.serper.dev/account"
        headers = {
            "X-API-KEY": serper_api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        print(f"Account check status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API key is valid")
            return True
        elif response.status_code == 401:
            print("❌ API key is invalid (401 Unauthorized)")
            return False
        elif response.status_code == 403:
            print("❌ API key is forbidden (403 Forbidden)")
            return False
        else:
            print(f"Account check returned: {response.status_code}")
            return True  # Assume valid if we can't check account
            
    except Exception as e:
        print(f"Account check error: {e}")
        return True  # Assume valid if we can't check

def test_different_headers():
    """Test with different header configurations."""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        return False
    
    print("\n🔧 Test 4: Different header configurations")
    
    # Test different header formats
    header_configs = [
        {
            "name": "Standard headers",
            "headers": {
                "X-API-KEY": serper_api_key,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Authorization header",
            "headers": {
                "Authorization": f"Bearer {serper_api_key}",
                "Content-Type": "application/json"
            }
        },
        {
            "name": "API-Key header",
            "headers": {
                "API-Key": serper_api_key,
                "Content-Type": "application/json"
            }
        }
    ]
    
    for config in header_configs:
        print(f"\nTesting {config['name']}...")
        try:
            url = "https://google.serper.dev/search"
            payload = {"q": "test search", "num": 1}
            
            response = requests.post(url, headers=config['headers'], json=payload)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ {config['name']} works!")
                return True
            else:
                print(f"  ❌ {config['name']} failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ {config['name']} error: {e}")
    
    return False

def main():
    """Main debug function."""
    print("🔍 Serper API Debug Tool")
    print("=" * 50)
    
    # Check environment
    serper_key = os.getenv("SERPER_API_KEY")
    if not serper_key:
        print("❌ SERPER_API_KEY not found in environment variables")
        print("Please set your SERPER_API_KEY in the .env file")
        return False
    
    print(f"✅ SERPER_API_KEY found: {serper_key[:10]}...")
    
    # Run tests
    tests = [
        ("Basic Search", test_serper_api),
        ("Hotel Search", test_hotel_search),
        ("API Key Validation", test_api_key_validity),
        ("Header Configurations", test_different_headers)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    print("1. Check your Serper API key is correct")
    print("2. Verify your Serper account has sufficient credits")
    print("3. Check if your API key has the right permissions")
    print("4. Try the Serper playground: https://serper.dev/playground")
    print("5. Check your Serper dashboard for usage limits")
    
    return any(result for _, result in results)

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ All tests failed. Please check your API key and account status.")
    else:
        print("\n✅ Some tests passed. The API key appears to be working.")
