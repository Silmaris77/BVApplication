"""
Simple script to test the logger implementation.
"""
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Import the modules that use get_logger
from utils.logger import get_logger
from utils.error_handler import logger as error_logger
from utils.helpers import logger as helper_logger

def test_logger():
    """Test if the logger is working properly."""
    # Create a new logger with a name
    test_logger = get_logger("test_module")
    
    # Log messages with different loggers
    print("Testing loggers...")
    test_logger.info("This is a test message from test_logger")
    error_logger.info("This is a test message from error_logger")
    helper_logger.info("This is a test message from helper_logger")
    
    print("Logger test complete!")
    return True

if __name__ == "__main__":
    try:
        success = test_logger()
        if success:
            print("✅ Logger test passed successfully!")
    except Exception as e:
        print(f"❌ Logger test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
