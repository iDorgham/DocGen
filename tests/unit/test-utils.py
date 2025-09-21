"""
Unit tests for utility functions.

Tests file I/O, formatting, and validation utilities.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from src.utils.file_io import read_file, write_file, file_exists, ensure_directory
from src.utils.formatting import format_markdown, format_yaml, format_json
from src.utils.validation import validate_file_path, validate_yaml, validate_email


class TestFileIO:
    """Test cases for file I/O utilities."""
    
    def test_read_file_success(self, temp_dir: Path):
        """Test reading a file successfully."""
        test_file = temp_dir / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)
        
        result = read_file(test_file)
        assert result == test_content
    
    def test_read_file_not_found(self, temp_dir: Path):
        """Test reading a non-existent file."""
        non_existent_file = temp_dir / "non_existent.txt"
        
        with pytest.raises(FileNotFoundError):
            read_file(non_existent_file)
    
    def test_read_file_permission_error(self, temp_dir: Path):
        """Test reading a file with permission error."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        with patch.object(Path, 'read_text', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                read_file(test_file)
    
    def test_write_file_success(self, temp_dir: Path):
        """Test writing a file successfully."""
        test_file = temp_dir / "test.txt"
        test_content = "Hello, World!"
        
        write_file(test_file, test_content)
        
        assert test_file.exists()
        assert test_file.read_text() == test_content
    
    def test_write_file_create_directory(self, temp_dir: Path):
        """Test writing a file creates parent directories."""
        test_file = temp_dir / "subdir" / "test.txt"
        test_content = "Hello, World!"
        
        write_file(test_file, test_content)
        
        assert test_file.exists()
        assert test_file.read_text() == test_content
    
    def test_write_file_permission_error(self, temp_dir: Path):
        """Test writing a file with permission error."""
        test_file = temp_dir / "test.txt"
        test_content = "test content"
        
        with patch.object(Path, 'write_text', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                write_file(test_file, test_content)
    
    def test_file_exists_true(self, temp_dir: Path):
        """Test file_exists returns True for existing file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        assert file_exists(test_file) is True
    
    def test_file_exists_false(self, temp_dir: Path):
        """Test file_exists returns False for non-existent file."""
        non_existent_file = temp_dir / "non_existent.txt"
        
        assert file_exists(non_existent_file) is False
    
    def test_ensure_directory_exists(self, temp_dir: Path):
        """Test ensure_directory creates directory if it doesn't exist."""
        new_dir = temp_dir / "new_directory"
        
        ensure_directory(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_ensure_directory_already_exists(self, temp_dir: Path):
        """Test ensure_directory doesn't fail if directory already exists."""
        existing_dir = temp_dir / "existing_directory"
        existing_dir.mkdir()
        
        # Should not raise an exception
        ensure_directory(existing_dir)
        
        assert existing_dir.exists()
        assert existing_dir.is_dir()


class TestFormatting:
    """Test cases for formatting utilities."""
    
    def test_format_markdown_basic(self):
        """Test basic markdown formatting."""
        content = "# Title\n\nThis is a **bold** statement."
        result = format_markdown(content)
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_format_markdown_empty(self):
        """Test markdown formatting with empty content."""
        result = format_markdown("")
        assert result == ""
    
    def test_format_markdown_none(self):
        """Test markdown formatting with None content."""
        result = format_markdown(None)
        assert result == ""
    
    def test_format_yaml_basic(self):
        """Test basic YAML formatting."""
        data = {"name": "test", "version": "1.0.0"}
        result = format_yaml(data)
        
        assert result is not None
        assert isinstance(result, str)
        assert "name: test" in result
        assert "version: 1.0.0" in result
    
    def test_format_yaml_empty(self):
        """Test YAML formatting with empty data."""
        result = format_yaml({})
        assert result == "{}\n"
    
    def test_format_yaml_none(self):
        """Test YAML formatting with None data."""
        result = format_yaml(None)
        assert result == "null\n"
    
    def test_format_json_basic(self):
        """Test basic JSON formatting."""
        data = {"name": "test", "version": "1.0.0"}
        result = format_json(data)
        
        assert result is not None
        assert isinstance(result, str)
        assert '"name": "test"' in result
        assert '"version": "1.0.0"' in result
    
    def test_format_json_empty(self):
        """Test JSON formatting with empty data."""
        result = format_json({})
        assert result == "{}"
    
    def test_format_json_none(self):
        """Test JSON formatting with None data."""
        result = format_json(None)
        assert result == "null"


class TestValidation:
    """Test cases for validation utilities."""
    
    def test_validate_file_path_valid(self, temp_dir: Path):
        """Test file path validation with valid path."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        result = validate_file_path(test_file)
        assert result is True
    
    def test_validate_file_path_invalid(self, temp_dir: Path):
        """Test file path validation with invalid path."""
        non_existent_file = temp_dir / "non_existent.txt"
        
        result = validate_file_path(non_existent_file)
        assert result is False
    
    def test_validate_file_path_directory(self, temp_dir: Path):
        """Test file path validation with directory."""
        result = validate_file_path(temp_dir)
        assert result is False  # Should be False for directories
    
    def test_validate_yaml_valid(self):
        """Test YAML validation with valid YAML."""
        valid_yaml = """
        name: test
        version: 1.0.0
        author: Test Author
        """
        
        result = validate_yaml(valid_yaml)
        assert result is True
    
    def test_validate_yaml_invalid(self):
        """Test YAML validation with invalid YAML."""
        invalid_yaml = """
        name: test
        version: 1.0.0
        invalid: [unclosed list
        """
        
        result = validate_yaml(invalid_yaml)
        assert result is False
    
    def test_validate_yaml_empty(self):
        """Test YAML validation with empty content."""
        result = validate_yaml("")
        assert result is True  # Empty YAML is valid
    
    def test_validate_yaml_none(self):
        """Test YAML validation with None content."""
        result = validate_yaml(None)
        assert result is False
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "user123@test-domain.com"
        ]
        
        for email in valid_emails:
            result = validate_email(email)
            assert result is True, f"Email {email} should be valid"
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@.example.com",
            "test@example..com"
        ]
        
        for email in invalid_emails:
            result = validate_email(email)
            assert result is False, f"Email {email} should be invalid"
    
    def test_validate_email_empty(self):
        """Test email validation with empty email."""
        result = validate_email("")
        assert result is False
    
    def test_validate_email_none(self):
        """Test email validation with None email."""
        result = validate_email(None)
        assert result is False
