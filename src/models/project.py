"""
Project Manager Module

Handles project data persistence and management for the DocGen CLI.
This module addresses FR4: Project Data Persistence.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml


class ProjectManager:
    """
    Manages project data persistence and retrieval.
    
    This class handles:
    - Creating and managing project configurations
    - Storing project metadata
    - Tracking recent projects
    - Managing project workspaces
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the ProjectManager.
        
        Args:
            config_dir: Directory to store configuration files. 
                       Defaults to ~/.docgen
        """
        if config_dir is None:
            config_dir = Path.home() / ".docgen"
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.projects_file = self.config_dir / "projects.json"
        self.recent_file = self.config_dir / "recent.json"
        self.current_project_file = self.config_dir / "current_project.json"
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self) -> None:
        """Initialize configuration files if they don't exist."""
        if not self.projects_file.exists():
            self._write_json(self.projects_file, {})
        
        if not self.recent_file.exists():
            self._write_json(self.recent_file, [])
        
        if not self.current_project_file.exists():
            self._write_json(self.current_project_file, {})
    
    def _read_json(self, file_path: Path) -> Any:
        """Read JSON data from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _write_json(self, file_path: Path, data: Any) -> None:
        """Write JSON data to a file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_project(self, name: str, path: Path, description: str = "") -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            name: Project name
            path: Project directory path
            description: Project description
            
        Returns:
            Project configuration dictionary
        """
        project_id = self._generate_project_id(name)
        project_config = {
            "id": project_id,
            "name": name,
            "path": str(path.absolute()),
            "description": description,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Save project configuration
        projects = self._read_json(self.projects_file)
        projects[project_id] = project_config
        self._write_json(self.projects_file, projects)
        
        # Add to recent projects
        self._add_to_recent(project_id)
        
        # Set as current project
        self.set_current_project(project_id)
        
        return project_config
    
    def _generate_project_id(self, name: str) -> str:
        """Generate a unique project ID."""
        # Simple ID generation - in production, you might want something more robust
        timestamp = int(datetime.now().timestamp())
        return f"{name.lower().replace(' ', '_')}_{timestamp}"
    
    def _add_to_recent(self, project_id: str) -> None:
        """Add project to recent projects list."""
        recent = self._read_json(self.recent_file)
        
        # Remove if already exists
        if project_id in recent:
            recent.remove(project_id)
        
        # Add to beginning
        recent.insert(0, project_id)
        
        # Keep only last 10 projects
        recent = recent[:10]
        
        self._write_json(self.recent_file, recent)
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project configuration by ID."""
        projects = self._read_json(self.projects_file)
        return projects.get(project_id)
    
    def get_all_projects(self) -> Dict[str, Dict[str, Any]]:
        """Get all projects."""
        return self._read_json(self.projects_file)
    
    def get_recent_projects(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent projects.
        
        Args:
            limit: Maximum number of recent projects to return
            
        Returns:
            List of recent project configurations
        """
        recent_ids = self._read_json(self.recent_file)
        projects = self._read_json(self.projects_file)
        
        recent_projects = []
        for project_id in recent_ids[:limit]:
            if project_id in projects:
                recent_projects.append(projects[project_id])
        
        return recent_projects
    
    def set_current_project(self, project_id: str) -> bool:
        """
        Set the current active project.
        
        Args:
            project_id: ID of the project to set as current
            
        Returns:
            True if successful, False if project doesn't exist
        """
        project = self.get_project(project_id)
        if not project:
            return False
        
        # Update last accessed time
        project["last_accessed"] = datetime.now().isoformat()
        projects = self._read_json(self.projects_file)
        projects[project_id] = project
        self._write_json(self.projects_file, projects)
        
        # Set as current
        current_data = {"project_id": project_id, "set_at": datetime.now().isoformat()}
        self._write_json(self.current_project_file, current_data)
        
        # Add to recent
        self._add_to_recent(project_id)
        
        return True
    
    def get_current_project(self) -> Optional[Dict[str, Any]]:
        """Get the current active project."""
        current_data = self._read_json(self.current_project_file)
        project_id = current_data.get("project_id")
        
        if not project_id:
            return None
        
        return self.get_project(project_id)
    
    def update_project(self, project_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update project configuration.
        
        Args:
            project_id: ID of the project to update
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False if project doesn't exist
        """
        projects = self._read_json(self.projects_file)
        
        if project_id not in projects:
            return False
        
        projects[project_id].update(updates)
        projects[project_id]["last_accessed"] = datetime.now().isoformat()
        
        self._write_json(self.projects_file, projects)
        return True
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: ID of the project to delete
            
        Returns:
            True if successful, False if project doesn't exist
        """
        projects = self._read_json(self.projects_file)
        
        if project_id not in projects:
            return False
        
        # Remove from projects
        del projects[project_id]
        self._write_json(self.projects_file, projects)
        
        # Remove from recent
        recent = self._read_json(self.recent_file)
        if project_id in recent:
            recent.remove(project_id)
            self._write_json(self.recent_file, recent)
        
        # Clear current project if it was deleted
        current_data = self._read_json(self.current_project_file)
        if current_data.get("project_id") == project_id:
            self._write_json(self.current_project_file, {})
        
        return True
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """
        Get project status information.
        
        Args:
            project_id: ID of the project
            
        Returns:
            Dictionary with status information
        """
        project = self.get_project(project_id)
        if not project:
            return {"status": "not_found"}
        
        project_path = Path(project["path"])
        
        status = {
            "project_id": project_id,
            "name": project["name"],
            "path": project["path"],
            "exists": project_path.exists(),
            "last_accessed": project["last_accessed"],
            "created_at": project["created_at"],
            "is_current": self.get_current_project() and self.get_current_project()["id"] == project_id
        }
        
        # Check for generated documents
        if project_path.exists():
            docs_dir = project_path / "docs"
            status["has_docs"] = docs_dir.exists()
            if docs_dir.exists():
                status["doc_files"] = list(docs_dir.glob("*.md")) + list(docs_dir.glob("*.pdf")) + list(docs_dir.glob("*.html"))
        
        return status
