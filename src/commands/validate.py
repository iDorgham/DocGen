"""
Validate command for DocGen CLI.
"""

import click
from pathlib import Path
from src.models.project_model import Project
from src.models.template_model import Template
from src.core.validation import ProjectValidator
from src.utils.file_io import read_file
from src.utils.validation import validate_yaml
import yaml


@click.group()
def validate_command():
    """Validation commands."""
    pass


@validate_command.command()
@click.option('--file', '-f', required=True, help='Project YAML file to validate')
def project(file: str):
    """Validate a project file."""
    try:
        if not Path(file).exists():
            click.echo(f"Error: File not found: {file}", err=True)
            raise click.Abort()
        
        content = read_file(Path(file))
        if not validate_yaml(content):
            click.echo("Error: Invalid YAML format", err=True)
            raise click.Abort()
        
        project_data = yaml.safe_load(content)
        project_obj = Project(**project_data)
        
        validator = ProjectValidator()
        validator.validate_project(project_obj)
        
        click.echo("Project is valid")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@validate_command.command()
@click.option('--file', '-f', required=True, help='Template file to validate')
def template(file: str):
    """Validate a template file."""
    try:
        if not Path(file).exists():
            click.echo(f"Error: File not found: {file}", err=True)
            raise click.Abort()
        
        content = read_file(Path(file))
        template_obj = Template(name="template", content=content)
        
        validator = ProjectValidator()
        validator.validate_template(template_obj)
        
        click.echo("Template is valid")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()