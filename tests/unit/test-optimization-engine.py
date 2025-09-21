"""
Unit tests for MCP Optimization Engine

This module contains comprehensive unit tests for the MCP Optimization Engine,
including tests for tool selection, performance monitoring, knowledge caching,
and optimization algorithms.

Author: DocGen CLI Team
Created: 2025-01-20
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.optimization_engine import (
    MCPOptimizationEngine,
    PerformanceMonitor,
    IntelligentToolSelector,
    KnowledgeCache,
    OptimizationStrategy,
    ToolSelectionMethod,
    ToolContext,
    OptimizationResult,
    PerformanceMetrics
)


class TestPerformanceMetrics:
    """Test PerformanceMetrics dataclass"""
    
    def test_performance_metrics_creation(self):
        """Test creating PerformanceMetrics instance"""
        metrics = PerformanceMetrics(
            response_time=1.5,
            success_rate=0.95,
            error_rate=0.05,
            throughput=100.0,
            resource_usage=0.3,
            last_updated=datetime.now()
        )
        
        assert metrics.response_time == 1.5
        assert metrics.success_rate == 0.95
        assert metrics.error_rate == 0.05
        assert metrics.throughput == 100.0
        assert metrics.resource_usage == 0.3
        assert isinstance(metrics.last_updated, datetime)
    
    def test_performance_metrics_to_dict(self):
        """Test converting PerformanceMetrics to dictionary"""
        now = datetime.now()
        metrics = PerformanceMetrics(
            response_time=2.0,
            success_rate=0.9,
            error_rate=0.1,
            throughput=50.0,
            resource_usage=0.5,
            last_updated=now
        )
        
        result = metrics.to_dict()
        
        assert result['response_time'] == 2.0
        assert result['success_rate'] == 0.9
        assert result['error_rate'] == 0.1
        assert result['throughput'] == 50.0
        assert result['resource_usage'] == 0.5
        assert result['last_updated'] == now.isoformat()


class TestToolContext:
    """Test ToolContext dataclass"""
    
    def test_tool_context_creation(self):
        """Test creating ToolContext instance"""
        context = ToolContext(
            task_type="testing",
            complexity="medium",
            requirements=["automated_testing", "quality_assurance"],
            constraints={"time_limit": 300},
            user_preferences={"prefer_fast": True},
            historical_success={"testsprite": 0.9}
        )
        
        assert context.task_type == "testing"
        assert context.complexity == "medium"
        assert context.requirements == ["automated_testing", "quality_assurance"]
        assert context.constraints == {"time_limit": 300}
        assert context.user_preferences == {"prefer_fast": True}
        assert context.historical_success == {"testsprite": 0.9}
    
    def test_tool_context_to_dict(self):
        """Test converting ToolContext to dictionary"""
        context = ToolContext(
            task_type="knowledge_retrieval",
            complexity="simple",
            requirements=["knowledge_management"],
            constraints={},
            user_preferences={},
            historical_success={}
        )
        
        result = context.to_dict()
        
        assert result['task_type'] == "knowledge_retrieval"
        assert result['complexity'] == "simple"
        assert result['requirements'] == ["knowledge_management"]
        assert result['constraints'] == {}
        assert result['user_preferences'] == {}
        assert result['historical_success'] == {}


class TestKnowledgeCache:
    """Test KnowledgeCache class"""
    
    def test_cache_initialization(self):
        """Test cache initialization"""
        cache = KnowledgeCache(max_size=100, compression_threshold=0.8)
        
        assert cache.max_size == 100
        assert cache.compression_threshold == 0.8
        assert len(cache.cache) == 0
        assert len(cache.access_times) == 0
        assert len(cache.access_counts) == 0
    
    def test_cache_set_and_get(self):
        """Test setting and getting items from cache"""
        cache = KnowledgeCache(max_size=10)
        
        # Set an item
        cache.set("test_key", "test_value")
        
        # Get the item
        result = cache.get("test_key")
        assert result == "test_value"
        
        # Check access tracking
        assert "test_key" in cache.access_times
        assert cache.access_counts["test_key"] == 1
    
    def test_cache_miss(self):
        """Test cache miss behavior"""
        cache = KnowledgeCache()
        
        result = cache.get("nonexistent_key")
        assert result is None
    
    def test_cache_eviction(self):
        """Test cache eviction when max size is reached"""
        cache = KnowledgeCache(max_size=2)
        
        # Fill cache to capacity
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Add one more item to trigger eviction
        cache.set("key3", "value3")
        
        # First item should be evicted
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
    
    def test_cache_access_tracking(self):
        """Test cache access time and count tracking"""
        cache = KnowledgeCache()
        
        cache.set("test_key", "test_value")
        
        # First access
        cache.get("test_key")
        assert cache.access_counts["test_key"] == 1
        
        # Second access
        cache.get("test_key")
        assert cache.access_counts["test_key"] == 2
        
        # Check access time is updated
        assert "test_key" in cache.access_times


class TestPerformanceMonitor:
    """Test PerformanceMonitor class"""
    
    def test_monitor_initialization(self):
        """Test monitor initialization"""
        monitor = PerformanceMonitor(history_size=100)
        
        assert monitor.history_size == 100
        assert len(monitor.metrics_history) == 0
        assert len(monitor.current_metrics) == 0
        assert len(monitor.alerts) == 0
    
    def test_record_metric(self):
        """Test recording performance metrics"""
        monitor = PerformanceMonitor()
        
        monitor.record_metric("test_server", "response_time", 2.5)
        
        # Check metric was recorded
        assert "test_server_response_time" in monitor.metrics_history
        assert len(monitor.metrics_history["test_server_response_time"]) == 1
        
        # Check current metrics were updated
        assert "test_server" in monitor.current_metrics
        assert monitor.current_metrics["test_server"].response_time == 2.5
    
    def test_get_server_performance(self):
        """Test getting server performance metrics"""
        monitor = PerformanceMonitor()
        
        # Record some metrics
        monitor.record_metric("test_server", "response_time", 1.5)
        monitor.record_metric("test_server", "success_rate", 0.95)
        
        # Get performance
        performance = monitor.get_server_performance("test_server")
        
        assert performance is not None
        assert performance.response_time == 1.5
        assert performance.success_rate == 0.95
    
    def test_get_nonexistent_server_performance(self):
        """Test getting performance for nonexistent server"""
        monitor = PerformanceMonitor()
        
        performance = monitor.get_server_performance("nonexistent_server")
        assert performance is None
    
    def test_performance_alerts(self):
        """Test performance alert generation"""
        monitor = PerformanceMonitor()
        
        # Record metric that should trigger alert
        monitor.record_metric("test_server", "response_time", 10.0)  # Above 5.0 threshold
        
        # Check alert was generated
        assert len(monitor.alerts) == 1
        alert = monitor.alerts[0]
        assert alert['server'] == "test_server"
        assert alert['metric'] == "response_time"
        assert alert['value'] == 10.0
        assert alert['severity'] == "high"
    
    def test_get_performance_trend(self):
        """Test getting performance trend"""
        monitor = PerformanceMonitor()
        
        # Record multiple metrics
        monitor.record_metric("test_server", "response_time", 1.0)
        monitor.record_metric("test_server", "response_time", 2.0)
        monitor.record_metric("test_server", "response_time", 3.0)
        
        # Get trend
        trend = monitor.get_performance_trend("test_server", "response_time")
        
        assert len(trend) == 3
        assert trend == [1.0, 2.0, 3.0]


class TestIntelligentToolSelector:
    """Test IntelligentToolSelector class"""
    
    def test_selector_initialization(self):
        """Test selector initialization"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        assert selector.performance_monitor == monitor
        assert len(selector.tool_capabilities) > 0
        assert len(selector.selection_history) == 0
    
    def test_tool_capabilities_initialization(self):
        """Test tool capabilities are properly initialized"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        # Check that major tools are present
        assert "byterover" in selector.tool_capabilities
        assert "testsprite" in selector.tool_capabilities
        assert "context7" in selector.tool_capabilities
        assert "browser_tools" in selector.tool_capabilities
        
        # Check tool structure
        byterover = selector.tool_capabilities["byterover"]
        assert "capabilities" in byterover
        assert "strengths" in byterover
        assert "best_for" in byterover
        assert "performance_weight" in byterover
    
    def test_context_based_selection(self):
        """Test context-based tool selection"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        # Add some performance data
        monitor.record_metric("testsprite", "success_rate", 0.9)
        monitor.record_metric("browser_tools", "success_rate", 0.8)
        monitor.record_metric("context7", "success_rate", 0.85)
        
        context = ToolContext(
            task_type="testing",
            complexity="medium",
            requirements=["automated_testing", "quality_assurance"],
            constraints={},
            user_preferences={},
            historical_success={}
        )
        
        available_tools = ["testsprite", "browser_tools", "context7"]
        selected = selector._context_based_selection(context, available_tools)
        
        # Should select tools with testing capabilities
        assert "testsprite" in selected  # Has automated_testing capability
        assert "browser_tools" in selected  # Has quality_assurance capability
    
    def test_performance_based_selection(self):
        """Test performance-based tool selection"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        # Add performance data with different success rates
        monitor.record_metric("server1", "success_rate", 0.95)
        monitor.record_metric("server1", "response_time", 1.0)
        monitor.record_metric("server1", "error_rate", 0.05)
        monitor.record_metric("server1", "resource_usage", 0.3)
        
        monitor.record_metric("server2", "success_rate", 0.8)
        monitor.record_metric("server2", "response_time", 2.0)
        monitor.record_metric("server2", "error_rate", 0.2)
        monitor.record_metric("server2", "resource_usage", 0.5)
        
        context = ToolContext(
            task_type="testing",
            complexity="medium",
            requirements=[],
            constraints={},
            user_preferences={},
            historical_success={}
        )
        
        available_tools = ["server1", "server2"]
        selected = selector._performance_based_selection(context, available_tools)
        
        # Should select server1 first (better performance)
        assert selected[0] == "server1"
    
    def test_hybrid_selection(self):
        """Test hybrid tool selection"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        # Add performance data
        monitor.record_metric("testsprite", "success_rate", 0.9)
        monitor.record_metric("browser_tools", "success_rate", 0.8)
        monitor.record_metric("context7", "success_rate", 0.85)
        
        context = ToolContext(
            task_type="testing",
            complexity="medium",
            requirements=["automated_testing"],
            constraints={},
            user_preferences={},
            historical_success={}
        )
        
        available_tools = ["testsprite", "browser_tools", "context7"]
        selected = selector._hybrid_selection(context, available_tools, OptimizationStrategy.BALANCED)
        
        # Should select tools based on both context and performance
        assert len(selected) <= 3
        assert "testsprite" in selected  # Good for testing context and performance
    
    def test_calculate_confidence(self):
        """Test confidence calculation"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        # Add performance data
        monitor.record_metric("testsprite", "success_rate", 0.9)
        
        context = ToolContext(
            task_type="testing",
            complexity="medium",
            requirements=["automated_testing"],
            constraints={},
            user_preferences={},
            historical_success={}
        )
        
        selected_tools = ["testsprite"]
        confidence = selector._calculate_confidence(selected_tools, context)
        
        # Should have reasonable confidence
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be confident with good performance and context match
    
    def test_generate_reasoning(self):
        """Test reasoning generation"""
        monitor = PerformanceMonitor()
        selector = IntelligentToolSelector(monitor)
        
        monitor.record_metric("testsprite", "success_rate", 0.9)
        
        context = ToolContext(
            task_type="testing",
            complexity="medium",
            requirements=["automated_testing"],
            constraints={},
            user_preferences={},
            historical_success={}
        )
        
        selected_tools = ["testsprite"]
        reasoning = selector._generate_reasoning(selected_tools, context, OptimizationStrategy.BALANCED)
        
        assert isinstance(reasoning, str)
        assert "testsprite" in reasoning
        assert "testing" in reasoning
        assert "BALANCED" in reasoning


class TestMCPOptimizationEngine:
    """Test MCPOptimizationEngine class"""
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            assert engine.config_path == config_path
            assert isinstance(engine.performance_monitor, PerformanceMonitor)
            assert isinstance(engine.tool_selector, IntelligentToolSelector)
            assert isinstance(engine.knowledge_cache, KnowledgeCache)
            assert len(engine.optimization_history) == 0
    
    def test_load_default_config(self):
        """Test loading default configuration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "nonexistent_config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Should load default config
            assert engine.config['optimization_strategy'] == 'balanced'
            assert engine.config['tool_selection_method'] == 'hybrid'
            assert engine.config['cache_size'] == 10000
    
    def test_optimize_tool_selection(self):
        """Test tool selection optimization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Add some performance data
            engine.record_performance_metric("testsprite", "success_rate", 0.9)
            engine.record_performance_metric("browser_tools", "success_rate", 0.8)
            
            result = engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing", "quality_assurance"],
                constraints={"time_limit": 300},
                user_preferences={"prefer_fast": True}
            )
            
            assert isinstance(result, OptimizationResult)
            assert len(result.selected_tools) > 0
            assert 0.0 <= result.confidence_score <= 1.0
            assert result.optimization_time > 0
            assert isinstance(result.reasoning, str)
    
    def test_record_performance_metric(self):
        """Test recording performance metrics"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            engine.record_performance_metric("test_server", "response_time", 2.5)
            
            # Check metric was recorded
            performance = engine.performance_monitor.get_server_performance("test_server")
            assert performance is not None
            assert performance.response_time == 2.5
    
    def test_get_performance_summary(self):
        """Test getting performance summary"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Add some performance data
            engine.record_performance_metric("server1", "success_rate", 0.9)
            engine.record_performance_metric("server2", "success_rate", 0.7)
            
            summary = engine.get_performance_summary()
            
            assert 'servers' in summary
            assert 'alerts' in summary
            assert 'overall_health' in summary
            assert 'server1' in summary['servers']
            assert 'server2' in summary['servers']
    
    def test_optimize_knowledge_retrieval(self):
        """Test knowledge retrieval optimization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            result = engine.optimize_knowledge_retrieval(
                query="test query",
                context={"task_type": "testing"}
            )
            
            assert 'result' in result
            assert 'source' in result
            assert 'optimization_applied' in result
            assert result['optimization_applied'] is True
    
    def test_get_optimization_insights(self):
        """Test getting optimization insights"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Add some optimization history
            engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing"]
            )
            
            insights = engine.get_optimization_insights()
            
            assert 'total_optimizations' in insights
            assert 'average_confidence' in insights
            assert 'most_common_tasks' in insights
            assert 'recommendations' in insights
    
    def test_assess_complexity(self):
        """Test complexity assessment"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Test different complexity levels
            simple_reqs = ["basic", "simple"]
            medium_reqs = ["multiple", "moderate"]
            complex_reqs = ["advanced", "complex", "comprehensive"]
            
            assert engine._assess_complexity(simple_reqs) == "simple"
            assert engine._assess_complexity(medium_reqs) == "medium"
            assert engine._assess_complexity(complex_reqs) == "complex"
    
    def test_generate_cache_key(self):
        """Test cache key generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            context = ToolContext(
                task_type="testing",
                complexity="medium",
                requirements=["automated_testing"],
                constraints={},
                user_preferences={},
                historical_success={}
            )
            
            key1 = engine._generate_cache_key(context)
            key2 = engine._generate_cache_key(context)
            
            # Same context should generate same key
            assert key1 == key2
            assert len(key1) == 32  # MD5 hash length
    
    def test_export_optimization_data(self):
        """Test exporting optimization data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            output_path = Path(temp_dir) / "export.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Add some data
            engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing"]
            )
            
            engine.export_optimization_data(output_path)
            
            # Check file was created and contains data
            assert output_path.exists()
            
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            assert 'config' in data
            assert 'optimization_history' in data
            assert 'performance_summary' in data
            assert 'insights' in data


class TestOptimizationResult:
    """Test OptimizationResult dataclass"""
    
    def test_optimization_result_creation(self):
        """Test creating OptimizationResult instance"""
        result = OptimizationResult(
            selected_tools=["testsprite", "browser_tools"],
            confidence_score=0.85,
            reasoning="Test reasoning",
            performance_prediction={"testsprite": {"predicted_success_rate": 0.9}},
            alternatives=[{"type": "performance_focused", "tools": ["testsprite"]}],
            optimization_time=0.1
        )
        
        assert result.selected_tools == ["testsprite", "browser_tools"]
        assert result.confidence_score == 0.85
        assert result.reasoning == "Test reasoning"
        assert result.performance_prediction == {"testsprite": {"predicted_success_rate": 0.9}}
        assert len(result.alternatives) == 1
        assert result.optimization_time == 0.1
    
    def test_optimization_result_to_dict(self):
        """Test converting OptimizationResult to dictionary"""
        result = OptimizationResult(
            selected_tools=["testsprite"],
            confidence_score=0.8,
            reasoning="Test",
            performance_prediction={},
            alternatives=[],
            optimization_time=0.05
        )
        
        result_dict = result.to_dict()
        
        assert result_dict['selected_tools'] == ["testsprite"]
        assert result_dict['confidence_score'] == 0.8
        assert result_dict['reasoning'] == "Test"
        assert result_dict['performance_prediction'] == {}
        assert result_dict['alternatives'] == []
        assert result_dict['optimization_time'] == 0.05


# Integration tests
class TestOptimizationEngineIntegration:
    """Integration tests for the optimization engine"""
    
    def test_full_optimization_workflow(self):
        """Test complete optimization workflow"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Record performance metrics for multiple servers
            servers = ["testsprite", "browser_tools", "context7", "byterover"]
            for server in servers:
                engine.record_performance_metric(server, "success_rate", 0.9)
                engine.record_performance_metric(server, "response_time", 2.0)
                engine.record_performance_metric(server, "error_rate", 0.1)
                engine.record_performance_metric(server, "resource_usage", 0.5)
            
            # Perform optimization
            result = engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing", "quality_assurance"],
                constraints={"time_limit": 300},
                user_preferences={"prefer_fast": True}
            )
            
            # Verify result
            assert isinstance(result, OptimizationResult)
            assert len(result.selected_tools) > 0
            assert result.confidence_score > 0
            
            # Test knowledge optimization
            knowledge_result = engine.optimize_knowledge_retrieval(
                query="test query",
                context={"task_type": "testing"}
            )
            
            assert knowledge_result['optimization_applied'] is True
            
            # Test performance summary
            summary = engine.get_performance_summary()
            assert len(summary['servers']) == len(servers)
            
            # Test insights
            insights = engine.get_optimization_insights()
            assert insights['total_optimizations'] > 0
    
    def test_caching_behavior(self):
        """Test caching behavior in optimization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # First optimization
            result1 = engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing"]
            )
            
            # Second optimization with same parameters
            result2 = engine.optimize_tool_selection(
                task_type="testing",
                requirements=["automated_testing"]
            )
            
            # Results should be similar (cached or consistent)
            assert result1.selected_tools == result2.selected_tools
            assert abs(result1.confidence_score - result2.confidence_score) < 0.1
    
    def test_performance_monitoring_integration(self):
        """Test performance monitoring integration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            engine = MCPOptimizationEngine(config_path=config_path)
            
            # Record metrics over time
            for i in range(10):
                engine.record_performance_metric("test_server", "response_time", 1.0 + i * 0.1)
                engine.record_performance_metric("test_server", "success_rate", 0.95 - i * 0.01)
            
            # Get performance summary
            summary = engine.get_performance_summary()
            
            # Check that metrics were recorded
            assert "test_server" in summary['servers']
            server_data = summary['servers']["test_server"]
            assert "metrics" in server_data
            assert "trends" in server_data
            
            # Check trends
            trends = server_data['trends']
            assert "response_time" in trends
            assert "success_rate" in trends


if __name__ == "__main__":
    pytest.main([__file__])
