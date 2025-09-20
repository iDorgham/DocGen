#!/usr/bin/env python3
"""
Comprehensive Error Recovery System for DocGen CLI
Provides automatic retry mechanisms, circuit breaker patterns, and intelligent recovery strategies.

Features:
- Automatic retry mechanisms with exponential backoff
- Circuit breaker pattern for failing services
- Graceful degradation when services are unavailable
- Error classification and intelligent recovery strategies
- Recovery status reporting and monitoring
- Integration with MCP servers and authentication systems

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
from typing import Dict, List, Any, Optional, Callable, Union
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from functools import wraps
import traceback

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.logging import RichHandler
    from rich.text import Text
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

class ErrorType(Enum):
    """Error type classification."""
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    SERVICE_UNAVAILABLE = "service_unavailable"
    CONFIGURATION = "configuration"
    PERMISSION = "permission"
    VALIDATION = "validation"
    UNKNOWN = "unknown"

class RecoveryStrategy(Enum):
    """Recovery strategy types."""
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    MANUAL_INTERVENTION = "manual_intervention"

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service is back

@dataclass
class ErrorInfo:
    """Error information."""
    error_type: ErrorType
    error_message: str
    timestamp: datetime
    service: str
    operation: str
    retry_count: int = 0
    recovery_strategy: RecoveryStrategy = RecoveryStrategy.RETRY
    context: Dict[str, Any] = None

@dataclass
class RetryConfig:
    """Retry configuration."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    success_threshold: int = 3
    timeout: float = 30.0

@dataclass
class RecoveryAction:
    """Recovery action information."""
    action_id: str
    service: str
    operation: str
    strategy: RecoveryStrategy
    timestamp: datetime
    success: bool
    details: str
    duration: float
    error_info: Optional[ErrorInfo] = None

class CircuitBreaker:
    """Circuit breaker implementation."""
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None
        
    def can_execute(self) -> bool:
        """Check if operation can be executed."""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if (self.last_failure_time and 
                time.time() - self.last_failure_time > self.config.recovery_timeout):
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True
        return False
    
    def on_success(self):
        """Handle successful operation."""
        self.last_success_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
    
    def on_failure(self):
        """Handle failed operation."""
        self.last_failure_time = time.time()
        self.failure_count += 1
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.state == CircuitState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current circuit breaker state information."""
        return {
            'name': self.name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time,
            'last_success_time': self.last_success_time,
            'can_execute': self.can_execute()
        }

class ErrorRecoverySystem:
    """
    Comprehensive Error Recovery System.
    
    Provides automatic retry mechanisms, circuit breaker patterns,
    and intelligent recovery strategies for MCP servers and operations.
    """
    
    def __init__(self, project_path: str = None, config_path: str = None):
        """
        Initialize Error Recovery System.
        
        Args:
            project_path: Path to the DocGen CLI project
            config_path: Path to MCP configuration file
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.config_path = config_path or os.path.join(
            self.project_path, 'assets', 'dev', 'config', 'mcp', 'mcp_config.yaml'
        )
        
        # Recovery configuration
        self.retry_configs: Dict[str, RetryConfig] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.recovery_actions: List[RecoveryAction] = []
        
        # Error tracking
        self.error_history: List[ErrorInfo] = []
        self.service_health: Dict[str, Dict[str, Any]] = {}
        
        # Recovery strategies
        self.recovery_strategies: Dict[ErrorType, RecoveryStrategy] = {
            ErrorType.NETWORK: RecoveryStrategy.RETRY,
            ErrorType.AUTHENTICATION: RecoveryStrategy.MANUAL_INTERVENTION,
            ErrorType.TIMEOUT: RecoveryStrategy.RETRY,
            ErrorType.RATE_LIMIT: RecoveryStrategy.RETRY,
            ErrorType.SERVICE_UNAVAILABLE: RecoveryStrategy.CIRCUIT_BREAKER,
            ErrorType.CONFIGURATION: RecoveryStrategy.MANUAL_INTERVENTION,
            ErrorType.PERMISSION: RecoveryStrategy.MANUAL_INTERVENTION,
            ErrorType.VALIDATION: RecoveryStrategy.FALLBACK,
            ErrorType.UNKNOWN: RecoveryStrategy.RETRY
        }
        
        # Load configuration
        self.load_configuration()
        self.initialize_circuit_breakers()
        
        logger.info("Error Recovery System initialized")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def load_configuration(self):
        """Load recovery configuration from MCP config."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Load retry configurations
            servers = config.get('servers', {})
            for server_name, server_config in servers.items():
                retry_config = RetryConfig(
                    max_attempts=server_config.get('retry_attempts', 3),
                    base_delay=server_config.get('retry_delay', 1.0),
                    max_delay=server_config.get('max_retry_delay', 60.0),
                    exponential_base=server_config.get('retry_exponential_base', 2.0),
                    jitter=server_config.get('retry_jitter', True)
                )
                self.retry_configs[server_name] = retry_config
            
            logger.info("Recovery configuration loaded")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Use default configurations
            for server_name in ['byterover', 'testsprite', 'context7', 'browser_tools', 'playwright', 'dart']:
                self.retry_configs[server_name] = RetryConfig()
    
    def initialize_circuit_breakers(self):
        """Initialize circuit breakers for all services."""
        circuit_config = CircuitBreakerConfig()
        
        for server_name in self.retry_configs.keys():
            self.circuit_breakers[server_name] = CircuitBreaker(server_name, circuit_config)
        
        logger.info(f"Initialized {len(self.circuit_breakers)} circuit breakers")
    
    def classify_error(self, error: Exception, service: str, operation: str) -> ErrorType:
        """Classify error type for appropriate recovery strategy."""
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # Network errors
        if any(keyword in error_str for keyword in ['connection', 'network', 'dns', 'timeout', 'unreachable']):
            return ErrorType.NETWORK
        
        # Authentication errors
        if any(keyword in error_str for keyword in ['auth', 'unauthorized', 'forbidden', 'credential', 'token']):
            return ErrorType.AUTHENTICATION
        
        # Timeout errors
        if any(keyword in error_str for keyword in ['timeout', 'timed out', 'deadline']):
            return ErrorType.TIMEOUT
        
        # Rate limit errors
        if any(keyword in error_str for keyword in ['rate limit', 'too many requests', 'quota']):
            return ErrorType.RATE_LIMIT
        
        # Service unavailable errors
        if any(keyword in error_str for keyword in ['service unavailable', '503', '502', '500']):
            return ErrorType.SERVICE_UNAVAILABLE
        
        # Configuration errors
        if any(keyword in error_str for keyword in ['config', 'configuration', 'missing', 'invalid']):
            return ErrorType.CONFIGURATION
        
        # Permission errors
        if any(keyword in error_str for keyword in ['permission', 'access denied', 'not allowed']):
            return ErrorType.PERMISSION
        
        # Validation errors
        if any(keyword in error_str for keyword in ['validation', 'invalid', 'malformed']):
            return ErrorType.VALIDATION
        
        return ErrorType.UNKNOWN
    
    def calculate_retry_delay(self, attempt: int, config: RetryConfig) -> float:
        """Calculate retry delay with exponential backoff and jitter."""
        delay = config.base_delay * (config.exponential_base ** attempt)
        delay = min(delay, config.max_delay)
        
        if config.jitter:
            # Add random jitter (±25%)
            import random
            jitter = delay * 0.25 * (2 * random.random() - 1)
            delay += jitter
        
        return max(0, delay)
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry and exponential backoff."""
        service = kwargs.get('service', 'unknown')
        operation = kwargs.get('operation', 'unknown')
        
        config = self.retry_configs.get(service, RetryConfig())
        circuit_breaker = self.circuit_breakers.get(service)
        
        last_error = None
        
        for attempt in range(config.max_attempts):
            try:
                # Check circuit breaker
                if circuit_breaker and not circuit_breaker.can_execute():
                    raise Exception(f"Circuit breaker is open for {service}")
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Record success
                if circuit_breaker:
                    circuit_breaker.on_success()
                
                # Update service health
                self.update_service_health(service, True, operation)
                
                return result
                
            except Exception as e:
                last_error = e
                
                # Record failure
                if circuit_breaker:
                    circuit_breaker.on_failure()
                
                # Update service health
                self.update_service_health(service, False, operation, str(e))
                
                # Classify error
                error_type = self.classify_error(e, service, operation)
                error_info = ErrorInfo(
                    error_type=error_type,
                    error_message=str(e),
                    timestamp=datetime.now(),
                    service=service,
                    operation=operation,
                    retry_count=attempt + 1,
                    recovery_strategy=self.recovery_strategies.get(error_type, RecoveryStrategy.RETRY)
                )
                
                self.error_history.append(error_info)
                
                # Check if we should retry
                if attempt < config.max_attempts - 1:
                    delay = self.calculate_retry_delay(attempt, config)
                    logger.warning(f"Attempt {attempt + 1} failed for {service}.{operation}: {e}. Retrying in {delay:.2f}s")
                    time.sleep(delay)
                else:
                    logger.error(f"All {config.max_attempts} attempts failed for {service}.{operation}: {e}")
                    break
        
        # All retries failed
        if last_error:
            raise last_error
    
    def update_service_health(self, service: str, success: bool, operation: str, error: str = None):
        """Update service health information."""
        if service not in self.service_health:
            self.service_health[service] = {
                'total_operations': 0,
                'successful_operations': 0,
                'failed_operations': 0,
                'last_success': None,
                'last_failure': None,
                'error_rate': 0.0,
                'operations': []
            }
        
        health = self.service_health[service]
        health['total_operations'] += 1
        
        if success:
            health['successful_operations'] += 1
            health['last_success'] = datetime.now()
        else:
            health['failed_operations'] += 1
            health['last_failure'] = datetime.now()
            health['operations'].append({
                'operation': operation,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
        
        # Calculate error rate
        if health['total_operations'] > 0:
            health['error_rate'] = health['failed_operations'] / health['total_operations']
        
        # Keep only last 100 operations
        if len(health['operations']) > 100:
            health['operations'] = health['operations'][-100:]
    
    def execute_with_recovery(self, func: Callable, service: str, operation: str, 
                            *args, **kwargs) -> Any:
        """Execute function with comprehensive error recovery."""
        start_time = time.time()
        action_id = f"{service}_{operation}_{int(start_time)}"
        
        try:
            # Execute with retry
            result = self.retry_with_backoff(func, *args, service=service, operation=operation, **kwargs)
            
            # Record successful recovery action
            recovery_action = RecoveryAction(
                action_id=action_id,
                service=service,
                operation=operation,
                strategy=RecoveryStrategy.RETRY,
                timestamp=datetime.now(),
                success=True,
                details="Operation completed successfully",
                duration=time.time() - start_time
            )
            self.recovery_actions.append(recovery_action)
            
            return result
            
        except Exception as e:
            # Record failed recovery action
            error_type = self.classify_error(e, service, operation)
            strategy = self.recovery_strategies.get(error_type, RecoveryStrategy.RETRY)
            
            recovery_action = RecoveryAction(
                action_id=action_id,
                service=service,
                operation=operation,
                strategy=strategy,
                timestamp=datetime.now(),
                success=False,
                details=f"Recovery failed: {str(e)}",
                duration=time.time() - start_time,
                error_info=ErrorInfo(
                    error_type=error_type,
                    error_message=str(e),
                    timestamp=datetime.now(),
                    service=service,
                    operation=operation,
                    recovery_strategy=strategy
                )
            )
            self.recovery_actions.append(recovery_action)
            
            # Log recovery failure
            logger.error(f"Recovery failed for {service}.{operation}: {e}")
            
            # Implement fallback strategies
            if strategy == RecoveryStrategy.FALLBACK:
                return self.execute_fallback(service, operation, e)
            elif strategy == RecoveryStrategy.GRACEFUL_DEGRADATION:
                return self.execute_graceful_degradation(service, operation, e)
            elif strategy == RecoveryStrategy.MANUAL_INTERVENTION:
                self.request_manual_intervention(service, operation, e)
                raise
            
            raise
    
    def execute_fallback(self, service: str, operation: str, error: Exception) -> Any:
        """Execute fallback strategy."""
        logger.info(f"Executing fallback for {service}.{operation}")
        
        # Implement service-specific fallbacks
        if service == 'byterover':
            # Fallback to local knowledge storage
            return self.fallback_to_local_storage(operation)
        elif service == 'testsprite':
            # Fallback to local testing
            return self.fallback_to_local_testing(operation)
        elif service == 'context7':
            # Fallback to cached documentation
            return self.fallback_to_cached_docs(operation)
        else:
            # Generic fallback
            return self.generic_fallback(service, operation, error)
    
    def execute_graceful_degradation(self, service: str, operation: str, error: Exception) -> Any:
        """Execute graceful degradation strategy."""
        logger.info(f"Executing graceful degradation for {service}.{operation}")
        
        # Return minimal functionality
        return {
            'service': service,
            'operation': operation,
            'status': 'degraded',
            'message': f'Service {service} is experiencing issues. Limited functionality available.',
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        }
    
    def request_manual_intervention(self, service: str, operation: str, error: Exception):
        """Request manual intervention for critical errors."""
        logger.critical(f"Manual intervention required for {service}.{operation}: {error}")
        
        # Create intervention request
        intervention_request = {
            'service': service,
            'operation': operation,
            'error': str(error),
            'timestamp': datetime.now().isoformat(),
            'priority': 'high',
            'action_required': 'manual_intervention'
        }
        
        # Save intervention request
        intervention_file = os.path.join(
            self.project_path, 'assets', 'reports', 'mcp',
            f'intervention_request_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        os.makedirs(os.path.dirname(intervention_file), exist_ok=True)
        with open(intervention_file, 'w') as f:
            json.dump(intervention_request, f, indent=2)
        
        logger.info(f"Intervention request saved to: {intervention_file}")
    
    def fallback_to_local_storage(self, operation: str) -> Any:
        """Fallback to local storage when Byterover is unavailable."""
        return {
            'service': 'byterover',
            'operation': operation,
            'status': 'fallback',
            'message': 'Using local storage fallback',
            'data': 'Local knowledge storage active'
        }
    
    def fallback_to_local_testing(self, operation: str) -> Any:
        """Fallback to local testing when TestSprite is unavailable."""
        return {
            'service': 'testsprite',
            'operation': operation,
            'status': 'fallback',
            'message': 'Using local testing fallback',
            'data': 'Local test execution active'
        }
    
    def fallback_to_cached_docs(self, operation: str) -> Any:
        """Fallback to cached documentation when Context7 is unavailable."""
        return {
            'service': 'context7',
            'operation': operation,
            'status': 'fallback',
            'message': 'Using cached documentation fallback',
            'data': 'Cached documentation active'
        }
    
    def generic_fallback(self, service: str, operation: str, error: Exception) -> Any:
        """Generic fallback for unknown services."""
        return {
            'service': service,
            'operation': operation,
            'status': 'fallback',
            'message': f'Generic fallback for {service}',
            'error': str(error),
            'data': 'Limited functionality available'
        }
    
    def get_recovery_summary(self) -> Dict[str, Any]:
        """Get comprehensive recovery system summary."""
        total_actions = len(self.recovery_actions)
        successful_actions = sum(1 for a in self.recovery_actions if a.success)
        failed_actions = total_actions - successful_actions
        
        # Circuit breaker status
        circuit_breaker_status = {}
        for name, cb in self.circuit_breakers.items():
            circuit_breaker_status[name] = cb.get_state_info()
        
        # Service health summary
        service_health_summary = {}
        for service, health in self.service_health.items():
            service_health_summary[service] = {
                'total_operations': health['total_operations'],
                'error_rate': health['error_rate'],
                'last_success': health['last_success'].isoformat() if health['last_success'] else None,
                'last_failure': health['last_failure'].isoformat() if health['last_failure'] else None
            }
        
        # Error type distribution
        error_type_distribution = {}
        for error in self.error_history:
            error_type = error.error_type.value
            error_type_distribution[error_type] = error_type_distribution.get(error_type, 0) + 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_recovery_actions': total_actions,
            'successful_actions': successful_actions,
            'failed_actions': failed_actions,
            'success_rate': successful_actions / total_actions if total_actions > 0 else 0,
            'circuit_breaker_status': circuit_breaker_status,
            'service_health': service_health_summary,
            'error_type_distribution': error_type_distribution,
            'total_errors': len(self.error_history),
            'recent_errors': len([e for e in self.error_history if (datetime.now() - e.timestamp).total_seconds() < 3600])
        }
    
    def display_recovery_dashboard(self):
        """Display error recovery system dashboard."""
        if not self.console:
            # Fallback to simple text output
            summary = self.get_recovery_summary()
            print(f"\nError Recovery System Summary:")
            print(f"  Total Actions: {summary['total_recovery_actions']}")
            print(f"  Success Rate: {summary['success_rate']:.1%}")
            print(f"  Total Errors: {summary['total_errors']}")
            print(f"  Recent Errors: {summary['recent_errors']}")
            return
        
        # Create dashboard layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="circuit_breakers", ratio=1),
            Layout(name="service_health", ratio=1),
            Layout(name="summary", ratio=1)
        )
        
        # Header
        header_text = Text("🛡️ Error Recovery System Dashboard", style="bold blue")
        layout["header"].update(Panel(header_text, border_style="blue"))
        
        # Circuit breakers table
        cb_table = Table(title="Circuit Breakers")
        cb_table.add_column("Service", style="cyan", width=12)
        cb_table.add_column("State", style="green", width=10)
        cb_table.add_column("Failures", style="yellow", width=8)
        cb_table.add_column("Can Execute", style="magenta", width=10)
        
        for name, cb in self.circuit_breakers.items():
            state_info = cb.get_state_info()
            state_icon = "🟢" if state_info['state'] == 'closed' else "🔴" if state_info['state'] == 'open' else "🟡"
            can_execute_icon = "✅" if state_info['can_execute'] else "❌"
            
            cb_table.add_row(
                name,
                f"{state_icon} {state_info['state']}",
                str(state_info['failure_count']),
                can_execute_icon
            )
        
        layout["circuit_breakers"].update(cb_table)
        
        # Service health table
        health_table = Table(title="Service Health")
        health_table.add_column("Service", style="cyan", width=12)
        health_table.add_column("Operations", style="blue", width=10)
        health_table.add_column("Error Rate", style="yellow", width=10)
        health_table.add_column("Last Success", style="green", width=12)
        
        for service, health in self.service_health.items():
            error_rate_color = "green" if health['error_rate'] < 0.1 else "yellow" if health['error_rate'] < 0.3 else "red"
            last_success = health['last_success'].strftime("%H:%M:%S") if health['last_success'] else "Never"
            
            health_table.add_row(
                service,
                str(health['total_operations']),
                f"[{error_rate_color}]{health['error_rate']:.1%}[/{error_rate_color}]",
                last_success
            )
        
        layout["service_health"].update(health_table)
        
        # Summary panel
        summary = self.get_recovery_summary()
        summary_text = f"""
Total Actions: {summary['total_recovery_actions']}
Successful: {summary['successful_actions']}
Failed: {summary['failed_actions']}
Success Rate: {summary['success_rate']:.1%}

Total Errors: {summary['total_errors']}
Recent Errors: {summary['recent_errors']}

Error Types:
{chr(10).join([f"  {error_type}: {count}" for error_type, count in summary['error_type_distribution'].items()])}
        """.strip()
        
        layout["summary"].update(Panel(summary_text, title="Summary", border_style="green"))
        
        # Footer
        footer_text = Text("Recovery system monitoring all MCP operations", style="dim")
        layout["footer"].update(Panel(footer_text, border_style="dim"))
        
        self.console.print(layout)
    
    def save_recovery_report(self, file_path: str = None):
        """Save recovery system report."""
        if not file_path:
            file_path = os.path.join(
                self.project_path, 'assets', 'reports', 'mcp',
                f'recovery_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.get_recovery_summary(),
            'recovery_actions': [asdict(action) for action in self.recovery_actions[-100:]],
            'error_history': [asdict(error) for error in self.error_history[-100:]],
            'service_health': self.service_health,
            'circuit_breakers': {name: cb.get_state_info() for name, cb in self.circuit_breakers.items()}
        }
        
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Recovery report saved to: {file_path}")
        return file_path

def with_recovery(service: str, operation: str = None):
    """Decorator for automatic error recovery."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            recovery_system = ErrorRecoverySystem()
            op_name = operation or func.__name__
            return recovery_system.execute_with_recovery(func, service, op_name, *args, **kwargs)
        return wrapper
    return decorator

def main():
    """Main function for Error Recovery System."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Error Recovery System for MCP Servers")
    parser.add_argument('--dashboard', action='store_true', help='Display recovery dashboard')
    parser.add_argument('--summary', action='store_true', help='Show recovery summary')
    parser.add_argument('--report', action='store_true', help='Generate recovery report')
    parser.add_argument('--test', action='store_true', help='Test recovery system')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize recovery system
        recovery_system = ErrorRecoverySystem()
        
        if args.dashboard:
            # Display dashboard
            recovery_system.display_recovery_dashboard()
        elif args.summary:
            # Show summary
            summary = recovery_system.get_recovery_summary()
            print(json.dumps(summary, indent=2))
        elif args.report:
            # Generate report
            report_path = recovery_system.save_recovery_report()
            print(f"Recovery report saved to: {report_path}")
        elif args.test:
            # Test recovery system
            def test_function():
                import random
                if random.random() < 0.7:  # 70% failure rate for testing
                    raise Exception("Simulated error for testing")
                return "Success"
            
            result = recovery_system.execute_with_recovery(test_function, "test_service", "test_operation")
            print(f"Test result: {result}")
        else:
            # Default: display dashboard
            recovery_system.display_recovery_dashboard()
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in Error Recovery System: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
