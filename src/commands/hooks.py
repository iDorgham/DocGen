"""
Agent Hooks Commands for DocGen CLI Phase 3.

This module provides CLI commands for managing agent hooks,
event-driven workflows, and intelligent automation.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.core.agent_hooks import AgentHookManager, HookRule, HookAction, create_agent_hook_manager
from src.core.error_handler import handle_error, DocGenError


console = Console()


@click.group()
def hooks():
    """Agent hooks management commands for driven workflow."""
    pass


@hooks.command()
@click.option('--daemon', is_flag=True, help='Run in daemon mode (background)')
@click.option('--config', type=click.Path(exists=True), help='Custom hooks configuration file')
def start(daemon: bool, config: Optional[str]):
    """
    Start agent hooks monitoring.
    
    Begins monitoring file system changes and executing
    automated workflows based on configured hooks.
    """
    try:
        project_root = Path.cwd()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Starting agent hooks...", total=None)
            
            # Create hook manager
            progress.update(task, description="Initializing hook manager...")
            hook_manager = create_agent_hook_manager(project_root)
            
            # Load custom config if provided
            if config:
                progress.update(task, description="Loading custom configuration...")
                _load_hooks_config(hook_manager, config)
            
            # Start monitoring
            progress.update(task, description="Starting file system monitoring...")
            hook_manager.start_monitoring()
            
            progress.update(task, description="Agent hooks started successfully!", completed=True)
        
        console.print(Panel.fit(
            "[green]✓ Agent hooks monitoring started[/green]\n\n"
            f"Project: {project_root}\n"
            f"Active hooks: {len([h for h in hook_manager.hooks.values() if h.enabled])}\n"
            f"Total hooks: {len(hook_manager.hooks)}",
            title="Agent Hooks Active",
            border_style="green"
        ))
        
        if not daemon:
            console.print("\n[yellow]Press Ctrl+C to stop monitoring...[/yellow]")
            try:
                # Keep the process running
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                console.print("\n[yellow]Stopping agent hooks...[/yellow]")
                hook_manager.stop_monitoring()
                console.print("[green]✓ Agent hooks stopped[/green]")
        
    except Exception as e:
        handle_error(e, "Failed to start agent hooks")


@hooks.command()
def stop():
    """
    Stop agent hooks monitoring.
    
    Stops the file system monitoring and terminates
    all automated workflows.
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        console.print("[yellow]Stopping agent hooks monitoring...[/yellow]")
        hook_manager.stop_monitoring()
        
        console.print(Panel.fit(
            "[green]✓ Agent hooks monitoring stopped[/green]",
            title="Agent Hooks Stopped",
            border_style="green"
        ))
        
    except Exception as e:
        handle_error(e, "Failed to stop agent hooks")


@hooks.command()
def status():
    """
    Show agent hooks status.
    
    Displays the current status of all configured hooks,
    monitoring state, and recent activity.
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        # Get hook status
        status_info = hook_manager.get_hook_status()
        
        # Display status
        console.print(Panel.fit(
            f"[bold]Monitoring:[/bold] {'Active' if status_info['monitoring_active'] else 'Inactive'}\n"
            f"[bold]Total Hooks:[/bold] {status_info['total_hooks']}\n"
            f"[bold]Enabled:[/bold] {status_info['enabled_hooks']}\n"
            f"[bold]Disabled:[/bold] {status_info['disabled_hooks']}",
            title="Agent Hooks Status",
            border_style="blue"
        ))
        
        # Show hooks table
        if status_info['hooks']:
            table = Table(title="Configured Hooks")
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Pattern", style="blue")
            table.add_column("Events", style="yellow")
            table.add_column("Actions", style="magenta")
            
            for name, hook_info in status_info['hooks'].items():
                status_text = "✓ Enabled" if hook_info['enabled'] else "✗ Disabled"
                status_color = "green" if hook_info['enabled'] else "red"
                
                table.add_row(
                    name,
                    f"[{status_color}]{status_text}[/{status_color}]",
                    hook_info['pattern'],
                    ", ".join(hook_info['event_types']),
                    str(hook_info['actions'])
                )
            
            console.print(table)
        else:
            console.print("[yellow]No hooks configured[/yellow]")
        
    except Exception as e:
        handle_error(e, "Failed to get hooks status")


@hooks.command()
@click.argument('hook_name')
def enable(hook_name: str):
    """
    Enable a specific hook.
    
    HOOK_NAME: Name of the hook to enable
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        hook_manager.enable_hook(hook_name)
        
        console.print(f"[green]✓ Hook '{hook_name}' enabled[/green]")
        
    except Exception as e:
        handle_error(e, f"Failed to enable hook '{hook_name}'")


@hooks.command()
@click.argument('hook_name')
def disable(hook_name: str):
    """
    Disable a specific hook.
    
    HOOK_NAME: Name of the hook to disable
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        hook_manager.disable_hook(hook_name)
        
        console.print(f"[green]✓ Hook '{hook_name}' disabled[/green]")
        
    except Exception as e:
        handle_error(e, f"Failed to disable hook '{hook_name}'")


@hooks.command()
@click.argument('config_file', type=click.Path())
@click.option('--name', help='Name for the new hook')
@click.option('--pattern', help='File pattern to match')
@click.option('--events', help='Comma-separated list of event types')
@click.option('--actions', help='Comma-separated list of actions')
def add(config_file: str, name: Optional[str], pattern: Optional[str], 
        events: Optional[str], actions: Optional[str]):
    """
    Add a new hook rule.
    
    CONFIG_FILE: Path to hook configuration file (JSON format)
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        if config_file:
            # Load from config file
            _load_hooks_config(hook_manager, config_file)
            console.print(f"[green]✓ Hooks loaded from {config_file}[/green]")
        else:
            # Create hook from command line options
            if not all([name, pattern, events, actions]):
                console.print("[red]Error: All options (--name, --pattern, --events, --actions) are required for command-line hook creation[/red]")
                return
            
            event_types = [e.strip() for e in events.split(',')]
            action_list = []
            
            for action_str in actions.split(','):
                action_parts = action_str.strip().split(':')
                if len(action_parts) >= 2:
                    action = HookAction(
                        action_type=action_parts[0],
                        target=action_parts[1],
                        parameters={}
                    )
                    action_list.append(action)
            
            hook = HookRule(
                name=name,
                pattern=pattern,
                event_types=event_types,
                actions=action_list
            )
            
            hook_manager.add_hook(hook)
            console.print(f"[green]✓ Hook '{name}' added[/green]")
        
    except Exception as e:
        handle_error(e, "Failed to add hook")


@hooks.command()
@click.argument('hook_name')
def remove(hook_name: str):
    """
    Remove a hook rule.
    
    HOOK_NAME: Name of the hook to remove
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        hook_manager.remove_hook(hook_name)
        
        console.print(f"[green]✓ Hook '{hook_name}' removed[/green]")
        
    except Exception as e:
        handle_error(e, f"Failed to remove hook '{hook_name}'")


@hooks.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for configuration')
def export(output: Optional[str]):
    """
    Export current hooks configuration.
    
    Saves the current hooks configuration to a JSON file
    for backup or sharing purposes.
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        # Export configuration
        config = {
            "hooks": [
                {
                    "name": hook.name,
                    "pattern": hook.pattern,
                    "event_types": hook.event_types,
                    "actions": [
                        {
                            "action_type": action.action_type,
                            "target": action.target,
                            "parameters": action.parameters,
                            "priority": action.priority,
                            "max_retries": action.max_retries
                        }
                        for action in hook.actions
                    ],
                    "enabled": hook.enabled,
                    "conditions": hook.conditions
                }
                for hook in hook_manager.hooks.values()
            ],
            "exported_at": str(datetime.now()),
            "project_root": str(project_root)
        }
        
        if not output:
            output = "hooks_config.json"
        
        output_path = Path(output)
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        console.print(f"[green]✓ Hooks configuration exported to {output_path}[/green]")
        
    except Exception as e:
        handle_error(e, "Failed to export hooks configuration")


@hooks.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--backup', is_flag=True, help='Create backup of current configuration')
def import_config(config_file: str, backup: bool):
    """
    Import hooks configuration from file.
    
    CONFIG_FILE: Path to hooks configuration file (JSON format)
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        if backup:
            # Create backup of current configuration
            backup_file = f"hooks_config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            _export_hooks_config(hook_manager, backup_file)
            console.print(f"[blue]Backup created: {backup_file}[/blue]")
        
        # Load new configuration
        _load_hooks_config(hook_manager, config_file)
        
        console.print(f"[green]✓ Hooks configuration imported from {config_file}[/green]")
        
    except Exception as e:
        handle_error(e, f"Failed to import hooks configuration from {config_file}")


@hooks.command()
@click.option('--hook', help='Test specific hook by name')
@click.option('--file', type=click.Path(exists=True), help='Test with specific file')
@click.option('--event', type=click.Choice(['file_modified', 'file_created', 'file_deleted']), 
              default='file_modified', help='Event type to simulate')
def test(hook: Optional[str], file: Optional[str], event: str):
    """
    Test hooks without file system monitoring.
    
    Simulates events to test hook configurations
    without actually monitoring the file system.
    """
    try:
        project_root = Path.cwd()
        hook_manager = create_agent_hook_manager(project_root)
        
        if file:
            test_file = Path(file)
        else:
            # Use a default test file
            test_file = project_root / "test_file.txt"
            test_file.touch()
        
        console.print(f"[blue]Testing hooks with event: {event}[/blue]")
        console.print(f"[blue]Test file: {test_file}[/blue]")
        
        # Create test event
        from src.core.agent_hooks import HookEvent
        test_event = HookEvent(
            event_type=event,
            file_path=str(test_file),
            timestamp=datetime.now(),
            metadata={"test": True},
            event_id="test_001"
        )
        
        # Find matching hooks
        matching_hooks = hook_manager._find_matching_hooks(test_event)
        
        if hook:
            # Test specific hook
            if hook in hook_manager.hooks:
                specific_hook = hook_manager.hooks[hook]
                if specific_hook in matching_hooks:
                    console.print(f"[green]✓ Hook '{hook}' would be triggered[/green]")
                    hook_manager._execute_hook_actions(specific_hook, test_event)
                else:
                    console.print(f"[yellow]⚠ Hook '{hook}' would not be triggered for this event[/yellow]")
            else:
                console.print(f"[red]✗ Hook '{hook}' not found[/red]")
        else:
            # Test all matching hooks
            if matching_hooks:
                console.print(f"[green]✓ {len(matching_hooks)} hook(s) would be triggered:[/green]")
                for hook_rule in matching_hooks:
                    console.print(f"  • {hook_rule.name}")
                    hook_manager._execute_hook_actions(hook_rule, test_event)
            else:
                console.print("[yellow]⚠ No hooks would be triggered for this event[/yellow]")
        
        # Clean up test file if we created it
        if not file and test_file.exists():
            test_file.unlink()
        
    except Exception as e:
        handle_error(e, "Failed to test hooks")


def _load_hooks_config(hook_manager: AgentHookManager, config_file: str):
    """Load hooks configuration from file."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    for hook_config in config.get('hooks', []):
        actions = [
            HookAction(
                action_type=action['action_type'],
                target=action['target'],
                parameters=action.get('parameters', {}),
                priority=action.get('priority', 0),
                max_retries=action.get('max_retries', 3)
            )
            for action in hook_config['actions']
        ]
        
        hook = HookRule(
            name=hook_config['name'],
            pattern=hook_config['pattern'],
            event_types=hook_config['event_types'],
            actions=actions,
            enabled=hook_config.get('enabled', True),
            conditions=hook_config.get('conditions')
        )
        
        hook_manager.add_hook(hook)


def _export_hooks_config(hook_manager: AgentHookManager, output_file: str):
    """Export hooks configuration to file."""
    config = {
        "hooks": [
            {
                "name": hook.name,
                "pattern": hook.pattern,
                "event_types": hook.event_types,
                "actions": [
                    {
                        "action_type": action.action_type,
                        "target": action.target,
                        "parameters": action.parameters,
                        "priority": action.priority,
                        "max_retries": action.max_retries
                    }
                    for action in hook.actions
                ],
                "enabled": hook.enabled,
                "conditions": hook.conditions
            }
            for hook in hook_manager.hooks.values()
        ],
        "exported_at": str(datetime.now()),
        "project_root": str(hook_manager.project_root)
    }
    
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
