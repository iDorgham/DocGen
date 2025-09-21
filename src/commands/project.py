"""
Project command for DocGen CLI.
"""

import click
from pathlib import Path
from src.models.project_model import Project
from src.core.validation import ProjectValidator
from src.utils.file_io import write_file
import yaml


@click.group()
def project_command():
    """Project management commands."""
    pass


@project_command.command()
@click.option('--name', '-n', required=True, help='Project name')
@click.option('--description', '-d', required=True, help='Project description')
@click.option('--version', '-v', default='1.0.0', help='Project version')
@click.option('--author', '-a', help='Project author')
@click.option('--email', '-e', help='Author email')
@click.option('--output', '-o', required=True, help='Output YAML file path')
def create(name: str, description: str, version: str, author: str, email: str, output: str):
    """Create a new project."""
    try:
        project_data = {
            "name": name,
            "description": description,
            "version": version
        }
        
        if author:
            project_data["author"] = author
        if email:
            project_data["email"] = email
        
        project = Project(**project_data)
        yaml_content = yaml.dump(project.model_dump(), default_flow_style=False)
        
        write_file(Path(output), yaml_content)
        click.echo(f"Project created successfully: {output}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@project_command.command()
@click.option('--project', '-p', required=True, help='Project YAML file path')
def validate(project: str):
    """Validate a project."""
    try:
        from src.utils.file_io import read_file
        project_data = yaml.safe_load(read_file(Path(project)))
        project_obj = Project(**project_data)
        
        validator = ProjectValidator()
        validator.validate_project(project_obj)
        
        click.echo("Project is valid")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()