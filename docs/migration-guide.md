# Migration Guide

This guide helps you migrate from the old OCD-T format to the new unified OCD format and validation system.

## What Changed

### Format Unification

- **OCD-T format deprecated**: The old OCD-T format is no longer supported
- **Unified OCD format**: All character data now uses YAML or JSON
- **Specification files**: Validation rules are now defined in `.ocd` files
- **Two-mode validation**: New relaxed and strict validation modes

### Key Changes

1. **Character files**: Now use YAML/JSON instead of OCD-T
2. **Validation**: New two-mode system (relaxed/strict)
3. **Specifications**: Custom validation rules in `.ocd` files
4. **CLI tools**: Updated with new options and behavior
5. **APIs**: New parameters for mode and specification paths

## Migration Steps

### Step 1: Update Character Files

Convert your OCD-T character files to YAML or JSON format.

**Old OCD-T format:**
```
character "Aria the Bold" {
  identity {
    kind: person
    species: human
    age: 25
  }
  personality {
    summary: "Brave and adventurous"
    traits: [courage: 0.8, wisdom: 0.6]
  }
}
```

**New YAML format:**
```yaml
ocd_version: "0.9.0"
id: "aria-the-bold"
names:
  canon: "Aria the Bold"
identity:
  entity_kind: "person"
  species: "human"
  sapience_level: "sapient"
  age: 25
personality:
  summary: "Brave and adventurous"
  traits:
    - name: "courage"
      kind: "scalar"
      value: 0.8
    - name: "wisdom"
      kind: "scalar"
      value: 0.6
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Step 2: Update Validation Commands

Update your validation commands to use the new format and options.

**Old commands:**
```bash
# Old OCD-T validation
ocd-validate character.ocdt
ocd-validate character.ocdt --strict
```

**New commands:**
```bash
# New YAML/JSON validation
ocd-validate character.yaml
ocd-validate character.yaml --mode strict
ocd-validate character.yaml --spec my-project-spec.ocd
```

### Step 3: Create Custom Specifications

If you had custom validation logic, create `.ocd` specification files.

**Old custom validation:**
```python
# Old custom validation logic
def validate_character(character):
    if len(character.personality.traits) < 3:
        raise ValidationError("Must have at least 3 traits")
    if character.identity.species not in ALLOWED_SPECIES:
        raise ValidationError("Invalid species")
```

**New specification file:**
```yaml
# my-project-spec.ocd
id: my-project-spec
type: validationSpec
metadata:
  name: My Project Validation Rules

validation:
  mode: strict
  rules:
    custom_validation:
      - code: MINIMUM_TRAITS
        condition: "personality.traits.length >= 3"
        message: "Must have at least 3 traits"
        severity: error
    enums:
      species:
        values: [human, elf, dwarf, halfling]
        strict: true
```

### Step 4: Update Integration Code

Update your application code to use the new validation APIs.

**Old Python integration:**
```python
from ocd import parse_ocdt, validate_character

# Parse OCD-T file
character = parse_ocdt("character.ocdt")

# Validate character
if validate_character(character, strict=True):
    print("Character is valid")
```

**New Python integration:**
```python
from ocd.validate import validate_and_normalize

# Load YAML file
with open("character.yaml") as f:
    character_data = yaml.safe_load(f)

# Validate character
result = validate_and_normalize(character_data, mode="strict")
if result["ok"]:
    print("Character is valid")
    print("Normalized data:", result["data"])
else:
    print("Validation failed:", result["errors"])
```

**Old TypeScript integration:**
```typescript
import { parseOcdt, validateCharacter } from '@ocd-tools/validator';

// Parse OCD-T file
const character = parseOcdt("character.ocdt");

// Validate character
if (validateCharacter(character, { strict: true })) {
  console.log("Character is valid");
}
```

**New TypeScript integration:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

// Load YAML file
const characterData = await loadYamlFile("character.yaml");

// Validate character
const result = await validateAndNormalize(characterData, 'strict');
if (result.ok) {
  console.log("Character is valid");
  console.log("Normalized data:", result.data);
} else {
  console.log("Validation failed:", result.errors);
}
```

## Field Mapping

### Identity Fields

| Old OCD-T | New OCD | Notes |
|-----------|---------|-------|
| `kind` | `entity_kind` | Renamed for clarity |
| `species` | `species` | Same |
| `age` | `age` | Same |
| `gender` | `gender` | Same |
| `sapience` | `sapience_level` | Renamed for clarity |

### Personality Fields

| Old OCD-T | New OCD | Notes |
|-----------|---------|-------|
| `summary` | `summary` | Same |
| `traits` | `traits` | Now array of objects |
| `motivations` | `motivations` | Same |
| `fears` | `fears` | Same |

### Meta Fields

| Old OCD-T | New OCD | Notes |
|-----------|---------|-------|
| `tags` | `meta.tags` | Moved under meta |
| `version` | `meta.versioning` | Expanded structure |
| `created` | `meta.versioning.created_at` | Moved under versioning |
| `modified` | `meta.versioning.last_modified` | Moved under versioning |

## Validation Mode Mapping

### Old Strict Mode → New Strict Mode

The old strict mode maps directly to the new strict mode:

```bash
# Old
ocd-validate character.ocdt --strict

# New
ocd-validate character.yaml --mode strict
```

### Old Default Mode → New Relaxed Mode

The old default mode maps to the new relaxed mode:

```bash
# Old
ocd-validate character.ocdt

# New
ocd-validate character.yaml --mode relaxed
```

## Common Migration Issues

### Issue: Missing Required Fields

**Problem:** Validation fails with "Missing required field" errors.

**Solution:** Add missing required fields to your character files:

```yaml
ocd_version: "0.9.0"  # Required
id: "my-character"    # Required
names:                # Required
  canon: "My Character"
identity:             # Required
  entity_kind: "person"
  species: "human"
  sapience_level: "sapient"
meta:                 # Required
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Issue: Invalid Enum Values

**Problem:** Validation fails with "Invalid enum value" errors.

**Solution:** Update enum values to match the new schema:

```yaml
identity:
  entity_kind: "person"      # Valid: person, creature, ai, collective
  species: "human"           # Valid: human, elf, dwarf, halfling, etc.
  sapience_level: "sapient"  # Valid: animal, tool, agent, sapient, transcendent
```

### Issue: Trait Format Changed

**Problem:** Old trait format no longer works.

**Solution:** Convert traits to the new array format:

```yaml
# Old format
personality:
  traits: [courage: 0.8, wisdom: 0.6]

# New format
personality:
  traits:
    - name: "courage"
      kind: "scalar"
      value: 0.8
    - name: "wisdom"
      kind: "scalar"
      value: 0.6
```

### Issue: Custom Validation Not Working

**Problem:** Custom validation rules aren't being applied.

**Solution:** Create a custom specification file:

```yaml
# custom-spec.ocd
id: my-custom-spec
type: validationSpec
metadata:
  name: My Custom Validation Rules

validation:
  mode: strict
  rules:
    custom_validation:
      - code: MY_CUSTOM_RULE
        condition: "personality.traits.length >= 3"
        message: "Must have at least 3 traits"
        severity: error
```

Then use it:
```bash
ocd-validate character.yaml --spec custom-spec.ocd
```

## Migration Tools

### Automated Conversion Script

Create a script to convert OCD-T files to YAML:

```python
#!/usr/bin/env python3
import os
import yaml
from pathlib import Path

def convert_ocdt_to_yaml(ocdt_file, yaml_file):
    """Convert OCD-T file to YAML format."""
    # This is a simplified example
    # You'll need to implement the actual conversion logic
    
    with open(ocdt_file, 'r') as f:
        ocdt_content = f.read()
    
    # Parse OCD-T content and convert to YAML structure
    yaml_data = parse_ocdt_content(ocdt_content)
    
    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False)

def parse_ocdt_content(content):
    """Parse OCD-T content and return YAML data structure."""
    # Implement your OCD-T parsing logic here
    # This is just a placeholder
    return {
        "ocd_version": "0.9.0",
        "id": "converted-character",
        "names": {"canon": "Converted Character"},
        "identity": {
            "entity_kind": "person",
            "species": "human",
            "sapience_level": "sapient"
        },
        "meta": {
            "versioning": {
                "created_at": "2024-01-01T00:00:00Z",
                "last_modified": "2024-01-01T00:00:00Z"
            }
        }
    }

# Convert all OCD-T files in a directory
def convert_directory(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for ocdt_file in input_path.glob("*.ocdt"):
        yaml_file = output_path / (ocdt_file.stem + ".yaml")
        convert_ocdt_to_yaml(ocdt_file, yaml_file)
        print(f"Converted {ocdt_file} to {yaml_file}")

if __name__ == "__main__":
    convert_directory("characters", "converted")
```

### Validation Script

Create a script to validate converted files:

```bash
#!/bin/bash
# validate-converted.sh

echo "Validating converted character files..."

VALID_COUNT=0
INVALID_COUNT=0

for file in converted/*.yaml; do
    if [ -f "$file" ]; then
        echo "Validating $file..."
        
        if ocd-validate "$file" --mode strict; then
            echo "✅ $file - Valid"
            ((VALID_COUNT++))
        else
            echo "❌ $file - Invalid"
            ((INVALID_COUNT++))
        fi
    fi
done

echo ""
echo "Validation Summary:"
echo "Valid: $VALID_COUNT"
echo "Invalid: $INVALID_COUNT"

if [ $INVALID_COUNT -gt 0 ]; then
    exit 1
fi
```

## Testing Your Migration

### Step 1: Validate All Files

```bash
# Validate all character files
for file in characters/*.yaml; do
    echo "Validating $file..."
    ocd-validate "$file" --mode strict
done
```

### Step 2: Test Custom Specifications

```bash
# Test with custom specification
ocd-validate character.yaml --spec my-project-spec.ocd
```

### Step 3: Test Integration

```python
# Test Python integration
from ocd.validate import validate_and_normalize

with open("character.yaml") as f:
    character_data = yaml.safe_load(f)

result = validate_and_normalize(character_data, mode="strict")
assert result["ok"], f"Validation failed: {result['errors']}"
```

```typescript
// Test TypeScript integration
import { validateAndNormalize } from '@ocd-tools/validator';

const characterData = await loadYamlFile("character.yaml");
const result = await validateAndNormalize(characterData, 'strict');

if (!result.ok) {
  throw new Error(`Validation failed: ${result.errors}`);
}
```

## Rollback Plan

If you need to rollback your migration:

1. **Keep backups** of your original OCD-T files
2. **Test thoroughly** before deploying
3. **Use feature flags** to switch between old and new systems
4. **Monitor validation results** after migration
5. **Have a rollback script** ready

## Getting Help

If you encounter issues during migration:

1. **Check the documentation** - see [Troubleshooting Guide](troubleshooting.md)
2. **Review examples** - look at the example characters
3. **Ask questions** - use GitHub Discussions
4. **Report bugs** - use GitHub Issues
5. **Join the community** - connect with other users

## Migration Checklist

- [ ] Convert OCD-T files to YAML/JSON
- [ ] Update validation commands
- [ ] Create custom specifications if needed
- [ ] Update integration code
- [ ] Test all character files
- [ ] Test custom specifications
- [ ] Test integration code
- [ ] Update documentation
- [ ] Train team on new system
- [ ] Deploy to production
- [ ] Monitor validation results
- [ ] Clean up old files

## Next Steps

After completing your migration:

1. **Explore new features** - try the new validation modes
2. **Create custom specifications** - define project-specific rules
3. **Integrate with your workflow** - use the new APIs
4. **Share feedback** - help improve the system
5. **Contribute** - help others with their migration
