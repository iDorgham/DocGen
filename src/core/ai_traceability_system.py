"""
AI Traceability System for DocGen CLI Phase 3.

This module provides comprehensive AI traceability, decision logging,
and audit trail generation for the driven workflow integration.
"""

import json
import uuid
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import threading
import queue

from src.core.error_handler import DocGenError, handle_error


class TraceabilityLevel(Enum):
    """Traceability levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DecisionType(Enum):
    """Decision types."""
    ARCHITECTURAL = "architectural"
    IMPLEMENTATION = "implementation"
    QUALITY = "quality"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USER_EXPERIENCE = "user_experience"


class ImpactLevel(Enum):
    """Impact levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


@dataclass
class AIDecision:
    """Represents an AI decision."""
    decision_id: str
    decision_type: DecisionType
    title: str
    description: str
    rationale: str
    alternatives_considered: List[str]
    chosen_solution: str
    impact_level: ImpactLevel
    traceability_level: TraceabilityLevel
    spec_references: List[str]
    code_references: List[str]
    test_references: List[str]
    documentation_references: List[str]
    created_by: str
    created_date: datetime
    last_updated: datetime
    status: str
    metadata: Dict[str, Any]


@dataclass
class TraceabilityLink:
    """Represents a traceability link."""
    link_id: str
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relationship_type: str
    confidence_score: float
    created_date: datetime
    metadata: Dict[str, Any]


@dataclass
class ImpactAnalysis:
    """Represents impact analysis results."""
    analysis_id: str
    decision_id: str
    affected_components: List[str]
    affected_files: List[str]
    affected_tests: List[str]
    risk_assessment: str
    mitigation_strategies: List[str]
    rollback_plan: str
    created_date: datetime
    metadata: Dict[str, Any]


@dataclass
class AuditTrail:
    """Represents an audit trail entry."""
    trail_id: str
    event_type: str
    event_description: str
    actor: str
    timestamp: datetime
    decision_id: Optional[str]
    affected_entities: List[str]
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    metadata: Dict[str, Any]


class DecisionLogger:
    """
    Logs AI decisions and maintains decision history.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the decision logger."""
        self.project_root = project_root
        self.decisions_file = project_root / "assets" / "reports" / "ai_decisions.json"
        self.decisions: Dict[str, AIDecision] = {}
        self.decisions_lock = threading.Lock()
        self._load_decisions()
    
    def _load_decisions(self) -> None:
        """Load decisions from file."""
        if self.decisions_file.exists():
            try:
                with open(self.decisions_file, 'r') as f:
                    data = json.load(f)
                
                for decision_data in data.get('decisions', []):
                    decision = AIDecision(
                        decision_id=decision_data['decision_id'],
                        decision_type=DecisionType(decision_data['decision_type']),
                        title=decision_data['title'],
                        description=decision_data['description'],
                        rationale=decision_data['rationale'],
                        alternatives_considered=decision_data['alternatives_considered'],
                        chosen_solution=decision_data['chosen_solution'],
                        impact_level=ImpactLevel(decision_data['impact_level']),
                        traceability_level=TraceabilityLevel(decision_data['traceability_level']),
                        spec_references=decision_data['spec_references'],
                        code_references=decision_data['code_references'],
                        test_references=decision_data['test_references'],
                        documentation_references=decision_data['documentation_references'],
                        created_by=decision_data['created_by'],
                        created_date=datetime.fromisoformat(decision_data['created_date']),
                        last_updated=datetime.fromisoformat(decision_data['last_updated']),
                        status=decision_data['status'],
                        metadata=decision_data['metadata']
                    )
                    self.decisions[decision.decision_id] = decision
                    
            except Exception as e:
                print(f"Error loading AI decisions: {e}")
    
    def log_decision(self, decision: AIDecision) -> None:
        """Log a new AI decision."""
        with self.decisions_lock:
            self.decisions[decision.decision_id] = decision
            self._save_decisions()
    
    def update_decision(self, decision_id: str, updates: Dict[str, Any]) -> None:
        """Update an existing decision."""
        with self.decisions_lock:
            if decision_id in self.decisions:
                decision = self.decisions[decision_id]
                
                for key, value in updates.items():
                    if hasattr(decision, key):
                        setattr(decision, key, value)
                
                decision.last_updated = datetime.now()
                self._save_decisions()
    
    def get_decision(self, decision_id: str) -> Optional[AIDecision]:
        """Get a decision by ID."""
        return self.decisions.get(decision_id)
    
    def list_decisions(self, decision_type: Optional[DecisionType] = None, 
                      status: Optional[str] = None) -> List[AIDecision]:
        """List decisions with optional filtering."""
        decisions = list(self.decisions.values())
        
        if decision_type:
            decisions = [d for d in decisions if d.decision_type == decision_type]
        
        if status:
            decisions = [d for d in decisions if d.status == status]
        
        return sorted(decisions, key=lambda d: d.created_date, reverse=True)
    
    def _save_decisions(self) -> None:
        """Save decisions to file."""
        try:
            self.decisions_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "total_decisions": len(self.decisions),
                "decisions": []
            }
            
            for decision in self.decisions.values():
                decision_data = asdict(decision)
                decision_data['decision_type'] = decision.decision_type.value
                decision_data['impact_level'] = decision.impact_level.value
                decision_data['traceability_level'] = decision.traceability_level.value
                decision_data['created_date'] = decision.created_date.isoformat()
                decision_data['last_updated'] = decision.last_updated.isoformat()
                data['decisions'].append(decision_data)
            
            with open(self.decisions_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving AI decisions: {e}")


class TraceabilityMapper:
    """
    Maps traceability links between specs, code, tests, and documentation.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the traceability mapper."""
        self.project_root = project_root
        self.links_file = project_root / "assets" / "reports" / "traceability_links.json"
        self.links: Dict[str, TraceabilityLink] = {}
        self.links_lock = threading.Lock()
        self._load_links()
    
    def _load_links(self) -> None:
        """Load traceability links from file."""
        if self.links_file.exists():
            try:
                with open(self.links_file, 'r') as f:
                    data = json.load(f)
                
                for link_data in data.get('links', []):
                    link = TraceabilityLink(
                        link_id=link_data['link_id'],
                        source_type=link_data['source_type'],
                        source_id=link_data['source_id'],
                        target_type=link_data['target_type'],
                        target_id=link_data['target_id'],
                        relationship_type=link_data['relationship_type'],
                        confidence_score=link_data['confidence_score'],
                        created_date=datetime.fromisoformat(link_data['created_date']),
                        metadata=link_data['metadata']
                    )
                    self.links[link.link_id] = link
                    
            except Exception as e:
                print(f"Error loading traceability links: {e}")
    
    def create_link(self, link: TraceabilityLink) -> None:
        """Create a new traceability link."""
        with self.links_lock:
            self.links[link.link_id] = link
            self._save_links()
    
    def find_links(self, source_type: str, source_id: str) -> List[TraceabilityLink]:
        """Find all links from a source."""
        return [link for link in self.links.values() 
                if link.source_type == source_type and link.source_id == source_id]
    
    def find_reverse_links(self, target_type: str, target_id: str) -> List[TraceabilityLink]:
        """Find all links to a target."""
        return [link for link in self.links.values() 
                if link.target_type == target_type and link.target_id == target_id]
    
    def get_traceability_chain(self, start_type: str, start_id: str, 
                              max_depth: int = 3) -> List[TraceabilityLink]:
        """Get a complete traceability chain."""
        chain = []
        visited = set()
        current_links = self.find_links(start_type, start_id)
        depth = 0
        
        while current_links and depth < max_depth:
            next_links = []
            
            for link in current_links:
                if link.link_id not in visited:
                    chain.append(link)
                    visited.add(link.link_id)
                    
                    # Find links from this target
                    next_links.extend(self.find_links(link.target_type, link.target_id))
            
            current_links = next_links
            depth += 1
        
        return chain
    
    def _save_links(self) -> None:
        """Save traceability links to file."""
        try:
            self.links_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "total_links": len(self.links),
                "links": []
            }
            
            for link in self.links.values():
                link_data = asdict(link)
                link_data['created_date'] = link.created_date.isoformat()
                data['links'].append(link_data)
            
            with open(self.links_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving traceability links: {e}")


class ImpactAnalyzer:
    """
    Analyzes the impact of decisions and changes.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the impact analyzer."""
        self.project_root = project_root
        self.analyses_file = project_root / "assets" / "reports" / "impact_analyses.json"
        self.analyses: Dict[str, ImpactAnalysis] = {}
        self.analyses_lock = threading.Lock()
        self._load_analyses()
    
    def _load_analyses(self) -> None:
        """Load impact analyses from file."""
        if self.analyses_file.exists():
            try:
                with open(self.analyses_file, 'r') as f:
                    data = json.load(f)
                
                for analysis_data in data.get('analyses', []):
                    analysis = ImpactAnalysis(
                        analysis_id=analysis_data['analysis_id'],
                        decision_id=analysis_data['decision_id'],
                        affected_components=analysis_data['affected_components'],
                        affected_files=analysis_data['affected_files'],
                        affected_tests=analysis_data['affected_tests'],
                        risk_assessment=analysis_data['risk_assessment'],
                        mitigation_strategies=analysis_data['mitigation_strategies'],
                        rollback_plan=analysis_data['rollback_plan'],
                        created_date=datetime.fromisoformat(analysis_data['created_date']),
                        metadata=analysis_data['metadata']
                    )
                    self.analyses[analysis.analysis_id] = analysis
                    
            except Exception as e:
                print(f"Error loading impact analyses: {e}")
    
    def analyze_impact(self, decision_id: str) -> ImpactAnalysis:
        """Analyze the impact of a decision."""
        analysis_id = str(uuid.uuid4())
        
        # Get the decision
        decision_logger = DecisionLogger(self.project_root)
        decision = decision_logger.get_decision(decision_id)
        
        if not decision:
            raise ValueError(f"Decision {decision_id} not found")
        
        # Analyze affected components
        affected_components = self._analyze_affected_components(decision)
        affected_files = self._analyze_affected_files(decision)
        affected_tests = self._analyze_affected_tests(decision)
        
        # Assess risk
        risk_assessment = self._assess_risk(decision, affected_components, affected_files)
        
        # Generate mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(decision, risk_assessment)
        
        # Create rollback plan
        rollback_plan = self._create_rollback_plan(decision, affected_files)
        
        # Create impact analysis
        analysis = ImpactAnalysis(
            analysis_id=analysis_id,
            decision_id=decision_id,
            affected_components=affected_components,
            affected_files=affected_files,
            affected_tests=affected_tests,
            risk_assessment=risk_assessment,
            mitigation_strategies=mitigation_strategies,
            rollback_plan=rollback_plan,
            created_date=datetime.now(),
            metadata={
                "decision_type": decision.decision_type.value,
                "impact_level": decision.impact_level.value,
                "traceability_level": decision.traceability_level.value
            }
        )
        
        # Save analysis
        with self.analyses_lock:
            self.analyses[analysis_id] = analysis
            self._save_analyses()
        
        return analysis
    
    def _analyze_affected_components(self, decision: AIDecision) -> List[str]:
        """Analyze affected components based on decision."""
        components = []
        
        # Analyze based on decision type
        if decision.decision_type == DecisionType.ARCHITECTURAL:
            components.extend(["core", "cli", "commands", "models"])
        elif decision.decision_type == DecisionType.IMPLEMENTATION:
            components.extend(decision.code_references)
        elif decision.decision_type == DecisionType.QUALITY:
            components.extend(["tests", "validation", "quality_gates"])
        elif decision.decision_type == DecisionType.SECURITY:
            components.extend(["authentication", "authorization", "validation"])
        elif decision.decision_type == DecisionType.PERFORMANCE:
            components.extend(["optimization", "caching", "monitoring"])
        elif decision.decision_type == DecisionType.USER_EXPERIENCE:
            components.extend(["cli", "templates", "output"])
        
        return list(set(components))
    
    def _analyze_affected_files(self, decision: AIDecision) -> List[str]:
        """Analyze affected files based on decision."""
        files = []
        
        # Add files from code references
        files.extend(decision.code_references)
        
        # Add files from spec references
        files.extend(decision.spec_references)
        
        # Add files from test references
        files.extend(decision.test_references)
        
        # Add files from documentation references
        files.extend(decision.documentation_references)
        
        return list(set(files))
    
    def _analyze_affected_tests(self, decision: AIDecision) -> List[str]:
        """Analyze affected tests based on decision."""
        tests = []
        
        # Add tests from test references
        tests.extend(decision.test_references)
        
        # Find related tests based on affected components
        affected_components = self._analyze_affected_components(decision)
        for component in affected_components:
            test_pattern = f"test_{component}*.py"
            test_files = list(self.project_root.glob(f"tests/**/{test_pattern}"))
            tests.extend([str(f) for f in test_files])
        
        return list(set(tests))
    
    def _assess_risk(self, decision: AIDecision, components: List[str], files: List[str]) -> str:
        """Assess risk level based on decision and affected entities."""
        risk_factors = []
        
        # Risk based on impact level
        if decision.impact_level == ImpactLevel.CRITICAL:
            risk_factors.append("Critical impact level")
        elif decision.impact_level == ImpactLevel.HIGH:
            risk_factors.append("High impact level")
        
        # Risk based on number of affected components
        if len(components) > 5:
            risk_factors.append("Many components affected")
        elif len(components) > 2:
            risk_factors.append("Multiple components affected")
        
        # Risk based on number of affected files
        if len(files) > 10:
            risk_factors.append("Many files affected")
        elif len(files) > 5:
            risk_factors.append("Multiple files affected")
        
        # Risk based on decision type
        if decision.decision_type == DecisionType.ARCHITECTURAL:
            risk_factors.append("Architectural change")
        elif decision.decision_type == DecisionType.SECURITY:
            risk_factors.append("Security-related change")
        
        # Determine overall risk level
        if len(risk_factors) >= 3:
            return "HIGH"
        elif len(risk_factors) >= 2:
            return "MEDIUM"
        elif len(risk_factors) >= 1:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _generate_mitigation_strategies(self, decision: AIDecision, risk_level: str) -> List[str]:
        """Generate mitigation strategies based on decision and risk level."""
        strategies = []
        
        if risk_level == "HIGH":
            strategies.extend([
                "Implement comprehensive testing before deployment",
                "Create detailed rollback plan",
                "Conduct thorough code review",
                "Perform security audit",
                "Monitor system closely after deployment"
            ])
        elif risk_level == "MEDIUM":
            strategies.extend([
                "Run full test suite",
                "Review affected code",
                "Update documentation",
                "Monitor for issues"
            ])
        elif risk_level == "LOW":
            strategies.extend([
                "Run relevant tests",
                "Update documentation if needed"
            ])
        
        # Add decision-specific strategies
        if decision.decision_type == DecisionType.SECURITY:
            strategies.append("Conduct security review")
        elif decision.decision_type == DecisionType.PERFORMANCE:
            strategies.append("Run performance benchmarks")
        elif decision.decision_type == DecisionType.USER_EXPERIENCE:
            strategies.append("Conduct user acceptance testing")
        
        return strategies
    
    def _create_rollback_plan(self, decision: AIDecision, affected_files: List[str]) -> str:
        """Create a rollback plan for the decision."""
        plan = f"Rollback plan for decision: {decision.title}\n\n"
        
        plan += "1. Identify affected files:\n"
        for file in affected_files:
            plan += f"   - {file}\n"
        
        plan += "\n2. Backup current state:\n"
        plan += "   - Create git branch for rollback\n"
        plan += "   - Document current configuration\n"
        
        plan += "\n3. Rollback steps:\n"
        plan += "   - Revert code changes\n"
        plan += "   - Restore configuration\n"
        plan += "   - Run tests to verify rollback\n"
        plan += "   - Update documentation\n"
        
        plan += "\n4. Verification:\n"
        plan += "   - Run full test suite\n"
        plan += "   - Verify system functionality\n"
        plan += "   - Monitor for issues\n"
        
        return plan
    
    def _save_analyses(self) -> None:
        """Save impact analyses to file."""
        try:
            self.analyses_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "total_analyses": len(self.analyses),
                "analyses": []
            }
            
            for analysis in self.analyses.values():
                analysis_data = asdict(analysis)
                analysis_data['created_date'] = analysis.created_date.isoformat()
                data['analyses'].append(analysis_data)
            
            with open(self.analyses_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving impact analyses: {e}")


class AuditTrailGenerator:
    """
    Generates audit trails for decisions and changes.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the audit trail generator."""
        self.project_root = project_root
        self.audit_file = project_root / "assets" / "reports" / "audit_trail.json"
        self.audit_entries: List[AuditTrail] = []
        self.audit_lock = threading.Lock()
        self._load_audit_trail()
    
    def _load_audit_trail(self) -> None:
        """Load audit trail from file."""
        if self.audit_file.exists():
            try:
                with open(self.audit_file, 'r') as f:
                    data = json.load(f)
                
                for entry_data in data.get('entries', []):
                    entry = AuditTrail(
                        trail_id=entry_data['trail_id'],
                        event_type=entry_data['event_type'],
                        event_description=entry_data['event_description'],
                        actor=entry_data['actor'],
                        timestamp=datetime.fromisoformat(entry_data['timestamp']),
                        decision_id=entry_data.get('decision_id'),
                        affected_entities=entry_data['affected_entities'],
                        before_state=entry_data['before_state'],
                        after_state=entry_data['after_state'],
                        metadata=entry_data['metadata']
                    )
                    self.audit_entries.append(entry)
                    
            except Exception as e:
                print(f"Error loading audit trail: {e}")
    
    def log_event(self, event: AuditTrail) -> None:
        """Log an audit trail event."""
        with self.audit_lock:
            self.audit_entries.append(event)
            self._save_audit_trail()
    
    def generate_audit_report(self, start_date: Optional[datetime] = None, 
                            end_date: Optional[datetime] = None,
                            event_type: Optional[str] = None) -> List[AuditTrail]:
        """Generate audit report with optional filtering."""
        entries = self.audit_entries
        
        if start_date:
            entries = [e for e in entries if e.timestamp >= start_date]
        
        if end_date:
            entries = [e for e in entries if e.timestamp <= end_date]
        
        if event_type:
            entries = [e for e in entries if e.event_type == event_type]
        
        return sorted(entries, key=lambda e: e.timestamp, reverse=True)
    
    def _save_audit_trail(self) -> None:
        """Save audit trail to file."""
        try:
            self.audit_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "total_entries": len(self.audit_entries),
                "entries": []
            }
            
            for entry in self.audit_entries:
                entry_data = asdict(entry)
                entry_data['timestamp'] = entry.timestamp.isoformat()
                data['entries'].append(entry_data)
            
            with open(self.audit_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving audit trail: {e}")


class AITraceabilitySystem:
    """
    Main AI traceability system that orchestrates all traceability components.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the AI traceability system."""
        self.project_root = project_root
        
        # Initialize components
        self.decision_logger = DecisionLogger(project_root)
        self.traceability_mapper = TraceabilityMapper(project_root)
        self.impact_analyzer = ImpactAnalyzer(project_root)
        self.audit_generator = AuditTrailGenerator(project_root)
    
    def log_decision(self, decision: AIDecision) -> None:
        """Log a new AI decision."""
        self.decision_logger.log_decision(decision)
        
        # Create audit trail entry
        audit_entry = AuditTrail(
            trail_id=str(uuid.uuid4()),
            event_type="decision_logged",
            event_description=f"AI decision logged: {decision.title}",
            actor=decision.created_by,
            timestamp=datetime.now(),
            decision_id=decision.decision_id,
            affected_entities=decision.code_references + decision.spec_references,
            before_state={},
            after_state={"decision": decision.title, "type": decision.decision_type.value},
            metadata={"impact_level": decision.impact_level.value}
        )
        self.audit_generator.log_event(audit_entry)
    
    def analyze_decision_impact(self, decision_id: str) -> ImpactAnalysis:
        """Analyze the impact of a decision."""
        analysis = self.impact_analyzer.analyze_impact(decision_id)
        
        # Create audit trail entry
        audit_entry = AuditTrail(
            trail_id=str(uuid.uuid4()),
            event_type="impact_analysis",
            event_description=f"Impact analysis performed for decision: {decision_id}",
            actor="AI_Traceability_System",
            timestamp=datetime.now(),
            decision_id=decision_id,
            affected_entities=analysis.affected_files,
            before_state={},
            after_state={"analysis_id": analysis.analysis_id, "risk": analysis.risk_assessment},
            metadata={"affected_components": len(analysis.affected_components)}
        )
        self.audit_generator.log_event(audit_entry)
        
        return analysis
    
    def create_traceability_link(self, source_type: str, source_id: str,
                               target_type: str, target_id: str,
                               relationship_type: str, confidence_score: float = 1.0) -> None:
        """Create a traceability link."""
        link = TraceabilityLink(
            link_id=str(uuid.uuid4()),
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            relationship_type=relationship_type,
            confidence_score=confidence_score,
            created_date=datetime.now(),
            metadata={}
        )
        
        self.traceability_mapper.create_link(link)
        
        # Create audit trail entry
        audit_entry = AuditTrail(
            trail_id=str(uuid.uuid4()),
            event_type="traceability_link_created",
            event_description=f"Traceability link created: {source_type}:{source_id} -> {target_type}:{target_id}",
            actor="AI_Traceability_System",
            timestamp=datetime.now(),
            decision_id=None,
            affected_entities=[source_id, target_id],
            before_state={},
            after_state={"link_id": link.link_id, "relationship": relationship_type},
            metadata={"confidence": confidence_score}
        )
        self.audit_generator.log_event(audit_entry)
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate compliance report."""
        decisions = self.decision_logger.list_decisions()
        links = list(self.traceability_mapper.links.values())
        analyses = list(self.impact_analyzer.analyses.values())
        audit_entries = self.audit_generator.audit_entries
        
        # Calculate compliance metrics
        total_decisions = len(decisions)
        traced_decisions = len([d for d in decisions if d.code_references or d.spec_references])
        analyzed_decisions = len([d for d in decisions if any(a.decision_id == d.decision_id for a in analyses)])
        
        traceability_score = (traced_decisions / total_decisions * 100) if total_decisions > 0 else 0
        analysis_score = (analyzed_decisions / total_decisions * 100) if total_decisions > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_decisions": total_decisions,
            "traced_decisions": traced_decisions,
            "analyzed_decisions": analyzed_decisions,
            "total_links": len(links),
            "total_analyses": len(analyses),
            "total_audit_entries": len(audit_entries),
            "traceability_score": round(traceability_score, 2),
            "analysis_score": round(analysis_score, 2),
            "overall_compliance": round((traceability_score + analysis_score) / 2, 2),
            "recent_decisions": [
                {
                    "id": d.decision_id,
                    "title": d.title,
                    "type": d.decision_type.value,
                    "impact": d.impact_level.value,
                    "created": d.created_date.isoformat()
                }
                for d in decisions[:10]
            ],
            "recommendations": self._generate_compliance_recommendations(
                traceability_score, analysis_score, total_decisions
            )
        }
    
    def _generate_compliance_recommendations(self, traceability_score: float, 
                                           analysis_score: float, total_decisions: int) -> List[str]:
        """Generate compliance recommendations."""
        recommendations = []
        
        if traceability_score < 90:
            recommendations.append("Improve decision traceability by adding more code and spec references")
        
        if analysis_score < 80:
            recommendations.append("Perform impact analysis for more decisions")
        
        if total_decisions < 10:
            recommendations.append("Log more AI decisions to improve traceability coverage")
        
        if traceability_score < 70:
            recommendations.append("Critical: Traceability score is below acceptable threshold")
        
        if analysis_score < 60:
            recommendations.append("Critical: Impact analysis coverage is below acceptable threshold")
        
        return recommendations


def create_ai_traceability_system(project_root: Path) -> AITraceabilitySystem:
    """
    Factory function to create an AI traceability system.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        Initialized AITraceabilitySystem instance
    """
    return AITraceabilitySystem(project_root)
