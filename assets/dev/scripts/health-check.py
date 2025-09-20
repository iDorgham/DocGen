#!/usr/bin/env python3
"""
Health check script for DocGen CLI production deployment.
This script performs comprehensive health checks to ensure the system is running properly.
"""

import sys
import os
import time
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def check_cli_availability() -> Dict[str, Any]:
    """Check if CLI is available and responding."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'src.cli_main', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            'status': 'healthy' if result.returncode == 0 else 'unhealthy',
            'version': result.stdout.strip() if result.returncode == 0 else None,
            'error': result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'unhealthy',
            'error': 'CLI command timed out'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def check_dependencies() -> Dict[str, Any]:
    """Check if all required dependencies are available."""
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
        'status': 'healthy' if not missing_modules else 'unhealthy',
        'missing_modules': missing_modules,
        'total_modules': len(required_modules),
        'available_modules': len(required_modules) - len(missing_modules)
    }

def check_file_system() -> Dict[str, Any]:
    """Check file system permissions and structure."""
    required_paths = [
        'src/',
        'src/cli/',
        'src/core/',
        'src/models/',
        'src/templates/',
        'src/utils/',
        'assets/',
        'assets/templates/',
        'assets/specs/'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
    
    return {
        'status': 'healthy' if not missing_paths else 'unhealthy',
        'missing_paths': missing_paths,
        'total_paths': len(required_paths),
        'available_paths': len(required_paths) - len(missing_paths)
    }

def check_templates() -> Dict[str, Any]:
    """Check if templates are accessible and valid."""
    template_dir = Path('src/templates')
    if not template_dir.exists():
        return {
            'status': 'unhealthy',
            'error': 'Template directory not found'
        }
    
    template_files = list(template_dir.glob('*.j2'))
    if not template_files:
        return {
            'status': 'unhealthy',
            'error': 'No template files found'
        }
    
    # Try to load a template
    try:
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_files[0].name)
        return {
            'status': 'healthy',
            'template_count': len(template_files),
            'sample_template': template_files[0].name
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': f'Template loading failed: {str(e)}'
        }

def check_performance() -> Dict[str, Any]:
    """Check basic performance metrics."""
    start_time = time.time()
    
    # Test CLI help command performance
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'src.cli_main', '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        end_time = time.time()
        response_time = end_time - start_time
        
        return {
            'status': 'healthy' if result.returncode == 0 and response_time < 2.0 else 'unhealthy',
            'response_time': response_time,
            'performance_ok': response_time < 2.0,
            'error': result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'unhealthy',
            'error': 'Performance test timed out'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def run_health_checks() -> Dict[str, Any]:
    """Run all health checks and return comprehensive status."""
    checks = {
        'cli_availability': check_cli_availability(),
        'dependencies': check_dependencies(),
        'file_system': check_file_system(),
        'templates': check_templates(),
        'performance': check_performance()
    }
    
    # Overall status
    all_healthy = all(check['status'] == 'healthy' for check in checks.values())
    
    return {
        'overall_status': 'healthy' if all_healthy else 'unhealthy',
        'timestamp': time.time(),
        'checks': checks
    }

def main():
    """Main health check function."""
    print("Running DocGen CLI health checks...")
    
    health_status = run_health_checks()
    
    # Print results
    print(f"\nOverall Status: {health_status['overall_status'].upper()}")
    print(f"Timestamp: {time.ctime(health_status['timestamp'])}")
    
    for check_name, check_result in health_status['checks'].items():
        status_icon = "✅" if check_result['status'] == 'healthy' else "❌"
        print(f"\n{status_icon} {check_name.replace('_', ' ').title()}: {check_result['status']}")
        
        if check_result['status'] == 'unhealthy' and 'error' in check_result:
            print(f"   Error: {check_result['error']}")
        
        # Print additional details for specific checks
        if check_name == 'dependencies' and 'available_modules' in check_result:
            print(f"   Available modules: {check_result['available_modules']}/{check_result['total_modules']}")
        
        if check_name == 'file_system' and 'available_paths' in check_result:
            print(f"   Available paths: {check_result['available_paths']}/{check_result['total_paths']}")
        
        if check_name == 'templates' and 'template_count' in check_result:
            print(f"   Template count: {check_result['template_count']}")
        
        if check_name == 'performance' and 'response_time' in check_result:
            print(f"   Response time: {check_result['response_time']:.3f}s")
    
    # Exit with appropriate code
    sys.exit(0 if health_status['overall_status'] == 'healthy' else 1)

if __name__ == '__main__':
    main()
