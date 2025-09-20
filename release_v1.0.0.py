#!/usr/bin/env python3
"""
DocGen CLI v1.0.0 Release Script

This script automates the release process for DocGen CLI v1.0.0.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository")
        return False
    
    # Check if virtual environment is activated
    if not os.environ.get("VIRTUAL_ENV"):
        print("❌ Virtual environment not activated")
        return False
    
    # Check if required tools are available
    tools = ["git", "python", "pip", "twine"]
    for tool in tools:
        if not run_command(f"which {tool}", f"Checking {tool}"):
            print(f"❌ {tool} not found")
            return False
    
    print("✅ All prerequisites met")
    return True

def run_tests():
    """Run all tests to ensure everything is working."""
    print("🧪 Running tests...")
    
    # Run unit tests
    if not run_command("python -m pytest tests/ -v", "Running unit tests"):
        return False
    
    # Run linting
    if not run_command("python -m flake8 src/", "Running linting"):
        return False
    
    # Run type checking
    if not run_command("python -m mypy src/", "Running type checking"):
        return False
    
    print("✅ All tests passed")
    return True

def build_package():
    """Build the package for distribution."""
    print("📦 Building package...")
    
    # Clean previous builds
    run_command("rm -rf dist/ build/ *.egg-info/", "Cleaning previous builds")
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        return False
    
    # Check the built package
    if not run_command("twine check dist/*", "Checking package"):
        return False
    
    print("✅ Package built successfully")
    return True

def create_git_tag():
    """Create and push git tag for the release."""
    print("🏷️ Creating git tag...")
    
    tag_name = "v1.0.0"
    tag_message = "Release v1.0.0: Stable release with comprehensive features"
    
    # Create tag
    if not run_command(f"git tag -a {tag_name} -m '{tag_message}'", "Creating git tag"):
        return False
    
    # Push tag
    if not run_command(f"git push origin {tag_name}", "Pushing git tag"):
        return False
    
    print("✅ Git tag created and pushed")
    return True

def upload_to_pypi():
    """Upload package to PyPI."""
    print("📤 Uploading to PyPI...")
    
    # Upload to PyPI
    if not run_command("twine upload dist/*", "Uploading to PyPI"):
        return False
    
    print("✅ Package uploaded to PyPI")
    return True

def create_github_release():
    """Create GitHub release."""
    print("🐙 Creating GitHub release...")
    
    # This would typically use GitHub CLI or API
    print("📝 Manual step: Create GitHub release with tag v1.0.0")
    print("   - Upload release notes from RELEASE_NOTES.md")
    print("   - Upload built packages from dist/")
    print("   - Mark as latest release")
    
    return True

def main():
    """Main release process."""
    print("🚀 DocGen CLI v1.0.0 Release Process")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met. Aborting release.")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed. Aborting release.")
        sys.exit(1)
    
    # Build package
    if not build_package():
        print("❌ Package build failed. Aborting release.")
        sys.exit(1)
    
    # Create git tag
    if not create_git_tag():
        print("❌ Git tag creation failed. Aborting release.")
        sys.exit(1)
    
    # Upload to PyPI
    if not upload_to_pypi():
        print("❌ PyPI upload failed. Aborting release.")
        sys.exit(1)
    
    # Create GitHub release
    if not create_github_release():
        print("❌ GitHub release creation failed.")
        sys.exit(1)
    
    print("\n🎉 DocGen CLI v1.0.0 Release Complete!")
    print("=" * 50)
    print("✅ Package built and uploaded to PyPI")
    print("✅ Git tag created and pushed")
    print("✅ GitHub release ready for creation")
    print("\n📝 Next steps:")
    print("1. Create GitHub release with tag v1.0.0")
    print("2. Upload release notes from RELEASE_NOTES.md")
    print("3. Upload built packages from dist/")
    print("4. Announce release to community")
    print("\n🎊 Congratulations on the successful release!")

if __name__ == "__main__":
    main()
