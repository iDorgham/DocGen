#!/usr/bin/env python3
"""
Production monitoring script for DocGen CLI.
This script provides continuous monitoring and alerting for production deployments.
"""

import sys
import os
import time
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DocGenMonitor:
    """Production monitoring for DocGen CLI."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize the monitor with configuration."""
        self.config = self.load_config(config_file)
        self.metrics = {}
        self.alerts = []
        
    def load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load monitoring configuration."""
        default_config = {
            'check_interval': 60,  # seconds
            'health_check_timeout': 30,  # seconds
            'performance_threshold': 2.0,  # seconds
            'memory_threshold': 100,  # MB
            'cpu_threshold': 80,  # percentage
            'alert_webhook': None,
            'log_retention_days': 30
        }
        
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config file {config_file}: {e}")
        
        return default_config
    
    def check_cli_health(self) -> Dict[str, Any]:
        """Check CLI health and performance."""
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'src.cli_main', '--version'],
                capture_output=True,
                text=True,
                timeout=self.config['health_check_timeout']
            )
            
            response_time = time.time() - start_time
            
            return {
                'status': 'healthy' if result.returncode == 0 else 'unhealthy',
                'response_time': response_time,
                'version': result.stdout.strip() if result.returncode == 0 else None,
                'error': result.stderr if result.returncode != 0 else None,
                'timestamp': datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'unhealthy',
                'response_time': self.config['health_check_timeout'],
                'error': 'Health check timed out',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'response_time': time.time() - start_time,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage."""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / (1024 * 1024),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024 * 1024 * 1024),
                'timestamp': datetime.now().isoformat()
            }
        except ImportError:
            logger.warning("psutil not available, skipping system resource check")
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'memory_used_mb': 0,
                'disk_percent': 0,
                'disk_free_gb': 0,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"System resource check failed: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Check dependency availability."""
        required_modules = [
            'click', 'jinja2', 'yaml', 'rich', 'pydantic',
            'email_validator', 'requests', 'semantic_version',
            'markdown', 'numpy', 'sklearn', 'joblib', 'watchdog'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        return {
            'missing_modules': missing_modules,
            'total_modules': len(required_modules),
            'available_modules': len(required_modules) - len(missing_modules),
            'status': 'healthy' if not missing_modules else 'unhealthy',
            'timestamp': datetime.now().isoformat()
        }
    
    def check_file_system(self) -> Dict[str, Any]:
        """Check file system health."""
        required_paths = [
            'src/', 'src/cli/', 'src/core/', 'src/models/',
            'src/templates/', 'src/utils/', 'assets/',
            'assets/templates/', 'assets/specs/'
        ]
        
        missing_paths = []
        for path in required_paths:
            if not Path(path).exists():
                missing_paths.append(path)
        
        return {
            'missing_paths': missing_paths,
            'total_paths': len(required_paths),
            'available_paths': len(required_paths) - len(missing_paths),
            'status': 'healthy' if not missing_paths else 'unhealthy',
            'timestamp': datetime.now().isoformat()
        }
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect all monitoring metrics."""
        metrics = {
            'cli_health': self.check_cli_health(),
            'system_resources': self.check_system_resources(),
            'dependencies': self.check_dependencies(),
            'file_system': self.check_file_system(),
            'collection_time': datetime.now().isoformat()
        }
        
        # Store metrics
        self.metrics = metrics
        
        return metrics
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for alert conditions."""
        alerts = []
        
        # CLI health alerts
        if metrics['cli_health']['status'] == 'unhealthy':
            alerts.append({
                'type': 'cli_health',
                'severity': 'critical',
                'message': f"CLI health check failed: {metrics['cli_health'].get('error', 'Unknown error')}",
                'timestamp': datetime.now().isoformat()
            })
        
        # Performance alerts
        if metrics['cli_health']['response_time'] > self.config['performance_threshold']:
            alerts.append({
                'type': 'performance',
                'severity': 'warning',
                'message': f"CLI response time {metrics['cli_health']['response_time']:.2f}s exceeds threshold {self.config['performance_threshold']}s",
                'timestamp': datetime.now().isoformat()
            })
        
        # System resource alerts
        if 'system_resources' in metrics and 'cpu_percent' in metrics['system_resources']:
            cpu_percent = metrics['system_resources']['cpu_percent']
            if cpu_percent > self.config['cpu_threshold']:
                alerts.append({
                    'type': 'cpu_usage',
                    'severity': 'warning',
                    'message': f"CPU usage {cpu_percent}% exceeds threshold {self.config['cpu_threshold']}%",
                    'timestamp': datetime.now().isoformat()
                })
            
            memory_mb = metrics['system_resources'].get('memory_used_mb', 0)
            if memory_mb > self.config['memory_threshold']:
                alerts.append({
                    'type': 'memory_usage',
                    'severity': 'warning',
                    'message': f"Memory usage {memory_mb:.1f}MB exceeds threshold {self.config['memory_threshold']}MB",
                    'timestamp': datetime.now().isoformat()
                })
        
        # Dependency alerts
        if metrics['dependencies']['status'] == 'unhealthy':
            alerts.append({
                'type': 'dependencies',
                'severity': 'critical',
                'message': f"Missing dependencies: {', '.join(metrics['dependencies']['missing_modules'])}",
                'timestamp': datetime.now().isoformat()
            })
        
        # File system alerts
        if metrics['file_system']['status'] == 'unhealthy':
            alerts.append({
                'type': 'file_system',
                'severity': 'critical',
                'message': f"Missing paths: {', '.join(metrics['file_system']['missing_paths'])}",
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def send_alert(self, alert: Dict[str, Any]) -> bool:
        """Send alert notification."""
        logger.warning(f"ALERT [{alert['severity'].upper()}] {alert['type']}: {alert['message']}")
        
        # Store alert
        self.alerts.append(alert)
        
        # Send webhook if configured
        if self.config.get('alert_webhook'):
            try:
                import requests
                requests.post(
                    self.config['alert_webhook'],
                    json=alert,
                    timeout=10
                )
                logger.info(f"Alert sent to webhook: {alert['type']}")
            except Exception as e:
                logger.error(f"Failed to send webhook alert: {e}")
        
        return True
    
    def save_metrics(self, metrics: Dict[str, Any]) -> None:
        """Save metrics to file."""
        metrics_file = Path('metrics.json')
        
        # Load existing metrics
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    existing_metrics = json.load(f)
            except:
                existing_metrics = []
        else:
            existing_metrics = []
        
        # Add new metrics
        existing_metrics.append(metrics)
        
        # Keep only recent metrics (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        filtered_metrics = [
            m for m in existing_metrics
            if datetime.fromisoformat(m['collection_time']) > cutoff_time
        ]
        
        # Save metrics
        with open(metrics_file, 'w') as f:
            json.dump(filtered_metrics, f, indent=2)
    
    def cleanup_logs(self) -> None:
        """Clean up old log files."""
        log_dir = Path('.')
        cutoff_date = datetime.now() - timedelta(days=self.config['log_retention_days'])
        
        for log_file in log_dir.glob('*.log'):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                logger.info(f"Cleaned up old log file: {log_file}")
    
    def run_monitoring_cycle(self) -> None:
        """Run one monitoring cycle."""
        logger.info("Starting monitoring cycle...")
        
        # Collect metrics
        metrics = self.collect_metrics()
        
        # Check for alerts
        alerts = self.check_alerts(metrics)
        
        # Send alerts
        for alert in alerts:
            self.send_alert(alert)
        
        # Save metrics
        self.save_metrics(metrics)
        
        # Log summary
        overall_status = 'healthy' if not alerts else 'unhealthy'
        logger.info(f"Monitoring cycle complete. Status: {overall_status}, Alerts: {len(alerts)}")
    
    def run_continuous_monitoring(self) -> None:
        """Run continuous monitoring."""
        logger.info(f"Starting continuous monitoring (interval: {self.config['check_interval']}s)")
        
        try:
            while True:
                self.run_monitoring_cycle()
                time.sleep(self.config['check_interval'])
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            raise

def main():
    """Main monitoring function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor DocGen CLI production deployment')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--once', action='store_true', help='Run monitoring once instead of continuously')
    parser.add_argument('--interval', type=int, help='Monitoring interval in seconds')
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = DocGenMonitor(args.config)
    
    # Override interval if specified
    if args.interval:
        monitor.config['check_interval'] = args.interval
    
    # Run monitoring
    if args.once:
        monitor.run_monitoring_cycle()
    else:
        monitor.run_continuous_monitoring()

if __name__ == '__main__':
    main()
