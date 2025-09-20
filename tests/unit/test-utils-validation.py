"""
Unit tests for validation utilities.

Tests the InputValidator class and validation functions.
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.utils.validation import InputValidator, validate_file_path, validate_yaml, validate_email
from src.core.error_handler import ValidationError


class TestInputValidator:
    """Test cases for InputValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = InputValidator()
    
    def test_validate_project_name_valid(self):
        """Test validating valid project names."""
        valid_names = [
            "My Project",
            "project-123",
            "project_123",
            "Project123",
            "a" * 50  # 50 characters
        ]
        
        for name in valid_names:
            assert self.validator.validate_project_name(name) is True
    
    def test_validate_project_name_invalid(self):
        """Test validating invalid project names."""
        invalid_names = [
            "",  # Empty
            "   ",  # Whitespace only
            None,  # None
            "a" * 101,  # Too long
            "project<test",  # Invalid character
            "project>test",  # Invalid character
            "project:test",  # Invalid character
            "project\"test",  # Invalid character
            "project|test",  # Invalid character
            "project?test",  # Invalid character
            "project*test",  # Invalid character
            "project\\test",  # Invalid character
            "project/test",  # Invalid character
        ]
        
        for name in invalid_names:
            with pytest.raises(ValidationError):
                self.validator.validate_project_name(name)
    
    def test_validate_file_path_valid(self):
        """Test validating valid file paths."""
        # Create a temporary file for testing
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            assert self.validator.validate_file_path(tmp_path) is True
        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)
    
    def test_validate_file_path_invalid(self):
        """Test validating invalid file paths."""
        invalid_paths = [
            "",  # Empty
            None,  # None
            "/nonexistent/path/file.txt",  # Non-existent file
            "not_a_file",  # Non-existent file
        ]
        
        for path in invalid_paths:
            with pytest.raises(ValidationError):
                self.validator.validate_file_path(path)
    
    def test_validate_file_path_exception_handling(self):
        """Test validate_file_path with exception handling."""
        from unittest.mock import patch
        
        # Test OSError handling in InputValidator
        with patch('pathlib.Path', side_effect=OSError("OS error")):
            with pytest.raises(ValidationError, match="Invalid file path: OS error"):
                self.validator.validate_file_path("test.txt")
        
        # Test ValueError handling in InputValidator
        with patch('pathlib.Path', side_effect=ValueError("Invalid path")):
            with pytest.raises(ValidationError, match="Invalid file path: Invalid path"):
                self.validator.validate_file_path("test.txt")
    
    def test_validate_email_valid(self):
        """Test validating valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com",
        ]
        
        for email in valid_emails:
            assert self.validator.validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test validating invalid email addresses."""
        invalid_emails = [
            "",  # Empty
            None,  # None
            "invalid-email",  # No @
            "@example.com",  # No local part
            "test@",  # No domain
            "test..test@example.com",  # Double dots
            "test@example..com",  # Double dots in domain
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                self.validator.validate_email(email)
    
    def test_validate_yaml_content_valid(self):
        """Test validating valid YAML content."""
        valid_yaml_contents = [
            "key: value",
            "name: Test\nversion: 1.0.0",
            "list:\n  - item1\n  - item2",
            "nested:\n  key: value",
        ]
        
        for content in valid_yaml_contents:
            assert self.validator.validate_yaml_content(content) is True
    
    def test_validate_yaml_content_invalid(self):
        """Test validating invalid YAML content."""
        invalid_yaml_contents = [
            None,  # None
            "invalid: yaml: content:",  # Invalid YAML syntax
            "key: value\n  invalid_indentation",  # Invalid indentation
            "key: [unclosed list",  # Unclosed list
            "key: {unclosed dict",  # Unclosed dict
        ]
        
        for content in invalid_yaml_contents:
            with pytest.raises(ValidationError):
                self.validator.validate_yaml_content(content)


class TestValidationFunctions:
    """Test cases for validation functions."""
    
    def test_validate_file_path_function(self):
        """Test validate_file_path function."""
        # Create a temporary file for testing
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            assert validate_file_path(Path(tmp_path)) is True
            assert validate_file_path(Path("/nonexistent/file.txt")) is False
        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)
    
    def test_validate_file_path_exception_handling(self):
        """Test validate_file_path with exception handling."""
        from unittest.mock import patch
        
        # Test OSError handling
        with patch('pathlib.Path.exists', side_effect=OSError("OS error")):
            assert validate_file_path(Path("test.txt")) is False
        
        # Test ValueError handling
        with patch('pathlib.Path', side_effect=ValueError("Invalid path")):
            assert validate_file_path(Path("test.txt")) is False
    
    def test_validate_yaml_function(self):
        """Test validate_yaml function."""
        assert validate_yaml("key: value") is True
        assert validate_yaml("invalid: yaml: content:") is False
        assert validate_yaml(None) is False
    
    def test_validate_email_function(self):
        """Test validate_email function."""
        assert validate_email("test@example.com") is True
        assert validate_email("invalid-email") is False
        assert validate_email("") is False
