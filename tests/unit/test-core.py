"""
Unit tests for core functionality.

Tests the core modules including generator, template manager, validation, and error handling.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

import pytest
from jinja2 import TemplateError

from src.core.generator import DocumentGenerator
from src.core.template_manager import TemplateManager
from src.core.validation import ProjectValidator
from src.core.error_handler import DocGenError, ValidationError, TemplateError as DocGenTemplateError
from src.models.project_model import Project
from src.models.template import Template


class TestDocumentGenerator:
    """Test cases for DocumentGenerator."""
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        generator = DocumentGenerator()
        assert generator is not None
    
    def test_generate_document_success(self, mock_project: Project, mock_template: Template):
        """Test successful document generation."""
        generator = DocumentGenerator()
        
        with patch('src.core.generator.TemplateManager') as mock_tm:
            mock_tm.return_value.load_template.return_value = mock_template
            mock_tm.return_value.render_template.return_value = "Generated content"
            
            result = generator.generate_document(mock_project, mock_template)
            
            assert result == "Generated content"
    
    def test_generate_document_template_error(self, mock_project: Project, mock_template: Template):
        """Test document generation with template error."""
        generator = DocumentGenerator()
        
        with patch('src.core.generator.TemplateManager') as mock_tm:
            mock_tm.return_value.load_template.return_value = mock_template
            mock_tm.return_value.render_template.side_effect = TemplateError("Template error")
            
            with pytest.raises(DocGenTemplateError):
                generator.generate_document(mock_project, mock_template)
    
    def test_generate_document_invalid_project(self, mock_template: Template):
        """Test document generation with invalid project."""
        generator = DocumentGenerator()
        
        with pytest.raises(ValidationError):
            generator.generate_document(None, mock_template)
    
    def test_generate_document_invalid_template(self, mock_project: Project):
        """Test document generation with invalid template."""
        generator = DocumentGenerator()
        
        with pytest.raises(ValidationError):
            generator.generate_document(mock_project, None)


class TestTemplateManager:
    """Test cases for TemplateManager."""
    
    def test_template_manager_initialization(self):
        """Test template manager initialization."""
        manager = TemplateManager()
        assert manager is not None
    
    def test_load_template_success(self, test_templates_dir: Path):
        """Test loading a template successfully."""
        manager = TemplateManager()
        template_path = test_templates_dir / "project_plan.j2"
        
        template = manager.load_template(template_path)
        
        assert template is not None
        assert "{{ project.name }}" in template
    
    def test_load_template_not_found(self, temp_dir: Path):
        """Test loading a non-existent template."""
        manager = TemplateManager()
        template_path = temp_dir / "non_existent.j2"
        
        with pytest.raises(FileNotFoundError):
            manager.load_template(template_path)
    
    def test_render_template_success(self, mock_project: Project):
        """Test rendering a template successfully."""
        manager = TemplateManager()
        template_content = "# {{ project.name }}\n\n{{ project.description }}"
        
        result = manager.render_template(template_content, project=mock_project)
        
        assert result is not None
        assert mock_project.name in result
        assert mock_project.description in result
    
    def test_render_template_missing_variable(self, mock_project: Project):
        """Test rendering a template with missing variable."""
        manager = TemplateManager()
        template_content = "# {{ project.name }}\n\n{{ project.missing_variable }}"
        
        with pytest.raises(TemplateError):
            manager.render_template(template_content, project=mock_project)
    
    def test_render_template_syntax_error(self, mock_project: Project):
        """Test rendering a template with syntax error."""
        manager = TemplateManager()
        template_content = "# {{ project.name }\n\n{{ project.description }}"  # Missing closing brace
        
        with pytest.raises(TemplateError):
            manager.render_template(template_content, project=mock_project)
    
    def test_save_template_success(self, temp_dir: Path, mock_template: Template):
        """Test saving a template successfully."""
        manager = TemplateManager()
        output_path = temp_dir / "output.md"
        
        with patch('src.utils.file_io.write_file') as mock_write:
            manager.save_template("Generated content", output_path)
            mock_write.assert_called_once_with(output_path, "Generated content")
    
    def test_save_template_permission_error(self, temp_dir: Path):
        """Test saving a template with permission error."""
        manager = TemplateManager()
        output_path = temp_dir / "output.md"
        
        with patch('src.utils.file_io.write_file', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                manager.save_template("Generated content", output_path)


class TestProjectValidator:
    """Test cases for ProjectValidator."""
    
    def test_validator_initialization(self):
        """Test validator initialization."""
        validator = ProjectValidator()
        assert validator is not None
    
    def test_validate_project_success(self, mock_project: Project):
        """Test validating a valid project."""
        validator = ProjectValidator()
        
        result = validator.validate_project(mock_project)
        
        assert result is True
    
    def test_validate_project_invalid_name(self):
        """Test validating a project with invalid name."""
        validator = ProjectValidator()
        invalid_project = Project(name="", description="Valid description")
        
        with pytest.raises(ValidationError):
            validator.validate_project(invalid_project)
    
    def test_validate_project_invalid_email(self):
        """Test validating a project with invalid email."""
        validator = ProjectValidator()
        invalid_project = Project(
            name="Valid Name",
            description="Valid description",
            email="invalid-email"
        )
        
        with pytest.raises(ValidationError):
            validator.validate_project(invalid_project)
    
    def test_validate_project_none(self):
        """Test validating a None project."""
        validator = ProjectValidator()
        
        with pytest.raises(ValidationError):
            validator.validate_project(None)
    
    def test_validate_template_success(self, mock_template: Template):
        """Test validating a valid template."""
        validator = ProjectValidator()
        
        result = validator.validate_template(mock_template)
        
        assert result is True
    
    def test_validate_template_invalid_name(self):
        """Test validating a template with invalid name."""
        validator = ProjectValidator()
        invalid_template = Template(name="", content="Valid content")
        
        with pytest.raises(ValidationError):
            validator.validate_template(invalid_template)
    
    def test_validate_template_invalid_content(self):
        """Test validating a template with invalid content."""
        validator = ProjectValidator()
        invalid_template = Template(name="Valid name", content="")
        
        with pytest.raises(ValidationError):
            validator.validate_template(invalid_template)
    
    def test_validate_template_none(self):
        """Test validating a None template."""
        validator = ProjectValidator()
        
        with pytest.raises(ValidationError):
            validator.validate_template(None)


class TestErrorHandler:
    """Test cases for error handling."""
    
    def test_docgen_error_creation(self):
        """Test creating a DocGenError."""
        error = DocGenError("Test error message")
        
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
    
    def test_validation_error_creation(self):
        """Test creating a ValidationError."""
        error = ValidationError("Validation failed")
        
        assert str(error) == "Validation failed"
        assert isinstance(error, DocGenError)
    
    def test_template_error_creation(self):
        """Test creating a DocGenTemplateError."""
        error = DocGenTemplateError("Template error")
        
        assert str(error) == "Template error"
        assert isinstance(error, DocGenError)
    
    def test_error_with_details(self):
        """Test creating an error with additional details."""
        error = DocGenError("Main error", details={"field": "name", "value": "invalid"})
        
        assert str(error) == "Main error"
        assert hasattr(error, 'details')
        assert error.details["field"] == "name"
    
    def test_error_inheritance(self):
        """Test error inheritance chain."""
        validation_error = ValidationError("Validation failed")
        template_error = DocGenTemplateError("Template error")
        
        assert isinstance(validation_error, DocGenError)
        assert isinstance(template_error, DocGenError)
        assert isinstance(validation_error, Exception)
        assert isinstance(template_error, Exception)
