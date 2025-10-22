# OCD Validation System

The OCD Validation System provides comprehensive validation for Open Character Specification documents using customizable validation rules defined in `.ocd` specification files.

## Overview

The validation system consists of:

- **Validation Modes**: Two modes for different validation strictness levels
- **Specification Files**: Custom `.ocd` files that define validation rules
- **Rule Engine**: Powerful rule system supporting various validation operators
- **Path Matching**: Flexible path selectors for targeting specific document locations
- **Constraint System**: High-level constraints for complex validation scenarios

## Validation Modes

### Relaxed Mode (Default)

- **Structure errors**: Always treated as errors (missing required fields, type mismatches)
- **Data errors**: Treated as warnings (enum violations, pattern mismatches, etc.)
- **Use case**: Development, prototyping, gradual validation adoption

### Strict Mode

- **Structure errors**: Treated as errors
- **Data errors**: Treated as errors
- **Use case**: Production, CI/CD pipelines, strict compliance

## Specification Files

Validation rules are defined in `.ocd` files using the OCD Validation Specification format:

```yaml
id: my-project-spec
type: validationSpec
schemaVersion: 1
metadata:
  name: "My Project Validation"
  description: "Custom validation rules for my project"

policy:
  allowUnknownFields: true
  unknownFieldSeverity: warning

definitions:
  enums:
    Species: ["human", "elf", "dwarf", "orc"]
  
rules:
  - path: "identity.species"
    enum: "@enums.Species"
    message: "Species must be from the allowed list"

constraints:
  disallow:
    tags: ["test", "draft"]
```

### Key Features

- **Inheritance**: Use `extends` to build upon existing specifications
- **References**: Define reusable enums and types with `@enums.Name` and `@types.Name`
- **Flexible Rules**: Target any path in the document with powerful operators
- **Constraints**: High-level constraints for complex validation scenarios

## Rule Operators

### Presence Control

```yaml
- path: "required.field"
  presence: required

- path: "optional.field"
  presence: optional

- path: "forbidden.field"
  presence: forbidden
```

### Type Validation

```yaml
- path: "name"
  type: string

- path: "age"
  type: integer
  min: 0
  max: 150

- path: "tags"
  type: array
  minItems: 1
  maxItems: 10
```

### Enum Constraints

```yaml
definitions:
  enums:
    Status: ["active", "inactive", "pending"]

rules:
  - path: "status"
    enum: "@enums.Status"
```

### String Validation

```yaml
- path: "email"
  type: string
  format: email

- path: "username"
  type: string
  pattern: "^[a-zA-Z0-9_]+$"
  minLength: 3
  maxLength: 20
```

### Array Constraints

```yaml
- path: "skills"
  type: array
  uniqueItems: true
  minItems: 1
  maxItems: 5
  items:
    type: string
```

## Path Selectors

Path selectors use dot notation with special array syntax:

- `field` - Direct field access
- `nested.field` - Nested object access
- `array[]` - All items in an array
- `array[*]` - All items in an array (alternative syntax)
- `array[0]` - Specific array index

## Constraint System

### Required/Forbidden Paths

```yaml
constraints:
  require:
    - "identity.name"
    - "identity.species"
  
  forbid:
    - "internal.debug"
    - "temp.data"
```

### Tag Restrictions

```yaml
constraints:
  disallow:
    tags: ["test", "draft", "placeholder"]
```

### Array Constraints

```yaml
constraints:
  arrays:
    unique:
      - path: "skills"
      - path: "tags"
    
    minItems:
      - path: "abilities"
        value: 1
```

## CLI Usage

### Python Validator

```bash
# Basic validation
ocd-validate character.yaml

# Strict mode
ocd-validate character.yaml --mode strict

# Custom specification
ocd-validate character.yaml --spec my-project-spec.ocd

# JSON output
ocd-validate character.yaml --output json

# Print normalized result
ocd-validate character.yaml --print
```

### Node Validator

```bash
# Basic validation
npx @ocd-tools/validator character.yaml

# Strict mode
npx @ocd-tools/validator character.yaml --mode strict

# Custom specification
npx @ocd-tools/validator character.yaml --spec my-project-spec.ocd

# JSON output
npx @ocd-tools/validator character.yaml --output json
```

## Integration

### Python Integration

```python
from ocd.validate.validator import validate_and_normalize

result = validate_and_normalize(
    character_data,
    mode="strict",
    spec_path="my-project-spec.ocd"
)

if result["ok"]:
    print("Validation passed")
    normalized_data = result["data"]
else:
    print("Validation failed")
    for error in result["errors"]:
        print(f"Error: {error['msg']}")
```

### Node Integration

```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

const result = await validateAndNormalize(
  characterData,
  'strict',
  'my-project-spec.ocd'
);

if (result.ok) {
  console.log('Validation passed');
  const normalizedData = result.data;
} else {
  console.log('Validation failed');
  for (const error of result.errors || []) {
    console.log(`Error: ${error.message}`);
  }
}
```

## Best Practices

1. **Start Simple**: Begin with basic type and presence validation
2. **Use Enums**: Define reusable value sets for consistency
3. **Leverage Inheritance**: Build complex specs by extending simpler ones
4. **Test Thoroughly**: Validate against diverse character data
5. **Document Rules**: Use meaningful messages for validation failures
6. **Progressive Strictness**: Start relaxed, move to strict as rules mature

## Error Handling

The validation system provides detailed error information:

- **Error Codes**: Standardized codes for programmatic handling
- **Path Information**: Exact location of validation failures
- **Severity Levels**: Distinguish between errors and warnings
- **Custom Messages**: Meaningful descriptions for end users

## Migration from OCD-T

If you're migrating from the old OCD-T format, see the [Migration Guide](../migration-guide.md) for detailed instructions on converting your validation rules to the new specification format.
