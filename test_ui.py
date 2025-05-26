"""
Test script to verify the ui.py setup_page function is working correctly.
"""

import sys
import os
import traceback

# Add the project directory to the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Print a message indicating the test is starting
print("Testing setup_page function...")

# Define a wrapper function to test importing the module
def test_import():
    try:
        from utils.ui import setup_page
        print("✓ Module import successful")
        return setup_page
    except Exception as e:
        print(f"✗ Module import failed: {str(e)}")
        traceback.print_exc()
        return None

# First try to import the module
setup_page = test_import()
if not setup_page:
    print("Cannot continue tests due to import failure")
    sys.exit(1)

# Test with default parameters
print("Testing with default parameters")
try:
    setup_page()
    print("✓ Default parameters test passed")
except Exception as e:
    print(f"✗ Default parameters test failed: {str(e)}")

# Test with layout="wide"
print("\nTesting with layout='wide'")
try:
    setup_page(layout="wide")
    print("✓ Wide layout test passed")
except Exception as e:
    print(f"✗ Wide layout test failed: {str(e)}")

# Test with initial_sidebar_state="expanded"
print("\nTesting with initial_sidebar_state='expanded'")
try:
    setup_page(initial_sidebar_state="expanded")
    print("✓ Expanded sidebar test passed")
except Exception as e:
    print(f"✗ Expanded sidebar test failed: {str(e)}")

# Test with both layout and initial_sidebar_state
print("\nTesting with layout='wide' and initial_sidebar_state='collapsed'")
try:
    setup_page(layout="wide", initial_sidebar_state="collapsed")
    print("✓ Combined parameters test passed")
except Exception as e:
    print(f"✗ Combined parameters test failed: {str(e)}")

print("\nAll tests completed")
