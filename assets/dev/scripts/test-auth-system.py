#!/usr/bin/env python3
"""
Test Script for Comprehensive Authentication System
Tests all components of the authentication system to ensure proper functionality.

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import time
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing module imports...")
    
    try:
        from real_time_auth_tracker import RealTimeAuthTracker, AuthStatus
        logger.info("✅ Real-time Auth Tracker imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Real-time Auth Tracker: {e}")
        return False
    
    try:
        from secure_key_manager import SecureKeyManager, KeyStatus
        logger.info("✅ Secure Key Manager imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Secure Key Manager: {e}")
        return False
    
    try:
        from error_recovery_system import ErrorRecoverySystem, ErrorType, RecoveryStrategy
        logger.info("✅ Error Recovery System imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Error Recovery System: {e}")
        return False
    
    try:
        from setup_wizard import SetupWizard, SetupStatus
        logger.info("✅ Setup Wizard imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Setup Wizard: {e}")
        return False
    
    try:
        from comprehensive_auth_system import ComprehensiveAuthSystem, SystemStatus
        logger.info("✅ Comprehensive Auth System imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Comprehensive Auth System: {e}")
        return False
    
    return True

def test_auth_tracker():
    """Test Real-time Authentication Tracker."""
    logger.info("Testing Real-time Authentication Tracker...")
    
    try:
        from real_time_auth_tracker import RealTimeAuthTracker
        
        # Initialize tracker
        tracker = RealTimeAuthTracker()
        logger.info("✅ Auth Tracker initialized")
        
        # Check authentication status
        results = tracker.check_all_authentication()
        logger.info(f"✅ Authentication check completed for {len(results)} servers")
        
        # Get summary
        summary = tracker.get_authentication_summary()
        logger.info(f"✅ Authentication summary: {summary['authenticated_servers']}/{summary['total_servers']} authenticated")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Auth Tracker test failed: {e}")
        return False

def test_key_manager():
    """Test Secure Key Manager."""
    logger.info("Testing Secure Key Manager...")
    
    try:
        from secure_key_manager import SecureKeyManager
        
        # Initialize key manager
        key_manager = SecureKeyManager()
        logger.info("✅ Key Manager initialized")
        
        # Get key summary
        summary = key_manager.get_key_summary()
        logger.info(f"✅ Key summary: {summary['total_keys']} total keys, {summary['active_keys']} active")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Key Manager test failed: {e}")
        return False

def test_error_recovery():
    """Test Error Recovery System."""
    logger.info("Testing Error Recovery System...")
    
    try:
        from error_recovery_system import ErrorRecoverySystem
        
        # Initialize error recovery
        recovery = ErrorRecoverySystem()
        logger.info("✅ Error Recovery System initialized")
        
        # Get recovery summary
        summary = recovery.get_recovery_summary()
        logger.info(f"✅ Recovery summary: {summary['total_recovery_actions']} actions, {summary['success_rate']:.1%} success rate")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error Recovery test failed: {e}")
        return False

def test_setup_wizard():
    """Test Setup Wizard."""
    logger.info("Testing Setup Wizard...")
    
    try:
        from setup_wizard import SetupWizard
        
        # Initialize setup wizard
        wizard = SetupWizard()
        logger.info("✅ Setup Wizard initialized")
        
        # Check setup steps
        total_steps = sum(len(steps) for steps in wizard.setup_steps.values())
        logger.info(f"✅ Setup steps loaded: {total_steps} total steps for {len(wizard.setup_steps)} servers")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Setup Wizard test failed: {e}")
        return False

def test_comprehensive_system():
    """Test Comprehensive Authentication System."""
    logger.info("Testing Comprehensive Authentication System...")
    
    try:
        from comprehensive_auth_system import ComprehensiveAuthSystem
        
        # Initialize comprehensive system
        auth_system = ComprehensiveAuthSystem()
        logger.info("✅ Comprehensive Auth System initialized")
        
        # Get system status
        status = auth_system.get_system_status()
        logger.info(f"✅ System status: {status['overall_status']}")
        
        # Calculate system health
        health = auth_system.calculate_system_health()
        logger.info(f"✅ System health: {health.overall_status.value}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Comprehensive System test failed: {e}")
        return False

def test_integration():
    """Test integration between components."""
    logger.info("Testing component integration...")
    
    try:
        from comprehensive_auth_system import ComprehensiveAuthSystem
        
        # Initialize system
        auth_system = ComprehensiveAuthSystem()
        
        # Test status callback
        callback_called = False
        
        def test_callback(old_health, new_health):
            nonlocal callback_called
            callback_called = True
            logger.info(f"Status change callback triggered: {old_health.overall_status.value} -> {new_health.overall_status.value}")
        
        # Add callback
        auth_system.add_status_callback(test_callback)
        
        # Start health monitoring briefly
        auth_system.start_health_monitoring()
        time.sleep(2)
        auth_system.stop_health_monitoring()
        
        logger.info("✅ Component integration test completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    logger.info("Starting Comprehensive Authentication System Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Auth Tracker", test_auth_tracker),
        ("Key Manager", test_key_manager),
        ("Error Recovery", test_error_recovery),
        ("Setup Wizard", test_setup_wizard),
        ("Comprehensive System", test_comprehensive_system),
        ("Integration", test_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Running {test_name} Test ---")
        try:
            success = test_func()
            results[test_name] = success
            if success:
                logger.info(f"✅ {test_name} test PASSED")
            else:
                logger.error(f"❌ {test_name} test FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} test ERROR: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Authentication system is working correctly.")
        return True
    else:
        logger.error(f"⚠️ {total - passed} tests failed. Please check the errors above.")
        return False

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Comprehensive Authentication System")
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--component', type=str, help='Test specific component')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.component:
            # Test specific component
            if args.component == 'imports':
                success = test_imports()
            elif args.component == 'auth_tracker':
                success = test_auth_tracker()
            elif args.component == 'key_manager':
                success = test_key_manager()
            elif args.component == 'error_recovery':
                success = test_error_recovery()
            elif args.component == 'setup_wizard':
                success = test_setup_wizard()
            elif args.component == 'comprehensive':
                success = test_comprehensive_system()
            elif args.component == 'integration':
                success = test_integration()
            else:
                logger.error(f"Unknown component: {args.component}")
                return 1
            
            return 0 if success else 1
        else:
            # Run all tests
            success = run_all_tests()
            return 0 if success else 1
            
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
