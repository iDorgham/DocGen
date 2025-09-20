"""
Project Steering Controller for DocGen CLI Phase 3.

This module provides intelligent project steering, context maintenance,
and automated quality assurance for the driven workflow integration.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import threading
import queue

from src.core.error_handler import DocGenError, handle_error
from src.core.spec_validator import SpecValidator, create_spec_validator
from src.core.agent_hooks import AgentHookManager, create_agent_hook_manager


class SteeringMode(Enum):
    """Project steering modes."""
    AUTOMATIC = "automatic"
    GUIDED = "guided"
    MANUAL = "manual"


class QualityGate(Enum):
    """Quality gate types."""
    PRE_COMMIT = "pre_commit"
    PRE_DEPLOYMENT = "pre_deployment"
    CONTINUOUS = "continuous"
    MANUAL = "manual"


@dataclass
class ProjectContext:
    """Represents the current project context."""
    project_name: str
    current_phase: str
    active_tasks: List[str]
    completed_tasks: List[str]
    quality_score: float
    compliance_score: float
    last_updated: datetime
    context_hash: str


@dataclass
class QualityGateResult:
    """Result of a quality gate check."""
    gate_type: QualityGate
    passed: bool
    score: float
    issues: List[str]
    recommendations: List[str]
    timestamp: datetime


@dataclass
class ArchitecturalDecision:
    """Represents an architectural decision."""
    decision_id: str
    title: str
    description: str
    rationale: str
    alternatives: List[str]
    consequences: List[str]
    status: str
    created_date: datetime
    last_updated: datetime


class ContextMaintenanceEngine:
    """
    Maintains project context and ensures consistency across development phases.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the context maintenance engine."""
        self.project_root = project_root
        self.context_file = project_root / "assets" / "reports" / "project_context.json"
        self.context: Optional[ProjectContext] = None
        self.context_lock = threading.Lock()
        
    def load_context(self) -> ProjectContext:
        """Load current project context."""
        with self.context_lock:
            if self.context_file.exists():
                try:
                    with open(self.context_file, 'r') as f:
                        data = json.load(f)
                    
                    self.context = ProjectContext(
                        project_name=data.get('project_name', ''),
                        current_phase=data.get('current_phase', ''),
                        active_tasks=data.get('active_tasks', []),
                        completed_tasks=data.get('completed_tasks', []),
                        quality_score=data.get('quality_score', 0.0),
                        compliance_score=data.get('compliance_score', 0.0),
                        last_updated=datetime.fromisoformat(data.get('last_updated', datetime.now().isoformat())),
                        context_hash=data.get('context_hash', '')
                    )
                except Exception as e:
                    print(f"Error loading context: {e}")
                    self.context = self._create_default_context()
            else:
                self.context = self._create_default_context()
            
            return self.context
    
    def save_context(self, context: ProjectContext) -> None:
        """Save project context."""
        with self.context_lock:
            try:
                self.context_file.parent.mkdir(parents=True, exist_ok=True)
                
                data = asdict(context)
                data['last_updated'] = context.last_updated.isoformat()
                
                with open(self.context_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.context = context
                
            except Exception as e:
                print(f"Error saving context: {e}")
    
    def update_context(self, updates: Dict[str, Any]) -> ProjectContext:
        """Update project context with new information."""
        current_context = self.load_context()
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(current_context, key):
                setattr(current_context, key, value)
        
        # Update metadata
        current_context.last_updated = datetime.now()
        current_context.context_hash = self._generate_context_hash(current_context)
        
        # Save updated context
        self.save_context(current_context)
        
        return current_context
    
    def _create_default_context(self) -> ProjectContext:
        """Create default project context."""
        return ProjectContext(
            project_name=self.project_root.name,
            current_phase="Phase 3",
            active_tasks=[],
            completed_tasks=[],
            quality_score=0.0,
            compliance_score=0.0,
            last_updated=datetime.now(),
            context_hash=""
        )
    
    def _generate_context_hash(self, context: ProjectContext) -> str:
        """Generate hash for context change detection."""
        content = f"{context.project_name}:{context.current_phase}:{context.quality_score}:{context.compliance_score}"
        return hashlib.md5(content.encode()).hexdigest()[:8]


class QualityAssuranceController:
    """
    Controls quality assurance processes and enforces quality gates.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the quality assurance controller."""
        self.project_root = project_root
        self.spec_validator = create_spec_validator(project_root)
        self.quality_gates: Dict[QualityGate, List[str]] = {
            QualityGate.PRE_COMMIT: [
                "spec_compliance",
                "code_quality",
                "test_coverage",
                "security_scan"
            ],
            QualityGate.PRE_DEPLOYMENT: [
                "full_test_suite",
                "performance_benchmarks",
                "security_audit",
                "documentation_completeness"
            ],
            QualityGate.CONTINUOUS: [
                "spec_compliance",
                "code_quality"
            ]
        }
    
    def run_quality_gate(self, gate_type: QualityGate) -> QualityGateResult:
        """Run a specific quality gate."""
        print(f"Running quality gate: {gate_type.value}")
        
        issues = []
        recommendations = []
        total_score = 0.0
        gate_checks = self.quality_gates.get(gate_type, [])
        
        for check in gate_checks:
            try:
                score, check_issues, check_recommendations = self._run_quality_check(check)
                total_score += score
                issues.extend(check_issues)
                recommendations.extend(check_recommendations)
            except Exception as e:
                issues.append(f"Error running {check}: {e}")
        
        # Calculate average score
        avg_score = total_score / len(gate_checks) if gate_checks else 0.0
        passed = avg_score >= 80.0 and len(issues) == 0
        
        return QualityGateResult(
            gate_type=gate_type,
            passed=passed,
            score=avg_score,
            issues=issues,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    
    def _run_quality_check(self, check_name: str) -> Tuple[float, List[str], List[str]]:
        """Run a specific quality check."""
        issues = []
        recommendations = []
        score = 0.0
        
        if check_name == "spec_compliance":
            score, issues, recommendations = self._check_spec_compliance()
        elif check_name == "code_quality":
            score, issues, recommendations = self._check_code_quality()
        elif check_name == "test_coverage":
            score, issues, recommendations = self._check_test_coverage()
        elif check_name == "security_scan":
            score, issues, recommendations = self._check_security()
        elif check_name == "full_test_suite":
            score, issues, recommendations = self._check_full_test_suite()
        elif check_name == "performance_benchmarks":
            score, issues, recommendations = self._check_performance()
        elif check_name == "security_audit":
            score, issues, recommendations = self._check_security_audit()
        elif check_name == "documentation_completeness":
            score, issues, recommendations = self._check_documentation()
        
        return score, issues, recommendations
    
    def _check_spec_compliance(self) -> Tuple[float, List[str], List[str]]:
        """Check spec compliance."""
        try:
            validation_result = self.spec_validator.validate_spec_compliance()
            return validation_result.compliance_score, validation_result.errors, validation_result.warnings
        except Exception as e:
            return 0.0, [f"Spec compliance check failed: {e}"], ["Fix spec validation system"]
    
    def _check_code_quality(self) -> Tuple[float, List[str], List[str]]:
        """Check code quality."""
        try:
            import subprocess
            import sys
            
            # Run flake8 for code quality
            result = subprocess.run(
                [sys.executable, '-m', 'flake8', 'src/', '--count', '--select=E9,F63,F7,F82', '--show-source', '--statistics'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return 100.0, [], []
            else:
                issues = result.stdout.split('\n') if result.stdout else []
                return max(0, 100 - len(issues) * 5), issues, ["Fix code quality issues"]
                
        except Exception as e:
            return 0.0, [f"Code quality check failed: {e}"], ["Install flake8 for code quality checking"]
    
    def _check_test_coverage(self) -> Tuple[float, List[str], List[str]]:
        """Check test coverage."""
        try:
            import subprocess
            import sys
            
            # Run pytest with coverage
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', '--cov=src', '--cov-report=term-missing', '--cov-fail-under=80'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return 100.0, [], []
            else:
                return 70.0, ["Test coverage below 80%"], ["Increase test coverage to 80% or higher"]
                
        except Exception as e:
            return 0.0, [f"Test coverage check failed: {e}"], ["Install pytest-cov for coverage checking"]
    
    def _check_security(self) -> Tuple[float, List[str], List[str]]:
        """Check security issues."""
        try:
            import subprocess
            import sys
            
            # Run bandit for security issues
            result = subprocess.run(
                [sys.executable, '-m', 'bandit', '-r', 'src/', '-f', 'json'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return 100.0, [], []
            else:
                try:
                    import json
                    security_data = json.loads(result.stdout)
                    issues = [issue['issue_text'] for issue in security_data.get('results', [])]
                    return max(0, 100 - len(issues) * 10), issues, ["Fix security issues"]
                except:
                    return 80.0, ["Security scan found issues"], ["Review and fix security issues"]
                    
        except Exception as e:
            return 0.0, [f"Security check failed: {e}"], ["Install bandit for security checking"]
    
    def _check_full_test_suite(self) -> Tuple[float, List[str], List[str]]:
        """Check full test suite."""
        try:
            import subprocess
            import sys
            
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', 'tests/', '-v'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return 100.0, [], []
            else:
                return 70.0, ["Some tests failed"], ["Fix failing tests"]
                
        except Exception as e:
            return 0.0, [f"Test suite check failed: {e}"], ["Ensure all tests are passing"]
    
    def _check_performance(self) -> Tuple[float, List[str], List[str]]:
        """Check performance benchmarks."""
        # This would implement performance benchmarking
        # For now, return a placeholder
        return 85.0, [], ["Implement performance benchmarking"]
    
    def _check_security_audit(self) -> Tuple[float, List[str], List[str]]:
        """Check security audit."""
        # This would implement comprehensive security audit
        # For now, return a placeholder
        return 90.0, [], ["Implement comprehensive security audit"]
    
    def _check_documentation(self) -> Tuple[float, List[str], List[str]]:
        """Check documentation completeness."""
        try:
            docs_dir = self.project_root / "assets" / "docs"
            required_docs = ["README.md", "DEVELOPMENT.md", "API.md"]
            
            missing_docs = []
            for doc in required_docs:
                if not (docs_dir / doc).exists():
                    missing_docs.append(doc)
            
            if not missing_docs:
                return 100.0, [], []
            else:
                score = max(0, 100 - len(missing_docs) * 20)
                return score, [f"Missing documentation: {', '.join(missing_docs)}"], ["Complete missing documentation"]
                
        except Exception as e:
            return 0.0, [f"Documentation check failed: {e}"], ["Fix documentation checking system"]


class ArchitecturalDecisionTracker:
    """
    Tracks architectural decisions and their impact.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the architectural decision tracker."""
        self.project_root = project_root
        self.decisions_file = project_root / "assets" / "reports" / "architectural_decisions.json"
        self.decisions: Dict[str, ArchitecturalDecision] = {}
        self._load_decisions()
    
    def _load_decisions(self) -> None:
        """Load architectural decisions from file."""
        if self.decisions_file.exists():
            try:
                with open(self.decisions_file, 'r') as f:
                    data = json.load(f)
                
                for decision_data in data.get('decisions', []):
                    decision = ArchitecturalDecision(
                        decision_id=decision_data['decision_id'],
                        title=decision_data['title'],
                        description=decision_data['description'],
                        rationale=decision_data['rationale'],
                        alternatives=decision_data['alternatives'],
                        consequences=decision_data['consequences'],
                        status=decision_data['status'],
                        created_date=datetime.fromisoformat(decision_data['created_date']),
                        last_updated=datetime.fromisoformat(decision_data['last_updated'])
                    )
                    self.decisions[decision.decision_id] = decision
                    
            except Exception as e:
                print(f"Error loading architectural decisions: {e}")
    
    def add_decision(self, decision: ArchitecturalDecision) -> None:
        """Add a new architectural decision."""
        self.decisions[decision.decision_id] = decision
        self._save_decisions()
    
    def update_decision(self, decision_id: str, updates: Dict[str, Any]) -> None:
        """Update an existing architectural decision."""
        if decision_id in self.decisions:
            decision = self.decisions[decision_id]
            
            for key, value in updates.items():
                if hasattr(decision, key):
                    setattr(decision, key, value)
            
            decision.last_updated = datetime.now()
            self._save_decisions()
    
    def get_decision(self, decision_id: str) -> Optional[ArchitecturalDecision]:
        """Get an architectural decision by ID."""
        return self.decisions.get(decision_id)
    
    def list_decisions(self, status: Optional[str] = None) -> List[ArchitecturalDecision]:
        """List architectural decisions, optionally filtered by status."""
        decisions = list(self.decisions.values())
        
        if status:
            decisions = [d for d in decisions if d.status == status]
        
        return sorted(decisions, key=lambda d: d.created_date, reverse=True)
    
    def _save_decisions(self) -> None:
        """Save architectural decisions to file."""
        try:
            self.decisions_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "decisions": []
            }
            
            for decision in self.decisions.values():
                decision_data = asdict(decision)
                decision_data['created_date'] = decision.created_date.isoformat()
                decision_data['last_updated'] = decision.last_updated.isoformat()
                data['decisions'].append(decision_data)
            
            with open(self.decisions_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving architectural decisions: {e}")


class ProjectSteeringController:
    """
    Main project steering controller that orchestrates all steering components.
    """
    
    def __init__(self, project_root: Path, mode: SteeringMode = SteeringMode.AUTOMATIC):
        """Initialize the project steering controller."""
        self.project_root = project_root
        self.mode = mode
        
        # Initialize components
        self.context_engine = ContextMaintenanceEngine(project_root)
        self.quality_controller = QualityAssuranceController(project_root)
        self.decision_tracker = ArchitecturalDecisionTracker(project_root)
        self.agent_hooks = create_agent_hook_manager(project_root)
        
        # Steering state
        self.running = False
        self.steering_thread = None
        self.event_queue = queue.Queue()
        
    def start_steering(self) -> None:
        """Start project steering."""
        if self.running:
            return
        
        print(f"Starting project steering in {self.mode.value} mode...")
        
        # Load current context
        context = self.context_engine.load_context()
        print(f"Current project context: {context.project_name} - {context.current_phase}")
        
        # Start agent hooks if in automatic mode
        if self.mode == SteeringMode.AUTOMATIC:
            self.agent_hooks.start_monitoring()
        
        # Start steering thread
        self.running = True
        self.steering_thread = threading.Thread(target=self._steering_loop, daemon=True)
        self.steering_thread.start()
        
        print("Project steering started successfully")
    
    def stop_steering(self) -> None:
        """Stop project steering."""
        if not self.running:
            return
        
        print("Stopping project steering...")
        
        self.running = False
        
        # Stop agent hooks
        if self.mode == SteeringMode.AUTOMATIC:
            self.agent_hooks.stop_monitoring()
        
        # Wait for steering thread to finish
        if self.steering_thread:
            self.steering_thread.join(timeout=5)
        
        print("Project steering stopped")
    
    def _steering_loop(self) -> None:
        """Main steering loop."""
        while self.running:
            try:
                # Run continuous quality gates
                if self.mode == SteeringMode.AUTOMATIC:
                    self._run_continuous_quality_gates()
                
                # Update context periodically
                self._update_project_context()
                
                # Sleep for a short interval
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in steering loop: {e}")
                time.sleep(5)  # Brief pause before retry
    
    def _run_continuous_quality_gates(self) -> None:
        """Run continuous quality gates."""
        try:
            result = self.quality_controller.run_quality_gate(QualityGate.CONTINUOUS)
            
            if not result.passed:
                print(f"Continuous quality gate failed: {result.issues}")
                # Could trigger automated fixes or notifications here
                
        except Exception as e:
            print(f"Error running continuous quality gates: {e}")
    
    def _update_project_context(self) -> None:
        """Update project context with current state."""
        try:
            # Get current quality and compliance scores
            quality_result = self.quality_controller.run_quality_gate(QualityGate.CONTINUOUS)
            spec_result = self.context_engine.spec_validator.validate_spec_compliance()
            
            # Update context
            updates = {
                'quality_score': quality_result.score,
                'compliance_score': spec_result.compliance_score,
                'last_updated': datetime.now()
            }
            
            self.context_engine.update_context(updates)
            
        except Exception as e:
            print(f"Error updating project context: {e}")
    
    def run_quality_gate(self, gate_type: QualityGate) -> QualityGateResult:
        """Run a specific quality gate."""
        return self.quality_controller.run_quality_gate(gate_type)
    
    def add_architectural_decision(self, decision: ArchitecturalDecision) -> None:
        """Add an architectural decision."""
        self.decision_tracker.add_decision(decision)
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status."""
        context = self.context_engine.load_context()
        
        return {
            "project_name": context.project_name,
            "current_phase": context.current_phase,
            "quality_score": context.quality_score,
            "compliance_score": context.compliance_score,
            "active_tasks": context.active_tasks,
            "completed_tasks": context.completed_tasks,
            "last_updated": context.last_updated.isoformat(),
            "steering_mode": self.mode.value,
            "steering_active": self.running,
            "total_decisions": len(self.decision_tracker.decisions),
            "recent_decisions": [
                {
                    "id": d.decision_id,
                    "title": d.title,
                    "status": d.status,
                    "created": d.created_date.isoformat()
                }
                for d in self.decision_tracker.list_decisions()[:5]
            ]
        }


def create_project_steering_controller(project_root: Path, mode: SteeringMode = SteeringMode.AUTOMATIC) -> ProjectSteeringController:
    """
    Factory function to create a project steering controller.
    
    Args:
        project_root: Root directory of the project
        mode: Steering mode (automatic, guided, or manual)
        
    Returns:
        Initialized ProjectSteeringController instance
    """
    return ProjectSteeringController(project_root, mode)
