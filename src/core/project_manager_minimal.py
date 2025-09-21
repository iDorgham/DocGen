"""
Minimal ProjectManager for testing.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml


class ProjectManager:
    """
    Minimal ProjectManager for testing.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the ProjectManager."""
        if config_dir is None:
            config_dir = Path.cwd() / ".docgen"
        
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
        """Create a new project."""
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
        
        return project_config
    
    def _generate_project_id(self, name: str) -> str:
        """Generate a unique project ID."""
        timestamp = int(datetime.now().timestamp())
        return f"{name.lower().replace(' ', '_')}_{timestamp}"
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project configuration by ID."""
        projects = self._read_json(self.projects_file)
        return projects.get(project_id)
    
    def get_all_projects(self) -> Dict[str, Dict[str, Any]]:
        """Get all projects."""
        return self._read_json(self.projects_file)
    
    def get_current_project(self) -> Optional[Dict[str, Any]]:
        """Get the current active project."""
        current_data = self._read_json(self.current_project_file)
        project_id = current_data.get("project_id")
        
        if not project_id:
            return None
        
        return self.get_project(project_id)
    
    def set_current_project(self, project_id: str) -> bool:
        """Set the current active project."""
        project = self.get_project(project_id)
        if not project:
            return False
        
        # Set as current
        current_data = {"project_id": project_id, "set_at": datetime.now().isoformat()}
        self._write_json(self.current_project_file, current_data)
        
        return True
