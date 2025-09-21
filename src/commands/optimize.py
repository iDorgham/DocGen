"""
MCP Optimization Engine CLI Commands

This module provides CLI commands for interacting with the MCP Optimization Engine,
including tool selection optimization, performance monitoring, and knowledge management.

Author: DocGen CLI Team
Created: 2025-01-20
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from ..core.optimization_engine import (
    MCPOptimizationEngine, 
    OptimizationStrategy, 
    ToolSelectionMethod,
    ToolContext
)

console = Console()


@click.group()
def optimize():
    """MCP Optimization Engine commands for intelligent tool selection and performance monitoring."""
    pass


@optimize.command()
@click.option('--task-type', required=True, help='Type of task to optimize for')
@click.option('--requirements', multiple=True, help='Task requirements')
@click.option('--strategy', 
              type=click.Choice(['performance', 'accuracy', 'balanced', 'cost_effective']),
              default='balanced', help='Optimization strategy')
@click.option('--method',
              type=click.Choice(['context_based', 'performance_based', 'hybrid', 'machine_learning']),
              default='hybrid', help='Tool selection method')
@click.option('--constraints', help='JSON string of constraints')
@click.option('--preferences', help='JSON string of user preferences')
@click.option('--output', help='Output file for results')
def select_tools(task_type: str, requirements: List[str], strategy: str, 
                method: str, constraints: Optional[str], preferences: Optional[str],
                output: Optional[str]):
    """Optimize tool selection for a specific task."""
    
    # Parse constraints and preferences
    constraints_dict = {}
    preferences_dict = {}
    
    if constraints:
        try:
            constraints_dict = json.loads(constraints)
        except json.JSONDecodeError:
            console.print("[red]Error: Invalid JSON in constraints parameter[/red]")
            return
    
    if preferences:
        try:
            preferences_dict = json.loads(preferences)
        except json.JSONDecodeError:
            console.print("[red]Error: Invalid JSON in preferences parameter[/red]")
            return
    
    # Initialize optimization engine
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Initializing optimization engine...", total=None)
        
        engine = MCPOptimizationEngine()
        progress.update(task, description="Optimizing tool selection...")
        
        # Perform optimization
        result = engine.optimize_tool_selection(
            task_type=task_type,
            requirements=list(requirements),
            constraints=constraints_dict,
            user_preferences=preferences_dict
        )
        
        progress.update(task, description="Optimization complete!", completed=True)
    
    # Display results
    display_optimization_result(result, task_type, strategy, method)
    
    # Save to file if requested
    if output:
        save_optimization_result(result, output)


@optimize.command()
@click.option('--server', help='Specific server to monitor (optional)')
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
@click.option('--output', help='Output file for results')
def performance(server: Optional[str], format: str, output: Optional[str]):
    """Monitor MCP server performance metrics."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Loading performance data...", total=None)
        
        engine = MCPOptimizationEngine()
        summary = engine.get_performance_summary()
        
        progress.update(task, description="Performance data loaded!", completed=True)
    
    if format == 'table':
        display_performance_summary(summary, server)
    else:
        display_performance_json(summary, server)
    
    if output:
        save_performance_data(summary, output)


@optimize.command()
@click.option('--query', required=True, help='Knowledge query to optimize')
@click.option('--context', help='JSON string of context information')
@click.option('--output', help='Output file for results')
def knowledge(query: str, context: Optional[str], output: Optional[str]):
    """Optimize knowledge retrieval with intelligent caching."""
    
    # Parse context
    context_dict = {}
    if context:
        try:
            context_dict = json.loads(context)
        except json.JSONDecodeError:
            console.print("[red]Error: Invalid JSON in context parameter[/red]")
            return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Optimizing knowledge retrieval...", total=None)
        
        engine = MCPOptimizationEngine()
        result = engine.optimize_knowledge_retrieval(query, context_dict)
        
        progress.update(task, description="Knowledge optimization complete!", completed=True)
    
    # Display results
    display_knowledge_result(result)
    
    if output:
        save_knowledge_result(result, output)


@optimize.command()
@click.option('--server', required=True, help='Server name')
@click.option('--metric', required=True, 
              type=click.Choice(['response_time', 'success_rate', 'error_rate', 'throughput', 'resource_usage']),
              help='Metric type')
@click.option('--value', required=True, type=float, help='Metric value')
def record_metric(server: str, metric: str, value: float):
    """Record a performance metric for a server."""
    
    engine = MCPOptimizationEngine()
    engine.record_performance_metric(server, metric, value)
    
    console.print(f"[green]✓[/green] Recorded {metric}={value} for server '{server}'")


@optimize.command()
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
@click.option('--output', help='Output file for results')
def insights(format: str, output: Optional[str]):
    """Get optimization insights and recommendations."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing optimization data...", total=None)
        
        engine = MCPOptimizationEngine()
        insights_data = engine.get_optimization_insights()
        
        progress.update(task, description="Analysis complete!", completed=True)
    
    if format == 'table':
        display_optimization_insights(insights_data)
    else:
        display_insights_json(insights_data)
    
    if output:
        save_insights_data(insights_data, output)


@optimize.command()
@click.option('--output', required=True, help='Output file for exported data')
def export(output: str):
    """Export optimization data for analysis."""
    
    output_path = Path(output)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Exporting optimization data...", total=None)
        
        engine = MCPOptimizationEngine()
        engine.export_optimization_data(output_path)
        
        progress.update(task, description="Export complete!", completed=True)
    
    console.print(f"[green]✓[/green] Optimization data exported to {output_path}")


@optimize.command()
@click.option('--config-file', help='Configuration file path')
def config(config_file: Optional[str]):
    """Show or update optimization engine configuration."""
    
    config_path = Path(config_file) if config_file else Path("assets/dev/config/optimization_engine.json")
    
    if not config_path.exists():
        console.print(f"[red]Error: Configuration file not found at {config_path}[/red]")
        return
    
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Display configuration
        config_syntax = Syntax(
            json.dumps(config_data, indent=2),
            "json",
            theme="monokai",
            line_numbers=True
        )
        
        console.print(Panel(
            config_syntax,
            title="Optimization Engine Configuration",
            border_style="blue"
        ))
        
    except Exception as e:
        console.print(f"[red]Error reading configuration: {e}[/red]")


def display_optimization_result(result, task_type: str, strategy: str, method: str):
    """Display optimization result in a formatted table."""
    
    # Create main result panel
    result_text = f"""
[bold blue]Task Type:[/bold blue] {task_type}
[bold blue]Strategy:[/bold blue] {strategy}
[bold blue]Method:[/bold blue] {method}
[bold blue]Selected Tools:[/bold blue] {', '.join(result.selected_tools)}
[bold blue]Confidence Score:[/bold blue] {result.confidence_score:.2f}
[bold blue]Optimization Time:[/bold blue] {result.optimization_time:.3f}s
"""
    
    console.print(Panel(
        result_text,
        title="🎯 Tool Selection Optimization Result",
        border_style="green"
    ))
    
    # Display reasoning
    console.print(Panel(
        result.reasoning,
        title="💭 Reasoning",
        border_style="yellow"
    ))
    
    # Display performance predictions
    if result.performance_prediction:
        table = Table(title="📊 Performance Predictions")
        table.add_column("Tool", style="cyan")
        table.add_column("Predicted Success Rate", style="green")
        table.add_column("Predicted Response Time", style="yellow")
        table.add_column("Confidence", style="blue")
        
        for tool, prediction in result.performance_prediction.items():
            table.add_row(
                tool,
                f"{prediction['predicted_success_rate']:.2f}",
                f"{prediction['predicted_response_time']:.2f}s",
                f"{prediction['confidence']:.2f}"
            )
        
        console.print(table)
    
    # Display alternatives
    if result.alternatives:
        console.print("\n[bold]🔄 Alternative Selections:[/bold]")
        for i, alt in enumerate(result.alternatives, 1):
            console.print(f"{i}. [bold]{alt['type']}[/bold]: {', '.join(alt['tools'])}")
            console.print(f"   [dim]{alt['reasoning']}[/dim]")


def display_performance_summary(summary: Dict[str, Any], server: Optional[str]):
    """Display performance summary in table format."""
    
    # Overall health
    health_color = {
        'good': 'green',
        'degraded': 'yellow',
        'poor': 'red'
    }.get(summary['overall_health'], 'white')
    
    console.print(f"\n[bold {health_color}]Overall Health: {summary['overall_health'].upper()}[/bold {health_color}]")
    
    if summary['alerts']:
        console.print(f"[red]Active Alerts: {len(summary['alerts'])}[/red]")
    
    # Server performance table
    table = Table(title="📈 Server Performance Metrics")
    table.add_column("Server", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Response Time", style="yellow")
    table.add_column("Success Rate", style="green")
    table.add_column("Error Rate", style="red")
    table.add_column("Resource Usage", style="blue")
    table.add_column("Last Updated", style="dim")
    
    servers = summary['servers']
    if server:
        servers = {k: v for k, v in servers.items() if k == server}
    
    for server_name, server_data in servers.items():
        metrics = server_data['metrics']
        status = server_data['status']
        
        status_color = 'green' if status == 'healthy' else 'yellow'
        
        table.add_row(
            server_name,
            f"[{status_color}]{status}[/{status_color}]",
            f"{metrics['response_time']:.2f}s",
            f"{metrics['success_rate']:.2f}",
            f"{metrics['error_rate']:.2f}",
            f"{metrics['resource_usage']:.2f}",
            metrics['last_updated'][:19]  # Truncate timestamp
        )
    
    console.print(table)


def display_performance_json(summary: Dict[str, Any], server: Optional[str]):
    """Display performance summary in JSON format."""
    if server and server in summary['servers']:
        filtered_summary = {
            'servers': {server: summary['servers'][server]},
            'alerts': summary['alerts'],
            'overall_health': summary['overall_health']
        }
        console.print_json(data=filtered_summary)
    else:
        console.print_json(data=summary)


def display_knowledge_result(result: Dict[str, Any]):
    """Display knowledge optimization result."""
    
    source_color = 'green' if result['source'] == 'cache' else 'blue'
    optimization_status = '✓' if result['optimization_applied'] else '✗'
    
    console.print(Panel(
        f"""
[bold blue]Query:[/bold blue] {result['result']['query']}
[bold blue]Source:[/bold blue] [{source_color}]{result['source']}[/{source_color}]
[bold blue]Optimization Applied:[/bold blue] {optimization_status}
[bold blue]Timestamp:[/bold blue] {result['result']['timestamp']}
""",
        title="🧠 Knowledge Retrieval Optimization",
        border_style="blue"
    ))


def display_optimization_insights(insights: Dict[str, Any]):
    """Display optimization insights in table format."""
    
    if 'message' in insights:
        console.print(f"[yellow]{insights['message']}[/yellow]")
        return
    
    # Main insights panel
    insights_text = f"""
[bold blue]Total Optimizations:[/bold blue] {insights['total_optimizations']}
[bold blue]Average Confidence:[/bold blue] {insights['average_confidence']:.2f}
"""
    
    console.print(Panel(
        insights_text,
        title="📊 Optimization Insights",
        border_style="blue"
    ))
    
    # Most common tasks
    if insights['most_common_tasks']:
        table = Table(title="🔥 Most Common Tasks")
        table.add_column("Task Type", style="cyan")
        table.add_column("Count", style="green")
        
        for task_type, count in insights['most_common_tasks'].items():
            table.add_row(task_type, str(count))
        
        console.print(table)
    
    # Recommendations
    if insights['recommendations']:
        console.print("\n[bold]💡 Recommendations:[/bold]")
        for i, rec in enumerate(insights['recommendations'], 1):
            console.print(f"{i}. {rec}")


def display_insights_json(insights: Dict[str, Any]):
    """Display insights in JSON format."""
    console.print_json(data=insights)


def save_optimization_result(result, output_path: str):
    """Save optimization result to file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(result.to_dict(), f, indent=2, default=str)
    
    console.print(f"[green]✓[/green] Results saved to {output_file}")


def save_performance_data(summary: Dict[str, Any], output_path: str):
    """Save performance data to file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    console.print(f"[green]✓[/green] Performance data saved to {output_file}")


def save_knowledge_result(result: Dict[str, Any], output_path: str):
    """Save knowledge result to file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    console.print(f"[green]✓[/green] Knowledge result saved to {output_file}")


def save_insights_data(insights: Dict[str, Any], output_path: str):
    """Save insights data to file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(insights, f, indent=2, default=str)
    
    console.print(f"[green]✓[/green] Insights data saved to {output_file}")


if __name__ == "__main__":
    optimize()
