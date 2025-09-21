"""
Validation utilities for DocGen CLI.

This module provides validation functions for various data types.
"""

import yaml
import re
from pathlib import Path
from src.core.error_handler import ValidationError


def validate_file_path(file_path: Path) -> bool:
    """
    Validate that a file path exists and is a file.
    
    Args:
        file_path: Path to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        path = Path(file_path)
        return path.exists() and path.is_file()
    except (OSError, ValueError):
        return False


def validate_yaml(content: str) -> bool:
    """
    Validate YAML content.
    
    Args:
        content: YAML content to validate
        
    Returns:
        True if valid YAML, False otherwise
    """
    if content is None:
        return False
    
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email, False otherwise
    """
    if not email:
        return False
    
    # Simple email validation - check basic structure and no double dots
    if '..' in email or email.startswith('.') or email.endswith('.'):
        return False
    
    # Check for dots at start/end of domain parts
    if '@' in email:
        local, domain = email.split('@', 1)
        if domain.startswith('.') or domain.endswith('.'):
            return False
    
    # Basic email pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


class InputValidator:
    """
    Input validation class for DocGen CLI.
    
    Provides comprehensive input validation for various data types
    and user inputs.
    """
    
    def __init__(self):
        """Initialize the input validator."""
        pass
    
    def validate_project_name(self, name: str) -> bool:
        """
        Validate project name.
        
        Args:
            name: Project name to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValidationError("Project name must be a non-empty string")
        
        if len(name.strip()) == 0:
            raise ValidationError("Project name cannot be empty or whitespace only")
        
        if len(name) > 100:
            raise ValidationError("Project name cannot exceed 100 characters")
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        if any(char in name for char in invalid_chars):
            raise ValidationError(f"Project name contains invalid characters: {invalid_chars}")
        
        return True
    
    def validate_file_path(self, file_path: str) -> bool:
        """
        Validate file path.
        
        Args:
            file_path: File path to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If path is invalid
        """
        if not file_path or not isinstance(file_path, str):
            raise ValidationError("File path must be a non-empty string")
        
        try:
            path = Path(file_path)
            if not validate_file_path(path):
                raise ValidationError(f"File does not exist or is not a file: {file_path}")
            return True
        except (OSError, ValueError) as e:
            raise ValidationError(f"Invalid file path: {e}")
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValidationError("Email must be a non-empty string")
        
        if not validate_email(email):
            raise ValidationError("Invalid email address format")
        
        return True
    
    def validate_yaml_content(self, content: str) -> bool:
        """
        Validate YAML content.
        
        Args:
            content: YAML content to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If content is invalid
        """
        if not content or not isinstance(content, str):
            raise ValidationError("YAML content must be a non-empty string")
        
        if not validate_yaml(content):
            raise ValidationError("Invalid YAML content")
        
        return True