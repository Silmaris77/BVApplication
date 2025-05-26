"""
Content configuration for the BrainVenture application.
Defines settings related to the educational content.
"""

import os
import json
from config.app_config import APP_PATHS

def load_course_structure():
    """
    Load and return the course structure from the JSON file.
    """
    try:
        with open(os.path.join(APP_PATHS["course_structure_json"]), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading course structure: {e}")
        return []

def load_neuroleader_types():
    """
    Load and return all neuroleader types from the JSON file.
    """
    try:
        with open(os.path.join(APP_PATHS["neuroleader_types_json"]), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading neuroleader types: {e}")
        return []

def load_neuroleader_test():
    """
    Load and return the neuroleader test from the JSON file.
    """
    try:
        with open(os.path.join(APP_PATHS["neuroleader_test_json"]), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading neuroleader test: {e}")
        return {}

def get_neuroleader_type_details(type_id):
    """
    Get detailed information about a specific neuroleader type.
    
    Args:
        type_id (str): The ID of the neuroleader type.
        
    Returns:
        dict: Detailed information about the neuroleader type.
    """
    try:
        types = load_neuroleader_types()
        for t in types:
            if t.get("id") == type_id:
                # If there's a markdown file, load its content
                if "markdown_file" in t:
                    markdown_path = os.path.join(
                        APP_PATHS["content_dir"], "neuroleader_types", t["markdown_file"]
                    )
                    try:
                        with open(markdown_path, "r", encoding="utf-8") as f:
                            t["markdown_content"] = f.read()
                    except Exception as e:
                        print(f"Error loading markdown for {type_id}: {e}")
                        t["markdown_content"] = "Content not available"
                return t
        return None
    except Exception as e:
        print(f"Error getting neuroleader type details: {e}")
        return None

# Additional content settings
CONTENT_CONFIG = {
    "test_completion_threshold": 80,  # Percentage completion required for test results
    "lesson_completion_time": 5,  # Minutes required to mark a lesson as completed
    "enable_difficulty_levels": False,  # Not in MVP
    "max_lessons_per_day": 10,  # Recommended daily lesson limit
    "content_update_frequency_days": 30,  # How often new content is added
}
