# Default OCD Specification

The Default OCD Specification provides a lenient baseline validation for Open Character Design Specification documents. It ensures basic structural integrity while allowing flexibility for diverse character types and use cases.

## Design Philosophy

The default specification follows these principles:

1. **Lenient by Design**: Prioritizes flexibility over strictness
2. **Structural Focus**: Ensures required fields exist and have correct types
3. **Soft Validation**: Treats data issues as warnings rather than errors
4. **Extensible**: Designed to be extended by project-specific specifications

## Specification Overview

```yaml
id: ocd-default-spec
type: validationSpec
schemaVersion: 1
metadata:
  name: Default OCD Specification
  description: Baseline validation and schema for OCD characters
  version: "1.0.0"

policy:
  allowUnknownFields: true
  unknownFieldSeverity: warning
```

### Key Features

- **Unknown Fields Allowed**: Permits additional fields not defined in rules
- **Warning Severity**: Unknown fields generate warnings, not errors
- **Minimal Requirements**: Only enforces essential structural elements

## Required Fields

The default specification requires these essential fields:

### Document Structure

```yaml
rules:
  - path: "ocd_version"
    presence: required
    type: string
    minLength: 1

  - path: "id"
    presence: required
    type: string
    minLength: 1

  - path: "names"
    presence: required
    type: object

  - path: "names.canon"
    presence: required
    type: string
    minLength: 1

  - path: "identity"
    presence: required
    type: object
```

### Identity Requirements

```yaml
  - path: "identity.entity_kind"
    presence: required
    type: string
    enum: "@enums.EntityKind"

  - path: "identity.sapience_level"
    presence: required
    type: string
    enum: "@enums.SapienceLevel"
```

## Enum Definitions

The default specification defines standard enums for common character attributes:

### Entity Types

```yaml
definitions:
  enums:
    EntityKind: ["person", "collective", "creature", "object", "place", "abstract", "ai"]
```

- **person**: Individual human or humanoid characters
- **collective**: Groups, organizations, or collective entities
- **creature**: Non-humanoid living beings
- **object**: Inanimate objects with character traits
- **place**: Locations with personality or character
- **abstract**: Conceptual entities (emotions, ideas, etc.)
- **ai**: Artificial intelligence entities

### Species Types

```yaml
    Species: ["human", "ai", "alien", "collective", "object", "deity", "other"]
```

- **human**: Human characters
- **ai**: Artificial intelligence
- **alien**: Non-human intelligent beings
- **collective**: Group entities
- **object**: Object characters
- **deity**: Divine or supernatural beings
- **other**: Unspecified or custom species

### Sapience Levels

```yaml
    SapienceLevel: ["animal", "tool", "agent", "sapient", "transcendent"]
```

- **animal**: Basic instinctual behavior
- **tool**: Simple programmed responses
- **agent**: Goal-oriented behavior
- **sapient**: Self-aware and reasoning
- **transcendent**: Beyond normal comprehension

### Trait Types

```yaml
    TraitKind: ["bipolar", "scalar", "flag"]
```

- **bipolar**: Traits with opposing poles (introversion ↔ extraversion)
- **scalar**: Traits with numeric scales (strength: 1-10)
- **flag**: Boolean traits (has_wings: true/false)

## Optional Fields

The default specification defines optional fields with type validation:

### Names and Identity

```yaml
  - path: "names.display"
    type: string

  - path: "names.aliases"
    type: array
    items:
      type: string

  - path: "identity.species"
    type: string
    enum: "@enums.Species"

  - path: "identity.pronouns"
    type: array
    items:
      type: string

  - path: "identity.age"
    type: string

  - path: "identity.physical_description"
    type: string
```

### Personality and Traits

```yaml
  - path: "personality"
    type: object

  - path: "personality.summary"
    type: string

  - path: "personality.traits"
    type: array
    items:
      type: object

  - path: "personality.traits[].name"
    type: string

  - path: "personality.traits[].kind"
    type: string
    enum: "@enums.TraitKind"

  - path: "personality.traits[].value"
    type: number

  - path: "personality.quirks"
    type: array
    items:
      type: string

  - path: "personality.motivations"
    type: array
    items:
      type: string
```

### Appearance and Background

```yaml
  - path: "appearance"
    type: object

  - path: "appearance.physical"
    type: object

  - path: "appearance.clothing"
    type: object

  - path: "appearance.accessories"
    type: array
    items:
      type: string

  - path: "background"
    type: object

  - path: "background.history"
    type: string

  - path: "background.culture"
    type: string

  - path: "background.education"
    type: string

  - path: "background.occupation"
    type: string
```

### Relationships and Metadata

```yaml
  - path: "relationships"
    type: array
    items:
      type: object

  - path: "relationships[].character_id"
    type: string

  - path: "relationships[].relationship_type"
    type: string

  - path: "relationships[].description"
    type: string

  - path: "meta"
    type: object

  - path: "meta.tags"
    type: array
    items:
      type: string
    maxLength: 32

  - path: "meta.genres"
    type: array
    items:
      type: string

  - path: "meta.media"
    type: array
    items:
      type: string

  - path: "meta.content_rating"
    type: string

  - path: "meta.character_content_profile"
    type: object
    presence: optional

  - path: "meta.character_content_profile.target_audience"
    type: object
    presence: optional

  - path: "meta.character_content_profile.target_audience.age_range"
    type: string
    presence: optional

  - path: "meta.character_content_profile.target_audience.demographics"
    type: string
    presence: optional

  - path: "meta.character_content_profile.target_audience.tone_alignment"
    type: string
    presence: optional

  - path: "meta.character_content_profile.appropriateness"
    type: object
    presence: optional

  - path: "meta.character_content_profile.appropriateness.violence_level"
    type: string
    enum: ["none", "cartoon", "realistic", "extreme"]
    presence: optional

  - path: "meta.character_content_profile.appropriateness.sexuality_level"
    type: string
    enum: ["none", "implied", "explicit"]
    presence: optional

  - path: "meta.character_content_profile.appropriateness.language_level"
    type: string
    enum: ["clean", "mild", "strong", "explicit"]
    presence: optional

  - path: "meta.character_content_profile.appropriateness.cultural_sensitivity"
    type: array
    items:
      type: string
    presence: optional

  - path: "meta.character_content_profile.content_rating"
    type: array
    items:
      type: object
    presence: optional

  - path: "meta.character_content_profile.content_rating[].system"
    type: string
    enum: ["ESRB", "PEGI", "IARC", "MPA", "CERO", "USK", "ACB"]
    presence: required

  - path: "meta.character_content_profile.content_rating[].rating"
    type: string
    presence: required

  - path: "meta.character_content_profile.content_rating[].notes"
    type: string
    presence: optional

  - path: "meta.character_content_profile.deployment_contexts"
    type: array
    items:
      type: string
    presence: optional

  - path: "meta.character_content_profile.safety_warnings"
    type: array
    items:
      type: string
    presence: optional

  - path: "meta.versioning"
    type: object

  - path: "extensions"
    type: object
```

## Usage Examples

### Basic Character

```yaml
ocd_version: "0.0.1"
id: "char-001"
names:
  canon: "Aria Ironleaf"
identity:
  entity_kind: "person"
  species: "elf"
  sapience_level: "sapient"
```

### Extended Character

```yaml
ocd_version: "0.0.1"
id: "char-002"
names:
  canon: "Zed Nova"
  aliases: ["Zed", "Nova"]
identity:
  entity_kind: "person"
  species: "android"
  sapience_level: "sapient"
  pronouns: ["they", "them"]
personality:
  summary: "Curious and analytical"
  traits:
    - name: "curiosity"
      kind: "scalar"
      value: 8
meta:
  tags: ["sci-fi", "android", "analyst"]
```

### Character with Content Rating

```yaml
ocd_version: "0.0.1"
id: "char-003"
names:
  canon: "Seraphine Fireblade"
identity:
  entity_kind: "person"
  species: "human"
  sapience_level: "sapient"
meta:
  character_content_profile:
    target_audience:
      age_range: "16+"
      demographics: "Fans of action RPGs; teen and adult players"
      tone_alignment: "gritty"
    appropriateness:
      violence_level: "realistic"
      sexuality_level: "implied"
      language_level: "mild"
      cultural_sensitivity:
        - "Depicts religious iconography in dark fantasy context"
    content_rating:
      - system: "ESRB"
        rating: "T for Teen"
        notes: "Rated T for fantasy violence, mild language, and suggestive themes"
      - system: "PEGI"
        rating: "16"
        notes: "Realistic-looking violence against humans and non-explicit sexual content"
    deployment_contexts:
      - "teen action RPG"
      - "fantasy-themed digital comic"
    safety_warnings:
      - "Mild horror elements (demonic transformations, possession)"
      - "Fantasy violence with blood"
  tags: ["demon-hunter", "dark-fantasy", "action-rpg"]
```

## Content Rating Validation

The default specification includes comprehensive validation for character content profiles under the `meta.character_content_profile` field. This optional field enables responsible character deployment across different platforms and audiences.

### Validation Rules

- **Optional Fields**: All content profile fields are optional, even in strict validation mode
- **Enum Validation**: Restricted values enforced for violence_level, sexuality_level, language_level
- **System Validation**: Rating system must be from approved list (ESRB, PEGI, IARC, MPA, CERO, USK, ACB)
- **Structure Validation**: Nested objects validated for proper types and required fields

### Content Level Enums

**Violence Level**: `none`, `cartoon`, `realistic`, `extreme`
**Sexuality Level**: `none`, `implied`, `explicit`
**Language Level**: `clean`, `mild`, `strong`, `explicit`
**Rating Systems**: `ESRB`, `PEGI`, `IARC`, `MPA`, `CERO`, `USK`, `ACB`

### Validation Examples

```yaml
# Valid content profile
meta:
  character_content_profile:
    appropriateness:
      violence_level: "realistic"  # Valid enum value
    content_rating:
      - system: "ESRB"             # Valid rating system
        rating: "T for Teen"       # Required field
        notes: "Fantasy violence"  # Optional field

# Invalid content profile (will generate warnings)
meta:
  character_content_profile:
    appropriateness:
      violence_level: "moderate"   # Invalid enum value
    content_rating:
      - system: "INVALID"          # Invalid rating system
        rating: "T for Teen"
      # Missing required 'rating' field
      - system: "ESRB"
```

## Extending the Default Spec

### Project-Specific Extensions

```yaml
id: fantasy-project-spec
type: validationSpec
schemaVersion: 1
extends: ["ocd-default-spec"]

definitions:
  enums:
    FantasySpecies: ["human", "elf", "dwarf", "orc", "halfling"]

rules:
  - path: "identity.species"
    enum: "@enums.FantasySpecies"
    message: "Only fantasy species allowed in this project"

constraints:
  disallow:
    tags: ["sci-fi", "modern", "futuristic"]
```

### Genre-Specific Extensions

```yaml
id: sci-fi-project-spec
type: validationSpec
schemaVersion: 1
extends: ["ocd-default-spec"]

definitions:
  enums:
    SciFiSpecies: ["human", "android", "alien", "cyborg"]

rules:
  - path: "identity.species"
    enum: "@enums.SciFiSpecies"

constraints:
  disallow:
    tags: ["fantasy", "medieval", "magic"]
```

## Validation Behavior

### Relaxed Mode (Default)

- **Structure Errors**: Missing required fields → Error
- **Type Errors**: Wrong data types → Error
- **Data Errors**: Invalid enum values, pattern mismatches → Warning
- **Unknown Fields**: Additional fields → Warning

### Strict Mode

- **All Errors**: All validation failures → Error
- **Unknown Fields**: Additional fields → Error (if policy allows)

## Best Practices

1. **Start with Default**: Use the default spec as your baseline
2. **Extend Gradually**: Add project-specific rules incrementally
3. **Test Thoroughly**: Validate against diverse character data
4. **Document Extensions**: Explain why custom rules are needed
5. **Consider Impact**: Balance strictness with flexibility

## Migration Notes

The default specification replaces the previous validation format. Key changes:

- **Unified Format**: All validation now uses `.ocd` specification files
- **Flexible Rules**: More powerful rule system than previous formats
- **Better Error Handling**: Detailed error codes and messages
- **Extensible Design**: Easy to customize for specific projects

For migration from previous formats, see the [Migration Guide](../migration-guide.md).
