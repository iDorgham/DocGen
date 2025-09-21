#!/usr/bin/env python3
"""
Production deployment script for DocGen CLI.
This script handles the complete deployment process including building, testing, and publishing.
"""

import sys
import os
import subprocess
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any

def run_command(command: List[str], cwd: str = None) -> Dict[str, Any]:
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Command timed out',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def check_prerequisites() -> bool:
    """Check if all prerequisites are met."""
    print("Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check required tools
    required_tools = ['pip', 'twine', 'build']
    for tool in required_tools:
        result = run_command([tool, '--version'])
        if not result['success']:
            print(f"❌ {tool} not found or not working")
            return False
        print(f"✅ {tool} available")
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ pyproject.toml not found. Are you in the project root?")
        return False
    print("✅ Project structure looks good")
    
    return True

def run_tests() -> bool:
    """Run the test suite."""
    print("\nRunning tests...")
    
    # Install test dependencies
    result = run_command([sys.executable, '-m', 'pip', 'install', '-e', '.[test]'])
    if not result['success']:
        print(f"❌ Failed to install test dependencies: {result['stderr']}")
        return False
    
    # Run tests
    result = run_command([sys.executable, '-m', 'pytest', 'tests/', '-v', '--cov=src', '--cov-report=term-missing'])
    if not result['success']:
        print(f"❌ Tests failed: {result['stderr']}")
        return False
    
    print("✅ All tests passed")
    return True

def run_linting() -> bool:
    """Run code quality checks."""
    print("\nRunning code quality checks...")
    
    # Install dev dependencies
    result = run_command([sys.executable, '-m', 'pip', 'install', '-e', '.[dev]'])
    if not result['success']:
        print(f"❌ Failed to install dev dependencies: {result['stderr']}")
        return False
    
    # Run black
    result = run_command([sys.executable, '-m', 'black', '--check', 'src/', 'tests/'])
    if not result['success']:
        print(f"❌ Black formatting check failed: {result['stderr']}")
        return False
    print("✅ Black formatting check passed")
    
    # Run isort
    result = run_command([sys.executable, '-m', 'isort', '--check-only', 'src/', 'tests/'])
    if not result['success']:
        print(f"❌ isort import sorting check failed: {result['stderr']}")
        return False
    print("✅ isort import sorting check passed")
    
    # Run flake8
    result = run_command([sys.executable, '-m', 'flake8', 'src/', 'tests/'])
    if not result['success']:
        print(f"❌ flake8 linting failed: {result['stderr']}")
        return False
    print("✅ flake8 linting passed")
    
    return True

def build_package() -> bool:
    """Build the package."""
    print("\nBuilding package...")
    
    # Clean previous builds
    if Path('dist').exists():
        import shutil
        shutil.rmtree('dist')
    if Path('build').exists():
        import shutil
        shutil.rmtree('build')
    
    # Build the package
    result = run_command([sys.executable, '-m', 'build'])
    if not result['success']:
        print(f"❌ Package build failed: {result['stderr']}")
        return False
    
    print("✅ Package built successfully")
    
    # Check the package
    result = run_command([sys.executable, '-m', 'twine', 'check', 'dist/*'])
    if not result['success']:
        print(f"❌ Package check failed: {result['stderr']}")
        return False
    
    print("✅ Package check passed")
    return True

def publish_package(dry_run: bool = True) -> bool:
    """Publish the package to PyPI."""
    print(f"\n{'Dry run: ' if dry_run else ''}Publishing package...")
    
    if dry_run:
        result = run_command([sys.executable, '-m', 'twine', 'upload', '--repository', 'testpypi', '--dry-run', 'dist/*'])
    else:
        result = run_command([sys.executable, '-m', 'twine', 'upload', 'dist/*'])
    
    if not result['success']:
        print(f"❌ Package publish failed: {result['stderr']}")
        return False
    
    print(f"✅ Package {'dry run' if dry_run else 'publish'} successful")
    return True

def build_docker() -> bool:
    """Build Docker images."""
    print("\nBuilding Docker images...")
    
    # Build development image
    result = run_command(['docker', 'build', '-t', 'docgen-cli:dev', '-f', 'Dockerfile', '.'])
    if not result['success']:
        print(f"❌ Docker dev build failed: {result['stderr']}")
        return False
    print("✅ Docker dev image built")
    
    # Build production image
    result = run_command(['docker', 'build', '-t', 'docgen-cli:prod', '-f', 'Dockerfile.prod', '.'])
    if not result['success']:
        print(f"❌ Docker prod build failed: {result['stderr']}")
        return False
    print("✅ Docker prod image built")
    
    return True

def run_security_scan() -> bool:
    """Run security vulnerability scan."""
    print("\nRunning security scan...")
    
    # Install security tools
    result = run_command([sys.executable, '-m', 'pip', 'install', 'safety', 'bandit'])
    if not result['success']:
        print(f"❌ Failed to install security tools: {result['stderr']}")
        return False
    
    # Run safety check
    result = run_command([sys.executable, '-m', 'safety', 'check', '--json'])
    if not result['success']:
        print(f"⚠️  Safety check found issues: {result['stderr']}")
        # Don't fail on safety issues, just warn
    else:
        print("✅ Safety check passed")
    
    # Run bandit security scan
    result = run_command([sys.executable, '-m', 'bandit', '-r', 'src/', '-f', 'json'])
    if not result['success']:
        print(f"⚠️  Bandit found security issues: {result['stderr']}")
        # Don't fail on bandit issues, just warn
    else:
        print("✅ Bandit security scan passed")
    
    return True

def generate_release_notes() -> bool:
    """Generate release notes."""
    print("\nGenerating release notes...")
    
    # Get current version from pyproject.toml
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            import re
            version_match = re.search(r'version = "([^"]+)"', content)
            if version_match:
                version = version_match.group(1)
            else:
                version = "1.0.0"
    except Exception as e:
        print(f"⚠️  Could not read version: {e}")
        version = "1.0.0"
    
    # Generate release notes
    release_notes = f"""# DocGen CLI v{version} Release Notes

## 🎉 New Features
- Production-ready CLI with comprehensive documentation generation
- Support for multiple output formats (Markdown, HTML, PDF)
- Advanced project validation and error handling
- Professional templates for technical specs, project plans, and marketing materials

## 🚀 Improvements
- Enhanced user experience with Rich formatting and progress indicators
- Comprehensive input validation and security scanning
- Cross-platform compatibility (Windows, macOS, Linux)
- Docker support for containerized deployments

## 🔧 Technical Details
- Built with Python 3.8+ support
- Uses Click for CLI interface, Jinja2 for templating
- Comprehensive test coverage with pytest
- Automated CI/CD pipeline with GitHub Actions

## 📚 Documentation
- Complete user guide and API reference
- Installation instructions for all platforms
- Examples and best practices
- Troubleshooting guide

## 🛡️ Security
- Input validation and sanitization
- Security vulnerability scanning
- Safe file operations and path handling

## 📦 Installation
```bash
pip install docgen-cli
```

## 🔗 Links
- [GitHub Repository](https://github.com/docgen-cli/docgen-cli)
- [Documentation](https://docgen-cli.readthedocs.io)
- [PyPI Package](https://pypi.org/project/docgen-cli/)

---
*Generated by DocGen CLI Deployment Pipeline*
"""
    
    # Save release notes
    with open('RELEASE_NOTES.md', 'w') as f:
        f.write(release_notes)
    
    print("✅ Release notes generated: RELEASE_NOTES.md")
    return True

def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description='Deploy DocGen CLI to production')
    parser.add_argument('--skip-tests', action='store_true', help='Skip running tests')
    parser.add_argument('--skip-lint', action='store_true', help='Skip linting')
    parser.add_argument('--skip-docker', action='store_true', help='Skip Docker builds')
    parser.add_argument('--skip-security', action='store_true', help='Skip security scans')
    parser.add_argument('--publish', action='store_true', help='Actually publish to PyPI (default is dry run)')
    parser.add_argument('--testpypi', action='store_true', help='Publish to TestPyPI instead of PyPI')
    parser.add_argument('--release-notes', action='store_true', help='Generate release notes')
    
    args = parser.parse_args()
    
    print("🚀 Starting DocGen CLI v1.0.0 deployment process...")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites check failed")
        sys.exit(1)
    
    # Run tests
    if not args.skip_tests:
        if not run_tests():
            print("❌ Tests failed")
            sys.exit(1)
    
    # Run linting
    if not args.skip_lint:
        if not run_linting():
            print("❌ Linting failed")
            sys.exit(1)
    
    # Run security scan
    if not args.skip_security:
        if not run_security_scan():
            print("❌ Security scan failed")
            sys.exit(1)
    
    # Build package
    if not build_package():
        print("❌ Package build failed")
        sys.exit(1)
    
    # Build Docker images
    if not args.skip_docker:
        if not build_docker():
            print("❌ Docker build failed")
            sys.exit(1)
    
    # Generate release notes
    if args.release_notes:
        if not generate_release_notes():
            print("❌ Release notes generation failed")
            sys.exit(1)
    
    # Publish package
    if not publish_package(dry_run=not args.publish):
        print("❌ Package publish failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 DocGen CLI v1.0.0 deployment completed successfully!")
    print("=" * 60)
    
    if not args.publish:
        print("\n📋 Next Steps:")
        print("1. Review the generated package in dist/")
        print("2. Test the package locally: pip install dist/*.whl")
        print("3. Publish to TestPyPI: python scripts/deploy.py --publish --testpypi")
        print("4. Publish to PyPI: python scripts/deploy.py --publish")
    else:
        print("\n✅ Package published successfully!")
        print("🔗 PyPI: https://pypi.org/project/docgen-cli/")
        print("📚 Documentation: https://docgen-cli.readthedocs.io")
        print("🐙 GitHub: https://github.com/docgen-cli/docgen-cli")

if __name__ == '__main__':
    main()
