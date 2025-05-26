"""
Simple test for the UI setup_page function
"""
print("Starting UI test")

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from utils.ui import setup_page
    print("Successfully imported setup_page")
    
    # Check the function signature
    import inspect
    print(f"Function signature: {inspect.signature(setup_page)}")
    print("UI module imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")

print("Test completed")
