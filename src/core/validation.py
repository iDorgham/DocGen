"""
Validation module for DocGen CLI.

This module provides validation for projects and templates.
"""

from src.models.project_model import Project
from src.models.template_model import Template
from src.core.error_handler import ValidationError


class ProjectValidator:
    """
    Validates project and template data.
    """
    
    def __init__(self):
        """Initialize the validator."""
        pass
    
    def validate_project(self, project: Project) -> bool:
        """
        Validate a project.
        
        Args:
            project: Project to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If project is invalid
        """
        if project is None:
            raise ValidationError("Project cannot be None")
        
        # Pydantic model validation is handled automatically
        # Additional custom validation can be added here
        
        return True
    
    def validate_template(self, template: Template) -> bool:
        """
        Validate a template.
        
        Args:
            template: Template to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If template is invalid
        """
        if template is None:
            raise ValidationError("Template cannot be None")
        
        # Pydantic model validation is handled automatically
        # Additional custom validation can be added here
        
        return True