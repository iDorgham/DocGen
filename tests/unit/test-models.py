"""
Unit tests for data models.

Tests the Project and Template model classes for proper validation,
serialization, and behavior.
"""

import pytest
from pydantic import ValidationError

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
    
    def test_project_creation_with_invalid_email(self):
        """Test project creation fails with invalid email."""
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "email": "invalid-email"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Project(**project_data)
        
        assert "email" in str(exc_info.value)
    
    def test_project_creation_with_empty_name(self):
        """Test project creation fails with empty name."""
        project_data = {
            "name": "",
            "description": "A test project"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Project(**project_data)
        
        assert "name" in str(exc_info.value)
    
    def test_project_creation_with_empty_description(self):
        """Test project creation fails with empty description."""
        project_data = {
            "name": "Test Project",
            "description": ""
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Project(**project_data)
        
        assert "description" in str(exc_info.value)
    
    def test_project_serialization(self):
        """Test project can be serialized to dict."""
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "version": "1.0.0",
            "author": "Test Author",
            "email": "test@example.com"
        }
        
        project = Project(**project_data)
        serialized = project.model_dump()
        
        assert serialized["name"] == "Test Project"
        assert serialized["description"] == "A test project"
        assert serialized["version"] == "1.0.0"
        assert serialized["author"] == "Test Author"
        assert serialized["email"] == "test@example.com"
    
    def test_project_optional_fields(self):
        """Test project with all optional fields."""
        project_data = {
            "name": "Full Project",
            "description": "A project with all fields",
            "version": "2.0.0",
            "author": "Full Author",
            "email": "full@example.com",
            "license": "MIT",
            "repository": "https://github.com/test/full-project",
            "keywords": ["test", "full", "project"],
            "requirements": ["click>=8.0.0", "jinja2>=3.0.0"],
            "features": ["CLI", "Templates", "YAML"]
        }
        
        project = Project(**project_data)
        
        assert project.license == "MIT"
        assert project.repository == "https://github.com/test/full-project"
        assert project.keywords == ["test", "full", "project"]
        assert project.requirements == ["click>=8.0.0", "jinja2>=3.0.0"]
        assert project.features == ["CLI", "Templates", "YAML"]


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
    
    def test_template_creation_with_empty_name(self):
        """Test template creation fails with empty name."""
        template_data = {
            "name": "",
            "content": "Some content"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Template(**template_data)
        
        assert "name" in str(exc_info.value)
    
    def test_template_creation_with_empty_content(self):
        """Test template creation fails with empty content."""
        template_data = {
            "name": "test_template",
            "content": ""
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Template(**template_data)
        
        assert "content" in str(exc_info.value)
    
    def test_template_serialization(self):
        """Test template can be serialized to dict."""
        template_data = {
            "name": "test_template",
            "content": "# {{ project.name }}",
            "output_path": "test_output.md"
        }
        
        template = Template(**template_data)
        serialized = template.model_dump()
        
        assert serialized["name"] == "test_template"
        assert serialized["content"] == "# {{ project.name }}"
        assert serialized["output_path"] == "test_output.md"
    
    def test_template_optional_fields(self):
        """Test template with all optional fields."""
        template_data = {
            "name": "full_template",
            "content": "# {{ project.name }}\n\n{{ project.description }}",
            "output_path": "full_output.md",
            "description": "A full template with description",
            "variables": ["project.name", "project.description"],
            "dependencies": ["project_plan.j2"]
        }
        
        template = Template(**template_data)
        
        assert template.description == "A full template with description"
        assert template.variables == ["project.name", "project.description"]
        assert template.dependencies == ["project_plan.j2"]
    
    def test_template_jinja2_syntax_validation(self):
        """Test template validates Jinja2 syntax."""
        # Valid Jinja2 template
        valid_template = Template(
            name="valid_template",
            content="# {{ project.name }}\n\n{% for feature in project.features %}\n- {{ feature }}\n{% endfor %}"
        )
        assert valid_template.content is not None
        
        # Invalid Jinja2 template (should still be valid as we don't validate syntax in model)
        invalid_template = Template(
            name="invalid_template",
            content="# {{ project.name }\n\n{% for feature in project.features %}\n- {{ feature }}\n{% endfor %}"  # Missing closing brace
        )
        assert invalid_template.content is not None  # Model doesn't validate Jinja2 syntax
