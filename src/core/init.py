"""
Core modules for DocGen CLI.

This package contains the core functionality for document generation,
project management, validation, and error handling.
"""

from .generator import DocumentGenerator
from .project_manager import ProjectManager
from .validation import ProjectValidator, ValidationError
from .error_handler import handle_error, get_user_friendly_message, DocGenError
from .template_manager import TemplateManager, TemplateMetadata
from .git_manager import GitManager, GitConfig, GitStatus
from .spec_validator import SpecValidator, SpecEvolutionTracker, create_spec_validator
from .agent_hooks import AgentHookManager, HookRule, HookAction, create_agent_hook_manager

__all__ = [
    "DocumentGenerator",
    "ProjectManager", 
    "ProjectValidator",
    "ValidationError",
    "handle_error",
    "get_user_friendly_message",
    "DocGenError",
    "TemplateManager",
    "TemplateMetadata",
    "GitManager",
    "GitConfig",
    "GitStatus",
    "SpecValidator",
    "SpecEvolutionTracker",
    "create_spec_validator",
    "AgentHookManager",
    "HookRule",
    "HookAction",
    "create_agent_hook_manager"
]