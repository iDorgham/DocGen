#!/usr/bin/env python3
"""
Simple Browser Automation Test Runner

This script runs basic browser automation tests to verify Playwright functionality
and basic browser automation capabilities.
"""

import os
import sys
import subprocess
import time
import json
import tempfile
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, expect


class SimpleBrowserTestRunner:
    """Simple browser automation test runner."""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            "start_time": datetime.now().isoformat(),
            "tests": {},
            "errors": [],
            "warnings": []
        }
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(__file__).parent.parent
        
    def log(self, message, level="INFO"):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def test_playwright_basic_functionality(self):
        """Test basic Playwright functionality."""
        self.log("Testing basic Playwright functionality...")
        
        try:
            with sync_playwright() as p:
                # Test Chromium
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<h1>Test</h1>")
                
                # Verify page content
                title = page.title()
                content = page.content()
                
                assert "Test" in content
                browser.close()
                
            self.log("✓ Basic Playwright functionality test passed")
            self.results["tests"]["playwright_basic"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"✗ Basic Playwright functionality test failed: {str(e)}", "ERROR")
            self.results["tests"]["playwright_basic"] = "FAIL"
            self.results["errors"].append(f"Playwright basic: {str(e)}")
            return False
    
    def test_browser_navigation(self):
        """Test browser navigation."""
        self.log("Testing browser navigation...")
        
        # Create test HTML file
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Navigation Test</title></head>
        <body>
            <h1>Navigation Test</h1>
            <p>This is a test page for navigation.</p>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "navigation_test.html"
        test_file.write_text(test_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to test file
                page.goto(f"file://{test_file}")
                
                # Verify navigation
                title = page.title()
                content = page.content()
                
                assert "Navigation Test" in title
                assert "Navigation Test" in content
                assert "This is a test page" in content
                
                browser.close()
                
            self.log("✓ Browser navigation test passed")
            self.results["tests"]["browser_navigation"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"✗ Browser navigation test failed: {str(e)}", "ERROR")
            self.results["tests"]["browser_navigation"] = "FAIL"
            self.results["errors"].append(f"Browser navigation: {str(e)}")
            return False
    
    def test_browser_interaction(self):
        """Test browser interaction."""
        self.log("Testing browser interaction...")
        
        # Create test HTML file with interaction
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Interaction Test</title></head>
        <body>
            <h1>Interaction Test</h1>
            <button id="test-button">Click Me</button>
            <div id="result" style="display: none;">Button clicked!</div>
            <script>
                document.getElementById('test-button').addEventListener('click', function() {
                    document.getElementById('result').style.display = 'block';
                });
            </script>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "interaction_test.html"
        test_file.write_text(test_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to test file
                page.goto(f"file://{test_file}")
                
                # Test interaction
                page.click("#test-button")
                
                # Verify result
                result_visible = page.is_visible("#result")
                result_text = page.text_content("#result")
                
                assert result_visible
                assert "Button clicked!" in result_text
                
                browser.close()
                
            self.log("✓ Browser interaction test passed")
            self.results["tests"]["browser_interaction"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"✗ Browser interaction test failed: {str(e)}", "ERROR")
            self.results["tests"]["browser_interaction"] = "FAIL"
            self.results["errors"].append(f"Browser interaction: {str(e)}")
            return False
    
    def test_browser_screenshot(self):
        """Test browser screenshot functionality."""
        self.log("Testing browser screenshot functionality...")
        
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Screenshot Test</title></head>
        <body>
            <h1>Screenshot Test</h1>
            <div style="width: 200px; height: 100px; background-color: red;">
                Red Box
            </div>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "screenshot_test.html"
        test_file.write_text(test_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to test file
                page.goto(f"file://{test_file}")
                
                # Take screenshot
                screenshot_path = Path(self.temp_dir) / "test_screenshot.png"
                page.screenshot(path=str(screenshot_path))
                
                # Verify screenshot was created
                assert screenshot_path.exists()
                assert screenshot_path.stat().st_size > 0
                
                browser.close()
                
            self.log("✓ Browser screenshot test passed")
            self.results["tests"]["browser_screenshot"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"✗ Browser screenshot test failed: {str(e)}", "ERROR")
            self.results["tests"]["browser_screenshot"] = "FAIL"
            self.results["errors"].append(f"Browser screenshot: {str(e)}")
            return False
    
    def test_cross_browser_basic(self):
        """Test basic cross-browser functionality."""
        self.log("Testing basic cross-browser functionality...")
        
        browsers = ["chromium", "firefox", "webkit"]
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Cross Browser Test</title></head>
        <body>
            <h1>Cross Browser Test</h1>
            <p>Testing across different browsers.</p>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "cross_browser_test.html"
        test_file.write_text(test_html)
        
        try:
            with sync_playwright() as p:
                for browser_name in browsers:
                    self.log(f"Testing {browser_name}...")
                    
                    browser = getattr(p, browser_name).launch(headless=True)
                    page = browser.new_page()
                    
                    # Navigate to test page
                    page.goto(f"file://{test_file}")
                    
                    # Verify basic functionality
                    title = page.title()
                    content = page.content()
                    
                    assert "Cross Browser Test" in title
                    assert "Cross Browser Test" in content
                    
                    browser.close()
                    
                    self.log(f"✓ {browser_name} test passed")
                    self.results["tests"][f"cross_browser_{browser_name}"] = "PASS"
            
            self.log("✓ Cross-browser functionality test passed")
            return True
            
        except Exception as e:
            self.log(f"✗ Cross-browser functionality test failed: {str(e)}", "ERROR")
            self.results["tests"]["cross_browser_functionality"] = "FAIL"
            self.results["errors"].append(f"Cross-browser functionality: {str(e)}")
            return False
    
    def test_performance_basic(self):
        """Test basic performance metrics."""
        self.log("Testing basic performance metrics...")
        
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Performance Test</title></head>
        <body>
            <h1>Performance Test</h1>
            <div id="content">
                <p>Performance test content</p>
            </div>
            <script>
                // Simulate some processing
                for (let i = 0; i < 100; i++) {
                    const div = document.createElement('div');
                    div.textContent = 'Element ' + i;
                    document.body.appendChild(div);
                }
            </script>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "performance_test.html"
        test_file.write_text(test_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to test page
                page.goto(f"file://{test_file}")
                
                # Get basic performance metrics
                metrics = page.evaluate("""
                    () => {
                        const navigation = performance.getEntriesByType('navigation')[0];
                        return {
                            loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                            totalElements: document.querySelectorAll('*').length
                        };
                    }
                """)
                
                # Verify metrics were collected
                assert isinstance(metrics, dict)
                assert "loadTime" in metrics
                assert "totalElements" in metrics
                assert metrics["totalElements"] > 100
                
                browser.close()
                
                self.log("✓ Basic performance metrics test passed")
                self.results["tests"]["performance_basic"] = "PASS"
                return True
                
        except Exception as e:
            self.log(f"✗ Basic performance metrics test failed: {str(e)}", "ERROR")
            self.results["tests"]["performance_basic"] = "FAIL"
            self.results["errors"].append(f"Performance basic: {str(e)}")
            return False
    
    def generate_report(self):
        """Generate test report."""
        self.log("Generating test report...")
        
        end_time = time.time()
        duration = end_time - self.start_time
        
        self.results["end_time"] = datetime.now().isoformat()
        self.results["duration"] = duration
        
        # Calculate test statistics
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for result in self.results["tests"].values() if result == "PASS")
        failed_tests = total_tests - passed_tests
        
        self.results["statistics"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        # Save report to file
        report_path = self.project_root / "assets" / "reports" / "simple_browser_test_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Generate summary
        self.log("=" * 60)
        self.log("SIMPLE BROWSER AUTOMATION TEST SUMMARY")
        self.log("=" * 60)
        self.log(f"Total Tests: {total_tests}")
        self.log(f"Passed: {passed_tests}")
        self.log(f"Failed: {failed_tests}")
        self.log(f"Success Rate: {self.results['statistics']['success_rate']:.1f}%")
        self.log(f"Duration: {duration:.2f} seconds")
        self.log(f"Report saved to: {report_path}")
        
        if self.results["errors"]:
            self.log("\nErrors:")
            for error in self.results["errors"]:
                self.log(f"  - {error}", "ERROR")
        
        if self.results["warnings"]:
            self.log("\nWarnings:")
            for warning in self.results["warnings"]:
                self.log(f"  - {warning}", "WARNING")
        
        self.log("=" * 60)
        
        return self.results["statistics"]["success_rate"] >= 80
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def run_all_tests(self):
        """Run all simple browser automation tests."""
        self.log("Starting simple browser automation testing...")
        
        try:
            # Run all test suites
            test_suites = [
                self.test_playwright_basic_functionality,
                self.test_browser_navigation,
                self.test_browser_interaction,
                self.test_browser_screenshot,
                self.test_cross_browser_basic,
                self.test_performance_basic
            ]
            
            for test_suite in test_suites:
                try:
                    test_suite()
                except Exception as e:
                    self.log(f"Test suite {test_suite.__name__} failed: {str(e)}", "ERROR")
                    self.results["errors"].append(f"{test_suite.__name__}: {str(e)}")
            
            # Generate report
            success = self.generate_report()
            
            return success
            
        finally:
            self.cleanup()


def main():
    """Main function to run simple browser automation tests."""
    runner = SimpleBrowserTestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        runner.log("Test execution interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        runner.log(f"Test execution failed: {str(e)}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
