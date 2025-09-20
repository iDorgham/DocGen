"""
Main CLI module for DocGen.

This module provides the command-line interface for the DocGen tool,
addressing the Interactive CLI Interface (P0) requirement.
"""

import click
import re
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

from src.core.project_manager import ProjectManager
from src.core.generator import DocumentGenerator
from src.core.validation import ProjectValidator, ValidationError
from src.utils.validation import InputValidator
from src.core.error_handler import handle_error, get_user_friendly_message
from src.core.cli_enhancements import EnhancedConsole, ProgressIndicator, HelpSystem
from src.core.guided_workflows import GuidedWorkflows
from src.core.documentation_system import DocumentationSystem
from src.core.testing_system import TestingSystem
from src.core.app_creation_guide import AppCreationGuide, DocGenError
from src.core.template_manager import TemplateManager, TemplateMetadata
from src.core.git_manager import GitManager, GitConfig, GitStatus

# Import MCP commands
from src.commands.mcp import mcp

# Import Spec commands
from src.commands.spec import spec

# Import Hooks commands
from src.commands.hooks import hooks

# Import Driven workflow commands
from src.commands.driven import driven


console = Console()

# Initialize enhanced systems
enhanced_console = EnhancedConsole()
progress = ProgressIndicator(enhanced_console)
help_system = HelpSystem(enhanced_console)
guided_workflows = GuidedWorkflows(enhanced_console)
documentation_system = DocumentationSystem(enhanced_console)
testing_system = TestingSystem(enhanced_console)
app_creation_guide = AppCreationGuide(enhanced_console)


@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    DocGen CLI - Generate project documentation from specifications.
    
    A powerful tool for creating technical specifications, project plans,
    and marketing materials from structured project data.
    """
    pass


# Export as 'cli' for backward compatibility with tests
cli = main


@main.command()
@click.option('--name', '-n', help='Project name')
@click.option('--path', '-p', type=click.Path(), help='Project directory path')
@click.option('--description', '-d', help='Project description')
@click.option('--skip-validation', is_flag=True, help='Skip input validation (not recommended)')
def create(name: str, path: str, description: str, skip_validation: bool):
    """
    Create a new DocGen project.
    
    This command sets up a new project with the necessary structure
    and configuration files. All inputs are validated for security and consistency.
    """
    project_manager = ProjectManager()
    validator = InputValidator()
    
    # Interactive prompts if not provided via options
    if not name:
        name = Prompt.ask("Enter project name")
    
    if not path:
        # Generate a safe default path based on the name
        safe_name = validator.sanitize_input(name).lower().replace(' ', '_')
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', safe_name)
        if not safe_name:
            safe_name = "project"
        default_path = Path.cwd() / safe_name
        path = Prompt.ask("Enter project directory path", default=str(default_path))
    
    if not description:
        description = Prompt.ask("Enter project description (optional)", default="")
    
    # Validate inputs
    if not skip_validation:
        console.print("[yellow]Validating inputs...[/yellow]")
        
        # Validate project name
        is_valid, error_msg = validator.validate_project_name(name)
        if not is_valid:
            console.print(f"[red]Error: {error_msg}[/red]")
            return
        
        # Validate project path
        is_valid, error_msg = validator.validate_project_path(path)
        if not is_valid:
            console.print(f"[red]Error: {error_msg}[/red]")
            return
        
        # Sanitize description
        description = validator.sanitize_input(description, max_length=500)
        
        console.print("[green]✓ Input validation passed[/green]")
    
    project_path = Path(path)
    
    # Check if directory already exists
    if project_path.exists() and any(project_path.iterdir()):
        if not Confirm.ask(f"Directory {project_path} already exists and is not empty. Continue?"):
            console.print("Project creation cancelled.")
            return
    
    try:
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create project configuration
        project_config = project_manager.create_project(name, project_path, description)
        
        # Create basic project structure
        _create_project_structure(project_path)
        
        # Create initial project data file
        _create_initial_project_data(project_path, project_config)
        
        console.print(Panel.fit(
            f"[green]✓ Project '{name}' created successfully![/green]\n\n"
            f"Project ID: {project_config['id']}\n"
            f"Path: {project_path}\n"
            f"Description: {description or 'None'}",
            title="Project Created",
            border_style="green"
        ))
        
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("1. Edit the project data in 'project_data.yaml'")
        console.print("2. Run 'docgen spec' to generate technical specification")
        console.print("3. Run 'docgen plan' to generate project plan")
        console.print("4. Run 'docgen marketing' to generate marketing materials")
        
    except Exception as e:
        # Use enhanced error handling
        if handle_error(e, {"command": "create", "project_name": name, "project_path": str(project_path)}):
            console.print("[green]Project creation recovered successfully![/green]")
        else:
            console.print(get_user_friendly_message(e))
        return


@main.command()
def recent():
    """
    Show recently accessed projects.
    
    Displays a list of recently created or accessed projects
    for quick access and project management.
    """
    project_manager = ProjectManager()
    recent_projects = project_manager.get_recent_projects()
    
    if not recent_projects:
        console.print("[yellow]No recent projects found.[/yellow]")
        console.print("Create a new project with: [blue]docgen create[/blue]")
        return
    
    table = Table(title="Recent Projects")
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="magenta")
    table.add_column("Last Accessed", style="green")
    table.add_column("Status", style="yellow")
    
    for project in recent_projects:
        status = "Current" if project_manager.get_current_project() and project_manager.get_current_project()["id"] == project["id"] else "Active"
        last_accessed = project["last_accessed"][:19].replace('T', ' ')
        
        table.add_row(
            project["name"],
            project["path"],
            last_accessed,
            status
        )
    
    console.print(table)
    
    console.print("\n[yellow]Commands:[/yellow]")
    console.print("• [blue]docgen switch[/blue] - Switch to a different project")
    console.print("• [blue]docgen status[/blue] - Show current project status")


@main.command()
@click.option('--project-id', help='Specific project ID to show status for')
def status(project_id: str):
    """
    Show current project status.
    
    Displays information about the current project or a specific project,
    including file status and generated documents.
    """
    project_manager = ProjectManager()
    
    if project_id:
        project = project_manager.get_project(project_id)
        if not project:
            console.print(f"[red]Project with ID '{project_id}' not found.[/red]")
            return
    else:
        project = project_manager.get_current_project()
        if not project:
            console.print("[yellow]No current project set.[/yellow]")
            console.print("Create a new project with: [blue]docgen create[/blue]")
            return
    
    status_info = project_manager.get_project_status(project["id"])
    
    # Create status panel
    status_text = f"""
[bold]Project:[/bold] {status_info['name']}
[bold]ID:[/bold] {status_info['project_id']}
[bold]Path:[/bold] {status_info['path']}
[bold]Created:[/bold] {status_info['created_at'][:19].replace('T', ' ')}
[bold]Last Accessed:[/bold] {status_info['last_accessed'][:19].replace('T', ' ')}
[bold]Directory Exists:[/bold] {'✓' if status_info['exists'] else '✗'}
[bold]Current Project:[/bold] {'✓' if status_info['is_current'] else '✗'}
"""
    
    if status_info['exists']:
        status_text += f"[bold]Has Docs:[/bold] {'✓' if status_info.get('has_docs') else '✗'}\n"
        
        if status_info.get('doc_files'):
            status_text += f"[bold]Generated Documents:[/bold] {len(status_info['doc_files'])}\n"
            for doc_file in status_info['doc_files'][:5]:  # Show first 5
                status_text += f"  • {doc_file.name}\n"
            if len(status_info['doc_files']) > 5:
                status_text += f"  • ... and {len(status_info['doc_files']) - 5} more\n"
    
    console.print(Panel.fit(
        status_text.strip(),
        title="Project Status",
        border_style="green" if status_info['exists'] else "red"
    ))
    
    if not status_info['exists']:
        console.print("\n[red]Warning:[/red] Project directory does not exist.")
        console.print("The project may have been moved or deleted.")


@main.command()
@click.option('--project-id', help='Project ID to switch to')
def switch(project_id: str):
    """
    Switch to a different project.
    
    Changes the current active project for document generation.
    If no project ID is provided, shows a list of available projects.
    """
    project_manager = ProjectManager()
    
    if not project_id:
        # Show available projects for selection
        projects = project_manager.get_all_projects()
        
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
            console.print("Create a new project with: [blue]docgen create[/blue]")
            return
        
        # Create selection table
        table = Table(title="Available Projects")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Path", style="magenta")
        table.add_column("Status", style="yellow")
        
        current_project = project_manager.get_current_project()
        current_id = current_project["id"] if current_project else None
        
        for project in projects.values():
            status = "Current" if project["id"] == current_id else "Active"
            table.add_row(
                project["id"],
                project["name"],
                project["path"],
                status
            )
        
        console.print(table)
        console.print("\n[yellow]Use --project-id to switch to a specific project.[/yellow]")
        console.print("Example: [blue]docgen switch --project-id project_name_1234567890[/blue]")
        return
    
    # Switch to specified project
    success = project_manager.set_current_project(project_id)
    
    if success:
        project = project_manager.get_project(project_id)
        console.print(Panel.fit(
            f"[green]✓ Switched to project '{project['name']}'[/green]\n\n"
            f"Project ID: {project['id']}\n"
            f"Path: {project['path']}",
            title="Project Switched",
            border_style="green"
        ))
    else:
        console.print(f"[red]Error: Project with ID '{project_id}' not found.[/red]")
        console.print("Use [blue]docgen recent[/blue] to see available projects.")


@main.command()
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['markdown', 'html', 'pdf'], case_sensitive=False),
              default='markdown', help='Output format for the document')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--validate-data', is_flag=True, help='Validate project data before generation')
@click.option('--auto-commit', is_flag=True, help='Automatically commit generated documents to Git')
def spec(output_format: str, output: str, validate_data: bool, auto_commit: bool):
    """
    Generate technical specification document.
    
    Creates a comprehensive technical specification document from project data
    using the technical_spec template.
    """
    project_manager = ProjectManager()
    current_project = project_manager.get_current_project()
    
    if not current_project:
        console.print("[red]Error: No current project set.[/red]")
        console.print("Create a new project with: [blue]docgen create[/blue]")
        console.print("Or switch to an existing project with: [blue]docgen switch[/blue]")
        return
    
    project_path = Path(current_project["path"])
    
    if not project_path.exists():
        console.print(f"[red]Error: Project directory does not exist: {project_path}[/red]")
        return
    
    try:
        # Initialize validator and generator
        validator = InputValidator()
        generator = DocumentGenerator()
        
        # Validate output format
        is_valid, error_msg = validator.validate_output_format(output_format)
        if not is_valid:
            console.print(f"[red]Error: {error_msg}[/red]")
            return
        
        # Validate output path if provided
        if output:
            is_valid, error_msg = validator.validate_output_path(output, output_format)
            if not is_valid:
                console.print(f"[red]Error: {error_msg}[/red]")
                return
        
        # Load and validate project data
        console.print("[yellow]Loading project data...[/yellow]")
        project_data = generator.load_project_data(project_path)
        
        if validate_data:
            console.print("[yellow]Validating project data...[/yellow]")
            is_valid, error_msg, warnings = validator.validate_project_data(project_data)
            
            if not is_valid:
                console.print(f"[red]Error: {error_msg}[/red]")
                return
            
            if warnings:
                console.print("[yellow]Data validation warnings:[/yellow]")
                for warning in warnings:
                    console.print(f"  • {warning}")
                
                if not Confirm.ask("Continue with warnings?"):
                    console.print("Document generation cancelled.")
                    return
        
        # Generate the document
        console.print(f"[yellow]Generating technical specification in {output_format} format...[/yellow]")
        
        content = generator.generate_document(
            "technical_spec",
            project_data,
            output_format
        )
        
        # Determine output path
        if output:
            output_path = Path(output)
        else:
            docs_dir = project_path / "docs"
            docs_dir.mkdir(exist_ok=True)
            output_path = docs_dir / f"technical_spec.{output_format}"
        
        # Save the document
        generator._save_document(content, output_path, output_format)
        
        console.print(Panel.fit(
            f"[green]✓ Technical specification generated successfully![/green]\n\n"
            f"Output: {output_path}\n"
            f"Format: {output_format}\n"
            f"Size: {len(content)} characters",
            title="Document Generated",
            border_style="green"
        ))
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Make sure your project has a 'project_data.yaml' file.")
    except Exception as e:
        console.print(f"[red]Error generating document: {e}[/red]")


@main.command()
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['markdown', 'html', 'pdf'], case_sensitive=False),
              default='markdown', help='Output format for the document')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def plan(output_format: str, output: str):
    """
    Generate project plan document.
    
    Creates a comprehensive project plan document from project data
    using the project_plan template.
    """
    project_manager = ProjectManager()
    current_project = project_manager.get_current_project()
    
    if not current_project:
        console.print("[red]Error: No current project set.[/red]")
        console.print("Create a new project with: [blue]docgen create[/blue]")
        console.print("Or switch to an existing project with: [blue]docgen switch[/blue]")
        return
    
    project_path = Path(current_project["path"])
    
    if not project_path.exists():
        console.print(f"[red]Error: Project directory does not exist: {project_path}[/red]")
        return
    
    try:
        # Initialize document generator
        generator = DocumentGenerator()
        
        # Generate the document
        console.print(f"[yellow]Generating project plan in {output_format} format...[/yellow]")
        
        content = generator.generate_document(
            "project_plan",
            generator.load_project_data(project_path),
            output_format
        )
        
        # Determine output path
        if output:
            output_path = Path(output)
        else:
            docs_dir = project_path / "docs"
            docs_dir.mkdir(exist_ok=True)
            output_path = docs_dir / f"project_plan.{output_format}"
        
        # Save the document
        generator._save_document(content, output_path, output_format)
        
        console.print(Panel.fit(
            f"[green]✓ Project plan generated successfully![/green]\n\n"
            f"Output: {output_path}\n"
            f"Format: {output_format}\n"
            f"Size: {len(content)} characters",
            title="Document Generated",
            border_style="green"
        ))
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Make sure your project has a 'project_data.yaml' file.")
    except Exception as e:
        console.print(f"[red]Error generating document: {e}[/red]")


@main.command()
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['markdown', 'html', 'pdf'], case_sensitive=False),
              default='markdown', help='Output format for the document')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def marketing(output_format: str, output: str):
    """
    Generate marketing materials document.
    
    Creates comprehensive marketing materials from project data
    using the marketing template.
    """
    project_manager = ProjectManager()
    current_project = project_manager.get_current_project()
    
    if not current_project:
        console.print("[red]Error: No current project set.[/red]")
        console.print("Create a new project with: [blue]docgen create[/blue]")
        console.print("Or switch to an existing project with: [blue]docgen switch[/blue]")
        return
    
    project_path = Path(current_project["path"])
    
    if not project_path.exists():
        console.print(f"[red]Error: Project directory does not exist: {project_path}[/red]")
        return
    
    try:
        # Initialize document generator
        generator = DocumentGenerator()
        
        # Generate the document
        console.print(f"[yellow]Generating marketing materials in {output_format} format...[/yellow]")
        
        content = generator.generate_document(
            "marketing",
            generator.load_project_data(project_path),
            output_format
        )
        
        # Determine output path
        if output:
            output_path = Path(output)
        else:
            docs_dir = project_path / "docs"
            docs_dir.mkdir(exist_ok=True)
            output_path = docs_dir / f"marketing.{output_format}"
        
        # Save the document
        generator._save_document(content, output_path, output_format)
        
        console.print(Panel.fit(
            f"[green]✓ Marketing materials generated successfully![/green]\n\n"
            f"Output: {output_path}\n"
            f"Format: {output_format}\n"
            f"Size: {len(content)} characters",
            title="Document Generated",
            border_style="green"
        ))
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Make sure your project has a 'project_data.yaml' file.")
    except Exception as e:
        console.print(f"[red]Error generating document: {e}[/red]")


@main.command()
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['markdown', 'html', 'pdf'], case_sensitive=False),
              default='markdown', help='Output format for all documents')
@click.option('--output-dir', '-d', type=click.Path(), help='Output directory for all documents')
def generate_all(output_format: str, output_dir: str):
    """
    Generate all available documents for the current project.
    
    Creates all document types (spec, plan, marketing) in the specified format.
    """
    project_manager = ProjectManager()
    current_project = project_manager.get_current_project()
    
    if not current_project:
        console.print("[red]Error: No current project set.[/red]")
        console.print("Create a new project with: [blue]docgen create[/blue]")
        console.print("Or switch to an existing project with: [blue]docgen switch[/blue]")
        return
    
    project_path = Path(current_project["path"])
    
    if not project_path.exists():
        console.print(f"[red]Error: Project directory does not exist: {project_path}[/red]")
        return
    
    try:
        # Initialize document generator
        generator = DocumentGenerator()
        
        # Determine output directory
        if output_dir:
            output_dir_path = Path(output_dir)
        else:
            output_dir_path = project_path / "docs"
        
        # Generate all documents
        console.print(f"[yellow]Generating all documents in {output_format} format...[/yellow]")
        
        generated_docs = generator.generate_all_documents(
            project_path,
            output_format,
            output_dir_path
        )
        
        if generated_docs:
            table = Table(title="Generated Documents")
            table.add_column("Document", style="cyan")
            table.add_column("Size", style="green")
            table.add_column("Output", style="magenta")
            
            for doc_name, content in generated_docs.items():
                output_file = output_dir_path / f"{doc_name}.{output_format}"
                table.add_row(
                    doc_name.replace('_', ' ').title(),
                    f"{len(content)} chars",
                    str(output_file)
                )
            
            console.print(table)
            
            console.print(Panel.fit(
                f"[green]✓ Generated {len(generated_docs)} documents successfully![/green]\n\n"
                f"Output Directory: {output_dir_path}\n"
                f"Format: {output_format}",
                title="All Documents Generated",
                border_style="green"
            ))
        else:
            console.print("[yellow]No documents were generated. Check your templates and project data.[/yellow]")
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Make sure your project has a 'project_data.yaml' file.")
    except Exception as e:
        console.print(f"[red]Error generating documents: {e}[/red]")


@main.command()
@click.option('--project-id', help='Specific project ID to validate')
@click.option('--fix-issues', is_flag=True, help='Attempt to fix common validation issues')
def validate(project_id: str, fix_issues: bool):
    """
    Validate project data and configuration.
    
    Performs comprehensive validation of project data, templates, and configuration
    to ensure data integrity and consistency.
    """
    project_manager = ProjectManager()
    validator = InputValidator()
    
    if project_id:
        project = project_manager.get_project(project_id)
        if not project:
            console.print(f"[red]Error: Project with ID '{project_id}' not found.[/red]")
            return
    else:
        project = project_manager.get_current_project()
        if not project:
            console.print("[red]Error: No current project set.[/red]")
            console.print("Create a new project with: [blue]docgen create[/blue]")
            console.print("Or switch to an existing project with: [blue]docgen switch[/blue]")
            return
    
    project_path = Path(project["path"])
    
    if not project_path.exists():
        console.print(f"[red]Error: Project directory does not exist: {project_path}[/red]")
        return
    
    console.print(f"[yellow]Validating project: {project['name']}[/yellow]")
    console.print(f"Path: {project_path}")
    
    validation_results = {
        "project_data": {"valid": False, "errors": [], "warnings": []},
        "templates": {"valid": False, "errors": [], "warnings": []},
        "structure": {"valid": False, "errors": [], "warnings": []}
    }
    
    # Validate project data file
    console.print("\n[yellow]Validating project data...[/yellow]")
    data_file = project_path / "project_data.yaml"
    
    is_valid, error_msg, data = validator.validate_yaml_file(data_file)
    if not is_valid:
        validation_results["project_data"]["errors"].append(error_msg)
    else:
        is_valid, error_msg, warnings = validator.validate_project_data(data)
        if not is_valid:
            validation_results["project_data"]["errors"].append(error_msg)
        else:
            validation_results["project_data"]["valid"] = True
            validation_results["project_data"]["warnings"] = warnings
    
    # Validate templates
    console.print("[yellow]Validating templates...[/yellow]")
    templates_dir = Path(__file__).parent.parent / "src" / "templates"
    template_files = list(templates_dir.glob("*.j2"))
    
    if not template_files:
        validation_results["templates"]["errors"].append("No template files found")
    else:
        all_templates_valid = True
        for template_file in template_files:
            is_valid, error_msg = validator.validate_template_file(template_file)
            if not is_valid:
                validation_results["templates"]["errors"].append(f"{template_file.name}: {error_msg}")
                all_templates_valid = False
        
        if all_templates_valid:
            validation_results["templates"]["valid"] = True
            validation_results["templates"]["warnings"].append(f"Found {len(template_files)} valid templates")
    
    # Validate project structure
    console.print("[yellow]Validating project structure...[/yellow]")
    required_dirs = ["docs", "templates", "data"]
    required_files = ["project_data.yaml"]
    
    structure_valid = True
    
    for dir_name in required_dirs:
        dir_path = project_path / dir_name
        if not dir_path.exists():
            validation_results["structure"]["warnings"].append(f"Directory '{dir_name}' does not exist")
        elif not dir_path.is_dir():
            validation_results["structure"]["errors"].append(f"'{dir_name}' exists but is not a directory")
            structure_valid = False
    
    for file_name in required_files:
        file_path = project_path / file_name
        if not file_path.exists():
            validation_results["structure"]["errors"].append(f"Required file '{file_name}' not found")
            structure_valid = False
        elif not file_path.is_file():
            validation_results["structure"]["errors"].append(f"'{file_name}' exists but is not a file")
            structure_valid = False
    
    if structure_valid and not validation_results["structure"]["errors"]:
        validation_results["structure"]["valid"] = True
    
    # Display results
    console.print("\n" + "="*60)
    console.print("[bold]VALIDATION RESULTS[/bold]")
    console.print("="*60)
    
    for category, results in validation_results.items():
        status = "✓ VALID" if results["valid"] else "✗ INVALID"
        color = "green" if results["valid"] else "red"
        
        console.print(f"\n[bold]{category.replace('_', ' ').title()}:[/bold] [{color}]{status}[/{color}]")
        
        if results["errors"]:
            console.print("  [red]Errors:[/red]")
            for error in results["errors"]:
                console.print(f"    • {error}")
        
        if results["warnings"]:
            console.print("  [yellow]Warnings:[/yellow]")
            for warning in results["warnings"]:
                console.print(f"    • {warning}")
    
    # Overall status
    all_valid = all(results["valid"] for results in validation_results.values())
    total_errors = sum(len(results["errors"]) for results in validation_results.values())
    total_warnings = sum(len(results["warnings"]) for results in validation_results.values())
    
    console.print(f"\n[bold]SUMMARY:[/bold]")
    console.print(f"  Total Errors: {total_errors}")
    console.print(f"  Total Warnings: {total_warnings}")
    
    if all_valid:
        console.print(Panel.fit(
            "[green]✓ All validations passed! Project is ready for document generation.[/green]",
            title="Validation Complete",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            f"[red]✗ Validation failed with {total_errors} errors.[/red]\n"
            f"Please fix the errors before generating documents.",
            title="Validation Failed",
            border_style="red"
        ))
        
        if fix_issues:
            console.print("\n[yellow]Attempting to fix common issues...[/yellow]")
            _attempt_fixes(project_path, validation_results)


def _attempt_fixes(project_path: Path, validation_results: dict) -> None:
    """Attempt to fix common validation issues."""
    fixes_applied = []
    
    # Fix missing directories
    required_dirs = ["docs", "templates", "data"]
    for dir_name in required_dirs:
        dir_path = project_path / dir_name
        if not dir_path.exists():
            try:
                dir_path.mkdir(exist_ok=True)
                fixes_applied.append(f"Created directory: {dir_name}")
            except Exception as e:
                console.print(f"[red]Failed to create directory {dir_name}: {e}[/red]")
    
    # Fix missing project data file
    data_file = project_path / "project_data.yaml"
    if not data_file.exists():
        try:
            # Create a minimal project data file
            from cli.main import _create_initial_project_data
            project_config = {
                "name": project_path.name,
                "description": "Auto-generated project",
                "created_at": datetime.now().isoformat()
            }
            _create_initial_project_data(project_path, project_config)
            fixes_applied.append("Created project_data.yaml with default content")
        except Exception as e:
            console.print(f"[red]Failed to create project data file: {e}[/red]")
    
    if fixes_applied:
        console.print("[green]Fixes applied:[/green]")
        for fix in fixes_applied:
            console.print(f"  • {fix}")
        console.print("\n[yellow]Please run validation again to check if issues are resolved.[/yellow]")
    else:
        console.print("[yellow]No automatic fixes could be applied.[/yellow]")


@main.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for error report')
def error_report(output: str):
    """
    Generate an error report for troubleshooting.
    
    Creates a detailed report of all errors encountered during the session,
    useful for debugging and support purposes.
    """
    from src.core.error_handler import error_handler
    
    summary = error_handler.get_error_summary()
    
    if summary["total_errors"] == 0:
        console.print(Panel.fit(
            "[green]✓ No errors encountered in this session![/green]",
            title="Error Report",
            border_style="green"
        ))
        return
    
    # Display summary
    console.print(Panel.fit(
        f"[yellow]Error Summary[/yellow]\n\n"
        f"Total Errors: {summary['total_errors']}\n"
        f"Categories: {', '.join(f'{k}: {v}' for k, v in summary['categories'].items())}\n"
        f"Severities: {', '.join(f'{k}: {v}' for k, v in summary['severities'].items())}",
        title="Error Report Summary",
        border_style="yellow"
    ))
    
    # Display recent errors
    if summary["recent_errors"]:
        console.print("\n[bold]Recent Errors:[/bold]")
        for i, error in enumerate(summary["recent_errors"], 1):
            console.print(f"\n{i}. [{error.severity.value.upper()}] {error.message}")
            if error.suggestions:
                console.print("   Suggestions:")
                for suggestion in error.suggestions:
                    console.print(f"     • {suggestion}")
    
    # Save report to file if requested
    if output:
        output_path = Path(output)
        error_handler.create_error_report(output_path)
        console.print(f"\n[green]Detailed error report saved to: {output_path}[/green]")
    else:
        console.print("\n[yellow]Use --output to save a detailed report to file.[/yellow]")


def _create_project_structure(project_path: Path) -> None:
    """Create the basic project directory structure."""
    # Create directories
    (project_path / "docs").mkdir(exist_ok=True)
    (project_path / "templates").mkdir(exist_ok=True)
    (project_path / "data").mkdir(exist_ok=True)


def _create_initial_project_data(project_path: Path, project_config: dict) -> None:
    """Create initial project data file."""
    project_data = {
        "project": {
            "name": project_config["name"],
            "description": project_config["description"],
            "version": "1.0.0",
            "created_at": project_config["created_at"],
            "goals": [
                "Deliver a high-quality product that meets user needs",
                "Ensure scalability and maintainability",
                "Provide excellent user experience"
            ],
            "objectives": [
                "Complete development within timeline",
                "Achieve target performance metrics",
                "Ensure security and compliance"
            ],
            "success_criteria": [
                "All functional requirements implemented",
                "Performance targets met",
                "User acceptance testing passed"
            ]
        },
        "team": {
            "lead": "Project Manager",
            "members": [
                {
                    "name": "Lead Developer",
                    "role": "Technical Lead",
                    "responsibilities": ["Architecture", "Code Review", "Technical Decisions"]
                },
                {
                    "name": "Frontend Developer",
                    "role": "UI/UX Developer",
                    "responsibilities": ["User Interface", "User Experience", "Frontend Development"]
                },
                {
                    "name": "Backend Developer",
                    "role": "Backend Developer",
                    "responsibilities": ["API Development", "Database Design", "Server Logic"]
                }
            ],
            "communication_plan": [
                {
                    "type": "Daily Standup",
                    "description": "Daily progress updates and blockers",
                    "frequency": "Daily at 9:00 AM"
                },
                {
                    "type": "Weekly Review",
                    "description": "Weekly progress review and planning",
                    "frequency": "Weekly on Fridays"
                }
            ]
        },
        "requirements": {
            "functional": [
                {
                    "id": "FR-001",
                    "title": "User Authentication",
                    "description": "Users must be able to register and login to the system",
                    "priority": "High",
                    "acceptance_criteria": [
                        "Users can register with email and password",
                        "Users can login with valid credentials",
                        "Password reset functionality works"
                    ],
                    "dependencies": []
                },
                {
                    "id": "FR-002",
                    "title": "Data Management",
                    "description": "Users can create, read, update, and delete their data",
                    "priority": "High",
                    "acceptance_criteria": [
                        "CRUD operations work correctly",
                        "Data validation is enforced",
                        "Data persistence is reliable"
                    ],
                    "dependencies": ["FR-001"]
                }
            ],
            "non_functional": {
                "performance": [
                    {"metric": "Response Time", "value": "200", "unit": "ms"},
                    {"metric": "Throughput", "value": "1000", "unit": "requests/second"}
                ],
                "security": [
                    "All data must be encrypted in transit",
                    "User passwords must be hashed",
                    "API endpoints must be authenticated"
                ],
                "scalability": [
                    "System must handle 10,000 concurrent users",
                    "Database must support horizontal scaling"
                ],
                "reliability": [
                    "99.9% uptime requirement",
                    "Automatic failover for critical components"
                ]
            },
            "user_stories": [
                {
                    "title": "User Registration",
                    "as_a": "new user",
                    "i_want": "to create an account",
                    "so_that": "I can access the system",
                    "acceptance_criteria": [
                        "I can enter my email and password",
                        "I receive a confirmation email",
                        "I can login after registration"
                    ]
                }
            ]
        },
        "timeline": {
            "phases": [
                {
                    "number": 1,
                    "name": "Planning & Setup",
                    "duration": "2 weeks",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-14",
                    "description": "Project setup, requirements gathering, and initial planning",
                    "deliverables": [
                        "Project charter",
                        "Requirements document",
                        "Technical architecture"
                    ],
                    "activities": [
                        "Stakeholder meetings",
                        "Requirements analysis",
                        "Technology selection"
                    ]
                },
                {
                    "number": 2,
                    "name": "Development",
                    "duration": "8 weeks",
                    "start_date": "2024-01-15",
                    "end_date": "2024-03-11",
                    "description": "Core development and implementation",
                    "deliverables": [
                        "MVP application",
                        "Unit tests",
                        "Integration tests"
                    ],
                    "activities": [
                        "Backend development",
                        "Frontend development",
                        "API integration"
                    ]
                }
            ],
            "milestones": [
                {
                    "name": "Requirements Complete",
                    "date": "2024-01-14",
                    "description": "All requirements documented and approved",
                    "success_criteria": "Stakeholder sign-off on requirements",
                    "dependencies": []
                },
                {
                    "name": "MVP Ready",
                    "date": "2024-03-11",
                    "description": "Minimum viable product ready for testing",
                    "success_criteria": "All core features implemented and tested",
                    "dependencies": ["Requirements Complete"]
                }
            ]
        },
        "marketing": {
            "target_audience": {
                "primary": "Small to medium businesses",
                "secondary": "Individual professionals",
                "demographics": [
                    {"category": "Age", "description": "25-45 years old"},
                    {"category": "Industry", "description": "Technology, Finance, Healthcare"}
                ],
                "psychographics": [
                    {"category": "Values", "description": "Efficiency, Innovation, Reliability"},
                    {"category": "Behavior", "description": "Tech-savvy, early adopters"}
                ]
            },
            "value_proposition": "Streamline your workflow with our intuitive and powerful solution that saves time and increases productivity.",
            "key_benefits": [
                {
                    "title": "Time Savings",
                    "description": "Reduce manual work by 50% with automated processes"
                },
                {
                    "title": "Easy Integration",
                    "description": "Seamlessly integrate with your existing tools and workflows"
                },
                {
                    "title": "Scalable Solution",
                    "description": "Grows with your business from startup to enterprise"
                }
            ],
            "key_features": [
                {
                    "name": "Dashboard",
                    "description": "Comprehensive overview of all your data and metrics",
                    "benefit": "Quick insights and decision making",
                    "target_user": "Managers and executives"
                },
                {
                    "name": "Automation",
                    "description": "Automate repetitive tasks and workflows",
                    "benefit": "Increased efficiency and reduced errors",
                    "target_user": "Operations teams"
                }
            ]
        },
        "technical": {
            "architecture": {
                "overview": "Microservices-based architecture with RESTful APIs and modern frontend framework"
            },
            "technology_stack": {
                "backend": ["Python", "FastAPI", "PostgreSQL", "Redis"],
                "frontend": ["React", "TypeScript", "Tailwind CSS"],
                "infrastructure": ["Docker", "AWS", "Kubernetes"]
            },
            "components": [
                {
                    "name": "API Gateway",
                    "description": "Entry point for all client requests",
                    "responsibilities": "Authentication, routing, rate limiting",
                    "interfaces": ["REST API", "WebSocket"]
                },
                {
                    "name": "User Service",
                    "description": "Handles user management and authentication",
                    "responsibilities": "User registration, login, profile management",
                    "interfaces": ["REST API", "Database"]
                }
            ]
        },
        "data_model": {
            "entities": [
                {
                    "name": "User",
                    "description": "Represents a system user",
                    "attributes": [
                        {"name": "id", "type": "UUID", "description": "Unique identifier"},
                        {"name": "email", "type": "String", "description": "User email address"},
                        {"name": "created_at", "type": "DateTime", "description": "Account creation timestamp"}
                    ],
                    "relationships": ["Has many Projects", "Belongs to Organization"]
                }
            ]
        },
        "development": {
            "coding_standards": [
                "Follow PEP 8 for Python code",
                "Use type hints for all functions",
                "Write comprehensive docstrings",
                "Maintain 80% test coverage"
            ],
            "testing_strategy": "Test-driven development with unit, integration, and end-to-end tests",
            "deployment_process": "Automated CI/CD pipeline with staging and production environments"
        },
        "risks": {
            "technical": [
                {
                    "title": "Third-party API Dependencies",
                    "description": "Reliance on external APIs that may change or become unavailable",
                    "impact": "High",
                    "probability": "Medium",
                    "mitigation": "Implement fallback mechanisms and API versioning"
                }
            ],
            "business": [
                {
                    "title": "Market Competition",
                    "description": "Competitors may release similar features",
                    "impact": "Medium",
                    "probability": "High",
                    "mitigation": "Focus on unique value proposition and rapid iteration"
                }
            ]
        },
        "glossary": {
            "API": "Application Programming Interface - a set of protocols for building software applications",
            "MVP": "Minimum Viable Product - the simplest version of a product that can be released",
            "CI/CD": "Continuous Integration/Continuous Deployment - automated software development practices"
        },
        "references": [
            "Project Charter v1.0",
            "Technical Architecture Document",
            "Market Research Report 2024"
        ]
    }
    
    import yaml
    with open(project_path / "project_data.yaml", 'w') as f:
        yaml.dump(project_data, f, default_flow_style=False, indent=2)


# Add MCP commands to main CLI
main.add_command(mcp)

# Add Spec commands to main CLI
main.add_command(spec)

# Add Hooks commands to main CLI
main.add_command(hooks)

# Add Driven workflow commands to main CLI
main.add_command(driven)

@main.group()
def template():
    """Template management commands."""
    pass


@template.command()
@click.option('--type', help='Filter by template type (spec, plan, marketing, custom)')
@click.option('--sort', type=click.Choice(['name', 'date', 'version']), default='name', help='Sort templates by field')
@click.option('--outdated', is_flag=True, help='Show only outdated templates')
def list(type: str, sort: str, outdated: bool):
    """
    List all available templates.
    
    Shows both built-in and custom templates with their metadata.
    """
    try:
        template_manager = TemplateManager()
        templates = template_manager.discover_templates()
        
        if not templates:
            console.print("[yellow]No templates found.[/yellow]")
            return
        
        # Filter templates
        if type:
            templates = {tid: meta for tid, meta in templates.items() 
                        if meta.template_type == type}
        
        if outdated:
            # Filter for outdated templates (simplified check)
            templates = {tid: meta for tid, meta in templates.items() 
                        if meta.version == "1.0.0"}  # Simplified outdated check
        
        if not templates:
            console.print(f"[yellow]No templates found matching criteria.[/yellow]")
            return
        
        # Sort templates
        if sort == 'name':
            sorted_templates = sorted(templates.items(), key=lambda x: x[1].name)
        elif sort == 'date':
            sorted_templates = sorted(templates.items(), key=lambda x: x[1].last_modified, reverse=True)
        elif sort == 'version':
            sorted_templates = sorted(templates.items(), key=lambda x: x[1].version, reverse=True)
        
        # Create table
        table = Table(title="Available Templates")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="blue")
        table.add_column("Version", style="yellow")
        table.add_column("Author", style="magenta")
        table.add_column("Source", style="dim")
        
        for template_id, metadata in sorted_templates:
            table.add_row(
                template_id,
                metadata.name,
                metadata.template_type,
                metadata.version,
                metadata.author,
                metadata.source
            )
        
        console.print(table)
        
        # Show summary
        console.print(f"\n[green]Found {len(templates)} template(s)[/green]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@template.command()
@click.argument('source')
@click.option('--name', help='Custom template name')
@click.option('--force', is_flag=True, help='Overwrite existing template')
def install(source: str, name: str, force: bool):
    """
    Install a template from various sources.
    
    SOURCE can be:
    - Local file path (.j2 or .zip)
    - Local directory path
    - URL to template package
    """
    try:
        template_manager = TemplateManager()
        
        # Check if template already exists
        if name and not force:
            existing = template_manager.get_template(name)
            if existing:
                if not Confirm.ask(f"Template '{name}' already exists. Overwrite?"):
                    console.print("[yellow]Installation cancelled.[/yellow]")
                    return
        
        console.print(f"[blue]Installing template from: {source}[/blue]")
        
        template_id = template_manager.install_template(source, name)
        
        console.print(f"[green]✓ Template installed successfully: {template_id}[/green]")
        
        # Show template info
        metadata = template_manager.get_template(template_id)
        if metadata:
            info_panel = Panel(
                f"[bold]Name:[/bold] {metadata.name}\n"
                f"[bold]Description:[/bold] {metadata.description}\n"
                f"[bold]Version:[/bold] {metadata.version}\n"
                f"[bold]Type:[/bold] {metadata.template_type}\n"
                f"[bold]Author:[/bold] {metadata.author}",
                title=f"Template: {template_id}",
                border_style="green"
            )
            console.print(info_panel)
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@template.command()
@click.option('--type', type=click.Choice(['spec', 'plan', 'marketing', 'custom']), help='Template type to create')
@click.option('--name', help='Template name')
def create(type: str, name: str):
    """
    Create a new template interactively.
    
    This command guides you through creating a custom template
    with proper metadata and structure.
    """
    try:
        template_manager = TemplateManager()
        
        # Get template name
        if not name:
            name = Prompt.ask("Template name")
        
        # Get template type
        if not type:
            type = Prompt.ask(
                "Template type",
                choices=['spec', 'plan', 'marketing', 'custom'],
                default='custom'
            )
        
        # Get other metadata
        description = Prompt.ask("Template description")
        author = Prompt.ask("Author name", default="Unknown")
        version = Prompt.ask("Version", default="1.0.0")
        
        # Create template directory
        template_id = name.lower().replace(' ', '-')
        template_dir = template_manager.custom_dir / template_id
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create basic template file
        template_file = template_dir / "template.j2"
        basic_template = f"""# {name}

## Overview
{description}

## Project Information
**Project Name:** {{{{ project.name }}}}
**Description:** {{{{ project.description }}}}

## Template Content
Add your template content here using Jinja2 syntax.

Available variables:
- project: Project information
- team: Team structure
- requirements: Project requirements
- timeline: Project timeline
- marketing: Marketing information

## Example Usage
```bash
docgen {type} --template {template_id}
```
"""
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(basic_template)
        
        # Create metadata
        from datetime import datetime
        metadata = TemplateMetadata(
            name=name,
            description=description,
            version=version,
            author=author,
            template_type=type,
            compatibility={},
            dependencies=[],
            tags=["custom", "created"],
            created=datetime.now().isoformat(),
            last_modified=datetime.now().isoformat(),
            source="local"
        )
        
        template_manager._save_template_metadata(template_dir, metadata)
        
        # Update registry
        template_manager.registry["templates"][template_id] = {
            "name": name,
            "description": description,
            "version": version,
            "author": author,
            "template_type": type,
            "compatibility": {},
            "dependencies": [],
            "tags": ["custom", "created"],
            "created": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "source": "local",
            "path": str(template_dir.relative_to(template_manager.templates_dir)),
            "installed": datetime.now().isoformat()
        }
        template_manager._save_template_registry()
        
        console.print(f"[green]✓ Template created successfully: {template_id}[/green]")
        console.print(f"[blue]Template location: {template_dir}[/blue]")
        console.print(f"[yellow]Edit the template file to customize: {template_file}[/yellow]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@template.command()
@click.argument('template_path')
def validate(template_path: str):
    """
    Validate a template for syntax and structure.
    
    TEMPLATE_PATH can be a file or directory path.
    """
    try:
        template_manager = TemplateManager()
        template_path_obj = Path(template_path)
        
        if not template_path_obj.exists():
            console.print(f"[red]Template path does not exist: {template_path}[/red]")
            return
        
        console.print(f"[blue]Validating template: {template_path}[/blue]")
        
        is_valid, errors = template_manager.validate_template(template_path_obj)
        
        if is_valid:
            console.print("[green]✓ Template validation passed[/green]")
            
            # Show template info if it's a directory
            if template_path_obj.is_dir():
                try:
                    metadata = template_manager._load_template_metadata(template_path_obj)
                    info_panel = Panel(
                        f"[bold]Name:[/bold] {metadata.name}\n"
                        f"[bold]Description:[/bold] {metadata.description}\n"
                        f"[bold]Version:[/bold] {metadata.version}\n"
                        f"[bold]Type:[/bold] {metadata.template_type}\n"
                        f"[bold]Author:[/bold] {metadata.author}",
                        title="Template Information",
                        border_style="green"
                    )
                    console.print(info_panel)
                except Exception as e:
                    console.print(f"[yellow]Could not load metadata: {e}[/yellow]")
        else:
            console.print("[red]✗ Template validation failed[/red]")
            for error in errors:
                console.print(f"[red]  • {error}[/red]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@main.group()
def git():
    """Git integration commands."""
    pass


@git.command()
@click.option('--initial-commit/--no-initial-commit', default=True, help='Create initial commit')
@click.option('--branch', default='main', help='Default branch name')
@click.option('--user-name', help='Git user name')
@click.option('--user-email', help='Git user email')
def init(initial_commit: bool, branch: str, user_name: str, user_email: str):
    """
    Initialize a Git repository for the current project.
    
    This command sets up Git version control for your DocGen project,
    including proper .gitignore configuration and optional initial commit.
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        
        # Create Git configuration
        git_config = GitConfig(
            auto_init=True,
            auto_commit=True,
            default_branch=branch,
            user_name=user_name,
            user_email=user_email
        )
        
        git_manager = GitManager(project_path, git_config)
        
        # Check if already a Git repository
        if git_manager.is_git_repository():
            console.print("[yellow]Project is already a Git repository.[/yellow]")
            
            # Show current status
            status = git_manager.get_status()
            if status.current_branch:
                console.print(f"[blue]Current branch: {status.current_branch}[/blue]")
            
            return
        
        console.print(f"[blue]Initializing Git repository in: {project_path}[/blue]")
        
        # Initialize repository
        success = git_manager.initialize_repository(initial_commit)
        
        if success:
            console.print("[green]✓ Git repository initialized successfully[/green]")
            
            # Show status
            status = git_manager.get_status()
            if status.current_branch:
                console.print(f"[blue]Default branch: {status.current_branch}[/blue]")
            
            if initial_commit:
                console.print("[green]✓ Initial commit created[/green]")
            
            # Show next steps
            next_steps = Panel(
                "[bold]Next steps:[/bold]\n"
                "• Add a remote repository: [cyan]docgen git remote add origin <url>[/cyan]\n"
                "• Commit generated documents: [cyan]docgen git commit[/cyan]\n"
                "• Push to remote: [cyan]docgen git push[/cyan]",
                title="Git Setup Complete",
                border_style="green"
            )
            console.print(next_steps)
        else:
            console.print("[red]✗ Failed to initialize Git repository[/red]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
@click.option('--message', '-m', help='Commit message')
@click.option('--files', help='Specific files to commit (comma-separated)')
@click.option('--auto', is_flag=True, help='Auto-generate commit message for document changes')
def commit(message: str, files: str, auto: bool):
    """
    Commit changes to the Git repository.
    
    This command commits changes to your Git repository. You can specify
    a custom message, specific files, or use auto-generated messages.
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Get current status
        status = git_manager.get_status()
        
        if not status.has_uncommitted_changes:
            console.print("[yellow]No changes to commit.[/yellow]")
            return
        
        # Show status
        if status.untracked_files:
            console.print(f"[blue]Untracked files: {len(status.untracked_files)}[/blue]")
        if status.modified_files:
            console.print(f"[blue]Modified files: {len(status.modified_files)}[/blue]")
        if status.staged_files:
            console.print(f"[blue]Staged files: {len(status.staged_files)}[/blue]")
        
        # Determine files to commit
        files_to_commit = None
        if files:
            files_to_commit = [f.strip() for f in files.split(',')]
        
        # Generate commit message
        if auto and not message:
            # Auto-generate message based on changes
            if status.modified_files:
                # Check if these are generated documents
                doc_files = [f for f in status.modified_files if f.endswith(('.md', '.html', '.pdf'))]
                if doc_files:
                    message = f"docs: update generated documents ({len(doc_files)} files)"
                else:
                    message = f"chore: update project files ({len(status.modified_files)} files)"
            elif status.untracked_files:
                doc_files = [f for f in status.untracked_files if f.endswith(('.md', '.html', '.pdf'))]
                if doc_files:
                    message = f"docs: add generated documents ({len(doc_files)} files)"
                else:
                    message = f"feat: add new files ({len(status.untracked_files)} files)"
            else:
                message = "chore: commit changes"
        
        if not message:
            message = Prompt.ask("Commit message")
        
        # Create commit
        success = git_manager.commit_changes(message, files_to_commit)
        
        if success:
            console.print(f"[green]✓ Changes committed successfully[/green]")
            console.print(f"[blue]Commit message: {message}[/blue]")
        else:
            console.print("[red]✗ Failed to commit changes[/red]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
def status():
    """
    Show Git repository status.
    
    Displays the current status of your Git repository including
    branch information, uncommitted changes, and file status.
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Get status
        status = git_manager.get_status()
        
        # Create status panel
        status_info = f"[bold]Repository:[/bold] {project_path}\n"
        status_info += f"[bold]Branch:[/bold] {status.current_branch or 'No branch'}\n"
        status_info += f"[bold]Remote:[/bold] {status.remote_url or 'No remote'}\n"
        status_info += f"[bold]Last commit:[/bold] {status.last_commit[:8] if status.last_commit else 'No commits'}\n"
        status_info += f"[bold]Working directory:[/bold] {'Clean' if not status.has_uncommitted_changes else 'Modified'}"
        
        status_panel = Panel(
            status_info,
            title="Git Repository Status",
            border_style="blue"
        )
        console.print(status_panel)
        
        # Show file changes
        if status.has_uncommitted_changes:
            if status.untracked_files:
                console.print(f"\n[green]Untracked files ({len(status.untracked_files)}):[/green]")
                for file in status.untracked_files[:10]:  # Show first 10
                    console.print(f"  [green]+[/green] {file}")
                if len(status.untracked_files) > 10:
                    console.print(f"  ... and {len(status.untracked_files) - 10} more")
            
            if status.modified_files:
                console.print(f"\n[yellow]Modified files ({len(status.modified_files)}):[/yellow]")
                for file in status.modified_files[:10]:  # Show first 10
                    console.print(f"  [yellow]M[/yellow] {file}")
                if len(status.modified_files) > 10:
                    console.print(f"  ... and {len(status.modified_files) - 10} more")
            
            if status.staged_files:
                console.print(f"\n[blue]Staged files ({len(status.staged_files)}):[/blue]")
                for file in status.staged_files[:10]:  # Show first 10
                    console.print(f"  [blue]A[/blue] {file}")
                if len(status.staged_files) > 10:
                    console.print(f"  ... and {len(status.staged_files) - 10} more")
        
        # Show recent commits
        commits = git_manager.get_commit_history(5)
        if commits:
            console.print(f"\n[bold]Recent commits:[/bold]")
            for commit in commits:
                console.print(f"  [dim]{commit['hash'][:8]}[/dim] {commit['message']} [dim]({commit['author']}, {commit['date']})[/dim]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
@click.option('--branch', help='Branch to push (defaults to current branch)')
@click.option('--set-upstream', is_flag=True, help='Set upstream branch')
def push(branch: str, set_upstream: bool):
    """
    Push changes to the remote repository.
    
    This command pushes your local commits to the remote repository.
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Get current status
        status = git_manager.get_status()
        
        if not status.remote_url:
            console.print("[red]No remote repository configured. Add a remote first.[/red]")
            console.print("[blue]Use: docgen git remote add origin <url>[/blue]")
            return
        
        # Determine branch
        if not branch:
            branch = status.current_branch
        
        if not branch:
            console.print("[red]No branch to push.[/red]")
            return
        
        console.print(f"[blue]Pushing to {status.remote_url} (branch: {branch})[/blue]")
        
        # Push changes
        success = git_manager.push_changes(branch)
        
        if success:
            console.print(f"[green]✓ Successfully pushed to {branch}[/green]")
        else:
            console.print("[red]✗ Failed to push changes[/red]")
            console.print("[yellow]Make sure you have push permissions and the remote exists.[/yellow]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
@click.argument('name')
@click.argument('url')
def remote(name: str, url: str):
    """
    Add or update a remote repository.
    
    NAME: Remote name (e.g., 'origin')
    URL: Remote repository URL
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Check if remote already exists
        remotes = git_manager.get_remotes()
        
        if name in remotes:
            # Update existing remote
            success = git_manager.set_remote_url(name, url)
            if success:
                console.print(f"[green]✓ Updated remote '{name}' to {url}[/green]")
            else:
                console.print(f"[red]✗ Failed to update remote '{name}'[/red]")
        else:
            # Add new remote
            success = git_manager.add_remote(name, url)
            if success:
                console.print(f"[green]✓ Added remote '{name}' ({url})[/green]")
            else:
                console.print(f"[red]✗ Failed to add remote '{name}'[/red]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
@click.argument('branch_name')
@click.option('--checkout/--no-checkout', default=True, help='Checkout the new branch')
def branch(branch_name: str, checkout: bool):
    """
    Create a new branch.
    
    BRANCH_NAME: Name of the new branch
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Create branch
        success = git_manager.create_branch(branch_name, checkout)
        
        if success:
            action = "Created and checked out" if checkout else "Created"
            console.print(f"[green]✓ {action} branch '{branch_name}'[/green]")
        else:
            console.print(f"[red]✗ Failed to create branch '{branch_name}'[/red]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
@click.argument('branch_name')
def checkout(branch_name: str):
    """
    Checkout an existing branch.
    
    BRANCH_NAME: Name of the branch to checkout
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Checkout branch
        success = git_manager.checkout_branch(branch_name)
        
        if success:
            console.print(f"[green]✓ Switched to branch '{branch_name}'[/green]")
        else:
            console.print(f"[red]✗ Failed to checkout branch '{branch_name}'[/red]")
            console.print("[yellow]Make sure the branch exists.[/yellow]")
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
def branches():
    """
    List all branches.
    
    Shows all local and remote branches in the repository.
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Get branches
        branches = git_manager.get_branches()
        
        if not branches:
            console.print("[yellow]No branches found.[/yellow]")
            return
        
        # Get current branch
        status = git_manager.get_status()
        current_branch = status.current_branch
        
        # Create table
        table = Table(title="Git Branches")
        table.add_column("Branch", style="cyan")
        table.add_column("Status", style="green")
        
        for branch in sorted(branches):
            status_text = "Current" if branch == current_branch else ""
            table.add_row(branch, status_text)
        
        console.print(table)
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


@git.command()
@click.option('--limit', default=10, help='Number of commits to show')
def log(limit: int):
    """
    Show commit history.
    
    Displays recent commits in the repository.
    """
    try:
        project_manager = ProjectManager()
        current_project = project_manager.get_current_project()
        
        if not current_project:
            console.print("[red]No current project found. Please create or switch to a project first.[/red]")
            return
        
        project_path = Path(current_project['path'])
        git_manager = GitManager(project_path)
        
        # Check if Git repository exists
        if not git_manager.is_git_repository():
            console.print("[red]Not a Git repository. Run 'docgen git init' first.[/red]")
            return
        
        # Get commit history
        commits = git_manager.get_commit_history(limit)
        
        if not commits:
            console.print("[yellow]No commits found.[/yellow]")
            return
        
        # Create table
        table = Table(title=f"Recent Commits (last {len(commits)})")
        table.add_column("Hash", style="dim", width=8)
        table.add_column("Message", style="white")
        table.add_column("Author", style="blue")
        table.add_column("Date", style="green")
        
        for commit in commits:
            table.add_row(
                commit['hash'][:8],
                commit['message'],
                commit['author'],
                commit['date']
            )
        
        console.print(table)
        
    except DocGenError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)


# Enhanced CLI Commands
@main.group()
def help_command():
    """Enhanced help and documentation commands."""
    pass


@help_command.command()
@click.argument('command', required=False)
def show(command: str):
    """Show enhanced help for commands."""
    if command:
        help_system.show_command_help(command)
    else:
        help_system.show_help()


@help_command.command()
def quick_start():
    """Show quick start guide."""
    documentation_system.show_quick_start()


@help_command.command()
def troubleshooting():
    """Show troubleshooting guide."""
    documentation_system.show_troubleshooting()


@main.group()
def examples():
    """Show examples and usage patterns."""
    pass


@examples.command()
@click.argument('command', required=False)
def show(command: str):
    """Show examples for commands."""
    documentation_system.show_examples(command)


@main.group()
def tutorial():
    """Interactive tutorials and learning guides."""
    pass


@tutorial.command()
@click.argument('topic', required=False)
def start(topic: str):
    """Start an interactive tutorial."""
    documentation_system.show_tutorial(topic)


@main.group()
def test():
    """Testing and validation commands."""
    pass


@test.command()
def run():
    """Run comprehensive test suite."""
    try:
        results = testing_system.run_comprehensive_tests()
        
        # Display summary
        summary = results['summary']
        console.print(f"\n[bold]Test Results Summary[/bold]")
        console.print(f"Total Tests: {summary['total_tests']}")
        console.print(f"Passed: {summary['passed']}")
        console.print(f"Failed: {summary['failed']}")
        console.print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        # Save report
        report_path = Path("test_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(results['report'])
        
        console.print(f"\n[green]Test report saved to: {report_path}[/green]")
        
    except Exception as e:
        handle_error(e)


@test.command()
@click.option('--category', type=click.Choice(['unit', 'integration', 'cli', 'template', 'validation', 'error', 'performance', 'security']), help='Test category to run')
def category(category: str):
    """Run specific test category."""
    try:
        if category == 'unit':
            results = testing_system._run_unit_tests()
        elif category == 'integration':
            results = testing_system._run_integration_tests()
        elif category == 'cli':
            results = testing_system._run_cli_tests()
        elif category == 'template':
            results = testing_system._run_template_tests()
        elif category == 'validation':
            results = testing_system._run_validation_tests()
        elif category == 'error':
            results = testing_system._run_error_handling_tests()
        elif category == 'performance':
            results = testing_system._run_performance_tests()
        elif category == 'security':
            results = testing_system._run_security_tests()
        
        console.print(f"\n[bold]{category.title()} Tests Results[/bold]")
        console.print(f"Passed: {results['passed']}")
        console.print(f"Failed: {results['failed']}")
        console.print(f"Total: {results['total']}")
        console.print(f"Success Rate: {(results['passed'] / results['total'] * 100):.1f}%")
        
    except Exception as e:
        handle_error(e)


@main.group()
def workflow():
    """Guided workflow commands."""
    pass


@workflow.command()
@click.argument('workflow_type', type=click.Choice(['create', 'generate', 'template', 'git', 'validate']))
def start(workflow_type: str):
    """Start a guided workflow."""
    try:
        if workflow_type == 'create':
            guided_workflows.create_project_workflow()
        elif workflow_type == 'generate':
            guided_workflows.generate_documents_workflow()
        elif workflow_type == 'template':
            guided_workflows.template_management_workflow()
        elif workflow_type == 'git':
            guided_workflows.git_integration_workflow()
        elif workflow_type == 'validate':
            guided_workflows.project_validation_workflow()
        
    except Exception as e:
        handle_error(e)


@workflow.command()
def list():
    """List available guided workflows."""
    guided_workflows.list_workflows()


# App & Website Creation Commands
@main.group()
def create_app():
    """App and website creation guidance commands."""
    pass


@create_app.command()
def start():
    """Start the interactive app/website creation guide."""
    try:
        app_creation_guide.start_creation_guide()
    except Exception as e:
        handle_error(e)


@create_app.command()
def templates():
    """Show available app and website templates."""
    try:
        choice = enhanced_console.prompt_choice(
            "What templates would you like to see?",
            ["App Templates", "Website Templates", "Both"],
            default="Both"
        )
        
        if choice in ["App Templates", "Both"]:
            app_creation_guide.show_app_templates()
        
        if choice in ["Website Templates", "Both"]:
            app_creation_guide.show_website_templates()
            
    except Exception as e:
        handle_error(e)


@create_app.command()
def tech_stack():
    """Show tech stack selection guide."""
    try:
        app_creation_guide.show_tech_stack_guide()
    except Exception as e:
        handle_error(e)


@create_app.command()
def best_practices():
    """Show development best practices guide."""
    try:
        app_creation_guide.show_best_practices()
    except Exception as e:
        handle_error(e)


@main.group()
def guide():
    """Comprehensive project guidance commands."""
    pass


@guide.command()
@click.argument('project_type', type=click.Choice(['web-app', 'mobile-app', 'desktop-app', 'api-service', 'cli-tool', 'business-website', 'portfolio-website', 'ecommerce-website', 'blog-website', 'landing-page']))
def create(project_type: str):
    """Create a specific type of project with guided assistance."""
    try:
        if project_type in ['web-app', 'mobile-app', 'desktop-app', 'api-service', 'cli-tool']:
            # App creation
            app_creation_guide._guide_app_creation()
        else:
            # Website creation
            app_creation_guide._guide_website_creation()
    except Exception as e:
        handle_error(e)


@guide.command()
def compare():
    """Compare different project types and technologies."""
    try:
        comparison_guide = """
# Project Type Comparison

## Apps vs Websites

### Web Applications
- **Best for:** Interactive functionality, user accounts, real-time features
- **Examples:** Social media, productivity tools, dashboards
- **Tech Stack:** React, Vue, Angular + Node.js, Python, Go
- **Complexity:** Medium to High
- **Timeline:** 2-8 weeks

### Mobile Applications
- **Best for:** Native mobile experience, offline functionality
- **Examples:** Games, productivity apps, social apps
- **Tech Stack:** React Native, Flutter, Swift, Kotlin
- **Complexity:** High
- **Timeline:** 6-12 weeks

### Desktop Applications
- **Best for:** System integration, offline work, complex UI
- **Examples:** Design tools, development tools, games
- **Tech Stack:** Electron, Qt, .NET, Java
- **Complexity:** Medium to High
- **Timeline:** 4-10 weeks

### Websites
- **Best for:** Content delivery, marketing, information sharing
- **Examples:** Business sites, portfolios, blogs, landing pages
- **Tech Stack:** HTML/CSS/JS, React, Vue, Next.js
- **Complexity:** Low to Medium
- **Timeline:** 1-4 weeks

## Technology Comparison

### Frontend Frameworks

| Framework | Learning Curve | Performance | Ecosystem | Best For |
|-----------|---------------|-------------|-----------|----------|
| React | Medium | High | Large | Complex UIs |
| Vue | Easy | High | Medium | Rapid Development |
| Angular | Hard | High | Large | Enterprise |
| Svelte | Easy | Very High | Small | Performance |

### Backend Technologies

| Technology | Learning Curve | Performance | Scalability | Best For |
|------------|---------------|-------------|-------------|----------|
| Node.js | Easy | Medium | High | Real-time Apps |
| Python | Easy | Medium | High | Data Apps |
| Go | Medium | High | Very High | APIs |
| Java | Hard | High | Very High | Enterprise |

### Databases

| Database | Type | Performance | Scalability | Best For |
|----------|------|-------------|-------------|----------|
| PostgreSQL | SQL | High | High | Complex Queries |
| MongoDB | NoSQL | Medium | Very High | Document Storage |
| SQLite | SQL | Medium | Low | Small Apps |
| Redis | NoSQL | Very High | High | Caching |
"""
        
        enhanced_console.print_markdown(comparison_guide, "Project Type Comparison")
        
    except Exception as e:
        handle_error(e)


@guide.command()
def roadmap():
    """Show development roadmap and milestones."""
    try:
        roadmap_guide = """
# Development Roadmap

## Phase 1: Planning & Setup (Week 1)
- [ ] Define project requirements
- [ ] Choose technology stack
- [ ] Set up development environment
- [ ] Create project structure
- [ ] Set up version control

## Phase 2: Core Development (Weeks 2-4)
- [ ] Implement basic functionality
- [ ] Create user interface
- [ ] Set up database
- [ ] Implement authentication
- [ ] Add core features

## Phase 3: Enhancement (Weeks 5-6)
- [ ] Add advanced features
- [ ] Implement error handling
- [ ] Add testing
- [ ] Optimize performance
- [ ] Improve user experience

## Phase 4: Testing & Deployment (Weeks 7-8)
- [ ] Comprehensive testing
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Security audit
- [ ] Deploy to production

## Milestones

### MVP (Minimum Viable Product)
- Core functionality working
- Basic user interface
- Essential features implemented
- Ready for initial testing

### Beta Release
- All planned features implemented
- Thoroughly tested
- Performance optimized
- Ready for user feedback

### Production Release
- Fully tested and optimized
- Security hardened
- Documentation complete
- Ready for public use

## Success Metrics

### Technical Metrics
- Code coverage > 80%
- Performance < 3s load time
- Zero critical security issues
- 99.9% uptime

### User Metrics
- User satisfaction > 4.5/5
- Low bounce rate < 30%
- High engagement
- Positive feedback
"""
        
        enhanced_console.print_markdown(roadmap_guide, "Development Roadmap")
        
    except Exception as e:
        handle_error(e)


@guide.command()
def checklist():
    """Show project development checklist."""
    try:
        checklist_guide = """
# Project Development Checklist

## Pre-Development
- [ ] Project requirements defined
- [ ] Technology stack selected
- [ ] Development environment set up
- [ ] Project structure created
- [ ] Git repository initialized
- [ ] Team roles assigned

## Development
- [ ] Core functionality implemented
- [ ] User interface designed
- [ ] Database schema created
- [ ] API endpoints developed
- [ ] Authentication implemented
- [ ] Error handling added
- [ ] Logging implemented
- [ ] Configuration management

## Testing
- [ ] Unit tests written
- [ ] Integration tests created
- [ ] End-to-end tests implemented
- [ ] Performance tests conducted
- [ ] Security tests performed
- [ ] Accessibility tests done
- [ ] Cross-browser testing
- [ ] Mobile responsiveness tested

## Deployment
- [ ] Production environment set up
- [ ] CI/CD pipeline configured
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] SSL certificates installed
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Documentation updated

## Post-Launch
- [ ] Performance monitoring
- [ ] User feedback collection
- [ ] Bug tracking
- [ ] Feature requests management
- [ ] Regular updates
- [ ] Security patches
- [ ] Performance optimization
- [ ] User support
"""
        
        enhanced_console.print_markdown(checklist_guide, "Development Checklist")
        
    except Exception as e:
        handle_error(e)


@main.group()
def resources():
    """Learning resources and tools."""
    pass


@resources.command()
def learning():
    """Show learning resources for app/website development."""
    try:
        learning_resources = """
# Learning Resources

## Online Courses
- **FreeCodeCamp:** Free comprehensive web development courses
- **Codecademy:** Interactive coding lessons
- **Coursera:** University-level courses
- **Udemy:** Practical project-based courses
- **Pluralsight:** Professional development courses

## Documentation
- **MDN Web Docs:** Comprehensive web development documentation
- **React Docs:** Official React documentation
- **Vue.js Guide:** Official Vue.js guide
- **Node.js Docs:** Official Node.js documentation
- **Python Docs:** Official Python documentation

## YouTube Channels
- **Traversy Media:** Web development tutorials
- **The Net Ninja:** Programming tutorials
- **Academind:** React and web development
- **Coding Addict:** JavaScript and React
- **Web Dev Simplified:** Web development concepts

## Books
- **"You Don't Know JS"** by Kyle Simpson
- **"Eloquent JavaScript"** by Marijn Haverbeke
- **"Clean Code"** by Robert C. Martin
- **"Design Patterns"** by Gang of Four
- **"The Pragmatic Programmer"** by David Thomas

## Tools & Platforms
- **VS Code:** Popular code editor
- **GitHub:** Version control and collaboration
- **Stack Overflow:** Q&A community
- **Dev.to:** Developer community
- **Hashnode:** Developer blogging platform

## Practice Platforms
- **LeetCode:** Algorithm practice
- **HackerRank:** Coding challenges
- **Codewars:** Programming kata
- **Frontend Mentor:** Frontend challenges
- **CodePen:** Code playground
"""
        
        enhanced_console.print_markdown(learning_resources, "Learning Resources")
        
    except Exception as e:
        handle_error(e)


@resources.command()
def tools():
    """Show essential development tools."""
    try:
        tools_guide = """
# Essential Development Tools

## Code Editors
- **VS Code:** Free, feature-rich editor with extensions
- **WebStorm:** Professional IDE for web development
- **Sublime Text:** Fast, lightweight editor
- **Atom:** Hackable text editor
- **Vim/Neovim:** Terminal-based editor

## Version Control
- **Git:** Distributed version control system
- **GitHub:** Git hosting and collaboration
- **GitLab:** DevOps platform
- **Bitbucket:** Git repository hosting
- **SourceTree:** Git GUI client

## Package Managers
- **npm:** Node.js package manager
- **yarn:** Fast, reliable package manager
- **pnpm:** Efficient package manager
- **pip:** Python package manager
- **composer:** PHP dependency manager

## Build Tools
- **Webpack:** Module bundler
- **Vite:** Fast build tool
- **Parcel:** Zero-config build tool
- **Rollup:** Module bundler
- **Gulp:** Task runner

## Testing Tools
- **Jest:** JavaScript testing framework
- **Cypress:** End-to-end testing
- **Playwright:** Browser automation
- **Selenium:** Web browser automation
- **Mocha:** JavaScript test framework

## Design Tools
- **Figma:** Collaborative design tool
- **Sketch:** Design toolkit
- **Adobe XD:** UI/UX design tool
- **InVision:** Design collaboration
- **Canva:** Graphic design platform

## Deployment Tools
- **Vercel:** Frontend deployment
- **Netlify:** Static site deployment
- **Heroku:** Platform as a service
- **AWS:** Cloud computing platform
- **Docker:** Containerization platform
"""
        
        enhanced_console.print_markdown(tools_guide, "Development Tools")
        
    except Exception as e:
        handle_error(e)


@resources.command()
def communities():
    """Show developer communities and forums."""
    try:
        communities_guide = """
# Developer Communities

## General Communities
- **Stack Overflow:** Q&A for programmers
- **Reddit r/programming:** Programming discussions
- **Dev.to:** Developer community platform
- **Hashnode:** Developer blogging
- **Medium:** Technical articles

## Language-Specific
- **React Community:** React developers
- **Vue.js Community:** Vue.js developers
- **Node.js Community:** Node.js developers
- **Python Community:** Python developers
- **JavaScript Community:** JavaScript developers

## Professional Networks
- **LinkedIn:** Professional networking
- **GitHub:** Code collaboration
- **GitLab:** DevOps collaboration
- **Dribbble:** Design community
- **Behance:** Creative portfolio

## Learning Communities
- **FreeCodeCamp:** Free coding education
- **Codecademy Community:** Learning support
- **Coursera Forums:** Course discussions
- **Udemy Community:** Course support
- **Pluralsight Community:** Skill development

## Local Communities
- **Meetup:** Local tech meetups
- **Eventbrite:** Tech events
- **Conference Websites:** Industry conferences
- **University Groups:** Student communities
- **Coworking Spaces:** Local developer hubs

## Discord/Slack Communities
- **Discord Developer Servers:** Real-time chat
- **Slack Workspaces:** Team collaboration
- **Telegram Groups:** Mobile-friendly chat
- **WhatsApp Groups:** Local developer groups
- **Matrix Rooms:** Decentralized chat
"""
        
        enhanced_console.print_markdown(communities_guide, "Developer Communities")
        
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    main()
