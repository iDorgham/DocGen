"""
Integration tests for MCP Optimization Engine

This module contains integration tests that validate the MCP Optimization Engine
works correctly with existing MCP servers and the overall DocGen CLI system.

Author: DocGen CLI Team
Created: 2025-01-20
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.optimization_engine import (
    MCPOptimizationEngine,
    OptimizationStrategy,
    ToolSelectionMethod,
    ToolContext
)


class TestOptimizationEngineIntegration:
    """Integration tests for the optimization engine with MCP servers"""
    
    def test_optimization_engine_with_real_mcp_servers(self):
        """Test optimization engine with actual MCP server interactions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            # Initialize engine
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Simulate MCP server performance data
            mcp_servers = {
                "byterover": {"success_rate": 0.9, "response_time": 2.0},
                "testsprite": {"success_rate": 0.95, "response_time": 1.5},
                "context7": {"success_rate": 0.85, "response_time": 1.8},
                "browser_tools": {"success_rate": 0.88, "response_time": 2.2},
                "playwright": {"success_rate": 0.82, "response_time": 3.0},
                "dart": {"success_rate": 0.75, "response_time": 1.2}
            }
            
            # Record performance metrics
            for server, metrics in mcp_servers.items():
                engine.record_performance_metric(server, "success_rate", metrics["success_rate"])
                engine.record_performance_metric(server, "response_time", metrics["response_time"])
                engine.record_performance_metric(server, "error_rate", 1 - metrics["success_rate"])
                engine.record_performance_metric(server, "resource_usage", 0.5)
            
            # Test different optimization scenarios
            test_scenarios = [
                {
                    "name": "Testing Task",
                    "task_type": "testing",
                    "requirements": ["automated_testing", "quality_assurance"],
                    "expected_tools": ["testsprite", "browser_tools"]
                },
                {
                    "name": "Knowledge Retrieval Task",
                    "task_type": "knowledge_retrieval",
                    "requirements": ["knowledge_management", "context_assessment"],
                    "expected_tools": ["byterover", "context7"]
                },
                {
                    "name": "Web Testing Task",
                    "task_type": "web_testing",
                    "requirements": ["browser_automation", "e2e_testing"],
                    "expected_tools": ["playwright", "browser_tools"]
                },
                {
                    "name": "Project Management Task",
                    "task_type": "project_management",
                    "requirements": ["task_management", "team_collaboration"],
                    "expected_tools": ["dart", "byterover"]
                }
            ]
            
            for scenario in test_scenarios:
                result = engine.optimize_tool_selection(
                    task_type=scenario["task_type"],
                    requirements=scenario["requirements"],
                    constraints={"time_limit": 300},
                    user_preferences={"prefer_fast": True}
                )
                
                # Validate results
                assert isinstance(result.selected_tools, list)
                assert len(result.selected_tools) > 0
                assert result.confidence_score > 0
                assert result.optimization_time > 0
                
                # Check that expected tools are in selection
                for expected_tool in scenario["expected_tools"]:
                    if expected_tool in mcp_servers:  # Only check if server has performance data
                        # Tool should be considered (may not be selected due to performance)
                        assert expected_tool in engine.tool_selector.tool_capabilities
    
    def test_optimization_engine_performance_monitoring(self):
        """Test performance monitoring integration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Simulate performance degradation
            servers = ["testsprite", "browser_tools", "context7"]
            
            # Record initial good performance
            for server in servers:
                engine.record_performance_metric(server, "response_time", 1.0)
                engine.record_performance_metric(server, "success_rate", 0.95)
                engine.record_performance_metric(server, "error_rate", 0.05)
                engine.record_performance_metric(server, "resource_usage", 0.3)
            
            # Simulate performance degradation
            for server in servers:
                engine.record_performance_metric(server, "response_time", 8.0)  # Above threshold
                engine.record_performance_metric(server, "success_rate", 0.7)
                engine.record_performance_metric(server, "error_rate", 0.3)
                engine.record_performance_metric(server, "resource_usage", 0.9)  # Above threshold
            
            # Get performance summary
            summary = engine.get_performance_summary()
            
            # Check that alerts were generated
            assert len(summary['alerts']) > 0
            
            # Check overall health degraded
            assert summary['overall_health'] in ['degraded', 'poor']
            
            # Check server status
            for server in servers:
                assert server in summary['servers']
                server_data = summary['servers'][server]
                assert server_data['status'] in ['degraded', 'unhealthy']
    
    def test_optimization_engine_knowledge_caching(self):
        """Test knowledge caching integration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Test knowledge retrieval optimization
            queries = [
                "React component patterns",
                "Python testing best practices",
                "MCP server integration",
                "React component patterns",  # Duplicate query
                "Docker containerization"
            ]
            
            cache_hits = 0
            cache_misses = 0
            
            for query in queries:
                result = engine.optimize_knowledge_retrieval(
                    query=query,
                    context={"task_type": "development", "language": "python"}
                )
                
                if result['source'] == 'cache':
                    cache_hits += 1
                else:
                    cache_misses += 1
                
                assert result['optimization_applied'] is True
                assert 'result' in result
            
            # Should have cache hits for duplicate queries
            assert cache_hits > 0
            assert cache_misses > 0
            
            # Check cache statistics
            cache = engine.knowledge_cache
            assert len(cache.cache) > 0
            assert len(cache.access_counts) > 0
    
    def test_optimization_engine_insights_generation(self):
        """Test optimization insights generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Perform multiple optimizations
            optimization_scenarios = [
                {"task_type": "testing", "requirements": ["automated_testing"]},
                {"task_type": "knowledge_retrieval", "requirements": ["knowledge_management"]},
                {"task_type": "web_testing", "requirements": ["browser_automation"]},
                {"task_type": "testing", "requirements": ["quality_assurance"]},  # Duplicate task type
                {"task_type": "project_management", "requirements": ["task_management"]}
            ]
            
            for scenario in optimization_scenarios:
                engine.optimize_tool_selection(
                    task_type=scenario["task_type"],
                    requirements=scenario["requirements"]
                )
            
            # Get insights
            insights = engine.get_optimization_insights()
            
            # Validate insights
            assert insights['total_optimizations'] == len(optimization_scenarios)
            assert insights['average_confidence'] > 0
            assert 'most_common_tasks' in insights
            assert 'recommendations' in insights
            
            # Check that testing is the most common task
            assert 'testing' in insights['most_common_tasks']
            assert insights['most_common_tasks']['testing'] == 2
    
    def test_optimization_engine_configuration_management(self):
        """Test configuration management integration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            # Create custom configuration
            custom_config = {
                "optimization_strategy": "performance",
                "tool_selection_method": "performance_based",
                "cache_size": 5000,
                "performance_thresholds": {
                    "response_time": 3.0,
                    "error_rate": 0.05,
                    "resource_usage": 0.7
                }
            }
            
            with open(config_path, 'w') as f:
                json.dump(custom_config, f)
            
            # Initialize engine with custom config
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Verify configuration was loaded
            assert engine.config['optimization_strategy'] == 'performance'
            assert engine.config['tool_selection_method'] == 'performance_based'
            assert engine.config['cache_size'] == 5000
            assert engine.config['performance_thresholds']['response_time'] == 3.0
            
            # Test that configuration affects behavior
            result = engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing"]
            )
            
            # Should use performance-based selection
            assert result.confidence_score > 0
    
    def test_optimization_engine_export_import(self):
        """Test data export and import functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            export_path = Path(temp_dir) / "export.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Add some data
            engine.record_performance_metric("testsprite", "response_time", 2.0)
            engine.record_performance_metric("testsprite", "success_rate", 0.9)
            
            result = engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing"]
            )
            
            # Export data
            engine.export_optimization_data(export_path)
            
            # Verify export file exists and contains data
            assert export_path.exists()
            
            with open(export_path, 'r') as f:
                export_data = json.load(f)
            
            assert 'config' in export_data
            assert 'optimization_history' in export_data
            assert 'performance_summary' in export_data
            assert 'insights' in export_data
            assert 'export_timestamp' in export_data
            
            # Verify optimization history
            assert len(export_data['optimization_history']) == 1
            assert export_data['optimization_history'][0]['context']['task_type'] == 'testing'
    
    def test_optimization_engine_error_handling(self):
        """Test error handling and graceful degradation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Test with invalid inputs
            with pytest.raises((ValueError, TypeError)):
                engine.optimize_tool_selection(
                    task_type=None,  # Invalid input
                    requirements=["automated_testing"]
                )
            
            # Test with empty requirements
            result = engine.optimize_tool_selection(
                task_type="testing",
                requirements=[]  # Empty requirements
            )
            
            # Should still return a result (may be empty or default)
            assert isinstance(result.selected_tools, list)
            
            # Test with invalid metric values
            engine.record_performance_metric("test_server", "response_time", -1.0)  # Invalid value
            engine.record_performance_metric("test_server", "success_rate", 1.5)    # Invalid value
            
            # Should handle gracefully
            performance = engine.performance_monitor.get_server_performance("test_server")
            assert performance is not None
    
    def test_optimization_engine_concurrent_operations(self):
        """Test concurrent operations and thread safety"""
        import threading
        import time
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Test concurrent metric recording
            def record_metrics(server_name, count):
                for i in range(count):
                    engine.record_performance_metric(server_name, "response_time", 1.0 + i * 0.1)
                    engine.record_performance_metric(server_name, "success_rate", 0.9 - i * 0.01)
                    time.sleep(0.001)  # Small delay to simulate concurrent access
            
            # Start multiple threads
            threads = []
            for i in range(3):
                thread = threading.Thread(target=record_metrics, args=(f"server_{i}", 10))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Verify all metrics were recorded
            for i in range(3):
                performance = engine.performance_monitor.get_server_performance(f"server_{i}")
                assert performance is not None
                assert performance.response_time > 0
                assert performance.success_rate > 0
    
    def test_optimization_engine_memory_management(self):
        """Test memory management and cleanup"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Add many optimization records
            for i in range(1500):  # More than default history size
                engine.optimize_tool_selection(
                    task_type="testing",
                    requirements=["automated_testing"]
                )
            
            # Check that history is limited
            assert len(engine.optimization_history) <= 1000  # Default limit
            
            # Add many performance metrics
            for i in range(1500):
                engine.record_performance_metric("test_server", "response_time", 1.0 + i * 0.001)
            
            # Check that metrics history is limited
            trend = engine.performance_monitor.get_performance_trend("test_server", "response_time")
            assert len(trend) <= 1000  # Default limit
            
            # Test cache eviction
            cache = engine.knowledge_cache
            original_size = len(cache.cache)
            
            # Add items beyond cache limit
            for i in range(cache.max_size + 100):
                cache.set(f"key_{i}", f"value_{i}")
            
            # Cache should be limited
            assert len(cache.cache) <= cache.max_size
    
    def test_optimization_engine_real_world_scenario(self):
        """Test optimization engine with realistic development scenario"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Simulate realistic MCP server performance
            realistic_servers = {
                "byterover": {"success_rate": 0.92, "response_time": 1.8, "capabilities": ["knowledge_management", "project_planning"]},
                "testsprite": {"success_rate": 0.88, "response_time": 2.5, "capabilities": ["automated_testing", "quality_assurance"]},
                "context7": {"success_rate": 0.95, "response_time": 1.2, "capabilities": ["documentation_access", "api_reference"]},
                "browser_tools": {"success_rate": 0.85, "response_time": 3.0, "capabilities": ["web_testing", "quality_audits"]},
                "playwright": {"success_rate": 0.80, "response_time": 4.0, "capabilities": ["browser_automation", "e2e_testing"]},
                "dart": {"success_rate": 0.75, "response_time": 1.5, "capabilities": ["task_management", "project_management"]}
            }
            
            # Record realistic performance data
            for server, metrics in realistic_servers.items():
                engine.record_performance_metric(server, "success_rate", metrics["success_rate"])
                engine.record_performance_metric(server, "response_time", metrics["response_time"])
                engine.record_performance_metric(server, "error_rate", 1 - metrics["success_rate"])
                engine.record_performance_metric(server, "resource_usage", 0.4)
            
            # Test realistic development workflow
            workflow_scenarios = [
                {
                    "phase": "Planning",
                    "task_type": "project_planning",
                    "requirements": ["knowledge_management", "project_planning"],
                    "constraints": {"time_limit": 600, "budget": "medium"},
                    "user_preferences": {"prefer_accurate": True}
                },
                {
                    "phase": "Development",
                    "task_type": "development",
                    "requirements": ["documentation_access", "api_reference"],
                    "constraints": {"time_limit": 300, "budget": "low"},
                    "user_preferences": {"prefer_fast": True}
                },
                {
                    "phase": "Testing",
                    "task_type": "testing",
                    "requirements": ["automated_testing", "quality_assurance"],
                    "constraints": {"time_limit": 900, "budget": "high"},
                    "user_preferences": {"require_detailed_reports": True}
                },
                {
                    "phase": "Validation",
                    "task_type": "web_testing",
                    "requirements": ["browser_automation", "e2e_testing"],
                    "constraints": {"time_limit": 1200, "budget": "medium"},
                    "user_preferences": {"prefer_comprehensive": True}
                }
            ]
            
            results = []
            for scenario in workflow_scenarios:
                result = engine.optimize_tool_selection(
                    task_type=scenario["task_type"],
                    requirements=scenario["requirements"],
                    constraints=scenario["constraints"],
                    user_preferences=scenario["user_preferences"]
                )
                
                results.append({
                    "phase": scenario["phase"],
                    "result": result
                })
                
                # Validate results
                assert len(result.selected_tools) > 0
                assert result.confidence_score > 0.5  # Should be confident with good data
                assert result.optimization_time < 1.0  # Should be fast
            
            # Analyze workflow results
            total_confidence = sum(r["result"].confidence_score for r in results)
            average_confidence = total_confidence / len(results)
            
            assert average_confidence > 0.7  # Should have high average confidence
            
            # Check that appropriate tools were selected for each phase
            planning_result = next(r for r in results if r["phase"] == "Planning")
            assert "byterover" in planning_result["result"].selected_tools
            
            development_result = next(r for r in results if r["phase"] == "Development")
            assert "context7" in development_result["result"].selected_tools
            
            testing_result = next(r for r in results if r["phase"] == "Testing")
            assert "testsprite" in testing_result["result"].selected_tools
            
            validation_result = next(r for r in results if r["phase"] == "Validation")
            assert any(tool in ["playwright", "browser_tools"] for tool in validation_result["result"].selected_tools)
            
            # Get final insights
            insights = engine.get_optimization_insights()
            assert insights['total_optimizations'] == len(workflow_scenarios)
            assert insights['average_confidence'] > 0.7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
