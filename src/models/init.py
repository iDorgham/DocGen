"""
Data models and business logic for DocGen.

This package contains all the core models and business logic for the DocGen application.
"""

from .project import ProjectManager
from .template import TemplateManager
from src.core.error_handler import DocGenError

__all__ = ["ProjectManager", "TemplateManager", "DocGenError"]
