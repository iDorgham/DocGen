"""
CLI interface tests for DocGen CLI.

Tests the command-line interface, argument parsing, and user interaction.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from src.cli_main import main as cli


class TestCLIInterface:
    """Test cases for CLI interface."""
    
    def test_cli_main_help(self, cli_runner: CliRunner):
        """Test main CLI help command."""
        result = cli_runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "DocGen CLI" in result.output
        assert "Commands:" in result.output
        assert "generate" in result.output
        assert "project" in result.output
        assert "validate" in result.output
    
    def test_cli_version(self, cli_runner: CliRunner):
        """Test CLI version command."""
        result = cli_runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert "version" in result.output.lower()
    
    def test_cli_no_arguments(self, cli_runner: CliRunner):
        """Test CLI with no arguments shows help."""
        result = cli_runner.invoke(cli, [])
        
        assert result.exit_code == 0
        assert "DocGen CLI" in result.output
        assert "Commands:" in result.output
    
    def test_cli_invalid_command(self, cli_runner: CliRunner):
        """Test CLI with invalid command."""
        result = cli_runner.invoke(cli, ['invalid-command'])
        
        assert result.exit_code != 0
        assert "No such command" in result.output or "Usage:" in result.output
    
    def test_cli_invalid_option(self, cli_runner: CliRunner):
        """Test CLI with invalid option."""
        result = cli_runner.invoke(cli, ['--invalid-option'])
        
        assert result.exit_code != 0
        assert "No such option" in result.output or "Usage:" in result.output


class TestGenerateCommandInterface:
    """Test cases for generate command interface."""
    
    def test_generate_command_help(self, cli_runner: CliRunner):
        """Test generate command help."""
        result = cli_runner.invoke(cli, ['generate', '--help'])
        
        assert result.exit_code == 0
        assert "Generate" in result.output
        assert "--project" in result.output
        assert "--template" in result.output
        assert "--output" in result.output
    
    def test_generate_command_required_arguments(self, cli_runner: CliRunner):
        """Test generate command with missing required arguments."""
        result = cli_runner.invoke(cli, ['generate'])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_generate_command_missing_project(self, cli_runner: CliRunner, temp_dir: Path):
        """Test generate command with missing project argument."""
        template_path = temp_dir / "template.j2"
        template_path.write_text("{{ project.name }}")
        output_path = temp_dir / "output.md"
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_generate_command_missing_template(self, cli_runner: CliRunner, temp_dir: Path):
        """Test generate command with missing template argument."""
        project_path = temp_dir / "project.yaml"
        project_path.write_text("name: Test\ndescription: Test project")
        output_path = temp_dir / "output.md"
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--output', str(output_path)
        ])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_generate_command_missing_output(self, cli_runner: CliRunner, temp_dir: Path):
        """Test generate command with missing output argument."""
        project_path = temp_dir / "project.yaml"
        project_path.write_text("name: Test\ndescription: Test project")
        template_path = temp_dir / "template.j2"
        template_path.write_text("{{ project.name }}")
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path)
        ])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_generate_command_invalid_file_paths(self, cli_runner: CliRunner):
        """Test generate command with invalid file paths."""
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', '/invalid/path/project.yaml',
            '--template', '/invalid/path/template.j2',
            '--output', '/invalid/path/output.md'
        ])
        
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()


class TestProjectCommandInterface:
    """Test cases for project command interface."""
    
    def test_project_command_help(self, cli_runner: CliRunner):
        """Test project command help."""
        result = cli_runner.invoke(cli, ['project', '--help'])
        
        assert result.exit_code == 0
        assert "Project" in result.output
        assert "create" in result.output
        assert "validate" in result.output
    
    def test_project_create_command_help(self, cli_runner: CliRunner):
        """Test project create command help."""
        result = cli_runner.invoke(cli, ['project', 'create', '--help'])
        
        assert result.exit_code == 0
        assert "Create" in result.output
        assert "--name" in result.output
        assert "--description" in result.output
        assert "--output" in result.output
    
    def test_project_validate_command_help(self, cli_runner: CliRunner):
        """Test project validate command help."""
        result = cli_runner.invoke(cli, ['project', 'validate', '--help'])
        
        assert result.exit_code == 0
        assert "Validate" in result.output
        assert "--project" in result.output
    
    def test_project_create_required_arguments(self, cli_runner: CliRunner):
        """Test project create with missing required arguments."""
        result = cli_runner.invoke(cli, ['project', 'create'])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_project_create_missing_name(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project create with missing name."""
        output_path = temp_dir / "project.yaml"
        
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--description', 'Test project',
            '--output', str(output_path)
        ])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_project_create_missing_description(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project create with missing description."""
        output_path = temp_dir / "project.yaml"
        
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Test Project',
            '--output', str(output_path)
        ])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_project_validate_required_arguments(self, cli_runner: CliRunner):
        """Test project validate with missing required arguments."""
        result = cli_runner.invoke(cli, ['project', 'validate'])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()


class TestValidateCommandInterface:
    """Test cases for validate command interface."""
    
    def test_validate_command_help(self, cli_runner: CliRunner):
        """Test validate command help."""
        result = cli_runner.invoke(cli, ['validate', '--help'])
        
        assert result.exit_code == 0
        assert "Validate" in result.output
        assert "project" in result.output
        assert "template" in result.output
    
    def test_validate_project_command_help(self, cli_runner: CliRunner):
        """Test validate project command help."""
        result = cli_runner.invoke(cli, ['validate', 'project', '--help'])
        
        assert result.exit_code == 0
        assert "Validate" in result.output
        assert "--file" in result.output
    
    def test_validate_template_command_help(self, cli_runner: CliRunner):
        """Test validate template command help."""
        result = cli_runner.invoke(cli, ['validate', 'template', '--help'])
        
        assert result.exit_code == 0
        assert "Validate" in result.output
        assert "--file" in result.output
    
    def test_validate_project_required_arguments(self, cli_runner: CliRunner):
        """Test validate project with missing required arguments."""
        result = cli_runner.invoke(cli, ['validate', 'project'])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()
    
    def test_validate_template_required_arguments(self, cli_runner: CliRunner):
        """Test validate template with missing required arguments."""
        result = cli_runner.invoke(cli, ['validate', 'template'])
        
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()


class TestCLIErrorHandling:
    """Test cases for CLI error handling."""
    
    def test_cli_handles_file_not_found(self, cli_runner: CliRunner):
        """Test CLI handles file not found errors gracefully."""
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', 'non_existent.yaml',
            '--template', 'non_existent.j2',
            '--output', 'output.md'
        ])
        
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()
    
    def test_cli_handles_permission_errors(self, cli_runner: CliRunner, temp_dir: Path):
        """Test CLI handles permission errors gracefully."""
        # Create a read-only file
        read_only_file = temp_dir / "read_only.yaml"
        read_only_file.write_text("name: Test\ndescription: Test")
        read_only_file.chmod(0o444)  # Read-only
        
        try:
            result = cli_runner.invoke(cli, [
                'project', 'validate',
                '--project', str(read_only_file)
            ])
            
            # Should still work for read-only files
            assert result.exit_code == 0
        finally:
            # Restore permissions
            read_only_file.chmod(0o644)
    
    def test_cli_handles_invalid_yaml(self, cli_runner: CliRunner, temp_dir: Path):
        """Test CLI handles invalid YAML gracefully."""
        invalid_yaml = temp_dir / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")
        
        result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(invalid_yaml)
        ])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "error" in result.output.lower()
    
    def test_cli_handles_template_errors(self, cli_runner: CliRunner, temp_dir: Path):
        """Test CLI handles template errors gracefully."""
        # Create valid project
        project_path = temp_dir / "project.yaml"
        project_path.write_text("name: Test\ndescription: Test project")
        
        # Create invalid template
        invalid_template = temp_dir / "invalid.j2"
        invalid_template.write_text("{{ project.name }")  # Missing closing brace
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(invalid_template),
            '--output', str(temp_dir / "output.md")
        ])
        
        assert result.exit_code != 0
        assert "error" in result.output.lower() or "invalid" in result.output.lower()
    
    def test_cli_provides_helpful_error_messages(self, cli_runner: CliRunner):
        """Test CLI provides helpful error messages."""
        result = cli_runner.invoke(cli, ['generate'])
        
        assert result.exit_code != 0
        # Should provide helpful information about required options
        assert "Missing option" in result.output or "required" in result.output.lower()
        assert "--project" in result.output or "--template" in result.output


class TestCLIInteractiveMode:
    """Test cases for CLI interactive mode."""
    
    def test_cli_interactive_project_creation(self, cli_runner: CliRunner, temp_dir: Path):
        """Test interactive project creation."""
        output_path = temp_dir / "interactive_project.yaml"
        
        # Simulate user input
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Interactive Project',
            '--description', 'A project created interactively',
            '--output', str(output_path)
        ], input='\n')  # Just press enter for any prompts
        
        assert result.exit_code == 0
        assert output_path.exists()
    
    def test_cli_handles_user_interruption(self, cli_runner: CliRunner):
        """Test CLI handles user interruption gracefully."""
        # This test simulates Ctrl+C interruption
        with patch('click.prompt', side_effect=KeyboardInterrupt):
            result = cli_runner.invoke(cli, ['project', 'create'])
            
            # Should handle interruption gracefully
            assert result.exit_code != 0
            assert "interrupted" in result.output.lower() or "cancelled" in result.output.lower()
