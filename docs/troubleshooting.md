# Troubleshooting Guide

This guide helps you resolve common issues when working with the Open Character Design Specification validation system.

## Common Validation Issues

### Missing Required Fields

**Error:** `Missing required field: ocd_version`

**Cause:** The character file is missing the `ocd_version` field.

**Solution:**
```yaml
ocd_version: "1.0.0"  # Add this field at the top level
id: "my-character"
# ... rest of character data
```

**Error:** `Missing required field: id`

**Cause:** The character file is missing the `id` field.

**Solution:**
```yaml
ocd_version: "1.0.0"
id: "my-character"  # Add this field
# ... rest of character data
```

### Invalid Enum Values

**Error:** `Invalid enum value: 'invalid-kind' for field 'identity.kind'`

**Cause:** The value doesn't match the allowed enum values.

**Solution:**
```yaml
identity:
  kind: "person"  # Use valid enum value: person, creature, ai, collective
  species: "human"
  sapience_level: "sapient"
```

**Valid enum values:**
- `kind`: `person`, `creature`, `ai`, `collective`
- `species`: `human`, `elf`, `dwarf`, `halfling`, `dragonborn`, `gnome`, `tiefling`
- `sapience_level`: `animal`, `tool`, `agent`, `sapient`, `transcendent`

### Type Validation Errors

**Error:** `Expected string, got number for field 'identity.age'`

**Cause:** The field has the wrong data type.

**Solution:**
```yaml
identity:
  age: 25  # Ensure it's a number, not a string
  # or
  age: "25"  # If you want it as a string, update your schema
```

### Structure Validation Errors

**Error:** `Expected object, got string for field 'personality'`

**Cause:** The field structure doesn't match the expected schema.

**Solution:**
```yaml
personality:
  summary: "Brave and adventurous"  # Correct structure
  traits:
    - name: "courage"
      kind: "scalar"
      value: 0.8
```

## Validation Mode Issues

### Relaxed Mode Too Permissive

**Problem:** Validation passes but you want stricter checking.

**Solution:**
```bash
# Use strict mode
ocd-validate character.yaml --mode strict

# Or create a custom specification
ocd-validate character.yaml --spec my-strict-spec.ocd
```

### Strict Mode Too Restrictive

**Problem:** Validation fails for valid character data.

**Solution:**
```bash
# Use relaxed mode
ocd-validate character.yaml --mode relaxed

# Or adjust your custom specification
ocd-validate character.yaml --spec my-relaxed-spec.ocd
```

## Custom Specification Issues

### Specification File Not Found

**Error:** `Specification file not found: my-spec.ocd`

**Cause:** The specification file path is incorrect or the file doesn't exist.

**Solution:**
```bash
# Check file exists
ls -la my-spec.ocd

# Use absolute path
ocd-validate character.yaml --spec /full/path/to/my-spec.ocd

# Use relative path from current directory
ocd-validate character.yaml --spec ./my-spec.ocd
```

### Invalid Specification Format

**Error:** `Invalid specification format: YAML parse error`

**Cause:** The specification file has invalid YAML syntax or structure.

**Solution:**
```yaml
# Ensure proper YAML syntax
id: my-spec
type: validationSpec
metadata:
  name: My Specification
  description: My custom validation rules

validation:
  mode: relaxed
  constraints:
    allowUnknownFields: true
    softEnums: true
```

### Custom Rules Not Working

**Problem:** Custom validation rules aren't being applied.

**Solution:**
1. Check rule syntax:
```yaml
validation:
  rules:
    custom_validation:
      - code: MINIMUM_TRAITS
        condition: "personality.traits.length >= 3"
        message: "Characters must have at least 3 personality traits"
        severity: error
```

2. Verify condition expressions are valid JavaScript
3. Ensure rule codes are unique
4. Test with simple examples first

## Installation Issues

### Python Package Not Found

**Error:** `ModuleNotFoundError: No module named 'ocd'`

**Cause:** The package isn't installed or installed incorrectly.

**Solution:**
```bash
# Install the package
pip install ocd-validate

# Or install from source
pip install -e .

# Check installation
python -c "import ocd; print(ocd.__version__)"
```

### Node.js Package Not Found

**Error:** `Cannot find module '@ocd-tools/validator'`

**Cause:** The package isn't installed or installed incorrectly.

**Solution:**
```bash
# Install the package
npm install @ocd-tools/validator

# Or install globally
npm install -g @ocd-tools/validator

# Check installation
npx @ocd-tools/validator --version
```

### Permission Denied

**Error:** `Permission denied: ocd-validate`

**Cause:** Insufficient permissions to run the validator.

**Solution:**
```bash
# Use npx for Node.js
npx @ocd-tools/validator character.yaml

# Or fix permissions
chmod +x /path/to/ocd-validate

# Or use sudo (not recommended)
sudo ocd-validate character.yaml
```

## Performance Issues

### Slow Validation

**Problem:** Validation takes too long for large character files.

**Solution:**
1. Use relaxed mode for development:
```bash
ocd-validate character.yaml --mode relaxed
```

2. Optimize your character data structure
3. Remove unnecessary fields
4. Use smaller specification files

### Memory Issues

**Problem:** Out of memory errors during validation.

**Solution:**
1. Increase available memory
2. Process characters in smaller batches
3. Use streaming validation for large files
4. Optimize character data structure

## Integration Issues

### API Integration Problems

**Problem:** Validation API calls failing.

**Solution:**
```python
# Python - handle errors properly
try:
    result = validate_and_normalize(character_data, mode="strict")
    if result["ok"]:
        print("Validation successful")
    else:
        print("Validation failed:", result["errors"])
except Exception as e:
    print("Validation error:", str(e))
```

```typescript
// TypeScript - handle errors properly
try {
  const result = await validateAndNormalize(characterData, 'strict');
  if (result.ok) {
    console.log('Validation successful');
  } else {
    console.log('Validation failed:', result.errors);
  }
} catch (error) {
  console.error('Validation error:', error);
}
```

### CLI Integration Problems

**Problem:** CLI output not suitable for scripts.

**Solution:**
```bash
# Use JSON output for parsing
ocd-validate character.yaml --format json

# Use exit codes for scripts
if ocd-validate character.yaml; then
  echo "Validation successful"
else
  echo "Validation failed"
  exit 1
fi
```

## Debugging Tips

### Enable Debug Mode

```bash
# Set debug environment variable
OCD_DEBUG=1 ocd-validate character.yaml

# Or use verbose output
ocd-validate character.yaml --verbose
```

### Check Character Structure

```bash
# Validate structure only
ocd-validate character.yaml --mode relaxed

# Check specific fields
ocd-validate character.yaml --mode strict --spec minimal-spec.ocd
```

### Test with Minimal Examples

```yaml
# Minimal valid character
ocd_version: "1.0.0"
id: "test"
names:
  canon: "Test"
identity:
  entity_kind: "person"
  species: "human"
  sapience_level: "sapient"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Getting Help

### Check Documentation

1. [Validation Reference](reference/validation.md)
2. [Integration Examples](integration/examples.md)
3. [Specification Format](spec/ocd-specification-format.md)

### Community Support

1. [GitHub Issues](https://github.com/Open-Character-Design/OCD-Specification/issues)
2. [GitHub Discussions](https://github.com/Open-Character-Design/OCD-Specification/discussions)
3. [Discord Community](https://discord.gg/ocd-spec)

### Report Bugs

When reporting bugs, include:

1. **Character file** (or minimal example)
2. **Validation command** used
3. **Expected behavior** vs actual behavior
4. **Error messages** (full output)
5. **Environment details** (OS, Python/Node version, package version)

### Example Bug Report

```
Title: Validation fails with custom specification

Description:
Validation fails when using a custom specification file, even though the character file is valid.

Steps to reproduce:
1. Create character.yaml with valid data
2. Create custom-spec.ocd with custom rules
3. Run: ocd-validate character.yaml --spec custom-spec.ocd
4. See error: "Invalid specification format"

Expected: Validation should succeed
Actual: Validation fails with specification error

Environment:
- OS: macOS 13.0
- Python: 3.9.0
- Package: ocd-validate 1.0.0

Files:
[Attach character.yaml and custom-spec.ocd]
```

## Best Practices

### Character Data

1. **Use consistent field names** across all characters
2. **Validate early and often** during development
3. **Use relaxed mode** for prototyping
4. **Use strict mode** for production
5. **Keep character files small** and focused

### Custom Specifications

1. **Start with default specification** and override only what you need
2. **Test thoroughly** with various character types
3. **Document custom rules** clearly
4. **Version control** your specifications
5. **Use descriptive rule codes** and messages

### Integration

1. **Handle errors gracefully** in your applications
2. **Use appropriate validation modes** for your use case
3. **Cache validation results** when possible
4. **Monitor validation performance** in production
5. **Keep validators updated** to latest versions
