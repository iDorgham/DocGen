#!/usr/bin/env python3
"""
Complete MCP Integration Runner for DocGen CLI
Orchestrates the complete MCP integration workflow with authentication and testing.

This script provides a comprehensive runner that:
- Sets up authentication for all MCP servers
- Executes enhanced MCP workflows
- Runs comprehensive testing and validation
- Generates detailed reports and documentation
- Provides error recovery and fallback mechanisms

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import yaml
import click
import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.logging import RichHandler
except ImportError:
    print("Warning: Rich library not available. Install with: pip install rich")
    Console = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler()] if Console else [logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class CompleteMCPIntegrationRunner:
    """
    Complete MCP Integration Runner for DocGen CLI.
    
    Orchestrates the complete MCP integration workflow including authentication,
    enhanced workflows, testing, and reporting.
    """
    
    def __init__(self, project_path: str = None):
        """
        Initialize Complete MCP Integration Runner.
        
        Args:
            project_path: Path to the DocGen CLI project
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.scripts_path = os.path.join(self.project_path, 'assets', 'dev', 'scripts')
        self.reports_path = os.path.join(self.project_path, 'assets', 'reports', 'mcp')
        
        # Ensure reports directory exists
        os.makedirs(self.reports_path, exist_ok=True)
        
        # Integration results tracking
        self.integration_results = {}
        self.performance_metrics = {}
        self.error_log = []
        
        logger.info("Complete MCP Integration Runner initialized")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def _run_script(self, script_name: str, args: List[str] = None, timeout: int = 300) -> Dict[str, Any]:
        """
        Run a Python script and capture results.
        
        Args:
            script_name: Name of the script to run
            args: Additional arguments to pass
            timeout: Timeout in seconds
            
        Returns:
            Dictionary with execution results
        """
        script_path = os.path.join(self.scripts_path, script_name)
        
        if not os.path.exists(script_path):
            return {
                'success': False,
                'error': f"Script not found: {script_path}",
                'duration': 0.0
            }
        
        # Prepare command
        cmd = ['python3', script_path]
        if args:
            cmd.extend(args)
        
        logger.info(f"Running script: {script_name}")
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': duration,
                'script': script_name
            }
            
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            return {
                'success': False,
                'error': f"Script timed out after {duration:.2f} seconds",
                'duration': duration,
                'script': script_name
            }
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return {
                'success': False,
                'error': f"Error running script: {str(e)}",
                'duration': duration,
                'script': script_name
            }
    
    def step_1_authentication_setup(self) -> Dict[str, Any]:
        """Step 1: Set up authentication for all MCP servers."""
        logger.info("Step 1: Setting up MCP authentication...")
        
        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Setting up authentication...", total=100)
                
                # Run authentication setup
                result = self._run_script('mcp_authentication_setup.py', ['--verbose'])
                
                progress.update(task, completed=100)
        else:
            result = self._run_script('mcp_authentication_setup.py', ['--verbose'])
        
        self.integration_results['authentication_setup'] = result
        
        if result['success']:
            logger.info("✅ Authentication setup completed successfully")
        else:
            logger.error(f"❌ Authentication setup failed: {result.get('error', 'Unknown error')}")
            self.error_log.append(f"Authentication setup failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def step_2_enhanced_integration(self) -> Dict[str, Any]:
        """Step 2: Run enhanced MCP integration workflow."""
        logger.info("Step 2: Running enhanced MCP integration...")
        
        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Running enhanced integration...", total=100)
                
                # Run enhanced integration
                result = self._run_script('enhanced_mcp_integration.py')
                
                progress.update(task, completed=100)
        else:
            result = self._run_script('enhanced_mcp_integration.py')
        
        self.integration_results['enhanced_integration'] = result
        
        if result['success']:
            logger.info("✅ Enhanced MCP integration completed successfully")
        else:
            logger.error(f"❌ Enhanced MCP integration failed: {result.get('error', 'Unknown error')}")
            self.error_log.append(f"Enhanced integration failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def step_3_comprehensive_testing(self) -> Dict[str, Any]:
        """Step 3: Run comprehensive MCP integration testing."""
        logger.info("Step 3: Running comprehensive testing...")
        
        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Running comprehensive tests...", total=100)
                
                # Run comprehensive testing
                result = self._run_script('test_mcp_integration.py')
                
                progress.update(task, completed=100)
        else:
            result = self._run_script('test_mcp_integration.py')
        
        self.integration_results['comprehensive_testing'] = result
        
        if result['success']:
            logger.info("✅ Comprehensive testing completed successfully")
        else:
            logger.error(f"❌ Comprehensive testing failed: {result.get('error', 'Unknown error')}")
            self.error_log.append(f"Comprehensive testing failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def step_4_quality_validation(self) -> Dict[str, Any]:
        """Step 4: Run quality validation and audits."""
        logger.info("Step 4: Running quality validation...")
        
        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Running quality validation...", total=100)
                
                # Run quality checks
                result = self._run_script('run_quality_checks.py')
                
                progress.update(task, completed=100)
        else:
            result = self._run_script('run_quality_checks.py')
        
        self.integration_results['quality_validation'] = result
        
        if result['success']:
            logger.info("✅ Quality validation completed successfully")
        else:
            logger.error(f"❌ Quality validation failed: {result.get('error', 'Unknown error')}")
            self.error_log.append(f"Quality validation failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def step_5_documentation_generation(self) -> Dict[str, Any]:
        """Step 5: Generate comprehensive documentation."""
        logger.info("Step 5: Generating documentation...")
        
        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Generating documentation...", total=100)
                
                # Generate documentation
                result = self._run_script('generate_docs.py')
                
                progress.update(task, completed=100)
        else:
            result = self._run_script('generate_docs.py')
        
        self.integration_results['documentation_generation'] = result
        
        if result['success']:
            logger.info("✅ Documentation generation completed successfully")
        else:
            logger.error(f"❌ Documentation generation failed: {result.get('error', 'Unknown error')}")
            self.error_log.append(f"Documentation generation failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def run_complete_integration(self) -> Dict[str, Any]:
        """Run the complete MCP integration workflow."""
        logger.info("Starting complete MCP integration workflow...")
        start_time = datetime.now()
        
        try:
            # Execute all steps
            step_1_result = self.step_1_authentication_setup()
            step_2_result = self.step_2_enhanced_integration()
            step_3_result = self.step_3_comprehensive_testing()
            step_4_result = self.step_4_quality_validation()
            step_5_result = self.step_5_documentation_generation()
            
            # Calculate overall results
            total_duration = (datetime.now() - start_time).total_seconds()
            successful_steps = sum(1 for result in [
                step_1_result, step_2_result, step_3_result, step_4_result, step_5_result
            ] if result.get('success', False))
            total_steps = 5
            success_rate = successful_steps / total_steps
            
            # Calculate performance metrics
            total_script_duration = sum(
                result.get('duration', 0) for result in self.integration_results.values()
            )
            
            self.performance_metrics = {
                'total_duration': total_duration,
                'script_duration': total_script_duration,
                'overhead_duration': total_duration - total_script_duration,
                'successful_steps': successful_steps,
                'total_steps': total_steps,
                'success_rate': success_rate,
                'error_count': len(self.error_log)
            }
            
            integration_summary = {
                'success': success_rate >= 0.8,  # 80% success rate threshold
                'success_rate': success_rate,
                'total_duration': total_duration,
                'successful_steps': successful_steps,
                'total_steps': total_steps,
                'steps': {
                    'authentication_setup': step_1_result,
                    'enhanced_integration': step_2_result,
                    'comprehensive_testing': step_3_result,
                    'quality_validation': step_4_result,
                    'documentation_generation': step_5_result
                },
                'performance_metrics': self.performance_metrics,
                'errors': self.error_log,
                'integration_results': self.integration_results
            }
            
            logger.info(f"Complete integration finished: {success_rate:.2%} success rate")
            return integration_summary
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_msg = f"Error in complete integration execution: {str(e)}"
            logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'total_duration': duration,
                'success_rate': 0.0
            }
    
    def display_integration_summary(self, summary: Dict[str, Any]):
        """Display integration summary in a formatted table."""
        if not self.console:
            # Fallback to simple text output
            print(f"\nComplete MCP Integration Summary:")
            print(f"  Success Rate: {summary.get('success_rate', 0):.2%}")
            print(f"  Total Duration: {summary.get('total_duration', 0):.2f}s")
            print(f"  Successful Steps: {summary.get('successful_steps', 0)}/{summary.get('total_steps', 0)}")
            print(f"  Errors: {len(summary.get('errors', []))}")
            return
        
        # Create integration summary table
        table = Table(title="Complete MCP Integration Summary")
        table.add_column("Step", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Duration", style="yellow")
        table.add_column("Details", style="blue")
        
        steps = summary.get('steps', {})
        for step_name, step_result in steps.items():
            status = "✅ Success" if step_result.get('success', False) else "❌ Failed"
            duration = step_result.get('duration', 0.0)
            details = step_result.get('script', step_name)
            
            table.add_row(
                step_name.replace('_', ' ').title(),
                status,
                f"{duration:.2f}s",
                details
            )
        
        self.console.print(table)
        
        # Display overall metrics
        metrics = summary.get('performance_metrics', {})
        metrics_panel = Panel(
            f"Success Rate: {summary.get('success_rate', 0):.2%}\n"
            f"Total Duration: {summary.get('total_duration', 0):.2f}s\n"
            f"Successful Steps: {summary.get('successful_steps', 0)}/{summary.get('total_steps', 0)}\n"
            f"Script Duration: {metrics.get('script_duration', 0):.2f}s\n"
            f"Overhead Duration: {metrics.get('overhead_duration', 0):.2f}s\n"
            f"Error Count: {len(summary.get('errors', []))}",
            title="Performance Metrics",
            border_style="green" if summary.get('success', False) else "red"
        )
        self.console.print(metrics_panel)
    
    def export_integration_report(self, summary: Dict[str, Any]) -> str:
        """Export complete integration report to JSON file."""
        report_path = os.path.join(self.reports_path, 'complete_mcp_integration_report.json')
        
        # Prepare report data
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'project_path': self.project_path,
            'integration_summary': summary,
            'performance_metrics': self.performance_metrics,
            'error_log': self.error_log,
            'integration_results': self.integration_results
        }
        
        # Write to file
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Complete integration report exported to: {report_path}")
        return report_path

@click.command()
@click.option('--project-path', help='Path to DocGen CLI project')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--skip-auth', is_flag=True, help='Skip authentication setup')
@click.option('--skip-tests', is_flag=True, help='Skip comprehensive testing')
@click.option('--export-report', is_flag=True, help='Export detailed report')
def main(project_path: str = None, verbose: bool = False, skip_auth: bool = False, 
         skip_tests: bool = False, export_report: bool = False):
    """Run complete MCP integration workflow."""
    try:
        # Initialize runner
        runner = CompleteMCPIntegrationRunner(project_path)
        
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Run complete integration
        summary = runner.run_complete_integration()
        
        # Display summary
        runner.display_integration_summary(summary)
        
        # Export report if requested
        if export_report:
            report_path = runner.export_integration_report(summary)
            print(f"\n📊 Detailed report exported to: {report_path}")
        
        # Display final status
        if summary.get('success', False):
            print("\n🎉 Complete MCP Integration completed successfully!")
            print(f"   Success Rate: {summary.get('success_rate', 0):.2%}")
            print(f"   Duration: {summary.get('total_duration', 0):.2f}s")
            print("   All MCP servers are now integrated and ready for use!")
        else:
            print("\n⚠️ Complete MCP Integration completed with issues")
            print(f"   Success Rate: {summary.get('success_rate', 0):.2%}")
            if summary.get('errors'):
                print("   Errors encountered:")
                for error in summary['errors']:
                    print(f"     - {error}")
            print("   Please review the errors and retry the integration")
        
        return 0 if summary.get('success', False) else 1
        
    except Exception as e:
        logger.error(f"Error in Complete MCP Integration Runner: {e}")
        return 1

if __name__ == "__main__":
    exit(main())