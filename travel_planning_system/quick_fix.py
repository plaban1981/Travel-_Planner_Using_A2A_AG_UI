#!/usr/bin/env python3
"""
Quick fix script for environment variable issues.
This script will help you set up the .env file properly.
"""

import os
import sys
from pathlib import Path

def main():
    print("🔧 Quick Fix for AG-UI Travel Planner Environment")
    print("=" * 60)
    
    # Check if .env file exists
    env_file = Path(".env")
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        
        # Get API keys from user
        print("\nPlease enter your API keys:")
        groq_key = input("Enter your GROQ_API_KEY: ").strip()
        serper_key = input("Enter your SERPER_API_KEY: ").strip()
        
        if not groq_key or not serper_key:
            print("❌ API keys cannot be empty. Please try again.")
            return False
        
        # Create .env file
        env_content = f"""# Environment variables for AG-UI Travel Planner System
GROQ_API_KEY={groq_key}
SERPER_API_KEY={serper_key}

# Optional: Server Configuration
AG_UI_HOST=localhost
AG_UI_PORT=8000
TRAVEL_PLANNER_HOST=localhost
TRAVEL_PLANNER_PORT=10001
HOTEL_AGENT_HOST=localhost
HOTEL_AGENT_PORT=10002
CAR_RENTAL_AGENT_HOST=localhost
CAR_RENTAL_AGENT_PORT=10003
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ .env file created successfully!")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    # Test environment loading
    print("\n🔍 Testing environment variable loading...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        serper_key = os.getenv("SERPER_API_KEY")
        
        if groq_key and serper_key and groq_key != "your_groq_api_key_here" and serper_key != "your_serper_api_key_here":
            print("✅ Environment variables loaded successfully!")
            print(f"   GROQ_API_KEY: {groq_key[:10]}...")
            print(f"   SERPER_API_KEY: {serper_key[:10]}...")
        else:
            print("❌ Environment variables not properly set")
            print("Please edit the .env file and add your actual API keys")
            return False
            
    except ImportError:
        print("❌ python-dotenv not installed. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
            print("✅ python-dotenv installed successfully")
            print("Please run this script again")
            return False
        except Exception as e:
            print(f"❌ Error installing python-dotenv: {e}")
            return False
    
    print("\n🎉 Environment setup complete!")
    print("You can now run: python start_complete_system.py")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
