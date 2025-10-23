"""Matcher module for compiling rule path selectors."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Union

from jsonpath_ng import JSONPath, parse


class PathMatcher:
    """Compiles and executes path selectors for OCD validation rules."""
    
    def __init__(self):
        """Initialize the path matcher."""
        self._compiled_paths: Dict[str, JSONPath] = {}
    
    def compile_path(self, path: str) -> JSONPath:
        """Compile a path selector to JSONPath."""
        if path not in self._compiled_paths:
            # Convert OCD path syntax to JSONPath
            jsonpath_str = self._convert_to_jsonpath(path)
            self._compiled_paths[path] = parse(jsonpath_str)
        
        return self._compiled_paths[path]
    
    def _convert_to_jsonpath(self, path: str) -> str:
        """Convert OCD path syntax to JSONPath syntax."""
        # Handle root path
        if path == "" or path == ".":
            return "$"
        
        # Split by dots and process each segment
        segments = path.split(".")
        jsonpath_segments = ["$"]
        
        for segment in segments:
            if segment == "":
                continue
            
            # Handle array notation
            if "[]" in segment:
                # Convert "field[]" to "field[*]"
                segment = segment.replace("[]", "[*]")
            
            # Handle wildcard arrays
            if segment == "[*]":
                jsonpath_segments.append("[*]")
            elif segment.endswith("[*]"):
                field_name = segment[:-3]
                jsonpath_segments.append(f".{field_name}[*]")
            elif segment.endswith("[]"):
                field_name = segment[:-2]
                jsonpath_segments.append(f".{field_name}[*]")
            else:
                jsonpath_segments.append(f".{segment}")
        
        return "".join(jsonpath_segments)
    
    def find_matches(self, document: Any, path: str) -> List[Dict[str, Any]]:
        """Find all values matching the given path in the document."""
        try:
            compiled_path = self.compile_path(path)
            matches = compiled_path.find(document)
            
            return [
                {
                    "value": match.value,
                    "path": str(match.full_path),
                    "context": self._get_context(document, match.full_path)
                }
                for match in matches
            ]
        except Exception as e:
            # If path matching fails, return empty list
            return []
    
    def _get_context(self, document: Any, full_path: JSONPath) -> Dict[str, Any]:
        """Get context information for a matched value."""
        context = {}
        
        try:
            # Get parent object
            if len(full_path.path) > 1:
                parent_path = JSONPath(full_path.path[:-1])
                parent_matches = parent_path.find(document)
                if parent_matches:
                    context["parent"] = parent_matches[0].value
        except Exception:
            pass
        
        return context
    
    def path_exists(self, document: Any, path: str) -> bool:
        """Check if a path exists in the document."""
        matches = self.find_matches(document, path)
        return len(matches) > 0
    
    def get_value_at_path(self, document: Any, path: str) -> Optional[Any]:
        """Get the value at a specific path (returns first match)."""
        matches = self.find_matches(document, path)
        return matches[0]["value"] if matches else None
    
    def validate_path_syntax(self, path: str) -> bool:
        """Validate that a path has correct syntax."""
        try:
            self.compile_path(path)
            return True
        except Exception:
            return False
    
    def get_path_info(self, path: str) -> Dict[str, Any]:
        """Get information about a path selector."""
        try:
            compiled_path = self.compile_path(path)
            return {
                "original": path,
                "jsonpath": str(compiled_path),
                "is_array_path": "[*]" in str(compiled_path) or "[]" in path,
                "is_wildcard": path.endswith("[*]") or path.endswith("[]"),
                "segments": path.split(".") if path else []
            }
        except Exception as e:
            return {
                "original": path,
                "error": str(e),
                "valid": False
            }
