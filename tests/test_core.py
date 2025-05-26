"""
Unit tests for core helper functions.
"""

import unittest
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.helpers import calculate_progress, format_time, slugify
from utils.validators import validate_email, validate_test_answers
from config.content_config import load_neuroleader_types, load_course_structure

class TestHelpers(unittest.TestCase):
    """Test helper functions."""
    
    def test_calculate_progress(self):
        """Test calculate_progress function."""
        self.assertEqual(calculate_progress(0, 10), 0)
        self.assertEqual(calculate_progress(5, 10), 50)
        self.assertEqual(calculate_progress(10, 10), 100)
        self.assertEqual(calculate_progress(20, 10), 100)  # Should cap at 100
        
    def test_format_time(self):
        """Test format_time function."""
        self.assertEqual(format_time(30), "30 sec")
        self.assertEqual(format_time(90), "1 min")
        self.assertEqual(format_time(3600), "1 h 0 min")
        self.assertEqual(format_time(3900), "1 h 5 min")
        
    def test_slugify(self):
        """Test slugify function."""
        self.assertEqual(slugify("Test String"), "test-string")
        self.assertEqual(slugify("Żółć!@#$"), "zolc")
        self.assertEqual(slugify("  Multiple   Spaces  "), "multiple-spaces")

class TestValidators(unittest.TestCase):
    """Test validator functions."""
    
    def test_validate_email(self):
        """Test email validation."""
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("test.name+tag@example.co.uk"))
        self.assertFalse(validate_email("not-an-email"))
        self.assertFalse(validate_email("missing@domain"))
        self.assertFalse(validate_email("@missing-username.com"))
        
    def test_validate_test_answers(self):
        """Test test answers validation."""
        valid_answers = {"q1": 3, "q2": 5, "q3": 1}
        incomplete_answers = {"q1": 3, "q3": 1}
        invalid_answers = {"q1": 0, "q2": 6, "q3": 1}
        
        self.assertTrue(validate_test_answers(valid_answers, ["q1", "q2", "q3"]))
        self.assertFalse(validate_test_answers(incomplete_answers, ["q1", "q2", "q3"]))
        self.assertFalse(validate_test_answers(invalid_answers, ["q1", "q2", "q3"]))

class TestContentLoaders(unittest.TestCase):
    """Test content loading functions."""
    
    def test_load_neuroleader_types(self):
        """Test loading neuroleader types."""
        types = load_neuroleader_types()
        self.assertIsInstance(types, list)
        if types:  # If types are loaded successfully
            self.assertTrue(all(isinstance(t, dict) for t in types))
            self.assertTrue(all("id" in t for t in types))
    def test_load_course_structure(self):
        """Test loading course structure."""
        structure = load_course_structure()
        self.assertIsInstance(structure, list)
        if structure:  # If structure is loaded successfully
            self.assertTrue(all(isinstance(block, dict) for block in structure))
            self.assertTrue(all("title" in block for block in structure))

if __name__ == "__main__":
    unittest.main()
