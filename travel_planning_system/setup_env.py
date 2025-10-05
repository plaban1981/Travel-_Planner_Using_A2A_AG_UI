#!/usr/bin/env python3
"""
Environment setup script for AG-UI Travel Planner System.
This script helps you create the .env file with the required API keys.
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with required environment variables."""
    
    env_content = """# Environment variables for AG-UI Travel Planner System
# Replace the placeholder values with your actual API keys

GROQ_API_KEY="your_groq_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"

# Optional: AG-UI Server Configuration
AG_UI_HOST=localhost
AG_UI_PORT=8000

# Optional: Agent Configuration
TRAVEL_PLANNER_HOST=localhost
TRAVEL_PLANNER_PORT=10001
HOTEL_AGENT_HOST=localhost
HOTEL_AGENT_PORT=10002
CAR_RENTAL_AGENT_HOST=localhost
CAR_RENTAL_AGENT_PORT=10003
"""
    
    env_file_path = Path(".env")
    
    if env_file_path.exists():
        print("✅ .env file already exists")
        return True
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("\n📝 Next steps:")
        print("1. Edit the .env file and replace the placeholder values:")
        print("   - GROQ_API_KEY=your_actual_groq_api_key")
        print("   - SERPER_API_KEY=your_actual_serper_api_key")
        print("2. Save the file")
        print("3. Run: python start_complete_system.py")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_env_vars():
    """Check if environment variables are properly set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["GROQ_API_KEY", "SERPER_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == "your_groq_api_key_here" or value == "your_serper_api_key_here":
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing or invalid environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    """Main setup function."""
    print("🔧 AG-UI Travel Planner Environment Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("📝 Creating .env file...")
        if not create_env_file():
            return False
    
    # Load and check environment variables
    print("\n🔍 Checking environment variables...")
    if check_env_vars():
        print("\n✅ Environment setup complete!")
        print("You can now run: python start_complete_system.py")
        return True
    else:
        print("\n❌ Please update your .env file with valid API keys")
        print("Edit the .env file and replace the placeholder values with your actual API keys")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
