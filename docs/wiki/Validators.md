## Validators

Rendered docs: `https://Open-Character-Design.github.io/OpenCharacter-Specification/integration/js-ts-validator/`, `https://Open-Character-Design.github.io/OpenCharacter-Specification/integration/python-validator/`

- Node (JS/TS): [[Integration-Node]]
- Python: [[Integration-Python]]

Use cases:
- Validate, normalize, lint, parse, serialize
- Diagnostics and warnings for authoring workflows

Common flags (CLI):
```bash
# Print normalized JSON (default indent 2)
--print

# Treat lint warnings as errors (exit code 2)
--warnings-as-errors

# Override input format detection
--format json|yaml

# Adjust indentation used with --print
--indent 4
```


