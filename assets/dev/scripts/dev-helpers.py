#!/usr/bin/env python3
"""
Development Helpers for DocGen CLI
Essential development utilities and project analysis
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DevHelpers:
    """Essential development helper utilities"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        
    def find_files_by_pattern(self, pattern: str, directory: str = None) -> List[Path]:
        """Find files matching a pattern"""
        search_dir = self.project_root / directory if directory else self.project_root
        return list(search_dir.rglob(pattern))
    
    def find_python_files(self, directory: str = None) -> List[Path]:
        """Find all Python files"""
        return self.find_files_by_pattern("*.py", directory)
    
    def find_test_files(self, directory: str = None) -> List[Path]:
        """Find all test files"""
        return self.find_files_by_pattern("test_*.py", directory)
    
    def find_template_files(self, directory: str = None) -> List[Path]:
        """Find all template files"""
        return self.find_files_by_pattern("*.j2", directory)
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze project structure and provide insights"""
        logger.info("Analyzing project structure...")
        
        analysis = {
            'timestamp': time.time(),
            'directories': {},
            'files': {},
            'statistics': {},
            'insights': []
        }
        
        # Analyze key directories
        key_directories = [
            'src', 'src/cli', 'src/commands', 'src/core', 'src/models', 
            'src/templates', 'src/utils', 'assets', 'assets/specs',
            'assets/templates', 'assets/dev', 'assets/docs'
        ]
        
        for dir_path in key_directories:
            full_path = self.project_root / dir_path
            if full_path.exists():
                file_count = len(list(full_path.rglob('*')))
                analysis['directories'][dir_path] = {
                    'exists': True,
                    'file_count': file_count,
                    'last_modified': full_path.stat().st_mtime
                }
            else:
                analysis['directories'][dir_path] = {'exists': False}
        
        # Analyze files
        python_files = self.find_python_files()
        test_files = self.find_test_files()
        template_files = self.find_template_files()
        
        analysis['files'] = {
            'python_files': len(python_files),
            'test_files': len(test_files),
            'template_files': len(template_files),
            'total_files': len(list(self.project_root.rglob('*')))
        }
        
        # Calculate statistics
        analysis['statistics'] = {
            'test_coverage_estimate': (len(test_files) / len(python_files) * 100) if python_files else 0,
            'average_file_size': sum(f.stat().st_size for f in python_files) / len(python_files) if python_files else 0,
            'project_age_days': (time.time() - min(f.stat().st_ctime for f in python_files)) / 86400 if python_files else 0
        }
        
        # Generate insights
        if analysis['statistics']['test_coverage_estimate'] < 50:
            analysis['insights'].append("Low test coverage - consider adding more tests")
        
        if analysis['files']['template_files'] == 0:
            analysis['insights'].append("No template files found - check template directory")
        
        if not analysis['directories'].get('src', {}).get('exists'):
            analysis['insights'].append("Source directory missing - check project structure")
        
        logger.info("Project structure analysis completed")
        return analysis
    
    def check_import_dependencies(self) -> Dict[str, Any]:
        """Check import dependencies and find issues"""
        logger.info("Checking import dependencies...")
        
        import_analysis = {
            'timestamp': time.time(),
            'import_issues': [],
            'missing_imports': [],
            'circular_imports': [],
            'unused_imports': [],
            'statistics': {}
        }
        
        python_files = self.find_python_files()
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common import issues
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    line = line.strip()
                    
                    # Check for relative imports that might be problematic
                    if line.startswith('from .') and 'src' not in str(py_file):
                        import_analysis['import_issues'].append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'Relative import outside src directory',
                            'severity': 'warning'
                        })
                    
                    # Check for missing src prefix in imports
                    if ('from docgen.' in line or 'import docgen.' in line) and 'src' in str(py_file):
                        import_analysis['import_issues'].append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'Outdated import path - should use src. prefix',
                            'severity': 'error'
                        })
            
            except Exception as e:
                import_analysis['import_issues'].append({
                    'file': str(py_file.relative_to(self.project_root)),
                    'line': 0,
                    'issue': f'Error reading file: {e}',
                    'severity': 'error'
                })
        
        # Calculate statistics
        import_analysis['statistics'] = {
            'total_files_checked': len(python_files),
            'files_with_issues': len(set(issue['file'] for issue in import_analysis['import_issues'])),
            'total_issues': len(import_analysis['import_issues']),
            'error_count': len([issue for issue in import_analysis['import_issues'] if issue['severity'] == 'error']),
            'warning_count': len([issue for issue in import_analysis['import_issues'] if issue['severity'] == 'warning'])
        }
        
        logger.info("Import dependency check completed")
        return import_analysis
    
    def generate_development_report(self) -> str:
        """Generate comprehensive development report"""
        logger.info("Generating development report...")
        
        try:
            # Run all analyses
            structure_analysis = self.analyze_project_structure()
            import_analysis = self.check_import_dependencies()
            
            # Combine all analyses
            report = {
                'timestamp': time.time(),
                'project_root': str(self.project_root),
                'structure_analysis': structure_analysis,
                'import_analysis': import_analysis,
                'summary': {
                    'overall_health': 'unknown',
                    'critical_issues': 0,
                    'recommendations': []
                }
            }
            
            # Calculate overall health
            critical_issues = import_analysis['statistics']['error_count']
            
            report['summary']['critical_issues'] = critical_issues
            
            if critical_issues == 0:
                report['summary']['overall_health'] = 'excellent'
            elif critical_issues <= 3:
                report['summary']['overall_health'] = 'good'
            elif critical_issues <= 6:
                report['summary']['overall_health'] = 'fair'
            else:
                report['summary']['overall_health'] = 'needs_attention'
            
            # Generate recommendations
            if import_analysis['statistics']['error_count'] > 0:
                report['summary']['recommendations'].append("Fix import path issues")
            
            if structure_analysis['statistics']['test_coverage_estimate'] < 50:
                report['summary']['recommendations'].append("Increase test coverage")
            
            # Save report
            report_path = self.project_root / 'assets' / 'reports' / 'development_analysis_report.json'
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"Development report saved to: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Error generating development report: {e}")
            return ""
    
    def display_development_summary(self, report_path: str = None):
        """Display development analysis summary"""
        if not report_path:
            report_path = self.generate_development_report()
        
        if not report_path or not Path(report_path).exists():
            logger.error("No development report available")
            return
        
        try:
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            print("\n" + "="*60)
            print("📊 DEVELOPMENT ANALYSIS SUMMARY")
            print("="*60)
            
            summary = report.get('summary', {})
            print(f"🏥 Overall Health: {summary.get('overall_health', 'unknown').upper()}")
            print(f"🚨 Critical Issues: {summary.get('critical_issues', 0)}")
            
            # Structure analysis
            structure = report.get('structure_analysis', {})
            print(f"\n📁 Project Structure:")
            print(f"   Python Files: {structure.get('files', {}).get('python_files', 0)}")
            print(f"   Test Files: {structure.get('files', {}).get('test_files', 0)}")
            print(f"   Template Files: {structure.get('files', {}).get('template_files', 0)}")
            print(f"   Test Coverage: {structure.get('statistics', {}).get('test_coverage_estimate', 0):.1f}%")
            
            # Import analysis
            imports = report.get('import_analysis', {})
            print(f"\n📦 Import Analysis:")
            print(f"   Files Checked: {imports.get('statistics', {}).get('total_files_checked', 0)}")
            print(f"   Import Issues: {imports.get('statistics', {}).get('total_issues', 0)}")
            print(f"   Errors: {imports.get('statistics', {}).get('error_count', 0)}")
            print(f"   Warnings: {imports.get('statistics', {}).get('warning_count', 0)}")
            
            # Recommendations
            recommendations = summary.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations:
                    print(f"   • {rec}")
            
            print("\n" + "="*60)
            
        except Exception as e:
            logger.error(f"Error displaying development summary: {e}")

def main():
    """Main function to run development helpers"""
    helpers = DevHelpers()
    
    print("🔧 DocGen CLI Development Helpers")
    print("=" * 50)
    
    # Generate and display development report
    report_path = helpers.generate_development_report()
    if report_path:
        helpers.display_development_summary(report_path)
        print(f"\n📄 Full report available at: {report_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
