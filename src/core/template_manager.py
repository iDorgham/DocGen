"""
Template manager for DocGen CLI.

This module handles template loading, rendering, and management.
"""

from pathlib import Path
from jinja2 import Environment, Template, TemplateError
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

from src.utils.file_io import read_file, write_file


class TemplateManager:
    """
    Manages Jinja2 templates for document generation.
    """
    
    def __init__(self):
        """Initialize the template manager."""
        self.env = Environment()
    
    def load_template(self, template_path: Path) -> str:
        """
        Load a template from a file.
        
        Args:
            template_path: Path to the template file
            
        Returns:
            Template content
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        return read_file(template_path)
    
    def render_template(self, template_content: str, **context) -> str:
        """
        Render a template with context data.
        
        Args:
            template_content: Template content
            **context: Context variables for template rendering
            
        Returns:
            Rendered template content
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.from_string(template_content)
            return template.render(**context)
        except TemplateError as e:
            raise TemplateError(f"Template rendering failed: {str(e)}")
    
    def save_template(self, content: str, output_path: Path) -> None:
        """
        Save rendered content to a file.
        
        Args:
            content: Content to save
            output_path: Path to save the content
            
        Raises:
            PermissionError: If file cannot be written
        """
        write_file(output_path, content)


@dataclass
class TemplateMetadata:
    """
    Metadata for a template.
    
    Contains information about a template including its properties,
    usage statistics, and configuration.
    """
    
    name: str
    path: Path
    description: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    tags: Optional[list] = None
    variables: Optional[Dict[str, Any]] = None
    dependencies: Optional[list] = None
    usage_count: int = 0
    last_used: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.tags is None:
            self.tags = []
        if self.variables is None:
            self.variables = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.modified_at is None:
            self.modified_at = datetime.now()
    
    def update_usage(self):
        """Update usage statistics."""
        self.usage_count += 1
        self.last_used = datetime.now()
    
    def add_tag(self, tag: str):
        """Add a tag to the template."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the template."""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def add_variable(self, name: str, value: Any):
        """Add a variable to the template."""
        self.variables[name] = value
    
    def remove_variable(self, name: str):
        """Remove a variable from the template."""
        if name in self.variables:
            del self.variables[name]
    
    def add_dependency(self, dependency: str):
        """Add a dependency to the template."""
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)
    
    def remove_dependency(self, dependency: str):
        """Remove a dependency from the template."""
        if dependency in self.dependencies:
            self.dependencies.remove(dependency)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            'name': self.name,
            'path': str(self.path),
            'description': self.description,
            'author': self.author,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
            'tags': self.tags,
            'variables': self.variables,
            'dependencies': self.dependencies,
            'usage_count': self.usage_count,
            'last_used': self.last_used.isoformat() if self.last_used else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TemplateMetadata':
        """Create metadata from dictionary."""
        # Convert string paths back to Path objects
        if 'path' in data and isinstance(data['path'], str):
            data['path'] = Path(data['path'])
        
        # Convert ISO datetime strings back to datetime objects
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        
        if 'modified_at' in data and isinstance(data['modified_at'], str):
            data['modified_at'] = datetime.fromisoformat(data['modified_at'])
        
        if 'last_used' in data and isinstance(data['last_used'], str):
            data['last_used'] = datetime.fromisoformat(data['last_used'])
        
        return cls(**data)