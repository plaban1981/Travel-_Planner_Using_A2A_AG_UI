"""
Configuration settings for AG-UI Travel Planner Server.
"""
import os
from typing import Optional

class Settings:
    """Configuration settings for the AG-UI Travel Planner Server."""
    
    # AG-UI Server Settings
    ag_ui_host: str = "localhost"
    ag_ui_port: int = 8000
    
    # Travel Planner Agent Settings
    travel_planner_host: str = "localhost"
    travel_planner_port: int = 10001
    
    # Hotel Booking Agent Settings
    hotel_agent_host: str = "localhost"
    hotel_agent_port: int = 10002
    
    # Car Rental Agent Settings
    car_rental_agent_host: str = "localhost"
    car_rental_agent_port: int = 10003
    
    # API Keys
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    serper_api_key: Optional[str] = os.getenv("SERPER_API_KEY")
    
    # Agent URLs
    @property
    def travel_planner_url(self) -> str:
        return f"http://{self.travel_planner_host}:{self.travel_planner_port}"
    
    @property
    def hotel_agent_url(self) -> str:
        return f"http://{self.hotel_agent_host}:{self.hotel_agent_port}"
    
    @property
    def car_rental_agent_url(self) -> str:
        return f"http://{self.car_rental_agent_host}:{self.car_rental_agent_port}"
    
    # Agent Capabilities
    TRAVEL_PLANNER_CAPABILITIES = [
        "travel_planning",
        "itinerary_creation",
        "budget_estimation",
        "coordination"
    ]
    
    HOTEL_AGENT_CAPABILITIES = [
        "hotel_search",
        "hotel_booking",
        "price_comparison",
        "hotel_recommendations"
    ]
    
    CAR_RENTAL_CAPABILITIES = [
        "car_rental_search",
        "car_booking",
        "price_comparison",
        "car_recommendations"
    ]

# Global settings instance
settings = Settings()
