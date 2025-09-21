"""
Project data model for DocGen CLI.

This module defines the Project data model using Pydantic for validation.
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class Project(BaseModel):
    """
    Project data model with validation.
    
    This model represents a project with all its metadata and configuration.
    """
    
    name: str = Field(..., min_length=1, description="Project name")
    description: str = Field(..., min_length=1, description="Project description")
    version: str = Field(default="1.0.0", description="Project version")
    author: Optional[str] = Field(default=None, description="Project author")
    email: Optional[EmailStr] = Field(default=None, description="Author email")
    license: Optional[str] = Field(default=None, description="Project license")
    repository: Optional[str] = Field(default=None, description="Repository URL")
    keywords: Optional[List[str]] = Field(default=None, description="Project keywords")
    requirements: Optional[List[str]] = Field(default=None, description="Project requirements")
    features: Optional[List[str]] = Field(default=None, description="Project features")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            EmailStr: str
        }
        schema_extra = {
            "example": {
                "name": "My Project",
                "description": "A sample project",
                "version": "1.0.0",
                "author": "John Doe",
                "email": "john@example.com",
                "license": "MIT",
                "repository": "https://github.com/john/my-project",
                "keywords": ["python", "cli", "documentation"],
                "requirements": ["click>=8.0.0", "jinja2>=3.0.0"],
                "features": ["CLI interface", "Template generation"]
            }
        }
