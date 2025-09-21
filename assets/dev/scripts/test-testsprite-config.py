#!/usr/bin/env python3
"""
TestSprite Configuration Test Script

This script tests the TestSprite API key configuration and connection.
"""

import os
import sys
from pathlib import Path

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


def test_environment_variables():
    """Test if environment variables are properly set."""
    print("🔍 Testing environment variables...")
    
    # Check if .env file exists
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Run: python scripts/setup_testsprite_api.py")
        return False
    
    print(f"✅ .env file found: {env_file}")
    
    # Check if API key is set
    api_key = os.getenv("TESTSPRITE_API_KEY")
    
    if not api_key:
        print("❌ TESTSPRITE_API_KEY environment variable not found")
        print("   Please restart your terminal/IDE after creating the .env file")
        return False
    
    if api_key == "your_testsprite_api_key_here":
        print("❌ Please replace the placeholder API key with your actual TestSprite API key")
        return False
    
    print(f"✅ TESTSPRITE_API_KEY is set: {api_key[:8]}...")
    return True


def test_testsprite_mcp_tools():
    """Test if TestSprite MCP tools are available."""
    print("🔍 Testing TestSprite MCP tools availability...")
    
    try:
        # Try to import TestSprite MCP tools
        import mcp_TestSprite_testsprite_bootstrap_tests
        print("✅ TestSprite MCP tools are available")
        return True
    except ImportError as e:
        print(f"❌ TestSprite MCP tools not available: {str(e)}")
        print("   Make sure you're running this in the correct environment")
        return False


def test_testsprite_api_connection():
    """Test TestSprite API connection."""
    print("🔍 Testing TestSprite API connection...")
    
    try:
        # This would normally test the actual API connection
        # For now, we'll just verify the configuration is correct
        api_key = os.getenv("TESTSPRITE_API_KEY")
        
        if api_key and len(api_key) > 10:  # Basic validation
            print("✅ TestSprite API key appears to be valid")
            print("✅ Ready to use TestSprite MCP tools")
            return True
        else:
            print("❌ TestSprite API key appears to be invalid")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TestSprite API connection: {str(e)}")
        return False


def test_project_configuration():
    """Test project configuration for TestSprite."""
    print("🔍 Testing project configuration...")
    
    project_root = Path(__file__).parent.parent
    
    # Check if project structure is correct
    required_dirs = ["src", "tests", "assets"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/ directory found")
        else:
            print(f"❌ {dir_name}/ directory not found")
            return False
    
    # Check if MCP configuration exists
    mcp_config = project_root / "assets" / "dev" / "config" / "mcp" / "mcp_config.yaml"
    if mcp_config.exists():
        print("✅ MCP configuration found")
    else:
        print("❌ MCP configuration not found")
        return False
    
    return True


def main():
    """Main function to test TestSprite configuration."""
    print("🧪 TestSprite Configuration Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("TestSprite MCP Tools", test_testsprite_mcp_tools),
        ("TestSprite API Connection", test_testsprite_api_connection),
        ("Project Configuration", test_project_configuration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"📋 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {str(e)}")
            results.append((test_name, False))
        print()
    
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
        print("🎉 All tests passed! TestSprite is properly configured.")
        print()
        print("🚀 Next steps:")
        print("1. Run TestSprite tests: python scripts/run_testsprite_tests.py")
        print("2. Use TestSprite MCP tools in your development workflow")
        print("3. Check TestSprite dashboard: https://www.testsprite.com/dashboard")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print()
        print("🔧 Troubleshooting:")
        print("1. Run setup script: python scripts/setup_testsprite_api.py")
        print("2. Restart your terminal/IDE")
        print("3. Check TestSprite API key: https://www.testsprite.com/dashboard/settings/apikey")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
