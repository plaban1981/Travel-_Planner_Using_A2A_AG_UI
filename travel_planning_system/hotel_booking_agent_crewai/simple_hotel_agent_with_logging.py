#!/usr/bin/env python3
"""
Simplified Hotel Booking Agent with proper logging and tracing.
Uses direct HTTP communication, Groq LLM, and structured logging.
"""

import os
import json
import requests
import logging
import time
from datetime import date
from typing import Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hotel_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class HotelBookingAgent:
    """Simplified Hotel Booking Agent with logging and tracing."""
    
    def __init__(self):
        """Initialize the hotel booking agent."""
        logger.info("Initializing Hotel Booking Agent")
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            logger.error("GROQ_API_KEY not found")
            raise ValueError("GROQ_API_KEY not found")
        
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
        logger.info("Hotel Booking Agent initialized successfully")
    
    def _log_trace(self, operation: str, details: Dict[str, Any]):
        """Log a trace event with structured data."""
        trace_data = {
            "timestamp": time.time(),
            "operation": operation,
            "details": details,
            "agent": "hotel_booking_agent"
        }
        logger.info(f"TRACE: {json.dumps(trace_data)}")
    
    def search_hotels(self, location: str, check_in: str, check_out: str, budget: str = "any") -> str:
        """Search for hotels using SerperAPI with logging."""
        self._log_trace("search_hotels_start", {
            "location": location,
            "check_in": check_in,
            "check_out": check_out,
            "budget": budget
        })
        
        if not self.serper_api_key:
            logger.error("SERPER_API_KEY not found")
            return json.dumps({"error": "SERPER_API_KEY not found"})
        
        search_query = f"budget friendly hotels in {location} from {check_in} to {check_out}"
        if budget != "any":
            search_query += f" {budget} hotels"
        
        logger.info(f"Searching for hotels with query: {search_query}")
        
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
            start_time = time.time()
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            
            search_duration = time.time() - start_time
            logger.info(f"Hotel search completed in {search_duration:.2f} seconds")
            
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
            
            self._log_trace("search_hotels_success", {
                "results_count": len(results),
                "search_duration": search_duration,
                "location": location
            })
            
            return json.dumps(results, indent=2)
        except Exception as e:
            logger.error(f"Hotel search failed: {str(e)}")
            self._log_trace("search_hotels_error", {
                "error": str(e),
                "location": location
            })
            return json.dumps({"error": f"Search failed: {str(e)}"})
    
    def book_hotel(self, hotel_name: str, check_in: str, check_out: str, guests: int = 1) -> str:
        """Simulate hotel booking process with logging."""
        self._log_trace("book_hotel_start", {
            "hotel_name": hotel_name,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests
        })
        
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
        
        logger.info(f"Hotel booking created: {booking_id}")
        self._log_trace("book_hotel_success", {
            "booking_id": booking_id,
            "hotel_name": hotel_name
        })
        
        return json.dumps(booking, indent=2)
    
    def process_request(self, message: str) -> str:
        """Process a hotel booking request using LLM with logging."""
        self._log_trace("process_request_start", {
            "message": message,
            "message_length": len(message)
        })
        
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
            
            logger.info("Sending request to LLM for analysis")
            start_time = time.time()
            response = self.llm.invoke(prompt)
            llm_duration = time.time() - start_time
            
            logger.info(f"LLM response received in {llm_duration:.2f} seconds")
            
            # Try to parse the response as JSON
            try:
                extracted_info = json.loads(response.content)
                logger.info("Successfully parsed LLM response as JSON")
            except:
                logger.warning("Failed to parse LLM response as JSON, using defaults")
                # If JSON parsing fails, use simple extraction
                extracted_info = {
                    "location": "Paris",  # Default
                    "check_in": "2025-10-06",
                    "check_out": "2025-10-07",
                    "guests": 2,
                    "budget": "any"
                }
            
            self._log_trace("llm_analysis_complete", {
                "extracted_info": extracted_info,
                "llm_duration": llm_duration
            })
            
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
            
            self._log_trace("process_request_success", {
                "response_length": len(final_response),
                "location": extracted_info.get("location", "Paris")
            })
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error processing hotel booking request: {str(e)}")
            self._log_trace("process_request_error", {
                "error": str(e),
                "message": message
            })
            return f"Error processing hotel booking request: {str(e)}"

# Global agent instance
hotel_booking_agent = HotelBookingAgent()

def get_hotel_booking_agent():
    """Get the hotel booking agent instance."""
    return hotel_booking_agent
