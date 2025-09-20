#!/usr/bin/env python3
"""
Quality Assurance Script for DocGen CLI
Run comprehensive quality checks on the codebase
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class QualityChecker:
    def __init__(self):
        self.project_root = Path.cwd()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'summary': {
                'total_checks': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
    
    def run_check(self, name, command, description=""):
        """Run a quality check and record results."""
        print(f"🔍 {name}...")
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
            
            self.results['checks'][name] = {
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'description': description,
                'status': 'passed' if result.returncode == 0 else 'failed'
            }
            
            if result.returncode == 0:
                print(f"   ✓ Passed")
                self.results['summary']['passed'] += 1
            else:
                print(f"   ✗ Failed (exit code: {result.returncode})")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                self.results['summary']['failed'] += 1
            
            self.results['summary']['total_checks'] += 1
            
        except Exception as e:
            print(f"   ✗ Error running check: {e}")
            self.results['checks'][name] = {
                'command': command,
                'error': str(e),
                'status': 'error'
            }
            self.results['summary']['failed'] += 1
            self.results['summary']['total_checks'] += 1
    
    def run_linting_checks(self):
        """Run code linting checks."""
        print("\n📋 Code Linting Checks")
        print("-" * 30)
        
        # Flake8
        self.run_check(
            "flake8",
            "flake8 src/ --max-line-length=88 --extend-ignore=E203,W503",
            "Python code style and error checking"
        )
        
        # MyPy
        self.run_check(
            "mypy",
            "mypy src/ --ignore-missing-imports",
            "Static type checking"
        )
        
        # Pylint
        self.run_check(
            "pylint",
            "pylint src/ --disable=C0114,C0116",
            "Code quality analysis"
        )
    
    def run_formatting_checks(self):
        """Run code formatting checks."""
        print("\n🎨 Code Formatting Checks")
        print("-" * 30)
        
        # Black
        self.run_check(
            "black_check",
            "black --check src/",
            "Code formatting consistency"
        )
        
        # isort
        self.run_check(
            "isort_check",
            "isort --check-only src/",
            "Import statement organization"
        )
    
    def run_security_checks(self):
        """Run security checks."""
        print("\n🔒 Security Checks")
        print("-" * 30)
        
        # Bandit
        self.run_check(
            "bandit",
            "bandit -r src/ -f json",
            "Security vulnerability scanning"
        )
        
        # Safety
        self.run_check(
            "safety",
            "safety check --json",
            "Dependency vulnerability scanning"
        )
    
    def run_test_checks(self):
        """Run test-related checks."""
        print("\n🧪 Test Checks")
        print("-" * 30)
        
        # Test discovery
        self.run_check(
            "test_discovery",
            "python -m pytest --collect-only",
            "Test discovery and validation"
        )
        
        # Test execution
        self.run_check(
            "test_execution",
            "python -m pytest -v --tb=short",
            "Test execution and results"
        )
    
    def run_documentation_checks(self):
        """Run documentation checks."""
        print("\n📚 Documentation Checks")
        print("-" * 30)
        
        # Docstring coverage
        self.run_check(
            "docstring_coverage",
            "docstr-coverage src/ --fail-under=80",
            "Docstring coverage analysis"
        )
        
        # Documentation build
        self.run_check(
            "docs_build",
            "python assets/dev/scripts/generate_docs.py",
            "Documentation generation"
        )
    
    def run_performance_checks(self):
        """Run performance checks."""
        print("\n⚡ Performance Checks")
        print("-" * 30)
        
        # Import time
        self.run_check(
            "import_time",
            "python -c \"import time; start=time.time(); import src; print(f'Import time: {time.time()-start:.3f}s')\"",
            "Module import performance"
        )
        
        # Memory usage
        self.run_check(
            "memory_usage",
            "python -c \"import psutil, os; print(f'Memory usage: {psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.1f} MB')\"",
            "Memory usage analysis"
        )
    
    def generate_report(self):
        """Generate quality check report."""
        report_file = self.project_root / 'assets' / 'reports' / 'quality_check_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Quality report saved to: {report_file}")
        return report_file
    
    def display_summary(self):
        """Display quality check summary."""
        summary = self.results['summary']
        total = summary['total_checks']
        passed = summary['passed']
        failed = summary['failed']
        
        print(f"\n📊 Quality Check Summary")
        print("=" * 40)
        print(f"Total Checks: {total}")
        print(f"Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        
        if failed > 0:
            print(f"\n❌ Failed Checks:")
            for name, check in self.results['checks'].items():
                if check['status'] == 'failed':
                    print(f"  - {name}: {check.get('description', '')}")
        
        success_rate = passed / total if total > 0 else 0
        if success_rate >= 0.8:
            print(f"\n✅ Quality check passed! ({success_rate*100:.1f}% success rate)")
            return True
        else:
            print(f"\n❌ Quality check failed! ({success_rate*100:.1f}% success rate)")
            return False
    
    def run_all_checks(self):
        """Run all quality checks."""
        print("🚀 DocGen CLI Quality Assurance")
        print("=" * 40)
        
        self.run_linting_checks()
        self.run_formatting_checks()
        self.run_security_checks()
        self.run_test_checks()
        self.run_documentation_checks()
        self.run_performance_checks()
        
        # Generate report
        self.generate_report()
        
        # Display summary
        return self.display_summary()

def main():
    """Main function."""
    checker = QualityChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
