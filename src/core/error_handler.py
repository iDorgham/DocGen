"""
Enhanced error handling for DocGen CLI.

This module provides comprehensive error handling with recovery mechanisms,
detailed error context, and user-friendly error messages.
"""

import os
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable, Union
from pathlib import Path
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories."""
    VALIDATION = "validation"
    FILE_IO = "file_io"
    TEMPLATE = "template"
    PROJECT = "project"
    SYSTEM = "system"
    NETWORK = "network"
    PERMISSION = "permission"
    CONFIGURATION = "configuration"


class DocGenError(Exception):
    """
    Enhanced base exception class for DocGen CLI.
    """
    
    def __init__(self, message: str, details: dict = None, severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 category: ErrorCategory = ErrorCategory.SYSTEM, suggestions: List[str] = None,
                 recovery_action: Callable = None):
        """
        Initialize the error.
        
        Args:
            message: Error message
            details: Additional error details
            severity: Error severity level
            category: Error category
            suggestions: List of suggested actions
            recovery_action: Optional recovery function
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.severity = severity
        self.category = category
        self.suggestions = suggestions or []
        self.recovery_action = recovery_action
        self.timestamp = datetime.now()
        self.context = {}
    
    def add_context(self, key: str, value: Any) -> None:
        """Add context information to the error."""
        self.context[key] = value
    
    def get_recovery_suggestions(self) -> List[str]:
        """Get recovery suggestions based on error type and context."""
        suggestions = self.suggestions.copy()
        
        # Add category-specific suggestions
        if self.category == ErrorCategory.FILE_IO:
            suggestions.extend([
                "Check if the file path exists and is accessible",
                "Verify file permissions",
                "Ensure sufficient disk space"
            ])
        elif self.category == ErrorCategory.VALIDATION:
            suggestions.extend([
                "Check input data format and values",
                "Run validation with --fix-issues flag",
                "Review project_data.yaml file"
            ])
        elif self.category == ErrorCategory.TEMPLATE:
            suggestions.extend([
                "Validate template syntax with 'docgen template validate'",
                "Check template file exists and is readable",
                "Verify template variables match project data"
            ])
        elif self.category == ErrorCategory.PROJECT:
            suggestions.extend([
                "Use 'docgen recent' to see available projects",
                "Create a new project with 'docgen create'",
                "Switch to existing project with 'docgen switch'"
            ])
        
        return suggestions


class ValidationError(DocGenError):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, field: str = None, value: Any = None, **kwargs):
        super().__init__(message, category=ErrorCategory.VALIDATION, **kwargs)
        if field:
            self.add_context("field", field)
        if value is not None:
            self.add_context("value", value)


class TemplateError(DocGenError):
    """Exception raised for template-related errors."""
    
    def __init__(self, message: str, template_path: str = None, line_number: int = None, **kwargs):
        super().__init__(message, category=ErrorCategory.TEMPLATE, **kwargs)
        if template_path:
            self.add_context("template_path", template_path)
        if line_number:
            self.add_context("line_number", line_number)


class FileIOError(DocGenError):
    """Exception raised for file I/O errors."""
    
    def __init__(self, message: str, file_path: str = None, operation: str = None, **kwargs):
        super().__init__(message, category=ErrorCategory.FILE_IO, **kwargs)
        if file_path:
            self.add_context("file_path", file_path)
        if operation:
            self.add_context("operation", operation)


class ProjectError(DocGenError):
    """Exception raised for project-related errors."""
    
    def __init__(self, message: str, project_id: str = None, project_path: str = None, **kwargs):
        super().__init__(message, category=ErrorCategory.PROJECT, **kwargs)
        if project_id:
            self.add_context("project_id", project_id)
        if project_path:
            self.add_context("project_path", project_path)


class NetworkError(DocGenError):
    """Exception raised for network-related errors."""
    
    def __init__(self, message: str, url: str = None, status_code: int = None, **kwargs):
        super().__init__(message, category=ErrorCategory.NETWORK, **kwargs)
        if url:
            self.add_context("url", url)
        if status_code:
            self.add_context("status_code", status_code)


class PermissionError(DocGenError):
    """Exception raised for permission-related errors."""
    
    def __init__(self, message: str, resource: str = None, required_permission: str = None, **kwargs):
        super().__init__(message, category=ErrorCategory.PERMISSION, **kwargs)
        if resource:
            self.add_context("resource", resource)
        if required_permission:
            self.add_context("required_permission", required_permission)


class ConfigurationError(DocGenError):
    """Exception raised for configuration-related errors."""
    
    def __init__(self, message: str, config_file: str = None, setting: str = None, **kwargs):
        super().__init__(message, category=ErrorCategory.CONFIGURATION, **kwargs)
        if config_file:
            self.add_context("config_file", config_file)
        if setting:
            self.add_context("setting", setting)


class ErrorRecovery:
    """Error recovery mechanisms."""
    
    @staticmethod
    def recover_file_not_found(error: FileIOError) -> bool:
        """Attempt to recover from file not found error."""
        file_path = error.context.get("file_path")
        if not file_path:
            return False
        
        path = Path(file_path)
        
        # Try to create parent directories
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def recover_permission_error(error: PermissionError) -> bool:
        """Attempt to recover from permission error."""
        resource = error.context.get("resource")
        if not resource:
            return False
        
        try:
            # Try to fix permissions
            if os.path.exists(resource):
                os.chmod(resource, 0o755)
                return True
        except Exception:
            pass
        
        return False
    
    @staticmethod
    def recover_validation_error(error: ValidationError) -> bool:
        """Attempt to recover from validation error."""
        # This would typically involve fixing the data
        # For now, just return False as it requires user intervention
        return False


class EnhancedErrorHandler:
    """Enhanced error handler with recovery and detailed reporting."""
    
    def __init__(self, console: Console = None):
        self.console = console or Console()
        self.error_log = []
        self.recovery_attempts = []
        self.error_stats = {
            "total_errors": 0,
            "by_category": {},
            "by_severity": {},
            "recovery_success_rate": 0.0
        }
    
    def handle_error(self, error: Exception, context: dict = None, 
                    attempt_recovery: bool = True) -> Dict[str, Any]:
        """Handle an error with enhanced logging and recovery."""
        # Convert to DocGenError if needed
        if not isinstance(error, DocGenError):
            error = DocGenError(
                str(error),
                details=context or {},
                severity=ErrorSeverity.MEDIUM,
                category=ErrorCategory.SYSTEM
            )
        
        # Add context
        if context:
            for key, value in context.items():
                error.add_context(key, value)
        
        # Log error
        error_info = {
            'error': error,
            'message': error.message,
            'type': type(error).__name__,
            'severity': error.severity.value,
            'category': error.category.value,
            'context': error.context,
            'timestamp': error.timestamp.isoformat(),
            'traceback': traceback.format_exc()
        }
        self.error_log.append(error_info)
        
        # Update statistics
        self._update_stats(error)
        
        # Attempt recovery
        recovery_success = False
        if attempt_recovery and error.recovery_action:
            try:
                recovery_success = error.recovery_action()
                self.recovery_attempts.append({
                    'error_type': type(error).__name__,
                    'success': recovery_success,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as recovery_error:
                self.console.print(f"[red]Recovery attempt failed: {recovery_error}[/red]")
        
        error_info['recovery_attempted'] = attempt_recovery
        error_info['recovery_success'] = recovery_success
        
        return error_info
    
    def _update_stats(self, error: DocGenError) -> None:
        """Update error statistics."""
        self.error_stats["total_errors"] += 1
        
        # Update category stats
        category = error.category.value
        self.error_stats["by_category"][category] = self.error_stats["by_category"].get(category, 0) + 1
        
        # Update severity stats
        severity = error.severity.value
        self.error_stats["by_severity"][severity] = self.error_stats["by_severity"].get(severity, 0) + 1
        
        # Update recovery success rate
        if self.recovery_attempts:
            successful_recoveries = sum(1 for attempt in self.recovery_attempts if attempt['success'])
            self.error_stats["recovery_success_rate"] = successful_recoveries / len(self.recovery_attempts)
    
    def get_user_friendly_message(self, error: Exception) -> str:
        """Get a user-friendly error message with suggestions."""
        if not isinstance(error, DocGenError):
            return f"An unexpected error occurred: {str(error)}"
        
        message = f"[{error.severity.value.upper()}] {error.message}"
        
        # Add context information
        if error.context:
            context_info = []
            for key, value in error.context.items():
                if key in ['file_path', 'template_path', 'project_path']:
                    context_info.append(f"{key}: {value}")
            if context_info:
                message += f"\nContext: {', '.join(context_info)}"
        
        return message
    
    def get_error_suggestions(self, error: Exception) -> List[str]:
        """Get actionable suggestions for resolving an error."""
        if not isinstance(error, DocGenError):
            return ["Check the error message and try again"]
        
        return error.get_recovery_suggestions()
    
    def display_error(self, error: Exception, show_traceback: bool = False) -> None:
        """Display a formatted error message."""
        if not isinstance(error, DocGenError):
            error = DocGenError(str(error))
        
        # Create error panel
        severity_color = {
            ErrorSeverity.LOW: "yellow",
            ErrorSeverity.MEDIUM: "orange3",
            ErrorSeverity.HIGH: "red",
            ErrorSeverity.CRITICAL: "bright_red"
        }
        
        color = severity_color.get(error.severity, "red")
        
        # Error message
        error_text = f"[{color}]✗[/{color}] {error.message}"
        
        # Add context
        if error.context:
            error_text += "\n\n[bold]Context:[/bold]"
            for key, value in error.context.items():
                error_text += f"\n  • {key}: {value}"
        
        # Add suggestions
        suggestions = self.get_error_suggestions(error)
        if suggestions:
            error_text += "\n\n[bold yellow]Suggestions:[/bold yellow]"
            for suggestion in suggestions:
                error_text += f"\n  • {suggestion}"
        
        # Add traceback if requested
        if show_traceback:
            error_text += f"\n\n[bold]Traceback:[/bold]\n[dim]{traceback.format_exc()}[/dim]"
        
        panel = Panel(
            error_text,
            title=f"[{color}]{error.severity.value.upper()} - {error.category.value.replace('_', ' ').title()}[/{color}]",
            border_style=color
        )
        
        self.console.print(panel)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of all errors encountered."""
        recent_errors = self.error_log[-10:] if self.error_log else []
        
        return {
            "total_errors": self.error_stats["total_errors"],
            "categories": self.error_stats["by_category"],
            "severities": self.error_stats["by_severity"],
            "recovery_success_rate": self.error_stats["recovery_success_rate"],
            "recent_errors": [error_info['error'] for error_info in recent_errors]
        }
    
    def create_error_report(self, output_path: Path) -> None:
        """Create a detailed error report file."""
        report_data = {
            "summary": self.get_error_summary(),
            "all_errors": self.error_log,
            "recovery_attempts": self.recovery_attempts,
            "generated_at": datetime.now().isoformat()
        }
        
        import json
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
    
    def clear_logs(self) -> None:
        """Clear all error logs and statistics."""
        self.error_log.clear()
        self.recovery_attempts.clear()
        self.error_stats = {
            "total_errors": 0,
            "by_category": {},
            "by_severity": {},
            "recovery_success_rate": 0.0
        }


# Global error handler instance
error_handler = EnhancedErrorHandler()


def handle_error(error: Exception, context: dict = None, attempt_recovery: bool = True):
    """Handle an error using the global error handler."""
    return error_handler.handle_error(error, context, attempt_recovery)


def get_user_friendly_message(error: Exception) -> str:
    """Get a user-friendly error message using the global error handler."""
    return error_handler.get_user_friendly_message(error)


def display_error(error: Exception, show_traceback: bool = False) -> None:
    """Display a formatted error message."""
    error_handler.display_error(error, show_traceback)