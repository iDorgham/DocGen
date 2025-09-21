"""
Formatting utilities for DocGen CLI.

This module provides content formatting functions.
"""

import json
import yaml
from typing import Any, Optional


def format_markdown(content: Optional[str]) -> str:
    """
    Format markdown content.
    
    Args:
        content: Markdown content to format
        
    Returns:
        Formatted markdown content
    """
    if content is None:
        return ""
    
    # Basic markdown formatting - strip leading/trailing whitespace and normalize
    return content.strip()


def format_yaml(data: Any) -> str:
    """
    Format data as YAML.
    
    Args:
        data: Data to format as YAML
        
    Returns:
        YAML formatted string
    """
    if data is None:
        return "null\n"
    
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)


def format_json(data: Any) -> str:
    """
    Format data as JSON.
    
    Args:
        data: Data to format as JSON
        
    Returns:
        JSON formatted string
    """
    if data is None:
        return "null"
    
    return json.dumps(data, indent=2, ensure_ascii=False)


class DocumentFormatter:
    """
    Document formatting class for DocGen CLI.
    
    Provides comprehensive document formatting capabilities
    for various output formats.
    """
    
    def __init__(self):
        """Initialize the document formatter."""
        pass
    
    def format_document(self, content: str, format_type: str = "markdown") -> str:
        """
        Format document content.
        
        Args:
            content: Document content to format
            format_type: Format type (markdown, html, pdf)
            
        Returns:
            Formatted document content
        """
        if not content:
            return ""
        
        if format_type == "markdown":
            return format_markdown(content)
        elif format_type == "yaml":
            return format_yaml(content)
        elif format_type == "json":
            return format_json(content)
        else:
            return content
    
    def format_markdown(self, content: str) -> str:
        """
        Format content as markdown.
        
        Args:
            content: Content to format
            
        Returns:
            Formatted markdown content
        """
        return format_markdown(content)
    
    def format_yaml(self, data: Any) -> str:
        """
        Format data as YAML.
        
        Args:
            data: Data to format
            
        Returns:
            YAML formatted string
        """
        return format_yaml(data)
    
    def format_json(self, data: Any) -> str:
        """
        Format data as JSON.
        
        Args:
            data: Data to format
            
        Returns:
            JSON formatted string
        """
        return format_json(data)