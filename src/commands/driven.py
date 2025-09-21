"""
Driven Workflow Commands for DocGen CLI Phase 3.

This module provides CLI commands for the driven workflow integration,
including spec validation, agent hooks, project steering, and AI traceability.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from src.core.error_handler import handle_error
from src.core.spec_validator import create_spec_validator
from src.core.agent_hooks import create_agent_hook_manager
from src.core.project_steering_controller import create_project_steering_controller, SteeringMode
from src.core.ai_traceability_system import create_ai_traceability_system, AIDecision, DecisionType, ImpactLevel, TraceabilityLevel
from src.core.audit_compliance_framework import create_audit_compliance_framework, AuditType

console = Console()


@click.group()
def driven():
    """Driven workflow integration commands."""
    pass


@driven.command()
@click.option('--auto-fix', is_flag=True, help='Automatically fix spec issues when possible')
@click.option('--output', type=click.Path(), help='Output file for validation report')
def validate_specs(auto_fix: bool, output: Optional[str]):
    """Validate spec compliance and traceability."""
    try:
        project_root = Path.cwd()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Validating specs...", total=None)
            
            # Create spec validator
            spec_validator = create_spec_validator(project_root)
            
            # Run validation
            validation_result = spec_validator.validate_spec_compliance()
            traceability_result = spec_validator.validate_spec_to_code_traceability()
            
            progress.update(task, description="Generating compliance report...")
            compliance_report = spec_validator.generate_compliance_report()
            
            progress.update(task, description="Complete!")
        
        # Display results
        console.print("\n[bold blue]Spec Validation Results[/bold blue]")
        
        # Validation summary
        status_color = "green" if validation_result.is_valid else "red"
        console.print(f"Status: [{status_color}]{'VALID' if validation_result.is_valid else 'INVALID'}[/{status_color}]")
        console.print(f"Compliance Score: {validation_result.compliance_score}%")
        console.print(f"Traceability Score: {traceability_result['traceability_score']}%")
        
        # Errors and warnings
        if validation_result.errors:
            console.print("\n[bold red]Errors:[/bold red]")
            for error in validation_result.errors:
                console.print(f"  • {error}")
        
        if validation_result.warnings:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for warning in validation_result.warnings:
                console.print(f"  • {warning}")
        
        # Recommendations
        if compliance_report.get('recommendations'):
            console.print("\n[bold blue]Recommendations:[/bold blue]")
            for rec in compliance_report['recommendations']:
                console.print(f"  • {rec}")
        
        # Save report if requested
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(compliance_report, f, indent=2, default=str)
            
            console.print(f"\n[green]Report saved to: {output_path}[/green]")
        
    except Exception as e:
        handle_error(e, "Failed to validate specs")


@driven.command()
@click.option('--start', is_flag=True, help='Start agent hooks monitoring')
@click.option('--stop', is_flag=True, help='Stop agent hooks monitoring')
@click.option('--status', is_flag=True, help='Show agent hooks status')
def agent_hooks(start: bool, stop: bool, status: bool):
    """Manage agent hooks system."""
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        if start:
            console.print("[bold blue]Starting agent hooks monitoring...[/bold blue]")
            hook_manager.start_monitoring()
            console.print("[green]Agent hooks monitoring started![/green]")
            
        elif stop:
            console.print("[bold blue]Stopping agent hooks monitoring...[/bold blue]")
            hook_manager.stop_monitoring()
            console.print("[green]Agent hooks monitoring stopped![/green]")
            
        elif status:
            hook_status = hook_manager.get_hook_status()
            
            console.print("\n[bold blue]Agent Hooks Status[/bold blue]")
            
            table = Table()
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Hooks", str(hook_status['total_hooks']))
            table.add_row("Enabled Hooks", str(hook_status['enabled_hooks']))
            table.add_row("Disabled Hooks", str(hook_status['disabled_hooks']))
            table.add_row("Monitoring Active", "Yes" if hook_status['monitoring_active'] else "No")
            
            console.print(table)
            
            # Show individual hooks
            if hook_status['hooks']:
                console.print("\n[bold blue]Hook Details:[/bold blue]")
                hooks_table = Table()
                hooks_table.add_column("Name", style="cyan")
                hooks_table.add_column("Enabled", style="green")
                hooks_table.add_column("Pattern", style="yellow")
                hooks_table.add_column("Events", style="blue")
                hooks_table.add_column("Actions", style="magenta")
                
                for name, hook_info in hook_status['hooks'].items():
                    hooks_table.add_row(
                        name,
                        "Yes" if hook_info['enabled'] else "No",
                        hook_info['pattern'],
                        ", ".join(hook_info['event_types']),
                        str(hook_info['actions'])
                    )
                
                console.print(hooks_table)
        
        else:
            console.print("[yellow]Please specify --start, --stop, or --status[/yellow]")
        
    except Exception as e:
        handle_error(e, "Failed to manage agent hooks")


@driven.command()
@click.option('--mode', type=click.Choice(['automatic', 'guided', 'manual']), 
              default='automatic', help='Steering mode')
@click.option('--start', is_flag=True, help='Start project steering')
@click.option('--stop', is_flag=True, help='Stop project steering')
@click.option('--status', is_flag=True, help='Show project status')
@click.option('--quality-gate', type=click.Choice(['pre_commit', 'pre_deployment', 'continuous']),
              help='Run specific quality gate')
def project_steering(mode: str, start: bool, stop: bool, status: bool, quality_gate: Optional[str]):
    """Manage project steering controller."""
    try:
        project_root = Path.cwd()
        steering_mode = SteeringMode(mode)
        steering_controller = create_project_steering_controller(project_root, steering_mode)
        
        if start:
            console.print(f"[bold blue]Starting project steering in {mode} mode...[/bold blue]")
            steering_controller.start_steering()
            console.print("[green]Project steering started![/green]")
            
        elif stop:
            console.print("[bold blue]Stopping project steering...[/bold blue]")
            steering_controller.stop_steering()
            console.print("[green]Project steering stopped![/green]")
            
        elif status:
            project_status = steering_controller.get_project_status()
            
            console.print("\n[bold blue]Project Status[/bold blue]")
            
            # Project overview
            overview_table = Table()
            overview_table.add_column("Metric", style="cyan")
            overview_table.add_column("Value", style="green")
            
            overview_table.add_row("Project Name", project_status['project_name'])
            overview_table.add_row("Current Phase", project_status['current_phase'])
            overview_table.add_row("Quality Score", f"{project_status['quality_score']:.1f}%")
            overview_table.add_row("Compliance Score", f"{project_status['compliance_score']:.1f}%")
            overview_table.add_row("Steering Mode", project_status['steering_mode'])
            overview_table.add_row("Steering Active", "Yes" if project_status['steering_active'] else "No")
            
            console.print(overview_table)
            
            # Active and completed tasks
            if project_status['active_tasks']:
                console.print("\n[bold blue]Active Tasks:[/bold blue]")
                for task in project_status['active_tasks']:
                    console.print(f"  • {task}")
            
            if project_status['completed_tasks']:
                console.print("\n[bold green]Completed Tasks:[/bold green]")
                for task in project_status['completed_tasks']:
                    console.print(f"  • {task}")
            
            # Recent decisions
            if project_status['recent_decisions']:
                console.print("\n[bold blue]Recent Architectural Decisions:[/bold blue]")
                decisions_table = Table()
                decisions_table.add_column("ID", style="cyan")
                decisions_table.add_column("Title", style="green")
                decisions_table.add_column("Status", style="yellow")
                decisions_table.add_column("Created", style="blue")
                
                for decision in project_status['recent_decisions']:
                    decisions_table.add_row(
                        decision['id'],
                        decision['title'],
                        decision['status'],
                        decision['created']
                    )
                
                console.print(decisions_table)
        
        elif quality_gate:
            console.print(f"[bold blue]Running {quality_gate} quality gate...[/bold blue]")
            
            from src.core.project_steering_controller import QualityGate
            gate_type = QualityGate(quality_gate)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Running {quality_gate} quality gate...", total=None)
                
                result = steering_controller.run_quality_gate(gate_type)
                
                progress.update(task, description="Complete!")
            
            # Display results
            status_color = "green" if result.passed else "red"
            console.print(f"\nQuality Gate: [{status_color}]{'PASSED' if result.passed else 'FAILED'}[/{status_color}]")
            console.print(f"Score: {result.score:.1f}%")
            
            if result.issues:
                console.print("\n[bold red]Issues:[/bold red]")
                for issue in result.issues:
                    console.print(f"  • {issue}")
            
            if result.recommendations:
                console.print("\n[bold blue]Recommendations:[/bold blue]")
                for rec in result.recommendations:
                    console.print(f"  • {rec}")
        
        else:
            console.print("[yellow]Please specify --start, --stop, --status, or --quality-gate[/yellow]")
        
    except Exception as e:
        handle_error(e, "Failed to manage project steering")


@driven.command()
@click.option('--log-decision', is_flag=True, help='Log a new AI decision')
@click.option('--analyze-impact', type=str, help='Analyze impact of a decision ID')
@click.option('--compliance-report', is_flag=True, help='Generate compliance report')
def ai_traceability(log_decision: bool, analyze_impact: Optional[str], compliance_report: bool):
    """Manage AI traceability system."""
    try:
        project_root = Path.cwd()
        traceability_system = create_ai_traceability_system(project_root)
        
        if log_decision:
            console.print("[bold blue]Logging new AI decision...[/bold blue]")
            
            # Interactive decision logging
            title = click.prompt("Decision title")
            description = click.prompt("Decision description")
            rationale = click.prompt("Rationale")
            decision_type = click.prompt("Decision type", 
                                       type=click.Choice([dt.value for dt in DecisionType]))
            impact_level = click.prompt("Impact level", 
                                      type=click.Choice([il.value for il in ImpactLevel]))
            traceability_level = click.prompt("Traceability level", 
                                            type=click.Choice([tl.value for tl in TraceabilityLevel]))
            
            # Create decision
            decision = AIDecision(
                decision_id=f"DEC-{int(time.time())}",
                decision_type=DecisionType(decision_type),
                title=title,
                description=description,
                rationale=rationale,
                alternatives_considered=[],
                chosen_solution=description,
                impact_level=ImpactLevel(impact_level),
                traceability_level=TraceabilityLevel(traceability_level),
                spec_references=[],
                code_references=[],
                test_references=[],
                documentation_references=[],
                created_by="User",
                created_date=datetime.now(),
                last_updated=datetime.now(),
                status="active",
                metadata={}
            )
            
            traceability_system.log_decision(decision)
            console.print(f"[green]Decision logged: {decision.decision_id}[/green]")
        
        elif analyze_impact:
            console.print(f"[bold blue]Analyzing impact of decision: {analyze_impact}[/bold blue]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Analyzing impact...", total=None)
                
                analysis = traceability_system.analyze_decision_impact(analyze_impact)
                
                progress.update(task, description="Complete!")
            
            # Display analysis results
            console.print(f"\n[bold blue]Impact Analysis: {analysis.analysis_id}[/bold blue]")
            console.print(f"Risk Assessment: {analysis.risk_assessment}")
            
            if analysis.affected_components:
                console.print("\n[bold yellow]Affected Components:[/bold yellow]")
                for component in analysis.affected_components:
                    console.print(f"  • {component}")
            
            if analysis.affected_files:
                console.print("\n[bold yellow]Affected Files:[/bold yellow]")
                for file in analysis.affected_files:
                    console.print(f"  • {file}")
            
            if analysis.mitigation_strategies:
                console.print("\n[bold blue]Mitigation Strategies:[/bold blue]")
                for strategy in analysis.mitigation_strategies:
                    console.print(f"  • {strategy}")
        
        elif compliance_report:
            console.print("[bold blue]Generating compliance report...[/bold blue]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Generating compliance report...", total=None)
                
                report = traceability_system.generate_compliance_report()
                
                progress.update(task, description="Complete!")
            
            # Display compliance report
            console.print("\n[bold blue]AI Traceability Compliance Report[/bold blue]")
            
            compliance_table = Table()
            compliance_table.add_column("Metric", style="cyan")
            compliance_table.add_column("Value", style="green")
            
            compliance_table.add_row("Total Decisions", str(report['total_decisions']))
            compliance_table.add_row("Traced Decisions", str(report['traced_decisions']))
            compliance_table.add_row("Analyzed Decisions", str(report['analyzed_decisions']))
            compliance_table.add_row("Total Links", str(report['total_links']))
            compliance_table.add_row("Total Analyses", str(report['total_analyses']))
            compliance_table.add_row("Traceability Score", f"{report['traceability_score']:.1f}%")
            compliance_table.add_row("Analysis Score", f"{report['analysis_score']:.1f}%")
            compliance_table.add_row("Overall Compliance", f"{report['overall_compliance']:.1f}%")
            
            console.print(compliance_table)
            
            if report['recommendations']:
                console.print("\n[bold blue]Recommendations:[/bold blue]")
                for rec in report['recommendations']:
                    console.print(f"  • {rec}")
        
        else:
            console.print("[yellow]Please specify --log-decision, --analyze-impact, or --compliance-report[/yellow]")
        
    except Exception as e:
        handle_error(e, "Failed to manage AI traceability")


@driven.command()
@click.option('--audit-type', type=click.Choice([at.value for at in AuditType]), 
              default='comprehensive', help='Type of audit to run')
@click.option('--output', type=click.Path(), help='Output file for audit report')
def audit_compliance(audit_type: str, output: Optional[str]):
    """Run compliance audit."""
    try:
        project_root = Path.cwd()
        audit_framework = create_audit_compliance_framework(project_root)
        
        console.print(f"[bold blue]Running {audit_type} compliance audit...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Running {audit_type} audit...", total=None)
            
            audit_type_enum = AuditType(audit_type)
            report = audit_framework.run_comprehensive_audit(audit_type_enum)
            
            progress.update(task, description="Complete!")
        
        # Display audit results
        console.print("\n[bold blue]Compliance Audit Results[/bold blue]")
        
        # Overall results
        status_color = "green" if report.compliance_level.value == "full" else "yellow" if report.compliance_level.value == "partial" else "red"
        console.print(f"Compliance Level: [{status_color}]{report.compliance_level.value.upper()}[/{status_color}]")
        console.print(f"Overall Score: {report.overall_score:.1f}%")
        console.print(f"Total Checks: {report.total_checks}")
        console.print(f"Passed Checks: {report.passed_checks}")
        console.print(f"Failed Checks: {report.failed_checks}")
        
        # Critical findings
        if report.critical_findings:
            console.print("\n[bold red]Critical Findings:[/bold red]")
            for finding in report.critical_findings:
                console.print(f"  • {finding}")
        
        # Recommendations
        if report.recommendations:
            console.print("\n[bold blue]Recommendations:[/bold blue]")
            for rec in report.recommendations:
                console.print(f"  • {rec}")
        
        # Save report if requested
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            report_data = {
                "report_id": report.report_id,
                "report_type": report.report_type.value,
                "standard": report.standard.value,
                "overall_score": report.overall_score,
                "compliance_level": report.compliance_level.value,
                "total_checks": report.total_checks,
                "passed_checks": report.passed_checks,
                "failed_checks": report.failed_checks,
                "critical_findings": report.critical_findings,
                "recommendations": report.recommendations,
                "generated_date": report.generated_date.isoformat(),
                "metadata": report.metadata
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            console.print(f"\n[green]Audit report saved to: {output_path}[/green]")
        
    except Exception as e:
        handle_error(e, "Failed to run compliance audit")


@driven.command()
def dashboard():
    """Show driven workflow dashboard."""
    try:
        project_root = Path.cwd()
        
        console.print("\n[bold blue]Driven Workflow Dashboard[/bold blue]")
        
        # Get status from all components
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Gathering status information...", total=None)
            
            # Spec validation status
            spec_validator = create_spec_validator(project_root)
            validation_result = spec_validator.validate_spec_compliance()
            
            # Agent hooks status
            hook_manager = create_agent_hook_manager(project_root)
            hook_status = hook_manager.get_hook_status()
            
            # Project steering status
            steering_controller = create_project_steering_controller(project_root)
            project_status = steering_controller.get_project_status()
            
            # AI traceability status
            traceability_system = create_ai_traceability_system(project_root)
            compliance_report = traceability_system.generate_compliance_report()
            
            # Audit compliance status
            audit_framework = create_audit_compliance_framework(project_root)
            dashboard_data = audit_framework.generate_compliance_dashboard()
            
            progress.update(task, description="Complete!")
        
        # Display dashboard
        console.print("\n[bold green]System Status Overview[/bold green]")
        
        # Main metrics table
        metrics_table = Table()
        metrics_table.add_column("Component", style="cyan")
        metrics_table.add_column("Status", style="green")
        metrics_table.add_column("Score", style="yellow")
        metrics_table.add_column("Details", style="blue")
        
        metrics_table.add_row(
            "Spec Validation",
            "✅ Active" if validation_result.is_valid else "❌ Issues",
            f"{validation_result.compliance_score:.1f}%",
            f"{len(validation_result.errors)} errors, {len(validation_result.warnings)} warnings"
        )
        
        metrics_table.add_row(
            "Agent Hooks",
            "✅ Active" if hook_status['monitoring_active'] else "⏸️ Stopped",
            f"{hook_status['enabled_hooks']}/{hook_status['total_hooks']}",
            f"{hook_status['enabled_hooks']} enabled hooks"
        )
        
        metrics_table.add_row(
            "Project Steering",
            "✅ Active" if project_status['steering_active'] else "⏸️ Stopped",
            f"{project_status['quality_score']:.1f}%",
            f"Mode: {project_status['steering_mode']}"
        )
        
        metrics_table.add_row(
            "AI Traceability",
            "✅ Active",
            f"{compliance_report['overall_compliance']:.1f}%",
            f"{compliance_report['total_decisions']} decisions logged"
        )
        
        metrics_table.add_row(
            "Audit Compliance",
            "✅ Active",
            f"{dashboard_data['overall_metrics']['success_rate']:.1f}%",
            f"{dashboard_data['overall_metrics']['passed_checks']}/{dashboard_data['overall_metrics']['total_checks']} checks passed"
        )
        
        console.print(metrics_table)
        
        # Recent activity
        if compliance_report.get('recent_decisions'):
            console.print("\n[bold blue]Recent AI Decisions[/bold blue]")
            recent_table = Table()
            recent_table.add_column("ID", style="cyan")
            recent_table.add_column("Title", style="green")
            recent_table.add_column("Type", style="yellow")
            recent_table.add_column("Impact", style="blue")
            recent_table.add_column("Created", style="magenta")
            
            for decision in compliance_report['recent_decisions'][:5]:
                recent_table.add_row(
                    decision['id'],
                    decision['title'],
                    decision['type'],
                    decision['impact'],
                    decision['created']
                )
            
            console.print(recent_table)
        
        # Critical issues
        critical_issues = []
        if validation_result.errors:
            critical_issues.extend([f"Spec: {e}" for e in validation_result.errors[:3]])
        if dashboard_data.get('critical_issues'):
            critical_issues.extend([f"Compliance: {ci}" for ci in dashboard_data['critical_issues'][:3]])
        
        if critical_issues:
            console.print("\n[bold red]Critical Issues[/bold red]")
            for issue in critical_issues:
                console.print(f"  • {issue}")
        
        # Recommendations
        all_recommendations = []
        if compliance_report.get('recommendations'):
            all_recommendations.extend(compliance_report['recommendations'])
        if dashboard_data.get('recommendations'):
            all_recommendations.extend(dashboard_data['recommendations'])
        
        if all_recommendations:
            console.print("\n[bold blue]Top Recommendations[/bold blue]")
            for rec in list(set(all_recommendations))[:5]:
                console.print(f"  • {rec}")
        
        console.print(f"\n[dim]Dashboard generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
        
    except Exception as e:
        handle_error(e, "Failed to generate dashboard")


if __name__ == '__main__':
    driven()
