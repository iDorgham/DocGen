"""
File I/O utilities for DocGen CLI.

This module provides file operations with proper error handling.
"""

from pathlib import Path
from typing import Union


def read_file(file_path: Union[str, Path]) -> str:
    """
    Read content from a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    try:
        return path.read_text(encoding='utf-8')
    except PermissionError:
        raise PermissionError(f"Permission denied: {path}")


def write_file(file_path: Union[str, Path], content: str) -> None:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Raises:
        PermissionError: If file cannot be written
    """
    path = Path(file_path)
    
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        path.write_text(content, encoding='utf-8')
    except PermissionError:
        raise PermissionError(f"Permission denied: {path}")


def file_exists(file_path: Union[str, Path]) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if file exists, False otherwise
    """
    path = Path(file_path)
    return path.exists() and path.is_file()


def ensure_directory(dir_path: Union[str, Path]) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        dir_path: Path to the directory
    """
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)


class FileManager:
    """
    File management class for DocGen CLI.
    
    Provides comprehensive file operations with proper error handling
    and validation.
    """
    
    def __init__(self):
        """Initialize the file manager."""
        pass
    
    def read_file(self, file_path: Union[str, Path]) -> str:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file cannot be read
        """
        return read_file(file_path)
    
    def write_file(self, file_path: Union[str, Path], content: str) -> None:
        """
        Write content to a file.
        
        Args:
            file_path: Path to the file to write
            content: Content to write to the file
            
        Raises:
            PermissionError: If file cannot be written
        """
        write_file(file_path, content)
    
    def file_exists(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return file_exists(file_path)
    
    def ensure_directory(self, dir_path: Union[str, Path]) -> None:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            dir_path: Path to the directory
        """
        ensure_directory(dir_path)
    
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> None:
        """
        Copy a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Raises:
            FileNotFoundError: If source file doesn't exist
            PermissionError: If file cannot be copied
        """
        import shutil
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(source_path, dest_path)
        except PermissionError:
            raise PermissionError(f"Permission denied copying to: {dest_path}")
    
    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> None:
        """
        Move a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Raises:
            FileNotFoundError: If source file doesn't exist
            PermissionError: If file cannot be moved
        """
        import shutil
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(source_path), str(dest_path))
        except PermissionError:
            raise PermissionError(f"Permission denied moving to: {dest_path}")
    
    def delete_file(self, file_path: Union[str, Path]) -> None:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file cannot be deleted
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            path.unlink()
        except PermissionError:
            raise PermissionError(f"Permission denied deleting: {path}")