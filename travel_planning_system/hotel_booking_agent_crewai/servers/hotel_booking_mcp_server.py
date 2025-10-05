import json
from mcp.server.fastmcp import FastMCP
from datetime import date
#
# Initialize FastMCP server
mcp = FastMCP("HotelBookingService")



@mcp.tool()
def booking_hotels(hotel_name: str, check_in: str, check_out: str, guests: int = 1) -> str:
    """Book a hotel room for specified dates and guests."""
    try:
        # Simulate hotel booking process
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
    except Exception as e:
        return json.dumps({"error": f"Booking failed: {str(e)}"})

if __name__ == "__main__":
    mcp.run(transport="stdio")