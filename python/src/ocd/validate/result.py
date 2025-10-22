"""Result module for diagnostic data structures and formatting."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class Severity(Enum):
    """Diagnostic severity levels."""
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Diagnostic:
    """A single validation diagnostic."""
    code: str
    severity: Severity
    message: str
    path: str
    rule: Dict[str, Any]
    spec_id: str
    schema_version: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnostic to dictionary."""
        result = asdict(self)
        result["severity"] = self.severity.value
        return result


@dataclass
class ValidationResult:
    """Complete validation result."""
    ok: bool
    diagnostics: List[Diagnostic]
    data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "ok": self.ok,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "data": self.data
        }
    
    def get_errors(self) -> List[Diagnostic]:
        """Get all error diagnostics."""
        return [diag for diag in self.diagnostics if diag.severity == Severity.ERROR]
    
    def get_warnings(self) -> List[Diagnostic]:
        """Get all warning diagnostics."""
        return [diag for diag in self.diagnostics if diag.severity == Severity.WARNING]
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.get_errors()) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.get_warnings()) > 0


class ResultFormatter:
    """Formats validation results for different output formats."""
    
    @staticmethod
    def format_text(result: ValidationResult) -> str:
        """Format result as human-readable text."""
        if result.ok:
            if result.has_warnings():
                return f"Validation succeeded with {len(result.get_warnings())} warning(s)."
            else:
                return "Validation succeeded."
        else:
            errors = result.get_errors()
            warnings = result.get_warnings()
            
            lines = []
            if errors:
                lines.append(f"Validation failed with {len(errors)} error(s):")
                for error in errors:
                    lines.append(f"  - {error.path}: {error.message}")
            
            if warnings:
                lines.append(f"Validation produced {len(warnings)} warning(s):")
                for warning in warnings:
                    lines.append(f"  - {warning.path}: {warning.message}")
            
            return "\n".join(lines)
    
    @staticmethod
    def format_json(result: ValidationResult) -> str:
        """Format result as JSON."""
        return json.dumps(result.to_dict(), indent=2)
    
    @staticmethod
    def format_summary(result: ValidationResult) -> str:
        """Format a brief summary of the result."""
        if result.ok:
            if result.has_warnings():
                return f"✅ Validation passed with {len(result.get_warnings())} warning(s)"
            else:
                return "✅ Validation passed"
        else:
            errors = result.get_errors()
            warnings = result.get_warnings()
            summary = f"❌ Validation failed with {len(errors)} error(s)"
            if warnings:
                summary += f" and {len(warnings)} warning(s)"
            return summary
