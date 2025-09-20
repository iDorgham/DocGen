#!/usr/bin/env python3
"""
MCP Orchestrator for DocGen CLI
Provides parallel execution and optimization for MCP server integration.

This module orchestrates multiple MCP servers for optimal performance,
providing intelligent selection, parallel execution, and performance monitoring.

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import asyncio
import time
import json
import logging
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.logging import RichHandler
except ImportError:
    print("Warning: Rich library not available. Install with: pip install rich")
    Console = None

# Import MCP Integration Core
try:
    from mcp_integration import MCPIntegrationCore, MCPIntegrationResult
except ImportError:
    # Add current directory to path for local imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from mcp_integration import MCPIntegrationCore, MCPIntegrationResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler()] if Console else [logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@dataclass
class MCPCall:
    """Represents an MCP server call."""
    server: str
    function: str
    args: List[Any] = None
    kwargs: Dict[str, Any] = None
    priority: int = 1
    timeout: int = 30
    retry_count: int = 0
    max_retries: int = 3

    def __post_init__(self):
        if self.args is None:
            self.args = []
        if self.kwargs is None:
            self.kwargs = {}

@dataclass
class OrchestrationResult:
    """Result of MCP orchestration operation."""
    calls_executed: int
    calls_successful: int
    calls_failed: int
    total_duration: float
    parallel_efficiency: float
    results: List[MCPIntegrationResult]
    performance_metrics: Dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class MCPOrchestrator:
    """
    MCP Orchestrator for parallel execution and optimization.
    
    Provides intelligent orchestration of MCP server calls with:
    - Parallel execution for optimal performance
    - Intelligent server selection
    - Performance monitoring and optimization
    - Error handling and retry mechanisms
    - Caching and optimization strategies
    """
    
    def __init__(self, mcp_core: MCPIntegrationCore = None, max_workers: int = 10):
        """
        Initialize MCP Orchestrator.
        
        Args:
            mcp_core: MCP Integration Core instance
            max_workers: Maximum number of parallel workers
        """
        self.console = Console() if Console else None
        self.mcp_core = mcp_core or MCPIntegrationCore()
        self.max_workers = max_workers
        self.execution_history = []
        self.performance_cache = {}
        self.optimization_rules = {}
        
        # Initialize optimization rules
        self._initialize_optimization_rules()
        
        logger.info("MCP Orchestrator initialized")
    
    def _initialize_optimization_rules(self):
        """Initialize optimization rules for MCP server calls."""
        self.optimization_rules = {
            'parallel_execution': {
                'enabled': True,
                'max_concurrent': self.max_workers,
                'timeout_threshold': 5.0  # Calls taking longer than 5s should be parallel
            },
            'caching': {
                'enabled': True,
                'cache_duration': 1800,  # 30 minutes
                'cache_size_limit': 1000
            },
            'retry_strategy': {
                'enabled': True,
                'max_retries': 3,
                'retry_delay': 1.0,
                'exponential_backoff': True
            },
            'performance_monitoring': {
                'enabled': True,
                'metrics_collection': True,
                'optimization_suggestions': True
            }
        }
    
    def _should_parallelize(self, calls: List[MCPCall]) -> bool:
        """Determine if calls should be executed in parallel."""
        if not self.optimization_rules['parallel_execution']['enabled']:
            return False
        
        if len(calls) < 2:
            return False
        
        # Check if any call is expected to take longer than threshold
        for call in calls:
            estimated_duration = self._estimate_call_duration(call)
            if estimated_duration > self.optimization_rules['parallel_execution']['timeout_threshold']:
                return True
        
        return True
    
    def _estimate_call_duration(self, call: MCPCall) -> float:
        """Estimate duration of an MCP call based on historical data."""
        cache_key = f"{call.server}.{call.function}"
        
        if cache_key in self.performance_cache:
            return self.performance_cache[cache_key]['average_duration']
        
        # Default estimates based on server type
        default_estimates = {
            'byterover': 2.0,
            'context7': 1.5,
            'testsprite': 5.0,
            'browser_tools': 3.0,
            'playwright': 4.0,
            'dart': 1.0
        }
        
        return default_estimates.get(call.server, 2.0)
    
    def _update_performance_cache(self, call: MCPCall, duration: float):
        """Update performance cache with call duration."""
        cache_key = f"{call.server}.{call.function}"
        
        if cache_key not in self.performance_cache:
            self.performance_cache[cache_key] = {
                'call_count': 0,
                'total_duration': 0.0,
                'average_duration': 0.0,
                'min_duration': float('inf'),
                'max_duration': 0.0
            }
        
        cache_entry = self.performance_cache[cache_key]
        cache_entry['call_count'] += 1
        cache_entry['total_duration'] += duration
        cache_entry['average_duration'] = cache_entry['total_duration'] / cache_entry['call_count']
        cache_entry['min_duration'] = min(cache_entry['min_duration'], duration)
        cache_entry['max_duration'] = max(cache_entry['max_duration'], duration)
    
    def _execute_single_call(self, call: MCPCall) -> MCPIntegrationResult:
        """Execute a single MCP call with retry logic."""
        start_time = time.time()
        
        for attempt in range(call.max_retries + 1):
            try:
                result = self.mcp_core.execute_mcp_call(
                    call.server,
                    call.function,
                    *call.args,
                    **call.kwargs
                )
                
                # Update performance cache
                duration = time.time() - start_time
                self._update_performance_cache(call, duration)
                
                return result
                
            except Exception as e:
                if attempt < call.max_retries:
                    delay = self.optimization_rules['retry_strategy']['retry_delay']
                    if self.optimization_rules['retry_strategy']['exponential_backoff']:
                        delay *= (2 ** attempt)
                    
                    logger.warning(f"Call failed, retrying in {delay}s: {call.server}.{call.function}")
                    time.sleep(delay)
                    continue
                else:
                    duration = time.time() - start_time
                    error_msg = f"Call failed after {call.max_retries} retries: {str(e)}"
                    logger.error(error_msg)
                    
                    return MCPIntegrationResult(
                        server=call.server,
                        success=False,
                        error=error_msg,
                        duration=duration
                    )
    
    def _execute_parallel_calls(self, calls: List[MCPCall]) -> List[MCPIntegrationResult]:
        """Execute multiple MCP calls in parallel."""
        logger.info(f"Executing {len(calls)} MCP calls in parallel with {self.max_workers} workers")
        
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all calls
            future_to_call = {
                executor.submit(self._execute_single_call, call): call 
                for call in calls
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_call):
                call = future_to_call[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.debug(f"Completed call: {call.server}.{call.function}")
                except Exception as e:
                    logger.error(f"Exception in parallel execution: {e}")
                    results.append(MCPIntegrationResult(
                        server=call.server,
                        success=False,
                        error=str(e),
                        duration=0.0
                    ))
        
        total_duration = time.time() - start_time
        
        # Calculate parallel efficiency
        sequential_estimate = sum(self._estimate_call_duration(call) for call in calls)
        parallel_efficiency = sequential_estimate / total_duration if total_duration > 0 else 1.0
        
        logger.info(f"Parallel execution completed in {total_duration:.2f}s with {parallel_efficiency:.2f}x efficiency")
        
        return results, total_duration, parallel_efficiency
    
    def _execute_sequential_calls(self, calls: List[MCPCall]) -> List[MCPIntegrationResult]:
        """Execute multiple MCP calls sequentially."""
        logger.info(f"Executing {len(calls)} MCP calls sequentially")
        
        results = []
        start_time = time.time()
        
        for call in calls:
            result = self._execute_single_call(call)
            results.append(result)
            logger.debug(f"Completed call: {call.server}.{call.function}")
        
        total_duration = time.time() - start_time
        parallel_efficiency = 1.0  # Sequential execution has no parallel efficiency
        
        logger.info(f"Sequential execution completed in {total_duration:.2f}s")
        
        return results, total_duration, parallel_efficiency
    
    def orchestrate_calls(self, calls: List[Union[MCPCall, Dict[str, Any]]]) -> OrchestrationResult:
        """
        Orchestrate multiple MCP calls with intelligent execution strategy.
        
        Args:
            calls: List of MCPCall objects or dictionaries representing calls
            
        Returns:
            OrchestrationResult with execution results and metrics
        """
        # Convert dictionaries to MCPCall objects
        mcp_calls = []
        for call in calls:
            if isinstance(call, dict):
                mcp_calls.append(MCPCall(**call))
            else:
                mcp_calls.append(call)
        
        logger.info(f"Orchestrating {len(mcp_calls)} MCP calls")
        
        start_time = time.time()
        
        # Determine execution strategy
        if self._should_parallelize(mcp_calls):
            results, total_duration, parallel_efficiency = self._execute_parallel_calls(mcp_calls)
        else:
            results, total_duration, parallel_efficiency = self._execute_sequential_calls(mcp_calls)
        
        # Calculate metrics
        successful_calls = sum(1 for r in results if r.success)
        failed_calls = len(results) - successful_calls
        
        # Generate performance metrics
        performance_metrics = {
            'total_calls': len(mcp_calls),
            'successful_calls': successful_calls,
            'failed_calls': failed_calls,
            'success_rate': successful_calls / len(mcp_calls) if mcp_calls else 0,
            'total_duration': total_duration,
            'parallel_efficiency': parallel_efficiency,
            'average_call_duration': sum(r.duration for r in results) / len(results) if results else 0,
            'execution_strategy': 'parallel' if self._should_parallelize(mcp_calls) else 'sequential',
            'optimization_rules': self.optimization_rules
        }
        
        # Create orchestration result
        orchestration_result = OrchestrationResult(
            calls_executed=len(mcp_calls),
            calls_successful=successful_calls,
            calls_failed=failed_calls,
            total_duration=total_duration,
            parallel_efficiency=parallel_efficiency,
            results=results,
            performance_metrics=performance_metrics
        )
        
        # Store in execution history
        self.execution_history.append(orchestration_result)
        
        logger.info(f"Orchestration completed: {successful_calls}/{len(mcp_calls)} successful")
        
        return orchestration_result
    
    def get_optimization_suggestions(self) -> List[str]:
        """Get optimization suggestions based on execution history."""
        suggestions = []
        
        if not self.execution_history:
            return ["No execution history available for optimization suggestions"]
        
        # Analyze recent executions
        recent_executions = self.execution_history[-10:]  # Last 10 executions
        
        # Check parallel efficiency
        avg_parallel_efficiency = sum(e.parallel_efficiency for e in recent_executions) / len(recent_executions)
        if avg_parallel_efficiency < 1.5:
            suggestions.append("Consider increasing max_workers for better parallel efficiency")
        
        # Check success rates
        avg_success_rate = sum(e.calls_successful / e.calls_executed for e in recent_executions) / len(recent_executions)
        if avg_success_rate < 0.9:
            suggestions.append("Success rate is below 90%, consider reviewing error handling")
        
        # Check call durations
        avg_duration = sum(e.total_duration for e in recent_executions) / len(recent_executions)
        if avg_duration > 10.0:
            suggestions.append("Average execution time is high, consider optimizing slow calls")
        
        # Check cache utilization
        if len(self.performance_cache) > self.optimization_rules['caching']['cache_size_limit']:
            suggestions.append("Performance cache is large, consider clearing old entries")
        
        return suggestions
    
    def display_orchestration_status(self):
        """Display orchestration status and metrics."""
        if not self.console:
            # Fallback to simple text output
            print("MCP Orchestrator Status:")
            print(f"  Max Workers: {self.max_workers}")
            print(f"  Execution History: {len(self.execution_history)} executions")
            print(f"  Performance Cache: {len(self.performance_cache)} entries")
            return
        
        # Create status table
        table = Table(title="MCP Orchestrator Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Max Workers", str(self.max_workers))
        table.add_row("Execution History", str(len(self.execution_history)))
        table.add_row("Performance Cache", str(len(self.performance_cache)))
        
        if self.execution_history:
            recent = self.execution_history[-1]
            table.add_row("Last Execution Calls", str(recent.calls_executed))
            table.add_row("Last Execution Success Rate", f"{recent.calls_successful/recent.calls_executed:.2%}")
            table.add_row("Last Execution Duration", f"{recent.total_duration:.2f}s")
            table.add_row("Last Parallel Efficiency", f"{recent.parallel_efficiency:.2f}x")
        
        self.console.print(table)
        
        # Display optimization suggestions
        suggestions = self.get_optimization_suggestions()
        if suggestions:
            suggestions_panel = Panel(
                "\n".join(f"• {suggestion}" for suggestion in suggestions),
                title="Optimization Suggestions",
                border_style="yellow"
            )
            self.console.print(suggestions_panel)
    
    def export_orchestration_report(self, output_path: str = None):
        """Export orchestration report to JSON file."""
        if not output_path:
            output_path = os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'reports', 'mcp', 'mcp_orchestration_report.json'
            )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Prepare report data
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'orchestrator_config': {
                'max_workers': self.max_workers,
                'optimization_rules': self.optimization_rules
            },
            'execution_history': [asdict(execution) for execution in self.execution_history],
            'performance_cache': self.performance_cache,
            'optimization_suggestions': self.get_optimization_suggestions()
        }
        
        # Convert datetime objects to strings
        for execution in report_data['execution_history']:
            if execution['timestamp']:
                execution['timestamp'] = execution['timestamp'].isoformat()
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Orchestration report exported to: {output_path}")
        return output_path

def main():
    """Main function for testing MCP Orchestrator."""
    try:
        # Initialize MCP Orchestrator
        orchestrator = MCPOrchestrator()
        
        # Display initial status
        orchestrator.display_orchestration_status()
        
        # Test orchestration with sample calls
        print("\n" + "="*50)
        print("Testing MCP Orchestration")
        print("="*50)
        
        # Create sample calls
        sample_calls = [
            MCPCall(
                server='byterover',
                function='retrieve_knowledge',
                args=['DocGen CLI orchestration test'],
                priority=1
            ),
            MCPCall(
                server='context7',
                function='resolve_library_id',
                args=['click'],
                priority=2
            ),
            MCPCall(
                server='testsprite',
                function='bootstrap_tests',
                args=[3000, 'backend', '/path/to/project', 'codebase'],
                priority=1
            ),
            MCPCall(
                server='browser_tools',
                function='runAccessibilityAudit',
                priority=3
            ),
            MCPCall(
                server='dart',
                function='create_task',
                args=[{
                    'title': 'Test orchestration',
                    'description': 'Testing MCP orchestration functionality',
                    'priority': 'medium'
                }],
                priority=2
            )
        ]
        
        # Orchestrate calls
        result = orchestrator.orchestrate_calls(sample_calls)
        
        # Display results
        if orchestrator.console:
            result_panel = Panel(
                f"Calls Executed: {result.calls_executed}\n"
                f"Calls Successful: {result.calls_successful}\n"
                f"Calls Failed: {result.calls_failed}\n"
                f"Total Duration: {result.total_duration:.2f}s\n"
                f"Parallel Efficiency: {result.parallel_efficiency:.2f}x",
                title="Orchestration Results",
                border_style="green"
            )
            orchestrator.console.print(result_panel)
        else:
            print(f"\nOrchestration Results:")
            print(f"  Calls Executed: {result.calls_executed}")
            print(f"  Calls Successful: {result.calls_successful}")
            print(f"  Calls Failed: {result.calls_failed}")
            print(f"  Total Duration: {result.total_duration:.2f}s")
            print(f"  Parallel Efficiency: {result.parallel_efficiency:.2f}x")
        
        # Display updated status
        print("\n" + "="*50)
        print("Updated Orchestration Status")
        print("="*50)
        orchestrator.display_orchestration_status()
        
        # Export report
        report_path = orchestrator.export_orchestration_report()
        print(f"\nOrchestration report exported to: {report_path}")
        
    except Exception as e:
        logger.error(f"Error in MCP Orchestrator test: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
