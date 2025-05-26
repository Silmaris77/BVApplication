"""
Validation utilities for the BrainVenture application.
"""

import re
import os

def validate_email(email):
    """
    Validate email address.
    
    Args:
        email (str): Email address to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate.
        
    Returns:
        tuple: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    has_number = any(char.isdigit() for char in password)
    has_letter = any(char.isalpha() for char in password)
    has_special = any(not char.isalnum() for char in password)
    
    if not (has_number and has_letter):
        return False, "Password must include both letters and numbers."
    
    if not has_special:
        return False, "Password should include at least one special character."
    
    return True, "Password is strong."

def validate_username(username):
    """
    Validate username.
    
    Args:
        username (str): Username to validate.
        
    Returns:
        tuple: (is_valid, message)
    """
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    
    if len(username) > 30:
        return False, "Username must be no more than 30 characters long."
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens."
    
    return True, "Username is valid."

def validate_form_data(data, required_fields=None):
    """
    Validate form data.
    
    Args:
        data (dict): Form data to validate.
        required_fields (list, optional): List of required field names.
        
    Returns:
        tuple: (is_valid, errors_dict)
    """
    if required_fields is None:
        required_fields = []
    
    errors = {}
    
    # Check required fields
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f"{field.replace('_', ' ').capitalize()} is required."
    
    # Special validations
    if "email" in data and data["email"]:
        if not validate_email(data["email"]):
            errors["email"] = "Please enter a valid email address."
    
    if "password" in data and data["password"]:
        valid, message = validate_password(data["password"])
        if not valid:
            errors["password"] = message
    
    if "username" in data and data["username"]:
        valid, message = validate_username(data["username"])
        if not valid:
            errors["username"] = message
    
    # If confirm_password is present, check it matches password
    if "password" in data and "confirm_password" in data:
        if data["password"] != data["confirm_password"]:
            errors["confirm_password"] = "Passwords do not match."
    
    return len(errors) == 0, errors

def validate_file_upload(file, allowed_extensions=None, max_size_mb=5):
    """
    Validate file upload.
    
    Args:
        file: File object from st.file_uploader.
        allowed_extensions (list, optional): List of allowed file extensions.
        max_size_mb (int): Maximum file size in MB.
        
    Returns:
        tuple: (is_valid, message)
    """
    if allowed_extensions is None:
        allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf']
    
    if file is None:
        return False, "No file uploaded."
    
    # Get file extension
    file_extension = os.path.splitext(file.name)[1][1:].lower()
    
    # Check file extension
    if file_extension not in allowed_extensions:
        return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}."
    
    # Check file size (convert bytes to MB)
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File size exceeds the maximum allowed ({max_size_mb} MB)."
    
    return True, "File is valid."

def sanitize_input(input_str):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        input_str (str): User input to sanitize.
        
    Returns:
        str: Sanitized input.
    """
    # Replace potentially dangerous characters
    sanitized = input_str
    
    # Replace < and > with their HTML entities
    sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")
    
    # Replace single and double quotes
    sanitized = sanitized.replace('"', "&quot;").replace("'", "&#39;")
    
    # Remove any script tags just to be super safe
    sanitized = re.sub(r'<\s*script.*?>.*?<\s*/\s*script\s*>', '', sanitized, flags=re.DOTALL)
    
    return sanitized

def validate_test_answers(answers, question_count):
    """
    Validate test answers.
    
    Args:
        answers (dict): User answers as {question_id: answer_value}.
        question_count (int): Total number of questions.
        
    Returns:
        tuple: (is_valid, completion_percentage, message)
    """
    # Count valid answers
    valid_answers = [q_id for q_id, answer in answers.items() if answer is not None]
    answered_count = len(valid_answers)
    
    # Calculate completion percentage
    completion_percentage = (answered_count / question_count) * 100
    
    # Check if enough questions were answered
    if completion_percentage < 70:
        return (
            False, 
            completion_percentage, 
            f"Please answer at least 70% of the questions. Current: {completion_percentage:.0f}%"
        )
    
    return True, completion_percentage, "Test answers are valid."
