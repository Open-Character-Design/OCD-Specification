# OCD Python Tools

The `ocd-validate` package provides validation, normalization, and linting helpers for the Open Character Specification.

## Installation

```bash
pip install ocd-validate
```

The project targets Python 3.10+ and ships as a pure-Python wheel.

## Command Line Interface

After installation the `ocd-validate` entry point becomes available:

```bash
# Validate a YAML document and print the normalized JSON
ocd-validate examples/bruenor.yaml --print

# Use strict validation mode
ocd-validate examples/bruenor.yaml --mode strict

# Use custom specification overlay
ocd-validate examples/bruenor.yaml --spec my-project-spec.ocd
```

Key options:

- `--format {auto,json,yaml}` – override automatic format detection.
- `--mode {relaxed,strict}` – validation mode (default: relaxed).
- `--spec PATH` – path to custom OCD specification overlay file.
- `--print` – emit the normalized document to standard output.
- `--indent N` – control the indentation used with `--print` (default: 2).
- `--warnings-as-errors` – exit with status 2 if lint warnings are encountered.

The CLI accepts `-` as the path argument to read from standard input.

## Library Usage

```python
from ocd.validate import validate_and_normalize, safe_load

with open("examples/bruenor.yaml", "r", encoding="utf-8") as handle:
    document = safe_load(handle.read())

# Basic validation (relaxed mode)
result = validate_and_normalize(document)

# Strict validation mode
result = validate_and_normalize(document, mode="strict")

# With custom specification overlay
result = validate_and_normalize(document, spec_path="my-project-spec.ocd")

if result["ok"]:
    print("Normalized:", result["data"])
    print("Warnings:", result["warnings"])
else:
    print("Errors:", result["errors"])
```

The library returns a dictionary with `ok`, `data`, `errors`, and `warnings` keys so you can integrate validation into custom pipelines.

## Module Execution

You can also run the validator as a module:

```bash
python -m ocd.validate examples/bruenor.yaml --print
```

## Namespace Package

This package is part of the `ocd` namespace package structure, allowing for future expansion with additional OCD-related tools under the same namespace.
