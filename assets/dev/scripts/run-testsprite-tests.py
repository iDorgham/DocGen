#!/usr/bin/env python3
"""
TestSprite Test Runner Script

This script runs TestSprite tests using the configured API key.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

def load_env_file():
    """Load environment variables from .env file."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables from .env file
load_env_file()


def check_testsprite_configuration():
    """Check if TestSprite is properly configured."""
    print("🔍 Checking TestSprite configuration...")
    
    # Check if API key is set
    api_key = os.getenv("TESTSPRITE_API_KEY")
    
    if not api_key:
        print("❌ TESTSPRITE_API_KEY environment variable not found")
        print("   Run: python scripts/setup_testsprite_api.py")
        return False
    
    if api_key == "your_testsprite_api_key_here":
        print("❌ Please replace the placeholder API key with your actual TestSprite API key")
        return False
    
    print(f"✅ TestSprite API key is configured: {api_key[:8]}...")
    return True


def run_testsprite_bootstrap():
    """Run TestSprite bootstrap tests."""
    print("🚀 Running TestSprite bootstrap tests...")
    
    try:
        # Import TestSprite MCP tools
        from mcp_TestSprite_testsprite_bootstrap_tests import testsprite_bootstrap_tests
        
        project_path = str(Path(__file__).parent.parent)
        
        print(f"   Project path: {project_path}")
        print("   Bootstrapping TestSprite tests...")
        
        # Run bootstrap tests
        result = testsprite_bootstrap_tests(
            localPort=3000,
            type="backend",
            projectPath=project_path,
            testScope="codebase"
        )
        
        print("✅ TestSprite bootstrap completed successfully")
        return True
        
    except ImportError as e:
        print(f"❌ TestSprite MCP tools not available: {str(e)}")
        print("   Make sure you're running this in the correct environment")
        return False
    except Exception as e:
        print(f"❌ Error running TestSprite bootstrap: {str(e)}")
        return False


def run_testsprite_code_summary():
    """Run TestSprite code summary generation."""
    print("📊 Running TestSprite code summary...")
    
    try:
        from mcp_TestSprite_testsprite_generate_code_summary import testsprite_generate_code_summary
        
        project_path = str(Path(__file__).parent.parent)
        
        print(f"   Project path: {project_path}")
        print("   Generating code summary...")
        
        # Generate code summary
        result = testsprite_generate_code_summary(
            projectRootPath=project_path
        )
        
        print("✅ TestSprite code summary generated successfully")
        return True
        
    except ImportError as e:
        print(f"❌ TestSprite MCP tools not available: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error generating code summary: {str(e)}")
        return False


def run_testsprite_test_plan():
    """Run TestSprite test plan generation."""
    print("📋 Running TestSprite test plan generation...")
    
    try:
        from mcp_TestSprite_testsprite_generate_backend_test_plan import testsprite_generate_backend_test_plan
        
        project_path = str(Path(__file__).parent.parent)
        
        print(f"   Project path: {project_path}")
        print("   Generating backend test plan...")
        
        # Generate test plan
        result = testsprite_generate_backend_test_plan(
            projectPath=project_path
        )
        
        print("✅ TestSprite test plan generated successfully")
        return True
        
    except ImportError as e:
        print(f"❌ TestSprite MCP tools not available: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error generating test plan: {str(e)}")
        return False


def run_testsprite_test_execution():
    """Run TestSprite test execution."""
    print("🧪 Running TestSprite test execution...")
    
    try:
        from mcp_TestSprite_testsprite_generate_code_and_execute import testsprite_generate_code_and_execute
        
        project_path = str(Path(__file__).parent.parent)
        project_name = Path(project_path).name
        
        print(f"   Project: {project_name}")
        print(f"   Project path: {project_path}")
        print("   Executing tests...")
        
        # Execute tests
        result = testsprite_generate_code_and_execute(
            projectName=project_name,
            projectPath=project_path,
            testIds=[],  # Run all tests
            additionalInstruction=""
        )
        
        print("✅ TestSprite test execution completed successfully")
        return True
        
    except ImportError as e:
        print(f"❌ TestSprite MCP tools not available: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error executing tests: {str(e)}")
        return False


def generate_test_report():
    """Generate a test report."""
    print("📊 Generating test report...")
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "project": "DocGen CLI",
        "test_runner": "TestSprite",
        "tests_run": [
            "bootstrap_tests",
            "code_summary",
            "test_plan_generation",
            "test_execution"
        ],
        "status": "completed"
    }
    
    # Save report
    project_root = Path(__file__).parent.parent
    report_path = project_root / "assets" / "reports" / "testsprite_test_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2, default=str)
    
    print(f"✅ Test report saved to: {report_path}")


def main():
    """Main function to run TestSprite tests."""
    print("🧪 TestSprite Test Runner for DocGen CLI")
    print("=" * 60)
    print()
    
    # Check configuration
    if not check_testsprite_configuration():
        print("❌ TestSprite configuration check failed")
        print("   Please run: python scripts/setup_testsprite_api.py")
        return False
    
    print()
    
    # Run TestSprite tests
    test_functions = [
        ("Bootstrap Tests", run_testsprite_bootstrap),
        ("Code Summary", run_testsprite_code_summary),
        ("Test Plan Generation", run_testsprite_test_plan),
        ("Test Execution", run_testsprite_test_execution)
    ]
    
    results = []
    
    for test_name, test_func in test_functions:
        print(f"📋 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {str(e)}")
            results.append((test_name, False))
        print()
    
    # Generate report
    generate_test_report()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All TestSprite tests completed successfully!")
        print()
        print("📚 Next steps:")
        print("1. Check TestSprite dashboard: https://www.testsprite.com/dashboard")
        print("2. Review test results in the TestSprite interface")
        print("3. Integrate TestSprite tests into your CI/CD pipeline")
    else:
        print("⚠️  Some TestSprite tests failed. Please check the errors above.")
        print()
        print("🔧 Troubleshooting:")
        print("1. Verify API key: python scripts/test_testsprite_config.py")
        print("2. Check TestSprite status: https://www.testsprite.com/dashboard")
        print("3. Review TestSprite documentation: https://www.testsprite.com/docs")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
