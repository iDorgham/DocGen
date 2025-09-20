"""
Git Integration Manager for DocGen CLI.

This module provides comprehensive Git integration capabilities including
repository initialization, commit management, and automated Git operations.
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
import json

from .error_handler import DocGenError, FileIOError, ValidationError


@dataclass
class GitConfig:
    """Git configuration for DocGen projects."""
    auto_init: bool = True
    auto_commit: bool = True
    commit_message_template: str = "docs: update {document_type}"
    default_branch: str = "main"
    remote_origin: Optional[str] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None


@dataclass
class GitStatus:
    """Git repository status information."""
    is_git_repo: bool
    current_branch: Optional[str]
    has_uncommitted_changes: bool
    untracked_files: List[str]
    modified_files: List[str]
    staged_files: List[str]
    remote_url: Optional[str]
    last_commit: Optional[str]


class GitManager:
    """Manages Git operations for DocGen projects."""
    
    def __init__(self, project_path: Path, config: Optional[GitConfig] = None):
        """Initialize the Git manager.
        
        Args:
            project_path: Path to the project directory
            config: Git configuration options
        """
        self.project_path = project_path
        self.config = config or GitConfig()
        self.git_dir = project_path / ".git"
        
    def _run_git_command(self, command: List[str], capture_output: bool = True) -> Tuple[bool, str, str]:
        """Run a Git command and return the result.
        
        Args:
            command: Git command as list of strings
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            # Ensure we're in the project directory
            original_cwd = os.getcwd()
            os.chdir(self.project_path)
            
            # Run the command
            result = subprocess.run(
                ["git"] + command,
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            raise DocGenError(f"Git command timed out: {' '.join(command)}")
        except FileNotFoundError:
            raise DocGenError("Git is not installed or not in PATH")
        except Exception as e:
            raise DocGenError(f"Git command failed: {e}")
        finally:
            os.chdir(original_cwd)
    
    def is_git_repository(self) -> bool:
        """Check if the project directory is a Git repository.
        
        Returns:
            True if it's a Git repository, False otherwise
        """
        return self.git_dir.exists() and self.git_dir.is_dir()
    
    def initialize_repository(self, initial_commit: bool = True) -> bool:
        """Initialize a Git repository for the project.
        
        Args:
            initial_commit: Whether to create an initial commit
            
        Returns:
            True if repository was initialized successfully
            
        Raises:
            DocGenError: If initialization fails
        """
        if self.is_git_repository():
            return True  # Already a Git repository
        
        try:
            # Initialize Git repository
            success, stdout, stderr = self._run_git_command(["init"])
            if not success:
                raise DocGenError(f"Failed to initialize Git repository: {stderr}")
            
            # Set default branch if specified
            if self.config.default_branch != "master":
                success, stdout, stderr = self._run_git_command([
                    "branch", "-M", self.config.default_branch
                ])
                if not success:
                    # Branch rename might fail if no commits exist yet
                    pass
            
            # Configure Git user if specified
            if self.config.user_name:
                self._run_git_command(["config", "user.name", self.config.user_name])
            
            if self.config.user_email:
                self._run_git_command(["config", "user.email", self.config.user_email])
            
            # Create .gitignore if it doesn't exist
            self._create_gitignore()
            
            # Create initial commit if requested
            if initial_commit:
                self._create_initial_commit()
            
            return True
            
        except Exception as e:
            raise DocGenError(f"Failed to initialize Git repository: {e}")
    
    def _create_gitignore(self) -> None:
        """Create a .gitignore file for the project."""
        gitignore_path = self.project_path / ".gitignore"
        
        if gitignore_path.exists():
            return  # .gitignore already exists
        
        gitignore_content = """# DocGen Project
# Generated documents
*.md
*.html
*.pdf
*.docx

# Project data (optional - uncomment if you want to exclude)
# project_data.yaml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
"""
        
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
        except IOError as e:
            raise FileIOError(f"Failed to create .gitignore: {e}")
    
    def _create_initial_commit(self) -> None:
        """Create the initial commit."""
        # Add all files
        success, stdout, stderr = self._run_git_command(["add", "."])
        if not success:
            return  # No files to add
        
        # Check if there are any changes to commit
        success, stdout, stderr = self._run_git_command(["diff", "--cached", "--quiet"])
        if success:
            return  # No changes to commit
        
        # Create initial commit
        success, stdout, stderr = self._run_git_command([
            "commit", "-m", "Initial commit: DocGen project setup"
        ])
        
        if not success:
            raise DocGenError(f"Failed to create initial commit: {stderr}")
    
    def get_status(self) -> GitStatus:
        """Get the current Git repository status.
        
        Returns:
            GitStatus object with repository information
        """
        if not self.is_git_repository():
            return GitStatus(
                is_git_repo=False,
                current_branch=None,
                has_uncommitted_changes=False,
                untracked_files=[],
                modified_files=[],
                staged_files=[],
                remote_url=None,
                last_commit=None
            )
        
        # Get current branch
        success, stdout, stderr = self._run_git_command(["branch", "--show-current"])
        current_branch = stdout.strip() if success and stdout.strip() else None
        
        # Get untracked files
        success, stdout, stderr = self._run_git_command(["ls-files", "--others", "--exclude-standard"])
        untracked_files = stdout.strip().split('\n') if stdout.strip() else []
        
        # Get modified files
        success, stdout, stderr = self._run_git_command(["diff", "--name-only"])
        modified_files = stdout.strip().split('\n') if stdout.strip() else []
        
        # Get staged files
        success, stdout, stderr = self._run_git_command(["diff", "--cached", "--name-only"])
        staged_files = stdout.strip().split('\n') if stdout.strip() else []
        
        # Get remote URL
        success, stdout, stderr = self._run_git_command(["remote", "get-url", "origin"])
        remote_url = stdout.strip() if success and stdout.strip() else None
        
        # Get last commit
        success, stdout, stderr = self._run_git_command(["log", "-1", "--format=%H"])
        last_commit = stdout.strip() if success and stdout.strip() else None
        
        # Check if there are uncommitted changes
        has_uncommitted_changes = bool(untracked_files or modified_files or staged_files)
        
        return GitStatus(
            is_git_repo=True,
            current_branch=current_branch,
            has_uncommitted_changes=has_uncommitted_changes,
            untracked_files=untracked_files,
            modified_files=modified_files,
            staged_files=staged_files,
            remote_url=remote_url,
            last_commit=last_commit
        )
    
    def add_files(self, files: List[str]) -> bool:
        """Add files to the Git staging area.
        
        Args:
            files: List of file paths to add
            
        Returns:
            True if files were added successfully
        """
        if not self.is_git_repository():
            return False
        
        if not files:
            return True
        
        success, stdout, stderr = self._run_git_command(["add"] + files)
        return success
    
    def commit_changes(self, message: str, files: Optional[List[str]] = None) -> bool:
        """Commit changes to the repository.
        
        Args:
            message: Commit message
            files: Optional list of specific files to commit
            
        Returns:
            True if commit was successful
        """
        if not self.is_git_repository():
            return False
        
        # Add files if specified
        if files:
            if not self.add_files(files):
                return False
        else:
            # Add all changes
            success, stdout, stderr = self._run_git_command(["add", "."])
            if not success:
                return False
        
        # Check if there are any changes to commit
        success, stdout, stderr = self._run_git_command(["diff", "--cached", "--quiet"])
        if success:
            return True  # No changes to commit
        
        # Create commit
        success, stdout, stderr = self._run_git_command(["commit", "-m", message])
        return success
    
    def create_commit_for_documents(self, document_type: str, files: List[str]) -> bool:
        """Create a commit specifically for generated documents.
        
        Args:
            document_type: Type of document (spec, plan, marketing)
            files: List of generated files
            
        Returns:
            True if commit was successful
        """
        if not files:
            return True
        
        # Generate commit message
        message = self.config.commit_message_template.format(
            document_type=document_type,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            file_count=len(files)
        )
        
        return self.commit_changes(message, files)
    
    def push_changes(self, branch: Optional[str] = None) -> bool:
        """Push changes to the remote repository.
        
        Args:
            branch: Branch to push (defaults to current branch)
            
        Returns:
            True if push was successful
        """
        if not self.is_git_repository():
            return False
        
        # Get current branch if not specified
        if not branch:
            status = self.get_status()
            branch = status.current_branch
        
        if not branch:
            return False
        
        # Push to remote
        success, stdout, stderr = self._run_git_command(["push", "origin", branch])
        return success
    
    def pull_changes(self, branch: Optional[str] = None) -> bool:
        """Pull changes from the remote repository.
        
        Args:
            branch: Branch to pull (defaults to current branch)
            
        Returns:
            True if pull was successful
        """
        if not self.is_git_repository():
            return False
        
        # Get current branch if not specified
        if not branch:
            status = self.get_status()
            branch = status.current_branch
        
        if not branch:
            return False
        
        # Pull from remote
        success, stdout, stderr = self._run_git_command(["pull", "origin", branch])
        return success
    
    def add_remote(self, name: str, url: str) -> bool:
        """Add a remote repository.
        
        Args:
            name: Remote name (e.g., 'origin')
            url: Remote URL
            
        Returns:
            True if remote was added successfully
        """
        if not self.is_git_repository():
            return False
        
        success, stdout, stderr = self._run_git_command(["remote", "add", name, url])
        return success
    
    def set_remote_url(self, name: str, url: str) -> bool:
        """Set the URL for an existing remote.
        
        Args:
            name: Remote name (e.g., 'origin')
            url: New remote URL
            
        Returns:
            True if remote URL was set successfully
        """
        if not self.is_git_repository():
            return False
        
        success, stdout, stderr = self._run_git_command(["remote", "set-url", name, url])
        return success
    
    def get_remotes(self) -> Dict[str, str]:
        """Get all remote repositories.
        
        Returns:
            Dictionary mapping remote names to URLs
        """
        if not self.is_git_repository():
            return {}
        
        success, stdout, stderr = self._run_git_command(["remote", "-v"])
        if not success:
            return {}
        
        remotes = {}
        for line in stdout.strip().split('\n'):
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    name = parts[0]
                    url = parts[1].split(' ')[0]  # Remove (fetch) or (push) suffix
                    remotes[name] = url
        
        return remotes
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """Create a new branch.
        
        Args:
            branch_name: Name of the new branch
            checkout: Whether to checkout the new branch
            
        Returns:
            True if branch was created successfully
        """
        if not self.is_git_repository():
            return False
        
        # Create branch
        success, stdout, stderr = self._run_git_command(["branch", branch_name])
        if not success:
            return False
        
        # Checkout branch if requested
        if checkout:
            success, stdout, stderr = self._run_git_command(["checkout", branch_name])
            return success
        
        return True
    
    def checkout_branch(self, branch_name: str) -> bool:
        """Checkout an existing branch.
        
        Args:
            branch_name: Name of the branch to checkout
            
        Returns:
            True if checkout was successful
        """
        if not self.is_git_repository():
            return False
        
        success, stdout, stderr = self._run_git_command(["checkout", branch_name])
        return success
    
    def get_branches(self) -> List[str]:
        """Get all branches.
        
        Returns:
            List of branch names
        """
        if not self.is_git_repository():
            return []
        
        success, stdout, stderr = self._run_git_command(["branch", "-a"])
        if not success:
            return []
        
        branches = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                # Remove * prefix for current branch and remote prefixes
                branch = line.strip().lstrip('* ').replace('remotes/origin/', '')
                if branch and branch not in branches:
                    branches.append(branch)
        
        return branches
    
    def get_commit_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent commit history.
        
        Args:
            limit: Maximum number of commits to return
            
        Returns:
            List of commit dictionaries with hash, message, author, and date
        """
        if not self.is_git_repository():
            return []
        
        success, stdout, stderr = self._run_git_command([
            "log", f"-{limit}", "--pretty=format:%H|%s|%an|%ad", "--date=short"
        ])
        
        if not success:
            return []
        
        commits = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        'hash': parts[0],
                        'message': parts[1],
                        'author': parts[2],
                        'date': parts[3]
                    })
        
        return commits
    
    def is_clean_working_directory(self) -> bool:
        """Check if the working directory is clean (no uncommitted changes).
        
        Returns:
            True if working directory is clean
        """
        status = self.get_status()
        return not status.has_uncommitted_changes
    
    def stash_changes(self, message: str = "DocGen: Stashed changes") -> bool:
        """Stash current changes.
        
        Args:
            message: Stash message
            
        Returns:
            True if stash was successful
        """
        if not self.is_git_repository():
            return False
        
        success, stdout, stderr = self._run_git_command(["stash", "push", "-m", message])
        return success
    
    def pop_stash(self) -> bool:
        """Pop the most recent stash.
        
        Returns:
            True if stash was popped successfully
        """
        if not self.is_git_repository():
            return False
        
        success, stdout, stderr = self._run_git_command(["stash", "pop"])
        return success
    
    def get_stash_list(self) -> List[Dict[str, str]]:
        """Get list of stashes.
        
        Returns:
            List of stash dictionaries with hash, message, and date
        """
        if not self.is_git_repository():
            return []
        
        success, stdout, stderr = self._run_git_command([
            "stash", "list", "--pretty=format:%gd|%gs|%gd"
        ])
        
        if not success:
            return []
        
        stashes = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('|')
                if len(parts) >= 2:
                    stashes.append({
                        'hash': parts[0],
                        'message': parts[1],
                        'date': parts[2] if len(parts) > 2 else ''
                    })
        
        return stashes

