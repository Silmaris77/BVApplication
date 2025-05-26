"""
Error handling utilities for the BrainVenture application.
"""

import streamlit as st
import traceback
import sys
import os
import json
from datetime import datetime
import logging
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class BrainVentureError(Exception):
    """Base exception class for BrainVenture application."""
    
    def __init__(self, message, error_code=None, context=None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)
        
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

class ContentError(BrainVentureError):
    """Exception raised for errors related to content loading or processing."""
    pass

class ValidationError(BrainVentureError):
    """Exception raised for validation errors."""
    pass

class UserDataError(BrainVentureError):
    """Exception raised for user data errors."""
    pass

class ConfigurationError(BrainVentureError):
    """Exception raised for configuration errors."""
    pass

def handle_error(func):
    """
    Decorator to handle exceptions in function calls.
    
    Args:
        func: The function to decorate.
        
    Returns:
        The decorated function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BrainVentureError as e:
            logger.error(f"BrainVenture error: {str(e)}", exc_info=True)
            display_error(str(e), is_user_friendly=True)
            return None
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Data error: {str(e)}", exc_info=True)
            display_error("Wystąpił problem z danymi aplikacji. Prosimy o zgłoszenie problemu.")
            return None
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
            display_error("Wystąpił nieoczekiwany błąd. Prosimy o zgłoszenie problemu.")
            return None
    return wrapper

def display_error(message, is_user_friendly=False, exception_details=None):
    """
    Display an error message to the user.
    
    Args:
        message (str): The error message to display.
        is_user_friendly (bool): Whether the message is suitable for users.
        exception_details (Exception, optional): The exception details.
    """
    if is_user_friendly:
        st.error(message)
    else:
        st.error(message)
        
    # Log error with exception details if provided
    if exception_details:
        logger.error(f"Error displayed to user: {message}", exc_info=exception_details)

def log_error_to_file(error_type, error_message, stack_trace=None):
    """
    Log an error to the error log file.
    
    Args:
        error_type (str): Type of error.
        error_message (str): Error message.
        stack_trace (str, optional): Stack trace of the error.
    """
    timestamp = datetime.now().isoformat()
    error_log_dir = os.path.join("data", "logs")
    error_log_file = os.path.join(error_log_dir, "errors.log")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(error_log_dir):
        try:
            os.makedirs(error_log_dir)
        except Exception as e:
            logger.error(f"Failed to create log directory: {str(e)}")
            return
    
    # Log error to file
    try:
        with open(error_log_file, "a") as f:
            f.write(f"[{timestamp}] {error_type}: {error_message}\n")
            if stack_trace:
                f.write(f"Stack trace:\n{stack_trace}\n")
            f.write("-" * 80 + "\n")
    except Exception as e:
        logger.error(f"Failed to write to error log: {str(e)}")

def get_traceback():
    """
    Get the traceback of the current exception.
    
    Returns:
        str: The formatted traceback.
    """
    return traceback.format_exc()

def safe_load_json(file_path, default=None):
    """
    Safely load JSON file with error handling.
    
    Args:
        file_path (str): Path to the JSON file.
        default (any, optional): Default value to return if loading fails.
        
    Returns:
        dict: The loaded JSON data or default value.
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return default
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in {file_path}: {str(e)}")
        log_error_to_file("JSONDecodeError", f"Failed to parse {file_path}: {str(e)}")
        return default
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}", exc_info=True)
        log_error_to_file("FileLoadError", f"Failed to load {file_path}: {str(e)}", get_traceback())
        return default
        
def safe_save_json(data, file_path):
    """
    Safely save data to JSON file with error handling.
    
    Args:
        data (dict): Data to save.
        file_path (str): Path to save the JSON file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving to {file_path}: {str(e)}", exc_info=True)
        log_error_to_file("FileSaveError", f"Failed to save to {file_path}: {str(e)}", get_traceback())
        return False
