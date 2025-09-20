#!/usr/bin/env python3
"""
Project Monitoring Script for DocGen CLI
Monitor project health, performance, and compliance
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class ProjectMonitor:
    def __init__(self):
        self.project_root = Path.cwd()
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'project_health': {},
            'performance': {},
            'compliance': {},
            'recommendations': []
        }
    
    def check_project_structure(self) -> Dict[str, Any]:
        """Check project structure compliance."""
        print("📁 Checking project structure...")
        
        structure_checks = {
            'src_directory': (self.project_root / 'src').exists(),
            'tests_directory': (self.project_root / 'tests').exists(),
            'docs_directory': (self.project_root / 'assets' / 'documentation').exists(),
            'config_files': {
                'pyproject_toml': (self.project_root / 'pyproject.toml').exists(),
                'requirements_txt': (self.project_root / 'requirements.txt').exists(),
                'gitignore': (self.project_root / '.gitignore').exists()
            },
            'template_files': list((self.project_root / 'src' / 'templates').glob('*.j2')),
            'script_files': list((self.project_root / 'assets' / 'development' / 'scripts').glob('*.py'))
        }
        
        # Calculate structure score
        total_checks = 0
        passed_checks = 0
        
        for key, value in structure_checks.items():
            if isinstance(value, bool):
                total_checks += 1
                if value:
                    passed_checks += 1
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    total_checks += 1
                    if sub_value:
                        passed_checks += 1
            elif isinstance(value, list):
                total_checks += 1
                if len(value) > 0:
                    passed_checks += 1
        
        structure_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        return {
            'checks': structure_checks,
            'score': structure_score,
            'status': 'healthy' if structure_score >= 80 else 'needs_attention'
        }
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Check project dependencies."""
        print("📦 Checking dependencies...")
        
        try:
            # Check if requirements.txt exists and is readable
            requirements_file = self.project_root / 'requirements.txt'
            if not requirements_file.exists():
                return {
                    'status': 'error',
                    'message': 'requirements.txt not found',
                    'score': 0
                }
            
            # Count dependencies
            with open(requirements_file, 'r') as f:
                dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # Check for common issues
            issues = []
            if len(dependencies) == 0:
                issues.append('No dependencies found')
            
            # Check for version pinning
            unpinned_deps = [dep for dep in dependencies if '==' not in dep and '>=' not in dep and '~=' not in dep]
            if unpinned_deps:
                issues.append(f'Unpinned dependencies: {len(unpinned_deps)}')
            
            # Check for security vulnerabilities
            try:
                result = subprocess.run(['safety', 'check', '--json'], capture_output=True, text=True)
                if result.returncode != 0:
                    issues.append('Security vulnerabilities detected')
            except FileNotFoundError:
                issues.append('Safety tool not installed')
            
            score = max(0, 100 - len(issues) * 20)
            
            return {
                'total_dependencies': len(dependencies),
                'unpinned_dependencies': len(unpinned_deps),
                'issues': issues,
                'score': score,
                'status': 'healthy' if score >= 80 else 'needs_attention'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'score': 0
            }
    
    def check_code_quality(self) -> Dict[str, Any]:
        """Check code quality metrics."""
        print("🔍 Checking code quality...")
        
        quality_metrics = {
            'linting': {'status': 'unknown', 'score': 0},
            'type_checking': {'status': 'unknown', 'score': 0},
            'test_coverage': {'status': 'unknown', 'score': 0}
        }
        
        # Check linting
        try:
            result = subprocess.run(['flake8', 'src/', '--count'], capture_output=True, text=True)
            if result.returncode == 0:
                quality_metrics['linting'] = {'status': 'passed', 'score': 100}
            else:
                error_count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
                score = max(0, 100 - error_count * 5)
                quality_metrics['linting'] = {'status': 'failed', 'score': score, 'errors': error_count}
        except FileNotFoundError:
            quality_metrics['linting'] = {'status': 'tool_not_found', 'score': 0}
        
        # Check type checking
        try:
            result = subprocess.run(['mypy', 'src/', '--ignore-missing-imports'], capture_output=True, text=True)
            if result.returncode == 0:
                quality_metrics['type_checking'] = {'status': 'passed', 'score': 100}
            else:
                quality_metrics['type_checking'] = {'status': 'failed', 'score': 50}
        except FileNotFoundError:
            quality_metrics['type_checking'] = {'status': 'tool_not_found', 'score': 0}
        
        # Check test coverage
        try:
            result = subprocess.run(['python', '-m', 'pytest', '--cov=src', '--cov-report=term-missing'], capture_output=True, text=True)
            if result.returncode == 0:
                # Extract coverage percentage from output
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'TOTAL' in line and '%' in line:
                        try:
                            coverage = float(line.split('%')[0].split()[-1])
                            quality_metrics['test_coverage'] = {'status': 'passed', 'score': coverage}
                        except:
                            quality_metrics['test_coverage'] = {'status': 'unknown', 'score': 0}
                        break
        except FileNotFoundError:
            quality_metrics['test_coverage'] = {'status': 'tool_not_found', 'score': 0}
        
        # Calculate overall quality score
        scores = [metric['score'] for metric in quality_metrics.values()]
        overall_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'metrics': quality_metrics,
            'overall_score': overall_score,
            'status': 'healthy' if overall_score >= 80 else 'needs_attention'
        }
    
    def check_performance(self) -> Dict[str, Any]:
        """Check project performance metrics."""
        print("⚡ Checking performance...")
        
        performance_metrics = {}
        
        # Check import time
        try:
            start_time = time.time()
            import src
            import_time = time.time() - start_time
            performance_metrics['import_time'] = {
                'value': import_time,
                'unit': 'seconds',
                'status': 'good' if import_time < 1.0 else 'slow'
            }
        except Exception as e:
            performance_metrics['import_time'] = {
                'value': None,
                'error': str(e),
                'status': 'error'
            }
        
        # Check memory usage
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            performance_metrics['memory_usage'] = {
                'value': memory_mb,
                'unit': 'MB',
                'status': 'good' if memory_mb < 100 else 'high'
            }
        except ImportError:
            performance_metrics['memory_usage'] = {
                'value': None,
                'error': 'psutil not available',
                'status': 'unknown'
            }
        
        # Check file sizes
        src_files = list((self.project_root / 'src').rglob('*.py'))
        total_size = sum(f.stat().st_size for f in src_files)
        avg_file_size = total_size / len(src_files) if src_files else 0
        
        performance_metrics['file_sizes'] = {
            'total_files': len(src_files),
            'total_size_kb': total_size / 1024,
            'avg_file_size_kb': avg_file_size / 1024,
            'status': 'good' if avg_file_size < 10000 else 'large'
        }
        
        return performance_metrics
    
    def check_compliance(self) -> Dict[str, Any]:
        """Check project compliance with standards."""
        print("📋 Checking compliance...")
        
        compliance_checks = {
            'python_version': self._check_python_version(),
            'coding_standards': self._check_coding_standards(),
            'documentation': self._check_documentation(),
            'security': self._check_security()
        }
        
        # Calculate compliance score
        scores = [check.get('score', 0) for check in compliance_checks.values()]
        overall_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'checks': compliance_checks,
            'overall_score': overall_score,
            'status': 'compliant' if overall_score >= 80 else 'non_compliant'
        }
    
    def _check_python_version(self) -> Dict[str, Any]:
        """Check Python version compliance."""
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            return {'score': 100, 'status': 'compliant', 'version': f'{version.major}.{version.minor}'}
        else:
            return {'score': 0, 'status': 'non_compliant', 'version': f'{version.major}.{version.minor}'}
    
    def _check_coding_standards(self) -> Dict[str, Any]:
        """Check coding standards compliance."""
        try:
            result = subprocess.run(['black', '--check', 'src/'], capture_output=True, text=True)
            if result.returncode == 0:
                return {'score': 100, 'status': 'compliant'}
            else:
                return {'score': 50, 'status': 'needs_formatting'}
        except FileNotFoundError:
            return {'score': 0, 'status': 'tool_not_found'}
    
    def _check_documentation(self) -> Dict[str, Any]:
        """Check documentation compliance."""
        doc_files = list((self.project_root / 'assets' / 'documentation').glob('*.md'))
        if len(doc_files) >= 3:
            return {'score': 100, 'status': 'compliant', 'files': len(doc_files)}
        else:
            return {'score': 50, 'status': 'incomplete', 'files': len(doc_files)}
    
    def _check_security(self) -> Dict[str, Any]:
        """Check security compliance."""
        try:
            result = subprocess.run(['bandit', '-r', 'src/', '-f', 'json'], capture_output=True, text=True)
            if result.returncode == 0:
                return {'score': 100, 'status': 'compliant'}
            else:
                return {'score': 75, 'status': 'warnings_found'}
        except FileNotFoundError:
            return {'score': 0, 'status': 'tool_not_found'}
    
    def generate_recommendations(self):
        """Generate improvement recommendations."""
        recommendations = []
        
        # Analyze project health
        if self.metrics['project_health'].get('structure', {}).get('score', 0) < 80:
            recommendations.append({
                'category': 'structure',
                'priority': 'high',
                'message': 'Improve project structure organization',
                'action': 'Review and reorganize project directories'
            })
        
        # Analyze code quality
        if self.metrics['project_health'].get('code_quality', {}).get('overall_score', 0) < 80:
            recommendations.append({
                'category': 'quality',
                'priority': 'high',
                'message': 'Improve code quality metrics',
                'action': 'Run linting, type checking, and increase test coverage'
            })
        
        # Analyze performance
        if self.metrics['performance'].get('import_time', {}).get('status') == 'slow':
            recommendations.append({
                'category': 'performance',
                'priority': 'medium',
                'message': 'Optimize import performance',
                'action': 'Review and optimize module imports'
            })
        
        # Analyze compliance
        if self.metrics['compliance'].get('overall_score', 0) < 80:
            recommendations.append({
                'category': 'compliance',
                'priority': 'high',
                'message': 'Improve compliance with standards',
                'action': 'Address compliance issues identified in checks'
            })
        
        self.metrics['recommendations'] = recommendations
    
    def generate_report(self) -> Path:
        """Generate monitoring report."""
        report_file = self.project_root / 'assets' / 'reports' / 'project_monitoring_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"\n📄 Monitoring report saved to: {report_file}")
        return report_file
    
    def display_summary(self):
        """Display monitoring summary."""
        print(f"\n📊 Project Monitoring Summary")
        print("=" * 40)
        
        # Project Health
        health = self.metrics['project_health']
        print(f"\n🏥 Project Health:")
        for key, value in health.items():
            if isinstance(value, dict) and 'score' in value:
                print(f"  {key}: {value['score']:.1f}% ({value.get('status', 'unknown')})")
        
        # Performance
        performance = self.metrics['performance']
        print(f"\n⚡ Performance:")
        for key, value in performance.items():
            if isinstance(value, dict) and 'value' is not None:
                print(f"  {key}: {value['value']} {value.get('unit', '')} ({value.get('status', 'unknown')})")
        
        # Compliance
        compliance = self.metrics['compliance']
        print(f"\n📋 Compliance:")
        print(f"  Overall Score: {compliance.get('overall_score', 0):.1f}% ({compliance.get('status', 'unknown')})")
        
        # Recommendations
        recommendations = self.metrics['recommendations']
        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"  [{rec['priority'].upper()}] {rec['message']}")
                print(f"      Action: {rec['action']}")
    
    def run_monitoring(self):
        """Run complete project monitoring."""
        print("🚀 DocGen CLI Project Monitoring")
        print("=" * 40)
        
        # Run all checks
        self.metrics['project_health']['structure'] = self.check_project_structure()
        self.metrics['project_health']['dependencies'] = self.check_dependencies()
        self.metrics['project_health']['code_quality'] = self.check_code_quality()
        self.metrics['performance'] = self.check_performance()
        self.metrics['compliance'] = self.check_compliance()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Generate report
        self.generate_report()
        
        # Display summary
        self.display_summary()

def main():
    """Main function."""
    monitor = ProjectMonitor()
    monitor.run_monitoring()

if __name__ == '__main__':
    main()
