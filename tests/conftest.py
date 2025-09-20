"""
Pytest configuration and shared fixtures for DocGen CLI tests.

This module provides common fixtures and configuration for all test modules.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch

import pytest
import yaml
from click.testing import CliRunner

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.cli.main import main as cli
from src.models.project_model import Project
from src.models.template_model import Template


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_project_data() -> Dict[str, Any]:
    """Provide sample project data for testing."""
    return {
        "name": "Test Project",
        "description": "A test project for DocGen CLI",
        "version": "1.0.0",
        "author": "Test Author",
        "email": "test@example.com",
        "license": "MIT",
        "repository": "https://github.com/test/test-project",
        "keywords": ["test", "documentation", "cli"],
        "requirements": [
            "click>=8.0.0",
            "jinja2>=3.0.0",
            "pyyaml>=6.0"
        ],
        "features": [
            "Command-line interface",
            "Template-based generation",
            "YAML configuration"
        ]
    }


@pytest.fixture
def sample_project_yaml(temp_dir: Path, sample_project_data: Dict[str, Any]) -> Path:
    """Create a sample project YAML file."""
    yaml_path = temp_dir / "project_data.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(sample_project_data, f)
    return yaml_path


@pytest.fixture
def mock_project() -> Project:
    """Provide a mock Project instance."""
    return Project(
        name="Test Project",
        description="A test project",
        version="1.0.0",
        author="Test Author",
        email="test@example.com"
    )


@pytest.fixture
def mock_template() -> Template:
    """Provide a mock Template instance."""
    return Template(
        name="test_template",
        content="# {{ project.name }}\n\n{{ project.description }}",
        output_path="test_output.md"
    )


@pytest.fixture
def mock_file_operations():
    """Mock file operations for testing."""
    with patch('src.utils.file_io.read_file') as mock_read, \
         patch('src.utils.file_io.write_file') as mock_write, \
         patch('src.utils.file_io.file_exists') as mock_exists:
        yield {
            'read': mock_read,
            'write': mock_write,
            'exists': mock_exists
        }


@pytest.fixture
def mock_git_operations():
    """Mock git operations for testing."""
    with patch('src.core.git_manager.GitManager') as mock_git:
        mock_git.return_value.is_git_repo.return_value = True
        mock_git.return_value.get_current_branch.return_value = "main"
        mock_git.return_value.get_commit_hash.return_value = "abc123"
        yield mock_git


@pytest.fixture
def mock_template_engine():
    """Mock Jinja2 template engine for testing."""
    with patch('jinja2.Environment') as mock_env:
        mock_template = Mock()
        mock_template.render.return_value = "Rendered content"
        mock_env.return_value.get_template.return_value = mock_template
        yield mock_env


@pytest.fixture
def test_templates_dir(temp_dir: Path) -> Path:
    """Create a test templates directory with sample templates."""
    templates_dir = temp_dir / "templates"
    templates_dir.mkdir()
    
    # Create sample templates
    (templates_dir / "project_plan.j2").write_text(
        "# {{ project.name }} Project Plan\n\n"
        "## Description\n{{ project.description }}\n\n"
        "## Version\n{{ project.version }}\n\n"
        "## Author\n{{ project.author }} <{{ project.email }}>"
    )
    
    (templates_dir / "technical_spec.j2").write_text(
        "# {{ project.name }} Technical Specification\n\n"
        "## Overview\n{{ project.description }}\n\n"
        "## Requirements\n"
        "{% for req in project.requirements %}\n"
        "- {{ req }}\n"
        "{% endfor %}"
    )
    
    return templates_dir


@pytest.fixture
def test_output_dir(temp_dir: Path) -> Path:
    """Create a test output directory."""
    output_dir = temp_dir / "output"
    output_dir.mkdir()
    return output_dir


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "cli: mark test as CLI test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "cli" in str(item.fspath):
            item.add_marker(pytest.mark.cli)
        
        # Add slow marker for tests that take > 1 second
        if "performance" in str(item.fspath) or "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
