#!/usr/bin/env python3
"""
MCP Integration Commands for DocGen CLI
Provides CLI commands for MCP server integration and management.

This module adds MCP-related commands to the DocGen CLI, allowing users
to interact with MCP servers, run workflows, and manage integration.

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import click
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Warning: Rich library not available. Install with: pip install rich")
    Console = None

# Import MCP Integration components
try:
    from assets.dev.scripts.mcp_integration import MCPIntegrationCore
    from assets.dev.scripts.enhanced_mcp_workflow import EnhancedMCPWorkflow
    from assets.dev.scripts.mcp_orchestrator import MCPOrchestrator
except ImportError:
    # Fallback for when MCP components are not available
    MCPIntegrationCore = None
    EnhancedMCPWorkflow = None
    MCPOrchestrator = None

# Configure logging
import logging
logger = logging.getLogger(__name__)

@click.group()
def mcp():
    """MCP (Model Context Protocol) integration commands for DocGen CLI."""
    pass

@mcp.command()
@click.option('--config-path', help='Path to MCP configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def status(config_path: str = None, verbose: bool = False):
    """Display MCP integration status and server information."""
    if not MCPIntegrationCore:
        click.echo("❌ MCP Integration Core not available. Please ensure MCP components are installed.")
        return
    
    try:
        # Initialize MCP Integration Core
        mcp_core = MCPIntegrationCore(config_path)
        
        # Display status
        if Console:
            console = Console()
            mcp_core.display_status()
        else:
            # Fallback to simple text output
            status = mcp_core.get_integration_status()
            click.echo(f"MCP Integration Status:")
            click.echo(f"  Servers Configured: {status['servers_configured']}")
            click.echo(f"  Servers Enabled: {status['servers_enabled']}")
            click.echo(f"  Total Calls: {status['total_calls']}")
            click.echo(f"  Success Rate: {status['success_rate']:.2%}")
            
            if verbose:
                click.echo(f"  Enabled Servers: {', '.join(status['enabled_servers'])}")
                click.echo(f"  Workflow Config: {status['workflow_config']}")
                click.echo(f"  Driven Workflow: {'Enabled' if status['driven_workflow_enabled'] else 'Disabled'}")
        
    except Exception as e:
        click.echo(f"❌ Error getting MCP status: {e}")
        if verbose:
            logger.exception("Error in MCP status command")

@mcp.command()
@click.option('--server', help='Specific MCP server to test')
@click.option('--function', help='Specific function to test')
@click.option('--args', help='Arguments to pass to the function (JSON format)')
@click.option('--config-path', help='Path to MCP configuration file')
def test(server: str = None, function: str = None, args: str = None, config_path: str = None):
    """Test MCP server connectivity and functionality."""
    if not MCPIntegrationCore:
        click.echo("❌ MCP Integration Core not available. Please ensure MCP components are installed.")
        return
    
    try:
        # Initialize MCP Integration Core
        mcp_core = MCPIntegrationCore(config_path)
        
        if server and function:
            # Test specific server and function
            click.echo(f"Testing {server}.{function}...")
            
            # Parse arguments if provided
            parsed_args = []
            if args:
                try:
                    parsed_args = json.loads(args)
                    if not isinstance(parsed_args, list):
                        parsed_args = [parsed_args]
                except json.JSONDecodeError:
                    click.echo("❌ Invalid JSON format for arguments")
                    return
            
            # Execute test call
            result = mcp_core.execute_mcp_call(server, function, *parsed_args)
            
            if result.success:
                click.echo(f"✅ {server}.{function} test successful")
                if Console:
                    console = Console()
                    console.print(f"Duration: {result.duration:.2f}s")
                    console.print(f"Data: {result.data}")
                else:
                    click.echo(f"  Duration: {result.duration:.2f}s")
                    click.echo(f"  Data: {result.data}")
            else:
                click.echo(f"❌ {server}.{function} test failed: {result.error}")
        else:
            # Test all enabled servers
            click.echo("Testing all enabled MCP servers...")
            
            enabled_servers = mcp_core.list_enabled_servers()
            test_results = {}
            
            for server_name in enabled_servers:
                click.echo(f"  Testing {server_name}...")
                
                # Test with a simple call
                result = mcp_core.execute_mcp_call(server_name, 'test_connection')
                test_results[server_name] = result.success
                
                if result.success:
                    click.echo(f"    ✅ {server_name} - OK")
                else:
                    click.echo(f"    ❌ {server_name} - Failed: {result.error}")
            
            # Display summary
            successful_tests = sum(1 for success in test_results.values() if success)
            total_tests = len(test_results)
            
            click.echo(f"\nTest Summary: {successful_tests}/{total_tests} servers successful")
        
    except Exception as e:
        click.echo(f"❌ Error testing MCP servers: {e}")
        logger.exception("Error in MCP test command")

@mcp.command()
@click.option('--phase', type=click.Choice(['1', '2', '3', '4', 'all']), default='all', 
              help='Specific phase to run (default: all)')
@click.option('--project-path', help='Path to DocGen CLI project')
@click.option('--config-path', help='Path to MCP configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def workflow(phase: str = 'all', project_path: str = None, config_path: str = None, verbose: bool = False):
    """Run Enhanced MCP Workflow for development."""
    if not EnhancedMCPWorkflow:
        click.echo("❌ Enhanced MCP Workflow not available. Please ensure MCP components are installed.")
        return
    
    try:
        # Initialize Enhanced MCP Workflow
        workflow = EnhancedMCPWorkflow(project_path, config_path)
        
        if phase == 'all':
            click.echo("Running complete Enhanced MCP Workflow...")
            results = workflow.execute_complete_workflow()
            
            if results.get('summary', {}).get('success_rate', 0) >= 0.8:
                click.echo("✅ Enhanced MCP Workflow completed successfully!")
            else:
                click.echo("⚠️ Enhanced MCP Workflow completed with some issues")
        else:
            phase_num = int(phase)
            click.echo(f"Running Phase {phase_num} of Enhanced MCP Workflow...")
            
            if phase_num == 1:
                results = workflow.phase_1_project_initialization()
            elif phase_num == 2:
                results = workflow.phase_2_active_development()
            elif phase_num == 3:
                results = workflow.phase_3_testing_validation()
            elif phase_num == 4:
                results = workflow.phase_4_documentation_knowledge()
            else:
                click.echo(f"❌ Invalid phase: {phase_num}")
                return
            
            # Check phase results
            phase_success = not any(comp.get('error') for comp in results.values())
            if phase_success:
                click.echo(f"✅ Phase {phase_num} completed successfully!")
            else:
                click.echo(f"⚠️ Phase {phase_num} completed with some issues")
        
        if verbose:
            click.echo(f"Results: {json.dumps(results, indent=2, default=str)}")
        
    except Exception as e:
        click.echo(f"❌ Error running MCP workflow: {e}")
        if verbose:
            logger.exception("Error in MCP workflow command")

@mcp.command()
@click.option('--calls', help='JSON file containing MCP calls to orchestrate')
@click.option('--max-workers', default=10, help='Maximum number of parallel workers')
@click.option('--config-path', help='Path to MCP configuration file')
@click.option('--export-report', is_flag=True, help='Export orchestration report')
def orchestrate(calls: str = None, max_workers: int = 10, config_path: str = None, export_report: bool = False):
    """Orchestrate multiple MCP calls with parallel execution."""
    if not MCPOrchestrator:
        click.echo("❌ MCP Orchestrator not available. Please ensure MCP components are installed.")
        return
    
    try:
        # Initialize MCP Orchestrator
        orchestrator = MCPOrchestrator(max_workers=max_workers)
        
        if calls:
            # Load calls from JSON file
            with open(calls, 'r') as f:
                calls_data = json.load(f)
            
            if not isinstance(calls_data, list):
                click.echo("❌ Calls file must contain a list of MCP calls")
                return
        else:
            # Use default test calls
            calls_data = [
                {
                    'server': 'byterover',
                    'function': 'retrieve_knowledge',
                    'args': ['DocGen CLI orchestration test'],
                    'priority': 1
                },
                {
                    'server': 'context7',
                    'function': 'resolve_library_id',
                    'args': ['click'],
                    'priority': 2
                },
                {
                    'server': 'browser_tools',
                    'function': 'runAccessibilityAudit',
                    'priority': 3
                }
            ]
        
        click.echo(f"Orchestrating {len(calls_data)} MCP calls...")
        
        # Execute orchestration
        result = orchestrator.orchestrate_calls(calls_data)
        
        # Display results
        if result.calls_successful == result.calls_executed:
            click.echo("✅ All MCP calls executed successfully!")
        else:
            click.echo(f"⚠️ {result.calls_successful}/{result.calls_executed} MCP calls successful")
        
        click.echo(f"  Total Duration: {result.total_duration:.2f}s")
        click.echo(f"  Parallel Efficiency: {result.parallel_efficiency:.2f}x")
        
        if Console:
            console = Console()
            orchestrator.display_orchestration_status()
        
        # Export report if requested
        if export_report:
            report_path = orchestrator.export_orchestration_report()
            click.echo(f"📊 Orchestration report exported to: {report_path}")
        
    except Exception as e:
        click.echo(f"❌ Error orchestrating MCP calls: {e}")
        logger.exception("Error in MCP orchestrate command")

@mcp.command()
@click.option('--component', type=click.Choice(['core', 'workflow', 'orchestrator', 'tests', 'validation', 'all']), 
              default='all', help='Component to run (default: all)')
@click.option('--project-path', help='Path to DocGen CLI project')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def run(component: str = 'all', project_path: str = None, verbose: bool = False):
    """Run MCP Integration Runner for automated execution."""
    try:
        # Import and run the MCP Integration Runner
        import subprocess
        import sys
        
        runner_script = os.path.join(
            os.path.dirname(__file__), '..', '..', 'assets', 'dev', 'scripts', 'run_mcp_integration.py'
        )
        
        if not os.path.exists(runner_script):
            click.echo("❌ MCP Integration Runner script not found")
            return
        
        # Prepare command
        cmd = [sys.executable, runner_script, '--component', component]
        if project_path:
            cmd.extend(['--project-path', project_path])
        if verbose:
            cmd.append('--verbose')
        
        click.echo(f"Running MCP Integration Runner: {component}")
        
        # Execute runner
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Display output
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr)
        
        if result.returncode == 0:
            click.echo("✅ MCP Integration Runner completed successfully!")
        else:
            click.echo("❌ MCP Integration Runner completed with errors")
        
    except Exception as e:
        click.echo(f"❌ Error running MCP Integration Runner: {e}")
        if verbose:
            logger.exception("Error in MCP run command")

@mcp.command()
@click.option('--server', help='Specific MCP server to configure')
@click.option('--enable/--disable', help='Enable or disable MCP server')
@click.option('--timeout', type=int, help='Set timeout for MCP server')
@click.option('--retry-attempts', type=int, help='Set retry attempts for MCP server')
@click.option('--config-path', help='Path to MCP configuration file')
def config(server: str = None, enable: bool = None, timeout: int = None, 
           retry_attempts: int = None, config_path: str = None):
    """Configure MCP server settings."""
    if not MCPIntegrationCore:
        click.echo("❌ MCP Integration Core not available. Please ensure MCP components are installed.")
        return
    
    try:
        # Initialize MCP Integration Core
        mcp_core = MCPIntegrationCore(config_path)
        
        if server:
            # Configure specific server
            server_config = mcp_core.get_server_config(server)
            if not server_config:
                click.echo(f"❌ Server '{server}' not found")
                return
            
            # Update configuration
            if enable is not None:
                server_config.enabled = enable
                click.echo(f"{'Enabled' if enable else 'Disabled'} server: {server}")
            
            if timeout is not None:
                server_config.timeout = timeout
                click.echo(f"Set timeout for {server}: {timeout}s")
            
            if retry_attempts is not None:
                server_config.retry_attempts = retry_attempts
                click.echo(f"Set retry attempts for {server}: {retry_attempts}")
            
            # Note: In a real implementation, this would save the configuration
            click.echo("⚠️ Configuration changes are not persisted in this demo")
        else:
            # Display current configuration
            click.echo("Current MCP Server Configuration:")
            
            if Console:
                console = Console()
                table = Table()
                table.add_column("Server", style="cyan")
                table.add_column("Enabled", style="green")
                table.add_column("Timeout", style="yellow")
                table.add_column("Retry Attempts", style="blue")
                
                for server_name, config in mcp_core.servers.items():
                    table.add_row(
                        server_name,
                        "✅" if config.enabled else "❌",
                        f"{config.timeout}s",
                        str(config.retry_attempts)
                    )
                
                console.print(table)
            else:
                for server_name, config in mcp_core.servers.items():
                    status = "Enabled" if config.enabled else "Disabled"
                    click.echo(f"  {server_name}: {status}, timeout={config.timeout}s, retries={config.retry_attempts}")
        
    except Exception as e:
        click.echo(f"❌ Error configuring MCP servers: {e}")
        logger.exception("Error in MCP config command")

@mcp.command()
@click.option('--output', '-o', help='Output file for the report')
@click.option('--format', type=click.Choice(['json', 'yaml']), default='json', help='Report format')
@click.option('--config-path', help='Path to MCP configuration file')
def report(output: str = None, format: str = 'json', config_path: str = None):
    """Generate MCP integration report."""
    if not MCPIntegrationCore:
        click.echo("❌ MCP Integration Core not available. Please ensure MCP components are installed.")
        return
    
    try:
        # Initialize MCP Integration Core
        mcp_core = MCPIntegrationCore(config_path)
        
        # Generate report data
        report_data = {
            'timestamp': str(datetime.now()),
            'integration_status': mcp_core.get_integration_status(),
            'performance_metrics': mcp_core.get_performance_metrics(),
            'results': [result.__dict__ for result in mcp_core.results]
        }
        
        # Determine output file
        if not output:
            output = f"mcp_integration_report.{format}"
        
        # Write report
        with open(output, 'w') as f:
            if format == 'json':
                json.dump(report_data, f, indent=2, default=str)
            else:  # yaml
                import yaml
                yaml.dump(report_data, f, default_flow_style=False, indent=2)
        
        click.echo(f"📊 MCP integration report generated: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error generating MCP report: {e}")
        logger.exception("Error in MCP report command")

if __name__ == '__main__':
    mcp()
