"""
Document generator for DocGen CLI.

This module handles document generation from templates and project data.
"""

from typing import Optional
from jinja2 import Environment, Template, TemplateError

from src.models.project_model import Project
from src.models.template_model import Template as TemplateModel
from src.core.error_handler import DocGenError, ValidationError, TemplateError as DocGenTemplateError


class DocumentGenerator:
    """
    Generates documents from templates and project data.
    """
    
    def __init__(self):
        """Initialize the document generator."""
        self.env = Environment()
    
    def generate_document(self, project: Project, template: TemplateModel) -> str:
        """
        Generate a document from a project and template.
        
        Args:
            project: Project data
            template: Template to use for generation
            
        Returns:
            Generated document content
            
        Raises:
            ValidationError: If project or template is invalid
            DocGenTemplateError: If template rendering fails
        """
        if project is None:
            raise ValidationError("Project cannot be None")
        
        if template is None:
            raise ValidationError("Template cannot be None")
        
        try:
            # Create Jinja2 template from content
            jinja_template = self.env.from_string(template.content)
            
            # Render template with project data
            rendered_content = jinja_template.render(project=project)
            
            return rendered_content
            
        except TemplateError as e:
            raise DocGenTemplateError(f"Template rendering failed: {str(e)}")
        except Exception as e:
            raise DocGenError(f"Document generation failed: {str(e)}")