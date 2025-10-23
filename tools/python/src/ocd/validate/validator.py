"""Main validator module using the new OCD validation spec pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence

from .loader import SpecLoader
from .merger import SpecMerger
from .matcher import PathMatcher
from .evaluator import RuleEvaluator
from .result import Diagnostic, ValidationResult, ResultFormatter, Severity
from .normalizer import normalize_in_place
from .linter import lint


def validate_and_normalize(
    doc: Any, 
    mode: Literal["relaxed", "strict"] = "relaxed",
    spec_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate and normalize an OCD document using the new validation spec system.
    
    Args:
        doc: The document to validate
        mode: Validation mode - "relaxed" for warnings, "strict" for errors
        spec_path: Optional path to custom OCD specification overlay
        
    Returns:
        Dictionary with validation results
    """
    try:
        # Load specifications
        loader = SpecLoader()
        specs_to_merge = []
        
        # Load custom spec if provided
        if spec_path:
            custom_spec = loader.load_spec(spec_path)
            specs_to_merge.append(custom_spec)
        else:
            # Load default spec only if no custom spec provided
            default_spec_path = Path(__file__).parent.parent.parent.parent.parent / "spec" / "ocd-default-spec.ocd"
            if not default_spec_path.exists():
                # Try tests directory
                default_spec_path = Path(__file__).parent.parent.parent.parent.parent / "tests" / "specs" / "ocd-default-spec.ocd"
            
            if not default_spec_path.exists():
                return {
                    "ok": False, 
                    "errors": [{"loc": ("spec",), "msg": "Default specification not found", "type": "spec_error"}]
                }
            
            specs_to_merge.append(loader.load_spec(str(default_spec_path)))
        
        # Merge specifications
        merger = SpecMerger()
        merged_spec = merger.merge_specs(specs_to_merge)
        resolved_spec = merger.resolve_references(merged_spec)
        
        # Initialize components
        matcher = PathMatcher()
        evaluator = RuleEvaluator(mode)
        
        # Collect diagnostics
        all_diagnostics: List[Diagnostic] = []
        
        # Evaluate rules
        if "rules" in resolved_spec:
            for rule in resolved_spec["rules"]:
                matches = matcher.find_matches(doc, rule["path"])
                rule_diagnostics = evaluator.evaluate_rule(
                    rule, matches, resolved_spec.get("id", "unknown"), resolved_spec.get("schemaVersion", 1)
                )
                all_diagnostics.extend(rule_diagnostics)
        
        # Evaluate constraints
        if "constraints" in resolved_spec:
            constraint_diagnostics = _evaluate_constraints(
                resolved_spec["constraints"], doc, matcher, evaluator, resolved_spec.get("id", "unknown"), resolved_spec.get("schemaVersion", 1)
            )
            all_diagnostics.extend(constraint_diagnostics)
        
        # Determine if validation passed
        errors = [d for d in all_diagnostics if d.severity == Severity.ERROR]
        warnings = [d for d in all_diagnostics if d.severity == Severity.WARNING]
        
        validation_passed = len(errors) == 0
        
        # Normalize data if validation passed
        normalized_data = None
        if validation_passed:
            normalized_data = json.loads(json.dumps(doc))  # Deep copy
            normalize_warnings = []
            normalize_in_place(normalized_data, normalize_warnings)
            
            # Convert normalize warnings to diagnostics
            for warning in normalize_warnings:
                all_diagnostics.append(Diagnostic(
                    code=warning.get("code", "NORMALIZATION_WARNING"),
                    severity=Severity.WARNING,
                    message=warning.get("detail", warning.get("msg", "Normalization warning")),
                    path=warning.get("path", "<root>"),
                    rule={},
                    spec_id=resolved_spec.get("id", "unknown"),
                    schema_version=resolved_spec.get("schemaVersion", 1)
                ))
            
            # Add linter warnings
            linter_warnings = lint(normalized_data)
            for warning in linter_warnings:
                all_diagnostics.append(Diagnostic(
                    code=warning.get("code", "LINT_WARNING"),
                    severity=Severity.WARNING,
                    message=warning.get("detail", warning.get("msg", "Lint warning")),
                    path=warning.get("path", "<root>"),
                    rule={},
                    spec_id=resolved_spec.get("id", "unknown"),
                    schema_version=resolved_spec.get("schemaVersion", 1)
                ))
        
        # Convert to legacy format for compatibility
        result = {
            "ok": validation_passed,
            "data": normalized_data,
            "errors": [{"loc": (d.path,), "msg": d.message, "type": d.code} for d in errors],
            "warnings": [{"path": d.path, "detail": d.message, "code": d.code} for d in warnings]
        }
        
        return result
        
    except Exception as exc:
        return {
            "ok": False, 
            "errors": [{"loc": ("validation",), "msg": str(exc), "type": "validation_error"}]
        }


def _evaluate_constraints(
    constraints: Dict[str, Any], 
    doc: Any, 
    matcher: PathMatcher, 
    evaluator: RuleEvaluator,
    spec_id: str,
    schema_version: int
) -> List[Diagnostic]:
    """Evaluate constraint rules."""
    diagnostics = []
    
    # Evaluate require constraints
    if "require" in constraints:
        for req in constraints["require"]:
            if isinstance(req, str):
                path = req
            elif isinstance(req, dict) and "path" in req:
                path = req["path"]
            else:
                continue
            
            if not matcher.path_exists(doc, path):
                diagnostics.append(Diagnostic(
                    code="REQUIRED_CONSTRAINT_MISSING",
                    severity=Severity.ERROR,
                    message=f"Required path missing: {path}",
                    path=path,
                    rule={"path": path, "presence": "required"},
                    spec_id=spec_id,
                    schema_version=schema_version
                ))
    
    # Evaluate forbid constraints
    if "forbid" in constraints:
        for forbid in constraints["forbid"]:
            if isinstance(forbid, str):
                path = forbid
            elif isinstance(forbid, dict) and "path" in forbid:
                path = forbid["path"]
            else:
                continue
            
            if matcher.path_exists(doc, path):
                diagnostics.append(Diagnostic(
                    code="FORBIDDEN_CONSTRAINT_PRESENT",
                    severity=Severity.ERROR,
                    message=f"Forbidden path present: {path}",
                    path=path,
                    rule={"path": path, "presence": "forbidden"},
                    spec_id=spec_id,
                    schema_version=schema_version
                ))
    
    # Evaluate disallow constraints
    if "disallow" in constraints:
        disallow = constraints["disallow"]
        if "tags" in disallow:
            forbidden_tags = disallow["tags"]
            tag_matches = matcher.find_matches(doc, "meta.tags")
            
            for match in tag_matches:
                if isinstance(match["value"], list):
                    for tag in match["value"]:
                        if tag in forbidden_tags:
                            diagnostics.append(Diagnostic(
                                code="DISALLOWED_TAG",
                                severity=Severity.ERROR,
                                message=f"Tag \"{tag}\" not allowed",
                                path=match["path"],
                                rule={"path": match["path"], "disallow": {"tags": forbidden_tags}},
                                spec_id=spec_id,
                                schema_version=schema_version
                            ))
    
    return diagnostics


def _parse_document(text: str, format_hint: str, source: str) -> Any:
    """Parse document text as JSON or YAML."""
    if format_hint == "json":
        return json.loads(text)
    if format_hint == "yaml":
        from .yaml_loader import safe_load
        return safe_load(text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            from .yaml_loader import safe_load
            return safe_load(text)
        except Exception as exc:
            raise ValueError(f"failed to parse '{source}' as JSON or YAML") from exc


def _format_location(location: Sequence[Any] | None) -> str:
    """Format location for display."""
    if not location:
        return "<root>"
    return ".".join(str(part) for part in location)


def _print_errors(errors: List[Dict[str, Any]]) -> None:
    """Print error messages."""
    if not errors:
        return

    print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
    for error in errors:
        loc = _format_location(error.get("loc"))
        msg = error.get("msg") or "validation error"
        print(f"  - {loc}: {msg}", file=sys.stderr)


def _print_warnings(warnings: List[Dict[str, Any]]) -> None:
    """Print warning messages."""
    if not warnings:
        return

    print(f"Validation produced {len(warnings)} warning(s):", file=sys.stderr)
    for warning in warnings:
        loc = warning.get("path") or warning.get("loc") or "<root>"
        detail = warning.get("detail") or warning.get("msg") or "warning"
        code = warning.get("code")
        prefix = f"[{code}] " if code else ""
        print(f"  - {loc}: {prefix}{detail}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate and normalize an Open Character Design Specification document",
    )
    parser.add_argument(
        "path",
        help="Path to an OCD document (YAML or JSON). Use '-' to read from standard input.",
    )
    parser.add_argument(
        "--format",
        choices=("auto", "json", "yaml"),
        default="auto",
        help="Force the input parser. Defaults to 'auto'.",
    )
    parser.add_argument(
        "--mode",
        choices=("relaxed", "strict"),
        default="relaxed",
        help="Validation mode: 'relaxed' for warnings, 'strict' for errors (default: relaxed).",
    )
    parser.add_argument(
        "--spec",
        help="Path to custom OCD specification overlay file.",
    )
    parser.add_argument(
        "--print",
        dest="print_normalized",
        action="store_true",
        help="Print the normalized document to stdout on success.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indent level to use when printing normalized JSON (default: 2).",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Exit with code 2 if any warnings are produced.",
    )
    parser.add_argument(
        "--output",
        choices=("text", "json"),
        default="text",
        help="Output format: 'text' for human-readable, 'json' for machine-readable diagnostics.",
    )

    args = parser.parse_args(argv)

    if args.indent < 0:
        parser.error("--indent must be non-negative")

    raw_text: str
    source = "stdin" if args.path == "-" else args.path
    try:
        if args.path == "-":
            raw_text = sys.stdin.read()
        else:
            raw_text = Path(args.path).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Failed to read {source}: {exc}", file=sys.stderr)
        return 2

    try:
        document = _parse_document(raw_text, args.format, source)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    result = validate_and_normalize(document, mode=args.mode, spec_path=args.spec)
    
    if args.output == "json":
        # JSON output: just diagnostics
        output = {
            "ok": result.get("ok", False),
            "errors": result.get("errors", []),
            "warnings": result.get("warnings", [])
        }
        json.dump(output, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0 if result.get("ok") else 1
    else:
        # Text output (existing behavior)
        if not result.get("ok"):
            _print_errors(result.get("errors", []))
            return 1
        
        warnings = result.get("warnings", [])
        if warnings:
            _print_warnings(warnings)
            if args.warnings_as_errors:
                return 2
        
        if args.print_normalized:
            indent = args.indent if args.indent > 0 else None
            json.dump(result.get("data"), sys.stdout, indent=indent)
            sys.stdout.write("\n")
        else:
            print("Validation succeeded.")
        
        return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())