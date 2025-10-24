# Validation

The Open Character Design Specification provides flexible validation with two distinct modes and support for custom specification overlays.

!!! tip "Validation Methodology"
    For systematic approaches to character validation and quality assessment, see our [Methodology Guides](../deep-dives/methodology/index.md) section, including the Character Analysis Framework for comprehensive validation strategies.

!!! info "Research Foundation"
    The validation criteria are based on research into universal character definition fields across all mediums. See [Common Character Definition Fields Across All Mediums](../deep-dives/research/common-character-fields.md) for the theoretical foundation behind OCD's validation approach.

## Validation Modes

The Open Character Design Specification provides two distinct validation modes:

| Feature | ⚡ Relaxed Mode (Default) | 🛡️ Strict Mode |
|---------|---------------------------|----------------|
| **Validation** | 🎨 Structure and Fields<br>Ensures required fields and general structure | 💻 Complete enforcement<br>All schema rules are enforced |
| **Type Checking** | 🔓 Basic validation<br>Basic type validation for critical fields | 🔒Strict validation<br>Exact type matching required |
| **Enum Handling** | 🤷Soft enforcement<br>Enum violations generate warnings, not errors | 🙎 Hard enforcement<br>Invalid enum values cause validation failures |
| **Unknown Fields** | ✅ Allowed<br>Allows additional fields not defined in the schema | ❌ Not allowed<br>Undefined fields cause validation failures |
| **Type Flexibility** | 🔭 Broad acceptance<br>Accepts broader type ranges where possible | 🔬 Strict acceptance<br>Only accepts defined type matches |
| **Reference Validation** | N/A | 🔎 Required<br>All references must be resolvable |
| **Usage**              | <pre><code>ocd-validate character.yaml<br/>ocd-validate character.yaml --mode relaxed</code></pre> | <pre><code><br/>ocd-validate character.yaml --mode strict</code></pre> |


## Specification Overlays

You can extend or override the default validation rules using custom OCD specification files.

### Default Specification

The default specification (`ocd-default-spec.ocd`) provides baseline validation rules:

```yaml
id: ocd-default-spec
type: validationSpec
metadata:
  name: Default OCD Specification
  description: Baseline validation and schema for OCD characters

validation:
  mode: relaxed
  constraints:
    allowUnknownFields: true
    softEnums: true
    strictTypes: false
    enforceRequired: true
    validateReferences: false
```

### Custom Specification Overlays

Create custom specification files to override validation behavior:

```yaml
# my-project-spec.ocd
id: my-project-spec
type: validationSpec
metadata:
  name: My Project Validation Rules
  description: Custom validation rules for my project

validation:
  mode: strict  # Override default mode
  constraints:
    allowUnknownFields: false  # Disallow unknown fields
    softEnums: false  # Enforce enum values strictly
    strictTypes: true  # Require exact type matching
    enforceRequired: true
    validateReferences: true  # Validate all references

  # Add custom validation rules
  rules:
    custom_validation:
      - code: CUSTOM_RULE_1
        condition: "personality.traits.length >= 3"
        message: "Characters must have at least 3 personality traits"
        severity: error
      - code: CUSTOM_RULE_2
        condition: "meta.tags.includes('protagonist')"
        message: "Protagonist characters should be tagged"
        severity: warning

  # Override enum values
  enums:
    species:
      values: [human, elf, dwarf, halfling, dragonborn]
      strict: true
```

### Using Specification Overlays

```bash
# Use custom specification
ocd-validate character.yaml --spec my-project-spec.ocd

# Combine with mode override
ocd-validate character.yaml --mode strict --spec my-project-spec.ocd
```

## Validation Examples

### Basic Validation

```bash
# Validate a character file
ocd-validate character.yaml

# Validate with output
ocd-validate character.yaml --print

# Validate in strict mode
ocd-validate character.yaml --mode strict
```

### Custom Specification

```bash
# Use project-specific validation rules
ocd-validate character.yaml --spec project-rules.ocd

# Validate multiple files with custom spec
for file in characters/*.yaml; do
  ocd-validate "$file" --spec project-rules.ocd
done
```

### Programmatic Usage

#### Python

```python
from ocd.validate import validate_and_normalize

# Basic validation
result = validate_and_normalize(character_data)

# With mode and spec
result = validate_and_normalize(
    character_data, 
    mode="strict", 
    spec_path="custom-spec.ocd"
)

if result["ok"]:
    print("Valid:", result["data"])
    print("Warnings:", result["warnings"])
else:
    print("Errors:", result["errors"])
```

#### TypeScript/JavaScript

```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

// Basic validation
const result = await validateAndNormalize(characterData);

// With mode and spec
const result = await validateAndNormalize(
    characterData, 
    'strict', 
    'custom-spec.ocd'
);

if (result.ok) {
    console.log('Valid:', result.data);
    console.log('Warnings:', result.warnings);
} else {
    console.log('Errors:', result.errors);
}
```

## Error Handling

### Validation Errors

Validation errors prevent successful validation and must be fixed:

```bash
$ ocd-validate invalid-character.yaml
Validation failed with 2 error(s):
  - names: Missing required field 'canon'
  - identity.species: 'invalid-species' is not one of ['human', 'ai', 'alien', 'collective', 'object', 'deity', 'other']
```

### Warnings

Warnings indicate potential issues but don't prevent validation:

```bash
$ ocd-validate character.yaml
Validation produced 3 warning(s):
  - names.canon: [NONCANONICAL_CANON_NAME] Canonical name should be properly capitalized
  - slug: [NORMALIZED_SLUG] Slug was normalized
  - personality.traits[0].axis: [NORMALIZED_AXIS] Trait axis was normalized
```

### Exit Codes

- `0`: Validation succeeded
- `1`: Validation failed with errors
- `2`: Warnings were produced (when using `--warnings-as-errors`)

## Specification File Format

OCD specification files use the same format as character files but with a different structure:

```yaml
id: my-validation-spec
type: validationSpec
metadata:
  name: My Validation Rules
  description: Custom validation configuration

validation:
  mode: relaxed | strict
  constraints:
    allowUnknownFields: boolean
    softEnums: boolean
    strictTypes: boolean
    enforceRequired: boolean
    validateReferences: boolean

  rules:
    # Custom validation rules
    custom_validation:
      - code: RULE_CODE
        condition: "expression"
        message: "Error message"
        severity: error | warning

  # Override enum definitions
  enums:
    field_name:
      values: [list, of, values]
      strict: boolean

  # Override type definitions
  types:
    field_name:
      type: string | number | boolean | object | array
      required: boolean
      properties: object

  # Custom warning rules
  warnings:
    - code: WARNING_CODE
      condition: "expression"
      message: "Warning message"
```

## Migration Guide

### From Previous Format

If you have existing previous format files, they need to be converted to YAML or JSON:

1. **Convert previous format to YAML/JSON**: Use the existing conversion tools
2. **Update validation calls**: Remove any previous format specific validation
3. **Use new CLI flags**: Replace custom validation with `--mode` and `--spec`

### From Custom Validation

If you have custom validation logic:

1. **Create specification overlay**: Convert custom rules to OCD specification format
2. **Update validation calls**: Use `--spec` flag instead of custom validation
3. **Test thoroughly**: Ensure all custom rules work as expected

## Best Practices

### Choosing Validation Mode

- **Use relaxed mode** for:
  - Development and prototyping
  - Creative workflows where flexibility is important
  - Legacy character data migration

- **Use strict mode** for:
  - Production systems
  - Data quality assurance
  - API validation endpoints

### Creating Specification Overlays

- **Start with defaults**: Begin with the default specification and override only what you need
- **Document custom rules**: Include clear descriptions for custom validation rules
- **Test thoroughly**: Validate against various character types to ensure rules work correctly
- **Version control**: Keep specification files in version control alongside your project

### Performance Considerations

- **Cache specifications**: Load and cache specification files when validating multiple characters
- **Use appropriate mode**: Don't use strict mode unless necessary for performance
- **Batch validation**: Validate multiple characters in a single process when possible

## Troubleshooting

### Common Issues

**Specification file not found:**
```bash
Error: Specification file not found: custom-spec.ocd
```
- Ensure the file path is correct
- Check file permissions
- Verify the file exists

**Invalid specification format:**
```bash
Error: Failed to load specification: YAML parse error
```
- Validate your specification file syntax
- Check for proper YAML formatting
- Ensure all required fields are present

**Mode override not working:**
- Check that your specification file has the correct `validation.mode` field
- Ensure the mode value is either "relaxed" or "strict"
- Verify the specification file is being loaded correctly

### Debug Mode

Enable debug output to troubleshoot validation issues:

```bash
# Python
OCD_DEBUG=1 ocd-validate character.yaml --spec custom-spec.ocd

# Node.js
DEBUG=ocd* npx @ocd-tools/validator character.yaml --spec custom-spec.ocd
```
