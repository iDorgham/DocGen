#!/usr/bin/env python3
"""
MCP Integration Test Suite for DocGen CLI
Comprehensive testing of all MCP integration components.

This script tests the complete MCP integration implementation including:
- MCP Integration Core functionality
- Enhanced MCP Workflow execution
- MCP Orchestrator parallel execution
- CLI command integration
- Error handling and recovery

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import time
import json
import subprocess
import logging
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

class MCPIntegrationTestSuite:
    """
    Comprehensive test suite for MCP integration components.
    
    Tests all aspects of the MCP integration including:
    - Core functionality
    - Workflow execution
    - Orchestration
    - CLI integration
    - Error handling
    """
    
    def __init__(self, project_path: str = None):
        """
        Initialize MCP Integration Test Suite.
        
        Args:
            project_path: Path to the DocGen CLI project
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.test_results = {}
        self.test_durations = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        logger.info("MCP Integration Test Suite initialized")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        # Navigate up from assets/dev/scripts to project root
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def _display_test_header(self, test_name: str):
        """Display test header with rich formatting."""
        if self.console:
            panel = Panel(
                f"[bold blue]{test_name}[/bold blue]\n"
                f"[dim]MCP Integration Test Suite[/dim]",
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(panel)
        else:
            print(f"\n{'='*60}")
            print(f"{test_name}")
            print('='*60)
    
    def _display_test_result(self, test_name: str, success: bool, duration: float, details: str = ""):
        """Display test result."""
        if self.console:
            status = "✅ PASSED" if success else "❌ FAILED"
            color = "green" if success else "red"
            
            panel = Panel(
                f"Status: [bold {color}]{status}[/bold {color}]\n"
                f"Duration: {duration:.2f} seconds\n"
                f"Details: {details}",
                title=f"{test_name} Result",
                border_style=color
            )
            self.console.print(panel)
        else:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"\n{test_name} Result:")
            print(f"  Status: {status}")
            print(f"  Duration: {duration:.2f} seconds")
            print(f"  Details: {details}")
    
    def _run_script_test(self, script_name: str, test_name: str) -> Dict[str, Any]:
        """
        Run a script and capture test results.
        
        Args:
            script_name: Name of the script to test
            test_name: Name of the test
            
        Returns:
            Dictionary with test results
        """
        script_path = os.path.join(self.project_path, 'assets', 'dev', 'scripts', script_name)
        
        if not os.path.exists(script_path):
            return {
                'success': False,
                'error': f"Script not found: {script_path}",
                'duration': 0.0
            }
        
        logger.info(f"Running test: {test_name}")
        start_time = time.time()
        
        try:
            # Run the script
            result = subprocess.run(
                ['python3', script_path],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )
            
            duration = time.time() - start_time
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': duration
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                'success': False,
                'error': f"Script timed out after {duration:.2f} seconds",
                'duration': duration
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'success': False,
                'error': f"Error running script: {str(e)}",
                'duration': duration
            }
    
    def test_mcp_integration_core(self) -> Dict[str, Any]:
        """Test MCP Integration Core functionality."""
        self._display_test_header("Testing MCP Integration Core")
        
        result = self._run_script_test('mcp_integration.py', 'MCP Integration Core')
        
        self.test_results['mcp_integration_core'] = result
        self.test_durations['mcp_integration_core'] = result['duration']
        self.total_tests += 1
        
        if result['success']:
            self.passed_tests += 1
            details = "Core MCP integration functionality working correctly"
        else:
            self.failed_tests += 1
            details = f"Core test failed: {result.get('error', 'Unknown error')}"
        
        self._display_test_result("MCP Integration Core", result['success'], result['duration'], details)
        return result
    
    def test_enhanced_workflow(self) -> Dict[str, Any]:
        """Test Enhanced MCP Workflow execution."""
        self._display_test_header("Testing Enhanced MCP Workflow")
        
        result = self._run_script_test('enhanced_mcp_workflow.py', 'Enhanced MCP Workflow')
        
        self.test_results['enhanced_workflow'] = result
        self.test_durations['enhanced_workflow'] = result['duration']
        self.total_tests += 1
        
        if result['success']:
            self.passed_tests += 1
            details = "4-phase development workflow executed successfully"
        else:
            self.failed_tests += 1
            details = f"Workflow test failed: {result.get('error', 'Unknown error')}"
        
        self._display_test_result("Enhanced MCP Workflow", result['success'], result['duration'], details)
        return result
    
    def test_mcp_orchestrator(self) -> Dict[str, Any]:
        """Test MCP Orchestrator parallel execution."""
        self._display_test_header("Testing MCP Orchestrator")
        
        result = self._run_script_test('mcp_orchestrator.py', 'MCP Orchestrator')
        
        self.test_results['mcp_orchestrator'] = result
        self.test_durations['mcp_orchestrator'] = result['duration']
        self.total_tests += 1
        
        if result['success']:
            self.passed_tests += 1
            details = "Parallel execution and optimization working correctly"
        else:
            self.failed_tests += 1
            details = f"Orchestrator test failed: {result.get('error', 'Unknown error')}"
        
        self._display_test_result("MCP Orchestrator", result['success'], result['duration'], details)
        return result
    
    def test_mcp_integration_runner(self) -> Dict[str, Any]:
        """Test MCP Integration Runner."""
        self._display_test_header("Testing MCP Integration Runner")
        
        result = self._run_script_test('run_mcp_integration.py', 'MCP Integration Runner')
        
        self.test_results['mcp_integration_runner'] = result
        self.test_durations['mcp_integration_runner'] = result['duration']
        self.total_tests += 1
        
        if result['success']:
            self.passed_tests += 1
            details = "Automated execution system working correctly"
        else:
            self.failed_tests += 1
            details = f"Integration runner test failed: {result.get('error', 'Unknown error')}"
        
        self._display_test_result("MCP Integration Runner", result['success'], result['duration'], details)
        return result
    
    def test_cli_integration(self) -> Dict[str, Any]:
        """Test CLI command integration."""
        self._display_test_header("Testing CLI Integration")
        
        # Test CLI commands
        cli_tests = [
            {
                'command': ['python3', 'docgen_cli.py', 'help'],
                'name': 'CLI Help Command',
                'expected_success': True
            },
            {
                'command': ['python3', 'docgen_cli.py', 'validate'],
                'name': 'CLI Validate Command',
                'expected_success': True
            }
        ]
        
        cli_results = []
        total_duration = 0.0
        
        for test in cli_tests:
            logger.info(f"Testing CLI: {test['name']}")
            start_time = time.time()
            
            try:
                result = subprocess.run(
                    test['command'],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                duration = time.time() - start_time
                total_duration += duration
                
                success = result.returncode == 0
                cli_results.append({
                    'name': test['name'],
                    'success': success,
                    'duration': duration,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                })
                
                if success:
                    logger.info(f"✅ {test['name']} - PASSED")
                else:
                    logger.error(f"❌ {test['name']} - FAILED")
                
            except Exception as e:
                duration = time.time() - start_time
                total_duration += duration
                cli_results.append({
                    'name': test['name'],
                    'success': False,
                    'duration': duration,
                    'error': str(e)
                })
                logger.error(f"❌ {test['name']} - ERROR: {e}")
        
        # Calculate overall CLI test result
        successful_cli_tests = sum(1 for r in cli_results if r['success'])
        total_cli_tests = len(cli_results)
        cli_success = successful_cli_tests == total_cli_tests
        
        result = {
            'success': cli_success,
            'cli_results': cli_results,
            'successful_tests': successful_cli_tests,
            'total_tests': total_cli_tests,
            'duration': total_duration
        }
        
        self.test_results['cli_integration'] = result
        self.test_durations['cli_integration'] = total_duration
        self.total_tests += 1
        
        if cli_success:
            self.passed_tests += 1
            details = f"All {total_cli_tests} CLI commands working correctly"
        else:
            self.failed_tests += 1
            details = f"{successful_cli_tests}/{total_cli_tests} CLI commands successful"
        
        self._display_test_result("CLI Integration", cli_success, total_duration, details)
        return result
    
    def test_file_structure(self) -> Dict[str, Any]:
        """Test MCP integration file structure."""
        self._display_test_header("Testing File Structure")
        
        required_files = [
            'assets/dev/config/mcp/mcp_config.yaml',
            'assets/dev/scripts/mcp_integration.py',
            'assets/dev/scripts/enhanced_mcp_workflow.py',
            'assets/dev/scripts/mcp_orchestrator.py',
            'assets/dev/scripts/run_mcp_integration.py',
            'src/commands/mcp.py'
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in required_files:
            full_path = os.path.join(self.project_path, file_path)
            if os.path.exists(full_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        success = len(missing_files) == 0
        duration = 0.1  # File check is very fast
        
        result = {
            'success': success,
            'existing_files': existing_files,
            'missing_files': missing_files,
            'total_files': len(required_files),
            'existing_count': len(existing_files),
            'missing_count': len(missing_files),
            'duration': duration
        }
        
        self.test_results['file_structure'] = result
        self.test_durations['file_structure'] = duration
        self.total_tests += 1
        
        if success:
            self.passed_tests += 1
            details = f"All {len(required_files)} required files present"
        else:
            self.failed_tests += 1
            details = f"{len(missing_files)} files missing: {', '.join(missing_files)}"
        
        self._display_test_result("File Structure", success, duration, details)
        return result
    
    def test_configuration(self) -> Dict[str, Any]:
        """Test MCP configuration."""
        self._display_test_header("Testing Configuration")
        
        config_path = os.path.join(self.project_path, 'assets', 'dev', 'config', 'mcp', 'mcp_config.yaml')
        
        if not os.path.exists(config_path):
            result = {
                'success': False,
                'error': 'Configuration file not found',
                'duration': 0.1
            }
        else:
            try:
                import yaml
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                # Check required configuration sections
                required_sections = ['servers', 'workflow', 'driven_workflow']
                missing_sections = [section for section in required_sections if section not in config]
                
                # Check server configurations
                servers = config.get('servers', {})
                required_servers = ['byterover', 'context7', 'testsprite', 'browser_tools', 'playwright', 'dart']
                missing_servers = [server for server in required_servers if server not in servers]
                
                success = len(missing_sections) == 0 and len(missing_servers) == 0
                
                result = {
                    'success': success,
                    'config_sections': list(config.keys()),
                    'missing_sections': missing_sections,
                    'servers_configured': list(servers.keys()),
                    'missing_servers': missing_servers,
                    'duration': 0.1
                }
                
            except Exception as e:
                result = {
                    'success': False,
                    'error': f'Configuration parsing failed: {str(e)}',
                    'duration': 0.1
                }
        
        self.test_results['configuration'] = result
        self.test_durations['configuration'] = result['duration']
        self.total_tests += 1
        
        if result['success']:
            self.passed_tests += 1
            details = "Configuration file valid and complete"
        else:
            self.failed_tests += 1
            details = f"Configuration test failed: {result.get('error', 'Unknown error')}"
        
        self._display_test_result("Configuration", result['success'], result['duration'], details)
        return result
    
    def run_complete_test_suite(self) -> Dict[str, Any]:
        """Run the complete MCP integration test suite."""
        self._display_test_header("MCP Integration Test Suite")
        
        start_time = time.time()
        
        try:
            # Run all tests
            logger.info("Starting complete MCP integration test suite...")
            
            # 1. File structure test
            self.test_file_structure()
            
            # 2. Configuration test
            self.test_configuration()
            
            # 3. MCP Integration Core test
            self.test_mcp_integration_core()
            
            # 4. Enhanced Workflow test
            self.test_enhanced_workflow()
            
            # 5. MCP Orchestrator test
            self.test_mcp_orchestrator()
            
            # 6. MCP Integration Runner test
            self.test_mcp_integration_runner()
            
            # 7. CLI Integration test
            self.test_cli_integration()
            
            # Calculate overall results
            total_duration = time.time() - start_time
            success_rate = self.passed_tests / self.total_tests if self.total_tests > 0 else 0
            
            overall_result = {
                'success': self.failed_tests == 0,
                'total_tests': self.total_tests,
                'passed_tests': self.passed_tests,
                'failed_tests': self.failed_tests,
                'success_rate': success_rate,
                'total_duration': total_duration,
                'test_results': self.test_results,
                'test_durations': self.test_durations
            }
            
            # Display final summary
            self._display_final_summary(overall_result)
            
            # Export test report
            self._export_test_report(overall_result)
            
            logger.info("MCP Integration Test Suite completed")
            return overall_result
            
        except Exception as e:
            logger.error(f"Error in test suite execution: {e}")
            return {
                'success': False,
                'error': str(e),
                'total_duration': time.time() - start_time
            }
    
    def _display_final_summary(self, result: Dict[str, Any]):
        """Display final test summary."""
        if not self.console:
            print(f"\n{'='*60}")
            print("MCP INTEGRATION TEST SUMMARY")
            print('='*60)
            print(f"Total Tests: {result['total_tests']}")
            print(f"Passed: {result['passed_tests']}")
            print(f"Failed: {result['failed_tests']}")
            print(f"Success Rate: {result['success_rate']:.2%}")
            print(f"Total Duration: {result['total_duration']:.2f} seconds")
            return
        
        # Create summary table
        table = Table(title="MCP Integration Test Summary")
        table.add_column("Test", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Duration", style="yellow")
        
        for test_name, test_result in result['test_results'].items():
            status = "✅ PASSED" if test_result.get('success', False) else "❌ FAILED"
            duration = test_result.get('duration', 0.0)
            table.add_row(
                test_name.replace('_', ' ').title(),
                status,
                f"{duration:.2f}s"
            )
        
        self.console.print(table)
        
        # Display overall metrics
        metrics_panel = Panel(
            f"Total Tests: {result['total_tests']}\n"
            f"Passed: {result['passed_tests']}\n"
            f"Failed: {result['failed_tests']}\n"
            f"Success Rate: {result['success_rate']:.2%}\n"
            f"Total Duration: {result['total_duration']:.2f} seconds",
            title="Overall Metrics",
            border_style="green" if result['success'] else "red"
        )
        self.console.print(metrics_panel)
    
    def _export_test_report(self, result: Dict[str, Any]):
        """Export test report to JSON file."""
        reports_dir = os.path.join(self.project_path, 'assets', 'reports', 'mcp')
        os.makedirs(reports_dir, exist_ok=True)
        
        report_path = os.path.join(reports_dir, 'mcp_integration_test_report.json')
        
        # Prepare report data
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'project_path': self.project_path,
            'test_summary': result,
            'test_results': result.get('test_results', {}),
            'test_durations': result.get('test_durations', {})
        }
        
        # Write to file
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Test report exported to: {report_path}")
        return report_path

def main():
    """Main function for MCP Integration Test Suite."""
    try:
        # Initialize test suite
        test_suite = MCPIntegrationTestSuite()
        
        # Run complete test suite
        results = test_suite.run_complete_test_suite()
        
        # Return appropriate exit code
        return 0 if results.get('success', False) else 1
        
    except Exception as e:
        logger.error(f"Error in MCP Integration Test Suite: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
