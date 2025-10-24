---
title: Validation Modes
description: Learn when to use relaxed or strict validation and how to tune custom OCD specifications.
search:
  boost: 2
tags:
  - validation
  - qa
  - workflow
---

# Validation Modes

This tutorial explains how to use the two validation modes in the Open Character Design Specification: relaxed and strict. You'll learn when to use each mode and how to create custom validation specifications.

!!! info "Need the full rule reference?"
    The normative rules live in the [Validation Overview](../reference/validation.md) and [Diagnostics Reference](../reference/diagnostics.md). Come back here when you want the narrative walkthrough and examples.

## Understanding Validation Modes

The OCD validation system provides two distinct modes to accommodate different use cases and workflows:

### Relaxed Mode (Default)

Relaxed mode prioritizes flexibility and ease of use:

- **Structure validation**: Ensures required fields are present
- **Soft type checking**: Basic type validation for critical fields
- **Soft enums**: Enum violations generate warnings, not errors
- **Unknown fields**: Allows additional fields not defined in the schema
- **Flexible types**: Accepts broader type ranges where possible

**Use relaxed mode when:**
- Prototyping or developing characters
- Working with legacy character data
- Creative workflows where flexibility is important
- Migrating from other character systems

### Strict Mode

Strict mode provides comprehensive validation:

- **Complete validation**: All schema rules are enforced
- **Enum enforcement**: Invalid enum values cause validation failures
- **Type strictness**: Exact type matching required
- **Reference validation**: All references must be resolvable
- **No unknown fields**: Additional fields cause validation failures

**Use strict mode when:**
- Production systems and APIs
- Data quality assurance
- Ensuring consistency across teams
- Final validation before deployment

## Basic Usage

### Command Line

```bash
# Relaxed mode (default)
ocd-validate character.yaml

# Explicit relaxed mode
ocd-validate character.yaml --mode relaxed

# Strict mode
ocd-validate character.yaml --mode strict
```

### Programmatic Usage

```python
# Python
from ocd.validate import validate_and_normalize

# Relaxed mode (default)
result = validate_and_normalize(character_data)

# Strict mode
result = validate_and_normalize(character_data, mode="strict")
```

```typescript
// TypeScript/JavaScript
import { validateAndNormalize } from '@ocd-tools/validator';

// Relaxed mode (default)
const result = await validateAndNormalize(characterData);

// Strict mode
const result = await validateAndNormalize(characterData, 'strict');
```

## Example: Character Validation

Let's see how the same character file behaves in different modes:

### Sample Character File

```yaml
# character.yaml
ocd_version: "1.0.0"
id: "hero-001"
names:
  canon: "Aria the Bold"
  aliases: ["Aria", "The Bold One"]
identity:
  entity_kind: "person"
  species: "human"  # Valid enum value
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
  tags: ["hero", "adventurer"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Relaxed Mode Validation

```bash
ocd-validate character.yaml --mode relaxed
```

**Result:** ✅ Validation succeeds
- All required fields present
- Basic structure is valid
- No critical errors

### Strict Mode Validation

```bash
ocd-validate character.yaml --mode strict
```

**Result:** ✅ Validation succeeds
- All schema rules enforced
- Enum values validated
- Type checking strict
- No additional fields

## Example: Invalid Character

Let's see how an invalid character behaves in different modes:

### Invalid Character File

```yaml
# invalid-character.yaml
ocd_version: "1.0.0"
id: "hero-002"
names:
  canon: "Aria the Bold"
  # Missing required fields
identity:
  entity_kind: "invalid-kind"  # Invalid enum value
  species: "human"
  sapience_level: "sapient"
personality:
  summary: "Brave"  # Too short for strict mode
  traits: []  # Empty array
meta:
  tags: ["hero"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Relaxed Mode Validation

```bash
ocd-validate invalid-character.yaml --mode relaxed
```

**Result:** ⚠️ Validation succeeds with warnings
- Missing required fields generate warnings
- Invalid enum values generate warnings
- Empty arrays generate warnings
- Short summary generates warnings

### Strict Mode Validation

```bash
ocd-validate invalid-character.yaml --mode strict
```

**Result:** ❌ Validation fails with errors
- Missing required fields cause errors
- Invalid enum values cause errors
- Empty arrays cause errors
- Short summary causes errors

## Creating Custom Specifications

You can create custom validation specifications that override the default behavior:

### Basic Custom Specification

```yaml
# my-project-spec.ocd
id: my-project-spec
type: validationSpec
metadata:
  name: My Project Validation Rules
  description: Custom validation for my project

validation:
  mode: strict  # Override default mode
  constraints:
    allowUnknownFields: false
    softEnums: false
    strictTypes: true
    enforceRequired: true
    validateReferences: true

  rules:
    custom_validation:
      - code: MINIMUM_TRAITS
        condition: "personality.traits.length >= 3"
        message: "Characters must have at least 3 personality traits"
        severity: error
      - code: PROTAGONIST_TAG
        condition: "meta.tags.includes('protagonist')"
        message: "Protagonist characters should be tagged"
        severity: warning

    enums:
      species:
        values: [human, elf, dwarf, halfling]
        strict: true
```

### Using Custom Specifications

```bash
# Use custom specification
ocd-validate character.yaml --spec my-project-spec.ocd

# Override mode in specification
ocd-validate character.yaml --mode relaxed --spec my-project-spec.ocd
```

## Workflow Examples

### Development Workflow

```bash
# 1. Start with relaxed mode for development
ocd-validate character.yaml --mode relaxed

# 2. Test with strict mode before commit
ocd-validate character.yaml --mode strict

# 3. Use custom spec for project requirements
ocd-validate character.yaml --spec project-spec.ocd
```

### CI/CD Pipeline

```bash
# In your CI pipeline
ocd-validate characters/*.yaml --mode strict --spec project-spec.ocd
```

### Team Development

```bash
# Team members use relaxed mode for development
ocd-validate character.yaml --mode relaxed

# Lead validates with strict mode before review
ocd-validate character.yaml --mode strict --spec project-spec.ocd
```

## Best Practices

### Choosing the Right Mode

**Use Relaxed Mode When:**
- Prototyping new characters
- Working with legacy data
- Creative exploration
- Development and testing

**Use Strict Mode When:**
- Production systems
- Data quality assurance
- Team consistency
- Final validation

### Custom Specifications

**Create Custom Specs For:**
- Project-specific requirements
- Team coding standards
- Genre-specific constraints
- Quality assurance rules

**Best Practices:**
- Start with default specification
- Override only what you need
- Test thoroughly
- Document custom rules
- Version control specifications

### Error Handling

**In Relaxed Mode:**
- Focus on critical errors only
- Use warnings for suggestions
- Allow flexibility in development

**In Strict Mode:**
- Enforce all rules
- Fail on any violation
- Ensure data quality

## Troubleshooting

### Common Issues

**Mode not working:**
- Check specification file has correct `validation.mode` field
- Ensure mode value is "relaxed" or "strict"
- Verify specification is being loaded

**Custom rules not working:**
- Validate condition expressions
- Check rule codes are unique
- Test with simple examples

**Validation too strict:**
- Switch to relaxed mode
- Adjust custom specification
- Check constraint settings

**Validation too loose:**
- Switch to strict mode
- Add custom validation rules
- Tighten constraint settings

### Debug Mode

```bash
# Enable debug output
OCD_DEBUG=1 ocd-validate character.yaml --mode strict --spec my-spec.ocd
```

## Next Steps

- Learn how custom rules are defined in the [Validation Overview](../reference/validation.md#custom-specification-overlays).
- Explore schema overlay patterns in the [OCD Specification Format](../spec/ocd-specification-format.md).
- See end-to-end validator usage in the [Integration Examples](../integration/examples.md).
- Troubleshoot stubborn issues with the [Validation Troubleshooting Guide](../troubleshooting.md).
