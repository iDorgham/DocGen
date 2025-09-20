"""
Unit tests for ProjectManager.

Tests the project management functionality.
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.core.project_manager import ProjectManager
from src.core.error_handler import DocGenError


class TestProjectManager:
    """Test cases for ProjectManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.project_manager = ProjectManager()
        self.temp_dir = tempfile.mkdtemp()
        self.test_project_path = Path(self.temp_dir) / "test_project"
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_init(self):
        """Test ProjectManager initialization."""
        assert self.project_manager is not None
    
    def test_create_project_success(self):
        """Test successful project creation."""
        project_data = {
            "name": "test_project",
            "description": "A test project",
            "version": "1.0.0",
            "author": "John Doe"
        }
        
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', mock_open()) as mock_file:
                result = self.project_manager.create_project(
                    self.test_project_path, 
                    project_data
                )
                assert result is True
                mock_file.assert_called()
    
    def test_create_project_invalid_path(self):
        """Test project creation with invalid path."""
        project_data = {
            "name": "test_project",
            "description": "A test project"
        }
        
        with patch('pathlib.Path.mkdir', side_effect=OSError("Permission denied")):
            with pytest.raises(DocGenError):
                self.project_manager.create_project(
                    Path("/invalid/path"), 
                    project_data
                )
    
    def test_load_project_success(self):
        """Test successful project loading."""
        project_data = {
            "name": "test_project",
            "description": "A test project",
            "version": "1.0.0"
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(project_data))):
            result = self.project_manager.load_project(self.test_project_path)
            assert result == project_data
    
    def test_load_project_file_not_found(self):
        """Test project loading with file not found."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(DocGenError):
                self.project_manager.load_project(self.test_project_path)
    
    def test_load_project_invalid_json(self):
        """Test project loading with invalid JSON."""
        invalid_json = "{ invalid json }"
        
        with patch('builtins.open', mock_open(read_data=invalid_json)):
            with pytest.raises(DocGenError):
                self.project_manager.load_project(self.test_project_path)
    
    def test_save_project_success(self):
        """Test successful project saving."""
        project_data = {
            "name": "test_project",
            "description": "A test project",
            "version": "1.0.0"
        }
        
        with patch('builtins.open', mock_open()) as mock_file:
            result = self.project_manager.save_project(
                self.test_project_path, 
                project_data
            )
            assert result is True
            mock_file.assert_called()
    
    def test_save_project_invalid_path(self):
        """Test project saving with invalid path."""
        project_data = {
            "name": "test_project",
            "description": "A test project"
        }
        
        with patch('builtins.open', side_effect=OSError("Permission denied")):
            with pytest.raises(DocGenError):
                self.project_manager.save_project(
                    Path("/invalid/path"), 
                    project_data
                )
    
    def test_update_project_success(self):
        """Test successful project update."""
        original_data = {
            "name": "test_project",
            "description": "A test project",
            "version": "1.0.0"
        }
        
        update_data = {
            "description": "An updated test project",
            "version": "1.1.0"
        }
        
        expected_data = {
            "name": "test_project",
            "description": "An updated test project",
            "version": "1.1.0"
        }
        
        with patch.object(self.project_manager, 'load_project', return_value=original_data):
            with patch.object(self.project_manager, 'save_project', return_value=True):
                result = self.project_manager.update_project(
                    self.test_project_path, 
                    update_data
                )
                assert result is True
    
    def test_update_project_not_found(self):
        """Test project update with project not found."""
        update_data = {
            "description": "An updated test project"
        }
        
        with patch.object(self.project_manager, 'load_project', side_effect=DocGenError("Project not found")):
            with pytest.raises(DocGenError):
                self.project_manager.update_project(
                    self.test_project_path, 
                    update_data
                )
    
    def test_delete_project_success(self):
        """Test successful project deletion."""
        with patch('shutil.rmtree'):
            result = self.project_manager.delete_project(self.test_project_path)
            assert result is True
    
    def test_delete_project_not_found(self):
        """Test project deletion with project not found."""
        with patch('shutil.rmtree', side_effect=OSError("No such file or directory")):
            with pytest.raises(DocGenError):
                self.project_manager.delete_project(self.test_project_path)
    
    def test_list_projects_success(self):
        """Test successful project listing."""
        projects_dir = Path(self.temp_dir) / "projects"
        project_dirs = [
            projects_dir / "project1",
            projects_dir / "project2",
            projects_dir / "project3"
        ]
        
        with patch('pathlib.Path.iterdir', return_value=project_dirs):
            with patch('pathlib.Path.is_dir', return_value=True):
                result = self.project_manager.list_projects(projects_dir)
                assert len(result) == 3
                assert all(isinstance(p, Path) for p in result)
    
    def test_list_projects_empty_directory(self):
        """Test project listing from empty directory."""
        projects_dir = Path(self.temp_dir) / "empty_projects"
        
        with patch('pathlib.Path.iterdir', return_value=[]):
            result = self.project_manager.list_projects(projects_dir)
            assert len(result) == 0
    
    def test_list_projects_nonexistent_directory(self):
        """Test project listing from nonexistent directory."""
        projects_dir = Path("/nonexistent/projects")
        
        with patch('pathlib.Path.iterdir', side_effect=OSError("Directory not found")):
            with pytest.raises(DocGenError):
                self.project_manager.list_projects(projects_dir)
    
    def test_validate_project_data_success(self):
        """Test successful project data validation."""
        project_data = {
            "name": "test_project",
            "description": "A test project",
            "version": "1.0.0",
            "author": "John Doe",
            "email": "john@example.com"
        }
        
        result = self.project_manager.validate_project_data(project_data)
        assert result is True
    
    def test_validate_project_data_missing_required(self):
        """Test project data validation with missing required fields."""
        project_data = {
            "description": "A test project"
            # Missing required 'name' field
        }
        
        with pytest.raises(DocGenError):
            self.project_manager.validate_project_data(project_data)
    
    def test_validate_project_data_invalid_email(self):
        """Test project data validation with invalid email."""
        project_data = {
            "name": "test_project",
            "description": "A test project",
            "email": "invalid-email"  # Invalid email format
        }
        
        with pytest.raises(DocGenError):
            self.project_manager.validate_project_data(project_data)
    
    def test_get_project_info_success(self):
        """Test successful project info retrieval."""
        project_data = {
            "name": "test_project",
            "description": "A test project",
            "version": "1.0.0",
            "author": "John Doe"
        }
        
        with patch.object(self.project_manager, 'load_project', return_value=project_data):
            result = self.project_manager.get_project_info(self.test_project_path)
            assert result == project_data
    
    def test_get_project_info_not_found(self):
        """Test project info retrieval with project not found."""
        with patch.object(self.project_manager, 'load_project', side_effect=DocGenError("Project not found")):
            with pytest.raises(DocGenError):
                self.project_manager.get_project_info(self.test_project_path)
    
    def test_project_exists_true(self):
        """Test project existence check when project exists."""
        with patch('pathlib.Path.exists', return_value=True):
            result = self.project_manager.project_exists(self.test_project_path)
            assert result is True
    
    def test_project_exists_false(self):
        """Test project existence check when project doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = self.project_manager.project_exists(self.test_project_path)
            assert result is False
