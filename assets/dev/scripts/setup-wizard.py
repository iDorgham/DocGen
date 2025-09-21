#!/usr/bin/env python3
"""
Interactive Setup Wizard for DocGen CLI MCP Integration
Provides step-by-step guided configuration for all MCP servers with platform-specific instructions.

Features:
- Interactive setup wizard for each MCP server
- Step-by-step guided configuration
- Platform-specific setup instructions (Windows, macOS, Linux)
- Automated setup validation and testing
- Setup progress tracking and rollback capabilities
- Integration with authentication and key management systems

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import yaml
import platform
import subprocess
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.logging import RichHandler
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich.layout import Layout
    from rich.align import Align
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

class SetupStatus(Enum):
    """Setup status enumeration."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class PlatformType(Enum):
    """Platform type enumeration."""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"

@dataclass
class SetupStep:
    """Setup step information."""
    step_id: str
    title: str
    description: str
    platform_instructions: Dict[str, List[str]]
    validation_command: Optional[str] = None
    required: bool = True
    dependencies: List[str] = None

@dataclass
class SetupProgress:
    """Setup progress tracking."""
    server: str
    status: SetupStatus
    current_step: int
    total_steps: int
    completed_steps: List[str]
    failed_steps: List[str]
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None

class SetupWizard:
    """
    Interactive Setup Wizard for MCP Integration.
    
    Provides comprehensive setup guidance for all MCP servers with
    platform-specific instructions and automated validation.
    """
    
    def __init__(self, project_path: str = None, config_path: str = None):
        """
        Initialize Setup Wizard.
        
        Args:
            project_path: Path to the DocGen CLI project
            config_path: Path to MCP configuration file
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.config_path = config_path or os.path.join(
            self.project_path, 'assets', 'dev', 'config', 'mcp', 'mcp_config.yaml'
        )
        
        # Platform detection
        self.platform = self._detect_platform()
        
        # Setup configuration
        self.setup_steps: Dict[str, List[SetupStep]] = {}
        self.setup_progress: Dict[str, SetupProgress] = {}
        
        # Load configuration and setup steps
        self.load_configuration()
        self.initialize_setup_steps()
        
        logger.info(f"Setup Wizard initialized for {self.platform.value}")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def _detect_platform(self) -> PlatformType:
        """Detect the current platform."""
        system = platform.system().lower()
        if system == 'windows':
            return PlatformType.WINDOWS
        elif system == 'darwin':
            return PlatformType.MACOS
        elif system == 'linux':
            return PlatformType.LINUX
        else:
            return PlatformType.UNKNOWN
    
    def load_configuration(self):
        """Load MCP configuration."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info("MCP configuration loaded")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = {}
    
    def initialize_setup_steps(self):
        """Initialize setup steps for all MCP servers."""
        
        # Byterover setup steps
        self.setup_steps['byterover'] = [
            SetupStep(
                step_id="install_extension",
                title="Install Byterover Extension",
                description="Install the Byterover extension in your IDE",
                platform_instructions={
                    "windows": [
                        "1. Open VS Code or Cursor",
                        "2. Go to Extensions (Ctrl+Shift+X)",
                        "3. Search for 'Byterover'",
                        "4. Click 'Install' on the Byterover extension",
                        "5. Wait for installation to complete"
                    ],
                    "macos": [
                        "1. Open VS Code or Cursor",
                        "2. Go to Extensions (Cmd+Shift+X)",
                        "3. Search for 'Byterover'",
                        "4. Click 'Install' on the Byterover extension",
                        "5. Wait for installation to complete"
                    ],
                    "linux": [
                        "1. Open VS Code or Cursor",
                        "2. Go to Extensions (Ctrl+Shift+X)",
                        "3. Search for 'Byterover'",
                        "4. Click 'Install' on the Byterover extension",
                        "5. Wait for installation to complete"
                    ]
                },
                validation_command="Check if Byterover extension is installed"
            ),
            SetupStep(
                step_id="authenticate",
                title="Authenticate with Byterover",
                description="Login to your Byterover account through the extension",
                platform_instructions={
                    "windows": [
                        "1. Open the Byterover extension panel",
                        "2. Click 'Login' or 'Connect'",
                        "3. Follow the authentication flow in your browser",
                        "4. Complete the login process",
                        "5. Verify you see 'Authenticated' status"
                    ],
                    "macos": [
                        "1. Open the Byterover extension panel",
                        "2. Click 'Login' or 'Connect'",
                        "3. Follow the authentication flow in your browser",
                        "4. Complete the login process",
                        "5. Verify you see 'Authenticated' status"
                    ],
                    "linux": [
                        "1. Open the Byterover extension panel",
                        "2. Click 'Login' or 'Connect'",
                        "3. Follow the authentication flow in your browser",
                        "4. Complete the login process",
                        "5. Verify you see 'Authenticated' status"
                    ]
                },
                validation_command="Check Byterover authentication status"
            ),
            SetupStep(
                step_id="connect_workspace",
                title="Connect to Workspace",
                description="Ensure the extension is connected to your current workspace",
                platform_instructions={
                    "windows": [
                        "1. Open the Byterover extension settings",
                        "2. Verify workspace connection status",
                        "3. If not connected, click 'Connect to Workspace'",
                        "4. Confirm the connection is established"
                    ],
                    "macos": [
                        "1. Open the Byterover extension settings",
                        "2. Verify workspace connection status",
                        "3. If not connected, click 'Connect to Workspace'",
                        "4. Confirm the connection is established"
                    ],
                    "linux": [
                        "1. Open the Byterover extension settings",
                        "2. Verify workspace connection status",
                        "3. If not connected, click 'Connect to Workspace'",
                        "4. Confirm the connection is established"
                    ]
                },
                validation_command="Check workspace connection status"
            )
        ]
        
        # TestSprite setup steps
        self.setup_steps['testsprite'] = [
            SetupStep(
                step_id="create_account",
                title="Create TestSprite Account",
                description="Create an account on TestSprite if you don't have one",
                platform_instructions={
                    "windows": [
                        "1. Open your web browser",
                        "2. Go to https://www.testsprite.com",
                        "3. Click 'Sign Up' or 'Create Account'",
                        "4. Fill in your details and create account",
                        "5. Verify your email address"
                    ],
                    "macos": [
                        "1. Open your web browser",
                        "2. Go to https://www.testsprite.com",
                        "3. Click 'Sign Up' or 'Create Account'",
                        "4. Fill in your details and create account",
                        "5. Verify your email address"
                    ],
                    "linux": [
                        "1. Open your web browser",
                        "2. Go to https://www.testsprite.com",
                        "3. Click 'Sign Up' or 'Create Account'",
                        "4. Fill in your details and create account",
                        "5. Verify your email address"
                    ]
                },
                validation_command="Check if TestSprite account exists"
            ),
            SetupStep(
                step_id="get_api_key",
                title="Get API Key",
                description="Generate an API key from your TestSprite dashboard",
                platform_instructions={
                    "windows": [
                        "1. Login to your TestSprite account",
                        "2. Go to Dashboard > Settings > API Keys",
                        "3. Click 'Create New API Key'",
                        "4. Give it a descriptive name (e.g., 'DocGen CLI')",
                        "5. Copy the generated API key",
                        "6. Keep it secure - you won't see it again"
                    ],
                    "macos": [
                        "1. Login to your TestSprite account",
                        "2. Go to Dashboard > Settings > API Keys",
                        "3. Click 'Create New API Key'",
                        "4. Give it a descriptive name (e.g., 'DocGen CLI')",
                        "5. Copy the generated API key",
                        "6. Keep it secure - you won't see it again"
                    ],
                    "linux": [
                        "1. Login to your TestSprite account",
                        "2. Go to Dashboard > Settings > API Keys",
                        "3. Click 'Create New API Key'",
                        "4. Give it a descriptive name (e.g., 'DocGen CLI')",
                        "5. Copy the generated API key",
                        "6. Keep it secure - you won't see it again"
                    ]
                },
                validation_command="Check if API key is valid"
            ),
            SetupStep(
                step_id="set_environment",
                title="Set Environment Variable",
                description="Set the TESTSPRITE_API_KEY environment variable",
                platform_instructions={
                    "windows": [
                        "1. Open Command Prompt or PowerShell",
                        "2. Run: set TESTSPRITE_API_KEY=your_api_key_here",
                        "3. Or add to .env file: TESTSPRITE_API_KEY=your_api_key_here",
                        "4. Restart your terminal/IDE",
                        "5. Verify: echo %TESTSPRITE_API_KEY%"
                    ],
                    "macos": [
                        "1. Open Terminal",
                        "2. Run: export TESTSPRITE_API_KEY='your_api_key_here'",
                        "3. Or add to .env file: TESTSPRITE_API_KEY=your_api_key_here",
                        "4. Restart your terminal/IDE",
                        "5. Verify: echo $TESTSPRITE_API_KEY"
                    ],
                    "linux": [
                        "1. Open Terminal",
                        "2. Run: export TESTSPRITE_API_KEY='your_api_key_here'",
                        "3. Or add to .env file: TESTSPRITE_API_KEY=your_api_key_here",
                        "4. Restart your terminal/IDE",
                        "5. Verify: echo $TESTSPRITE_API_KEY"
                    ]
                },
                validation_command="Check environment variable is set"
            )
        ]
        
        # Playwright setup steps
        self.setup_steps['playwright'] = [
            SetupStep(
                step_id="install_playwright",
                title="Install Playwright",
                description="Install Playwright Python package",
                platform_instructions={
                    "windows": [
                        "1. Open Command Prompt or PowerShell",
                        "2. Run: pip install playwright",
                        "3. Wait for installation to complete",
                        "4. Verify: playwright --version"
                    ],
                    "macos": [
                        "1. Open Terminal",
                        "2. Run: pip install playwright",
                        "3. Wait for installation to complete",
                        "4. Verify: playwright --version"
                    ],
                    "linux": [
                        "1. Open Terminal",
                        "2. Run: pip install playwright",
                        "3. Wait for installation to complete",
                        "4. Verify: playwright --version"
                    ]
                },
                validation_command="Check Playwright installation"
            ),
            SetupStep(
                step_id="install_browsers",
                title="Install Browser Engines",
                description="Install browser engines for Playwright",
                platform_instructions={
                    "windows": [
                        "1. Run: playwright install chromium",
                        "2. Wait for browser download and installation",
                        "3. Optional: playwright install firefox webkit",
                        "4. Verify: playwright codegen"
                    ],
                    "macos": [
                        "1. Run: playwright install chromium",
                        "2. Wait for browser download and installation",
                        "3. Optional: playwright install firefox webkit",
                        "4. Verify: playwright codegen"
                    ],
                    "linux": [
                        "1. Run: playwright install chromium",
                        "2. Wait for browser download and installation",
                        "3. Optional: playwright install firefox webkit",
                        "4. Verify: playwright codegen"
                    ]
                },
                validation_command="Check browser installation"
            )
        ]
        
        # Context7 setup steps (no setup required)
        self.setup_steps['context7'] = [
            SetupStep(
                step_id="verify_access",
                title="Verify API Access",
                description="Context7 uses public API - no setup required",
                platform_instructions={
                    "windows": [
                        "1. Ensure internet connection is available",
                        "2. Context7 API is publicly accessible",
                        "3. No authentication required"
                    ],
                    "macos": [
                        "1. Ensure internet connection is available",
                        "2. Context7 API is publicly accessible",
                        "3. No authentication required"
                    ],
                    "linux": [
                        "1. Ensure internet connection is available",
                        "2. Context7 API is publicly accessible",
                        "3. No authentication required"
                    ]
                },
                validation_command="Check Context7 API connectivity",
                required=False
            )
        ]
        
        # Browser Tools setup steps
        self.setup_steps['browser_tools'] = [
            SetupStep(
                step_id="verify_browser",
                title="Verify Browser Installation",
                description="Browser Tools uses local browser - verify browser is installed",
                platform_instructions={
                    "windows": [
                        "1. Check if Chrome, Firefox, or Edge is installed",
                        "2. Browser Tools will use the default browser",
                        "3. No additional setup required"
                    ],
                    "macos": [
                        "1. Check if Chrome, Firefox, or Safari is installed",
                        "2. Browser Tools will use the default browser",
                        "3. No additional setup required"
                    ],
                    "linux": [
                        "1. Check if Chrome, Firefox, or Chromium is installed",
                        "2. Browser Tools will use the default browser",
                        "3. No additional setup required"
                    ]
                },
                validation_command="Check browser availability",
                required=False
            )
        ]
        
        # Dart setup steps
        self.setup_steps['dart'] = [
            SetupStep(
                step_id="verify_workspace",
                title="Verify Workspace Configuration",
                description="Dart uses workspace-based authentication",
                platform_instructions={
                    "windows": [
                        "1. Ensure you're in a valid project workspace",
                        "2. Dart will automatically detect workspace",
                        "3. No additional setup required"
                    ],
                    "macos": [
                        "1. Ensure you're in a valid project workspace",
                        "2. Dart will automatically detect workspace",
                        "3. No additional setup required"
                    ],
                    "linux": [
                        "1. Ensure you're in a valid project workspace",
                        "2. Dart will automatically detect workspace",
                        "3. No additional setup required"
                    ]
                },
                validation_command="Check workspace configuration",
                required=False
            )
        ]
        
        logger.info(f"Initialized setup steps for {len(self.setup_steps)} servers")
    
    def display_welcome(self):
        """Display welcome message and overview."""
        if not self.console:
            print("\n=== DocGen CLI MCP Setup Wizard ===")
            print("This wizard will guide you through setting up MCP servers for DocGen CLI.")
            print(f"Platform: {self.platform.value}")
            return
        
        welcome_text = """
🔧 DocGen CLI MCP Setup Wizard

This interactive wizard will guide you through setting up all MCP servers
required for the DocGen CLI project. Each server will be configured with
platform-specific instructions and automated validation.

The setup process includes:
• Byterover: Extension-based authentication
• TestSprite: API key authentication  
• Playwright: Local installation
• Context7: Public API (no setup)
• Browser Tools: Local browser access
• Dart: Workspace-based authentication
        """.strip()
        
        platform_info = f"Platform: {self.platform.value.title()}"
        
        self.console.print(Panel(welcome_text, title="Welcome", border_style="blue"))
        self.console.print(Panel(platform_info, border_style="green"))
    
    def display_server_menu(self) -> str:
        """Display server selection menu."""
        if not self.console:
            print("\nAvailable MCP servers:")
            for i, server in enumerate(self.setup_steps.keys(), 1):
                print(f"  {i}. {server}")
            choice = input("Select server (1-{}): ".format(len(self.setup_steps)))
            try:
                server_index = int(choice) - 1
                return list(self.setup_steps.keys())[server_index]
            except (ValueError, IndexError):
                return None
        
        # Create server selection table
        table = Table(title="Select MCP Server to Setup")
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Server", style="green", width=15)
        table.add_column("Description", style="yellow", width=40)
        table.add_column("Status", style="magenta", width=15)
        
        for i, (server, steps) in enumerate(self.setup_steps.items(), 1):
            # Get server description from config
            server_config = self.config.get('servers', {}).get(server, {})
            description = server_config.get('description', f'{server} MCP server')
            
            # Check setup status
            if server in self.setup_progress:
                status = self.setup_progress[server].status.value
            else:
                status = "not_started"
            
            table.add_row(
                str(i),
                server,
                description,
                status
            )
        
        self.console.print(table)
        
        # Get user selection
        choice = Prompt.ask(
            "Select server to setup",
            choices=[str(i) for i in range(1, len(self.setup_steps) + 1)]
        )
        
        server_index = int(choice) - 1
        return list(self.setup_steps.keys())[server_index]
    
    def run_server_setup(self, server: str) -> bool:
        """Run setup for a specific server."""
        if server not in self.setup_steps:
            logger.error(f"Unknown server: {server}")
            return False
        
        steps = self.setup_steps[server]
        
        # Initialize progress tracking
        self.setup_progress[server] = SetupProgress(
            server=server,
            status=SetupStatus.IN_PROGRESS,
            current_step=0,
            total_steps=len(steps),
            completed_steps=[],
            failed_steps=[],
            start_time=datetime.now()
        )
        
        if not self.console:
            print(f"\n=== Setting up {server} ===")
            print(f"Total steps: {len(steps)}")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=self.console,
                transient=True
            ) as progress:
                
                task = progress.add_task(f"Setting up {server}", total=len(steps))
                
                for i, step in enumerate(steps):
                    self.setup_progress[server].current_step = i + 1
                    progress.update(task, description=f"Step {i+1}: {step.title}")
                    
                    # Display step instructions
                    if not self.run_setup_step(server, step):
                        self.setup_progress[server].failed_steps.append(step.step_id)
                        if step.required:
                            self.setup_progress[server].status = SetupStatus.FAILED
                            self.setup_progress[server].error_message = f"Required step failed: {step.title}"
                            return False
                    else:
                        self.setup_progress[server].completed_steps.append(step.step_id)
                    
                    progress.advance(task)
            
            # Mark as completed
            self.setup_progress[server].status = SetupStatus.COMPLETED
            self.setup_progress[server].end_time = datetime.now()
            
            if not self.console:
                print(f"✅ {server} setup completed successfully!")
            else:
                self.console.print(f"✅ [green]{server} setup completed successfully![/green]")
            
            return True
            
        except Exception as e:
            self.setup_progress[server].status = SetupStatus.FAILED
            self.setup_progress[server].error_message = str(e)
            self.setup_progress[server].end_time = datetime.now()
            
            logger.error(f"Setup failed for {server}: {e}")
            return False
    
    def run_setup_step(self, server: str, step: SetupStep) -> bool:
        """Run a single setup step."""
        if not self.console:
            print(f"\n--- {step.title} ---")
            print(step.description)
            print("\nInstructions:")
            for instruction in step.platform_instructions.get(self.platform.value, []):
                print(f"  {instruction}")
            
            if step.validation_command:
                print(f"\nValidation: {step.validation_command}")
            
            return Confirm.ask("Did you complete this step successfully?")
        
        # Display step information
        step_panel = Panel(
            f"{step.description}\n\n[bold]Platform:[/bold] {self.platform.value.title()}",
            title=step.title,
            border_style="blue"
        )
        self.console.print(step_panel)
        
        # Display platform-specific instructions
        instructions = step.platform_instructions.get(self.platform.value, [])
        if instructions:
            instruction_text = "\n".join(instructions)
            self.console.print(Panel(instruction_text, title="Instructions", border_style="yellow"))
        
        # Display validation command if available
        if step.validation_command:
            self.console.print(Panel(
                f"Validation: {step.validation_command}",
                title="Validation",
                border_style="green"
            ))
        
        # Ask for confirmation
        if step.required:
            return Confirm.ask("Did you complete this step successfully?", default=True)
        else:
            return Confirm.ask("Did you complete this step successfully? (optional)", default=True)
    
    def validate_setup(self, server: str) -> bool:
        """Validate setup for a specific server."""
        if server not in self.setup_steps:
            return False
        
        # Import validation modules
        try:
            from real_time_auth_tracker import RealTimeAuthTracker
            from secure_key_manager import SecureKeyManager
            
            # Check authentication status
            auth_tracker = RealTimeAuthTracker()
            auth_status = auth_tracker.check_server_authentication(server)
            
            if auth_status and auth_status.status.value == 'authenticated':
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Validation error for {server}: {e}")
            return False
    
    def display_setup_summary(self):
        """Display setup summary for all servers."""
        if not self.console:
            print("\n=== Setup Summary ===")
            for server, progress in self.setup_progress.items():
                print(f"{server}: {progress.status.value}")
            return
        
        # Create summary table
        table = Table(title="Setup Summary")
        table.add_column("Server", style="cyan", width=15)
        table.add_column("Status", style="green", width=15)
        table.add_column("Progress", style="yellow", width=20)
        table.add_column("Duration", style="magenta", width=12)
        table.add_column("Error", style="red", width=30)
        
        for server, progress in self.setup_progress.items():
            # Status icon
            if progress.status == SetupStatus.COMPLETED:
                status_icon = "✅"
                status_color = "green"
            elif progress.status == SetupStatus.FAILED:
                status_icon = "❌"
                status_color = "red"
            elif progress.status == SetupStatus.IN_PROGRESS:
                status_icon = "🔄"
                status_color = "yellow"
            else:
                status_icon = "⏸️"
                status_color = "white"
            
            # Progress bar
            if progress.total_steps > 0:
                completed = len(progress.completed_steps)
                progress_text = f"{completed}/{progress.total_steps} steps"
            else:
                progress_text = "Not started"
            
            # Duration
            if progress.end_time:
                duration = progress.end_time - progress.start_time
                duration_text = str(duration).split('.')[0]  # Remove microseconds
            else:
                duration_text = "In progress"
            
            # Error message
            error_text = progress.error_message or ""
            if len(error_text) > 30:
                error_text = error_text[:27] + "..."
            
            table.add_row(
                server,
                f"{status_icon} {progress.status.value}",
                progress_text,
                duration_text,
                error_text
            )
        
        self.console.print(table)
    
    def save_setup_report(self, file_path: str = None):
        """Save setup report."""
        if not file_path:
            file_path = os.path.join(
                self.project_path, 'assets', 'reports', 'mcp',
                f'setup_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'platform': self.platform.value,
            'setup_progress': {server: asdict(progress) for server, progress in self.setup_progress.items()},
            'setup_steps': {
                server: [asdict(step) for step in steps] 
                for server, steps in self.setup_steps.items()
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Setup report saved to: {file_path}")
        return file_path
    
    def run_interactive_setup(self):
        """Run interactive setup wizard."""
        self.display_welcome()
        
        while True:
            # Display server menu
            server = self.display_server_menu()
            if not server:
                break
            
            # Run setup for selected server
            success = self.run_server_setup(server)
            
            if success:
                # Validate setup
                if self.validate_setup(server):
                    if self.console:
                        self.console.print(f"✅ [green]{server} setup validated successfully![/green]")
                else:
                    if self.console:
                        self.console.print(f"⚠️ [yellow]{server} setup completed but validation failed[/yellow]")
            
            # Ask if user wants to continue
            if not Confirm.ask("Setup another server?"):
                break
        
        # Display final summary
        self.display_setup_summary()
        
        # Save setup report
        report_path = self.save_setup_report()
        if self.console:
            self.console.print(f"\n📄 Setup report saved to: {report_path}")

def main():
    """Main function for Setup Wizard."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive Setup Wizard for MCP Servers")
    parser.add_argument('--server', type=str, help='Setup specific server')
    parser.add_argument('--interactive', action='store_true', help='Run interactive setup wizard')
    parser.add_argument('--validate', type=str, help='Validate setup for specific server')
    parser.add_argument('--summary', action='store_true', help='Show setup summary')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize setup wizard
        wizard = SetupWizard()
        
        if args.server:
            # Setup specific server
            success = wizard.run_server_setup(args.server)
            return 0 if success else 1
        elif args.interactive:
            # Run interactive setup
            wizard.run_interactive_setup()
            return 0
        elif args.validate:
            # Validate specific server
            success = wizard.validate_setup(args.validate)
            print(f"Validation for {args.validate}: {'PASSED' if success else 'FAILED'}")
            return 0 if success else 1
        elif args.summary:
            # Show setup summary
            wizard.display_setup_summary()
            return 0
        else:
            # Default: run interactive setup
            wizard.run_interactive_setup()
            return 0
        
    except Exception as e:
        logger.error(f"Error in Setup Wizard: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
