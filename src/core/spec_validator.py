"""
Spec Validation System for DocGen CLI Phase 3.

This module provides comprehensive spec validation, traceability, and compliance monitoring
for the driven workflow integration.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re

from src.core.error_handler import ValidationError, DocGenError


@dataclass
class SpecValidationResult:
    """Result of spec validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    compliance_score: float
    traceability_map: Dict[str, List[str]]
    last_updated: datetime
    spec_hash: str


@dataclass
class SpecTraceabilityEntry:
    """Entry in the spec-to-code traceability map."""
    spec_section: str
    spec_file: str
    code_files: List[str]
    test_files: List[str]
    documentation_files: List[str]
    last_verified: datetime
    verification_status: str


class SpecValidator:
    """
    Comprehensive spec validation system for driven workflow.
    
    Provides real-time spec compliance checking, traceability mapping,
    and automated validation gates.
    """
    
    def __init__(self, project_root: Path):
        """
        Initialize the spec validator.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.specs_dir = project_root / "assets" / "specs"
        self.src_dir = project_root / "src"
        self.tests_dir = project_root / "tests"
        self.docs_dir = project_root / "assets" / "docs"
        
        # Validation rules and patterns
        self.validation_rules = self._load_validation_rules()
        self.traceability_map: Dict[str, SpecTraceabilityEntry] = {}
        
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules from configuration."""
        return {
            "required_spec_files": [
                "requirements.md",
                "tasks.md", 
                "technical.md"
            ],
            "required_sections": {
                "requirements.md": [
                    "## Overview",
                    "## Functional Requirements",
                    "## Non-Functional Requirements"
                ],
                "tasks.md": [
                    "## Overview",
                    "## Phase 1",
                    "## Phase 2", 
                    "## Phase 3"
                ],
                "technical.md": [
                    "## Architecture",
                    "## Technology Stack",
                    "## Implementation Details"
                ]
            },
            "code_patterns": {
                "cli_commands": r"def\s+\w+.*:\s*#\s*CLI\s+command",
                "validation": r"def\s+validate_\w+.*:\s*#\s*Validation",
                "error_handling": r"except\s+.*:\s*#\s*Error\s+handling"
            }
        }
    
    def validate_spec_compliance(self) -> SpecValidationResult:
        """
        Perform comprehensive spec compliance validation.
        
        Returns:
            SpecValidationResult with validation details
        """
        errors = []
        warnings = []
        traceability_map = {}
        
        # Check required spec files exist
        missing_files = self._check_required_files()
        if missing_files:
            errors.extend([f"Missing required spec file: {f}" for f in missing_files])
        
        # Validate spec file content
        for spec_file in self.validation_rules["required_spec_files"]:
            spec_path = self.specs_dir / spec_file
            if spec_path.exists():
                file_errors, file_warnings = self._validate_spec_file(spec_path)
                errors.extend(file_errors)
                warnings.extend(file_warnings)
                
                # Build traceability map
                traceability_map[spec_file] = self._build_traceability_map(spec_path)
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(errors, warnings)
        
        # Generate spec hash for change detection
        spec_hash = self._generate_spec_hash()
        
        return SpecValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            compliance_score=compliance_score,
            traceability_map=traceability_map,
            last_updated=datetime.now(),
            spec_hash=spec_hash
        )
    
    def _check_required_files(self) -> List[str]:
        """Check if all required spec files exist."""
        missing_files = []
        for required_file in self.validation_rules["required_spec_files"]:
            if not (self.specs_dir / required_file).exists():
                missing_files.append(required_file)
        return missing_files
    
    def _validate_spec_file(self, spec_path: Path) -> Tuple[List[str], List[str]]:
        """Validate a single spec file."""
        errors = []
        warnings = []
        
        try:
            content = spec_path.read_text(encoding='utf-8')
            file_name = spec_path.name
            
            # Check required sections
            required_sections = self.validation_rules["required_sections"].get(file_name, [])
            for section in required_sections:
                if section not in content:
                    errors.append(f"Missing required section '{section}' in {file_name}")
            
            # Check for TODO items (warnings)
            todo_count = content.count("[ ]")
            if todo_count > 10:
                warnings.append(f"High number of TODO items ({todo_count}) in {file_name}")
            
            # Check for completion status
            if "[ ]" in content and "✅" not in content:
                warnings.append(f"No completed items found in {file_name}")
                
        except Exception as e:
            errors.append(f"Error reading spec file {spec_path}: {str(e)}")
        
        return errors, warnings
    
    def _build_traceability_map(self, spec_path: Path) -> List[str]:
        """Build traceability map for a spec file."""
        related_files = []
        
        try:
            content = spec_path.read_text(encoding='utf-8')
            file_name = spec_path.stem
            
            # Find related code files based on spec content
            if "cli" in content.lower() or "command" in content.lower():
                related_files.extend(self._find_cli_files())
            
            if "validation" in content.lower():
                related_files.extend(self._find_validation_files())
            
            if "template" in content.lower():
                related_files.extend(self._find_template_files())
            
            if "test" in content.lower():
                related_files.extend(self._find_test_files())
                
        except Exception as e:
            print(f"Warning: Could not build traceability map for {spec_path}: {e}")
        
        return related_files
    
    def _find_cli_files(self) -> List[str]:
        """Find CLI-related files."""
        cli_files = []
        for pattern in ["**/cli/**/*.py", "**/commands/**/*.py"]:
            cli_files.extend([str(f) for f in self.project_root.glob(pattern)])
        return cli_files
    
    def _find_validation_files(self) -> List[str]:
        """Find validation-related files."""
        validation_files = []
        for pattern in ["**/validation*.py", "**/validator*.py"]:
            validation_files.extend([str(f) for f in self.project_root.glob(pattern)])
        return validation_files
    
    def _find_template_files(self) -> List[str]:
        """Find template-related files."""
        template_files = []
        for pattern in ["**/template*.py", "**/templates/**/*.j2"]:
            template_files.extend([str(f) for f in self.project_root.glob(pattern)])
        return template_files
    
    def _find_test_files(self) -> List[str]:
        """Find test files."""
        test_files = []
        for pattern in ["**/test_*.py", "**/tests/**/*.py"]:
            test_files.extend([str(f) for f in self.project_root.glob(pattern)])
        return test_files
    
    def _calculate_compliance_score(self, errors: List[str], warnings: List[str]) -> float:
        """Calculate compliance score based on errors and warnings."""
        total_issues = len(errors) + len(warnings)
        if total_issues == 0:
            return 100.0
        
        # Weight errors more heavily than warnings
        error_weight = 2.0
        warning_weight = 1.0
        
        weighted_score = (len(errors) * error_weight + len(warnings) * warning_weight)
        max_possible_issues = 20  # Assume max 20 issues for scoring
        
        score = max(0, 100 - (weighted_score / max_possible_issues) * 100)
        return round(score, 2)
    
    def _generate_spec_hash(self) -> str:
        """Generate hash of all spec files for change detection."""
        hasher = hashlib.md5()
        
        for spec_file in self.validation_rules["required_spec_files"]:
            spec_path = self.specs_dir / spec_file
            if spec_path.exists():
                hasher.update(spec_path.read_bytes())
        
        return hasher.hexdigest()
    
    def validate_spec_to_code_traceability(self) -> Dict[str, Any]:
        """
        Validate spec-to-code traceability.
        
        Returns:
            Dictionary with traceability validation results
        """
        results = {
            "total_specs": 0,
            "traced_specs": 0,
            "missing_traces": [],
            "traceability_score": 0.0
        }
        
        for spec_file in self.validation_rules["required_spec_files"]:
            spec_path = self.specs_dir / spec_file
            if spec_path.exists():
                results["total_specs"] += 1
                
                # Check if spec has corresponding code
                related_files = self._build_traceability_map(spec_path)
                if related_files:
                    results["traced_specs"] += 1
                else:
                    results["missing_traces"].append(spec_file)
        
        if results["total_specs"] > 0:
            results["traceability_score"] = (results["traced_specs"] / results["total_specs"]) * 100
        
        return results
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report.
        
        Returns:
            Dictionary with compliance report data
        """
        validation_result = self.validate_spec_compliance()
        traceability_result = self.validate_spec_to_code_traceability()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "validation": asdict(validation_result),
            "traceability": traceability_result,
            "overall_compliance": (validation_result.compliance_score + traceability_result["traceability_score"]) / 2,
            "recommendations": self._generate_recommendations(validation_result, traceability_result)
        }
    
    def _generate_recommendations(self, validation_result: SpecValidationResult, 
                                traceability_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if validation_result.compliance_score < 80:
            recommendations.append("Improve spec compliance by addressing errors and warnings")
        
        if traceability_result["traceability_score"] < 90:
            recommendations.append("Enhance spec-to-code traceability mapping")
        
        if validation_result.warnings:
            recommendations.append("Address spec warnings to improve quality")
        
        if traceability_result["missing_traces"]:
            recommendations.append(f"Add traceability for: {', '.join(traceability_result['missing_traces'])}")
        
        return recommendations


class SpecEvolutionTracker:
    """
    Tracks spec evolution and changes over time.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the spec evolution tracker."""
        self.project_root = project_root
        self.evolution_log = project_root / "assets" / "reports" / "spec_evolution.json"
    
    def track_spec_changes(self, current_hash: str) -> Dict[str, Any]:
        """
        Track changes in spec files.
        
        Args:
            current_hash: Current hash of spec files
            
        Returns:
            Dictionary with change tracking information
        """
        changes = {
            "timestamp": datetime.now().isoformat(),
            "current_hash": current_hash,
            "has_changes": False,
            "change_summary": []
        }
        
        if self.evolution_log.exists():
            try:
                with open(self.evolution_log, 'r') as f:
                    history = json.load(f)
                
                if history and "last_hash" in history:
                    if history["last_hash"] != current_hash:
                        changes["has_changes"] = True
                        changes["change_summary"].append("Spec files have been modified")
                
            except Exception as e:
                changes["change_summary"].append(f"Error reading evolution log: {e}")
        
        # Save current state
        self._save_evolution_state(changes)
        
        return changes
    
    def _save_evolution_state(self, changes: Dict[str, Any]) -> None:
        """Save current evolution state."""
        try:
            self.evolution_log.parent.mkdir(parents=True, exist_ok=True)
            
            evolution_data = {
                "last_updated": changes["timestamp"],
                "last_hash": changes["current_hash"],
                "change_history": changes.get("change_summary", [])
            }
            
            with open(self.evolution_log, 'w') as f:
                json.dump(evolution_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save evolution state: {e}")


def create_spec_validator(project_root: Path) -> SpecValidator:
    """
    Factory function to create a spec validator.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        Initialized SpecValidator instance
    """
    return SpecValidator(project_root)
