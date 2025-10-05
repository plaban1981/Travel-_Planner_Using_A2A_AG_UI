#!/usr/bin/env python3
"""
Simplified Car Rental Agent without LangGraph dependencies.
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

class CarRentalAgent:
    """Simplified Car Rental Agent using Groq LLM."""
    
    def __init__(self):
        """Initialize the car rental agent."""
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
        self.serper_api_key = os.getenv("SERPER_API_KEY")
    
    def search_car_rentals(self, location: str, start_date: str, end_date: str, budget: str = "any") -> str:
        """Search for car rentals using SerperAPI."""
        if not self.serper_api_key:
            return json.dumps({"error": "SERPER_API_KEY not found"})
        
        search_query = f"car rental in {location} from {start_date} to {end_date}"
        if budget != "any":
            search_query += f" {budget} budget"
        
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
                        "start_date": start_date,
                        "end_date": end_date,
                        "budget": budget,
                        "estimated_cost_usd": price_usd if price_usd else "N/A"
                    })
            
            return json.dumps(results, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Search failed: {str(e)}"})
    
    def book_car_rental(self, car_name: str, location: str, start_date: str, end_date: str, driver_age: int = 25) -> str:
        """Simulate car rental booking process."""
        booking_id = f"CR{date.today().strftime('%Y%m%d')}{hash(car_name) % 10000:04d}"
        
        booking = {
            "booking_id": booking_id,
            "car_name": car_name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "driver_age": driver_age,
            "status": "confirmed",
            "booking_date": date.today().isoformat()
        }
        
        return json.dumps(booking, indent=2)
    
    def process_request(self, message: str) -> str:
        """Process a car rental request using LLM."""
        try:
            # Use LLM to understand the request and extract information
            prompt = f"""
            Analyze this car rental request: "{message}"
            
            Extract the following information:
            1. Location (city/country)
            2. Start date (YYYY-MM-DD format)
            3. End date (YYYY-MM-DD format)
            4. Budget preference (budget/mid-range/luxury/any)
            5. Driver age (if mentioned)
            
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
                    "start_date": "2025-10-06",
                    "end_date": "2025-10-07",
                    "budget": "any",
                    "driver_age": 25
                }
            
            # Search for car rentals
            search_results = self.search_car_rentals(
                extracted_info.get("location", "Paris"),
                extracted_info.get("start_date", "2025-10-06"),
                extracted_info.get("end_date", "2025-10-07"),
                extracted_info.get("budget", "any")
            )
            
            # Generate a comprehensive response
            final_response = f"""
**Car Rental Options for {extracted_info.get('location', 'Paris')}**

{search_results}

**Booking Information:**
- Start Date: {extracted_info.get('start_date', '2025-10-06')}
- End Date: {extracted_info.get('end_date', '2025-10-07')}
- Driver Age: {extracted_info.get('driver_age', 25)}
- Budget: {extracted_info.get('budget', 'any')}

**Next Steps:**
To book a car rental, please specify:
1. The car rental company you prefer
2. Your contact information
3. Any special requirements

This response was generated using the Simplified Car Rental Agent with Groq LLM.
            """
            
            return final_response
            
        except Exception as e:
            return f"Error processing car rental request: {str(e)}"

# Global agent instance
car_rental_agent = CarRentalAgent()

def get_car_rental_agent():
    """Get the car rental agent instance."""
    return car_rental_agent
