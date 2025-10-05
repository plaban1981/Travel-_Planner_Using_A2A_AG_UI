import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from datetime import date
from dotenv import load_dotenv

load_dotenv()




class HotelBookingAgent:
    """Agent that handles hotel booking tasks using MCP tools."""

    SUPPORTED_CONTENT_TYPES = ["text/plain"]

    def __init__(self):
        """Initializes the HotelBookingAgent with MCP tools."""
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")

        self.llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=groq_api_key
        )

        # Configure MCP server parameters for search functionality
        search_server_params = StdioServerParameters(
            command="python",
            args=["servers/hotel_search_mcp_server.py"],
            env={"UV_PYTHON": "3.12", **os.environ},
        )

        # Configure MCP server parameters for booking functionality
        booking_server_params = StdioServerParameters(
            command="python",
            args=["servers/hotel_booking_mcp_server.py"],
            env={"UV_PYTHON": "3.12", **os.environ},
        )

        # Get MCP tools using context manager for automatic connection management
        # Combine tools from multiple servers
        with MCPServerAdapter(search_server_params) as search_tools, MCPServerAdapter(booking_server_params) as booking_tools:
            all_tools = [*search_tools, *booking_tools]
            
            self.hotel_booking_assistant = Agent(
                role="Hotel Booking Specialist",
                goal="Find and book the best hotels for travelers based on their preferences and requirements.",
                backstory=(
                    "You are an expert hotel booking specialist with years of experience in the travel industry. "
                    "You have extensive knowledge of hotels worldwide and can find the perfect accommodation "
                    "for any traveler's needs. You use advanced search tools to find current availability and "
                    "pricing, and you can handle bookings efficiently."
                ),
                verbose=True,
                allow_delegation=False,
                tools=all_tools,  # Use MCP tools instead of custom BaseTool
                llm=self.llm,
            )

    def invoke(self, question: str) -> str:
        """Kicks off the crew to answer a hotel booking question."""
        # Configure MCP server parameters for search functionality
        search_server_params = StdioServerParameters(
            command="python",
            args=["servers/hotel_search_mcp_server.py"],
            env={"UV_PYTHON": "3.12", **os.environ},
        )

        # Configure MCP server parameters for booking functionality
        booking_server_params = StdioServerParameters(
            command="python",
            args=["servers/hotel_booking_mcp_server.py"],
            env={"UV_PYTHON": "3.12", **os.environ},
        )

        # Get MCP tools using context manager for automatic connection management
        # Combine tools from multiple servers
        with MCPServerAdapter(search_server_params) as search_tools, MCPServerAdapter(booking_server_params) as booking_tools:
            all_tools = [*search_tools, *booking_tools]
            
            # Create agent with MCP tools
            hotel_booking_assistant = Agent(
                role="Hotel Booking Specialist",
                goal="Find and book the best hotels for travelers based on their preferences and requirements.",
                backstory=(
                    "You are an expert hotel booking specialist with years of experience in the travel industry. "
                    "You have extensive knowledge of hotels worldwide and can find the perfect accommodation "
                    "for any traveler's needs. You use advanced search tools to find current availability and "
                    "pricing, and you can handle bookings efficiently."
                ),
                verbose=True,
                allow_delegation=False,
                tools=all_tools,
                llm=self.llm,
            )

            task_description = (
                f"Help the user with their hotel booking request. The user asked: '{question}'. "
                f"Today's date is {date.today().strftime('%Y-%m-%d')}. "
                f"Use the available search tools to find hotels and provide booking options."
            )

            hotel_booking_task = Task(
                description=task_description,
                expected_output="A list of available hotels with details and pricing",
                agent=hotel_booking_assistant,
            )

            crew = Crew(
                agents=[hotel_booking_assistant],
                tasks=[hotel_booking_task],
                process=Process.sequential,
                verbose=True,
            )
            
            result = crew.kickoff()
            print(f"Hotel response CREWAI: {result.raw}")
            return result.raw