"""
Browser Automation Integration Tests

This module contains comprehensive browser automation tests using Playwright
for end-to-end testing of the DocGen CLI project.
"""

import pytest
import tempfile
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect


class TestBrowserAutomation:
    """Test class for browser automation using Playwright."""
    
    @pytest.fixture(autouse=True)
    def setup_test_environment(self):
        """Set up test environment for browser automation."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_project_dir = Path(self.temp_dir) / "test_project"
        self.test_project_dir.mkdir()
        
        # Create a simple HTML file for testing
        self.test_html = self.test_project_dir / "index.html"
        self.test_html.write_text("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DocGen CLI Test</title>
        </head>
        <body>
            <h1>DocGen CLI Browser Test</h1>
            <button id="test-button">Click Me</button>
            <div id="result" style="display: none;">Button clicked!</div>
            <script>
                document.getElementById('test-button').addEventListener('click', function() {
                    document.getElementById('result').style.display = 'block';
                });
            </script>
        </body>
        </html>
        """)
        
        yield
        
        # Cleanup
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_browser_navigation(self):
        """Test basic browser navigation functionality."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the test HTML file
            page.goto(f"file://{self.test_html}")
            
            # Verify page title
            expect(page).to_have_title("DocGen CLI Test")
            
            # Verify page content
            expect(page.locator("h1")).to_contain_text("DocGen CLI Browser Test")
            
            browser.close()
    
    def test_browser_interaction(self):
        """Test browser interaction capabilities."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the test HTML file
            page.goto(f"file://{self.test_html}")
            
            # Click the button
            page.click("#test-button")
            
            # Verify the result
            expect(page.locator("#result")).to_be_visible()
            expect(page.locator("#result")).to_contain_text("Button clicked!")
            
            browser.close()
    
    def test_browser_screenshot(self):
        """Test browser screenshot functionality."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the test HTML file
            page.goto(f"file://{self.test_html}")
            
            # Take a screenshot
            screenshot_path = self.test_project_dir / "screenshot.png"
            page.screenshot(path=str(screenshot_path))
            
            # Verify screenshot was created
            assert screenshot_path.exists()
            assert screenshot_path.stat().st_size > 0
            
            browser.close()
    
    def test_browser_console_logs(self):
        """Test browser console log capture."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set up console log capture
            console_logs = []
            page.on("console", lambda msg: console_logs.append(msg.text))
            
            # Navigate to a page with console output
            page.goto(f"file://{self.test_html}")
            
            # Execute JavaScript to generate console output
            page.evaluate("console.log('Test console message')")
            
            # Verify console logs were captured
            assert len(console_logs) > 0
            assert any("Test console message" in log for log in console_logs)
            
            browser.close()
    
    def test_browser_network_requests(self):
        """Test browser network request monitoring."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set up network request monitoring
            requests = []
            page.on("request", lambda req: requests.append(req.url))
            
            # Navigate to a page
            page.goto(f"file://{self.test_html}")
            
            # Verify network requests were captured
            assert len(requests) > 0
            assert any("index.html" in req for req in requests)
            
            browser.close()
    
    def test_browser_multiple_tabs(self):
        """Test browser multiple tab functionality."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # Create first tab
            page1 = browser.new_page()
            page1.goto(f"file://{self.test_html}")
            
            # Create second tab
            page2 = browser.new_page()
            page2.goto(f"file://{self.test_html}")
            
            # Verify both tabs are working
            expect(page1.locator("h1")).to_contain_text("DocGen CLI Browser Test")
            expect(page2.locator("h1")).to_contain_text("DocGen CLI Browser Test")
            
            browser.close()
    
    def test_browser_responsive_design(self):
        """Test browser responsive design capabilities."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the test HTML file
            page.goto(f"file://{self.test_html}")
            
            # Test different viewport sizes
            page.set_viewport_size({"width": 320, "height": 568})  # Mobile
            mobile_screenshot = self.test_project_dir / "mobile_screenshot.png"
            page.screenshot(path=str(mobile_screenshot))
            
            page.set_viewport_size({"width": 1024, "height": 768})  # Desktop
            desktop_screenshot = self.test_project_dir / "desktop_screenshot.png"
            page.screenshot(path=str(desktop_screenshot))
            
            # Verify screenshots were created
            assert mobile_screenshot.exists()
            assert desktop_screenshot.exists()
            
            browser.close()
    
    def test_browser_error_handling(self):
        """Test browser error handling capabilities."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Test navigation to non-existent page
            try:
                page.goto("file:///non-existent-page.html", timeout=1000)
            except Exception as e:
                # Verify error was caught
                assert "net::ERR_FILE_NOT_FOUND" in str(e) or "Timeout" in str(e)
            
            browser.close()
    
    def test_browser_performance_metrics(self):
        """Test browser performance metrics collection."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the test HTML file
            page.goto(f"file://{self.test_html}")
            
            # Get performance metrics
            metrics = page.evaluate("""
                () => {
                    const navigation = performance.getEntriesByType('navigation')[0];
                    return {
                        loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
                    };
                }
            """)
            
            # Verify metrics were collected
            assert isinstance(metrics, dict)
            assert "loadTime" in metrics
            assert "domContentLoaded" in metrics
            
            browser.close()


class TestDocGenCLIBrowserIntegration:
    """Test class for DocGen CLI browser integration."""
    
    @pytest.fixture(autouse=True)
    def setup_cli_environment(self):
        """Set up CLI environment for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_project_dir = Path(self.temp_dir) / "test_project"
        self.test_project_dir.mkdir()
        
        # Create a sample project data file
        self.project_data = self.test_project_dir / "project_data.yaml"
        self.project_data.write_text("""
name: "Test Project"
description: "A test project for browser automation"
version: "1.0.0"
author: "Test Author"
license: "MIT"
repository: "https://github.com/test/test-project"
        """)
        
        yield
        
        # Cleanup
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cli_generate_command_browser_validation(self):
        """Test CLI generate command with browser validation."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Run CLI command to generate documentation
            result = subprocess.run([
                "python", "-m", "src.cli.main", "generate",
                "--project-data", str(self.project_data),
                "--output-dir", str(self.test_project_dir / "output"),
                "--template", "marketing"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            # Verify CLI command succeeded
            assert result.returncode == 0
            
            # Check if output files were created
            output_dir = self.test_project_dir / "output"
            if output_dir.exists():
                output_files = list(output_dir.glob("*.md"))
                assert len(output_files) > 0
                
                # Open generated documentation in browser
                for output_file in output_files:
                    page.goto(f"file://{output_file}")
                    expect(page.locator("body")).to_contain_text("Test Project")
            
            browser.close()
    
    def test_cli_validate_command_browser_validation(self):
        """Test CLI validate command with browser validation."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Run CLI validation command
            result = subprocess.run([
                "python", "-m", "src.cli.main", "validate",
                "--project-data", str(self.project_data)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            # Verify CLI command succeeded
            assert result.returncode == 0
            
            # Verify validation output
            assert "validation" in result.stdout.lower() or "valid" in result.stdout.lower()
            
            browser.close()
    
    def test_cli_project_command_browser_validation(self):
        """Test CLI project command with browser validation."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Run CLI project command
            result = subprocess.run([
                "python", "-m", "src.cli.main", "project",
                "--create",
                "--name", "Browser Test Project",
                "--output-dir", str(self.test_project_dir)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            # Verify CLI command succeeded
            assert result.returncode == 0
            
            # Check if project files were created
            project_files = list(self.test_project_dir.glob("*.yaml"))
            assert len(project_files) > 0
            
            browser.close()


@pytest.mark.integration
@pytest.mark.browser
class TestBrowserPerformance:
    """Test class for browser performance validation."""
    
    def test_browser_startup_performance(self):
        """Test browser startup performance."""
        start_time = time.time()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            browser.close()
        
        end_time = time.time()
        startup_time = end_time - start_time
        
        # Verify browser startup is reasonably fast (< 5 seconds)
        assert startup_time < 5.0
    
    def test_browser_memory_usage(self):
        """Test browser memory usage."""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to a simple page
            page.goto("data:text/html,<h1>Test</h1>")
            
            # Get memory usage after browser operations
            current_memory = process.memory_info().rss
            memory_increase = current_memory - initial_memory
            
            # Verify memory usage is reasonable (< 100MB increase)
            assert memory_increase < 100 * 1024 * 1024  # 100MB in bytes
            
            browser.close()
    
    def test_browser_concurrent_operations(self):
        """Test browser concurrent operations."""
        import threading
        import time
        
        results = []
        
        def browser_operation():
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<h1>Test</h1>")
                results.append("success")
                browser.close()
        
        # Start multiple browser operations concurrently
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=browser_operation)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all operations succeeded
        assert len(results) == 3
        assert all(result == "success" for result in results)
