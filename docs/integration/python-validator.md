# Python Validator

The Python validator provides comprehensive validation, normalization, and diagnostics for OCS documents using Pydantic v2 and JSON Schema.

## Installation

```bash
pip install ocs==1.0.0
```

## Usage

### CLI

```bash
# Validate a file
ocs-validate character.yaml

# Print normalized output
ocs-validate character.yaml --print

# Treat warnings as errors
ocs-validate character.yaml --warnings-as-errors

# Force input format
ocs-validate character.yaml --format yaml
```

### Programmatic API

```python
from ocs.ocs_validate import validate_and_normalize

# Validate a document
result = validate_and_normalize(document)

if result["ok"]:
    print("Valid:", result["data"])
    print("Warnings:", result["warnings"])
else:
    print("Errors:", result["errors"])
```

### CLI Options

```bash
ocs-validate [OPTIONS] PATH

Arguments:
  PATH  Path to an OCS document (YAML or JSON). Use '-' to read from standard input.

Options:
  --format [auto|json|yaml]  Force the input parser. Defaults to 'auto'.
  --print                    Print the normalized document to stdout on success.
  --indent INTEGER           Indent level to use when printing normalized JSON (default: 2).
  --warnings-as-errors       Exit with code 2 if any warnings are produced.
  --help                     Show this message and exit.
```

## API Reference

### `validate_and_normalize(doc: Any) -> Dict[str, Any]`

Validates and normalizes an OCS document.

**Parameters:**
- `doc`: The document to validate (dict, list, or primitive)

**Returns:**
- `Dict[str, Any]`: Result object with the following structure:
  - `ok: bool`: Whether validation succeeded
  - `data?: dict`: Normalized document (if valid)
  - `errors?: list`: Validation errors (if invalid)
  - `warnings: list`: Linting warnings

**Example:**
```python
from ocs.ocs_validate import validate_and_normalize

document = {
    "kind": "CharacterDefinition",
    "ocs_version": "1.0.0",
    "id": "char-123",
    "slug": "example-character",
    "names": {"canon": "Example Character"},
    "identity": {"kind": "humanoid"},
    "meta": {"versioning": {"created_at": "2024-01-01T00:00:00Z", "last_modified": "2024-01-01T00:00:00Z"}}
}

result = validate_and_normalize(document)
```

## Normalization

The validator performs the following normalizations:

- **Bipolar trait names**: Canonicalize to `↔` arrow syntax
- **Tokens**: Lowercase and deduplicate arrays for `tags`, `genres`, `media`, `media_targets`
- **Slugs**: Normalize using consistent token rules
- **Axis names**: Standardize trait axis separators

## Diagnostics

The validator provides comprehensive linting with the following warning codes:

- `RATING_CONFLICT`: Conflicting content ratings
- `MISSING_SKILL_TAGS`: Skills without appropriate tags
- `UNRESOLVED_REF`: References that cannot be resolved
- `MISSING_CANON_NAME`: Missing canonical name
- `NONCANONICAL_CANON_NAME`: Non-canonical name formatting
- `DEFINITION_RUNTIME_FIELD`: Runtime fields in definition
- `COMPOSITE_CONTROL_SHARE_OVERFLOW`: Composite control share exceeds 1.0
- `COMPOSITE_SECRET_WITHOUT_IDENTITY`: Secret composite without identity
- `COMPOSITE_SECRET_IDENTITY_MISMATCH`: Secret identity mismatch
- `NORMALIZED_SLUG`: Slug normalization applied
- `NORMALIZED_AXIS`: Axis name normalization applied

## Dependencies

- `jsonschema>=4.22`: JSON Schema validation
- `pydantic>=2.7`: Data validation and parsing
- `pyyaml>=6.0`: YAML parsing support

## Source Files

- `src/ocs/ocs_validate.py` - Main validation logic
- `src/ocs/ocs_normalize.py` - Normalization functions
- `src/ocs/ocs_lint.py` - Linting rules
- `src/ocs/ocs_model.py` - Pydantic models
