"""
Generate command for DocGen CLI.
"""

import click
from pathlib import Path
from src.core.generator import DocumentGenerator
from src.models.project_model import Project
from src.models.template_model import Template
from src.utils.file_io import read_file, write_file
import yaml


@click.command()
@click.option('--project', '-p', required=True, help='Project YAML file path')
@click.option('--template', '-t', required=True, help='Template file path')
@click.option('--output', '-o', required=True, help='Output file path')
def generate_command(project: str, template: str, output: str):
    """Generate a document from a project and template."""
    try:
        # Load project data
        project_data = yaml.safe_load(read_file(Path(project)))
        project_obj = Project(**project_data)
        
        # Load template
        template_content = read_file(Path(template))
        template_obj = Template(name="template", content=template_content)
        
        # Generate document
        generator = DocumentGenerator()
        content = generator.generate_document(project_obj, template_obj)
        
        # Save output
        write_file(Path(output), content)
        
        click.echo(f"Document generated successfully: {output}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()