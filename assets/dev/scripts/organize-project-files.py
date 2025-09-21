#!/usr/bin/env python3
"""
Project File Organization Script

This script automatically organizes project files according to the established
naming conventions and directory structure rules.

Usage:
    python organize-project-files.py [--dry-run] [--verbose]

Options:
    --dry-run    Show what would be done without making changes
    --verbose    Show detailed output
"""

import os
import sys
import shutil
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

class ProjectFileOrganizer:
    """Organizes project files according to established rules."""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.moves_made = []
        self.errors = []
        
        # Define file placement rules
        self.placement_rules = {
            # Documentation files
            '*.md': 'assets/docs/project-docs/',
            'AGENTS.md': 'assets/docs/project-docs/agents.md',
            'API_REFERENCE.md': 'assets/docs/project-docs/api-reference.md',
            'CHANGELOG.md': 'assets/docs/project-docs/changelog.md',
            'CLAUDE.md': 'assets/docs/project-docs/claude.md',
            'CODE_OF_CONDUCT.md': 'assets/docs/project-docs/code-of-conduct.md',
            'CONTRIBUTING.md': 'assets/docs/project-docs/contributing.md',
            'DEPLOYMENT.md': 'assets/docs/project-docs/deployment.md',
            'INSTALLATION.md': 'assets/docs/project-docs/installation.md',
            'SECURITY.md': 'assets/docs/project-docs/security.md',
            'USER_GUIDE.md': 'assets/docs/project-docs/user-guide.md',
            
            # Report files
            '*_SUMMARY.md': 'assets/reports/',
            '*_REPORT.md': 'assets/reports/',
            'COMPREHENSIVE_BROWSER_AUTOMATION_SUMMARY.md': 'assets/reports/comprehensive-browser-automation-summary.md',
            'PHASE3_COMPLETION_SUMMARY.md': 'assets/reports/phase3-completion-summary.md',
            'PHASE3_FINAL_REPORT.md': 'assets/reports/phase3-final-report.md',
            'PLAYWRIGHT_INTEGRATION_SUMMARY.md': 'assets/reports/playwright-integration-summary.md',
            'PRODUCTION_DEPLOYMENT_SUMMARY.md': 'assets/reports/production-deployment-summary.md',
            'TEST_COVERAGE_IMPLEMENTATION_SUMMARY.md': 'assets/reports/test-coverage-implementation-summary.md',
            'TESTSPRITE_API_CONFIGURATION_SUMMARY.md': 'assets/reports/testsprite-api-configuration-summary.md',
            
            # Setup guides
            'TESTSPRITE_SETUP_GUIDE.md': 'assets/docs/developer/testsprite-setup-guide.md',
            
            # Script files
            'debug_tests.py': 'assets/dev/scripts/debug-tests.py',
            'run_tests.py': 'assets/dev/scripts/run-tests.py',
            'test_standalone.py': 'assets/dev/scripts/test-standalone.py',
            
            # Data files
            'output.j2': 'assets/data/output.j2',
            'output.txt': 'assets/data/output.txt',
            'test-project': 'assets/data/test-project',
            'testsprite_tests': 'assets/reports/testsprite-tests',
            'release_artifacts': 'assets/data/release-artifacts',
        }
        
        # Files allowed in root
        self.allowed_root_files = {
            'README.md', 'pyproject.toml', 'requirements.txt', 'pytest.ini',
            '.gitignore', '.env.example', '.env', 'LICENSE', 'docker-compose.yml',
            'Dockerfile', 'Dockerfile.prod', 'docgen_cli.py', 'BYTEROVER.md', 'venv'
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with appropriate level."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{level}] {message}")
    
    def convert_to_lowercase_hyphen(self, filename: str) -> str:
        """Convert filename to lowercase-hyphen format."""
        # Remove extension
        name, ext = os.path.splitext(filename)
        
        # Convert to lowercase
        name = name.lower()
        
        # Replace underscores and spaces with hyphens
        name = re.sub(r'[_ ]+', '-', name)
        
        # Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)
        
        # Remove leading/trailing hyphens
        name = name.strip('-')
        
        return f"{name}{ext}"
    
    def get_target_path(self, filename: str) -> Tuple[Path, str]:
        """Get the target path for a file based on placement rules."""
        # Check for exact matches first
        if filename in self.placement_rules:
            target = self.placement_rules[filename]
            if target.endswith('/'):
                # Directory target, convert filename
                new_name = self.convert_to_lowercase_hyphen(filename)
                return self.project_root / target, new_name
            else:
                # Full path target
                return self.project_root / target, None
        
        # Check for pattern matches
        for pattern, target_dir in self.placement_rules.items():
            if pattern.startswith('*') and filename.endswith(pattern[1:]):
                new_name = self.convert_to_lowercase_hyphen(filename)
                return self.project_root / target_dir, new_name
        
        return None, None
    
    def should_move_file(self, filename: str) -> bool:
        """Check if a file should be moved from root."""
        # Don't move allowed root files
        if filename in self.allowed_root_files:
            return False
        
        # Don't move directories that are already in correct location
        if filename in ['src', 'tests', 'assets', 'venv']:
            return False
        
        # Don't move hidden files/directories
        if filename.startswith('.'):
            return False
        
        return True
    
    def create_directory(self, path: Path):
        """Create directory if it doesn't exist."""
        if not path.exists():
            if not self.dry_run:
                path.mkdir(parents=True, exist_ok=True)
            self.log(f"Created directory: {path}")
    
    def move_file(self, src: Path, dst: Path, new_name: str = None):
        """Move a file to its target location."""
        if new_name:
            dst = dst / new_name
        
        # Create target directory if it doesn't exist
        self.create_directory(dst.parent)
        
        if not self.dry_run:
            try:
                shutil.move(str(src), str(dst))
                self.moves_made.append((str(src), str(dst)))
                self.log(f"Moved: {src} → {dst}")
            except Exception as e:
                self.errors.append(f"Failed to move {src} to {dst}: {e}")
                self.log(f"Error moving {src}: {e}", "ERROR")
        else:
            self.log(f"Would move: {src} → {dst}")
    
    def organize_root_files(self):
        """Organize files in the root directory."""
        self.log("Organizing root directory files...")
        
        root_files = [f for f in os.listdir(self.project_root) 
                     if os.path.isfile(os.path.join(self.project_root, f))]
        
        for filename in root_files:
            if not self.should_move_file(filename):
                continue
            
            src_path = self.project_root / filename
            target_path, new_name = self.get_target_path(filename)
            
            if target_path:
                self.move_file(src_path, target_path, new_name)
            else:
                self.log(f"No placement rule for: {filename}", "WARNING")
    
    def organize_directories(self):
        """Organize directories in the root directory."""
        self.log("Organizing root directory subdirectories...")
        
        root_dirs = [d for d in os.listdir(self.project_root) 
                    if os.path.isdir(os.path.join(self.project_root, d))]
        
        for dirname in root_dirs:
            if not self.should_move_file(dirname):
                continue
            
            src_path = self.project_root / dirname
            target_path, new_name = self.get_target_path(dirname)
            
            if target_path:
                self.move_file(src_path, target_path, new_name)
            else:
                self.log(f"No placement rule for directory: {dirname}", "WARNING")
    
    def validate_structure(self):
        """Validate the current project structure."""
        self.log("Validating project structure...")
        
        # Check for forbidden files in root
        root_files = [f for f in os.listdir(self.project_root) 
                     if os.path.isfile(os.path.join(self.project_root, f))]
        
        forbidden_files = []
        for filename in root_files:
            if filename not in self.allowed_root_files:
                forbidden_files.append(filename)
        
        if forbidden_files:
            self.log(f"Found forbidden files in root: {forbidden_files}", "WARNING")
        else:
            self.log("Root directory is clean ✓")
        
        # Check directory structure
        required_dirs = [
            'assets/docs/project-docs',
            'assets/docs/developer',
            'assets/reports',
            'assets/dev/scripts',
            'assets/data',
            'src',
            'tests'
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            self.log(f"Missing required directories: {missing_dirs}", "WARNING")
        else:
            self.log("Directory structure is valid ✓")
    
    def run(self):
        """Run the file organization process."""
        self.log("Starting project file organization...")
        
        if self.dry_run:
            self.log("DRY RUN MODE - No changes will be made")
        
        try:
            self.organize_root_files()
            self.organize_directories()
            self.validate_structure()
            
            # Summary
            self.log(f"\nOrganization complete!")
            self.log(f"Moves made: {len(self.moves_made)}")
            self.log(f"Errors: {len(self.errors)}")
            
            if self.errors:
                self.log("\nErrors encountered:", "ERROR")
                for error in self.errors:
                    self.log(f"  - {error}", "ERROR")
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.log(f"Organization failed: {e}", "ERROR")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Organize project files according to established rules")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    organizer = ProjectFileOrganizer(dry_run=args.dry_run, verbose=args.verbose)
    success = organizer.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
