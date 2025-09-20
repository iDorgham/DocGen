"""
Template data model for DocGen CLI.

This module defines the Template data model using Pydantic for validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Template(BaseModel):
    """
    Template data model with validation.
    
    This model represents a Jinja2 template with its metadata and configuration.
    """
    
    name: str = Field(..., min_length=1, description="Template name")
    content: str = Field(..., min_length=1, description="Template content")
    output_path: str = Field(default="output.md", description="Output file path")
    description: Optional[str] = Field(default=None, description="Template description")
    variables: Optional[List[str]] = Field(default=None, description="Template variables")
    dependencies: Optional[List[str]] = Field(default=None, description="Template dependencies")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "name": "project_plan",
                "content": "# {{ project.name }}\n\n{{ project.description }}",
                "output_path": "project_plan.md",
                "description": "Project plan template",
                "variables": ["project.name", "project.description"],
                "dependencies": []
            }
        }
