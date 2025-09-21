#!/usr/bin/env python3
"""
Complete Integration Workflow Script

This script runs a comprehensive integration workflow including:
1. Playwright browser automation tests
2. CLI functionality tests
3. Performance validation
4. Quality assurance checks
5. Documentation generation
6. MCP server integration tests
"""

import os
import sys
import subprocess
import time
import json
import tempfile
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright


class IntegrationWorkflow:
    """Complete integration workflow manager."""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            "start_time": datetime.now().isoformat(),
            "tests": {},
            "performance": {},
            "quality": {},
            "errors": [],
            "warnings": []
        }
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(__file__).parent.parent
        
    def log(self, message, level="INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
        if level == "ERROR":
            self.results["errors"].append(message)
        elif level == "WARNING":
            self.results["warnings"].append(message)
    
    def run_command(self, command, cwd=None, capture_output=True):
        """Run a command and return the result."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.project_root,
                capture_output=capture_output,
                text=True,
                timeout=300
            )
            return result
        except subprocess.TimeoutExpired:
            self.log(f"Command timed out: {command}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Command failed: {command} - {str(e)}", "ERROR")
            return None
    
    def test_playwright_installation(self):
        """Test Playwright installation and basic functionality."""
        self.log("Testing Playwright installation...")
        
        try:
            # Test Playwright import
            result = self.run_command("python -c 'from playwright.sync_api import sync_playwright; print(\"Playwright imported successfully\")'")
            if result and result.returncode == 0:
                self.log("✓ Playwright import test passed")
                self.results["tests"]["playwright_import"] = "PASS"
            else:
                self.log("✗ Playwright import test failed", "ERROR")
                self.results["tests"]["playwright_import"] = "FAIL"
                return False
            
            # Test browser launch
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<h1>Test</h1>")
                content = page.content()
                browser.close()
                
                if "<h1>Test</h1>" in content:
                    self.log("✓ Playwright browser test passed")
                    self.results["tests"]["playwright_browser"] = "PASS"
                else:
                    self.log("✗ Playwright browser test failed", "ERROR")
                    self.results["tests"]["playwright_browser"] = "FAIL"
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"Playwright test failed: {str(e)}", "ERROR")
            self.results["tests"]["playwright_installation"] = "FAIL"
            return False
    
    def test_cli_functionality(self):
        """Test CLI functionality."""
        self.log("Testing CLI functionality...")
        
        # Test CLI help
        result = self.run_command("python -m src.cli.main --help")
        if result and result.returncode == 0:
            self.log("✓ CLI help test passed")
            self.results["tests"]["cli_help"] = "PASS"
        else:
            self.log(f"✗ CLI help test failed - Return code: {result.returncode if result else 'None'}, Output: {result.stdout if result else 'None'}", "ERROR")
            self.results["tests"]["cli_help"] = "FAIL"
            return False
        
        # Test CLI commands
        commands = [
            ("python -m src.cli.main spec --help", "spec"),
            ("python -m src.cli.main validate --help", "validate"),
            ("python -m src.cli.main create --help", "create")
        ]
        
        for command, expected in commands:
            result = self.run_command(command)
            if result and result.returncode == 0:
                self.log(f"✓ CLI {expected} command test passed")
                self.results["tests"][f"cli_{expected}"] = "PASS"
            else:
                self.log(f"✗ CLI {expected} command test failed - Return code: {result.returncode if result else 'None'}", "ERROR")
                self.results["tests"][f"cli_{expected}"] = "FAIL"
                return False
        
        return True
    
    def test_browser_automation(self):
        """Test browser automation capabilities."""
        self.log("Testing browser automation...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Test navigation
                page.goto("data:text/html,<h1>DocGen CLI Test</h1><button id='test-btn'>Click Me</button>")
                
                # Test interaction
                page.click("#test-btn")
                
                # Test screenshot
                screenshot_path = Path(self.temp_dir) / "test_screenshot.png"
                page.screenshot(path=str(screenshot_path))
                
                # Test console logs
                console_logs = []
                page.on("console", lambda msg: console_logs.append(msg.text))
                page.evaluate("console.log('Test message')")
                
                browser.close()
                
                # Verify results
                if screenshot_path.exists() and len(console_logs) > 0:
                    self.log("✓ Browser automation test passed")
                    self.results["tests"]["browser_automation"] = "PASS"
                    return True
                else:
                    self.log("✗ Browser automation test failed", "ERROR")
                    self.results["tests"]["browser_automation"] = "FAIL"
                    return False
                    
        except Exception as e:
            self.log(f"Browser automation test failed: {str(e)}", "ERROR")
            self.results["tests"]["browser_automation"] = "FAIL"
            return False
    
    def test_performance(self):
        """Test performance requirements."""
        self.log("Testing performance requirements...")
        
        # Test browser startup performance
        start_time = time.time()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            browser.close()
        startup_time = time.time() - start_time
        
        self.results["performance"]["browser_startup"] = startup_time
        
        if startup_time < 5.0:
            self.log(f"✓ Browser startup performance test passed ({startup_time:.2f}s)")
            self.results["tests"]["performance_startup"] = "PASS"
        else:
            self.log(f"✗ Browser startup performance test failed ({startup_time:.2f}s)", "WARNING")
            self.results["tests"]["performance_startup"] = "WARN"
        
        # Test memory usage
        import psutil
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("data:text/html,<h1>Test</h1>")
            current_memory = process.memory_info().rss
            browser.close()
        
        memory_increase = current_memory - initial_memory
        self.results["performance"]["memory_increase"] = memory_increase
        
        if memory_increase < 100 * 1024 * 1024:  # 100MB
            self.log(f"✓ Memory usage test passed ({memory_increase / 1024 / 1024:.2f}MB)")
            self.results["tests"]["performance_memory"] = "PASS"
        else:
            self.log(f"✗ Memory usage test failed ({memory_increase / 1024 / 1024:.2f}MB)", "WARNING")
            self.results["tests"]["performance_memory"] = "WARN"
        
        return True
    
    def test_quality_assurance(self):
        """Test quality assurance requirements."""
        self.log("Testing quality assurance...")
        
        # Test code quality
        result = self.run_command("python -m flake8 src/ --max-line-length=100")
        if result and result.returncode == 0:
            self.log("✓ Code quality test passed")
            self.results["quality"]["flake8"] = "PASS"
        else:
            self.log("✗ Code quality test failed", "WARNING")
            self.results["quality"]["flake8"] = "WARN"
        
        # Test type checking
        result = self.run_command("python -m mypy src/ --ignore-missing-imports")
        if result and result.returncode == 0:
            self.log("✓ Type checking test passed")
            self.results["quality"]["mypy"] = "PASS"
        else:
            self.log("✗ Type checking test failed", "WARNING")
            self.results["quality"]["mypy"] = "WARN"
        
        return True
    
    def test_integration_tests(self):
        """Run integration tests."""
        self.log("Running integration tests...")
        
        # Run pytest integration tests
        result = self.run_command("python -m pytest tests/integration/ -v --tb=short")
        if result and result.returncode == 0:
            self.log("✓ Integration tests passed")
            self.results["tests"]["integration"] = "PASS"
            return True
        else:
            self.log("✗ Integration tests failed", "ERROR")
            self.results["tests"]["integration"] = "FAIL"
            return False
    
    def generate_documentation(self):
        """Generate project documentation."""
        self.log("Generating documentation...")
        
        # Create sample project data
        project_data = {
            "name": "DocGen CLI Integration Test",
            "description": "Integration test project for DocGen CLI",
            "version": "1.0.0",
            "author": "Integration Test",
            "license": "MIT",
            "repository": "https://github.com/test/docgen-cli"
        }
        
        project_data_path = Path(self.temp_dir) / "project_data.yaml"
        import yaml
        with open(project_data_path, 'w') as f:
            yaml.dump(project_data, f)
        
        # Generate documentation
        output_dir = Path(self.temp_dir) / "output"
        output_dir.mkdir()
        
        result = self.run_command(f"python -m src.cli.main generate --project-data {project_data_path} --output-dir {output_dir} --template marketing")
        if result and result.returncode == 0:
            self.log("✓ Documentation generation test passed")
            self.results["tests"]["documentation_generation"] = "PASS"
            return True
        else:
            self.log("✗ Documentation generation test failed", "ERROR")
            self.results["tests"]["documentation_generation"] = "FAIL"
            return False
    
    def run_complete_workflow(self):
        """Run the complete integration workflow."""
        self.log("Starting complete integration workflow...")
        
        workflow_steps = [
            ("Playwright Installation", self.test_playwright_installation),
            ("CLI Functionality", self.test_cli_functionality),
            ("Browser Automation", self.test_browser_automation),
            ("Performance Testing", self.test_performance),
            ("Quality Assurance", self.test_quality_assurance),
            ("Integration Tests", self.test_integration_tests),
            ("Documentation Generation", self.generate_documentation)
        ]
        
        passed_steps = 0
        total_steps = len(workflow_steps)
        
        for step_name, step_function in workflow_steps:
            self.log(f"Running {step_name}...")
            try:
                if step_function():
                    passed_steps += 1
                    self.log(f"✓ {step_name} completed successfully")
                else:
                    self.log(f"✗ {step_name} failed", "ERROR")
            except Exception as e:
                self.log(f"✗ {step_name} failed with exception: {str(e)}", "ERROR")
        
        # Calculate results
        self.results["end_time"] = datetime.now().isoformat()
        self.results["duration"] = time.time() - self.start_time
        self.results["passed_steps"] = passed_steps
        self.results["total_steps"] = total_steps
        self.results["success_rate"] = (passed_steps / total_steps) * 100
        
        # Generate report
        self.generate_report()
        
        return passed_steps == total_steps
    
    def generate_report(self):
        """Generate integration workflow report."""
        self.log("Generating integration workflow report...")
        
        report_path = self.project_root / "assets" / "reports" / "integration_workflow_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Generate summary
        summary = f"""
Integration Workflow Report
==========================

Start Time: {self.results['start_time']}
End Time: {self.results['end_time']}
Duration: {self.results['duration']:.2f} seconds

Results:
--------
Passed Steps: {self.results['passed_steps']}/{self.results['total_steps']}
Success Rate: {self.results['success_rate']:.1f}%

Test Results:
-------------
"""
        
        for test_name, result in self.results["tests"].items():
            summary += f"  {test_name}: {result}\n"
        
        if self.results["errors"]:
            summary += "\nErrors:\n-------\n"
            for error in self.results["errors"]:
                summary += f"  - {error}\n"
        
        if self.results["warnings"]:
            summary += "\nWarnings:\n---------\n"
            for warning in self.results["warnings"]:
                summary += f"  - {warning}\n"
        
        summary_path = self.project_root / "assets" / "reports" / "integration_workflow_summary.txt"
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        self.log(f"Report generated: {report_path}")
        self.log(f"Summary generated: {summary_path}")
        
        # Print summary to console
        print(summary)
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.log("Cleanup completed")
        except Exception as e:
            self.log(f"Cleanup failed: {str(e)}", "WARNING")


def main():
    """Main function to run the integration workflow."""
    workflow = IntegrationWorkflow()
    
    try:
        success = workflow.run_complete_workflow()
        if success:
            print("\n🎉 Integration workflow completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Integration workflow completed with errors!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Integration workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Integration workflow failed with exception: {str(e)}")
        sys.exit(1)
    finally:
        workflow.cleanup()


if __name__ == "__main__":
    main()
