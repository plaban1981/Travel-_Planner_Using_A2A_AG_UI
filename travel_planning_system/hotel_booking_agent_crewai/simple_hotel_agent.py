#!/usr/bin/env python3
"""
Simplified Hotel Booking Agent without CrewAI dependencies.
Uses direct HTTP communication and Groq LLM.
"""

import os
import json
import requests
from datetime import date
from typing import Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class HotelBookingAgent:
    """Simplified Hotel Booking Agent using Groq LLM."""
    
    def __init__(self):
        """Initialize the hotel booking agent."""
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
        self.serper_api_key = os.getenv("SERPER_API_KEY")
    
    def search_hotels(self, location: str, check_in: str, check_out: str, budget: str = "any") -> str:
        """Search for hotels using SerperAPI."""
        if not self.serper_api_key:
            return json.dumps({"error": "SERPER_API_KEY not found"})
        
        search_query = f"budget friendly hotels in {location} from {check_in} to {check_out}"
        if budget != "any":
            search_query += f" {budget} hotels"
        
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": search_query,
            "num": 10
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "organic" in data:
                for result in data["organic"][:5]:
                    price_usd = None
                    snippet = result.get("snippet", "")
                    import re
                    price_match = re.search(r"\$([0-9]+[,.]?[0-9]*)", snippet)
                    if price_match:
                        price_usd = f"${price_match.group(1)} USD"
                    
                    results.append({
                        "name": result.get("title", ""),
                        "description": snippet,
                        "link": result.get("link", ""),
                        "location": location,
                        "check_in": check_in,
                        "check_out": check_out,
                        "budget": budget,
                        "estimated_cost_usd": price_usd if price_usd else "N/A"
                    })
            
            return json.dumps(results, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Search failed: {str(e)}"})
    
    def book_hotel(self, hotel_name: str, check_in: str, check_out: str, guests: int = 1) -> str:
        """Simulate hotel booking process."""
        booking_id = f"HB{date.today().strftime('%Y%m%d')}{hash(hotel_name) % 10000:04d}"
        
        booking = {
            "booking_id": booking_id,
            "hotel_name": hotel_name,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "status": "confirmed",
            "booking_date": date.today().isoformat()
        }
        
        return json.dumps(booking, indent=2)
    
    def process_request(self, message: str) -> str:
        """Process a hotel booking request using LLM."""
        try:
            # Use LLM to understand the request and extract information
            prompt = f"""
            Analyze this hotel booking request: "{message}"
            
            Extract the following information:
            1. Location (city/country)
            2. Check-in date (YYYY-MM-DD format)
            3. Check-out date (YYYY-MM-DD format)
            4. Number of guests
            5. Budget preference (budget/mid-range/luxury/any)
            
            Return a JSON response with the extracted information.
            If any information is missing, use reasonable defaults.
            """
            
            response = self.llm.invoke(prompt)
            
            # Try to parse the response as JSON
            try:
                extracted_info = json.loads(response.content)
            except:
                # If JSON parsing fails, use simple extraction
                extracted_info = {
                    "location": "Paris",  # Default
                    "check_in": "2025-10-06",
                    "check_out": "2025-10-07",
                    "guests": 2,
                    "budget": "any"
                }
            
            # Search for hotels
            search_results = self.search_hotels(
                extracted_info.get("location", "Paris"),
                extracted_info.get("check_in", "2025-10-06"),
                extracted_info.get("check_out", "2025-10-07"),
                extracted_info.get("budget", "any")
            )
            
            # Generate a comprehensive response
            final_response = f"""
**Hotel Recommendations for {extracted_info.get('location', 'Paris')}**

{search_results}

**Booking Information:**
- Check-in: {extracted_info.get('check_in', '2025-10-06')}
- Check-out: {extracted_info.get('check_out', '2025-10-07')}
- Guests: {extracted_info.get('guests', 2)}
- Budget: {extracted_info.get('budget', 'any')}

**Next Steps:**
To book a hotel, please specify:
1. The hotel you prefer
2. Your contact information
3. Any special requirements

This response was generated using the Simplified Hotel Booking Agent with Groq LLM.
            """
            
            return final_response
            
        except Exception as e:
            return f"Error processing hotel booking request: {str(e)}"

# Global agent instance
hotel_booking_agent = HotelBookingAgent()

def get_hotel_booking_agent():
    """Get the hotel booking agent instance."""
    return hotel_booking_agent