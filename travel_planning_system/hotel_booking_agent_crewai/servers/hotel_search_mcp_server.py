from typing import Optional
import os
import requests
import json
import re
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel,Field
from dotenv import load_dotenv
load_dotenv()
from serper_config import serper_api_key
#
# Initialize FastMCP server
mcp = FastMCP("HotelSearchService")

class HotelSearchResult(BaseModel):
    """Input schema for HotelSearchTool."""

    location: str = Field(
        ...,
        description="The location/city to search for hotels in.",
    )
    check_in: str = Field(
        ...,
        description="Check-in date in YYYY-MM-DD format.",
    )
    check_out: str = Field(
        ...,
        description="Check-out date in YYYY-MM-DD format.",
    )
    budget: str = Field(
        default="any",
        description="Budget range (e.g., 'budget', 'mid-range', 'luxury', 'any').",
    )


@mcp.tool()
def search_hotels(location: str, check_in: str, check_out: str, budget: str = "any") -> str:
    """Search for hotels using SERPER API."""
    # Try to get API key from environment, fallback to hardcoded key
    #serper_api_key = os.getenv("SERPER_API_KEY") or "40005d9f557bfcecfbb4ed60a9b6ba6b2973e3a6"
    if not serper_api_key:
        return json.dumps({"error": "SERPER_API_KEY not found"})
    
    # Create a more specific search query to ensure location accuracy
    search_query = f"budget friendly hotels in {location} {budget} under $150 per night from {check_in} to {check_out}"
    if budget != "any":
        search_query = f"{budget} hotels in {location} under $150 per night from {check_in} to {check_out}"
    
    url = "https://google.serper.dev/search"
    print(f"🔍 Search Query: {search_query}")
    print(f"📍 Location: {location}")
    headers = {
            "X-API-KEY": serper_api_key,
            "Content-Type": "application/json"
        }
    payload = {
            "q": search_query,
            "num": 10
        }
        
    
    try:
        # Use the exact format that works in Serper playground
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        
        print(f"📊 API Response: {json.dumps(data, indent=2)[:500]}...")
        
        results = []
        if "organic" in data:
            for result in data["organic"][:5]:
                price_usd = None
                snippet = result.get("snippet", "")
                title = result.get("title", "")
                
                # Extract price from snippet
                price_match = re.search(r"\$([0-9]+[,.]?[0-9]*)", snippet)
                if price_match:
                    price_usd = f"${price_match.group(1)} USD"
                
                # Try to extract actual location from title or snippet
                actual_location = location  # Default to input location
                if location.lower() in title.lower() or location.lower() in snippet.lower():
                    actual_location = location
                elif "new york" in title.lower() or "new york" in snippet.lower():
                    actual_location = "New York"
                elif "paris" in title.lower() or "paris" in snippet.lower():
                    actual_location = "Paris"
                
                print(f"🏨 Hotel: {title[:50]}... | Location: {actual_location}")
                
                results.append({
                    "name": title,
                    "description": snippet,
                    "link": result.get("link", ""),
                    "location": actual_location,
                    "check_in": check_in,
                    "check_out": check_out,
                    "budget": budget,
                    "estimated_cost_usd": price_usd if price_usd else "N/A"
                })
        
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})

if __name__ == "__main__":
    mcp.run(transport="stdio")