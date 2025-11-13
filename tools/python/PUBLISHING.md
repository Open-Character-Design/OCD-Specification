# Publishing ocd-validate to PyPI

## Prerequisites

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Ensure you have PyPI credentials:
   - Test PyPI: https://test.pypi.org/
   - Production PyPI: https://pypi.org/

## Building the Package

From the `tools/python` directory:

```bash
# Clean previous builds
rm -rf dist build *.egg-info

# Build wheel and source distribution
python -m build
```

This creates:
- `dist/ocd_validate-1.0.0-py3-none-any.whl` (wheel)
- `dist/ocd_validate-1.0.0.tar.gz` (source distribution)

## Testing the Build

Before publishing, test the package locally:

```bash
# Install in a virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install dist/ocd_validate-1.0.0-py3-none-any.whl

# Test the CLI
ocd-validate --help

# Test the library
python -c "from ocd.validate import validate_and_normalize; print('OK')"
```

## Publishing to Test PyPI

First, test the upload process:

```bash
twine upload --repository testpypi dist/*
```

Enter credentials when prompted.

Then test installation from Test PyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ ocd-validate
```

## Publishing to Production PyPI

Once verified on Test PyPI:

```bash
twine upload dist/*
```

## Version Management

To update the version, edit `pyproject.toml`:

```toml
[project]
version = "1.0.1"  # Update version number
```

Then rebuild and re-upload.

## Package Contents

The package includes:
- All Python source files in `src/ocd/validate/`
- Default specification: `ocd/validate/data/ocd-default-spec.ocd`
- Validation schema: `ocd/validate/data/ocd-validation-spec.schema.json`
- Core schema: `ocd/validate/data/core.schema.json`

These files are automatically included via the build configuration in `pyproject.toml`.

## Verification Checklist

- [ ] Package builds without errors
- [ ] All test cases pass
- [ ] Package installs correctly
- [ ] CLI command works (`ocd-validate --help`)
- [ ] Library imports work (`from ocd.validate import validate_and_normalize`)
- [ ] Default spec is found when installed
- [ ] Schema validation works
- [ ] README.md is readable and accurate
- [ ] Version number is correct
- [ ] All dependencies are listed in `pyproject.toml`

