@echo off
echo Starting AG-UI Travel Planner System...
echo ========================================

echo Starting Travel Planner Agent...
start "Travel Planner Agent" cmd /k "cd /d travel_planner_agent_adk && python simple_executor.py"

timeout /t 5 /nobreak >nul

echo Starting Hotel Booking Agent...
start "Hotel Booking Agent" cmd /k "cd /d hotel_booking_agent_crewai && python simple_executor.py"

timeout /t 5 /nobreak >nul

echo Starting Car Rental Agent...
start "Car Rental Agent" cmd /k "cd /d car_rental_agent_langgraph && python app/simple_executor.py"

timeout /t 10 /nobreak >nul

echo Starting AG-UI Server...
start "AG-UI Server" cmd /k "python start_ag_ui_server.py"

echo.
echo All agents are starting...
echo Please wait for all agents to fully start before using the system.
echo.
echo Once all agents are running, open your browser to: http://localhost:8000
echo.
pause
