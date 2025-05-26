"""
Run all tests for the BrainVenture application.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if __name__ == "__main__":
    # Find all test files in the tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not test_result.wasSuccessful())
