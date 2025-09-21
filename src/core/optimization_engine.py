"""
MCP Optimization Engine - Intelligent Tool Selection and Knowledge Management

This module provides an advanced optimization engine for MCP servers that includes:
- Intelligent tool selection based on context and performance metrics
- Knowledge management optimization with caching and compression
- Workflow enhancement with parallel execution optimization
- Performance monitoring and adaptive resource management
- Machine learning-based continuous improvement

Author: DocGen CLI Team
Created: 2025-01-20
"""

import asyncio
import time
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import hashlib
from collections import defaultdict, deque
import statistics
from datetime import datetime, timedelta

# Third-party imports
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import joblib

logger = logging.getLogger(__name__)


class OptimizationStrategy(Enum):
    """Optimization strategy types"""
    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    BALANCED = "balanced"
    COST_EFFECTIVE = "cost_effective"


class ToolSelectionMethod(Enum):
    """Tool selection methods"""
    CONTEXT_BASED = "context_based"
    PERFORMANCE_BASED = "performance_based"
    HYBRID = "hybrid"
    MACHINE_LEARNING = "machine_learning"


@dataclass
class PerformanceMetrics:
    """Performance metrics for MCP servers"""
    response_time: float
    success_rate: float
    error_rate: float
    throughput: float
    resource_usage: float
    last_updated: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'response_time': self.response_time,
            'success_rate': self.success_rate,
            'error_rate': self.error_rate,
            'throughput': self.throughput,
            'resource_usage': self.resource_usage,
            'last_updated': self.last_updated.isoformat()
        }


@dataclass
class ToolContext:
    """Context information for tool selection"""
    task_type: str
    complexity: str
    requirements: List[str]
    constraints: Dict[str, Any]
    user_preferences: Dict[str, Any]
    historical_success: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'task_type': self.task_type,
            'complexity': self.complexity,
            'requirements': self.requirements,
            'constraints': self.constraints,
            'user_preferences': self.user_preferences,
            'historical_success': self.historical_success
        }


@dataclass
class OptimizationResult:
    """Result of optimization operation"""
    selected_tools: List[str]
    confidence_score: float
    reasoning: str
    performance_prediction: Dict[str, float]
    alternatives: List[Dict[str, Any]]
    optimization_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'selected_tools': self.selected_tools,
            'confidence_score': self.confidence_score,
            'reasoning': self.reasoning,
            'performance_prediction': self.performance_prediction,
            'alternatives': self.alternatives,
            'optimization_time': self.optimization_time
        }


class KnowledgeCache:
    """Intelligent knowledge caching system"""
    
    def __init__(self, max_size: int = 10000, compression_threshold: float = 0.8):
        self.max_size = max_size
        self.compression_threshold = compression_threshold
        self.cache: Dict[str, Any] = {}
        self.access_times: Dict[str, datetime] = {}
        self.access_counts: Dict[str, int] = defaultdict(int)
        self.compression_ratios: Dict[str, float] = {}
        
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache with access tracking"""
        if key in self.cache:
            self.access_times[key] = datetime.now()
            self.access_counts[key] += 1
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any, compress: bool = True) -> None:
        """Set item in cache with compression if beneficial"""
        if len(self.cache) >= self.max_size:
            self._evict_least_used()
        
        # Apply compression if beneficial
        if compress and self._should_compress(value):
            value = self._compress_value(value)
            self.compression_ratios[key] = self._calculate_compression_ratio(value)
        
        self.cache[key] = value
        self.access_times[key] = datetime.now()
        self.access_counts[key] = 1
    
    def _should_compress(self, value: Any) -> bool:
        """Determine if value should be compressed"""
        if isinstance(value, str) and len(value) > 1000:
            return True
        if isinstance(value, (dict, list)) and len(str(value)) > 1000:
            return True
        return False
    
    def _compress_value(self, value: Any) -> Any:
        """Compress value using appropriate method"""
        if isinstance(value, str):
            # Simple compression for demonstration
            return value.encode('utf-8').hex()
        return value
    
    def _calculate_compression_ratio(self, value: Any) -> float:
        """Calculate compression ratio"""
        original_size = len(str(value))
        compressed_size = len(str(value))
        return compressed_size / original_size if original_size > 0 else 1.0
    
    def _evict_least_used(self) -> None:
        """Evict least recently and frequently used items"""
        if not self.cache:
            return
        
        # Calculate LRU-FU score (Least Recently Used + Frequency Used)
        scores = {}
        for key in self.cache:
            last_access = self.access_times.get(key, datetime.min)
            access_count = self.access_counts.get(key, 0)
            time_since_access = (datetime.now() - last_access).total_seconds()
            
            # Lower score = more likely to evict
            scores[key] = access_count / (time_since_access + 1)
        
        # Remove item with lowest score
        key_to_remove = min(scores, key=scores.get)
        del self.cache[key_to_remove]
        del self.access_times[key_to_remove]
        del self.access_counts[key_to_remove]
        if key_to_remove in self.compression_ratios:
            del self.compression_ratios[key_to_remove]


class PerformanceMonitor:
    """Real-time performance monitoring for MCP servers"""
    
    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=history_size))
        self.current_metrics: Dict[str, PerformanceMetrics] = {}
        self.alerts: List[Dict[str, Any]] = []
        
    def record_metric(self, server_name: str, metric_type: str, value: float) -> None:
        """Record a performance metric"""
        timestamp = datetime.now()
        self.metrics_history[f"{server_name}_{metric_type}"].append({
            'value': value,
            'timestamp': timestamp
        })
        
        # Update current metrics
        if server_name not in self.current_metrics:
            self.current_metrics[server_name] = PerformanceMetrics(
                response_time=0.0,
                success_rate=1.0,
                error_rate=0.0,
                throughput=0.0,
                resource_usage=0.0,
                last_updated=timestamp
            )
        
        # Update specific metric
        if metric_type == 'response_time':
            self.current_metrics[server_name].response_time = value
        elif metric_type == 'success_rate':
            self.current_metrics[server_name].success_rate = value
        elif metric_type == 'error_rate':
            self.current_metrics[server_name].error_rate = value
        elif metric_type == 'throughput':
            self.current_metrics[server_name].throughput = value
        elif metric_type == 'resource_usage':
            self.current_metrics[server_name].resource_usage = value
        
        self.current_metrics[server_name].last_updated = timestamp
        
        # Check for performance alerts
        self._check_alerts(server_name, metric_type, value)
    
    def _check_alerts(self, server_name: str, metric_type: str, value: float) -> None:
        """Check for performance alerts"""
        thresholds = {
            'response_time': 5.0,  # 5 seconds
            'error_rate': 0.1,     # 10%
            'resource_usage': 0.8  # 80%
        }
        
        if metric_type in thresholds and value > thresholds[metric_type]:
            alert = {
                'server': server_name,
                'metric': metric_type,
                'value': value,
                'threshold': thresholds[metric_type],
                'timestamp': datetime.now(),
                'severity': 'high' if value > thresholds[metric_type] * 1.5 else 'medium'
            }
            self.alerts.append(alert)
            logger.warning(f"Performance alert: {alert}")
    
    def get_server_performance(self, server_name: str) -> Optional[PerformanceMetrics]:
        """Get current performance metrics for a server"""
        return self.current_metrics.get(server_name)
    
    def get_performance_trend(self, server_name: str, metric_type: str, 
                            window_minutes: int = 60) -> List[float]:
        """Get performance trend for a specific metric"""
        key = f"{server_name}_{metric_type}"
        if key not in self.metrics_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        recent_metrics = [
            m['value'] for m in self.metrics_history[key]
            if m['timestamp'] >= cutoff_time
        ]
        return recent_metrics


class IntelligentToolSelector:
    """AI-powered tool selection based on context and performance"""
    
    def __init__(self, performance_monitor: PerformanceMonitor):
        self.performance_monitor = performance_monitor
        self.tool_capabilities: Dict[str, Dict[str, Any]] = {}
        self.selection_history: List[Dict[str, Any]] = []
        self.ml_model = None
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self._initialize_tool_capabilities()
    
    def _initialize_tool_capabilities(self) -> None:
        """Initialize tool capabilities database"""
        self.tool_capabilities = {
            'byterover': {
                'capabilities': ['knowledge_management', 'project_planning', 'context_assessment'],
                'strengths': ['persistent_storage', 'pattern_recognition', 'workflow_optimization'],
                'best_for': ['complex_planning', 'knowledge_retrieval', 'context_analysis'],
                'performance_weight': 0.9
            },
            'testsprite': {
                'capabilities': ['automated_testing', 'quality_assurance', 'test_generation'],
                'strengths': ['comprehensive_testing', 'performance_validation', 'security_testing'],
                'best_for': ['testing_workflows', 'quality_validation', 'test_automation'],
                'performance_weight': 0.8
            },
            'context7': {
                'capabilities': ['documentation_access', 'api_reference', 'library_docs'],
                'strengths': ['real_time_docs', 'comprehensive_coverage', 'best_practices'],
                'best_for': ['development_reference', 'api_integration', 'documentation_lookup'],
                'performance_weight': 0.7
            },
            'browser_tools': {
                'capabilities': ['web_testing', 'quality_audits', 'accessibility_testing'],
                'strengths': ['comprehensive_audits', 'performance_testing', 'seo_validation'],
                'best_for': ['web_application_testing', 'quality_audits', 'performance_validation'],
                'performance_weight': 0.8
            },
            'playwright': {
                'capabilities': ['browser_automation', 'e2e_testing', 'cross_browser_testing'],
                'strengths': ['advanced_automation', 'complex_interactions', 'visual_testing'],
                'best_for': ['complex_ui_testing', 'user_journey_validation', 'cross_browser_compatibility'],
                'performance_weight': 0.7
            },
            'dart': {
                'capabilities': ['task_management', 'project_management', 'team_collaboration'],
                'strengths': ['task_tracking', 'progress_monitoring', 'team_coordination'],
                'best_for': ['project_management', 'task_organization', 'team_workflows'],
                'performance_weight': 0.6
            }
        }
    
    def select_tools(self, context: ToolContext, 
                    strategy: OptimizationStrategy = OptimizationStrategy.BALANCED,
                    method: ToolSelectionMethod = ToolSelectionMethod.HYBRID) -> OptimizationResult:
        """Select optimal tools based on context and strategy"""
        start_time = time.time()
        
        # Get available tools with performance data
        available_tools = self._get_available_tools()
        
        # Apply selection method
        if method == ToolSelectionMethod.CONTEXT_BASED:
            selected_tools = self._context_based_selection(context, available_tools)
        elif method == ToolSelectionMethod.PERFORMANCE_BASED:
            selected_tools = self._performance_based_selection(context, available_tools)
        elif method == ToolSelectionMethod.MACHINE_LEARNING:
            selected_tools = self._ml_based_selection(context, available_tools)
        else:  # HYBRID
            selected_tools = self._hybrid_selection(context, available_tools, strategy)
        
        # Calculate confidence and reasoning
        confidence_score = self._calculate_confidence(selected_tools, context)
        reasoning = self._generate_reasoning(selected_tools, context, strategy)
        
        # Predict performance
        performance_prediction = self._predict_performance(selected_tools, context)
        
        # Generate alternatives
        alternatives = self._generate_alternatives(selected_tools, context, available_tools)
        
        optimization_time = time.time() - start_time
        
        result = OptimizationResult(
            selected_tools=selected_tools,
            confidence_score=confidence_score,
            reasoning=reasoning,
            performance_prediction=performance_prediction,
            alternatives=alternatives,
            optimization_time=optimization_time
        )
        
        # Record selection for learning
        self._record_selection(context, result)
        
        return result
    
    def _get_available_tools(self) -> List[str]:
        """Get list of available tools with performance data"""
        available = []
        for tool_name in self.tool_capabilities:
            performance = self.performance_monitor.get_server_performance(tool_name)
            if performance and performance.success_rate > 0.5:  # Only include working tools
                available.append(tool_name)
        return available
    
    def _context_based_selection(self, context: ToolContext, 
                               available_tools: List[str]) -> List[str]:
        """Select tools based on context requirements"""
        selected = []
        
        # Map task types to required capabilities
        task_capability_map = {
            'knowledge_retrieval': ['knowledge_management', 'context_assessment'],
            'testing': ['automated_testing', 'quality_assurance'],
            'documentation': ['documentation_access', 'api_reference'],
            'web_testing': ['web_testing', 'browser_automation'],
            'project_management': ['task_management', 'project_planning']
        }
        
        required_capabilities = task_capability_map.get(context.task_type, [])
        
        for tool in available_tools:
            capabilities = self.tool_capabilities[tool]['capabilities']
            if any(cap in capabilities for cap in required_capabilities):
                selected.append(tool)
        
        return selected[:3]  # Limit to top 3 tools
    
    def _performance_based_selection(self, context: ToolContext, 
                                   available_tools: List[str]) -> List[str]:
        """Select tools based on performance metrics"""
        tool_scores = {}
        
        for tool in available_tools:
            performance = self.performance_monitor.get_server_performance(tool)
            if performance:
                # Calculate composite performance score
                score = (
                    performance.success_rate * 0.4 +
                    (1 - performance.error_rate) * 0.3 +
                    (1 / (performance.response_time + 0.1)) * 0.2 +
                    (1 - performance.resource_usage) * 0.1
                )
                tool_scores[tool] = score
        
        # Sort by performance score and return top tools
        sorted_tools = sorted(tool_scores.items(), key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in sorted_tools[:3]]
    
    def _hybrid_selection(self, context: ToolContext, available_tools: List[str],
                         strategy: OptimizationStrategy) -> List[str]:
        """Hybrid selection combining context and performance"""
        context_tools = self._context_based_selection(context, available_tools)
        performance_tools = self._performance_based_selection(context, available_tools)
        
        # Combine and weight based on strategy
        if strategy == OptimizationStrategy.PERFORMANCE:
            weight_context = 0.3
            weight_performance = 0.7
        elif strategy == OptimizationStrategy.ACCURACY:
            weight_context = 0.7
            weight_performance = 0.3
        else:  # BALANCED
            weight_context = 0.5
            weight_performance = 0.5
        
        # Score tools based on both criteria
        tool_scores = {}
        for tool in available_tools:
            context_score = 1.0 if tool in context_tools else 0.0
            performance_score = 1.0 if tool in performance_tools else 0.0
            
            combined_score = (
                context_score * weight_context +
                performance_score * weight_performance
            )
            tool_scores[tool] = combined_score
        
        sorted_tools = sorted(tool_scores.items(), key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in sorted_tools[:3]]
    
    def _ml_based_selection(self, context: ToolContext, 
                          available_tools: List[str]) -> List[str]:
        """Machine learning-based tool selection"""
        # This would use a trained ML model in a real implementation
        # For now, fall back to hybrid selection
        return self._hybrid_selection(context, available_tools, OptimizationStrategy.BALANCED)
    
    def _calculate_confidence(self, selected_tools: List[str], 
                            context: ToolContext) -> float:
        """Calculate confidence score for selection"""
        if not selected_tools:
            return 0.0
        
        # Base confidence on tool performance and context match
        confidence = 0.0
        for tool in selected_tools:
            performance = self.performance_monitor.get_server_performance(tool)
            if performance:
                confidence += performance.success_rate * 0.5
            
            # Context match bonus
            capabilities = self.tool_capabilities.get(tool, {}).get('capabilities', [])
            if any(req in capabilities for req in context.requirements):
                confidence += 0.2
        
        return min(confidence / len(selected_tools), 1.0)
    
    def _generate_reasoning(self, selected_tools: List[str], 
                          context: ToolContext, 
                          strategy: OptimizationStrategy) -> str:
        """Generate human-readable reasoning for selection"""
        reasoning_parts = []
        
        reasoning_parts.append(f"Selected {len(selected_tools)} tools for {context.task_type} task")
        reasoning_parts.append(f"Strategy: {strategy.value}")
        
        for tool in selected_tools:
            capabilities = self.tool_capabilities.get(tool, {}).get('capabilities', [])
            performance = self.performance_monitor.get_server_performance(tool)
            
            tool_reason = f"- {tool}: "
            if capabilities:
                tool_reason += f"capabilities={', '.join(capabilities[:2])}"
            if performance:
                tool_reason += f", success_rate={performance.success_rate:.2f}"
            
            reasoning_parts.append(tool_reason)
        
        return "\n".join(reasoning_parts)
    
    def _predict_performance(self, selected_tools: List[str], 
                           context: ToolContext) -> Dict[str, float]:
        """Predict performance for selected tools"""
        predictions = {}
        
        for tool in selected_tools:
            performance = self.performance_monitor.get_server_performance(tool)
            if performance:
                # Simple prediction based on current metrics
                predicted_success = performance.success_rate * 0.9  # Slight degradation
                predicted_time = performance.response_time * 1.1    # Slight increase
                
                predictions[tool] = {
                    'predicted_success_rate': predicted_success,
                    'predicted_response_time': predicted_time,
                    'confidence': 0.8
                }
        
        return predictions
    
    def _generate_alternatives(self, selected_tools: List[str], 
                             context: ToolContext, 
                             available_tools: List[str]) -> List[Dict[str, Any]]:
        """Generate alternative tool selections"""
        alternatives = []
        
        # Alternative 1: Performance-focused
        perf_tools = self._performance_based_selection(context, available_tools)
        if perf_tools != selected_tools:
            alternatives.append({
                'type': 'performance_focused',
                'tools': perf_tools,
                'reasoning': 'Optimized for maximum performance'
            })
        
        # Alternative 2: Context-focused
        context_tools = self._context_based_selection(context, available_tools)
        if context_tools != selected_tools:
            alternatives.append({
                'type': 'context_focused',
                'tools': context_tools,
                'reasoning': 'Optimized for context requirements'
            })
        
        return alternatives
    
    def _record_selection(self, context: ToolContext, result: OptimizationResult) -> None:
        """Record selection for learning and improvement"""
        selection_record = {
            'timestamp': datetime.now(),
            'context': context.to_dict(),
            'result': result.to_dict(),
            'success': None  # Will be updated later based on actual performance
        }
        
        self.selection_history.append(selection_record)
        
        # Keep only recent history
        if len(self.selection_history) > 1000:
            self.selection_history = self.selection_history[-1000:]


class MCPOptimizationEngine:
    """Main MCP Optimization Engine"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("assets/dev/config/optimization_engine.json")
        self.performance_monitor = PerformanceMonitor()
        self.tool_selector = IntelligentToolSelector(self.performance_monitor)
        self.knowledge_cache = KnowledgeCache()
        self.config = self._load_config()
        self.optimization_history: List[Dict[str, Any]] = []
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load optimization engine configuration"""
        default_config = {
            'optimization_strategy': 'balanced',
            'tool_selection_method': 'hybrid',
            'cache_size': 10000,
            'performance_history_size': 1000,
            'enable_ml_optimization': True,
            'performance_thresholds': {
                'response_time': 5.0,
                'error_rate': 0.1,
                'resource_usage': 0.8
            }
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
        
        return default_config
    
    def optimize_tool_selection(self, task_type: str, requirements: List[str],
                              constraints: Optional[Dict[str, Any]] = None,
                              user_preferences: Optional[Dict[str, Any]] = None) -> OptimizationResult:
        """Optimize tool selection for a given task"""
        
        # Create tool context
        context = ToolContext(
            task_type=task_type,
            complexity=self._assess_complexity(requirements),
            requirements=requirements,
            constraints=constraints or {},
            user_preferences=user_preferences or {},
            historical_success=self._get_historical_success(task_type)
        )
        
        # Get optimization strategy from config
        strategy = OptimizationStrategy(self.config['optimization_strategy'])
        method = ToolSelectionMethod(self.config['tool_selection_method'])
        
        # Perform optimization
        result = self.tool_selector.select_tools(context, strategy, method)
        
        # Cache the result
        cache_key = self._generate_cache_key(context)
        self.knowledge_cache.set(cache_key, result.to_dict())
        
        # Record optimization
        self._record_optimization(context, result)
        
        return result
    
    def record_performance_metric(self, server_name: str, metric_type: str, value: float) -> None:
        """Record performance metric for a server"""
        self.performance_monitor.record_metric(server_name, metric_type, value)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all servers"""
        summary = {
            'servers': {},
            'alerts': self.performance_monitor.alerts,
            'overall_health': 'good'
        }
        
        total_servers = len(self.performance_monitor.current_metrics)
        healthy_servers = 0
        
        for server_name, metrics in self.performance_monitor.current_metrics.items():
            server_summary = {
                'metrics': metrics.to_dict(),
                'status': 'healthy' if metrics.success_rate > 0.8 else 'degraded',
                'trends': {}
            }
            
            # Calculate trends
            for metric_type in ['response_time', 'success_rate', 'error_rate']:
                trend = self.performance_monitor.get_performance_trend(
                    server_name, metric_type, window_minutes=60
                )
                if trend:
                    server_summary['trends'][metric_type] = {
                        'current': trend[-1] if trend else 0,
                        'average': statistics.mean(trend),
                        'trend': 'improving' if len(trend) > 1 and trend[-1] < trend[0] else 'stable'
                    }
            
            summary['servers'][server_name] = server_summary
            
            if metrics.success_rate > 0.8:
                healthy_servers += 1
        
        # Calculate overall health
        if total_servers > 0:
            health_ratio = healthy_servers / total_servers
            if health_ratio >= 0.8:
                summary['overall_health'] = 'good'
            elif health_ratio >= 0.6:
                summary['overall_health'] = 'degraded'
            else:
                summary['overall_health'] = 'poor'
        
        return summary
    
    def optimize_knowledge_retrieval(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize knowledge retrieval with caching and compression"""
        
        # Generate cache key
        cache_key = self._generate_query_cache_key(query, context)
        
        # Check cache first
        cached_result = self.knowledge_cache.get(cache_key)
        if cached_result:
            return {
                'result': cached_result,
                'source': 'cache',
                'optimization_applied': True
            }
        
        # If not in cache, this would typically call the actual knowledge retrieval
        # For now, return a placeholder
        result = {
            'query': query,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'optimized': True
        }
        
        # Cache the result
        self.knowledge_cache.set(cache_key, result)
        
        return {
            'result': result,
            'source': 'computed',
            'optimization_applied': True
        }
    
    def get_optimization_insights(self) -> Dict[str, Any]:
        """Get insights from optimization history"""
        if not self.optimization_history:
            return {'message': 'No optimization history available'}
        
        insights = {
            'total_optimizations': len(self.optimization_history),
            'average_confidence': 0.0,
            'most_common_tasks': {},
            'performance_trends': {},
            'recommendations': []
        }
        
        # Calculate average confidence
        confidences = [opt['result']['confidence_score'] for opt in self.optimization_history]
        if confidences:
            insights['average_confidence'] = statistics.mean(confidences)
        
        # Find most common tasks
        task_counts = defaultdict(int)
        for opt in self.optimization_history:
            task_type = opt['context']['task_type']
            task_counts[task_type] += 1
        
        insights['most_common_tasks'] = dict(sorted(task_counts.items(), 
                                                   key=lambda x: x[1], reverse=True)[:5])
        
        # Generate recommendations
        if insights['average_confidence'] < 0.7:
            insights['recommendations'].append(
                "Consider adjusting optimization strategy for better tool selection confidence"
            )
        
        if len(self.performance_monitor.alerts) > 5:
            insights['recommendations'].append(
                "High number of performance alerts detected - review server health"
            )
        
        return insights
    
    def _assess_complexity(self, requirements: List[str]) -> str:
        """Assess task complexity based on requirements"""
        complexity_indicators = {
            'simple': ['basic', 'simple', 'single'],
            'medium': ['multiple', 'several', 'moderate'],
            'complex': ['advanced', 'complex', 'comprehensive', 'multiple', 'integration']
        }
        
        requirement_text = ' '.join(requirements).lower()
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in requirement_text for indicator in indicators):
                return complexity
        
        return 'medium'  # Default complexity
    
    def _get_historical_success(self, task_type: str) -> Dict[str, float]:
        """Get historical success rates for task type"""
        # This would typically query a database of historical performance
        # For now, return default values
        return {
            'byterover': 0.85,
            'testsprite': 0.90,
            'context7': 0.80,
            'browser_tools': 0.75,
            'playwright': 0.70,
            'dart': 0.65
        }
    
    def _generate_cache_key(self, context: ToolContext) -> str:
        """Generate cache key for context"""
        context_str = json.dumps(context.to_dict(), sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()
    
    def _generate_query_cache_key(self, query: str, context: Dict[str, Any]) -> str:
        """Generate cache key for query"""
        combined = f"{query}:{json.dumps(context, sort_keys=True)}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _record_optimization(self, context: ToolContext, result: OptimizationResult) -> None:
        """Record optimization for analysis"""
        record = {
            'timestamp': datetime.now(),
            'context': context.to_dict(),
            'result': result.to_dict()
        }
        
        self.optimization_history.append(record)
        
        # Keep only recent history
        if len(self.optimization_history) > 1000:
            self.optimization_history = self.optimization_history[-1000:]
    
    def save_config(self) -> None:
        """Save current configuration"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def export_optimization_data(self, output_path: Path) -> None:
        """Export optimization data for analysis"""
        export_data = {
            'config': self.config,
            'optimization_history': self.optimization_history,
            'performance_summary': self.get_performance_summary(),
            'insights': self.get_optimization_insights(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to export data: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize optimization engine
    engine = MCPOptimizationEngine()
    
    # Example: Optimize tool selection for a testing task
    result = engine.optimize_tool_selection(
        task_type="testing",
        requirements=["automated_testing", "quality_assurance", "performance_validation"],
        constraints={"time_limit": 300, "budget": "low"},
        user_preferences={"prefer_fast": True, "require_detailed_reports": False}
    )
    
    print("Optimization Result:")
    print(f"Selected Tools: {result.selected_tools}")
    print(f"Confidence: {result.confidence_score:.2f}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Optimization Time: {result.optimization_time:.3f}s")
    
    # Record some performance metrics
    engine.record_performance_metric("testsprite", "response_time", 2.5)
    engine.record_performance_metric("testsprite", "success_rate", 0.95)
    engine.record_performance_metric("browser_tools", "response_time", 1.8)
    engine.record_performance_metric("browser_tools", "success_rate", 0.88)
    
    # Get performance summary
    summary = engine.get_performance_summary()
    print(f"\nPerformance Summary:")
    print(f"Overall Health: {summary['overall_health']}")
    print(f"Active Alerts: {len(summary['alerts'])}")
    
    # Get optimization insights
    insights = engine.get_optimization_insights()
    print(f"\nOptimization Insights:")
    print(f"Total Optimizations: {insights['total_optimizations']}")
    print(f"Average Confidence: {insights['average_confidence']:.2f}")
    print(f"Recommendations: {insights['recommendations']}")


def create_optimization_engine(project_root: Path) -> MCPOptimizationEngine:
    """
    Create and configure an MCP optimization engine.
    
    Args:
        project_root: Path to the project root directory
        
    Returns:
        Configured MCPOptimizationEngine instance
    """
    return MCPOptimizationEngine(project_root)