"""
Unit tests for formatting utilities.

Tests the DocumentFormatter class and formatting functions.
"""

import pytest
import sys
import os
import json
import yaml

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.utils.formatting import DocumentFormatter, format_markdown, format_yaml, format_json


class TestDocumentFormatter:
    """Test cases for DocumentFormatter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = DocumentFormatter()
    
    def test_format_document_markdown(self):
        """Test formatting document as markdown."""
        content = "  # Test Title\n\n  Some content  "
        result = self.formatter.format_document(content, "markdown")
        assert result == "# Test Title\n\n  Some content"
    
    def test_format_document_yaml(self):
        """Test formatting document as YAML."""
        data = {"name": "test", "version": "1.0.0"}
        result = self.formatter.format_document(data, "yaml")
        expected = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        assert result == expected
    
    def test_format_document_json(self):
        """Test formatting document as JSON."""
        data = {"name": "test", "version": "1.0.0"}
        result = self.formatter.format_document(data, "json")
        expected = json.dumps(data, indent=2, ensure_ascii=False)
        assert result == expected
    
    def test_format_document_default(self):
        """Test formatting document with default format."""
        content = "test content"
        result = self.formatter.format_document(content)
        assert result == "test content"
    
    def test_format_document_empty(self):
        """Test formatting empty document."""
        result = self.formatter.format_document("")
        assert result == ""
        
        result = self.formatter.format_document(None)
        assert result == ""
    
    def test_format_document_unknown_format(self):
        """Test formatting document with unknown format type."""
        content = "test content"
        result = self.formatter.format_document(content, "unknown")
        assert result == content
    
    def test_format_markdown_method(self):
        """Test format_markdown method."""
        content = "  # Test Title\n\n  Some content  "
        result = self.formatter.format_markdown(content)
        assert result == "# Test Title\n\n  Some content"
    
    def test_format_yaml_method(self):
        """Test format_yaml method."""
        data = {"name": "test", "version": "1.0.0"}
        result = self.formatter.format_yaml(data)
        expected = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        assert result == expected
    
    def test_format_json_method(self):
        """Test format_json method."""
        data = {"name": "test", "version": "1.0.0"}
        result = self.formatter.format_json(data)
        expected = json.dumps(data, indent=2, ensure_ascii=False)
        assert result == expected


class TestFormattingFunctions:
    """Test cases for formatting functions."""
    
    def test_format_markdown_function(self):
        """Test format_markdown function."""
        content = "  # Test Title\n\n  Some content  "
        result = format_markdown(content)
        assert result == "# Test Title\n\n  Some content"
        
        # Test with None
        result = format_markdown(None)
        assert result == ""
    
    def test_format_yaml_function(self):
        """Test format_yaml function."""
        data = {"name": "test", "version": "1.0.0"}
        result = format_yaml(data)
        expected = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        assert result == expected
        
        # Test with None
        result = format_yaml(None)
        assert result == "null\n"
    
    def test_format_json_function(self):
        """Test format_json function."""
        data = {"name": "test", "version": "1.0.0"}
        result = format_json(data)
        expected = json.dumps(data, indent=2, ensure_ascii=False)
        assert result == expected
        
        # Test with None
        result = format_json(None)
        assert result == "null"
    
    def test_format_yaml_with_unicode(self):
        """Test format_yaml with unicode characters."""
        data = {"name": "测试", "description": "Unicode test"}
        result = format_yaml(data)
        expected = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        assert result == expected
    
    def test_format_json_with_unicode(self):
        """Test format_json with unicode characters."""
        data = {"name": "测试", "description": "Unicode test"}
        result = format_json(data)
        expected = json.dumps(data, indent=2, ensure_ascii=False)
        assert result == expected
