#!/usr/bin/env python3
"""
Comprehensive Authentication System for DocGen CLI
Integrates real-time authentication tracking, secure key management, error recovery, and setup wizard.

Features:
- Real-time authentication status monitoring
- Secure API key management with encryption
- Comprehensive error recovery with circuit breakers
- Interactive setup wizard with platform-specific instructions
- Unified dashboard and reporting system
- Integration with all MCP servers

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import yaml
import time
import asyncio
import logging
import threading
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.logging import RichHandler
    from rich.text import Text
    from rich.live import Live
except ImportError:
    print("Warning: Rich library not available. Install with: pip install rich")
    Console = None

# Import our custom modules
try:
    from real_time_auth_tracker import RealTimeAuthTracker, AuthStatus
    from secure_key_manager import SecureKeyManager, KeyStatus
    from error_recovery_system import ErrorRecoverySystem, ErrorType, RecoveryStrategy
    from setup_wizard import SetupWizard, SetupStatus
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all authentication system modules are available")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler()] if Console else [logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class SystemStatus(Enum):
    """Overall system status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class SystemHealth:
    """System health information."""
    overall_status: SystemStatus
    authentication_health: float
    key_management_health: float
    error_recovery_health: float
    setup_completion: float
    critical_services_healthy: int
    total_services: int
    last_updated: datetime
    issues: List[str] = None

class ComprehensiveAuthSystem:
    """
    Comprehensive Authentication System.
    
    Integrates all authentication, key management, error recovery,
    and setup components into a unified system.
    """
    
    def __init__(self, project_path: str = None, config_path: str = None):
        """
        Initialize Comprehensive Authentication System.
        
        Args:
            project_path: Path to the DocGen CLI project
            config_path: Path to MCP configuration file
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.config_path = config_path or os.path.join(
            self.project_path, 'assets', 'dev', 'config', 'mcp', 'mcp_config.yaml'
        )
        
        # Initialize subsystems
        self.auth_tracker = RealTimeAuthTracker(self.project_path, self.config_path)
        self.key_manager = SecureKeyManager(self.project_path, self.config_path)
        self.error_recovery = ErrorRecoverySystem(self.project_path, self.config_path)
        self.setup_wizard = SetupWizard(self.project_path, self.config_path)
        
        # System health tracking
        self.system_health: Optional[SystemHealth] = None
        self.health_check_interval = 60  # seconds
        self.health_check_running = False
        self.health_check_thread: Optional[threading.Thread] = None
        
        # Status change callbacks
        self.status_callbacks: List[Callable] = []
        
        # Load configuration
        self.load_configuration()
        
        logger.info("Comprehensive Authentication System initialized")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def load_configuration(self):
        """Load system configuration."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info("System configuration loaded")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = {}
    
    def add_status_callback(self, callback: Callable):
        """Add a callback for system status changes."""
        self.status_callbacks.append(callback)
        logger.info("System status callback added")
    
    def remove_status_callback(self, callback: Callable):
        """Remove a system status callback."""
        if callback in self.status_callbacks:
            self.status_callbacks.remove(callback)
            logger.info("System status callback removed")
    
    def notify_status_change(self, old_health: SystemHealth, new_health: SystemHealth):
        """Notify all callbacks of system status changes."""
        for callback in self.status_callbacks:
            try:
                callback(old_health, new_health)
            except Exception as e:
                logger.error(f"Error in status change callback: {e}")
    
    def calculate_system_health(self) -> SystemHealth:
        """Calculate overall system health."""
        # Get authentication health
        auth_summary = self.auth_tracker.get_authentication_summary()
        auth_health = auth_summary.get('average_health_score', 0.0)
        
        # Get key management health
        key_summary = self.key_manager.get_key_summary()
        key_health = 100.0 if key_summary['active_keys'] > 0 else 0.0
        
        # Get error recovery health
        recovery_summary = self.error_recovery.get_recovery_summary()
        recovery_health = recovery_summary.get('success_rate', 0.0) * 100
        
        # Get setup completion
        setup_completion = 0.0
        if self.setup_wizard.setup_progress:
            completed_setups = sum(1 for p in self.setup_wizard.setup_progress.values() 
                                 if p.status == SetupStatus.COMPLETED)
            setup_completion = (completed_setups / len(self.setup_wizard.setup_progress)) * 100
        
        # Calculate critical services health
        critical_services = ['byterover', 'testsprite']  # Critical services
        total_services = len(self.auth_tracker.auth_status)
        critical_healthy = 0
        
        for service in critical_services:
            if service in self.auth_tracker.auth_status:
                status = self.auth_tracker.auth_status[service].status
                if status == AuthStatus.AUTHENTICATED:
                    critical_healthy += 1
        
        # Calculate overall health score
        overall_health_score = (auth_health + key_health + recovery_health + setup_completion) / 4
        
        # Determine overall status
        if overall_health_score >= 80 and critical_healthy == len(critical_services):
            overall_status = SystemStatus.HEALTHY
        elif overall_health_score >= 50 and critical_healthy >= len(critical_services) // 2:
            overall_status = SystemStatus.DEGRADED
        elif overall_health_score >= 20:
            overall_status = SystemStatus.CRITICAL
        else:
            overall_status = SystemStatus.UNKNOWN
        
        # Identify issues
        issues = []
        if auth_health < 80:
            issues.append("Authentication system health below threshold")
        if key_health < 80:
            issues.append("Key management system health below threshold")
        if recovery_health < 80:
            issues.append("Error recovery system health below threshold")
        if setup_completion < 80:
            issues.append("Setup completion below threshold")
        if critical_healthy < len(critical_services):
            issues.append("Critical services not fully healthy")
        
        return SystemHealth(
            overall_status=overall_status,
            authentication_health=auth_health,
            key_management_health=key_health,
            error_recovery_health=recovery_health,
            setup_completion=setup_completion,
            critical_services_healthy=critical_healthy,
            total_services=total_services,
            last_updated=datetime.now(),
            issues=issues
        )
    
    def start_health_monitoring(self):
        """Start continuous health monitoring."""
        if self.health_check_running:
            logger.warning("Health monitoring already running")
            return
        
        self.health_check_running = True
        self.health_check_thread = threading.Thread(
            target=self._health_monitoring_worker,
            daemon=True,
            name="HealthMonitoring"
        )
        self.health_check_thread.start()
        
        logger.info("Health monitoring started")
    
    def stop_health_monitoring(self):
        """Stop health monitoring."""
        if not self.health_check_running:
            logger.warning("Health monitoring not running")
            return
        
        self.health_check_running = False
        if self.health_check_thread:
            self.health_check_thread.join(timeout=5)
        
        logger.info("Health monitoring stopped")
    
    def _health_monitoring_worker(self):
        """Background health monitoring worker."""
        logger.debug("Health monitoring worker started")
        
        while self.health_check_running:
            try:
                old_health = self.system_health
                new_health = self.calculate_system_health()
                
                # Check for status changes
                if old_health and old_health.overall_status != new_health.overall_status:
                    logger.info(f"System status changed: {old_health.overall_status.value} -> {new_health.overall_status.value}")
                    self.notify_status_change(old_health, new_health)
                
                self.system_health = new_health
                time.sleep(self.health_check_interval)
                
            except Exception as e:
                logger.error(f"Error in health monitoring worker: {e}")
                time.sleep(self.health_check_interval)
        
        logger.debug("Health monitoring worker stopped")
    
    def run_complete_setup(self) -> bool:
        """Run complete system setup."""
        logger.info("Starting complete system setup...")
        
        try:
            # Start health monitoring
            self.start_health_monitoring()
            
            # Run setup wizard
            self.setup_wizard.run_interactive_setup()
            
            # Validate all setups
            all_valid = True
            for server in self.setup_wizard.setup_steps.keys():
                if not self.setup_wizard.validate_setup(server):
                    logger.warning(f"Setup validation failed for {server}")
                    all_valid = False
            
            # Generate comprehensive report
            self.generate_comprehensive_report()
            
            logger.info("Complete system setup finished")
            return all_valid
            
        except Exception as e:
            logger.error(f"Error in complete setup: {e}")
            return False
    
    def display_unified_dashboard(self):
        """Display unified system dashboard."""
        if not self.console:
            # Fallback to simple text output
            health = self.system_health or self.calculate_system_health()
            print(f"\nSystem Health: {health.overall_status.value}")
            print(f"Authentication: {health.authentication_health:.1f}%")
            print(f"Key Management: {health.key_management_health:.1f}%")
            print(f"Error Recovery: {health.error_recovery_health:.1f}%")
            print(f"Setup Completion: {health.setup_completion:.1f}%")
            return
        
        # Create unified dashboard layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="system_health", ratio=1),
            Layout(name="auth_status", ratio=1),
            Layout(name="key_status", ratio=1)
        )
        
        # Header
        health = self.system_health or self.calculate_system_health()
        status_icon = "🟢" if health.overall_status == SystemStatus.HEALTHY else "🟡" if health.overall_status == SystemStatus.DEGRADED else "🔴"
        
        header_text = Text(f"🔐 Comprehensive Authentication System Dashboard {status_icon}", style="bold blue")
        layout["header"].update(Panel(header_text, border_style="blue"))
        
        # System health panel
        health_text = f"""
Overall Status: {health.overall_status.value.title()}
Authentication: {health.authentication_health:.1f}%
Key Management: {health.key_management_health:.1f}%
Error Recovery: {health.error_recovery_health:.1f}%
Setup Completion: {health.setup_completion:.1f}%

Critical Services: {health.critical_services_healthy}/{len(['byterover', 'testsprite'])}
Total Services: {health.total_services}

Issues:
{chr(10).join([f"• {issue}" for issue in health.issues]) if health.issues else "• No issues detected"}
        """.strip()
        
        layout["system_health"].update(Panel(health_text, title="System Health", border_style="green"))
        
        # Authentication status panel
        auth_summary = self.auth_tracker.get_authentication_summary()
        auth_text = f"""
Authenticated: {auth_summary['authenticated_servers']}/{auth_summary['total_servers']}
Setup Required: {auth_summary['setup_required']}
Errors: {auth_summary['error_servers']}
Health Score: {auth_summary['average_health_score']:.1f}%

Health Checks: {'🟢 Running' if auth_summary['health_check_running'] else '🔴 Stopped'}
Status Changes: {auth_summary['status_history_count']}
        """.strip()
        
        layout["auth_status"].update(Panel(auth_text, title="Authentication Status", border_style="blue"))
        
        # Key management status panel
        key_summary = self.key_manager.get_key_summary()
        key_text = f"""
Total Keys: {key_summary['total_keys']}
Active Keys: {key_summary['active_keys']}
Expired Keys: {key_summary['expired_keys']}
Rotated Keys: {key_summary['rotated_keys']}
Revoked Keys: {key_summary['revoked_keys']}

Audit Log: {key_summary['audit_log_entries']} entries
        """.strip()
        
        layout["key_status"].update(Panel(key_text, title="Key Management", border_style="yellow"))
        
        # Footer
        footer_text = Text("Press Ctrl+C to stop monitoring", style="dim")
        layout["footer"].update(Panel(footer_text, border_style="dim"))
        
        self.console.print(layout)
    
    def run_live_dashboard(self, refresh_interval: int = 10):
        """Run live unified dashboard."""
        if not self.console:
            logger.error("Rich console not available for live dashboard")
            return
        
        logger.info(f"Starting live unified dashboard (refresh: {refresh_interval}s)")
        
        # Start health monitoring
        self.start_health_monitoring()
        
        try:
            with Live(self.display_unified_dashboard, refresh_per_second=1/refresh_interval) as live:
                while True:
                    # Update dashboard
                    live.update(self.display_unified_dashboard())
                    time.sleep(refresh_interval)
                    
        except KeyboardInterrupt:
            logger.info("Live dashboard stopped by user")
        finally:
            # Stop health monitoring
            self.stop_health_monitoring()
    
    def generate_comprehensive_report(self, file_path: str = None):
        """Generate comprehensive system report."""
        if not file_path:
            file_path = os.path.join(
                self.project_path, 'assets', 'reports', 'mcp',
                f'comprehensive_auth_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Gather all system data
        system_health = self.calculate_system_health()
        auth_summary = self.auth_tracker.get_authentication_summary()
        key_summary = self.key_manager.get_key_summary()
        recovery_summary = self.error_recovery.get_recovery_summary()
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'system_health': asdict(system_health),
            'authentication_summary': auth_summary,
            'key_management_summary': key_summary,
            'error_recovery_summary': recovery_summary,
            'setup_progress': {
                server: asdict(progress) 
                for server, progress in self.setup_wizard.setup_progress.items()
            },
            'configuration': {
                'project_path': self.project_path,
                'config_path': self.config_path,
                'health_check_interval': self.health_check_interval,
                'health_check_running': self.health_check_running
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Comprehensive report saved to: {file_path}")
        return file_path
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        health = self.system_health or self.calculate_system_health()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_status': health.overall_status.value,
            'health_scores': {
                'authentication': health.authentication_health,
                'key_management': health.key_management_health,
                'error_recovery': health.error_recovery_health,
                'setup_completion': health.setup_completion
            },
            'service_status': {
                'critical_healthy': health.critical_services_healthy,
                'total_services': health.total_services
            },
            'issues': health.issues,
            'last_updated': health.last_updated.isoformat()
        }

def main():
    """Main function for Comprehensive Authentication System."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Authentication System for MCP Servers")
    parser.add_argument('--dashboard', action='store_true', help='Display unified dashboard')
    parser.add_argument('--live', action='store_true', help='Run live dashboard')
    parser.add_argument('--setup', action='store_true', help='Run complete system setup')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive report')
    parser.add_argument('--refresh', type=int, default=10, help='Dashboard refresh interval (seconds)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize comprehensive system
        auth_system = ComprehensiveAuthSystem()
        
        if args.live:
            # Run live dashboard
            auth_system.run_live_dashboard(args.refresh)
        elif args.dashboard:
            # Display dashboard
            auth_system.display_unified_dashboard()
        elif args.setup:
            # Run complete setup
            success = auth_system.run_complete_setup()
            return 0 if success else 1
        elif args.status:
            # Show system status
            status = auth_system.get_system_status()
            print(json.dumps(status, indent=2))
        elif args.report:
            # Generate report
            report_path = auth_system.generate_comprehensive_report()
            print(f"Comprehensive report saved to: {report_path}")
        else:
            # Default: display dashboard
            auth_system.display_unified_dashboard()
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in Comprehensive Authentication System: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
