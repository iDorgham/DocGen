"""
Unit tests for TemplateManager.

Tests the template management functionality.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.core.template_manager import TemplateManager, TemplateMetadata
from src.core.error_handler import DocGenError


class TestTemplateManager:
    """Test cases for TemplateManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template_manager = TemplateManager()
    
    def test_init(self):
        """Test TemplateManager initialization."""
        assert self.template_manager is not None
    
    def test_load_template_success(self):
        """Test successful template loading."""
        template_content = "Hello {{ name }}!"
        template_path = Path("test.j2")
        
        with patch('src.utils.file_io.read_file', return_value=template_content):
            result = self.template_manager.load_template(template_path)
            assert result == template_content
    
    def test_load_template_file_not_found(self):
        """Test template loading with file not found."""
        template_path = "nonexistent.j2"
        
        with pytest.raises(DocGenError):
            self.template_manager.load_template(template_path)
    
    def test_load_template_invalid_syntax(self):
        """Test template loading with invalid syntax."""
        template_content = "Hello {{ name }"  # Missing closing brace
        template_path = "invalid.j2"
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            with pytest.raises(DocGenError):
                self.template_manager.load_template(template_path)
    
    def test_render_template_success(self):
        """Test successful template rendering."""
        template_content = "Hello {{ name }}!"
        data = {"name": "World"}
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            template = self.template_manager.load_template("test.j2")
            result = self.template_manager.render_template(template, data)
            assert result == "Hello World!"
    
    def test_render_template_missing_data(self):
        """Test template rendering with missing data."""
        template_content = "Hello {{ name }}!"
        data = {}  # Missing 'name' key
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            template = self.template_manager.load_template("test.j2")
            with pytest.raises(DocGenError):
                self.template_manager.render_template(template, data)
    
    def test_save_template_success(self):
        """Test successful template saving."""
        template_content = "Hello {{ name }}!"
        template_path = "output.j2"
        
        with patch('builtins.open', mock_open()) as mock_file:
            self.template_manager.save_template(template_content, template_path)
            mock_file.assert_called_once_with(template_path, 'w', encoding='utf-8')
            mock_file().write.assert_called_once_with(template_content)
    
    def test_save_template_invalid_path(self):
        """Test template saving with invalid path."""
        template_content = "Hello {{ name }}!"
        template_path = "/invalid/path/output.j2"
        
        with patch('builtins.open', side_effect=OSError("Permission denied")):
            with pytest.raises(DocGenError):
                self.template_manager.save_template(template_content, template_path)
    
    def test_get_template_metadata(self):
        """Test getting template metadata."""
        template_content = """
# Template: {{ title }}
# Author: {{ author }}
# Version: {{ version }}
Hello {{ name }}!
"""
        template_path = "metadata.j2"
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            template = self.template_manager.load_template(template_path)
            metadata = self.template_manager.get_template_metadata(template)
            
            assert metadata is not None
            assert isinstance(metadata, TemplateMetadata)
    
    def test_validate_template_success(self):
        """Test successful template validation."""
        template_content = "Hello {{ name }}!"
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            template = self.template_manager.load_template("test.j2")
            result = self.template_manager.validate_template(template)
            assert result is True
    
    def test_validate_template_invalid(self):
        """Test template validation with invalid template."""
        template_content = "Hello {{ name }"  # Missing closing brace
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            with pytest.raises(DocGenError):
                self.template_manager.load_template("invalid.j2")
    
    def test_list_templates(self):
        """Test listing available templates."""
        template_dir = Path("templates")
        template_files = ["template1.j2", "template2.j2", "template3.j2"]
        
        with patch('pathlib.Path.glob', return_value=[Path(f) for f in template_files]):
            templates = self.template_manager.list_templates(template_dir)
            assert len(templates) == 3
            assert all(t.endswith('.j2') for t in templates)
    
    def test_list_templates_empty_directory(self):
        """Test listing templates from empty directory."""
        template_dir = Path("empty_templates")
        
        with patch('pathlib.Path.glob', return_value=[]):
            templates = self.template_manager.list_templates(template_dir)
            assert len(templates) == 0
    
    def test_list_templates_nonexistent_directory(self):
        """Test listing templates from nonexistent directory."""
        template_dir = Path("nonexistent")
        
        with patch('pathlib.Path.glob', side_effect=OSError("Directory not found")):
            with pytest.raises(DocGenError):
                self.template_manager.list_templates(template_dir)


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
