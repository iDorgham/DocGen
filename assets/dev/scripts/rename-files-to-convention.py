#!/usr/bin/env python3
"""
File Renaming Script

This script automatically renames all files to follow the lowercase-hyphen
naming convention throughout the project.

Usage:
    python rename-files-to-convention.py [--dry-run] [--verbose]

Options:
    --dry-run    Show what would be done without making changes
    --verbose    Show detailed output
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

class FileRenamer:
    """Renames files to follow lowercase-hyphen naming convention."""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.renames_made = []
        self.errors = []
        
        # Files to skip (keep as-is)
        self.skip_files = {
            'README.md',  # Keep README.md as-is (common convention)
            'LICENSE',    # Keep LICENSE as-is
            'pyproject.toml',
            'requirements.txt',
            'pytest.ini',
            '.gitignore',
            '.env.example',
            '.env',
            'docker-compose.yml',
            'Dockerfile',
            'Dockerfile.prod',
            'docgen_cli.py',
            'BYTEROVER.md'
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with appropriate level."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{level}] {message}")
    
    def convert_to_lowercase_hyphen(self, filename: str) -> str:
        """Convert filename to lowercase-hyphen format."""
        # Remove extension
        name, ext = os.path.splitext(filename)
        
        # Skip if file should not be renamed
        if filename in self.skip_files:
            return filename
        
        # Convert to lowercase
        name = name.lower()
        
        # Replace underscores and spaces with hyphens
        name = re.sub(r'[_ ]+', '-', name)
        
        # Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)
        
        # Remove leading/trailing hyphens
        name = name.strip('-')
        
        return f"{name}{ext}"
    
    def rename_file(self, file_path: Path):
        """Rename a single file to follow naming convention."""
        old_name = file_path.name
        new_name = self.convert_to_lowercase_hyphen(old_name)
        
        if old_name == new_name:
            return  # No change needed
        
        new_path = file_path.parent / new_name
        
        # Check if target already exists
        if new_path.exists():
            self.log(f"Target already exists: {new_path}", "WARNING")
            return
        
        if not self.dry_run:
            try:
                file_path.rename(new_path)
                self.renames_made.append((str(file_path), str(new_path)))
                self.log(f"Renamed: {file_path} → {new_path}")
            except Exception as e:
                self.errors.append(f"Failed to rename {file_path}: {e}")
                self.log(f"Error renaming {file_path}: {e}", "ERROR")
        else:
            self.log(f"Would rename: {file_path} → {new_path}")
    
    def rename_directory(self, dir_path: Path):
        """Rename a directory to follow naming convention."""
        old_name = dir_path.name
        new_name = self.convert_to_lowercase_hyphen(old_name)
        
        if old_name == new_name:
            return  # No change needed
        
        new_path = dir_path.parent / new_name
        
        # Check if target already exists
        if new_path.exists():
            self.log(f"Target directory already exists: {new_path}", "WARNING")
            return
        
        if not self.dry_run:
            try:
                dir_path.rename(new_path)
                self.renames_made.append((str(dir_path), str(new_path)))
                self.log(f"Renamed directory: {dir_path} → {new_path}")
            except Exception as e:
                self.errors.append(f"Failed to rename directory {dir_path}: {e}")
                self.log(f"Error renaming directory {dir_path}: {e}", "ERROR")
        else:
            self.log(f"Would rename directory: {dir_path} → {new_path}")
    
    def process_directory(self, directory: Path):
        """Process all files and directories in a directory."""
        if not directory.exists():
            return
        
        # First, rename all files
        for item in directory.iterdir():
            if item.is_file():
                self.rename_file(item)
            elif item.is_dir():
                # Recursively process subdirectories
                self.process_directory(item)
                # Then rename the directory itself
                self.rename_directory(item)
    
    def run(self):
        """Run the file renaming process."""
        self.log("Starting file renaming process...")
        
        if self.dry_run:
            self.log("DRY RUN MODE - No changes will be made")
        
        try:
            # Process assets directory
            assets_path = self.project_root / 'assets'
            if assets_path.exists():
                self.log("Processing assets directory...")
                self.process_directory(assets_path)
            
            # Process tests directory
            tests_path = self.project_root / 'tests'
            if tests_path.exists():
                self.log("Processing tests directory...")
                self.process_directory(tests_path)
            
            # Process src directory
            src_path = self.project_root / 'src'
            if src_path.exists():
                self.log("Processing src directory...")
                self.process_directory(src_path)
            
            # Summary
            self.log(f"\nRenaming complete!")
            self.log(f"Files renamed: {len(self.renames_made)}")
            self.log(f"Errors: {len(self.errors)}")
            
            if self.errors:
                self.log("\nErrors encountered:", "ERROR")
                for error in self.errors:
                    self.log(f"  - {error}", "ERROR")
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.log(f"Renaming failed: {e}", "ERROR")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Rename files to follow lowercase-hyphen naming convention")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    renamer = FileRenamer(dry_run=args.dry_run, verbose=args.verbose)
    success = renamer.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
