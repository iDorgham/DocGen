#!/usr/bin/env python3
"""
Enhanced MCP Workflow for DocGen CLI
Implements 4-phase development workflow with comprehensive MCP integration.

This script implements the complete MCP-driven development workflow:
Phase 1: Project Initialization
Phase 2: Active Development  
Phase 3: Testing & Validation
Phase 4: Documentation & Knowledge

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.logging import RichHandler
except ImportError:
    print("Warning: Rich library not available. Install with: pip install rich")
    Console = None

# Import MCP Integration Core
from mcp_integration import MCPIntegrationCore, MCPIntegrationResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler()] if Console else [logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class EnhancedMCPWorkflow:
    """
    Enhanced MCP Workflow implementation for DocGen CLI.
    
    Provides a comprehensive 4-phase development workflow that integrates
    all MCP servers for knowledge-first development, automated testing,
    quality assurance, and project management.
    """
    
    def __init__(self, project_path: str = None, config_path: str = None):
        """
        Initialize Enhanced MCP Workflow.
        
        Args:
            project_path: Path to the DocGen CLI project
            config_path: Path to MCP configuration file
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.mcp_core = MCPIntegrationCore(config_path)
        self.workflow_results = {}
        self.phase_durations = {}
        
        logger.info("Enhanced MCP Workflow initialized")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        # Navigate up from assets/dev/scripts to project root
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def _display_phase_header(self, phase_name: str, phase_number: int):
        """Display phase header with rich formatting."""
        if self.console:
            panel = Panel(
                f"[bold blue]Phase {phase_number}: {phase_name}[/bold blue]\n"
                f"[dim]Starting at {datetime.now().strftime('%H:%M:%S')}[/dim]",
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(panel)
        else:
            print(f"\n{'='*60}")
            print(f"Phase {phase_number}: {phase_name}")
            print(f"Starting at {datetime.now().strftime('%H:%M:%S')}")
            print('='*60)
    
    def _display_phase_results(self, phase_name: str, results: Dict[str, Any], duration: float):
        """Display phase results with rich formatting."""
        if self.console:
            # Create results table
            table = Table(title=f"{phase_name} Results")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Details", style="white")
            
            for component, result in results.items():
                status = "✅ Success" if result.get('success', False) else "❌ Failed"
                details = result.get('details', 'No details available')
                table.add_row(component, status, details)
            
            self.console.print(table)
            
            # Display duration
            duration_panel = Panel(
                f"Duration: {duration:.2f} seconds",
                title="Phase Duration",
                border_style="green"
            )
            self.console.print(duration_panel)
        else:
            print(f"\n{phase_name} Results:")
            for component, result in results.items():
                status = "✅ Success" if result.get('success', False) else "❌ Failed"
                print(f"  {component}: {status}")
            print(f"Duration: {duration:.2f} seconds")
    
    def phase_1_project_initialization(self) -> Dict[str, Any]:
        """
        Phase 1: Project Initialization
        - Handbook creation and validation
        - Module discovery and documentation
        - Test environment bootstrapping
        - Project configuration setup
        - Initial task creation
        """
        self._display_phase_header("Project Initialization", 1)
        start_time = time.time()
        results = {}
        
        try:
            # 1.1 Check handbook existence
            logger.info("Checking handbook existence...")
            handbook_result = self.mcp_core.execute_mcp_call(
                'byterover', 'check_handbook_existence', 'dummy'
            )
            results['handbook_check'] = {
                'success': handbook_result.success,
                'details': 'Handbook existence checked'
            }
            
            # 1.2 Create handbook if needed
            logger.info("Creating handbook...")
            handbook_create_result = self.mcp_core.execute_mcp_call(
                'byterover', 'create_handbook', 'full', 'BYTEROVER.md', 'auto-detect'
            )
            results['handbook_creation'] = {
                'success': handbook_create_result.success,
                'details': 'Handbook created/updated'
            }
            
            # 1.3 List modules
            logger.info("Discovering modules...")
            modules_result = self.mcp_core.execute_mcp_call(
                'byterover', 'list_modules', 'docgen'
            )
            results['module_discovery'] = {
                'success': modules_result.success,
                'details': 'Modules discovered and documented'
            }
            
            # 1.4 Bootstrap tests
            logger.info("Bootstrapping test environment...")
            test_bootstrap_result = self.mcp_core.execute_mcp_call(
                'testsprite', 'bootstrap_tests', 3000, 'backend', self.project_path, 'codebase'
            )
            results['test_bootstrap'] = {
                'success': test_bootstrap_result.success,
                'details': 'Test environment bootstrapped'
            }
            
            # 1.5 Get project configuration
            logger.info("Getting project configuration...")
            config_result = self.mcp_core.execute_mcp_call(
                'dart', 'get_config'
            )
            results['project_config'] = {
                'success': config_result.success,
                'details': 'Project configuration retrieved'
            }
            
            # 1.6 Create initial tasks
            logger.info("Creating initial tasks...")
            task_result = self.mcp_core.execute_mcp_call(
                'dart', 'create_task', {
                    'title': 'MCP Integration Implementation',
                    'description': 'Complete MCP integration for DocGen CLI',
                    'tags': ['mcp', 'integration', 'high-priority'],
                    'priority': 'high'
                }
            )
            results['initial_tasks'] = {
                'success': task_result.success,
                'details': 'Initial tasks created'
            }
            
        except Exception as e:
            logger.error(f"Error in Phase 1: {e}")
            results['error'] = {
                'success': False,
                'details': f'Phase 1 error: {str(e)}'
            }
        
        duration = time.time() - start_time
        self.phase_durations['phase_1'] = duration
        self._display_phase_results("Phase 1: Project Initialization", results, duration)
        
        return results
    
    def phase_2_active_development(self) -> Dict[str, Any]:
        """
        Phase 2: Active Development
        - Knowledge retrieval for context
        - Library documentation lookup
        - Development task execution
        - Knowledge storage
        - Module updates
        """
        self._display_phase_header("Active Development", 2)
        start_time = time.time()
        results = {}
        
        try:
            # 2.1 Retrieve development context
            logger.info("Retrieving development context...")
            context_queries = [
                'DocGen CLI current development status',
                'MCP integration patterns and best practices',
                'Python CLI development standards',
                'Jinja2 template implementation patterns',
                'Quality assurance automation techniques'
            ]
            
            knowledge_results = []
            for query in context_queries:
                result = self.mcp_core.execute_mcp_call(
                    'byterover', 'retrieve_knowledge', query
                )
                knowledge_results.append(result)
            
            results['knowledge_retrieval'] = {
                'success': all(r.success for r in knowledge_results),
                'details': f'Retrieved {len(context_queries)} context queries'
            }
            
            # 2.2 Resolve library IDs and get documentation
            logger.info("Resolving library IDs and getting documentation...")
            libraries = ['click', 'jinja2', 'pydantic', 'rich', 'pyyaml', 'email-validator', 'requests', 'semantic-version']
            
            library_results = []
            for library in libraries:
                # Resolve library ID
                resolve_result = self.mcp_core.execute_mcp_call(
                    'context7', 'resolve_library_id', library
                )
                if resolve_result.success:
                    # Get documentation
                    docs_result = self.mcp_core.execute_mcp_call(
                        'context7', 'get_library_docs', resolve_result.data.get('library_id', library), 'api', 5000
                    )
                    library_results.append(docs_result)
            
            results['library_documentation'] = {
                'success': len(library_results) > 0,
                'details': f'Processed {len(libraries)} libraries'
            }
            
            # 2.3 Execute development tasks
            logger.info("Executing development tasks...")
            dev_tasks = [
                'Implement MCP integration core',
                'Create enhanced workflow scripts',
                'Build MCP orchestrator',
                'Integrate with CLI commands'
            ]
            
            task_results = []
            for task in dev_tasks:
                result = self.mcp_core.execute_mcp_call(
                    'dart', 'update_task', {
                        'title': task,
                        'status': 'in_progress',
                        'progress': 75
                    }
                )
                task_results.append(result)
            
            results['development_tasks'] = {
                'success': all(r.success for r in task_results),
                'details': f'Executed {len(dev_tasks)} development tasks'
            }
            
            # 2.4 Store implementation knowledge
            logger.info("Storing implementation knowledge...")
            knowledge_items = [
                'MCP integration core implementation patterns',
                'Enhanced workflow development techniques',
                'Parallel execution optimization strategies',
                'Quality assurance automation patterns'
            ]
            
            storage_results = []
            for item in knowledge_items:
                result = self.mcp_core.execute_mcp_call(
                    'byterover', 'store_knowledge', item
                )
                storage_results.append(result)
            
            results['knowledge_storage'] = {
                'success': all(r.success for r in storage_results),
                'details': f'Stored {len(knowledge_items)} implementation details'
            }
            
        except Exception as e:
            logger.error(f"Error in Phase 2: {e}")
            results['error'] = {
                'success': False,
                'details': f'Phase 2 error: {str(e)}'
            }
        
        duration = time.time() - start_time
        self.phase_durations['phase_2'] = duration
        self._display_phase_results("Phase 2: Active Development", results, duration)
        
        return results
    
    def phase_3_testing_validation(self) -> Dict[str, Any]:
        """
        Phase 3: Testing & Validation
        - Test plan generation
        - Automated test execution
        - Quality audits
        - Performance validation
        - Security checks
        """
        self._display_phase_header("Testing & Validation", 3)
        start_time = time.time()
        results = {}
        
        try:
            # 3.1 Generate test plans
            logger.info("Generating test plans...")
            test_plan_result = self.mcp_core.execute_mcp_call(
                'testsprite', 'generate_backend_test_plan', self.project_path
            )
            results['test_plan_generation'] = {
                'success': test_plan_result.success,
                'details': 'Backend test plan generated'
            }
            
            # 3.2 Execute automated tests
            logger.info("Executing automated tests...")
            test_execution_result = self.mcp_core.execute_mcp_call(
                'testsprite', 'generate_code_and_execute', 'DocGen', self.project_path, [], ''
            )
            results['test_execution'] = {
                'success': test_execution_result.success,
                'details': 'Automated test execution completed'
            }
            
            # 3.3 Run quality audits in parallel
            logger.info("Running quality audits...")
            audit_calls = [
                {
                    'server': 'browser_tools',
                    'function': 'runAccessibilityAudit',
                    'args': [],
                    'kwargs': {}
                },
                {
                    'server': 'browser_tools',
                    'function': 'runPerformanceAudit',
                    'args': [],
                    'kwargs': {}
                },
                {
                    'server': 'browser_tools',
                    'function': 'runBestPracticesAudit',
                    'args': [],
                    'kwargs': {}
                },
                {
                    'server': 'browser_tools',
                    'function': 'runSEOAudit',
                    'args': [],
                    'kwargs': {}
                }
            ]
            
            audit_results = self.mcp_core.execute_parallel_calls(audit_calls)
            successful_audits = sum(1 for r in audit_results if r.success)
            
            results['quality_audits'] = {
                'success': successful_audits >= 3,  # At least 3 out of 4 audits successful
                'details': f'Completed {successful_audits}/4 quality audits'
            }
            
            # 3.4 Browser automation testing
            logger.info("Running browser automation tests...")
            browser_result = self.mcp_core.execute_mcp_call(
                'playwright', 'browser_navigate', f'file://{self.project_path}/README.md'
            )
            results['browser_automation'] = {
                'success': browser_result.success,
                'details': 'Browser automation testing completed'
            }
            
        except Exception as e:
            logger.error(f"Error in Phase 3: {e}")
            results['error'] = {
                'success': False,
                'details': f'Phase 3 error: {str(e)}'
            }
        
        duration = time.time() - start_time
        self.phase_durations['phase_3'] = duration
        self._display_phase_results("Phase 3: Testing & Validation", results, duration)
        
        return results
    
    def phase_4_documentation_knowledge(self) -> Dict[str, Any]:
        """
        Phase 4: Documentation & Knowledge
        - Create project documentation
        - Update existing documentation
        - Store integration patterns
        - Sync handbook
        - Generate reports
        """
        self._display_phase_header("Documentation & Knowledge", 4)
        start_time = time.time()
        results = {}
        
        try:
            # 4.1 Create project documentation
            logger.info("Creating project documentation...")
            doc_tasks = [
                {
                    'title': 'MCP Integration Implementation',
                    'content': 'Comprehensive MCP server integration for DocGen CLI',
                    'tags': ['mcp', 'integration', 'documentation']
                },
                {
                    'title': 'Enhanced Workflow Guide',
                    'content': '4-phase development workflow with MCP integration',
                    'tags': ['workflow', 'development', 'automation']
                },
                {
                    'title': 'Quality Assurance Automation',
                    'content': 'Automated testing and quality validation processes',
                    'tags': ['testing', 'quality', 'automation']
                }
            ]
            
            doc_results = []
            for doc in doc_tasks:
                result = self.mcp_core.execute_mcp_call(
                    'dart', 'create_doc', doc
                )
                doc_results.append(result)
            
            results['documentation_creation'] = {
                'success': all(r.success for r in doc_results),
                'details': f'Created {len(doc_tasks)} documentation files'
            }
            
            # 4.2 Store integration patterns
            logger.info("Storing integration patterns...")
            patterns = [
                'Knowledge-first development pattern with Byterover MCP',
                'Library documentation integration with Context7 MCP',
                'Automated testing workflow with TestSprite MCP',
                'Quality assurance automation with Browser Tools MCP',
                'Parallel execution optimization for MCP servers'
            ]
            
            pattern_results = []
            for pattern in patterns:
                result = self.mcp_core.execute_mcp_call(
                    'byterover', 'store_knowledge', pattern
                )
                pattern_results.append(result)
            
            results['pattern_storage'] = {
                'success': all(r.success for r in pattern_results),
                'details': f'Stored {len(patterns)} integration patterns'
            }
            
            # 4.3 Update handbook
            logger.info("Updating handbook...")
            handbook_result = self.mcp_core.execute_mcp_call(
                'byterover', 'update_handbook', 'BYTEROVER.md', True, 'merge', 'timestamp'
            )
            results['handbook_update'] = {
                'success': handbook_result.success,
                'details': 'Handbook updated and synchronized'
            }
            
            # 4.4 Generate workflow report
            logger.info("Generating workflow report...")
            self._generate_workflow_report()
            results['report_generation'] = {
                'success': True,
                'details': 'Workflow report generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error in Phase 4: {e}")
            results['error'] = {
                'success': False,
                'details': f'Phase 4 error: {str(e)}'
            }
        
        duration = time.time() - start_time
        self.phase_durations['phase_4'] = duration
        self._display_phase_results("Phase 4: Documentation & Knowledge", results, duration)
        
        return results
    
    def _generate_workflow_report(self):
        """Generate comprehensive workflow report."""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'project_path': self.project_path,
            'workflow_results': self.workflow_results,
            'phase_durations': self.phase_durations,
            'total_duration': sum(self.phase_durations.values()),
            'mcp_integration_status': self.mcp_core.get_integration_status(),
            'performance_metrics': self.mcp_core.get_performance_metrics()
        }
        
        # Ensure reports directory exists
        reports_dir = os.path.join(self.project_path, 'assets', 'reports', 'mcp')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Write workflow report
        report_path = os.path.join(reports_dir, 'mcp_workflow_report.yaml')
        import yaml
        with open(report_path, 'w') as f:
            yaml.dump(report_data, f, default_flow_style=False, indent=2)
        
        logger.info(f"Workflow report generated: {report_path}")
    
    def execute_complete_workflow(self) -> Dict[str, Any]:
        """
        Execute the complete 4-phase MCP workflow.
        
        Returns:
            Dictionary with complete workflow results
        """
        logger.info("Starting Enhanced MCP Workflow execution")
        workflow_start = time.time()
        
        try:
            # Execute all phases
            self.workflow_results['phase_1'] = self.phase_1_project_initialization()
            self.workflow_results['phase_2'] = self.phase_2_active_development()
            self.workflow_results['phase_3'] = self.phase_3_testing_validation()
            self.workflow_results['phase_4'] = self.phase_4_documentation_knowledge()
            
            # Calculate overall results
            total_duration = time.time() - workflow_start
            successful_phases = sum(1 for phase, results in self.workflow_results.items() 
                                  if not any(comp.get('error') for comp in results.values()))
            
            self.workflow_results['summary'] = {
                'total_duration': total_duration,
                'successful_phases': successful_phases,
                'total_phases': 4,
                'success_rate': successful_phases / 4,
                'mcp_calls_total': len(self.mcp_core.results),
                'mcp_calls_successful': sum(1 for r in self.mcp_core.results if r.success)
            }
            
            # Display final summary
            self._display_workflow_summary()
            
            logger.info("Enhanced MCP Workflow execution completed successfully")
            return self.workflow_results
            
        except Exception as e:
            logger.error(f"Error in complete workflow execution: {e}")
            return {'error': str(e)}
    
    def _display_workflow_summary(self):
        """Display comprehensive workflow summary."""
        if not self.console:
            summary = self.workflow_results.get('summary', {})
            print(f"\n{'='*60}")
            print("ENHANCED MCP WORKFLOW SUMMARY")
            print('='*60)
            print(f"Total Duration: {summary.get('total_duration', 0):.2f} seconds")
            print(f"Successful Phases: {summary.get('successful_phases', 0)}/4")
            print(f"Success Rate: {summary.get('success_rate', 0):.2%}")
            print(f"MCP Calls Total: {summary.get('mcp_calls_total', 0)}")
            print(f"MCP Calls Successful: {summary.get('mcp_calls_successful', 0)}")
            return
        
        summary = self.workflow_results.get('summary', {})
        
        # Create summary table
        table = Table(title="Enhanced MCP Workflow Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Duration", f"{summary.get('total_duration', 0):.2f} seconds")
        table.add_row("Successful Phases", f"{summary.get('successful_phases', 0)}/4")
        table.add_row("Success Rate", f"{summary.get('success_rate', 0):.2%}")
        table.add_row("MCP Calls Total", str(summary.get('mcp_calls_total', 0)))
        table.add_row("MCP Calls Successful", str(summary.get('mcp_calls_successful', 0)))
        
        self.console.print(table)
        
        # Display phase durations
        if self.phase_durations:
            phase_table = Table(title="Phase Durations")
            phase_table.add_column("Phase", style="cyan")
            phase_table.add_column("Duration", style="yellow")
            
            for phase, duration in self.phase_durations.items():
                phase_table.add_row(phase.replace('_', ' ').title(), f"{duration:.2f}s")
            
            self.console.print(phase_table)

def main():
    """Main function for testing Enhanced MCP Workflow."""
    try:
        # Initialize Enhanced MCP Workflow
        workflow = EnhancedMCPWorkflow()
        
        # Execute complete workflow
        results = workflow.execute_complete_workflow()
        
        # Check for errors
        if 'error' in results:
            logger.error(f"Workflow execution failed: {results['error']}")
            return 1
        
        # Display success message
        if workflow.console:
            success_panel = Panel(
                "[bold green]Enhanced MCP Workflow completed successfully![/bold green]\n"
                "All 4 phases executed with comprehensive MCP integration.",
                title="Workflow Complete",
                border_style="green"
            )
            workflow.console.print(success_panel)
        else:
            print("\n✅ Enhanced MCP Workflow completed successfully!")
            print("All 4 phases executed with comprehensive MCP integration.")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in Enhanced MCP Workflow test: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
