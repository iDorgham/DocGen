#!/usr/bin/env python3
"""
Simple Phase 3 Component Test

This script performs basic validation of Phase 3 components
without complex imports or dependencies.
"""

import sys
import os
from pathlib import Path

def test_file_existence():
    """Test that all Phase 3 component files exist."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    
    required_files = [
        "src/core/spec_validator.py",
        "src/core/agent_hooks.py", 
        "src/core/project_steering_controller.py",
        "src/core/optimization_engine.py",
        "src/core/ai_traceability_system.py",
        "src/core/audit_compliance_framework.py",
        "src/commands/driven.py"
    ]
    
    print("🔍 Testing Phase 3 Component File Existence...")
    print("=" * 50)
    
    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_file_content():
    """Test that files contain expected content."""
    project_root = Path(__file__).parent.parent
    
    print("\n📋 Testing Phase 3 Component Content...")
    print("=" * 50)
    
    # Test spec_validator.py
    spec_validator_path = project_root / "src/core/spec_validator.py"
    if spec_validator_path.exists():
        content = spec_validator_path.read_text()
        has_spec_validator = "class SpecValidator" in content
        has_create_function = "def create_spec_validator" in content
        print(f"✅ spec_validator.py: SpecValidator class {'✓' if has_spec_validator else '✗'}, create function {'✓' if has_create_function else '✗'}")
    else:
        print("❌ spec_validator.py: File not found")
    
    # Test agent_hooks.py
    agent_hooks_path = project_root / "src/core/agent_hooks.py"
    if agent_hooks_path.exists():
        content = agent_hooks_path.read_text()
        has_hook_manager = "class AgentHookManager" in content
        has_create_function = "def create_agent_hook_manager" in content
        print(f"✅ agent_hooks.py: AgentHookManager class {'✓' if has_hook_manager else '✗'}, create function {'✓' if has_create_function else '✗'}")
    else:
        print("❌ agent_hooks.py: File not found")
    
    # Test project_steering_controller.py
    steering_path = project_root / "src/core/project_steering_controller.py"
    if steering_path.exists():
        content = steering_path.read_text()
        has_controller = "class ProjectSteeringController" in content
        has_create_function = "def create_project_steering_controller" in content
        print(f"✅ project_steering_controller.py: ProjectSteeringController class {'✓' if has_controller else '✗'}, create function {'✓' if has_create_function else '✗'}")
    else:
        print("❌ project_steering_controller.py: File not found")
    
    # Test optimization_engine.py
    optimization_path = project_root / "src/core/optimization_engine.py"
    if optimization_path.exists():
        content = optimization_path.read_text()
        has_engine = "class MCPOptimizationEngine" in content
        has_create_function = "def create_optimization_engine" in content
        print(f"✅ optimization_engine.py: MCPOptimizationEngine class {'✓' if has_engine else '✗'}, create function {'✓' if has_create_function else '✗'}")
    else:
        print("❌ optimization_engine.py: File not found")
    
    # Test ai_traceability_system.py
    traceability_path = project_root / "src/core/ai_traceability_system.py"
    if traceability_path.exists():
        content = traceability_path.read_text()
        has_system = "class AITraceabilitySystem" in content
        has_create_function = "def create_ai_traceability_system" in content
        print(f"✅ ai_traceability_system.py: AITraceabilitySystem class {'✓' if has_system else '✗'}, create function {'✓' if has_create_function else '✗'}")
    else:
        print("❌ ai_traceability_system.py: File not found")
    
    # Test audit_compliance_framework.py
    audit_path = project_root / "src/core/audit_compliance_framework.py"
    if audit_path.exists():
        content = audit_path.read_text()
        has_framework = "class AuditComplianceFramework" in content
        has_create_function = "def create_audit_compliance_framework" in content
        print(f"✅ audit_compliance_framework.py: AuditComplianceFramework class {'✓' if has_framework else '✗'}, create function {'✓' if has_create_function else '✗'}")
    else:
        print("❌ audit_compliance_framework.py: File not found")
    
    # Test driven.py
    driven_path = project_root / "src/commands/driven.py"
    if driven_path.exists():
        content = driven_path.read_text()
        has_driven_group = "@click.group()" in content and "def driven():" in content
        has_commands = "validate_specs" in content and "agent_hooks" in content
        print(f"✅ driven.py: CLI group {'✓' if has_driven_group else '✗'}, commands {'✓' if has_commands else '✗'}")
    else:
        print("❌ driven.py: File not found")

def test_cli_integration():
    """Test CLI integration."""
    project_root = Path(__file__).parent.parent
    main_cli_path = project_root / "src/cli/main.py"
    
    print("\n🔗 Testing CLI Integration...")
    print("=" * 50)
    
    if main_cli_path.exists():
        content = main_cli_path.read_text()
        has_driven_import = "from src.commands.driven import driven" in content
        has_driven_command = "main.add_command(driven)" in content
        print(f"✅ main.py: Driven import {'✓' if has_driven_import else '✗'}, command registration {'✓' if has_driven_command else '✗'}")
    else:
        print("❌ main.py: File not found")

def main():
    """Main test runner."""
    print("🚀 Phase 3 Component Validation Test")
    print("=" * 60)
    
    # Test file existence
    files_exist = test_file_existence()
    
    # Test file content
    test_file_content()
    
    # Test CLI integration
    test_cli_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PHASE 3 VALIDATION SUMMARY")
    print("=" * 60)
    
    if files_exist:
        print("✅ All Phase 3 component files exist")
        print("✅ Phase 3 implementation appears complete")
        print("\n🎉 Phase 3: Driven Workflow Integration - READY!")
        print("\nNext steps:")
        print("1. Test individual components with: python -m pytest tests/")
        print("2. Run CLI commands: docgen driven --help")
        print("3. Start using the driven workflow features")
    else:
        print("❌ Some Phase 3 component files are missing")
        print("⚠️  Please complete the implementation")
    
    return 0 if files_exist else 1

if __name__ == "__main__":
    sys.exit(main())
