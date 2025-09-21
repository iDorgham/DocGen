#!/usr/bin/env python3
"""
Workflow Automation Script for DocGen CLI
Automate daily, weekly, and monthly development tasks
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

class WorkflowAutomation:
    def __init__(self):
        self.project_root = Path.cwd()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tasks': {},
            'summary': {
                'total_tasks': 0,
                'completed': 0,
                'failed': 0,
                'skipped': 0
            }
        }
    
    def run_task(self, name: str, command: str, description: str = "", required: bool = True):
        """Run a workflow task and record results."""
        print(f"🔄 {name}...")
        if description:
            print(f"   {description}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            self.results['tasks'][name] = {
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'description': description,
                'required': required,
                'status': 'completed' if result.returncode == 0 else 'failed'
            }
            
            if result.returncode == 0:
                print(f"   ✓ Completed")
                self.results['summary']['completed'] += 1
            else:
                print(f"   ✗ Failed (exit code: {result.returncode})")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                self.results['summary']['failed'] += 1
            
            self.results['summary']['total_tasks'] += 1
            
        except Exception as e:
            print(f"   ✗ Error running task: {e}")
            self.results['tasks'][name] = {
                'command': command,
                'error': str(e),
                'required': required,
                'status': 'error'
            }
            self.results['summary']['failed'] += 1
            self.results['summary']['total_tasks'] += 1
    
    def run_daily_tasks(self):
        """Run daily development tasks."""
        print("\n📅 Daily Tasks")
        print("-" * 30)
        
        # Code formatting
        self.run_task(
            "format_code",
            "black src/ && isort src/",
            "Format code with Black and isort"
        )
        
        # Linting
        self.run_task(
            "lint_code",
            "flake8 src/ --max-line-length=88 --extend-ignore=E203,W503",
            "Run code linting"
        )
        
        # Type checking
        self.run_task(
            "type_check",
            "mypy src/ --ignore-missing-imports",
            "Run static type checking"
        )
        
        # Test execution
        self.run_task(
            "run_tests",
            "python -m pytest -v --tb=short",
            "Run test suite"
        )
        
        # Documentation generation
        self.run_task(
            "generate_docs",
            "python assets/dev/scripts/generate_docs.py",
            "Generate project documentation"
        )
    
    def run_weekly_tasks(self):
        """Run weekly development tasks."""
        print("\n📅 Weekly Tasks")
        print("-" * 30)
        
        # Security scan
        self.run_task(
            "security_scan",
            "bandit -r src/ -f json",
            "Run security vulnerability scan"
        )
        
        # Dependency check
        self.run_task(
            "dependency_check",
            "safety check --json",
            "Check for vulnerable dependencies"
        )
        
        # Code quality analysis
        self.run_task(
            "quality_analysis",
            "pylint src/ --disable=C0114,C0116",
            "Run comprehensive code quality analysis"
        )
        
        # Test coverage
        self.run_task(
            "test_coverage",
            "python -m pytest --cov=src --cov-report=html --cov-report=term",
            "Generate test coverage report"
        )
        
        # Documentation validation
        self.run_task(
            "validate_docs",
            "docstr-coverage src/ --fail-under=80",
            "Validate documentation coverage"
        )
    
    def run_monthly_tasks(self):
        """Run monthly development tasks."""
        print("\n📅 Monthly Tasks")
        print("-" * 30)
        
        # Project health check
        self.run_task(
            "project_health",
            "python assets/dev/scripts/project_monitoring.py",
            "Run comprehensive project health check"
        )
        
        # Performance analysis
        self.run_task(
            "performance_analysis",
            "python -c \"import time; start=time.time(); import src; print(f'Import time: {time.time()-start:.3f}s')\"",
            "Analyze project performance"
        )
        
        # Dependency updates
        self.run_task(
            "check_updates",
            "pip list --outdated",
            "Check for outdated dependencies"
        )
        
        # Archive old reports
        self.run_task(
            "archive_reports",
            "find assets/reports -name '*.json' -mtime +30 -exec mv {} assets/reports/archive/ \\;",
            "Archive old reports"
        )
        
        # Cleanup temporary files
        self.run_task(
            "cleanup_temp",
            "find . -name '*.pyc' -delete && find . -name '__pycache__' -type d -exec rm -rf {} +",
            "Clean up temporary files"
        )
    
    def run_project_health_check(self):
        """Run comprehensive project health check."""
        print("\n🏥 Project Health Check")
        print("-" * 30)
        
        # Check project structure
        self.run_task(
            "check_structure",
            "python assets/dev/scripts/dev_helpers.py --check-structure",
            "Validate project structure"
        )
        
        # Check dependencies
        self.run_task(
            "check_dependencies",
            "python assets/dev/scripts/dev_helpers.py --check-deps",
            "Validate project dependencies"
        )
        
        # Check templates
        self.run_task(
            "check_templates",
            "python assets/dev/scripts/dev_helpers.py --check-templates",
            "Validate Jinja2 templates"
        )
        
        # Check documentation sync
        self.run_task(
            "check_docs_sync",
            "python assets/dev/scripts/dev_helpers.py --check-docs-sync",
            "Check documentation synchronization"
        )
    
    def run_specification_validation(self):
        """Run specification validation tasks."""
        print("\n📋 Specification Validation")
        print("-" * 30)
        
        # Validate requirements
        self.run_task(
            "validate_requirements",
            "python assets/config/validation.py --validate-requirements",
            "Validate project requirements"
        )
        
        # Validate tasks
        self.run_task(
            "validate_tasks",
            "python assets/config/validation.py --validate-tasks",
            "Validate project tasks"
        )
        
        # Validate technical specs
        self.run_task(
            "validate_technical",
            "python assets/config/validation.py --validate-technical",
            "Validate technical specifications"
        )
    
    def generate_report(self):
        """Generate workflow automation report."""
        report_file = self.project_root / 'assets' / 'reports' / 'workflow_automation_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Workflow report saved to: {report_file}")
        return report_file
    
    def display_summary(self):
        """Display workflow automation summary."""
        summary = self.results['summary']
        total = summary['total_tasks']
        completed = summary['completed']
        failed = summary['failed']
        
        print(f"\n📊 Workflow Automation Summary")
        print("=" * 40)
        print(f"Total Tasks: {total}")
        print(f"Completed: {completed} ({completed/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        
        if failed > 0:
            print(f"\n❌ Failed Tasks:")
            for name, task in self.results['tasks'].items():
                if task['status'] == 'failed':
                    print(f"  - {name}: {task.get('description', '')}")
        
        success_rate = completed / total if total > 0 else 0
        if success_rate >= 0.8:
            print(f"\n✅ Workflow automation completed! ({success_rate*100:.1f}% success rate)")
            return True
        else:
            print(f"\n❌ Workflow automation failed! ({success_rate*100:.1f}% success rate)")
            return False
    
    def run_workflow(self, workflow_type: str = "daily"):
        """Run specified workflow type."""
        print(f"🚀 DocGen CLI Workflow Automation - {workflow_type.title()}")
        print("=" * 50)
        
        if workflow_type == "daily":
            self.run_daily_tasks()
        elif workflow_type == "weekly":
            self.run_weekly_tasks()
        elif workflow_type == "monthly":
            self.run_monthly_tasks()
        elif workflow_type == "health":
            self.run_project_health_check()
        elif workflow_type == "specs":
            self.run_specification_validation()
        elif workflow_type == "all":
            self.run_daily_tasks()
            self.run_weekly_tasks()
            self.run_monthly_tasks()
            self.run_project_health_check()
            self.run_specification_validation()
        else:
            print(f"Unknown workflow type: {workflow_type}")
            return False
        
        # Generate report
        self.generate_report()
        
        # Display summary
        return self.display_summary()

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='DocGen CLI Workflow Automation')
    parser.add_argument(
        '--workflow', 
        choices=['daily', 'weekly', 'monthly', 'health', 'specs', 'all'],
        default='daily',
        help='Workflow type to run'
    )
    
    args = parser.parse_args()
    
    automation = WorkflowAutomation()
    success = automation.run_workflow(args.workflow)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
