#!/usr/bin/env python3
"""
Test runner script for DocGen CLI.

This script provides a convenient way to run tests with different configurations
and generate coverage reports.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run DocGen CLI tests")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "cli", "all"], 
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--html", 
        action="store_true",
        help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--fast", 
        action="store_true",
        help="Skip slow tests"
    )
    parser.add_argument(
        "--lint", 
        action="store_true",
        help="Run linting checks"
    )
    parser.add_argument(
        "--format", 
        action="store_true",
        help="Format code with black and isort"
    )
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🧪 DocGen CLI Test Runner")
    print(f"📁 Working directory: {project_root}")
    
    success = True
    
    # Code formatting
    if args.format:
        success &= run_command(
            ["python", "-m", "black", "src", "tests"],
            "Code formatting with black"
        )
        success &= run_command(
            ["python", "-m", "isort", "src", "tests"],
            "Import sorting with isort"
        )
    
    # Linting
    if args.lint:
        success &= run_command(
            ["python", "-m", "flake8", "src", "tests"],
            "Code linting with flake8"
        )
        success &= run_command(
            ["python", "-m", "mypy", "src"],
            "Type checking with mypy"
        )
    
    # Test execution
    if args.type == "all":
        test_commands = [
            (["python", "-m", "pytest", "tests/unit", "-v"], "Unit tests"),
            (["python", "-m", "pytest", "tests/integration", "-v"], "Integration tests"),
            (["python", "-m", "pytest", "tests/cli", "-v"], "CLI tests"),
        ]
    elif args.type == "unit":
        test_commands = [
            (["python", "-m", "pytest", "tests/unit", "-v"], "Unit tests"),
        ]
    elif args.type == "integration":
        test_commands = [
            (["python", "-m", "pytest", "tests/integration", "-v"], "Integration tests"),
        ]
    elif args.type == "cli":
        test_commands = [
            (["python", "-m", "pytest", "tests/cli", "-v"], "CLI tests"),
        ]
    
    # Add coverage options
    for i, (command, description) in enumerate(test_commands):
        if args.coverage:
            command.extend(["--cov=src", "--cov-report=term-missing"])
        if args.html:
            command.extend(["--cov-report=html:htmlcov"])
        if args.verbose:
            command.append("-vv")
        if args.fast:
            command.extend(["-m", "not slow"])
        
        success &= run_command(command, description)
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        if args.coverage:
            print("📊 Coverage report generated")
        if args.html:
            print("📄 HTML coverage report available in htmlcov/")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
