#!/usr/bin/env python3
"""
Comprehensive logging configuration for the travel planning system.
Replaces OpenTelemetry tracing with structured logging.
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class StructuredLogger:
    """Structured logger for the travel planning system."""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        """Initialize the structured logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure file handler
        if log_file:
            file_handler = logging.FileHandler(log_dir / log_file)
        else:
            file_handler = logging.FileHandler(log_dir / f"{name}.log")
        
        file_handler.setLevel(logging.INFO)
        
        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def trace(self, operation: str, details: Dict[str, Any], duration: Optional[float] = None):
        """Log a trace event with structured data."""
        trace_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "duration": duration,
            "type": "trace"
        }
        self.logger.info(f"TRACE: {json.dumps(trace_data)}")
    
    def error_trace(self, operation: str, error: str, details: Dict[str, Any]):
        """Log an error trace event."""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "error": error,
            "details": details,
            "type": "error_trace"
        }
        self.logger.error(f"ERROR_TRACE: {json.dumps(error_data)}")
    
    def performance_trace(self, operation: str, metrics: Dict[str, Any]):
        """Log a performance trace event."""
        perf_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "metrics": metrics,
            "type": "performance"
        }
        self.logger.info(f"PERFORMANCE: {json.dumps(perf_data)}")
    
    def info(self, message: str, **kwargs):
        """Log an info message."""
        if kwargs:
            self.logger.info(f"{message} - {json.dumps(kwargs)}")
        else:
            self.logger.info(message)
    
    def error(self, message: str, **kwargs):
        """Log an error message."""
        if kwargs:
            self.logger.error(f"{message} - {json.dumps(kwargs)}")
        else:
            self.logger.error(message)
    
    def warning(self, message: str, **kwargs):
        """Log a warning message."""
        if kwargs:
            self.logger.warning(f"{message} - {json.dumps(kwargs)}")
        else:
            self.logger.warning(message)

class TraceContext:
    """Context manager for tracing operations."""
    
    def __init__(self, logger: StructuredLogger, operation: str, details: Dict[str, Any]):
        """Initialize the trace context."""
        self.logger = logger
        self.operation = operation
        self.details = details
        self.start_time = None
    
    def __enter__(self):
        """Enter the trace context."""
        self.start_time = time.time()
        self.logger.trace(f"{self.operation}_start", self.details)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the trace context."""
        duration = time.time() - self.start_time if self.start_time else None
        
        if exc_type:
            self.logger.error_trace(f"{self.operation}_error", str(exc_val), self.details)
        else:
            self.logger.trace(f"{self.operation}_success", self.details, duration)

# Global loggers for different components
travel_planner_logger = StructuredLogger("travel_planner", "travel_planner.log")
hotel_agent_logger = StructuredLogger("hotel_agent", "hotel_agent.log")
car_rental_logger = StructuredLogger("car_rental", "car_rental.log")
ag_ui_logger = StructuredLogger("ag_ui", "ag_ui.log")

def get_logger(component: str) -> StructuredLogger:
    """Get a logger for a specific component."""
    loggers = {
        "travel_planner": travel_planner_logger,
        "hotel_agent": hotel_agent_logger,
        "car_rental": car_rental_logger,
        "ag_ui": ag_ui_logger
    }
    return loggers.get(component, StructuredLogger(component))

# Example usage functions
def trace_llm_call(logger: StructuredLogger, model: str, prompt: str, response: str, duration: float):
    """Trace an LLM call."""
    logger.performance_trace("llm_call", {
        "model": model,
        "prompt_length": len(prompt),
        "response_length": len(response),
        "duration": duration
    })

def trace_api_call(logger: StructuredLogger, service: str, endpoint: str, status_code: int, duration: float):
    """Trace an API call."""
    logger.performance_trace("api_call", {
        "service": service,
        "endpoint": endpoint,
        "status_code": status_code,
        "duration": duration
    })

def trace_agent_communication(logger: StructuredLogger, from_agent: str, to_agent: str, message: str, response: str, duration: float):
    """Trace agent-to-agent communication."""
    logger.trace("agent_communication", {
        "from_agent": from_agent,
        "to_agent": to_agent,
        "message_length": len(message),
        "response_length": len(response),
        "duration": duration
    })
