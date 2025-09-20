"""
Integration tests for complete workflows.

Tests end-to-end workflows including project creation, document generation, and validation.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from src.cli_main import main as cli


class TestCompleteWorkflows:
    """Test cases for complete user workflows."""
    
    def test_project_creation_to_document_generation_workflow(self, cli_runner: CliRunner, temp_dir: Path):
        """Test complete workflow from project creation to document generation."""
        # Step 1: Create a new project
        project_path = temp_dir / "test_project.yaml"
        
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Integration Test Project',
            '--description', 'A project for integration testing',
            '--version', '1.0.0',
            '--author', 'Test Author',
            '--email', 'test@example.com',
            '--output', str(project_path)
        ])
        
        assert create_result.exit_code == 0
        assert project_path.exists()
        
        # Step 2: Validate the created project
        validate_result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(project_path)
        ])
        
        assert validate_result.exit_code == 0
        
        # Step 3: Create a simple template
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "project_plan.j2"
        template_path.write_text("""
# {{ project.name }} Project Plan

## Description
{{ project.description }}

## Version
{{ project.version }}

## Author
{{ project.author }} <{{ project.email }}>

## Features
{% for feature in project.features %}
- {{ feature }}
{% endfor %}
""")
        
        # Step 4: Generate document from the project
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "project_plan.md"
        
        generate_result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        assert generate_result.exit_code == 0
        assert output_path.exists()
        
        # Step 5: Verify the generated content
        generated_content = output_path.read_text()
        assert "Integration Test Project" in generated_content
        assert "A project for integration testing" in generated_content
        assert "1.0.0" in generated_content
        assert "Test Author" in generated_content
        assert "test@example.com" in generated_content
    
    def test_multiple_document_generation_workflow(self, cli_runner: CliRunner, temp_dir: Path):
        """Test generating multiple documents from the same project."""
        # Create project with more data
        project_path = temp_dir / "multi_doc_project.yaml"
        
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Multi-Document Project',
            '--description', 'A project for multiple document generation',
            '--version', '2.0.0',
            '--author', 'Multi Author',
            '--email', 'multi@example.com',
            '--output', str(project_path)
        ])
        
        assert create_result.exit_code == 0
        
        # Create multiple templates
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        
        # Template 1: Project Plan
        plan_template = templates_dir / "project_plan.j2"
        plan_template.write_text("""
# {{ project.name }} Project Plan

## Overview
{{ project.description }}

## Version
{{ project.version }}

## Author
{{ project.author }} <{{ project.email }}>
""")
        
        # Template 2: Technical Specification
        tech_template = templates_dir / "technical_spec.j2"
        tech_template.write_text("""
# {{ project.name }} Technical Specification

## Project Information
- **Name**: {{ project.name }}
- **Version**: {{ project.version }}
- **Author**: {{ project.author }}

## Description
{{ project.description }}
""")
        
        # Generate multiple documents
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        # Generate project plan
        plan_output = output_dir / "project_plan.md"
        plan_result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(plan_template),
            '--output', str(plan_output)
        ])
        
        assert plan_result.exit_code == 0
        assert plan_output.exists()
        
        # Generate technical specification
        tech_output = output_dir / "technical_spec.md"
        tech_result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(tech_template),
            '--output', str(tech_output)
        ])
        
        assert tech_result.exit_code == 0
        assert tech_output.exists()
        
        # Verify both documents contain project information
        plan_content = plan_output.read_text()
        tech_content = tech_output.read_text()
        
        assert "Multi-Document Project" in plan_content
        assert "Multi-Document Project" in tech_content
        assert "2.0.0" in plan_content
        assert "2.0.0" in tech_content
    
    def test_error_recovery_workflow(self, cli_runner: CliRunner, temp_dir: Path):
        """Test error recovery in workflows."""
        # Create a project with invalid data
        invalid_project_path = temp_dir / "invalid_project.yaml"
        invalid_project_path.write_text("""
name: "Test Project"
description: "A test project"
email: "invalid-email"  # Invalid email format
""")
        
        # Try to validate the invalid project
        validate_result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(invalid_project_path)
        ])
        
        assert validate_result.exit_code != 0
        assert "invalid" in validate_result.output.lower() or "error" in validate_result.output.lower()
        
        # Fix the project data
        valid_project_path = temp_dir / "valid_project.yaml"
        valid_project_path.write_text("""
name: "Test Project"
description: "A test project"
email: "valid@example.com"
""")
        
        # Validate the fixed project
        validate_result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(valid_project_path)
        ])
        
        assert validate_result.exit_code == 0
        
        # Continue with document generation
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "test.j2"
        template_path.write_text("# {{ project.name }}\n\n{{ project.description }}")
        
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "test.md"
        
        generate_result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(valid_project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        assert generate_result.exit_code == 0
        assert output_path.exists()
    
    def test_template_validation_workflow(self, cli_runner: CliRunner, temp_dir: Path):
        """Test template validation workflow."""
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        
        # Create a template with syntax error
        invalid_template = templates_dir / "invalid.j2"
        invalid_template.write_text("{{ project.name }")  # Missing closing brace
        
        # Validate the invalid template
        validate_result = cli_runner.invoke(cli, [
            'validate', 'template',
            '--file', str(invalid_template)
        ])
        
        assert validate_result.exit_code != 0
        assert "invalid" in validate_result.output.lower() or "error" in validate_result.output.lower()
        
        # Fix the template
        valid_template = templates_dir / "valid.j2"
        valid_template.write_text("{{ project.name }}")
        
        # Validate the fixed template
        validate_result = cli_runner.invoke(cli, [
            'validate', 'template',
            '--file', str(valid_template)
        ])
        
        assert validate_result.exit_code == 0
    
    def test_batch_processing_workflow(self, cli_runner: CliRunner, temp_dir: Path):
        """Test batch processing of multiple projects."""
        # Create multiple projects
        projects_dir = temp_dir / "projects"
        projects_dir.mkdir()
        
        project1_path = projects_dir / "project1.yaml"
        project1_path.write_text("""
name: "Project 1"
description: "First project"
version: "1.0.0"
author: "Author 1"
email: "author1@example.com"
""")
        
        project2_path = projects_dir / "project2.yaml"
        project2_path.write_text("""
name: "Project 2"
description: "Second project"
version: "2.0.0"
author: "Author 2"
email: "author2@example.com"
""")
        
        # Create a template
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "batch.j2"
        template_path.write_text("# {{ project.name }}\n\n{{ project.description }}")
        
        # Generate documents for both projects
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        # Process project 1
        output1_path = output_dir / "project1.md"
        result1 = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project1_path),
            '--template', str(template_path),
            '--output', str(output1_path)
        ])
        
        assert result1.exit_code == 0
        assert output1_path.exists()
        
        # Process project 2
        output2_path = output_dir / "project2.md"
        result2 = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project2_path),
            '--template', str(template_path),
            '--output', str(output2_path)
        ])
        
        assert result2.exit_code == 0
        assert output2_path.exists()
        
        # Verify both documents
        content1 = output1_path.read_text()
        content2 = output2_path.read_text()
        
        assert "Project 1" in content1
        assert "First project" in content1
        assert "Project 2" in content2
        assert "Second project" in content2
    
    def test_file_system_operations_workflow(self, cli_runner: CliRunner, temp_dir: Path):
        """Test file system operations in workflows."""
        # Test creating nested directories
        nested_dir = temp_dir / "nested" / "deep" / "structure"
        nested_dir.mkdir(parents=True)
        
        # Create project in nested directory
        project_path = nested_dir / "nested_project.yaml"
        
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Nested Project',
            '--description', 'A project in nested directory',
            '--output', str(project_path)
        ])
        
        assert create_result.exit_code == 0
        assert project_path.exists()
        
        # Create template in nested directory
        template_path = nested_dir / "nested_template.j2"
        template_path.write_text("# {{ project.name }}\n\n{{ project.description }}")
        
        # Generate document in nested output directory
        output_dir = nested_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "nested_output.md"
        
        generate_result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        assert generate_result.exit_code == 0
        assert output_path.exists()
        
        # Verify the generated content
        content = output_path.read_text()
        assert "Nested Project" in content
        assert "A project in nested directory" in content
