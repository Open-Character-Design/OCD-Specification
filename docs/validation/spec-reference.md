# OCD Validation Specification Reference

Complete reference for the OCD Validation Specification format, operators, and validation rules.

## Specification Structure

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the specification |
| `type` | string | Yes | Must be `"validationSpec"` |
| `schemaVersion` | integer | Yes | Schema version (currently `1`) |
| `extends` | string[] | No | Array of specification IDs to inherit from |
| `metadata` | object | No | Metadata about the specification |
| `policy` | object | No | Validation policy settings |
| `definitions` | object | No | Reusable definitions (enums, types, patterns) |
| `rules` | object[] | No | Array of validation rules |
| `constraints` | object | No | High-level constraints |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable name |
| `description` | string | Description of the specification |
| `version` | string | Version string |

### Policy Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `allowUnknownFields` | boolean | `true` | Allow fields not defined in rules |
| `allowUnknownTopLevel` | boolean | `true` | Allow unknown top-level fields |
| `unknownFieldSeverity` | string | `"warning"` | Severity for unknown fields |

## Rule Operators

### Presence Control

Controls whether fields must be present, optional, or forbidden.

```yaml
- path: "required.field"
  presence: required    # Field must exist

- path: "optional.field"
  presence: optional    # Field may exist

- path: "forbidden.field"
  presence: forbidden   # Field must not exist
```

### Type Validation

Validates the data type of values.

```yaml
- path: "name"
  type: string          # Must be a string

- path: "age"
  type: integer         # Must be an integer

- path: "score"
  type: number          # Must be a number

- path: "active"
  type: boolean         # Must be a boolean

- path: "data"
  type: object          # Must be an object

- path: "items"
  type: array           # Must be an array
```

### Enum Constraints

Restricts values to a predefined set.

```yaml
definitions:
  enums:
    Status: ["active", "inactive", "pending"]
    Priority: ["low", "medium", "high"]

rules:
  - path: "status"
    enum: "@enums.Status"    # Reference to enum definition

  - path: "priority"
    enum: ["low", "medium", "high"]  # Inline enum
```

### Constant Values

Requires exact value matches.

```yaml
- path: "version"
  const: "1.0"          # Must be exactly "1.0"

- path: "enabled"
  const: true           # Must be exactly true
```

### Numeric Constraints

Validates numeric ranges and limits.

```yaml
- path: "age"
  type: integer
  min: 0                # Minimum value
  max: 150              # Maximum value

- path: "score"
  type: number
  min: 0.0
  max: 100.0
```

### String Constraints

Validates string length, patterns, and formats.

```yaml
- path: "username"
  type: string
  minLength: 3          # Minimum length
  maxLength: 20         # Maximum length
  pattern: "^[a-zA-Z0-9_]+$"  # Regex pattern

- path: "email"
  type: string
  format: email         # Built-in email format

- path: "website"
  type: string
  format: url           # Built-in URL format
```

### Array Constraints

Validates array properties and contents.

```yaml
- path: "skills"
  type: array
  minItems: 1           # Minimum number of items
  maxItems: 10          # Maximum number of items
  uniqueItems: true     # All items must be unique
  items:                # Validate each item
    type: string
    minLength: 1
```

### Object Constraints

Validates object properties.

```yaml
- path: "address"
  type: object
  properties:           # Validate object properties
    street:
      type: string
      minLength: 1
    city:
      type: string
      minLength: 1
    zipCode:
      type: string
      pattern: "^[0-9]{5}$"
```

### Dependent Requirements

Requires fields based on other field values.

```yaml
- path: "contact"
  type: object
  dependentRequired:    # If email exists, phone is required
    email: ["phone"]
    phone: ["email"]
```

### Comparison Constraints

Compares values with other fields.

```yaml
- path: "endDate"
  type: string
  compare:
    greaterThan: "startDate"    # Must be after startDate
    lessThan: "deadline"         # Must be before deadline
```

## Path Language

### Basic Syntax

- `field` - Direct field access
- `nested.field` - Nested object access
- `array[0]` - Specific array index
- `array[]` - All items in array
- `array[*]` - All items in array (alternative)

### Examples

```yaml
# Target specific fields
- path: "name"
- path: "identity.species"
- path: "personality.traits[0].name"

# Target all array items
- path: "skills[]"
- path: "personality.traits[*].value"

# Target nested arrays
- path: "relationships[].character_id"
```

## Constraint System

### Required Paths

```yaml
constraints:
  require:
    - "identity.name"           # String path
    - path: "identity.species" # Object with path property
```

### Forbidden Paths

```yaml
constraints:
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
    unique:                    # Ensure array uniqueness
      - path: "skills"
      - path: "tags"
    
    minItems:                  # Minimum array lengths
      - path: "abilities"
        value: 1
      - path: "equipment"
        value: 0
    
    maxItems:                  # Maximum array lengths
      - path: "spells"
        value: 10
```

## Definitions

### Enums

Define reusable value sets.

```yaml
definitions:
  enums:
    Species: ["human", "elf", "dwarf", "orc", "halfling"]
    Status: ["active", "inactive", "pending", "archived"]
    Priority: ["low", "medium", "high", "critical"]
```

### Types

Define reusable type definitions.

```yaml
definitions:
  types:
    EmailAddress:
      type: string
      format: email
      minLength: 5
      maxLength: 100
    
    PositiveInteger:
      type: integer
      min: 1
    
    NonEmptyString:
      type: string
      minLength: 1
```

### Patterns

Define reusable regex patterns.

```yaml
definitions:
  patterns:
    Username: "^[a-zA-Z0-9_]{3,20}$"
    PhoneNumber: "^\\+?[1-9]\\d{1,14}$"
    Slug: "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$"
```

## Inheritance

### Extending Specifications

```yaml
id: fantasy-project-spec
type: validationSpec
schemaVersion: 1
extends: ["ocd-default-spec"]  # Inherit from default spec

# Add additional rules
rules:
  - path: "species"
    enum: ["human", "elf", "dwarf", "orc"]  # Override default species
```

### Rule Override Behavior

- Rules with the same path and operator combination override parent rules
- Child specifications take precedence over parent specifications
- Definitions are merged (child values override parent values)

## Severity Levels

### Rule-Level Severity

```yaml
- path: "optional.field"
  type: string
  severity: warning     # Override default severity for this rule
```

### Mode-Based Severity

- **Relaxed Mode**: Data validation errors become warnings
- **Strict Mode**: All validation errors remain errors
- **Structure Errors**: Always errors regardless of mode

## Error Codes

Standard error codes for programmatic handling:

| Code | Description |
|------|-------------|
| `REQUIRED_FIELD_MISSING` | Required field is not present |
| `FORBIDDEN_FIELD_PRESENT` | Forbidden field is present |
| `TYPE_MISMATCH` | Value type doesn't match expected type |
| `INVALID_ENUM_VALUE` | Value not in allowed enum set |
| `CONST_MISMATCH` | Value doesn't match required constant |
| `VALUE_TOO_SMALL` | Numeric value below minimum |
| `VALUE_TOO_LARGE` | Numeric value above maximum |
| `STRING_TOO_SHORT` | String length below minimum |
| `STRING_TOO_LONG` | String length above maximum |
| `PATTERN_MISMATCH` | String doesn't match regex pattern |
| `INVALID_FORMAT` | String doesn't match format requirement |
| `ARRAY_TOO_SHORT` | Array has too few items |
| `ARRAY_TOO_LONG` | Array has too many items |
| `ARRAY_NOT_UNIQUE` | Array contains duplicate items |

## Built-in Formats

Supported string formats:

- `email` - Email address format
- `uri` - URI format
- `url` - URL format
- `uuid` - UUID format
- `date` - Date format (YYYY-MM-DD)
- `date-time` - ISO 8601 datetime format
- `slug` - URL-friendly slug format
- `locale` - Locale format (e.g., en-US)
- `language-code` - ISO 639 language code
