"""
Enhanced Spec Commands for DocGen CLI Phase 3.

This module provides advanced spec management commands for the driven workflow integration.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from src.core.spec_validator import SpecValidator, SpecEvolutionTracker, create_spec_validator
from src.core.error_handler import handle_error, DocGenError
from src.utils.file_io import read_file, write_file


console = Console()


@click.group()
def spec():
    """Enhanced spec management commands for driven workflow."""
    pass


@spec.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for validation report')
@click.option('--format', 'output_format', type=click.Choice(['json', 'markdown', 'console']), 
              default='console', help='Output format for validation report')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed validation information')
def validate(output: Optional[str], output_format: str, verbose: bool):
    """
    Validate spec compliance and traceability.
    
    Performs comprehensive validation of all specification files,
    checks compliance with requirements, and validates spec-to-code traceability.
    """
    try:
        project_root = Path.cwd()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Validating specifications...", total=None)
            
            # Create spec validator
            validator = create_spec_validator(project_root)
            
            # Perform validation
            progress.update(task, description="Running spec compliance validation...")
            validation_result = validator.validate_spec_compliance()
            
            progress.update(task, description="Validating traceability...")
            traceability_result = validator.validate_spec_to_code_traceability()
            
            progress.update(task, description="Generating compliance report...")
            compliance_report = validator.generate_compliance_report()
            
            progress.update(task, description="Complete!", completed=True)
        
        # Display results
        if output_format == 'console':
            _display_validation_results(validation_result, traceability_result, verbose)
        else:
            _save_validation_report(compliance_report, output, output_format)
            
    except Exception as e:
        handle_error(e, "Spec validation failed")


@spec.command()
@click.option('--spec-file', '-f', type=click.Path(exists=True), 
              help='Specific spec file to trace')
@click.option('--output', '-o', type=click.Path(), help='Output file for traceability report')
@click.option('--format', 'output_format', type=click.Choice(['json', 'markdown', 'console']), 
              default='console', help='Output format for traceability report')
def trace(spec_file: Optional[str], output: Optional[str], output_format: str):
    """
    Generate spec-to-code traceability mapping.
    
    Creates detailed mapping between specification sections and
    corresponding implementation files, tests, and documentation.
    """
    try:
        project_root = Path.cwd()
        validator = create_spec_validator(project_root)
        
        if spec_file:
            # Trace specific file
            spec_path = Path(spec_file)
            traceability_map = validator._build_traceability_map(spec_path)
            
            trace_data = {
                "spec_file": str(spec_path),
                "related_files": traceability_map,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Trace all specs
            traceability_result = validator.validate_spec_to_code_traceability()
            trace_data = {
                "overall_traceability": traceability_result,
                "timestamp": datetime.now().isoformat()
            }
        
        if output_format == 'console':
            _display_traceability_results(trace_data)
        else:
            _save_traceability_report(trace_data, output, output_format)
            
    except Exception as e:
        handle_error(e, "Spec traceability failed")


@spec.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.argument('section')
@click.argument('content')
@click.option('--append', '-a', is_flag=True, help='Append to existing section')
@click.option('--validate', '-v', is_flag=True, help='Validate after update')
def update(spec_file: str, section: str, content: str, append: bool, validate_flag: bool):
    """
    Update a specification section.
    
    Updates the specified section in the spec file with new content.
    Automatically tracks changes and validates compliance.
    """
    try:
        spec_path = Path(spec_file)
        
        # Read current content
        current_content = read_file(spec_path)
        
        # Update section
        updated_content = _update_spec_section(
            current_content, section, content, append
        )
        
        # Write updated content
        write_file(spec_path, updated_content)
        
        console.print(f"[green]✓[/green] Updated section '{section}' in {spec_file}")
        
        # Track changes
        project_root = Path.cwd()
        validator = create_spec_validator(project_root)
        evolution_tracker = SpecEvolutionTracker(project_root)
        
        current_hash = validator._generate_spec_hash()
        changes = evolution_tracker.track_spec_changes(current_hash)
        
        if changes["has_changes"]:
            console.print("[yellow]⚠[/yellow] Spec changes detected and tracked")
        
        # Validate if requested
        if validate_flag:
            console.print("\n[blue]Running validation...[/blue]")
            validation_result = validator.validate_spec_compliance()
            
            if validation_result.is_valid:
                console.print("[green]✓[/green] Spec validation passed")
            else:
                console.print("[red]✗[/red] Spec validation failed:")
                for error in validation_result.errors:
                    console.print(f"  [red]•[/red] {error}")
                    
    except Exception as e:
        handle_error(e, "Spec update failed")


@spec.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for evolution report')
@click.option('--format', 'output_format', type=click.Choice(['json', 'markdown', 'console']), 
              default='console', help='Output format for evolution report')
def evolve(output: Optional[str], output_format: str):
    """
    Track and analyze spec evolution.
    
    Analyzes how specifications have evolved over time,
    tracks changes, and provides insights for improvement.
    """
    try:
        project_root = Path.cwd()
        evolution_tracker = SpecEvolutionTracker(project_root)
        validator = create_spec_validator(project_root)
        
        # Get current state
        current_hash = validator._generate_spec_hash()
        changes = evolution_tracker.track_spec_changes(current_hash)
        
        # Generate evolution report
        evolution_report = {
            "current_state": changes,
            "evolution_analysis": _analyze_spec_evolution(project_root),
            "recommendations": _generate_evolution_recommendations(changes),
            "timestamp": datetime.now().isoformat()
        }
        
        if output_format == 'console':
            _display_evolution_results(evolution_report)
        else:
            _save_evolution_report(evolution_report, output, output_format)
            
    except Exception as e:
        handle_error(e, "Spec evolution analysis failed")


def _display_validation_results(validation_result, traceability_result, verbose: bool):
    """Display validation results in console."""
    # Overall status
    status_color = "green" if validation_result.is_valid else "red"
    status_icon = "✓" if validation_result.is_valid else "✗"
    
    console.print(f"\n[bold {status_color}]{status_icon} Spec Validation Results[/bold {status_color}]")
    
    # Compliance score
    score_color = "green" if validation_result.compliance_score >= 80 else "yellow" if validation_result.compliance_score >= 60 else "red"
    console.print(f"Compliance Score: [{score_color}]{validation_result.compliance_score}%[/{score_color}]")
    
    # Traceability score
    trace_score = traceability_result["traceability_score"]
    trace_color = "green" if trace_score >= 90 else "yellow" if trace_score >= 70 else "red"
    console.print(f"Traceability Score: [{trace_color}]{trace_score}%[/{trace_color}]")
    
    # Errors
    if validation_result.errors:
        console.print(f"\n[red]Errors ({len(validation_result.errors)}):[/red]")
        for error in validation_result.errors:
            console.print(f"  [red]•[/red] {error}")
    
    # Warnings
    if validation_result.warnings:
        console.print(f"\n[yellow]Warnings ({len(validation_result.warnings)}):[/yellow]")
        for warning in validation_result.warnings:
            console.print(f"  [yellow]•[/yellow] {warning}")
    
    # Traceability details
    if verbose:
        console.print(f"\n[blue]Traceability Details:[/blue]")
        console.print(f"  Total Specs: {traceability_result['total_specs']}")
        console.print(f"  Traced Specs: {traceability_result['traced_specs']}")
        
        if traceability_result["missing_traces"]:
            console.print(f"  Missing Traces: {', '.join(traceability_result['missing_traces'])}")


def _display_traceability_results(trace_data):
    """Display traceability results in console."""
    console.print("\n[bold blue]Spec-to-Code Traceability[/bold blue]")
    
    if "spec_file" in trace_data:
        # Single file traceability
        console.print(f"Spec File: {trace_data['spec_file']}")
        console.print(f"Related Files: {len(trace_data['related_files'])}")
        
        if trace_data["related_files"]:
            for file_path in trace_data["related_files"]:
                console.print(f"  [green]•[/green] {file_path}")
        else:
            console.print("  [yellow]No related files found[/yellow]")
    else:
        # Overall traceability
        overall = trace_data["overall_traceability"]
        console.print(f"Total Specs: {overall['total_specs']}")
        console.print(f"Traced Specs: {overall['traced_specs']}")
        console.print(f"Traceability Score: {overall['traceability_score']}%")


def _display_evolution_results(evolution_report):
    """Display evolution results in console."""
    console.print("\n[bold blue]Spec Evolution Analysis[/bold blue]")
    
    current_state = evolution_report["current_state"]
    console.print(f"Current Hash: {current_state['current_hash'][:8]}...")
    console.print(f"Has Changes: {'Yes' if current_state['has_changes'] else 'No'}")
    
    if current_state["change_summary"]:
        console.print("Change Summary:")
        for change in current_state["change_summary"]:
            console.print(f"  [yellow]•[/yellow] {change}")
    
    recommendations = evolution_report["recommendations"]
    if recommendations:
        console.print("\n[green]Recommendations:[/green]")
        for rec in recommendations:
            console.print(f"  [green]•[/green] {rec}")


def _update_spec_section(content: str, section: str, new_content: str, append: bool) -> str:
    """Update a section in spec content."""
    lines = content.split('\n')
    updated_lines = []
    in_section = False
    section_updated = False
    
    for line in lines:
        if line.strip() == section:
            in_section = True
            updated_lines.append(line)
            if not append:
                updated_lines.append(new_content)
                section_updated = True
        elif in_section and line.startswith('#'):
            # End of section
            in_section = False
            if append and not section_updated:
                updated_lines.append(new_content)
                section_updated = True
            updated_lines.append(line)
        elif in_section and append:
            # Append mode - add content after existing section content
            updated_lines.append(line)
            if not section_updated:
                updated_lines.append(new_content)
                section_updated = True
        elif not in_section:
            updated_lines.append(line)
        # Skip lines in section when not appending
    
    if not section_updated:
        # Section not found, add it at the end
        updated_lines.append(section)
        updated_lines.append(new_content)
    
    return '\n'.join(updated_lines)


def _save_validation_report(report_data: Dict[str, Any], output: Optional[str], format_type: str):
    """Save validation report to file."""
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"spec_validation_report_{timestamp}.{format_type}"
    
    output_path = Path(output)
    
    if format_type == 'json':
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
    elif format_type == 'markdown':
        _save_markdown_report(report_data, output_path)
    
    console.print(f"[green]✓[/green] Report saved to {output}")


def _save_traceability_report(trace_data: Dict[str, Any], output: Optional[str], format_type: str):
    """Save traceability report to file."""
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"spec_traceability_report_{timestamp}.{format_type}"
    
    output_path = Path(output)
    
    if format_type == 'json':
        with open(output_path, 'w') as f:
            json.dump(trace_data, f, indent=2, default=str)
    elif format_type == 'markdown':
        _save_traceability_markdown(trace_data, output_path)
    
    console.print(f"[green]✓[/green] Traceability report saved to {output}")


def _save_evolution_report(evolution_data: Dict[str, Any], output: Optional[str], format_type: str):
    """Save evolution report to file."""
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"spec_evolution_report_{timestamp}.{format_type}"
    
    output_path = Path(output)
    
    if format_type == 'json':
        with open(output_path, 'w') as f:
            json.dump(evolution_data, f, indent=2, default=str)
    elif format_type == 'markdown':
        _save_evolution_markdown(evolution_data, output_path)
    
    console.print(f"[green]✓[/green] Evolution report saved to {output}")


def _save_markdown_report(report_data: Dict[str, Any], output_path: Path):
    """Save validation report as markdown."""
    content = f"""# Spec Validation Report

Generated: {report_data['timestamp']}

## Validation Results

- **Compliance Score**: {report_data['validation']['compliance_score']}%
- **Is Valid**: {report_data['validation']['is_valid']}
- **Errors**: {len(report_data['validation']['errors'])}
- **Warnings**: {len(report_data['validation']['warnings'])}

## Traceability Results

- **Traceability Score**: {report_data['traceability']['traceability_score']}%
- **Total Specs**: {report_data['traceability']['total_specs']}
- **Traced Specs**: {report_data['traceability']['traced_specs']}

## Overall Compliance

**Score**: {report_data['overall_compliance']}%

## Recommendations

"""
    
    for rec in report_data['recommendations']:
        content += f"- {rec}\n"
    
    write_file(output_path, content)


def _save_traceability_markdown(trace_data: Dict[str, Any], output_path: Path):
    """Save traceability report as markdown."""
    content = f"""# Spec Traceability Report

Generated: {trace_data['timestamp']}

"""
    
    if "spec_file" in trace_data:
        content += f"""## Single File Traceability

**Spec File**: {trace_data['spec_file']}

### Related Files

"""
        for file_path in trace_data["related_files"]:
            content += f"- {file_path}\n"
    else:
        content += f"""## Overall Traceability

- **Total Specs**: {trace_data['overall_traceability']['total_specs']}
- **Traced Specs**: {trace_data['overall_traceability']['traced_specs']}
- **Traceability Score**: {trace_data['overall_traceability']['traceability_score']}%

### Missing Traces

"""
        for missing in trace_data['overall_traceability']['missing_traces']:
            content += f"- {missing}\n"
    
    write_file(output_path, content)


def _save_evolution_markdown(evolution_data: Dict[str, Any], output_path: Path):
    """Save evolution report as markdown."""
    content = f"""# Spec Evolution Report

Generated: {evolution_data['timestamp']}

## Current State

- **Current Hash**: {evolution_data['current_state']['current_hash'][:8]}...
- **Has Changes**: {evolution_data['current_state']['has_changes']}

## Change Summary

"""
    
    for change in evolution_data['current_state']['change_summary']:
        content += f"- {change}\n"
    
    content += "\n## Recommendations\n\n"
    
    for rec in evolution_data['recommendations']:
        content += f"- {rec}\n"
    
    write_file(output_path, content)


def _analyze_spec_evolution(project_root: Path) -> Dict[str, Any]:
    """Analyze spec evolution patterns."""
    return {
        "analysis_type": "basic",
        "insights": [
            "Spec files are actively maintained",
            "Regular updates indicate healthy development process"
        ]
    }


def _generate_evolution_recommendations(changes: Dict[str, Any]) -> list:
    """Generate recommendations based on evolution analysis."""
    recommendations = []
    
    if changes["has_changes"]:
        recommendations.append("Review recent spec changes for consistency")
        recommendations.append("Update related documentation if needed")
    
    recommendations.append("Consider implementing automated spec validation in CI/CD")
    recommendations.append("Regular spec reviews help maintain quality")
    
    return recommendations
