#!/usr/bin/env python3
"""
Quick Development Setup for DocGen CLI
Automated development environment setup and configuration
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuickDevSetup:
    """Quick development setup and configuration"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.setup_results = {
            'timestamp': datetime.now().isoformat(),
            'steps': {},
            'success': False,
            'errors': []
        }
        
    def log_step(self, step: str, status: str, details: str = None):
        """Log setup step results"""
        self.setup_results['steps'][step] = {
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        if status == 'success':
            logger.info(f"✅ {step}: {details or 'Completed successfully'}")
        elif status == 'error':
            logger.error(f"❌ {step}: {details or 'Failed'}")
            self.setup_results['errors'].append(f"{step}: {details}")
        else:
            logger.info(f"ℹ️ {step}: {details or 'In progress'}")
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        try:
            version = sys.version_info
            if version.major == 3 and version.minor >= 8:
                self.log_step("Python Version Check", "success", f"Python {version.major}.{version.minor}.{version.micro}")
                return True
            else:
                self.log_step("Python Version Check", "error", f"Python {version.major}.{version.minor} not supported (requires 3.8+)")
                return False
        except Exception as e:
            self.log_step("Python Version Check", "error", str(e))
            return False
    
    def check_virtual_environment(self) -> bool:
        """Check if virtual environment is active"""
        try:
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                self.log_step("Virtual Environment Check", "success", "Virtual environment is active")
                return True
            else:
                self.log_step("Virtual Environment Check", "warning", "No virtual environment detected")
                return False
        except Exception as e:
            self.log_step("Virtual Environment Check", "error", str(e))
            return False
    
    def create_virtual_environment(self) -> bool:
        """Create virtual environment if needed"""
        try:
            venv_path = self.project_root / 'venv'
            if not venv_path.exists():
                subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
                self.log_step("Virtual Environment Creation", "success", f"Created at {venv_path}")
            else:
                self.log_step("Virtual Environment Creation", "success", "Already exists")
            return True
        except Exception as e:
            self.log_step("Virtual Environment Creation", "error", str(e))
            return False
    
    def install_dependencies(self) -> bool:
        """Install project dependencies"""
        try:
            requirements_file = self.project_root / 'requirements.txt'
            if requirements_file.exists():
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], check=True)
                self.log_step("Dependencies Installation", "success", "Installed from requirements.txt")
            else:
                self.log_step("Dependencies Installation", "warning", "No requirements.txt found")
            return True
        except Exception as e:
            self.log_step("Dependencies Installation", "error", str(e))
            return False
    
    def setup_development_dependencies(self) -> bool:
        """Setup development dependencies"""
        try:
            dev_deps = [
                'pytest>=7.0.0',
                'pytest-cov>=4.0.0',
                'black>=22.0.0',
                'flake8>=5.0.0',
                'mypy>=1.0.0',
                'pre-commit>=2.20.0'
            ]
            
            for dep in dev_deps:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
            
            self.log_step("Development Dependencies", "success", f"Installed {len(dev_deps)} packages")
            return True
        except Exception as e:
            self.log_step("Development Dependencies", "error", str(e))
            return False
    
    def create_project_structure(self) -> bool:
        """Create essential project directories"""
        try:
            directories = [
                'assets/reports',
                'assets/logs',
                'assets/temp',
                'tests/unit',
                'tests/integration',
                'docs/generated'
            ]
            
            for dir_path in directories:
                full_path = self.project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
            
            self.log_step("Project Structure", "success", f"Created {len(directories)} directories")
            return True
        except Exception as e:
            self.log_step("Project Structure", "error", str(e))
            return False
    
    def setup_git_hooks(self) -> bool:
        """Setup git hooks for development"""
        try:
            git_hooks_dir = self.project_root / '.git' / 'hooks'
            if git_hooks_dir.exists():
                # Create pre-commit hook
                pre_commit_hook = git_hooks_dir / 'pre-commit'
                pre_commit_content = '''#!/bin/sh
# Run basic checks before commit
python -m flake8 src/
python -m black --check src/
python -m pytest tests/unit/ -v
'''
                with open(pre_commit_hook, 'w') as f:
                    f.write(pre_commit_content)
                pre_commit_hook.chmod(0o755)
                
                self.log_step("Git Hooks", "success", "Pre-commit hook created")
            else:
                self.log_step("Git Hooks", "warning", "Not a git repository")
            return True
        except Exception as e:
            self.log_step("Git Hooks", "error", str(e))
            return False
    
    def setup_environment_config(self) -> bool:
        """Setup environment configuration"""
        try:
            env_example = self.project_root / '.env.example'
            env_content = '''# DocGen CLI Environment Configuration
# Copy this file to .env and update values as needed

# Development settings
DEBUG=true
LOG_LEVEL=INFO

# Project settings
PROJECT_NAME=DocGen CLI
PROJECT_VERSION=1.0.0

# Template settings
TEMPLATE_DIR=src/templates
OUTPUT_DIR=assets/docs/generated

# MCP Integration
MCP_ENABLED=true
MCP_CONFIG_PATH=assets/config/mcp/mcp_config.yaml
'''
            
            with open(env_example, 'w') as f:
                f.write(env_content)
            
            self.log_step("Environment Config", "success", "Created .env.example")
            return True
        except Exception as e:
            self.log_step("Environment Config", "error", str(e))
            return False
    
    def setup_mcp_configuration(self) -> bool:
        """Setup MCP configuration"""
        try:
            mcp_config_dir = self.project_root / 'assets' / 'configuration' / 'mcp'
            mcp_config_dir.mkdir(parents=True, exist_ok=True)
            
            mcp_config = {
                'servers': {
                    'byterover': {
                        'enabled': True,
                        'config_path': 'assets/config/mcp/byterover.json'
                    },
                    'testsprite': {
                        'enabled': True,
                        'test_port': 3000,
                        'test_type': 'backend',
                        'test_scope': 'codebase'
                    },
                    'context7': {
                        'enabled': True,
                        'libraries': ['click', 'jinja2', 'pydantic', 'rich']
                    },
                    'browser_tools': {
                        'enabled': True,
                        'audit_types': ['accessibility', 'performance', 'seo', 'best_practices']
                    },
                    'dart': {
                        'enabled': True,
                        'workspace': 'docgen_cli_workspace'
                    }
                },
                'workflow': {
                    'knowledge_first': True,
                    'parallel_execution': True,
                    'quality_gates': {
                        'test_coverage': 80,
                        'performance_threshold': 5,
                        'accessibility_score': 90
                    }
                }
            }
            
            config_file = mcp_config_dir / 'mcp_config.yaml'
            import yaml
            with open(config_file, 'w') as f:
                yaml.dump(mcp_config, f, default_flow_style=False, indent=2)
            
            self.log_step("MCP Configuration", "success", "Created mcp_config.yaml")
            return True
        except Exception as e:
            self.log_step("MCP Configuration", "error", str(e))
            return False
    
    def run_initial_tests(self) -> bool:
        """Run initial tests to verify setup"""
        try:
            # Add src to Python path
            sys.path.insert(0, str(self.project_root / 'src'))
            
            # Run basic import test
            try:
                import src.cli.main
                self.log_step("Import Test", "success", "Core modules import successfully")
            except ImportError as e:
                self.log_step("Import Test", "error", f"Import failed: {e}")
                return False
            
            # Run basic validation
            try:
                from src.core.validation import ValidationManager
                validator = ValidationManager()
                self.log_step("Validation Test", "success", "Validation system working")
            except Exception as e:
                self.log_step("Validation Test", "error", f"Validation failed: {e}")
                return False
            
            return True
        except Exception as e:
            self.log_step("Initial Tests", "error", str(e))
            return False
    
    def generate_setup_report(self) -> str:
        """Generate setup report"""
        try:
            report_path = self.project_root / 'assets' / 'reports' / 'setup_report.json'
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(self.setup_results, f, indent=2, default=str)
            
            logger.info(f"Setup report saved to: {report_path}")
            return str(report_path)
        except Exception as e:
            logger.error(f"Error generating setup report: {e}")
            return ""
    
    def run_complete_setup(self) -> bool:
        """Run complete development setup"""
        logger.info("🚀 Starting Quick Development Setup")
        logger.info("=" * 50)
        
        setup_steps = [
            ("Python Version Check", self.check_python_version),
            ("Virtual Environment Check", self.check_virtual_environment),
            ("Virtual Environment Creation", self.create_virtual_environment),
            ("Dependencies Installation", self.install_dependencies),
            ("Development Dependencies", self.setup_development_dependencies),
            ("Project Structure", self.create_project_structure),
            ("Git Hooks", self.setup_git_hooks),
            ("Environment Config", self.setup_environment_config),
            ("MCP Configuration", self.setup_mcp_configuration),
            ("Initial Tests", self.run_initial_tests)
        ]
        
        success_count = 0
        for step_name, step_func in setup_steps:
            logger.info(f"\n📋 {step_name}...")
            if step_func():
                success_count += 1
        
        # Calculate overall success
        self.setup_results['success'] = success_count == len(setup_steps)
        self.setup_results['success_rate'] = success_count / len(setup_steps)
        
        # Generate report
        report_path = self.generate_setup_report()
        
        logger.info(f"\n🎉 Setup completed: {success_count}/{len(setup_steps)} steps successful")
        return self.setup_results['success']
    
    def display_setup_summary(self):
        """Display setup summary"""
        print("\n" + "="*60)
        print("🚀 QUICK DEVELOPMENT SETUP SUMMARY")
        print("="*60)
        
        print(f"📊 Overall Status: {'✅ SUCCESS' if self.setup_results['success'] else '❌ FAILED'}")
        print(f"📈 Success Rate: {self.setup_results.get('success_rate', 0):.1%}")
        print(f"🚨 Errors: {len(self.setup_results['errors'])}")
        
        print(f"\n📋 Setup Steps:")
        for step_name, step_data in self.setup_results['steps'].items():
            status_icon = "✅" if step_data['status'] == 'success' else "❌" if step_data['status'] == 'error' else "⚠️"
            print(f"   {status_icon} {step_name}: {step_data['status']}")
        
        if self.setup_results['errors']:
            print(f"\n🚨 Errors:")
            for error in self.setup_results['errors']:
                print(f"   • {error}")
        
        print("\n" + "="*60)

def main():
    """Main function to run quick development setup"""
    setup = QuickDevSetup()
    
    print("🚀 DocGen CLI Quick Development Setup")
    print("=" * 50)
    
    # Run complete setup
    success = setup.run_complete_setup()
    
    # Display summary
    setup.display_setup_summary()
    
    if success:
        print("\n🎉 Development environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Activate virtual environment: source venv/bin/activate")
        print("2. Copy .env.example to .env and configure")
        print("3. Run tests: python -m pytest tests/")
        print("4. Start development: python src/cli_main.py --help")
        return 0
    else:
        print("\n❌ Setup completed with errors")
        print("Please review the errors and fix them before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())
