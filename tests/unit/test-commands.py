"""
Unit tests for CLI commands.

Tests the command-line interface and command handlers.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from src.cli.main import cli
from src.commands.generate import generate_command
from src.commands.project import project_command
from src.commands.validate import validate_command


class TestCLI:
    """Test cases for CLI interface."""
    
    def test_cli_help(self, cli_runner: CliRunner):
        """Test CLI help command."""
        result = cli_runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "DocGen CLI" in result.output
        assert "Commands:" in result.output
    
    def test_cli_version(self, cli_runner: CliRunner):
        """Test CLI version command."""
        result = cli_runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert "version" in result.output.lower()
    
    def test_cli_invalid_command(self, cli_runner: CliRunner):
        """Test CLI with invalid command."""
        result = cli_runner.invoke(cli, ['invalid-command'])
        
        assert result.exit_code != 0
        assert "No such command" in result.output or "Usage:" in result.output


class TestGenerateCommand:
    """Test cases for generate command."""
    
    def test_generate_command_help(self, cli_runner: CliRunner):
        """Test generate command help."""
        result = cli_runner.invoke(cli, ['generate', '--help'])
        
        assert result.exit_code == 0
        assert "Generate" in result.output
    
    def test_generate_command_success(self, cli_runner: CliRunner, sample_project_yaml: Path, test_templates_dir: Path, test_output_dir: Path):
        """Test successful document generation."""
        with patch('src.commands.generate.DocumentGenerator') as mock_generator:
            mock_generator.return_value.generate_document.return_value = "Generated content"
            
            result = cli_runner.invoke(cli, [
                'generate',
                '--project', str(sample_project_yaml),
                '--template', str(test_templates_dir / "project_plan.j2"),
                '--output', str(test_output_dir / "output.md")
            ])
            
            assert result.exit_code == 0
            assert "Generated" in result.output or "Success" in result.output
    
    def test_generate_command_missing_project(self, cli_runner: CliRunner, test_templates_dir: Path, test_output_dir: Path):
        """Test generate command with missing project file."""
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', 'non_existent.yaml',
            '--template', str(test_templates_dir / "project_plan.j2"),
            '--output', str(test_output_dir / "output.md")
        ])
        
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()
    
    def test_generate_command_missing_template(self, cli_runner: CliRunner, sample_project_yaml: Path, test_output_dir: Path):
        """Test generate command with missing template file."""
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(sample_project_yaml),
            '--template', 'non_existent.j2',
            '--output', str(test_output_dir / "output.md")
        ])
        
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()
    
    def test_generate_command_invalid_yaml(self, cli_runner: CliRunner, temp_dir: Path, test_templates_dir: Path, test_output_dir: Path):
        """Test generate command with invalid YAML file."""
        invalid_yaml = temp_dir / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(invalid_yaml),
            '--template', str(test_templates_dir / "project_plan.j2"),
            '--output', str(test_output_dir / "output.md")
        ])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "error" in result.output.lower()
    
    def test_generate_command_template_error(self, cli_runner: CliRunner, sample_project_yaml: Path, test_templates_dir: Path, test_output_dir: Path):
        """Test generate command with template rendering error."""
        with patch('src.commands.generate.DocumentGenerator') as mock_generator:
            mock_generator.return_value.generate_document.side_effect = Exception("Template error")
            
            result = cli_runner.invoke(cli, [
                'generate',
                '--project', str(sample_project_yaml),
                '--template', str(test_templates_dir / "project_plan.j2"),
                '--output', str(test_output_dir / "output.md")
            ])
            
            assert result.exit_code != 0
            assert "error" in result.output.lower()


class TestProjectCommand:
    """Test cases for project command."""
    
    def test_project_command_help(self, cli_runner: CliRunner):
        """Test project command help."""
        result = cli_runner.invoke(cli, ['project', '--help'])
        
        assert result.exit_code == 0
        assert "Project" in result.output
    
    def test_project_create_success(self, cli_runner: CliRunner, temp_dir: Path):
        """Test successful project creation."""
        project_path = temp_dir / "new_project.yaml"
        
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Test Project',
            '--description', 'A test project',
            '--output', str(project_path)
        ])
        
        assert result.exit_code == 0
        assert project_path.exists()
        assert "Test Project" in project_path.read_text()
    
    def test_project_create_missing_name(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project creation with missing name."""
        project_path = temp_dir / "new_project.yaml"
        
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--description', 'A test project',
            '--output', str(project_path)
        ])
        
        assert result.exit_code != 0
        assert "required" in result.output.lower() or "missing" in result.output.lower()
    
    def test_project_create_missing_description(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project creation with missing description."""
        project_path = temp_dir / "new_project.yaml"
        
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Test Project',
            '--output', str(project_path)
        ])
        
        assert result.exit_code != 0
        assert "required" in result.output.lower() or "missing" in result.output.lower()
    
    def test_project_validate_success(self, cli_runner: CliRunner, sample_project_yaml: Path):
        """Test successful project validation."""
        result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(sample_project_yaml)
        ])
        
        assert result.exit_code == 0
        assert "valid" in result.output.lower() or "success" in result.output.lower()
    
    def test_project_validate_invalid(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project validation with invalid project."""
        invalid_yaml = temp_dir / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")
        
        result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(invalid_yaml)
        ])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "error" in result.output.lower()
    
    def test_project_validate_missing_file(self, cli_runner: CliRunner):
        """Test project validation with missing file."""
        result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', 'non_existent.yaml'
        ])
        
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()


class TestValidateCommand:
    """Test cases for validate command."""
    
    def test_validate_command_help(self, cli_runner: CliRunner):
        """Test validate command help."""
        result = cli_runner.invoke(cli, ['validate', '--help'])
        
        assert result.exit_code == 0
        assert "Validate" in result.output
    
    def test_validate_project_success(self, cli_runner: CliRunner, sample_project_yaml: Path):
        """Test successful project validation."""
        result = cli_runner.invoke(cli, [
            'validate', 'project',
            '--file', str(sample_project_yaml)
        ])
        
        assert result.exit_code == 0
        assert "valid" in result.output.lower() or "success" in result.output.lower()
    
    def test_validate_template_success(self, cli_runner: CliRunner, test_templates_dir: Path):
        """Test successful template validation."""
        result = cli_runner.invoke(cli, [
            'validate', 'template',
            '--file', str(test_templates_dir / "project_plan.j2")
        ])
        
        assert result.exit_code == 0
        assert "valid" in result.output.lower() or "success" in result.output.lower()
    
    def test_validate_project_invalid(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project validation with invalid file."""
        invalid_yaml = temp_dir / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")
        
        result = cli_runner.invoke(cli, [
            'validate', 'project',
            '--file', str(invalid_yaml)
        ])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "error" in result.output.lower()
    
    def test_validate_template_invalid(self, cli_runner: CliRunner, temp_dir: Path):
        """Test template validation with invalid template."""
        invalid_template = temp_dir / "invalid.j2"
        invalid_template.write_text("{{ project.name }")  # Missing closing brace
        
        result = cli_runner.invoke(cli, [
            'validate', 'template',
            '--file', str(invalid_template)
        ])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "error" in result.output.lower()
    
    def test_validate_missing_file(self, cli_runner: CliRunner):
        """Test validation with missing file."""
        result = cli_runner.invoke(cli, [
            'validate', 'project',
            '--file', 'non_existent.yaml'
        ])
        
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()
