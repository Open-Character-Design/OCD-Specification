# Python Validator

The Python validator provides comprehensive validation, normalization, and diagnostics for OCD documents using the validation spec pipeline with JSON Schema and Pydantic v2.

> Audience: Developers, data engineers, CI users. Prefer no install? Try the [In-Browser Playground (Preview)](../validation/playground.md).

## Installation

```bash
pip install ocd-validate
```

Requires Python 3.10 or newer.

## Overview

The validator uses a flexible `.ocd` specification system that allows you to define custom validation rules. It supports two validation modes and provides comprehensive diagnostics through an evaluator-based pipeline.

### Validation Spec System

Validation uses `.ocd` specification files that define:
- **Rules**: Path-based validation rules with operators like `type`, `enum`, `presence`, etc.
- **Constraints**: High-level constraints like `require`, `forbid`, `disallow`
- **Definitions**: Reusable enums and types referenced with `@enums.Name` and `@types.Name`
- **Policy**: Controls how unknown fields and errors are handled

The validator pipeline includes:
1. **SpecLoader**: Loads and validates `.ocd` spec files
2. **SpecMerger**: Merges multiple specs and resolves references
3. **PathMatcher**: Finds matching paths in documents using dot notation
4. **RuleEvaluator**: Evaluates rules and constraints, produces diagnostics
5. **Normalizer**: Normalizes trait names, slugs, tokens, etc.
6. **Linter**: Provides additional diagnostic warnings

## CLI Usage

```bash
# Validate a file (relaxed mode by default)
ocd-validate character.yaml

# Use strict validation mode
ocd-validate character.yaml --mode strict

# Use custom specification overlay
ocd-validate character.yaml --spec my-project-spec.ocd

# Combine mode and spec
ocd-validate character.yaml --mode strict --spec my-project-spec.ocd

# Print normalized output
ocd-validate character.yaml --print

# Treat warnings as errors
ocd-validate character.yaml --warnings-as-errors

# Force input format
ocd-validate character.yaml --format yaml

# Read from stdin
cat character.yaml | ocd-validate - --print
```

### CLI Options

```bash
ocd-validate [OPTIONS] PATH

Arguments:
  PATH  Path to an OCD document (YAML or JSON). Use '-' to read from standard input.

Options:
  -f, --format [auto|json|yaml]  Force the input parser. Defaults to 'auto'.
  --mode [relaxed|strict]        Validation mode (default: relaxed).
  --spec PATH                    Path to custom OCD specification overlay file.
  --print                        Print the normalized document to stdout on success.
  --indent INTEGER               Indent level to use when printing normalized JSON (default: 2).
  --warnings-as-errors           Exit with code 2 if any warnings are produced.
  --output [text|json]           Output format for diagnostics (default: text).
  -h, --help                     Show this message and exit.
```

### Exit Codes

- `0`: Validation succeeded
- `1`: Validation failed with errors
- `2`: Warnings were produced (when using `--warnings-as-errors`)

## Programmatic API

```python
from ocd.validate import validate_and_normalize, safe_load

# Load a YAML document
with open("character.yaml", "r") as f:
    document = safe_load(f.read())

# Basic validation (relaxed mode)
result = validate_and_normalize(document)

# Strict validation mode
result = validate_and_normalize(document, mode="strict")

# With custom specification overlay
result = validate_and_normalize(document, spec_path="my-project-spec.ocd")

# Combine mode and spec
result = validate_and_normalize(document, mode="strict", spec_path="my-project-spec.ocd")

if result["ok"]:
    print("Valid:", result["data"])
    print("Warnings:", result["warnings"])
else:
    print("Errors:", result["errors"])
```

## API Reference

### `validate_and_normalize(doc: Any, mode: str = "relaxed", spec_path: str | None = None) -> dict`

Validates and normalizes an OCD document using the validation spec system.

**Parameters:**
- `doc`: The document to validate (dict, list, or primitive)
- `mode`: Validation mode - "relaxed" (warnings for data errors) or "strict" (errors for all violations)
- `spec_path`: Optional path to custom `.ocd` specification file

**Returns:**
- `dict`: Result object with the following keys:
  - `ok: bool`: Whether validation succeeded (no errors)
  - `data?: dict`: Normalized document (present if `ok` is True)
  - `errors?: list[dict]`: Validation errors with `loc`, `msg`, and `type` keys
  - `warnings: list[dict]`: Diagnostic warnings with `path`, `detail`, and `code` keys

**Example:**

```python
from ocd.validate import validate_and_normalize

document = {
    "kind": "CharacterDefinition",
    "ocd_version": "0.0.1",
    "id": "char-123",
    "slug": "example-character",
    "names": {"canon": "Example Character"},
    "identity": {
        "entity_kind": "person",
        "sapience_level": "sapient"
    },
    "meta": {
        "versioning": {
            "created_at": "2024-01-01T00:00:00Z",
            "last_modified": "2024-01-01T00:00:00Z"
        }
    }
}

result = validate_and_normalize(document)
```

### `safe_load(text: str) -> Any`

Safely loads a YAML document without executing arbitrary Python code.

**Parameters:**
- `text`: The YAML string to parse

**Returns:**
- Parsed YAML as Python objects

## Validation Modes

### Relaxed Mode (Default)

In relaxed mode:
- **Structure errors**: Always treated as errors (missing required fields, type mismatches)
- **Data errors**: Treated as warnings (enum violations, pattern mismatches, etc.)
- **Use case**: Development, prototyping, gradual validation adoption

### Strict Mode

In strict mode:
- **Structure errors**: Treated as errors
- **Data errors**: Treated as errors
- **Use case**: Production, CI/CD pipelines, strict compliance

## Custom Validation Specs

Create custom `.ocd` files to extend or override validation rules:

```yaml
id: my-project-spec
type: validationSpec
schemaVersion: 1
metadata:
  name: "My Project Validation"
  description: "Custom validation rules for my project"

policy:
  allowUnknownFields: true
  unknownFieldSeverity: warning

definitions:
  enums:
    Species: ["human", "elf", "dwarf", "orc"]

rules:
  - path: "identity.species"
    type: string
    enum: "@enums.Species"
    message: "Species must be from the allowed list"

constraints:
  require:
    - "names.canon"
    - "identity.entity_kind"
  
  disallow:
    tags: ["test", "draft"]
```

Use your custom spec:

```python
from ocd.validate import validate_and_normalize

result = validate_and_normalize(document, spec_path="my-project-spec.ocd")
```

## Normalization

The validator performs the following normalizations automatically:

- **Bipolar trait names**: Canonicalize to `-` dash syntax (e.g., `introversion_extraversion` → `introversion-extraversion`)
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

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from ocd.validate import validate_and_normalize
from pydantic import BaseModel

app = FastAPI()

class CharacterCreate(BaseModel):
    character_data: dict

@app.post("/characters")
async def create_character(character: CharacterCreate):
    """Create character with validation"""
    result = validate_and_normalize(character.character_data)
    
    if not result["ok"]:
        raise HTTPException(
            status_code=400, 
            detail={"errors": result["errors"]}
        )
    
    # Store validated character (implementation-specific)
    return {
        "data": result["data"],
        "warnings": result.get("warnings", [])
    }
```

### Batch Validation

```python
from pathlib import Path
from ocd.validate import validate_and_normalize, safe_load

def validate_directory(directory: str) -> dict:
    """Validate all YAML files in a directory"""
    results = {"valid": [], "invalid": []}
    directory_path = Path(directory)
    
    for yaml_file in directory_path.glob("*.yaml"):
        with open(yaml_file, "r") as f:
            document = safe_load(f.read())
        
        result = validate_and_normalize(document)
        
        if result["ok"]:
            results["valid"].append(str(yaml_file))
        else:
            results["invalid"].append({
                "file": str(yaml_file),
                "errors": result["errors"]
            })
    
    return results
```

### Loading from Files

```python
from pathlib import Path
import json
import yaml
from ocd.validate import validate_and_normalize

def load_and_validate(file_path: str):
    """Load and validate a character file"""
    file = Path(file_path)
    
    with open(file, 'r') as f:
        if file.suffix in ['.yaml', '.yml']:
            from ocd.validate import safe_load
            document = safe_load(f.read())
        else:
            document = json.load(f)
    
    return validate_and_normalize(document)
```

## Dependencies

- `jsonschema>=4.22`: JSON Schema validation
- `pydantic>=2.7`: Data validation and parsing
- `pyyaml>=6.0`: YAML parsing support
- `jsonpath-ng>=1.6`: Path matching for validation rules

## Module Execution

You can also run the validator as a module:

```bash
python -m ocd.validate character.yaml --print
```

## What's Next?

- **[TypeScript/JavaScript Validator](js-ts-validator.md)**: Compare with Node.js implementation
- **[Validation System](../validation/index.md)**: Learn about the validation spec system
- **[Spec Format Reference](../spec/ocd-specification-format.md)**: Details on `.ocd` file format
- **[Examples](../authoring/examples.md)**: Character examples and templates
