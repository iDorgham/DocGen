"""
Simple unit tests for TemplateManager.

Tests the template management functionality with actual implementation.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.core.template_manager import TemplateManager, TemplateMetadata
from jinja2 import TemplateError


class TestTemplateManager:
    """Test cases for TemplateManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template_manager = TemplateManager()
    
    def test_init(self):
        """Test TemplateManager initialization."""
        assert self.template_manager is not None
        assert self.template_manager.env is not None
    
    def test_load_template_success(self):
        """Test successful template loading."""
        template_content = "Hello {{ name }}!"
        template_path = Path("test.j2")
        
        with patch('src.utils.file_io.read_file', return_value=template_content):
            result = self.template_manager.load_template(template_path)
            assert result == template_content
    
    def test_load_template_file_not_found(self):
        """Test template loading with file not found."""
        template_path = Path("nonexistent.j2")
        
        with patch('src.utils.file_io.read_file', side_effect=FileNotFoundError("File not found")):
            with pytest.raises(FileNotFoundError):
                self.template_manager.load_template(template_path)
    
    def test_render_template_success(self):
        """Test successful template rendering."""
        template_content = "Hello {{ name }}!"
        context = {"name": "World"}
        
        result = self.template_manager.render_template(template_content, **context)
        assert result == "Hello World!"
    
    def test_render_template_missing_data(self):
        """Test template rendering with missing data."""
        template_content = "Hello {{ name }}!"
        context = {}  # Missing 'name' key
        
        with pytest.raises(TemplateError):
            self.template_manager.render_template(template_content, **context)
    
    def test_render_template_invalid_syntax(self):
        """Test template rendering with invalid syntax."""
        template_content = "Hello {{ name }"  # Missing closing brace
        context = {"name": "World"}
        
        with pytest.raises(TemplateError):
            self.template_manager.render_template(template_content, **context)
    
    def test_save_template_success(self):
        """Test successful template saving."""
        content = "Hello World!"
        output_path = Path("output.txt")
        
        with patch('src.utils.file_io.write_file') as mock_write:
            self.template_manager.save_template(content, output_path)
            mock_write.assert_called_once_with(output_path, content)
    
    def test_save_template_invalid_path(self):
        """Test template saving with invalid path."""
        content = "Hello World!"
        output_path = Path("/invalid/path/output.txt")
        
        with patch('src.utils.file_io.write_file', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                self.template_manager.save_template(content, output_path)
    
    def test_render_template_complex(self):
        """Test template rendering with complex template."""
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
        context = {
            "title": "My Project",
            "description": "A test project",
            "features": ["Feature 1", "Feature 2", "Feature 3"],
            "author": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
        
        result = self.template_manager.render_template(template_content, **context)
        assert "My Project" in result
        assert "A test project" in result
        assert "Feature 1" in result
        assert "Feature 2" in result
        assert "Feature 3" in result
        assert "John Doe" in result
        assert "john@example.com" in result
    
    def test_render_template_with_filters(self):
        """Test template rendering with built-in filters."""
        template_content = "{{ name | upper }} - {{ version | default('1.0.0') }}"
        context = {"name": "test"}
        
        result = self.template_manager.render_template(template_content, **context)
        assert result == "TEST - 1.0.0"
    
    def test_render_template_empty_context(self):
        """Test template rendering with empty context."""
        template_content = "Hello World!"
        context = {}
        
        result = self.template_manager.render_template(template_content, **context)
        assert result == "Hello World!"
    
    def test_render_template_none_context(self):
        """Test template rendering with None context."""
        template_content = "Hello World!"
        
        result = self.template_manager.render_template(template_content)
        assert result == "Hello World!"


class TestTemplateMetadata:
    """Test cases for TemplateMetadata."""
    
    def test_template_metadata_creation(self):
        """Test TemplateMetadata creation."""
        metadata = TemplateMetadata(
            name="test_template",
            description="A test template",
            author="John Doe",
            version="1.0.0",
            created_at="2025-01-01",
            updated_at="2025-01-01"
        )
        
        assert metadata.name == "test_template"
        assert metadata.description == "A test template"
        assert metadata.author == "John Doe"
        assert metadata.version == "1.0.0"
        assert metadata.created_at == "2025-01-01"
        assert metadata.updated_at == "2025-01-01"
    
    def test_template_metadata_defaults(self):
        """Test TemplateMetadata with default values."""
        metadata = TemplateMetadata(name="test_template")
        
        assert metadata.name == "test_template"
        assert metadata.description is None
        assert metadata.author is None
        assert metadata.version is None
        assert metadata.created_at is None
        assert metadata.updated_at is None
    
    def test_template_metadata_to_dict(self):
        """Test TemplateMetadata to_dict method."""
        metadata = TemplateMetadata(
            name="test_template",
            description="A test template",
            author="John Doe",
            version="1.0.0"
        )
        
        result = metadata.to_dict()
        assert result["name"] == "test_template"
        assert result["description"] == "A test template"
        assert result["author"] == "John Doe"
        assert result["version"] == "1.0.0"
