"""Evaluator module for applying validation operators to matched values."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .result import Diagnostic, Severity


class RuleEvaluator:
    """Evaluates validation rules against matched values."""
    
    def __init__(self, mode: str = "relaxed"):
        """Initialize evaluator with validation mode."""
        self.mode = mode
    
    def evaluate_rule(self, rule: Dict[str, Any], matches: List[Dict[str, Any]], spec_id: str, schema_version: int) -> List[Diagnostic]:
        """Evaluate a single rule against its matches."""
        diagnostics = []
        
        # Handle presence validation
        if "presence" in rule:
            presence_diags = self._evaluate_presence(rule, matches, spec_id, schema_version)
            diagnostics.extend(presence_diags)
        
        # Evaluate other operators on existing values
        for match in matches:
            value = match["value"]
            path = match["path"]
            
            # Skip if value is None and presence is optional
            if value is None and rule.get("presence") == "optional":
                continue
            
            # Evaluate type
            if "type" in rule:
                type_diag = self._evaluate_type(rule, value, path, spec_id, schema_version)
                if type_diag:
                    diagnostics.append(type_diag)
            
            # Evaluate enum
            if "enum" in rule:
                enum_diag = self._evaluate_enum(rule, value, path, spec_id, schema_version)
                if enum_diag:
                    diagnostics.append(enum_diag)
            
            # Evaluate const
            if "const" in rule:
                const_diag = self._evaluate_const(rule, value, path, spec_id, schema_version)
                if const_diag:
                    diagnostics.append(const_diag)
            
            # Evaluate numeric constraints
            if "min" in rule or "max" in rule:
                numeric_diag = self._evaluate_numeric(rule, value, path, spec_id, schema_version)
                if numeric_diag:
                    diagnostics.append(numeric_diag)
            
            # Evaluate string constraints
            if "minLength" in rule or "maxLength" in rule or "pattern" in rule or "format" in rule:
                string_diag = self._evaluate_string(rule, value, path, spec_id, schema_version)
                if string_diag:
                    diagnostics.append(string_diag)
            
            # Evaluate array constraints
            if "uniqueItems" in rule or "minItems" in rule or "maxItems" in rule:
                array_diag = self._evaluate_array(rule, value, path, spec_id, schema_version)
                if array_diag:
                    diagnostics.append(array_diag)
            
            # Evaluate items/properties
            if "items" in rule or "properties" in rule:
                nested_diag = self._evaluate_nested(rule, value, path, spec_id, schema_version)
                if nested_diag:
                    diagnostics.append(nested_diag)
            
            # Evaluate dependent required
            if "dependentRequired" in rule:
                dep_diag = self._evaluate_dependent_required(rule, value, path, spec_id, schema_version)
                if dep_diag:
                    diagnostics.append(dep_diag)
            
            # Evaluate compare
            if "compare" in rule:
                compare_diag = self._evaluate_compare(rule, value, path, spec_id, schema_version)
                if compare_diag:
                    diagnostics.append(compare_diag)
        
        return diagnostics
    
    def _evaluate_presence(self, rule: Dict[str, Any], matches: List[Dict[str, Any]], spec_id: str, schema_version: int) -> List[Diagnostic]:
        """Evaluate presence constraints."""
        diagnostics = []
        presence = rule["presence"]
        
        if presence == "required" and not matches:
            diagnostics.append(Diagnostic(
                code="REQUIRED_FIELD_MISSING",
                severity=Severity.ERROR,
                message=rule.get("message", f"Required field missing"),
                path=rule["path"],
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            ))
        elif presence == "forbidden" and matches:
            diagnostics.append(Diagnostic(
                code="FORBIDDEN_FIELD_PRESENT",
                severity=Severity.ERROR,
                message=rule.get("message", f"Forbidden field present"),
                path=rule["path"],
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            ))
        
        return diagnostics
    
    def _evaluate_type(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate type constraints."""
        expected_type = rule["type"]
        
        # Handle type references
        if isinstance(expected_type, dict):
            expected_type = expected_type.get("type", "string")
        
        actual_type = self._get_python_type(value)
        
        if actual_type != expected_type:
            severity = self._get_severity(rule, "TYPE_MISMATCH")
            return Diagnostic(
                code="TYPE_MISMATCH",
                severity=severity,
                message=rule.get("message", f"Expected {expected_type}, got {actual_type}"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        return None
    
    def _evaluate_enum(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate enum constraints."""
        allowed_values = rule["enum"]
        
        if value not in allowed_values:
            severity = self._get_severity(rule, "INVALID_ENUM_VALUE")
            return Diagnostic(
                code="INVALID_ENUM_VALUE",
                severity=severity,
                message=rule.get("message", f"Value must be one of: {', '.join(map(str, allowed_values))}"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        return None
    
    def _evaluate_const(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate const constraints."""
        expected_value = rule["const"]
        
        if value != expected_value:
            severity = self._get_severity(rule, "CONST_MISMATCH")
            return Diagnostic(
                code="CONST_MISMATCH",
                severity=severity,
                message=rule.get("message", f"Value must be exactly: {expected_value}"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        return None
    
    def _evaluate_numeric(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate numeric constraints."""
        if not isinstance(value, (int, float)):
            return None
        
        if "min" in rule and value < rule["min"]:
            severity = self._get_severity(rule, "VALUE_TOO_SMALL")
            return Diagnostic(
                code="VALUE_TOO_SMALL",
                severity=severity,
                message=rule.get("message", f"Value must be >= {rule['min']}"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        if "max" in rule and value > rule["max"]:
            severity = self._get_severity(rule, "VALUE_TOO_LARGE")
            return Diagnostic(
                code="VALUE_TOO_LARGE",
                severity=severity,
                message=rule.get("message", f"Value must be <= {rule['max']}"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        return None
    
    def _evaluate_string(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate string constraints."""
        if not isinstance(value, str):
            return None
        
        if "minLength" in rule and len(value) < rule["minLength"]:
            severity = self._get_severity(rule, "STRING_TOO_SHORT")
            return Diagnostic(
                code="STRING_TOO_SHORT",
                severity=severity,
                message=rule.get("message", f"String must be at least {rule['minLength']} characters"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        if "maxLength" in rule and len(value) > rule["maxLength"]:
            severity = self._get_severity(rule, "STRING_TOO_LONG")
            return Diagnostic(
                code="STRING_TOO_LONG",
                severity=severity,
                message=rule.get("message", f"String must be at most {rule['maxLength']} characters"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        if "pattern" in rule:
            # Pattern validation: check if value matches the regex pattern
            pattern = rule["pattern"]
            try:
                # For negative lookahead patterns, use case-insensitive matching
                # Pattern like ^((?!laser|plasma|railgun).)*$ matches if forbidden words are NOT found
                if pattern.startswith("^") and pattern.endswith("$"):
                    # Anchored pattern - use match with case-insensitive flag
                    matches_pattern = bool(re.match(pattern, value, re.IGNORECASE))
                else:
                    # Unanchored pattern - use search with case-insensitive flag
                    matches_pattern = bool(re.search(pattern, value, re.IGNORECASE))
                
                if not matches_pattern:
                    severity = self._get_severity(rule, "PATTERN_MISMATCH")
                    return Diagnostic(
                        code="PATTERN_MISMATCH",
                        severity=severity,
                        message=rule.get("message", f"String does not match required pattern"),
                        path=path,
                        rule=rule,
                        spec_id=spec_id,
                        schema_version=schema_version
                    )
            except re.error:
                # Invalid regex pattern - skip validation
                pass
        
        if "format" in rule:
            format_diag = self._evaluate_format(rule, value, path, spec_id, schema_version)
            if format_diag:
                return format_diag
        
        return None
    
    def _evaluate_format(self, rule: Dict[str, Any], value: str, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate format constraints."""
        format_type = rule["format"]
        
        if format_type == "email":
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                severity = self._get_severity(rule, "INVALID_EMAIL_FORMAT")
                return Diagnostic(
                    code="INVALID_EMAIL_FORMAT",
                    severity=severity,
                    message=rule.get("message", "Invalid email format"),
                    path=path,
                    rule=rule,
                    spec_id=spec_id,
                    schema_version=schema_version
                )
        
        elif format_type == "url":
            url_pattern = r'^https?://.+'
            if not re.match(url_pattern, value):
                severity = self._get_severity(rule, "INVALID_URL_FORMAT")
                return Diagnostic(
                    code="INVALID_URL_FORMAT",
                    severity=severity,
                    message=rule.get("message", "Invalid URL format"),
                    path=path,
                    rule=rule,
                    spec_id=spec_id,
                    schema_version=schema_version
                )
        
        # Add more format validations as needed
        
        return None
    
    def _evaluate_array(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate array constraints."""
        if not isinstance(value, list):
            return None
        
        if "minItems" in rule and len(value) < rule["minItems"]:
            severity = self._get_severity(rule, "ARRAY_TOO_SHORT")
            return Diagnostic(
                code="ARRAY_TOO_SHORT",
                severity=severity,
                message=rule.get("message", f"Array must have at least {rule['minItems']} items"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        if "maxItems" in rule and len(value) > rule["maxItems"]:
            severity = self._get_severity(rule, "ARRAY_TOO_LONG")
            return Diagnostic(
                code="ARRAY_TOO_LONG",
                severity=severity,
                message=rule.get("message", f"Array must have at most {rule['maxItems']} items"),
                path=path,
                rule=rule,
                spec_id=spec_id,
                schema_version=schema_version
            )
        
        if "uniqueItems" in rule and rule["uniqueItems"]:
            if len(value) != len(set(value)):
                severity = self._get_severity(rule, "ARRAY_NOT_UNIQUE")
                return Diagnostic(
                    code="ARRAY_NOT_UNIQUE",
                    severity=severity,
                    message=rule.get("message", "Array items must be unique"),
                    path=path,
                    rule=rule,
                    spec_id=spec_id,
                    schema_version=schema_version
                )
        
        return None
    
    def _evaluate_nested(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate nested object/array constraints."""
        # This is a simplified implementation
        # In a full implementation, you'd recursively evaluate items/properties
        return None
    
    def _evaluate_dependent_required(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate dependent required constraints."""
        # This is a simplified implementation
        # In a full implementation, you'd check if required fields are present
        return None
    
    def _evaluate_compare(self, rule: Dict[str, Any], value: Any, path: str, spec_id: str, schema_version: int) -> Optional[Diagnostic]:
        """Evaluate comparison constraints."""
        compare = rule["compare"]
        
        # This is a simplified implementation
        # In a full implementation, you'd compare values based on the comparison type
        return None
    
    def _get_python_type(self, value: Any) -> str:
        """Get the Python type name for a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "unknown"
    
    def _get_severity(self, rule: Dict[str, Any], default_code: str) -> Severity:
        """Get the severity for a diagnostic."""
        if "severity" in rule:
            return Severity(rule["severity"])
        
        # Default severity based on mode
        if self.mode == "strict":
            return Severity.ERROR
        else:
            return Severity.WARNING
