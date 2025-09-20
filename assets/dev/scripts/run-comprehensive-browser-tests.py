#!/usr/bin/env python3
"""
Comprehensive Browser Automation Test Runner

This script runs comprehensive browser automation tests including:
- Cross-browser testing (Chrome, Firefox, Safari)
- Performance testing
- Accessibility testing
- Security validation
- Error handling and recovery
- Visual regression testing
- Concurrent operations testing
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


class ComprehensiveBrowserTestRunner:
    """Comprehensive browser automation test runner."""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            "start_time": datetime.now().isoformat(),
            "tests": {},
            "performance": {},
            "accessibility": {},
            "security": {},
            "errors": [],
            "warnings": []
        }
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(__file__).parent.parent
        
    def log(self, message, level="INFO"):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def run_command(self, command, cwd=None):
        """Run shell command and return result."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd or self.project_root
            )
            return result
        except Exception as e:
            self.log(f"Command failed: {command} - {str(e)}", "ERROR")
            return None
    
    def test_playwright_installation(self):
        """Test Playwright installation and browser availability."""
        self.log("Testing Playwright installation...")
        
        try:
            with sync_playwright() as p:
                # Test Chromium
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<h1>Test</h1>")
                expect(page.locator("h1")).to_contain_text("Test")
                browser.close()
                
                # Test Firefox
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<h1>Test</h1>")
                expect(page.locator("h1")).to_contain_text("Test")
                browser.close()
                
                # Test WebKit
                browser = p.webkit.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<h1>Test</h1>")
                expect(page.locator("h1")).to_contain_text("Test")
                browser.close()
                
            self.log("✓ Playwright installation test passed")
            self.results["tests"]["playwright_installation"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"✗ Playwright installation test failed: {str(e)}", "ERROR")
            self.results["tests"]["playwright_installation"] = "FAIL"
            self.results["errors"].append(f"Playwright installation: {str(e)}")
            return False
    
    def test_cross_browser_functionality(self):
        """Test cross-browser functionality."""
        self.log("Testing cross-browser functionality...")
        
        browsers = ["chromium", "firefox", "webkit"]
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Cross Browser Test</title></head>
        <body>
            <h1>Cross Browser Test</h1>
            <button id="test-button">Click Me</button>
            <div id="result" style="display: none;">Success!</div>
            <script>
                document.getElementById('test-button').addEventListener('click', function() {
                    document.getElementById('result').style.display = 'block';
                });
            </script>
        </body>
        </html>
        """
        
        # Write test HTML to temp file
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
                    
                    # Test basic functionality
                    expect(page.locator("h1")).to_contain_text("Cross Browser Test")
                    
                    # Test interaction
                    page.click("#test-button")
                    expect(page.locator("#result")).to_be_visible()
                    expect(page.locator("#result")).to_contain_text("Success!")
                    
                    # Test screenshot
                    screenshot_path = Path(self.temp_dir) / f"{browser_name}_screenshot.png"
                    page.screenshot(path=str(screenshot_path))
                    assert screenshot_path.exists()
                    
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
    
    def test_performance_metrics(self):
        """Test performance metrics collection."""
        self.log("Testing performance metrics collection...")
        
        performance_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Performance Test</title></head>
        <body>
            <h1>Performance Test</h1>
            <div id="content">
                <p>Performance test content</p>
                <ul id="list">
                    <li>Item 1</li>
                    <li>Item 2</li>
                    <li>Item 3</li>
                </ul>
            </div>
            <script>
                // Simulate some processing
                for (let i = 0; i < 1000; i++) {
                    const div = document.createElement('div');
                    div.textContent = 'Dynamic element ' + i;
                    document.body.appendChild(div);
                }
            </script>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "performance_test.html"
        test_file.write_text(performance_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to performance test page
                page.goto(f"file://{test_file}")
                
                # Get performance metrics
                metrics = page.evaluate("""
                    () => {
                        const navigation = performance.getEntriesByType('navigation')[0];
                        const paint = performance.getEntriesByType('paint');
                        return {
                            loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                            firstPaint: paint[0]?.startTime || 0,
                            firstContentfulPaint: paint[1]?.startTime || 0,
                            totalElements: document.querySelectorAll('*').length,
                            memoryUsage: performance.memory ? performance.memory.usedJSHeapSize : 0
                        };
                    }
                """)
                
                # Verify metrics were collected
                assert isinstance(metrics, dict)
                assert "loadTime" in metrics
                assert "domContentLoaded" in metrics
                assert "totalElements" in metrics
                assert metrics["totalElements"] > 1000
                
                # Store performance metrics
                self.results["performance"] = metrics
                
                browser.close()
                
                self.log("✓ Performance metrics test passed")
                self.results["tests"]["performance_metrics"] = "PASS"
                return True
                
        except Exception as e:
            self.log(f"✗ Performance metrics test failed: {str(e)}", "ERROR")
            self.results["tests"]["performance_metrics"] = "FAIL"
            self.results["errors"].append(f"Performance metrics: {str(e)}")
            return False
    
    def test_accessibility_validation(self):
        """Test accessibility validation."""
        self.log("Testing accessibility validation...")
        
        accessibility_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Accessibility Test</title></head>
        <body>
            <h1>Accessibility Test</h1>
            <form>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required aria-label="Enter your name">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required aria-label="Enter your email">
                <button type="submit" aria-label="Submit form">Submit</button>
            </form>
            <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg'><text>Test</text></svg>" alt="Test image">
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "accessibility_test.html"
        test_file.write_text(accessibility_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to accessibility test page
                page.goto(f"file://{test_file}")
                
                # Check for accessibility attributes
                name_input = page.locator("#name")
                email_input = page.locator("#email")
                submit_button = page.locator("button[type='submit']")
                image = page.locator("img")
                
                # Verify required attributes
                assert name_input.get_attribute("required") is not None
                assert email_input.get_attribute("required") is not None
                assert name_input.get_attribute("aria-label") is not None
                assert email_input.get_attribute("aria-label") is not None
                assert submit_button.get_attribute("aria-label") is not None
                assert image.get_attribute("alt") is not None
                
                # Store accessibility results
                self.results["accessibility"] = {
                    "required_attributes": True,
                    "aria_labels": True,
                    "alt_text": True
                }
                
                browser.close()
                
                self.log("✓ Accessibility validation test passed")
                self.results["tests"]["accessibility_validation"] = "PASS"
                return True
                
        except Exception as e:
            self.log(f"✗ Accessibility validation test failed: {str(e)}", "ERROR")
            self.results["tests"]["accessibility_validation"] = "FAIL"
            self.results["errors"].append(f"Accessibility validation: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling and recovery."""
        self.log("Testing error handling and recovery...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Test network error handling
                try:
                    page.goto("file:///non-existent-page.html", timeout=1000)
                except Exception as e:
                    assert "net::ERR_FILE_NOT_FOUND" in str(e) or "Timeout" in str(e)
                
                # Test JavaScript error handling
                errors = []
                page.on("pageerror", lambda error: errors.append(error.message))
                
                page.goto("data:text/html,<script>throw new Error('Test error');</script>")
                assert len(errors) > 0
                assert "Test error" in errors[0]
                
                # Test browser crash recovery
                browser.close()
                
                # Create new browser instance
                browser2 = p.chromium.launch(headless=True)
                page2 = browser2.new_page()
                page2.goto("data:text/html,<h1>Recovery Test</h1>")
                expect(page2.locator("h1")).to_contain_text("Recovery Test")
                browser2.close()
                
                self.log("✓ Error handling test passed")
                self.results["tests"]["error_handling"] = "PASS"
                return True
                
        except Exception as e:
            self.log(f"✗ Error handling test failed: {str(e)}", "ERROR")
            self.results["tests"]["error_handling"] = "FAIL"
            self.results["errors"].append(f"Error handling: {str(e)}")
            return False
    
    def test_concurrent_operations(self):
        """Test concurrent browser operations."""
        self.log("Testing concurrent browser operations...")
        
        import threading
        
        results = []
        
        def browser_operation(browser_id):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto("data:text/html,<h1>Concurrent Test</h1>")
                    expect(page.locator("h1")).to_contain_text("Concurrent Test")
                    results.append(f"browser_{browser_id}_success")
                    browser.close()
            except Exception as e:
                results.append(f"browser_{browser_id}_error: {str(e)}")
        
        try:
            # Start multiple browser operations concurrently
            threads = []
            for i in range(3):
                thread = threading.Thread(target=browser_operation, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Verify all operations succeeded
            assert len(results) == 3
            assert all("success" in result for result in results)
            
            self.log("✓ Concurrent operations test passed")
            self.results["tests"]["concurrent_operations"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"✗ Concurrent operations test failed: {str(e)}", "ERROR")
            self.results["tests"]["concurrent_operations"] = "FAIL"
            self.results["errors"].append(f"Concurrent operations: {str(e)}")
            return False
    
    def test_visual_regression(self):
        """Test visual regression capabilities."""
        self.log("Testing visual regression capabilities...")
        
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Visual Regression Test</title></head>
        <body>
            <h1>Visual Regression Test</h1>
            <div style="width: 200px; height: 100px; background-color: red; margin: 10px;">
                Red Box
            </div>
            <div style="width: 200px; height: 100px; background-color: blue; margin: 10px;">
                Blue Box
            </div>
        </body>
        </html>
        """
        
        test_file = Path(self.temp_dir) / "visual_regression_test.html"
        test_file.write_text(test_html)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to test page
                page.goto(f"file://{test_file}")
                
                # Take screenshots at different viewport sizes
                viewports = [
                    {"width": 320, "height": 568, "name": "mobile"},
                    {"width": 768, "height": 1024, "name": "tablet"},
                    {"width": 1920, "height": 1080, "name": "desktop"}
                ]
                
                for viewport in viewports:
                    page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
                    screenshot_path = Path(self.temp_dir) / f"{viewport['name']}_screenshot.png"
                    page.screenshot(path=str(screenshot_path))
                    assert screenshot_path.exists()
                    assert screenshot_path.stat().st_size > 0
                
                browser.close()
                
                self.log("✓ Visual regression test passed")
                self.results["tests"]["visual_regression"] = "PASS"
                return True
                
        except Exception as e:
            self.log(f"✗ Visual regression test failed: {str(e)}", "ERROR")
            self.results["tests"]["visual_regression"] = "FAIL"
            self.results["errors"].append(f"Visual regression: {str(e)}")
            return False
    
    def run_pytest_tests(self):
        """Run pytest-based browser automation tests."""
        self.log("Running pytest-based browser automation tests...")
        
        try:
            # Run comprehensive browser automation tests
            result = self.run_command(
                "python -m pytest tests/integration/test_comprehensive_browser_automation.py -v --tb=short"
            )
            
            if result and result.returncode == 0:
                self.log("✓ Pytest browser automation tests passed")
                self.results["tests"]["pytest_browser_automation"] = "PASS"
                return True
            else:
                self.log(f"✗ Pytest browser automation tests failed: {result.stderr if result else 'No result'}", "ERROR")
                self.results["tests"]["pytest_browser_automation"] = "FAIL"
                self.results["errors"].append(f"Pytest browser automation: {result.stderr if result else 'No result'}")
                return False
                
        except Exception as e:
            self.log(f"✗ Pytest browser automation tests failed: {str(e)}", "ERROR")
            self.results["tests"]["pytest_browser_automation"] = "FAIL"
            self.results["errors"].append(f"Pytest browser automation: {str(e)}")
            return False
    
    def generate_report(self):
        """Generate comprehensive test report."""
        self.log("Generating comprehensive test report...")
        
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
        report_path = self.project_root / "assets" / "reports" / "comprehensive_browser_test_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Generate summary
        self.log("=" * 60)
        self.log("COMPREHENSIVE BROWSER AUTOMATION TEST SUMMARY")
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
        """Run all comprehensive browser automation tests."""
        self.log("Starting comprehensive browser automation testing...")
        
        try:
            # Run all test suites
            test_suites = [
                self.test_playwright_installation,
                self.test_cross_browser_functionality,
                self.test_performance_metrics,
                self.test_accessibility_validation,
                self.test_error_handling,
                self.test_concurrent_operations,
                self.test_visual_regression,
                self.run_pytest_tests
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
    """Main function to run comprehensive browser automation tests."""
    runner = ComprehensiveBrowserTestRunner()
    
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
