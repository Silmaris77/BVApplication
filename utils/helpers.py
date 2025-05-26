"""
Helper functions for the BrainVenture application.
"""

import json
import os
import re
import time
import random
from datetime import datetime, timedelta
import streamlit as st
from utils.logger import get_logger
from utils.error_handler import safe_load_json, safe_save_json, handle_error, UserDataError

# Initialize logger
logger = get_logger(__name__)

def format_time(seconds):
    """
    Format seconds into a human-readable time string.
    
    Args:
        seconds (int): Time in seconds.
        
    Returns:
        str: Formatted time string.
    """
    if seconds < 60:
        return f"{seconds} sec"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} min"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} h {minutes} min"

def calculate_progress(completed, total):
    """
    Calculate progress as a percentage.
    
    Args:
        completed (int): Number of completed items.
        total (int): Total number of items.
        
    Returns:
        float: Progress percentage (0-100).
    """
    if total == 0:
        return 0
    return min(100, round((completed / total) * 100, 1))

def slugify(text):
    """
    Convert text to slug format (lowercase, hyphens instead of spaces).
    
    Args:
        text (str): Text to convert.
        
    Returns:
        str: Slugified text.
    """
    # Remove special characters and replace spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')

def get_reading_time(text, words_per_minute=200):
    """
    Calculate estimated reading time for a text.
    
    Args:
        text (str): The text to analyze.
        words_per_minute (int): Average reading speed in words per minute.
        
    Returns:
        int: Estimated reading time in minutes.
    """
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes

def format_date(date_obj=None, format_str="%d-%m-%Y"):
    """
    Format a date object to string.
    
    Args:
        date_obj (datetime, optional): Date to format. Defaults to today.
        format_str (str): Format string.
        
    Returns:
        str: Formatted date string.
    """
    if date_obj is None:
        date_obj = datetime.now()
    return date_obj.strftime(format_str)

def parse_markdown_frontmatter(markdown_text):
    """
    Extract frontmatter from markdown.
    
    Args:
        markdown_text (str): Markdown text with frontmatter.
        
    Returns:
        tuple: (frontmatter_dict, content)
    """
    # Check if the markdown has frontmatter (between --- or +++)
    pattern = r'^(---|\+\+\+)$\n(.*?)^\1$\n(.*)$'
    match = re.match(pattern, markdown_text, re.DOTALL | re.MULTILINE)
    
    if not match:
        # No frontmatter found
        return {}, markdown_text
    
    try:
        # Extract the frontmatter and parse it
        frontmatter_str = match.group(2)
        content = match.group(3)
        
        # Try to parse as YAML or simple key-value pairs
        frontmatter = {}
        for line in frontmatter_str.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        
        return frontmatter, content.strip()
    
    except Exception:
        # If parsing fails, return empty dict and original content
        return {}, markdown_text

def extract_keywords(text, max_keywords=5):
    """
    Extract keywords from text.
    
    Args:
        text (str): Text to extract keywords from.
        max_keywords (int): Maximum number of keywords to extract.
        
    Returns:
        list: List of keywords.
    """
    # This is a simple implementation; in production, use a proper NLP library
    # Remove common stop words and punctuation, then take most frequent words
    stop_words = {
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
        "you", "your", "yours", "yourself", "yourselves", 
        "he", "him", "his", "himself", "she", "her", "hers", "herself", 
        "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
        "what", "which", "who", "whom", "this", "that", "these", "those", 
        "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", 
        "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", 
        "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", 
        "for", "with", "about", "against", "between", "into", "through", 
        "during", "before", "after", "above", "below", "to", "from", "up", "down", 
        "in", "out", "on", "off", "over", "under", "again", "further", "then", 
        "once", "here", "there", "when", "where", "why", "how", "all", "any", 
        "both", "each", "few", "more", "most", "other", "some", "such", "no", 
        "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
        "t", "can", "will", "just", "don", "don't", "should", "should've", "now", 
        "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", 
        "couldn't", "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", 
        "hasn't", "haven", "haven't", "isn", "isn't", "ma", "mightn", "mightn't", 
        "mustn", "mustn't", "needn", "needn't", "shan", "shan't", "shouldn", 
        "shouldn't", "wasn", "wasn't", "weren", "weren't", "won", "won't", "wouldn", 
        "wouldn't"
    }
    
    # Clean text and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count word frequency
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Sort by frequency
    keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Return top keywords
    return [word for word, _ in keywords[:max_keywords]]

@handle_error
def save_user_data(user_data, user_id="default_user"):
    """
    Save user data to file.
    
    Args:
        user_data (dict): User data to save.
        user_id (str, optional): User ID. Defaults to "default_user".
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Validate input
    if not user_data or not isinstance(user_data, dict):
        logger.warning("Invalid user data provided for saving")
        raise UserDataError("Invalid user data format")
      # In a full implementation, this would be a database operation
    # Get the absolute base path of the application
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    user_file_path = os.path.join(base_path, "data", "user_files", f"{user_id}.json")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(user_file_path), exist_ok=True)
    
    # Update last modified timestamp
    user_data["updated_at"] = datetime.now().isoformat()
    
    # Save the data using safe_save_json
    if safe_save_json(user_data, user_file_path):
        logger.info(f"User data saved successfully for user {user_id}")
        return True
    else:
        logger.error(f"Failed to save user data for user {user_id}")
        return False

@handle_error
def load_user_data(user_id="default_user"):
    """
    Load user data from file.
    
    Args:
        user_id (str, optional): User ID. Defaults to "default_user".
        
    Returns:
        dict: User data or default user data if not found.
    """
    # Get the absolute base path of the application
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    user_file_path = os.path.join(base_path, "data", "user_files", f"{user_id}.json")
    
    # Use safe_load_json to load the user data
    user_data = safe_load_json(user_file_path)
    
    if user_data:
        logger.info(f"User data loaded successfully for user {user_id}")
        return user_data
    
    # Return default user data if file doesn't exist or there's an error
    logger.info(f"Creating default user data for user {user_id}")
    
    # Create a new default user record
    default_user = {
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "profile": {
            "display_name": "Demo User",
            "email": "",
            "bio": "",
            "avatar": None,
        },
        "progress": {
            "completed_lessons": [],
            "last_activity": None,
            "tests_taken": [],
            "neuroleader_type": None
        },        "preferences": {
            "theme": "light",
            "notifications_enabled": True,
            "email_updates": False
        },
        "achievements": []
    }
    
    # Ensure the directory exists
    os.makedirs(os.path.join("data", "user_files"), exist_ok=True)
      # Save the default user data
    save_user_data(default_user, user_id)
    
    return default_user

def generate_achievement(name, description, icon):
    """
    Generate an achievement object.
    
    Args:
        name (str): Achievement name.
        description (str): Achievement description.
        icon (str): Achievement icon (emoji).
        
    Returns:
        dict: Achievement data.
    """
    return {
        "id": slugify(name),
        "name": name,
        "description": description,
        "icon": icon,
        "earned_at": format_date(datetime.now())
    }

def award_achievement(user_id, achievement_name, description, icon):
    """
    Award an achievement to a user.
    
    Args:
        user_id (str): User ID.
        achievement_name (str): Achievement name.
        description (str): Achievement description.
        icon (str): Achievement icon (emoji).
        
    Returns:
        bool: True if successful, False otherwise.
    """
    user_data = load_user_data(user_id)
    
    # Check if the user already has this achievement
    achievement_id = slugify(achievement_name)
    existing_achievements = [a.get("id") for a in user_data.get("achievements", [])]
    
    if achievement_id not in existing_achievements:
        # Add the achievement
        achievement = generate_achievement(achievement_name, description, icon)
        if "achievements" not in user_data:
            user_data["achievements"] = []
        user_data["achievements"].append(achievement)
        
        # Save the updated user data
        return save_user_data(user_data, user_id)
    
    return False

def get_user_achievements(user_id):
    """
    Get all achievements for a user.
    
    Args:
        user_id (str): User ID.
        
    Returns:
        list: User achievements.
    """
    user_data = load_user_data(user_id)
    return user_data.get("achievements", [])

def load_file(file_path, file_type=None):
    """
    Load content from a file based on its extension or specified type.
    
    Args:
        file_path (str): Path to the file to load
        file_type (str, optional): Force interpretation as specific type ('json', 'markdown', 'text', etc.)
                                 If None, will determine from file extension.
    
    Returns:
        The loaded content in appropriate Python format, or None if loading fails
    """
    import os
    import json
    import logging
    
    logger = get_logger(__name__)
    
    try:
        # Make sure the file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        # Determine file type if not specified
        if file_type is None:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            if ext == '.json':
                file_type = 'json'
            elif ext in ['.md', '.markdown']:
                file_type = 'markdown'
            elif ext in ['.txt', '.text']:
                file_type = 'text'
            elif ext in ['.py', '.python']:
                file_type = 'python'
            else:
                file_type = 'text'  # Default to text
        
        # Load file based on type
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_type == 'json':
                return json.load(f)
            elif file_type in ['text', 'markdown', 'python']:
                return f.read()
            else:
                # Default to reading as text
                return f.read()
                
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        return None
