"""
Unit tests for file I/O utilities.

Tests the FileManager class and file I/O functions.
"""

import pytest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.utils.file_io import (
    FileManager, read_file, write_file, file_exists, ensure_directory
)


class TestFileManager:
    """Test cases for FileManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.file_manager = FileManager()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_read_file_success(self):
        """Test successful file reading."""
        test_file = self.temp_dir / "test.txt"
        test_content = "Hello, World!"
        
        # Write test content
        test_file.write_text(test_content)
        
        # Read and verify
        result = self.file_manager.read_file(test_file)
        assert result == test_content
    
    def test_read_file_not_found(self):
        """Test reading non-existent file."""
        non_existent_file = self.temp_dir / "nonexistent.txt"
        
        with pytest.raises(FileNotFoundError):
            self.file_manager.read_file(non_existent_file)
    
    def test_read_file_not_a_file(self):
        """Test reading a directory instead of a file."""
        # Create a directory
        test_dir = self.temp_dir / "test_dir"
        test_dir.mkdir()
        
        with pytest.raises(ValueError, match="Path is not a file"):
            self.file_manager.read_file(test_dir)
    
    def test_read_file_permission_error(self):
        """Test reading a file with permission error."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test content")
        
        with patch.object(Path, 'read_text', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError, match="Permission denied"):
                self.file_manager.read_file(test_file)
    
    def test_write_file_success(self):
        """Test successful file writing."""
        test_file = self.temp_dir / "test.txt"
        test_content = "Hello, World!"
        
        # Write content
        self.file_manager.write_file(test_file, test_content)
        
        # Verify content
        assert test_file.exists()
        assert test_file.read_text() == test_content
    
    def test_write_file_creates_directory(self):
        """Test that write_file creates parent directories."""
        test_file = self.temp_dir / "subdir" / "test.txt"
        test_content = "Hello, World!"
        
        # Write content (should create subdir)
        self.file_manager.write_file(test_file, test_content)
        
        # Verify content and directory creation
        assert test_file.exists()
        assert test_file.read_text() == test_content
        assert test_file.parent.exists()
    
    def test_write_file_permission_error(self):
        """Test writing a file with permission error."""
        test_file = self.temp_dir / "test.txt"
        test_content = "test content"
        
        with patch.object(Path, 'write_text', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError, match="Permission denied"):
                self.file_manager.write_file(test_file, test_content)
    
    def test_file_exists_true(self):
        """Test file_exists with existing file."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test")
        
        assert self.file_manager.file_exists(test_file) is True
    
    def test_file_exists_false(self):
        """Test file_exists with non-existing file."""
        non_existent_file = self.temp_dir / "nonexistent.txt"
        
        assert self.file_manager.file_exists(non_existent_file) is False
    
    def test_ensure_directory_creates_directory(self):
        """Test ensure_directory creates directory."""
        test_dir = self.temp_dir / "new_dir"
        
        self.file_manager.ensure_directory(test_dir)
        
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_ensure_directory_existing_directory(self):
        """Test ensure_directory with existing directory."""
        test_dir = self.temp_dir / "existing_dir"
        test_dir.mkdir()
        
        # Should not raise error
        self.file_manager.ensure_directory(test_dir)
        
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_copy_file_success(self):
        """Test successful file copying."""
        source_file = self.temp_dir / "source.txt"
        dest_file = self.temp_dir / "dest.txt"
        test_content = "Hello, World!"
        
        # Create source file
        source_file.write_text(test_content)
        
        # Copy file
        self.file_manager.copy_file(source_file, dest_file)
        
        # Verify copy
        assert dest_file.exists()
        assert dest_file.read_text() == test_content
    
    def test_copy_file_source_not_found(self):
        """Test copying non-existent source file."""
        source_file = self.temp_dir / "nonexistent.txt"
        dest_file = self.temp_dir / "dest.txt"
        
        with pytest.raises(FileNotFoundError):
            self.file_manager.copy_file(source_file, dest_file)
    
    def test_copy_file_permission_error(self):
        """Test copying a file with permission error."""
        source_file = self.temp_dir / "source.txt"
        dest_file = self.temp_dir / "dest.txt"
        test_content = "Hello, World!"
        
        # Create source file
        source_file.write_text(test_content)
        
        with patch('shutil.copy2', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError, match="Permission denied copying to"):
                self.file_manager.copy_file(source_file, dest_file)
    
    def test_move_file_success(self):
        """Test successful file moving."""
        source_file = self.temp_dir / "source.txt"
        dest_file = self.temp_dir / "dest.txt"
        test_content = "Hello, World!"
        
        # Create source file
        source_file.write_text(test_content)
        
        # Move file
        self.file_manager.move_file(source_file, dest_file)
        
        # Verify move
        assert not source_file.exists()
        assert dest_file.exists()
        assert dest_file.read_text() == test_content
    
    def test_move_file_source_not_found(self):
        """Test moving non-existent source file."""
        source_file = self.temp_dir / "nonexistent.txt"
        dest_file = self.temp_dir / "dest.txt"
        
        with pytest.raises(FileNotFoundError):
            self.file_manager.move_file(source_file, dest_file)
    
    def test_move_file_permission_error(self):
        """Test moving a file with permission error."""
        source_file = self.temp_dir / "source.txt"
        dest_file = self.temp_dir / "dest.txt"
        test_content = "Hello, World!"
        
        # Create source file
        source_file.write_text(test_content)
        
        with patch('shutil.move', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError, match="Permission denied moving to"):
                self.file_manager.move_file(source_file, dest_file)
    
    def test_delete_file_success(self):
        """Test successful file deletion."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test")
        
        # Delete file
        self.file_manager.delete_file(test_file)
        
        # Verify deletion
        assert not test_file.exists()
    
    def test_delete_file_not_found(self):
        """Test deleting non-existent file."""
        non_existent_file = self.temp_dir / "nonexistent.txt"
        
        with pytest.raises(FileNotFoundError):
            self.file_manager.delete_file(non_existent_file)
    
    def test_delete_file_permission_error(self):
        """Test deleting a file with permission error."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test content")
        
        with patch.object(Path, 'unlink', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError, match="Permission denied deleting"):
                self.file_manager.delete_file(test_file)


class TestFileIOFunctions:
    """Test cases for file I/O functions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_read_file_function(self):
        """Test read_file function."""
        test_file = self.temp_dir / "test.txt"
        test_content = "Hello, World!"
        
        # Write test content
        test_file.write_text(test_content)
        
        # Read and verify
        result = read_file(test_file)
        assert result == test_content
    
    def test_write_file_function(self):
        """Test write_file function."""
        test_file = self.temp_dir / "test.txt"
        test_content = "Hello, World!"
        
        # Write content
        write_file(test_file, test_content)
        
        # Verify content
        assert test_file.exists()
        assert test_file.read_text() == test_content
    
    def test_file_exists_function(self):
        """Test file_exists function."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test")
        
        assert file_exists(test_file) is True
        assert file_exists(self.temp_dir / "nonexistent.txt") is False
    
    def test_ensure_directory_function(self):
        """Test ensure_directory function."""
        test_dir = self.temp_dir / "new_dir"
        
        ensure_directory(test_dir)
        
        assert test_dir.exists()
        assert test_dir.is_dir()
