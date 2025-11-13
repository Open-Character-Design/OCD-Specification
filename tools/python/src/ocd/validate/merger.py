"""Merger module for combining OCD validation specifications."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Set


class SpecMerger:
    """Merges OCD validation specifications with proper inheritance."""
    
    def merge_specs(self, base_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple specifications, with later specs overriding earlier ones."""
        if not base_specs:
            raise ValueError("At least one specification must be provided")
        
        merged = base_specs[0].copy()
        
        for spec in base_specs[1:]:
            merged = self._merge_single(merged, spec)
        
        return merged
    
    def _merge_single(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Merge a single overlay specification into the base."""
        merged = base.copy()
        
        # Merge metadata
        if "metadata" in overlay:
            merged["metadata"] = self._deep_merge(
                merged.get("metadata", {}), 
                overlay["metadata"]
            )
        
        # Merge policy
        if "policy" in overlay:
            merged["policy"] = self._deep_merge(
                merged.get("policy", {}), 
                overlay["policy"]
            )
        
        # Merge definitions
        if "definitions" in overlay:
            merged["definitions"] = self._merge_definitions(
                merged.get("definitions", {}), 
                overlay["definitions"]
            )
        
        # Merge rules with de-duplication
        if "rules" in overlay:
            merged["rules"] = self._merge_rules(
                merged.get("rules", []), 
                overlay["rules"]
            )
        
        # Merge constraints
        if "constraints" in overlay:
            merged["constraints"] = self._merge_constraints(
                merged.get("constraints", {}), 
                overlay["constraints"]
            )
        
        return merged
    
    def _deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _merge_definitions(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Merge definitions sections."""
        merged = base.copy()
        
        for section in ["enums", "types", "patterns"]:
            if section in overlay:
                if section in merged:
                    merged[section] = self._deep_merge(merged[section], overlay[section])
                else:
                    merged[section] = overlay[section].copy()
        
        return merged
    
    def _merge_rules(self, base_rules: List[Dict[str, Any]], overlay_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge rules with de-duplication by path (child rules override parent rules for same path)."""
        # Create lookup for base rules by path
        base_rules_by_path = {}
        for rule in base_rules:
            path = rule.get("path", "")
            # If multiple base rules have same path, keep the last one
            base_rules_by_path[path] = rule
        
        # Process overlay rules - these override base rules with same path
        merged_rules = []
        overlay_paths: Set[str] = set()
        
        for rule in overlay_rules:
            path = rule.get("path", "")
            overlay_paths.add(path)
            merged_rules.append(rule)
        
        # Add base rules that weren't overridden (different path)
        for rule in base_rules:
            path = rule.get("path", "")
            if path not in overlay_paths:
                merged_rules.append(rule)
        
        return merged_rules
    
    def _rule_key(self, rule: Dict[str, Any]) -> str:
        """Generate a unique key for a rule based on path and operator keys."""
        path = rule.get("path", "")
        
        # Get all operator keys (excluding path, message, severity)
        operator_keys = []
        for key in rule.keys():
            if key not in ["path", "message", "severity"]:
                operator_keys.append(key)
        
        operator_keys.sort()
        operator_hash = hashlib.md5(str(operator_keys).encode()).hexdigest()[:8]
        
        return f"{path}:{operator_hash}"
    
    def _merge_constraints(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Merge constraints sections."""
        merged = base.copy()
        
        for constraint_type in ["require", "forbid", "disallow", "arrays"]:
            if constraint_type in overlay:
                if constraint_type in merged:
                    if constraint_type == "arrays":
                        # Special handling for arrays constraints
                        merged[constraint_type] = self._merge_array_constraints(
                            merged[constraint_type], 
                            overlay[constraint_type]
                        )
                    else:
                        # For require/forbid/disallow, overlay replaces base
                        merged[constraint_type] = overlay[constraint_type]
                else:
                    merged[constraint_type] = overlay[constraint_type]
        
        return merged
    
    def _merge_array_constraints(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Merge array constraints."""
        merged = base.copy()
        
        for array_type in ["unique", "minItems", "maxItems"]:
            if array_type in overlay:
                if array_type in merged:
                    # Combine arrays
                    merged[array_type] = merged[array_type] + overlay[array_type]
                else:
                    merged[array_type] = overlay[array_type]
        
        return merged
    
    def resolve_references(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve @enums.Name and @types.Name references in rules."""
        resolved_spec = spec.copy()
        
        if "rules" in resolved_spec:
            resolved_spec["rules"] = [
                self._resolve_rule_references(rule, spec.get("definitions", {}))
                for rule in resolved_spec["rules"]
            ]
        
        return resolved_spec
    
    def _resolve_rule_references(self, rule: Dict[str, Any], definitions: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve references in a single rule."""
        resolved_rule = rule.copy()
        
        # Resolve enum references
        if "enum" in rule and isinstance(rule["enum"], str) and rule["enum"].startswith("@enums."):
            enum_name = rule["enum"][7:]  # Remove "@enums." prefix
            enums = definitions.get("enums", {})
            if enum_name in enums:
                resolved_rule["enum"] = enums[enum_name]
            else:
                raise ValueError(f"Enum reference not found: {rule['enum']}")
        
        # Resolve type references
        if "type" in rule and isinstance(rule["type"], str) and rule["type"].startswith("@types."):
            type_name = rule["type"][7:]  # Remove "@types." prefix
            types = definitions.get("types", {})
            if type_name in types:
                resolved_rule["type"] = types[type_name]
            else:
                raise ValueError(f"Type reference not found: {rule['type']}")
        
        return resolved_rule
