"""
Simple unit tests for data models without CLI dependencies.
"""

import pytest
from pydantic import ValidationError

# Add src to Python path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.models.project_model import Project
from src.models.template_model import Template


class TestProject:
    """Test cases for Project model."""
    
    def test_project_creation_with_valid_data(self):
        """Test creating a project with valid data."""
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "version": "1.0.0",
            "author": "Test Author",
            "email": "test@example.com"
        }
        
        project = Project(**project_data)
        
        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert project.version == "1.0.0"
        assert project.author == "Test Author"
        assert project.email == "test@example.com"
    
    def test_project_creation_with_minimal_data(self):
        """Test creating a project with minimal required data."""
        project_data = {
            "name": "Minimal Project",
            "description": "A minimal project"
        }
        
        project = Project(**project_data)
        
        assert project.name == "Minimal Project"
        assert project.description == "A minimal project"
        assert project.version == "1.0.0"  # Default value
        assert project.author is None
        assert project.email is None


class TestTemplate:
    """Test cases for Template model."""
    
    def test_template_creation_with_valid_data(self):
        """Test creating a template with valid data."""
        template_data = {
            "name": "test_template",
            "content": "# {{ project.name }}\n\n{{ project.description }}",
            "output_path": "test_output.md"
        }
        
        template = Template(**template_data)
        
        assert template.name == "test_template"
        assert template.content == "# {{ project.name }}\n\n{{ project.description }}"
        assert template.output_path == "test_output.md"
    
    def test_template_creation_with_minimal_data(self):
        """Test creating a template with minimal required data."""
        template_data = {
            "name": "minimal_template",
            "content": "Minimal content"
        }
        
        template = Template(**template_data)
        
        assert template.name == "minimal_template"
        assert template.content == "Minimal content"
        assert template.output_path == "output.md"  # Default value
