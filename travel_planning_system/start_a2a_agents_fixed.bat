@echo off
echo Starting A2A Multi-Agent Travel Planner System
echo ================================================

echo Starting Hotel Booking Agent...
start "Hotel Agent" cmd /k "cd /d C:\Users\nayak\Documents\agui\car_rental\Travel-Planner-Multi-Agent-A2A\travel_planning_system\hotel_booking_agent_crewai && python a2a_hotel_executor.py"

timeout /t 3 /nobreak > nul

echo Starting Car Rental Agent...
start "Car Agent" cmd /k "cd /d C:\Users\nayak\Documents\agui\car_rental\Travel-Planner-Multi-Agent-A2A\travel_planning_system\car_rental_agent_langgraph && python a2a_car_executor.py"

timeout /t 3 /nobreak > nul

echo Starting Travel Planner Agent...
start "Travel Planner Agent" cmd /k "cd /d C:\Users\nayak\Documents\agui\car_rental\Travel-Planner-Multi-Agent-A2A\travel_planning_system\travel_planner_agent_adk && python simple_a2a_executor.py"

echo All A2A agents started!
echo ================================================
echo Hotel Agent: http://localhost:10002
echo Car Agent: http://localhost:10003  
echo Travel Planner: http://localhost:10001
echo ================================================
pause
