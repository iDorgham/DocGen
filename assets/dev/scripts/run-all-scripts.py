#!/usr/bin/env python3
"""
Run All Scripts - DocGen CLI
Execute all essential development scripts in sequence
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

class ScriptRunner:
    def __init__(self):
        self.project_root = Path.cwd()
        self.scripts_dir = self.project_root / 'assets' / 'development' / 'scripts'
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'scripts': {},
            'summary': {
                'total_scripts': 0,
                'successful': 0,
                'failed': 0,
                'duration': 0
            }
        }
        self.start_time = time.time()
    
    def run_script(self, script_name: str, description: str = "", required: bool = True):
        """Run a script and record results."""
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_name}")
            self.results['scripts'][script_name] = {
                'status': 'not_found',
                'error': 'Script file not found'
            }
            self.results['summary']['failed'] += 1
            self.results['summary']['total_scripts'] += 1
            return False
        
        print(f"🚀 Running {script_name}...")
        if description:
            print(f"   {description}")
        
        try:
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            duration = time.time() - start_time
            
            self.results['scripts'][script_name] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': duration,
                'status': 'success' if result.returncode == 0 else 'failed'
            }
            
            if result.returncode == 0:
                print(f"   ✓ Success ({duration:.1f}s)")
                self.results['summary']['successful'] += 1
            else:
                print(f"   ✗ Failed (exit code: {result.returncode}, {duration:.1f}s)")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                self.results['summary']['failed'] += 1
            
            self.results['summary']['total_scripts'] += 1
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout (5 minutes)")
            self.results['scripts'][script_name] = {
                'status': 'timeout',
                'error': 'Script execution timeout'
            }
            self.results['summary']['failed'] += 1
            self.results['summary']['total_scripts'] += 1
            return False
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
            self.results['scripts'][script_name] = {
                'status': 'error',
                'error': str(e)
            }
            self.results['summary']['failed'] += 1
            self.results['summary']['total_scripts'] += 1
            return False
    
    def run_essential_scripts(self):
        """Run all essential development scripts."""
        print("🚀 DocGen CLI - Running All Essential Scripts")
        print("=" * 50)
        
        # Script execution order
        scripts = [
            ('quick_dev_setup.py', 'Development environment setup', True),
            ('dev_helpers.py', 'Development helper utilities', True),
            ('generate_docs.py', 'Documentation generation', True),
            ('run_quality_checks.py', 'Quality assurance checks', True),
            ('workflow_automation.py', 'Workflow automation', False),
            ('project_monitoring.py', 'Project health monitoring', False),
            ('run_mcp_integration.py', 'MCP server integration', False)
        ]
        
        for script_name, description, required in scripts:
            success = self.run_script(script_name, description, required)
            
            # Add delay between scripts
            time.sleep(1)
            
            # Stop on critical failure if required
            if not success and required:
                print(f"\n❌ Critical script failed: {script_name}")
                print("Stopping execution due to critical failure.")
                break
        
        # Calculate total duration
        self.results['summary']['duration'] = time.time() - self.start_time
    
    def generate_report(self):
        """Generate execution report."""
        report_file = self.project_root / 'assets' / 'reports' / 'script_execution_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Execution report saved to: {report_file}")
        return report_file
    
    def display_summary(self):
        """Display execution summary."""
        summary = self.results['summary']
        total = summary['total_scripts']
        successful = summary['successful']
        failed = summary['failed']
        duration = summary['duration']
        
        print(f"\n📊 Script Execution Summary")
        print("=" * 40)
        print(f"Total Scripts: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"Total Duration: {duration:.1f} seconds")
        
        if failed > 0:
            print(f"\n❌ Failed Scripts:")
            for name, result in self.results['scripts'].items():
                if result['status'] in ['failed', 'error', 'timeout', 'not_found']:
                    print(f"  - {name}: {result.get('error', result['status'])}")
        
        success_rate = successful / total if total > 0 else 0
        if success_rate >= 0.8:
            print(f"\n✅ Script execution completed successfully! ({success_rate*100:.1f}% success rate)")
            return True
        else:
            print(f"\n❌ Script execution had issues! ({success_rate*100:.1f}% success rate)")
            return False

def main():
    """Main function."""
    runner = ScriptRunner()
    runner.run_essential_scripts()
    runner.generate_report()
    success = runner.display_summary()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
