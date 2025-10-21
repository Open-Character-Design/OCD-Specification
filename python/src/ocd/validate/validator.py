from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence, Tuple

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError
from pydantic import ValidationError

from .models import CharacterDefinition, CharacterInstance
from .normalizer import normalize_in_place
from .linter import lint
from .yaml_loader import safe_load

_CORE_SCHEMA_VALIDATOR: Draft202012Validator | None = None
_DEFAULT_SPEC: Dict[str, Any] | None = None


def _load_core_schema_validator() -> Draft202012Validator:
    global _CORE_SCHEMA_VALIDATOR
    if _CORE_SCHEMA_VALIDATOR is None:
        schema = _load_core_schema()
        _CORE_SCHEMA_VALIDATOR = Draft202012Validator(schema)
    return _CORE_SCHEMA_VALIDATOR


def _load_core_schema() -> Dict[str, Any]:
    """Load the bundled core schema, falling back to the repository copy."""

    candidate_paths: Iterable[Path] = (
        Path(__file__).resolve().parent / "data" / "core.schema.json",
        Path(__file__).resolve().parents[3] / "spec" / "core.schema.json",
    )

    last_error: Exception | None = None
    for path in candidate_paths:
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError as exc:
            last_error = exc
            continue

    message = "could not locate bundled core.schema.json"
    if last_error is not None:
        raise FileNotFoundError(message) from last_error
    raise FileNotFoundError(message)


def _load_default_spec() -> Dict[str, Any]:
    """Load the bundled default OCD specification."""
    global _DEFAULT_SPEC
    if _DEFAULT_SPEC is None:
        candidate_paths: Iterable[Path] = (
            Path(__file__).resolve().parents[3] / "spec" / "ocd-default-spec.ocd",
            Path(__file__).resolve().parents[3] / "docs" / "examples" / "ocd-default-spec.ocd",
        )

        last_error: Exception | None = None
        for path in candidate_paths:
            try:
                with path.open("r", encoding="utf-8") as handle:
                    # Parse OCD spec file (YAML-like format)
                    _DEFAULT_SPEC = safe_load(handle.read())
                    break
            except Exception as exc:
                last_error = exc
                continue

        if _DEFAULT_SPEC is None:
            message = "could not locate bundled ocd-default-spec.ocd"
            if last_error is not None:
                raise FileNotFoundError(message) from last_error
            raise FileNotFoundError(message)
    
    return _DEFAULT_SPEC


def _load_spec_overlay(spec_path: str) -> Dict[str, Any]:
    """Load a custom OCD specification overlay."""
    path = Path(spec_path)
    if not path.exists():
        raise FileNotFoundError(f"Specification file not found: {spec_path}")
    
    with path.open("r", encoding="utf-8") as handle:
        return safe_load(handle.read())


def _merge_specs(base_spec: Dict[str, Any], overlay_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overlay specification into base specification."""
    # Deep merge the specifications
    merged = base_spec.copy()
    
    def deep_merge(base: Dict[str, Any], overlay: Dict[str, Any]) -> None:
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
    
    deep_merge(merged, overlay_spec)
    return merged


def _format_schema_error(error: JSONSchemaValidationError) -> Dict[str, Any]:
    location: Tuple[Any, ...] = tuple(error.absolute_path)
    return {
        "loc": location,
        "msg": error.message,
        "type": f"jsonschema.{error.validator}",
    }


def _collect_schema_errors(doc: Any) -> List[Dict[str, Any]]:
    validator = _load_core_schema_validator()
    errors = sorted(validator.iter_errors(doc), key=lambda err: (tuple(err.absolute_path), err.message))
    return [_format_schema_error(error) for error in errors]


def validate_and_normalize(
    doc: Any, 
    mode: Literal["relaxed", "strict"] = "relaxed",
    spec_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate and normalize an OCD document.
    
    Args:
        doc: The document to validate
        mode: Validation mode - "relaxed" for structure-only, "strict" for full validation
        spec_path: Optional path to custom OCD specification overlay
        
    Returns: { ok: bool, data?: dict, errors?: list, warnings?: list }
    """
    # Load specification
    try:
        base_spec = _load_default_spec()
        if spec_path:
            overlay_spec = _load_spec_overlay(spec_path)
            spec = _merge_specs(base_spec, overlay_spec)
        else:
            spec = base_spec
    except Exception as exc:
        return {"ok": False, "errors": [{"loc": ("spec",), "msg": str(exc), "type": "spec_error"}]}
    
    # Override mode from spec if provided
    if "validation" in spec and "mode" in spec["validation"]:
        mode = spec["validation"]["mode"]
    
    model = CharacterDefinition
    schema_errors = _collect_schema_errors(doc)
    unsupported_kind_error: Dict[str, Any] | None = None
    if isinstance(doc, dict):
        kind = doc.get("kind")
        if kind == "CharacterInstance":
            model = CharacterInstance
        elif kind not in (None, "CharacterDefinition"):
            unsupported_kind_error = {
                "loc": ("kind",),
                "msg": f"unsupported kind '{kind}'",
                "type": "value_error",
            }

    errors: List[Dict[str, Any]] = []
    
    # In relaxed mode, only add critical schema errors
    if mode == "relaxed":
        # Filter to only critical errors (missing required fields, type mismatches)
        critical_errors = []
        for error in schema_errors:
            if error.get("type") in ["jsonschema.required", "jsonschema.type"]:
                critical_errors.append(error)
        errors.extend(critical_errors)
    else:
        # In strict mode, include all schema errors
        errors.extend(schema_errors)
    
    if unsupported_kind_error is not None:
        errors.append(unsupported_kind_error)

    obj = None
    if unsupported_kind_error is None:
        try:
            obj = model.model_validate(doc)
        except ValidationError as exc:
            if mode == "strict":
                errors.extend(exc.errors())
            else:
                # In relaxed mode, convert validation errors to warnings
                for error in exc.errors():
                    warnings.append({
                        "code": "VALIDATION_WARNING",
                        "path": _format_location(error.get("loc")),
                        "detail": error.get("msg", "validation warning")
                    })

    if errors:
        return {"ok": False, "errors": errors}

    assert obj is not None

    data: Dict[str, Any] = obj.model_dump(mode="python")
    warnings: List[Dict[str, Any]] = []

    normalize_in_place(data, warnings)
    warnings.extend(lint(data))

    return {"ok": True, "data": data, "warnings": warnings}


def _parse_document(text: str, format_hint: str, source: str) -> Any:
    if format_hint == "json":
        return json.loads(text)
    if format_hint == "yaml":
        return safe_load(text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            return safe_load(text)
        except Exception as exc:  # pragma: no cover - yaml loader has its own tests
            raise ValueError(f"failed to parse '{source}' as JSON or YAML") from exc


def _format_location(location: Sequence[Any] | None) -> str:
    if not location:
        return "<root>"
    return ".".join(str(part) for part in location)


def _print_errors(errors: List[Dict[str, Any]]) -> None:
    if not errors:
        return

    print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
    for error in errors:
        loc = _format_location(error.get("loc"))
        msg = error.get("msg") or "validation error"
        print(f"  - {loc}: {msg}", file=sys.stderr)


def _print_warnings(warnings: List[Dict[str, Any]]) -> None:
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
    parser = argparse.ArgumentParser(
        description="Validate and normalize an Open Character Specification document",
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
        help="Validation mode: 'relaxed' for structure-only validation, 'strict' for full validation (default: relaxed).",
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
