#!/usr/bin/env python3
"""
Project Structure Validation Script

This script validates that the project structure follows the established
organization rules and naming conventions.

Usage:
    python validate-project-structure.py [--verbose]

Options:
    --verbose    Show detailed output
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

class ProjectStructureValidator:
    """Validates project structure according to established rules."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.errors = []
        self.warnings = []
        self.passed_checks = 0
        self.total_checks = 0
        
        # Define allowed root files
        self.allowed_root_files = {
            'README.md', 'pyproject.toml', 'requirements.txt', 'pytest.ini',
            '.gitignore', '.env.example', '.env', 'LICENSE', 'docker-compose.yml',
            'Dockerfile', 'Dockerfile.prod', 'docgen_cli.py', 'BYTEROVER.md', 'venv'
        }
        
        # Define required directory structure
        self.required_directories = {
            'assets/docs/project-docs',
            'assets/docs/developer',
            'assets/reports',
            'assets/dev/scripts',
            'assets/data',
            'assets/management',
            'assets/specs',
            'assets/templates',
            'src',
            'tests'
        }
        
        # Define forbidden patterns in root
        self.forbidden_root_patterns = [
            r'.*_SUMMARY\.md$',
            r'.*_REPORT\.md$',
            r'.*_test\.py$',
            r'test_.*\.py$',
            r'.*\.tmp$',
            r'.*\.temp$',
            r'.*\.cache$',
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with appropriate level."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{level}] {message}")
    
    def check(self, condition: bool, message: str, error_type: str = "ERROR"):
        """Perform a check and log the result."""
        self.total_checks += 1
        if condition:
            self.passed_checks += 1
            if self.verbose:
                self.log(f"✓ {message}")
        else:
            if error_type == "ERROR":
                self.errors.append(message)
            else:
                self.warnings.append(message)
            self.log(f"✗ {message}", error_type)
    
    def validate_root_directory(self):
        """Validate the root directory structure."""
        self.log("Validating root directory...")
        
        root_files = [f for f in os.listdir(self.project_root) 
                     if os.path.isfile(os.path.join(self.project_root, f))]
        
        # Check for forbidden files
        for filename in root_files:
            if filename not in self.allowed_root_files:
                # Check if it matches forbidden patterns
                is_forbidden = any(re.match(pattern, filename) for pattern in self.forbidden_root_patterns)
                if is_forbidden:
                    self.check(False, f"Forbidden file in root: {filename}")
                else:
                    self.check(False, f"Unexpected file in root: {filename}", "WARNING")
            else:
                self.check(True, f"Allowed file in root: {filename}")
        
        # Check for required files
        required_files = ['README.md', 'pyproject.toml', 'requirements.txt', 'docgen_cli.py']
        for filename in required_files:
            self.check(
                filename in root_files,
                f"Required file missing from root: {filename}"
            )
    
    def validate_directory_structure(self):
        """Validate the directory structure."""
        self.log("Validating directory structure...")
        
        for dir_path in self.required_directories:
            full_path = self.project_root / dir_path
            self.check(
                full_path.exists(),
                f"Required directory missing: {dir_path}"
            )
    
    def validate_naming_conventions(self):
        """Validate file naming conventions."""
        self.log("Validating naming conventions...")
        
        # Check all files in assets directory
        assets_path = self.project_root / 'assets'
        if assets_path.exists():
            for root, dirs, files in os.walk(assets_path):
                for filename in files:
                    if filename.endswith('.md'):
                        # Check if filename follows lowercase-hyphen convention
                        expected_name = self.convert_to_lowercase_hyphen(filename)
                        self.check(
                            filename == expected_name,
                            f"File naming convention violation: {filename} (should be {expected_name})"
                        )
    
    def convert_to_lowercase_hyphen(self, filename: str) -> str:
        """Convert filename to lowercase-hyphen format."""
        # Remove extension
        name, ext = os.path.splitext(filename)
        
        # Convert to lowercase
        name = name.lower()
        
        # Replace underscores and spaces with hyphens
        name = re.sub(r'[_ ]+', '-', name)
        
        # Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)
        
        # Remove leading/trailing hyphens
        name = name.strip('-')
        
        return f"{name}{ext}"
    
    def validate_file_placements(self):
        """Validate that files are in correct locations."""
        self.log("Validating file placements...")
        
        # Check documentation files
        docs_path = self.project_root / 'assets/docs/project-docs'
        if docs_path.exists():
            expected_docs = [
                'agents.md', 'api-reference.md', 'changelog.md', 'claude.md',
                'code-of-conduct.md', 'contributing.md', 'deployment.md',
                'installation.md', 'security.md', 'user-guide.md'
            ]
            
            actual_docs = [f for f in os.listdir(docs_path) if f.endswith('.md')]
            for expected_doc in expected_docs:
                self.check(
                    expected_doc in actual_docs,
                    f"Expected documentation file missing: {expected_doc}"
                )
        
        # Check report files
        reports_path = self.project_root / 'assets/reports'
        if reports_path.exists():
            expected_reports = [
                'comprehensive-browser-automation-summary.md',
                'phase3-completion-summary.md',
                'phase3-final-report.md',
                'playwright-integration-summary.md',
                'production-deployment-summary.md',
                'test-coverage-implementation-summary.md',
                'testsprite-api-configuration-summary.md'
            ]
            
            actual_reports = [f for f in os.listdir(reports_path) if f.endswith('.md')]
            for expected_report in expected_reports:
                self.check(
                    expected_report in actual_reports,
                    f"Expected report file missing: {expected_report}"
                )
        
        # Check script files
        scripts_path = self.project_root / 'assets/dev/scripts'
        if scripts_path.exists():
            expected_scripts = [
                'debug-tests.py', 'run-tests.py', 'test-standalone.py',
                'organize-project-files.py', 'validate-project-structure.py'
            ]
            
            actual_scripts = [f for f in os.listdir(scripts_path) if f.endswith('.py')]
            for expected_script in expected_scripts:
                self.check(
                    expected_script in actual_scripts,
                    f"Expected script file missing: {expected_script}"
                )
    
    def validate_configuration_files(self):
        """Validate configuration files."""
        self.log("Validating configuration files...")
        
        # Check pyproject.toml
        pyproject_path = self.project_root / 'pyproject.toml'
        self.check(
            pyproject_path.exists(),
            "pyproject.toml missing from root"
        )
        
        # Check requirements.txt
        requirements_path = self.project_root / 'requirements.txt'
        self.check(
            requirements_path.exists(),
            "requirements.txt missing from root"
        )
        
        # Check pytest.ini
        pytest_path = self.project_root / 'pytest.ini'
        self.check(
            pytest_path.exists(),
            "pytest.ini missing from root"
        )
    
    def generate_report(self):
        """Generate validation report."""
        self.log("\n" + "="*60)
        self.log("PROJECT STRUCTURE VALIDATION REPORT")
        self.log("="*60)
        
        self.log(f"Total checks: {self.total_checks}")
        self.log(f"Passed: {self.passed_checks}")
        self.log(f"Failed: {len(self.errors)}")
        self.log(f"Warnings: {len(self.warnings)}")
        
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        self.log(f"Success rate: {success_rate:.1f}%")
        
        if self.errors:
            self.log("\nERRORS:", "ERROR")
            for error in self.errors:
                self.log(f"  - {error}", "ERROR")
        
        if self.warnings:
            self.log("\nWARNINGS:", "WARNING")
            for warning in self.warnings:
                self.log(f"  - {warning}", "WARNING")
        
        if not self.errors and not self.warnings:
            self.log("\n✓ All validations passed! Project structure is correct.")
        
        return len(self.errors) == 0
    
    def run(self):
        """Run all validation checks."""
        self.log("Starting project structure validation...")
        
        try:
            self.validate_root_directory()
            self.validate_directory_structure()
            self.validate_naming_conventions()
            self.validate_file_placements()
            self.validate_configuration_files()
            
            return self.generate_report()
            
        except Exception as e:
            self.log(f"Validation failed: {e}", "ERROR")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate project structure according to established rules")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    validator = ProjectStructureValidator(verbose=args.verbose)
    success = validator.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
