"""
Logging utilities for the BrainVenture application.
"""

import logging
import os
from datetime import datetime

# Set up logging configuration
class Logger:
    """
    Custom logger class for the BrainVenture application.
    """
    
    def __init__(self, name="brainventure", log_level=logging.INFO, log_to_file=True):
        """
        Initialize the logger.
        
        Args:
            name (str): Name for the logger
            log_level (int): Logging level (e.g., logging.INFO)
            log_to_file (bool): Whether to log to a file
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if enabled
        if log_to_file:
            # Create logs directory if it doesn't exist
            logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
            os.makedirs(logs_dir, exist_ok=True)
            
            # Create log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file = os.path.join(logs_dir, f"brainventure_{timestamp}.log")
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message, *args, **kwargs):
        """Log an info message."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log a warning message."""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log an error message."""
        self.logger.error(message, *args, **kwargs)
    
    def debug(self, message, *args, **kwargs):
        """Log a debug message."""
        self.logger.debug(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log a critical message."""
        self.logger.critical(message, *args, **kwargs)
    
    def log_user_activity(self, user_id, action, details=None):
        """
        Log user activity.
        
        Args:
            user_id (str): User ID
            action (str): Action performed (e.g., "login", "test_completed")
            details (dict, optional): Additional details about the action
        """
        log_data = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            log_data["details"] = details
        
        self.info(f"User Activity: {action}", extra={"user_activity": log_data})
    
    def log_error(self, error_type, error_message, details=None):
        """
        Log an application error.
        
        Args:
            error_type (str): Type of error
            error_message (str): Error message
            details (dict, optional): Additional details about the error
        """
        log_data = {
            "error_type": error_type,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            log_data["details"] = details
        
        self.error(f"Application Error: {error_type} - {error_message}", extra={"app_error": log_data})

# Create a default logger instance
default_logger = Logger()

def get_logger(name=None):
    """
    Get the application logger instance.
    
    Args:
        name (str, optional): Logger name. If provided, creates a new logger with the given name.
                             If None, returns the default logger.
    
    Returns:
        Logger: Application logger
    """
    if name is None:
        return default_logger
    else:
        return Logger(name=name)
