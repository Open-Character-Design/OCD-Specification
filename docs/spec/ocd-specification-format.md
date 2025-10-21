# OCD Specification Format

The OCD (Open Character Design) specification format is a human-readable format for defining validation rules and constraints for character data. This format is used to create custom validation specifications that can override or extend the default validation behavior.

## Overview

OCD specification files use the same YAML-like syntax as character files but with a different structure focused on validation rules rather than character data. They allow you to:

- Define custom validation modes (relaxed/strict)
- Override enum values and constraints
- Add custom validation rules
- Configure normalization behavior
- Set warning conditions

## File Structure

### Basic Structure

```yaml
id: my-validation-spec
type: validationSpec
metadata:
  name: My Project Validation Rules
  description: Custom validation configuration for my project
  version: "1.0.0"
  created_at: "2024-01-01T00:00:00Z"
  last_modified: "2024-01-01T00:00:00Z"

validation:
  mode: relaxed  # or strict
  constraints:
    allowUnknownFields: true
    softEnums: true
    strictTypes: false
    enforceRequired: true
    validateReferences: false

  rules:
    # Custom validation rules go here
    custom_validation: []
    enums: {}
    types: {}
    warnings: []
```

### Required Fields

- `id`: Unique identifier for the specification
- `type`: Must be `validationSpec`
- `metadata`: Information about the specification
- `validation`: The main validation configuration

## Validation Configuration

### Mode Setting

```yaml
validation:
  mode: relaxed  # Default mode for this specification
```

**Modes:**
- `relaxed`: Structure-only validation, soft enums, allows unknown fields
- `strict`: Full validation with strict type checking and enum enforcement

### Constraints

```yaml
validation:
  constraints:
    allowUnknownFields: true    # Allow fields not defined in schema
    softEnums: true            # Convert enum violations to warnings
    strictTypes: false         # Use loose type checking
    enforceRequired: true      # Enforce required field validation
    validateReferences: false  # Validate all references
```

### Custom Validation Rules

```yaml
validation:
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
```

**Rule Properties:**
- `code`: Unique identifier for the rule
- `condition`: JavaScript-like expression to evaluate
- `message`: Error or warning message
- `severity`: `error` or `warning`

### Enum Overrides

```yaml
validation:
  rules:
    enums:
      species:
        values: [human, elf, dwarf, halfling, dragonborn]
        strict: true
      entity_kind:
        values: [person, creature, ai, collective]
        strict: false
```

**Enum Properties:**
- `values`: Array of allowed values
- `strict`: Whether to enforce exact matches (true) or allow warnings (false)

### Type Definitions

```yaml
validation:
  rules:
    types:
      personality:
        type: object
        required: true
        properties:
          summary:
            type: string
            required: true
            minLength: 10
          traits:
            type: array
            required: true
            minItems: 1
```

### Warning Rules

```yaml
validation:
  rules:
    warnings:
      - code: MISSING_BIO
        condition: "!background.history"
        message: "Consider adding character background history"
      - code: SINGLE_TRAIT
        condition: "personality.traits.length === 1"
        message: "Characters with only one trait may lack depth"
```

## Normalization Configuration

```yaml
validation:
  rules:
    normalization:
      slugs:
        pattern: "^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        case: lower
        separator: "-"
      tags:
        case: lower
        deduplicate: true
      trait_axes:
        canonical: "↔"
        alternatives: ["-", "_", "↔"]
        normalize: true
```

## Extension Points

```yaml
validation:
  extensions:
    custom_rules: []
    custom_enums: {}
    custom_types: {}
    custom_warnings: []
```

## Complete Example

Here's a complete example of a project-specific validation specification:

```yaml
id: fantasy-rpg-spec
type: validationSpec
metadata:
  name: Fantasy RPG Validation Rules
  description: Validation rules for fantasy role-playing game characters
  version: "1.0.0"
  created_at: "2024-01-01T00:00:00Z"
  last_modified: "2024-01-01T00:00:00Z"

validation:
  mode: strict
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
      - code: VALID_AGE
        condition: "identity.age && identity.age >= 0 && identity.age <= 1000"
        message: "Character age must be between 0 and 1000"
        severity: error

    enums:
      species:
        values: [human, elf, dwarf, halfling, dragonborn, gnome, tiefling]
        strict: true
      entity_kind:
        values: [person, creature, ai]
        strict: true
      sapience_level:
        values: [animal, tool, agent, sapient, transcendent]
        strict: true

    types:
      personality:
        type: object
        required: true
        properties:
          summary:
            type: string
            required: true
            minLength: 20
          traits:
            type: array
            required: true
            minItems: 3
            maxItems: 10

    warnings:
      - code: MISSING_BIO
        condition: "!background.history"
        message: "Consider adding character background history"
      - code: SINGLE_TRAIT
        condition: "personality.traits.length === 1"
        message: "Characters with only one trait may lack depth"
      - code: NO_RELATIONSHIPS
        condition: "!relationships || relationships.length === 0"
        message: "Characters without relationships may feel isolated"

    normalization:
      slugs:
        pattern: "^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        case: lower
        separator: "-"
      tags:
        case: lower
        deduplicate: true
      trait_axes:
        canonical: "↔"
        alternatives: ["-", "_", "↔"]
        normalize: true

  extensions:
    custom_rules: []
    custom_enums: {}
    custom_types: {}
    custom_warnings: []
```

## Using Specification Files

### Command Line

```bash
# Use custom specification
ocd-validate character.yaml --spec my-project-spec.ocd

# Combine with mode override
ocd-validate character.yaml --mode strict --spec my-project-spec.ocd
```

### Programmatic Usage

```python
# Python
from ocd.validate import validate_and_normalize

result = validate_and_normalize(
    character_data, 
    mode="strict", 
    spec_path="my-project-spec.ocd"
)
```

```typescript
// TypeScript/JavaScript
import { validateAndNormalize } from '@ocd-tools/validator';

const result = await validateAndNormalize(
    characterData, 
    'strict', 
    'my-project-spec.ocd'
);
```

## Best Practices

### Naming Conventions

- Use descriptive IDs: `fantasy-rpg-spec`, `sci-fi-campaign-spec`
- Include version numbers in metadata
- Use clear, descriptive names and descriptions

### Rule Organization

- Group related rules together
- Use consistent naming for rule codes
- Provide clear, actionable error messages
- Use appropriate severity levels

### Testing

- Test specifications against various character types
- Validate both valid and invalid characters
- Ensure rules work as expected in both modes
- Document any custom rule behavior

### Version Control

- Keep specification files in version control
- Tag releases with version numbers
- Document changes in commit messages
- Consider backward compatibility when updating

## Migration from Custom Validation

If you have existing custom validation logic:

1. **Identify validation rules**: List all your current validation requirements
2. **Create specification file**: Convert rules to OCD specification format
3. **Test thoroughly**: Validate against existing character data
4. **Update validation calls**: Replace custom validation with `--spec` flag
5. **Document changes**: Update documentation and team guidelines

## Troubleshooting

### Common Issues

**Specification not found:**
- Check file path is correct
- Ensure file exists and is readable
- Verify file permissions

**Invalid specification format:**
- Validate YAML syntax
- Check required fields are present
- Ensure proper indentation

**Rules not working:**
- Verify condition expressions are valid
- Check rule codes are unique
- Test with simple examples first

**Mode override not working:**
- Ensure specification has correct `validation.mode` field
- Check mode value is "relaxed" or "strict"
- Verify specification is being loaded correctly
