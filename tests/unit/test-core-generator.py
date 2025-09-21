"""
Unit tests for DocumentGenerator.

Tests the document generation functionality.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.core.generator import DocumentGenerator
from src.core.error_handler import DocGenError


class TestDocumentGenerator:
    """Test cases for DocumentGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = DocumentGenerator()
    
    def test_init(self):
        """Test DocumentGenerator initialization."""
        assert self.generator is not None
    
    def test_generate_document_basic(self):
        """Test basic document generation."""
        template_content = "Hello {{ name }}!"
        data = {"name": "World"}
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            result = self.generator.generate_document("test.j2", data)
            assert result == "Hello World!"
    
    def test_generate_document_missing_template(self):
        """Test document generation with missing template."""
        data = {"name": "World"}
        
        with pytest.raises(DocGenError):
            self.generator.generate_document("nonexistent.j2", data)
    
    def test_generate_document_invalid_template(self):
        """Test document generation with invalid template."""
        template_content = "Hello {{ name }"  # Missing closing brace
        data = {"name": "World"}
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            with pytest.raises(DocGenError):
                self.generator.generate_document("invalid.j2", data)
    
    def test_generate_document_missing_data(self):
        """Test document generation with missing data."""
        template_content = "Hello {{ name }}!"
        data = {}  # Missing 'name' key
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            with pytest.raises(DocGenError):
                self.generator.generate_document("test.j2", data)
    
    def test_generate_document_complex_template(self):
        """Test document generation with complex template."""
        template_content = """
# {{ title }}

## Overview
{{ description }}

## Features
{% for feature in features %}
- {{ feature }}
{% endfor %}

## Author
{{ author.name }} ({{ author.email }})
"""
        data = {
            "title": "My Project",
            "description": "A test project",
            "features": ["Feature 1", "Feature 2", "Feature 3"],
            "author": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
        
        expected = """
# My Project

## Overview
A test project

## Features
- Feature 1
- Feature 2
- Feature 3

## Author
John Doe (john@example.com)
"""
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            result = self.generator.generate_document("complex.j2", data)
            assert result.strip() == expected.strip()
    
    def test_generate_document_with_filters(self):
        """Test document generation with custom filters."""
        template_content = "{{ name | upper }} - {{ version | default('1.0.0') }}"
        data = {"name": "test"}
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            result = self.generator.generate_document("filters.j2", data)
            assert result == "TEST - 1.0.0"
    
    def test_generate_document_empty_data(self):
        """Test document generation with empty data."""
        template_content = "Hello World!"
        data = {}
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            result = self.generator.generate_document("empty.j2", data)
            assert result == "Hello World!"
    
    def test_generate_document_none_data(self):
        """Test document generation with None data."""
        template_content = "Hello World!"
        data = None
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            result = self.generator.generate_document("none.j2", data)
            assert result == "Hello World!"
