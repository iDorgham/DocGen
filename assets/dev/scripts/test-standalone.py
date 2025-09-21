#!/usr/bin/env python3
"""
Standalone test script for DocGen CLI models.

This script tests the new model classes without importing the existing codebase.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import only the new model classes directly
from src.models.project_model import Project
from src.models.template_model import Template
from src.utils.file_io import read_file, write_file, file_exists, ensure_directory
from src.utils.formatting import format_markdown, format_yaml, format_json
from src.utils.validation import validate_file_path, validate_yaml, validate_email
from src.core.generator import DocumentGenerator
from src.core.template_manager import TemplateManager
from src.core.validation import ProjectValidator
from src.core.error_handler import DocGenError, ValidationError, TemplateError as DocGenTemplateError


def test_project_model():
    """Test Project model functionality."""
    print("🧪 Testing Project Model...")
    
    # Test valid project creation
    project_data = {
        "name": "Test Project",
        "description": "A test project for DocGen CLI",
        "version": "1.0.0",
        "author": "Test Author",
        "email": "test@example.com"
    }
    
    project = Project(**project_data)
    assert project.name == "Test Project"
    assert project.description == "A test project for DocGen CLI"
    assert project.version == "1.0.0"
    assert project.author == "Test Author"
    assert project.email == "test@example.com"
    
    # Test minimal project creation
    minimal_data = {
        "name": "Minimal Project",
        "description": "A minimal project"
    }
    
    minimal_project = Project(**minimal_data)
    assert minimal_project.name == "Minimal Project"
    assert minimal_project.description == "A minimal project"
    assert minimal_project.version == "1.0.0"  # Default value
    assert minimal_project.author is None
    assert minimal_project.email is None
    
    # Test serialization
    serialized = project.model_dump()
    assert serialized["name"] == "Test Project"
    assert serialized["version"] == "1.0.0"
    
    print("✅ Project Model tests passed!")


def test_template_model():
    """Test Template model functionality."""
    print("🧪 Testing Template Model...")
    
    # Test valid template creation
    template_data = {
        "name": "test_template",
        "content": "# {{ project.name }}\n\n{{ project.description }}",
        "output_path": "test_output.md"
    }
    
    template = Template(**template_data)
    assert template.name == "test_template"
    assert template.content == "# {{ project.name }}\n\n{{ project.description }}"
    assert template.output_path == "test_output.md"
    
    # Test minimal template creation
    minimal_data = {
        "name": "minimal_template",
        "content": "Minimal content"
    }
    
    minimal_template = Template(**minimal_data)
    assert minimal_template.name == "minimal_template"
    assert minimal_template.content == "Minimal content"
    assert minimal_template.output_path == "output.md"  # Default value
    
    # Test serialization
    serialized = template.model_dump()
    assert serialized["name"] == "test_template"
    assert serialized["content"] == "# {{ project.name }}\n\n{{ project.description }}"
    
    print("✅ Template Model tests passed!")


def test_utils():
    """Test utility functions."""
    print("🧪 Testing Utility Functions...")
    
    # Test formatting functions
    assert format_markdown("# Test") == "# Test"
    assert format_markdown("") == ""
    assert format_markdown(None) == ""
    
    yaml_data = {"name": "test", "version": "1.0.0"}
    yaml_result = format_yaml(yaml_data)
    assert "name: test" in yaml_result
    assert "version: 1.0.0" in yaml_result
    
    json_data = {"name": "test", "version": "1.0.0"}
    json_result = format_json(json_data)
    assert '"name": "test"' in json_result
    assert '"version": "1.0.0"' in json_result
    
    # Test validation functions
    assert validate_yaml("name: test\nversion: 1.0.0") is True
    assert validate_yaml("invalid: yaml: [") is False
    assert validate_yaml("") is True
    assert validate_yaml(None) is False
    
    assert validate_email("test@example.com") is True
    assert validate_email("invalid-email") is False
    assert validate_email("") is False
    assert validate_email(None) is False
    
    print("✅ Utility Functions tests passed!")


def test_core_functionality():
    """Test core functionality."""
    print("🧪 Testing Core Functionality...")
    
    # Test document generator
    generator = DocumentGenerator()
    assert generator is not None
    
    # Test template manager
    manager = TemplateManager()
    assert manager is not None
    
    # Test project validator
    validator = ProjectValidator()
    assert validator is not None
    
    # Test error handling
    error = DocGenError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)
    
    validation_error = ValidationError("Validation failed")
    assert str(validation_error) == "Validation failed"
    assert isinstance(validation_error, DocGenError)
    
    template_error = DocGenTemplateError("Template error")
    assert str(template_error) == "Template error"
    assert isinstance(template_error, DocGenError)
    
    print("✅ Core Functionality tests passed!")


def test_file_operations():
    """Test file operations with temporary files."""
    print("🧪 Testing File Operations...")
    
    import tempfile
    import shutil
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    try:
        # Test file writing and reading
        test_file = temp_dir / "test.txt"
        test_content = "Hello, World!"
        
        write_file(test_file, test_content)
        assert test_file.exists()
        
        read_content = read_file(test_file)
        assert read_content == test_content
        
        # Test file existence check
        assert file_exists(test_file) is True
        assert file_exists(temp_dir / "nonexistent.txt") is False
        
        # Test directory creation
        new_dir = temp_dir / "new_directory"
        ensure_directory(new_dir)
        assert new_dir.exists()
        assert new_dir.is_dir()
        
        print("✅ File Operations tests passed!")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Run all tests."""
    print("🚀 Starting DocGen CLI Test Suite")
    print("=" * 50)
    
    try:
        test_project_model()
        test_template_model()
        test_utils()
        test_core_functionality()
        test_file_operations()
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        print("✅ Test coverage implementation is working correctly")
        
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
