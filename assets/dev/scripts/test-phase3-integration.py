#!/usr/bin/env python3
"""
Phase 3 Integration Test Script

This script tests all Phase 3 components of the DocGen CLI:
- Spec Validation System
- Agent Hooks System
- Project Steering Controller
- MCP Optimization Engine
- AI Traceability System
- Audit Compliance Framework
- Driven Workflow Integration

Usage:
    python scripts/test_phase3_integration.py
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from core.spec_validator import create_spec_validator
    from core.agent_hooks import create_agent_hook_manager
    from core.project_steering_controller import create_project_steering_controller, SteeringMode
    from core.optimization_engine import create_optimization_engine, OptimizationStrategy, ToolSelectionMethod
    from core.ai_traceability_system import create_ai_traceability_system, AIDecision, DecisionType, ImpactLevel, TraceabilityLevel
    from core.audit_compliance_framework import create_audit_compliance_framework, AuditType
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all Phase 3 components are properly implemented.")
    sys.exit(1)


class Phase3IntegrationTester:
    """Test suite for Phase 3 components."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_results = {
            "spec_validation": {"passed": False, "errors": []},
            "agent_hooks": {"passed": False, "errors": []},
            "project_steering": {"passed": False, "errors": []},
            "mcp_optimization": {"passed": False, "errors": []},
            "ai_traceability": {"passed": False, "errors": []},
            "audit_compliance": {"passed": False, "errors": []},
            "driven_workflow": {"passed": False, "errors": []}
        }
        self.start_time = time.time()
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 3 integration tests."""
        print("🚀 Starting Phase 3 Integration Tests")
        print("=" * 60)
        
        # Test each component
        self.test_spec_validation()
        self.test_agent_hooks()
        self.test_project_steering()
        self.test_mcp_optimization()
        self.test_ai_traceability()
        self.test_audit_compliance()
        self.test_driven_workflow()
        
        # Generate summary
        return self.generate_summary()
    
    def test_spec_validation(self):
        """Test Spec Validation System."""
        print("\n📋 Testing Spec Validation System...")
        
        try:
            # Create spec validator
            spec_validator = create_spec_validator(self.project_root)
            
            # Test spec compliance validation
            validation_result = spec_validator.validate_spec_compliance()
            print(f"  ✓ Spec compliance validation: {validation_result.compliance_score}%")
            
            # Test traceability validation
            traceability_result = spec_validator.validate_spec_to_code_traceability()
            print(f"  ✓ Traceability validation: {traceability_result['traceability_score']}%")
            
            # Test compliance report generation
            compliance_report = spec_validator.generate_compliance_report()
            print(f"  ✓ Compliance report generated: {len(compliance_report.get('recommendations', []))} recommendations")
            
            self.test_results["spec_validation"]["passed"] = True
            print("  ✅ Spec Validation System: PASSED")
            
        except Exception as e:
            error_msg = f"Spec validation failed: {str(e)}"
            self.test_results["spec_validation"]["errors"].append(error_msg)
            print(f"  ❌ Spec Validation System: FAILED - {error_msg}")
    
    def test_agent_hooks(self):
        """Test Agent Hooks System."""
        print("\n🔗 Testing Agent Hooks System...")
        
        try:
            # Create agent hook manager
            hook_manager = create_agent_hook_manager(self.project_root)
            
            # Test hook status
            hook_status = hook_manager.get_hook_status()
            print(f"  ✓ Hook status retrieved: {hook_status['total_hooks']} total hooks")
            
            # Test starting monitoring (briefly)
            hook_manager.start_monitoring()
            print("  ✓ Monitoring started")
            
            # Test stopping monitoring
            hook_manager.stop_monitoring()
            print("  ✓ Monitoring stopped")
            
            self.test_results["agent_hooks"]["passed"] = True
            print("  ✅ Agent Hooks System: PASSED")
            
        except Exception as e:
            error_msg = f"Agent hooks failed: {str(e)}"
            self.test_results["agent_hooks"]["errors"].append(error_msg)
            print(f"  ❌ Agent Hooks System: FAILED - {error_msg}")
    
    def test_project_steering(self):
        """Test Project Steering Controller."""
        print("\n🎯 Testing Project Steering Controller...")
        
        try:
            # Create project steering controller
            steering_controller = create_project_steering_controller(
                self.project_root, 
                SteeringMode.AUTOMATIC
            )
            
            # Test project status
            project_status = steering_controller.get_project_status()
            print(f"  ✓ Project status retrieved: {project_status['project_name']}")
            
            # Test starting steering
            steering_controller.start_steering()
            print("  ✓ Steering started")
            
            # Test quality gate
            from core.project_steering_controller import QualityGate
            quality_result = steering_controller.run_quality_gate(QualityGate.PRE_COMMIT)
            print(f"  ✓ Quality gate executed: {quality_result.score:.1f}%")
            
            # Test stopping steering
            steering_controller.stop_steering()
            print("  ✓ Steering stopped")
            
            self.test_results["project_steering"]["passed"] = True
            print("  ✅ Project Steering Controller: PASSED")
            
        except Exception as e:
            error_msg = f"Project steering failed: {str(e)}"
            self.test_results["project_steering"]["errors"].append(error_msg)
            print(f"  ❌ Project Steering Controller: FAILED - {error_msg}")
    
    def test_mcp_optimization(self):
        """Test MCP Optimization Engine."""
        print("\n⚡ Testing MCP Optimization Engine...")
        
        try:
            # Create optimization engine
            optimization_engine = create_optimization_engine(self.project_root)
            
            # Test tool selection
            tool_context = {
                "task_type": "code_generation",
                "complexity": "medium",
                "available_tools": ["byterover", "context7", "testsprite"],
                "user_preferences": {"speed": "high", "accuracy": "medium"}
            }
            
            selection_result = optimization_engine.select_optimal_tools(
                tool_context,
                OptimizationStrategy.BALANCED,
                ToolSelectionMethod.ML_BASED
            )
            print(f"  ✓ Tool selection: {len(selection_result.selected_tools)} tools selected")
            
            # Test performance optimization
            optimization_result = optimization_engine.optimize_performance(
                tool_context,
                OptimizationStrategy.PERFORMANCE_FOCUSED
            )
            print(f"  ✓ Performance optimization: {optimization_result.improvement_percentage:.1f}% improvement")
            
            # Test knowledge management
            knowledge_result = optimization_engine.optimize_knowledge_management(
                tool_context,
                OptimizationStrategy.KNOWLEDGE_FOCUSED
            )
            print(f"  ✓ Knowledge management: {knowledge_result.improvement_percentage:.1f}% improvement")
            
            self.test_results["mcp_optimization"]["passed"] = True
            print("  ✅ MCP Optimization Engine: PASSED")
            
        except Exception as e:
            error_msg = f"MCP optimization failed: {str(e)}"
            self.test_results["mcp_optimization"]["errors"].append(error_msg)
            print(f"  ❌ MCP Optimization Engine: FAILED - {error_msg}")
    
    def test_ai_traceability(self):
        """Test AI Traceability System."""
        print("\n🔍 Testing AI Traceability System...")
        
        try:
            # Create AI traceability system
            traceability_system = create_ai_traceability_system(self.project_root)
            
            # Test decision logging
            test_decision = AIDecision(
                decision_id="TEST-DEC-001",
                decision_type=DecisionType.ARCHITECTURAL,
                title="Test Decision",
                description="A test decision for validation",
                rationale="Testing the traceability system",
                alternatives_considered=["Alternative 1", "Alternative 2"],
                chosen_solution="Test solution",
                impact_level=ImpactLevel.MEDIUM,
                traceability_level=TraceabilityLevel.HIGH,
                spec_references=["spec-001"],
                code_references=["src/core/test.py"],
                test_references=["tests/test_core.py"],
                documentation_references=["docs/architecture.md"],
                created_by="Test System",
                created_date=datetime.now(),
                last_updated=datetime.now(),
                status="active",
                metadata={"test": True}
            )
            
            traceability_system.log_decision(test_decision)
            print("  ✓ Decision logged successfully")
            
            # Test impact analysis
            impact_analysis = traceability_system.analyze_decision_impact("TEST-DEC-001")
            print(f"  ✓ Impact analysis: {impact_analysis.risk_assessment}")
            
            # Test compliance report
            compliance_report = traceability_system.generate_compliance_report()
            print(f"  ✓ Compliance report: {compliance_report['overall_compliance']:.1f}% compliance")
            
            self.test_results["ai_traceability"]["passed"] = True
            print("  ✅ AI Traceability System: PASSED")
            
        except Exception as e:
            error_msg = f"AI traceability failed: {str(e)}"
            self.test_results["ai_traceability"]["errors"].append(error_msg)
            print(f"  ❌ AI Traceability System: FAILED - {error_msg}")
    
    def test_audit_compliance(self):
        """Test Audit Compliance Framework."""
        print("\n📊 Testing Audit Compliance Framework...")
        
        try:
            # Create audit compliance framework
            audit_framework = create_audit_compliance_framework(self.project_root)
            
            # Test comprehensive audit
            audit_report = audit_framework.run_comprehensive_audit(AuditType.COMPREHENSIVE)
            print(f"  ✓ Comprehensive audit: {audit_report.overall_score:.1f}% score")
            
            # Test compliance dashboard
            dashboard_data = audit_framework.generate_compliance_dashboard()
            print(f"  ✓ Compliance dashboard: {dashboard_data['overall_metrics']['success_rate']:.1f}% success rate")
            
            # Test compliance monitoring
            monitoring_data = audit_framework.start_compliance_monitoring()
            print("  ✓ Compliance monitoring started")
            
            # Test stopping monitoring
            audit_framework.stop_compliance_monitoring()
            print("  ✓ Compliance monitoring stopped")
            
            self.test_results["audit_compliance"]["passed"] = True
            print("  ✅ Audit Compliance Framework: PASSED")
            
        except Exception as e:
            error_msg = f"Audit compliance failed: {str(e)}"
            self.test_results["audit_compliance"]["errors"].append(error_msg)
            print(f"  ❌ Audit Compliance Framework: FAILED - {error_msg}")
    
    def test_driven_workflow(self):
        """Test Driven Workflow Integration."""
        print("\n🔄 Testing Driven Workflow Integration...")
        
        try:
            # Test that all components can work together
            components = {
                "spec_validator": create_spec_validator(self.project_root),
                "hook_manager": create_agent_hook_manager(self.project_root),
                "steering_controller": create_project_steering_controller(self.project_root, SteeringMode.AUTOMATIC),
                "optimization_engine": create_optimization_engine(self.project_root),
                "traceability_system": create_ai_traceability_system(self.project_root),
                "audit_framework": create_audit_compliance_framework(self.project_root)
            }
            
            print("  ✓ All components created successfully")
            
            # Test integration workflow
            # 1. Start all systems
            components["hook_manager"].start_monitoring()
            components["steering_controller"].start_steering()
            components["audit_framework"].start_compliance_monitoring()
            print("  ✓ All systems started")
            
            # 2. Run validation
            validation_result = components["spec_validator"].validate_spec_compliance()
            print(f"  ✓ Spec validation: {validation_result.compliance_score}%")
            
            # 3. Run quality gate
            from core.project_steering_controller import QualityGate
            quality_result = components["steering_controller"].run_quality_gate(QualityGate.CONTINUOUS)
            print(f"  ✓ Quality gate: {quality_result.score:.1f}%")
            
            # 4. Run audit
            audit_report = components["audit_framework"].run_comprehensive_audit(AuditType.COMPREHENSIVE)
            print(f"  ✓ Audit: {audit_report.overall_score:.1f}%")
            
            # 5. Stop all systems
            components["hook_manager"].stop_monitoring()
            components["steering_controller"].stop_steering()
            components["audit_framework"].stop_compliance_monitoring()
            print("  ✓ All systems stopped")
            
            self.test_results["driven_workflow"]["passed"] = True
            print("  ✅ Driven Workflow Integration: PASSED")
            
        except Exception as e:
            error_msg = f"Driven workflow failed: {str(e)}"
            self.test_results["driven_workflow"]["errors"].append(error_msg)
            print(f"  ❌ Driven Workflow Integration: FAILED - {error_msg}")
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary."""
        end_time = time.time()
        duration = end_time - self.start_time
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["passed"])
        failed_tests = total_tests - passed_tests
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": round((passed_tests / total_tests) * 100, 1),
            "test_results": self.test_results
        }
        
        print("\n" + "=" * 60)
        print("📊 PHASE 3 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📈 Success Rate: {summary['success_rate']}%")
        print(f"✅ Passed: {passed_tests}/{total_tests}")
        print(f"❌ Failed: {failed_tests}/{total_tests}")
        
        print("\n📋 Component Results:")
        for component, result in self.test_results.items():
            status = "✅ PASSED" if result["passed"] else "❌ FAILED"
            print(f"  {component.replace('_', ' ').title()}: {status}")
            if result["errors"]:
                for error in result["errors"]:
                    print(f"    • {error}")
        
        if failed_tests == 0:
            print("\n🎉 All Phase 3 components are working correctly!")
        else:
            print(f"\n⚠️  {failed_tests} component(s) need attention.")
        
        return summary


def main():
    """Main test runner."""
    # Get project root
    project_root = Path(__file__).parent.parent
    
    # Create tester
    tester = Phase3IntegrationTester(project_root)
    
    # Run tests
    summary = tester.run_all_tests()
    
    # Save results
    results_file = project_root / "assets" / "reports" / "phase3_integration_test_results.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if summary["failed_tests"] == 0 else 1)


if __name__ == "__main__":
    main()
