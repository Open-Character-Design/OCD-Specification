# OCS Python Tools

The `ocs` package provides validation, normalization, and linting helpers for the Open Character Specification.

## Installation

```bash
pip install ocs
```

The project targets Python 3.10+ and ships as a pure-Python wheel.

## Command Line Interface

After installation the `ocs-validate` entry point becomes available:

```bash
# Validate a YAML document and print the normalized JSON
ocs-validate examples/bruenor.yaml --print
```

Key options:

- `--format {auto,json,yaml}` – override automatic format detection.
- `--print` – emit the normalized document to standard output.
- `--indent N` – control the indentation used with `--print` (default: 2).
- `--warnings-as-errors` – exit with status 2 if lint warnings are encountered.

The CLI accepts `-` as the path argument to read from standard input.

## Library Usage

```python
from ocs import validate_and_normalize
from ocs.yaml_loader import safe_load

with open("examples/bruenor.yaml", "r", encoding="utf-8") as handle:
    document = safe_load(handle.read())

result = validate_and_normalize(document)
if result["ok"]:
    print("Normalized:", result["data"])
else:
    print("Errors:", result["errors"])
```

The library returns a dictionary with `ok`, `data`, `errors`, and `warnings` keys so you can integrate validation into custom pipelines.
