"""Loader module for parsing OCD validation specs and character files."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jsonschema import Draft202012Validator, ValidationError as JSONSchemaValidationError

from .yaml_loader import safe_load


class SpecLoader:
    """Loads and validates OCD validation specification files."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize with optional custom schema path."""
        self.schema_path = schema_path or "schema/ocd-validation-spec.schema.json"
        self._schema_validator: Optional[Draft202012Validator] = None
    
    def _load_schema_validator(self) -> Draft202012Validator:
        """Load and cache the JSON schema validator."""
        if self._schema_validator is None:
            # Try to load schema from installed package data first
            schema_data = None
            try:
                with resources.files("ocd.validate.data").joinpath("ocd-validation-spec.schema.json").open("r", encoding="utf-8") as f:
                    schema_data = json.load(f)
            except (ImportError, FileNotFoundError, ModuleNotFoundError):
                # Fall back to development location
                schema_path = Path(self.schema_path)
                if not schema_path.exists() or not schema_path.is_absolute():
                    # Try relative to current file
                    # From tools/python/src/ocd/validate/loader.py, go up 6 levels to project root
                    schema_path = Path(__file__).parent.parent.parent.parent.parent.parent / "schema" / "ocd-validation-spec.schema.json"
                
                if schema_path.exists():
                    with schema_path.open("r", encoding="utf-8") as f:
                        schema_data = json.load(f)
            
            if schema_data is None:
                raise FileNotFoundError("Could not find ocd-validation-spec.schema.json in package or development paths")
            
            self._schema_validator = Draft202012Validator(schema_data)
        
        return self._schema_validator
    
    def load_spec(self, spec_path: str) -> Dict[str, Any]:
        """Load and validate a .ocd specification file."""
        path = Path(spec_path)
        if not path.exists() and not path.is_absolute():
            # Try relative to project root
            # From tools/python/src/ocd/validate/loader.py, go up 6 levels to project root
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            path = project_root / spec_path
        if not path.exists():
            raise FileNotFoundError(f"Specification file not found: {spec_path}")
        
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse YAML/JSON
        try:
            spec = safe_load(content)
        except Exception as e:
            raise ValueError(f"Failed to parse specification file: {e}")
        
        # Validate against schema
        validator = self._load_schema_validator()
        try:
            validator.validate(spec)
        except JSONSchemaValidationError as e:
            raise ValueError(f"Specification validation failed: {e.message}")
        
        return spec
    
    def load_character(self, character_path: str) -> Dict[str, Any]:
        """Load a character file (YAML or JSON)."""
        path = Path(character_path)
        if not path.exists() and not path.is_absolute():
            # Try relative to project root
            # From tools/python/src/ocd/validate/loader.py, go up 6 levels to project root
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            path = project_root / character_path
        if not path.exists():
            raise FileNotFoundError(f"Character file not found: {character_path}")
        
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse YAML/JSON
        try:
            return safe_load(content)
        except Exception as e:
            raise ValueError(f"Failed to parse character file: {e}")
    
    def resolve_extends(self, spec: Dict[str, Any], base_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """Resolve extends references in a specification. Returns list of base specs."""
        if "extends" not in spec:
            return []
        
        if base_dir is None:
            # Try to find project root
            # From tools/python/src/ocd/validate/loader.py, go up 6 levels to project root
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            base_dir = str(project_root)
        
        extended_specs = []
        
        for extend_id in spec["extends"]:
            # Look for spec file with matching ID
            spec_file = self._find_spec_by_id(extend_id, base_dir)
            if spec_file:
                extended_spec = self.load_spec(spec_file)
                # Recursively resolve extends for this base spec
                base_specs = self.resolve_extends(extended_spec, base_dir)
                extended_specs.extend(base_specs)
                extended_specs.append(extended_spec)
            else:
                raise ValueError(f"Could not find specification with ID: {extend_id}")
        
        return extended_specs
    
    def _find_spec_by_id(self, spec_id: str, base_dir: str) -> Optional[str]:
        """Find a specification file by its ID."""
        base_path = Path(base_dir)
        
        # Look in common locations relative to base_dir
        search_paths = [
            base_path / "tests" / "specs",
            base_path / "specs",
            base_path / "spec",
        ]
        
        # Also try looking from project root
        # From tools/python/src/ocd/validate/loader.py, go up 6 levels to project root
        project_root = Path(__file__).parent.parent.parent.parent.parent.parent
        search_paths.extend([
            project_root / "tests" / "specs",
            project_root / "specs",
            project_root / "spec",
        ])
        
        for search_path in search_paths:
            if search_path.exists():
                for spec_file in search_path.glob("*.ocd"):
                    try:
                        # Use absolute path to avoid resolution issues
                        abs_spec_file = spec_file.resolve()
                        spec = self.load_spec(str(abs_spec_file))
                        if spec.get("id") == spec_id:
                            return str(abs_spec_file)
                    except Exception:
                        continue
        
        return None
