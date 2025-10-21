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
```

Key options:

- `--format {auto,json,yaml}` – override automatic format detection.
- `--print` – emit the normalized document to standard output.
- `--indent N` – control the indentation used with `--print` (default: 2).
- `--warnings-as-errors` – exit with status 2 if lint warnings are encountered.

The CLI accepts `-` as the path argument to read from standard input.

## Library Usage

```python
from ocd.validate import validate_and_normalize, safe_load

with open("examples/bruenor.yaml", "r", encoding="utf-8") as handle:
    document = safe_load(handle.read())

result = validate_and_normalize(document)
if result["ok"]:
    print("Normalized:", result["data"])
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
