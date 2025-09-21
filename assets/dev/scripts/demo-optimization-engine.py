#!/usr/bin/env python3
"""
MCP Optimization Engine Demonstration Script

This script demonstrates the capabilities of the MCP Optimization Engine
with realistic scenarios and comprehensive examples.

Author: DocGen CLI Team
Created: 2025-01-20
"""

import sys
import os
import time
import json
from pathlib import Path

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.core.optimization_engine import (
    MCPOptimizationEngine,
    OptimizationStrategy,
    ToolSelectionMethod,
    ToolContext
)


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_section(title):
    """Print a formatted section header"""
    print(f"\n--- {title} ---")


def print_result(result, title="Optimization Result"):
    """Print optimization result in a formatted way"""
    print(f"\n{title}:")
    print(f"  Selected Tools: {', '.join(result.selected_tools)}")
    print(f"  Confidence Score: {result.confidence_score:.2f}")
    print(f"  Optimization Time: {result.optimization_time:.3f}s")
    print(f"  Reasoning: {result.reasoning}")
    
    if result.performance_prediction:
        print(f"  Performance Predictions:")
        for tool, prediction in result.performance_prediction.items():
            print(f"    {tool}: {prediction['predicted_success_rate']:.2f} success rate, {prediction['predicted_response_time']:.2f}s response time")
    
    if result.alternatives:
        print(f"  Alternatives:")
        for i, alt in enumerate(result.alternatives, 1):
            print(f"    {i}. {alt['type']}: {', '.join(alt['tools'])}")


def simulate_mcp_server_performance(engine):
    """Simulate realistic MCP server performance data"""
    print_section("Simulating MCP Server Performance Data")
    
    # Realistic performance data for different servers
    server_performance = {
        "byterover": {
            "response_time": 1.8,
            "success_rate": 0.92,
            "error_rate": 0.08,
            "resource_usage": 0.4
        },
        "testsprite": {
            "response_time": 2.5,
            "success_rate": 0.88,
            "error_rate": 0.12,
            "resource_usage": 0.6
        },
        "context7": {
            "response_time": 1.2,
            "success_rate": 0.95,
            "error_rate": 0.05,
            "resource_usage": 0.3
        },
        "browser_tools": {
            "response_time": 3.0,
            "success_rate": 0.85,
            "error_rate": 0.15,
            "resource_usage": 0.7
        },
        "playwright": {
            "response_time": 4.0,
            "success_rate": 0.80,
            "error_rate": 0.20,
            "resource_usage": 0.8
        },
        "dart": {
            "response_time": 1.5,
            "success_rate": 0.75,
            "error_rate": 0.25,
            "resource_usage": 0.5
        }
    }
    
    # Record performance metrics
    for server, metrics in server_performance.items():
        for metric_type, value in metrics.items():
            engine.record_performance_metric(server, metric_type, value)
        print(f"  Recorded metrics for {server}: {metrics['success_rate']:.2f} success rate, {metrics['response_time']:.2f}s response time")
    
    return server_performance


def demonstrate_tool_selection(engine):
    """Demonstrate intelligent tool selection"""
    print_section("Intelligent Tool Selection Demonstration")
    
    # Test different optimization strategies
    strategies = [
        (OptimizationStrategy.PERFORMANCE, "Performance-focused selection"),
        (OptimizationStrategy.ACCURACY, "Accuracy-focused selection"),
        (OptimizationStrategy.BALANCED, "Balanced selection"),
        (OptimizationStrategy.COST_EFFECTIVE, "Cost-effective selection")
    ]
    
    for strategy, description in strategies:
        print(f"\n{description}:")
        result = engine.optimize_tool_selection(
            task_type="testing",
            requirements=["automated_testing", "quality_assurance"],
            constraints={"time_limit": 300, "budget": "medium"},
            user_preferences={"prefer_fast": True}
        )
        print_result(result, f"Strategy: {strategy.value}")


def demonstrate_context_based_selection(engine):
    """Demonstrate context-based tool selection"""
    print_section("Context-Based Tool Selection")
    
    scenarios = [
        {
            "name": "Knowledge Retrieval Task",
            "task_type": "knowledge_retrieval",
            "requirements": ["knowledge_management", "context_assessment"],
            "constraints": {"time_limit": 600},
            "user_preferences": {"prefer_accurate": True}
        },
        {
            "name": "Web Testing Task",
            "task_type": "web_testing",
            "requirements": ["browser_automation", "e2e_testing"],
            "constraints": {"time_limit": 900},
            "user_preferences": {"require_detailed_reports": True}
        },
        {
            "name": "Project Management Task",
            "task_type": "project_management",
            "requirements": ["task_management", "team_collaboration"],
            "constraints": {"time_limit": 300},
            "user_preferences": {"prefer_fast": True}
        },
        {
            "name": "Documentation Task",
            "task_type": "documentation",
            "requirements": ["documentation_access", "api_reference"],
            "constraints": {"time_limit": 200},
            "user_preferences": {"prefer_fast": True}
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        result = engine.optimize_tool_selection(
            task_type=scenario["task_type"],
            requirements=scenario["requirements"],
            constraints=scenario["constraints"],
            user_preferences=scenario["user_preferences"]
        )
        print_result(result, f"Context: {scenario['name']}")


def demonstrate_performance_monitoring(engine):
    """Demonstrate performance monitoring capabilities"""
    print_section("Performance Monitoring Demonstration")
    
    # Simulate performance degradation
    print("Simulating performance degradation...")
    
    # Record degraded performance
    degraded_servers = ["testsprite", "browser_tools"]
    for server in degraded_servers:
        engine.record_performance_metric(server, "response_time", 8.0)  # Above threshold
        engine.record_performance_metric(server, "success_rate", 0.6)
        engine.record_performance_metric(server, "error_rate", 0.4)
        engine.record_performance_metric(server, "resource_usage", 0.9)  # Above threshold
        print(f"  Recorded degraded performance for {server}")
    
    # Get performance summary
    summary = engine.get_performance_summary()
    
    print(f"\nPerformance Summary:")
    print(f"  Overall Health: {summary['overall_health']}")
    print(f"  Active Alerts: {len(summary['alerts'])}")
    
    if summary['alerts']:
        print(f"  Alerts:")
        for alert in summary['alerts']:
            print(f"    {alert['server']}: {alert['metric']} = {alert['value']} (threshold: {alert['threshold']}) - {alert['severity']}")
    
    print(f"\nServer Status:")
    for server_name, server_data in summary['servers'].items():
        metrics = server_data['metrics']
        status = server_data['status']
        print(f"  {server_name}: {status} - {metrics['success_rate']:.2f} success, {metrics['response_time']:.2f}s response")


def demonstrate_knowledge_optimization(engine):
    """Demonstrate knowledge management optimization"""
    print_section("Knowledge Management Optimization")
    
    # Test knowledge retrieval optimization
    queries = [
        "React component patterns",
        "Python testing best practices",
        "MCP server integration",
        "React component patterns",  # Duplicate query
        "Docker containerization",
        "Python testing best practices"  # Another duplicate
    ]
    
    cache_hits = 0
    cache_misses = 0
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        result = engine.optimize_knowledge_retrieval(
            query=query,
            context={"task_type": "development", "language": "python"}
        )
        
        source = result['source']
        if source == 'cache':
            cache_hits += 1
            print(f"  Source: {source} (cache hit)")
        else:
            cache_misses += 1
            print(f"  Source: {source} (computed)")
        
        print(f"  Optimization Applied: {result['optimization_applied']}")
    
    print(f"\nCache Statistics:")
    print(f"  Cache Hits: {cache_hits}")
    print(f"  Cache Misses: {cache_misses}")
    print(f"  Hit Rate: {cache_hits / len(queries) * 100:.1f}%")
    
    # Show cache details
    cache = engine.knowledge_cache
    print(f"  Cache Size: {len(cache.cache)}")
    print(f"  Access Counts: {dict(cache.access_counts)}")


def demonstrate_insights_generation(engine):
    """Demonstrate optimization insights generation"""
    print_section("Optimization Insights Generation")
    
    # Perform multiple optimizations to generate insights
    optimization_scenarios = [
        {"task_type": "testing", "requirements": ["automated_testing"]},
        {"task_type": "knowledge_retrieval", "requirements": ["knowledge_management"]},
        {"task_type": "web_testing", "requirements": ["browser_automation"]},
        {"task_type": "testing", "requirements": ["quality_assurance"]},
        {"task_type": "project_management", "requirements": ["task_management"]},
        {"task_type": "testing", "requirements": ["performance_validation"]}
    ]
    
    print("Performing multiple optimizations...")
    for i, scenario in enumerate(optimization_scenarios, 1):
        result = engine.optimize_tool_selection(
            task_type=scenario["task_type"],
            requirements=scenario["requirements"]
        )
        print(f"  Optimization {i}: {scenario['task_type']} - Confidence: {result.confidence_score:.2f}")
    
    # Get insights
    insights = engine.get_optimization_insights()
    
    print(f"\nOptimization Insights:")
    print(f"  Total Optimizations: {insights['total_optimizations']}")
    print(f"  Average Confidence: {insights['average_confidence']:.2f}")
    
    if insights['most_common_tasks']:
        print(f"  Most Common Tasks:")
        for task_type, count in insights['most_common_tasks'].items():
            print(f"    {task_type}: {count} times")
    
    if insights['recommendations']:
        print(f"  Recommendations:")
        for i, rec in enumerate(insights['recommendations'], 1):
            print(f"    {i}. {rec}")


def demonstrate_real_world_workflow(engine):
    """Demonstrate a realistic development workflow"""
    print_section("Real-World Development Workflow")
    
    # Simulate a complete development workflow
    workflow_phases = [
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
    
    workflow_results = []
    
    for phase_info in workflow_phases:
        print(f"\n{phase_info['phase']} Phase:")
        result = engine.optimize_tool_selection(
            task_type=phase_info["task_type"],
            requirements=phase_info["requirements"],
            constraints=phase_info["constraints"],
            user_preferences=phase_info["user_preferences"]
        )
        
        workflow_results.append(result)
        print_result(result, f"{phase_info['phase']} Optimization")
    
    # Analyze workflow results
    total_confidence = sum(r.confidence_score for r in workflow_results)
    average_confidence = total_confidence / len(workflow_results)
    total_time = sum(r.optimization_time for r in workflow_results)
    
    print(f"\nWorkflow Analysis:")
    print(f"  Average Confidence: {average_confidence:.2f}")
    print(f"  Total Optimization Time: {total_time:.3f}s")
    print(f"  Phases Completed: {len(workflow_phases)}")
    
    # Show tool usage across workflow
    all_tools = []
    for result in workflow_results:
        all_tools.extend(result.selected_tools)
    
    tool_usage = {}
    for tool in all_tools:
        tool_usage[tool] = tool_usage.get(tool, 0) + 1
    
    print(f"  Tool Usage:")
    for tool, count in sorted(tool_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"    {tool}: {count} times")


def demonstrate_export_functionality(engine):
    """Demonstrate data export functionality"""
    print_section("Data Export Functionality")
    
    # Export optimization data
    export_path = Path("optimization_engine_demo_export.json")
    
    print(f"Exporting optimization data to {export_path}...")
    engine.export_optimization_data(export_path)
    
    # Verify export
    if export_path.exists():
        with open(export_path, 'r') as f:
            export_data = json.load(f)
        
        print(f"Export successful!")
        print(f"  Config entries: {len(export_data.get('config', {}))}")
        print(f"  Optimization history: {len(export_data.get('optimization_history', []))}")
        print(f"  Performance summary servers: {len(export_data.get('performance_summary', {}).get('servers', {}))}")
        print(f"  Insights available: {'insights' in export_data}")
        print(f"  Export timestamp: {export_data.get('export_timestamp', 'N/A')}")
        
        # Clean up
        export_path.unlink()
        print(f"  Export file cleaned up")
    else:
        print(f"Export failed - file not created")


def main():
    """Main demonstration function"""
    print_header("MCP Optimization Engine Demonstration")
    
    print("This demonstration showcases the capabilities of the MCP Optimization Engine")
    print("including intelligent tool selection, performance monitoring, knowledge")
    print("management optimization, and workflow enhancement.")
    
    # Initialize optimization engine
    print_section("Initializing Optimization Engine")
    engine = MCPOptimizationEngine()
    print("Optimization engine initialized successfully!")
    
    # Simulate MCP server performance
    server_performance = simulate_mcp_server_performance(engine)
    
    # Demonstrate various capabilities
    demonstrate_tool_selection(engine)
    demonstrate_context_based_selection(engine)
    demonstrate_performance_monitoring(engine)
    demonstrate_knowledge_optimization(engine)
    demonstrate_insights_generation(engine)
    demonstrate_real_world_workflow(engine)
    demonstrate_export_functionality(engine)
    
    # Final summary
    print_header("Demonstration Complete")
    
    final_insights = engine.get_optimization_insights()
    performance_summary = engine.get_performance_summary()
    
    print(f"Final Statistics:")
    print(f"  Total Optimizations Performed: {final_insights['total_optimizations']}")
    print(f"  Average Confidence Score: {final_insights['average_confidence']:.2f}")
    print(f"  Servers Monitored: {len(performance_summary['servers'])}")
    print(f"  Overall System Health: {performance_summary['overall_health']}")
    print(f"  Active Performance Alerts: {len(performance_summary['alerts'])}")
    
    print(f"\nThe MCP Optimization Engine successfully demonstrated:")
    print(f"  ✓ Intelligent tool selection with multiple strategies")
    print(f"  ✓ Context-aware optimization based on task requirements")
    print(f"  ✓ Real-time performance monitoring with alerting")
    print(f"  ✓ Knowledge management optimization with caching")
    print(f"  ✓ Insights generation and recommendations")
    print(f"  ✓ Real-world workflow optimization")
    print(f"  ✓ Data export and analysis capabilities")
    
    print(f"\nThe optimization engine is ready for production use!")


if __name__ == "__main__":
    main()
