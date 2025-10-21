# Diagnostics Reference

Comprehensive reference for OCD validation diagnostics, warnings, and error messages.

## Understanding Diagnostics

OCD validators provide three types of feedback:

- **✅ Success**: Character is valid with no issues
- **⚠️ Warnings**: Suggestions for improvement (validation still succeeds)
- **❌ Errors**: Critical issues that prevent validation

## Warning Codes

### Content Rating Warnings

#### `RATING_CONFLICT`
**Severity:** Warning  
**Description:** Conflict between personality traits and content appropriateness ratings.

**Example:**
```yaml
personality:
  traits:
    - name: "violent-pacifist"
      polarity: 0.8  # Leans violent
meta_properties:
  appropriateness:
    violence: "none"  # But rated as no violence
```

**How to Fix:**
- Adjust trait polarity to match content rating
- Update content rating to match character traits
- Add justification in character notes

### Reference Resolution Warnings

#### `UNRESOLVED_REF`
**Severity:** Warning  
**Description:** Character reference cannot be resolved.

**Example:**
```yaml
background:
  relationships:
    - target_ref: "char-nonexistent-character"
      role: "friend"
```

**How to Fix:**
- Create the referenced character
- Remove the reference
- Use a placeholder ID with documentation

### Missing Information Warnings

#### `MISSING_SKILL_TAGS`
**Severity:** Warning  
**Description:** Skills without appropriate categorization tags.

**Example:**
```yaml
capabilities:
  skills:
    - name: "Sword Fighting"
      level: 3
      # Missing tags
```

**How to Fix:**
- Add relevant tags: `["combat", "melee", "martial"]`
- Use standardized tag vocabulary

#### `MISSING_CANON_NAME`
**Severity:** Warning  
**Description:** Character lacks a canonical name.

**Example:**
```yaml
names:
  aliases: ["The Hero", "Champion"]
  # Missing canon field
```

**How to Fix:**
- Add `canon` field with primary name
- Use most commonly known name

#### `NONCANONICAL_CANON_NAME`
**Severity:** Warning  
**Description:** Canonical name doesn't follow naming conventions.

**Example:**
```yaml
names:
  canon: "the-hero-001"  # Should be proper name
```

**How to Fix:**
- Use proper character name: `"Rita"` or `"Sir Galahad"`
- Avoid IDs or codes in canon field

### Composite Identity Warnings

#### `COMPOSITE_CONTROL_SHARE_OVERFLOW`
**Severity:** Warning  
**Description:** Composite control shares exceed 1.0 total.

**Example:**
```yaml
identity:
  composite_of:
    - identity: "char-form-1"
      control_share: 0.6
    - identity: "char-form-2"
      control_share: 0.7  # Total: 1.3
```

**How to Fix:**
- Adjust control shares to sum to 1.0 or less
- Redistribute control proportionally

#### `COMPOSITE_SECRET_WITHOUT_IDENTITY`
**Severity:** Warning  
**Description:** Secret composite identity lacks proper identity definition.

**Example:**
```yaml
identity:
  secret_identities:
    - identity: "char-batman"
      exposure: "secret"
      # Missing char-batman character
```

**How to Fix:**
- Create the secret identity character
- Remove the secret identity reference
- Document the relationship properly

#### `COMPOSITE_SECRET_IDENTITY_MISMATCH`
**Severity:** Warning  
**Description:** Secret identity doesn't match expected character.

**Example:**
```yaml
identity:
  secret_identities:
    - identity: "char-batman"
      exposure: "secret"
# char-batman is actually Bruce Wayne, not Batman
```

**How to Fix:**
- Correct the identity reference
- Update character relationships
- Clarify identity structure

### Normalization Warnings

#### `NORMALIZED_SLUG`
**Severity:** Info  
**Description:** Slug was normalized to standard format.

**Example:**
```yaml
id: "char_my_character"  # Normalized to "char-my-character"
```

**How to Fix:**
- Use hyphenated format: `"char-my-character"`
- Update references to use normalized ID

#### `NORMALIZED_AXIS`
**Severity:** Info  
**Description:** Trait axis name was normalized to standard format.

**Example:**
```yaml
personality:
  traits:
    - name: "introversion-extraversion"  # Normalized to "introversion-extraversion"
```

**How to Fix:**
- Use `-` separator for bipolar traits
- Update trait names to use standard format

#### `NORMALIZED_TAGS`
**Severity:** Info  
**Description:** Tags were normalized (lowercased, deduplicated).

**Example:**
```yaml
meta:
  tags: ["ADVENTURER", "Hero", "adventurer"]  # Normalized to ["adventurer", "hero"]
```

**How to Fix:**
- Use lowercase tags
- Remove duplicates
- Follow tag vocabulary standards

### Definition vs Runtime Warnings

#### `DEFINITION_RUNTIME_FIELD`
**Severity:** Warning  
**Description:** Runtime fields found in character definition.

**Example:**
```yaml
# In character definition (should be in runtime state)
state_dynamics:
  health: 0.8  # This should be in runtime, not definition
```

**How to Fix:**
- Move runtime fields to appropriate runtime state
- Keep definitions static and portable
- Use state management for dynamic values

## Error Codes

### Required Field Errors

#### `MISSING_REQUIRED_FIELD`
**Severity:** Error  
**Description:** Required field is missing.

**Common Missing Fields:**
- `ocd_version`
- `id`
- `names.canon`
- `identity.kind`
- `identity.species`
- `meta.versioning.created_at`
- `meta.versioning.last_modified`

**How to Fix:**
- Add all required fields
- Use proper field names and types
- Follow field reference documentation

### Validation Errors

#### `INVALID_FIELD_VALUE`
**Severity:** Error  
**Description:** Field value doesn't match expected type or constraints.

**Examples:**
```yaml
# Invalid identity kind
identity:
  kind: "invalid-kind"  # Must be valid enum

# Invalid timestamp format
meta:
  versioning:
    created_at: "January 1, 2024"  # Must be ISO 8601

# Invalid trait polarity
personality:
  traits:
    - name: "introversion-extraversion"
      polarity: 1.5  # Must be between -1 and 1
```

**How to Fix:**
- Use valid enum values
- Follow ISO 8601 timestamp format
- Ensure trait values are within valid ranges

#### `INVALID_SCHEMA_VERSION`
**Severity:** Error  
**Description:** OCD version is not supported.

**Example:**
```yaml
ocd_version: "99.99.99"  # Unsupported version
```

**How to Fix:**
- Use supported OCD version: `"0.0.1"`
- Check validator compatibility
- Update to latest version

#### `INVALID_TIMESTAMP_FORMAT`
**Severity:** Error  
**Description:** Timestamp doesn't use ISO 8601 format.

**Example:**
```yaml
meta:
  versioning:
    created_at: "2024-01-01"  # Missing time and timezone
```

**How to Fix:**
- Use full ISO 8601 format: `"2024-01-01T00:00:00Z"`
- Include time and timezone information
- Validate timestamp format

## Diagnostic Categories

### Content Quality Warnings
- `RATING_CONFLICT`
- `MISSING_SKILL_TAGS`
- `MISSING_CANON_NAME`
- `NONCANONICAL_CANON_NAME`

### Structural Warnings
- `UNRESOLVED_REF`
- `COMPOSITE_CONTROL_SHARE_OVERFLOW`
- `COMPOSITE_SECRET_WITHOUT_IDENTITY`
- `COMPOSITE_SECRET_IDENTITY_MISMATCH`

### Normalization Info
- `NORMALIZED_SLUG`
- `NORMALIZED_AXIS`
- `NORMALIZED_TAGS`

### Runtime vs Definition
- `DEFINITION_RUNTIME_FIELD`

### Critical Errors
- `MISSING_REQUIRED_FIELD`
- `INVALID_FIELD_VALUE`
- `INVALID_SCHEMA_VERSION`
- `INVALID_TIMESTAMP_FORMAT`

## Validation Workflow

### Pre-Validation Checklist
- [ ] All required fields present
- [ ] Valid OCD version specified
- [ ] Proper timestamp format
- [ ] Valid enum values
- [ ] Trait values within ranges

### Post-Validation Actions
- [ ] Review all warnings
- [ ] Fix critical errors
- [ ] Address content quality issues
- [ ] Resolve reference problems
- [ ] Update normalized fields

### Continuous Validation
- [ ] Validate on every change
- [ ] Use `--warnings-as-errors` in CI/CD
- [ ] Monitor for new diagnostic codes
- [ ] Update validation rules as needed

## Best Practices

### Preventing Warnings
1. **Use Standard Formats**
   - Hyphenated IDs: `"char-rita-adventurer"`
   - ISO 8601 timestamps: `"2024-01-01T00:00:00Z"`
   - Standard trait names: `"introversion-extraversion"`

2. **Complete Character Information**
   - Add skill tags for categorization
   - Include canonical names
   - Provide comprehensive metadata

3. **Consistent Content Ratings**
   - Align traits with appropriateness ratings
   - Document rating decisions
   - Review for conflicts

### Handling Errors
1. **Required Fields**
   - Always include all required fields
   - Use proper field names and types
   - Validate against schema

2. **Field Values**
   - Use valid enum values
   - Follow type constraints
   - Validate ranges and formats

3. **References**
   - Ensure referenced characters exist
   - Use consistent ID formats
   - Document relationships

## Diagnostic Tools

### Command Line Validation
```bash
# Basic validation
ocd-validate character.yaml

# With warnings as errors
ocd-validate character.yaml --warnings-as-errors

# Print normalized output
ocd-validate character.yaml --print
```

### Programmatic Validation
```python
from ocd.ocd_validate import validate_and_normalize

result = validate_and_normalize(document)
if result["ok"]:
    print("Valid:", result["data"])
    print("Warnings:", result["warnings"])
else:
    print("Errors:", result["errors"])
```

### Batch Validation
```bash
# Validate all characters
find . -name "*.yaml" -exec ocd-validate {} \;

# Validate with error on warnings
find . -name "*.yaml" -exec ocd-validate {} --warnings-as-errors \;
```

## Troubleshooting Common Issues

### "Character validates but doesn't work in my game"
- Check for missing extension data
- Verify system-specific requirements
- Ensure complete character information

### "Getting too many warnings"
- Review warning categories
- Focus on content quality warnings
- Use `--warnings-as-errors` for strict validation

### "References not resolving"
- Create referenced characters
- Use consistent ID formats
- Check file paths and locations

### "Timestamps always invalid"
- Use ISO 8601 format: `YYYY-MM-DDTHH:mm:ssZ`
- Include time and timezone
- Validate format before submission

## Quick Reference

### Required Fields
- `ocd_version`, `id`, `names.canon`
- `identity.kind`, `identity.species`
- `meta.versioning.created_at`, `meta.versioning.last_modified`

### Common Warning Codes
- `RATING_CONFLICT` - Trait/rating mismatch
- `UNRESOLVED_REF` - Missing character reference
- `MISSING_SKILL_TAGS` - Skills without tags
- `NORMALIZED_SLUG` - ID format normalized

### Critical Error Codes
- `MISSING_REQUIRED_FIELD` - Required field missing
- `INVALID_FIELD_VALUE` - Invalid field value
- `INVALID_TIMESTAMP_FORMAT` - Bad timestamp format

### Validation Commands
```bash
# Basic validation
ocd-validate character.yaml

# Strict validation
ocd-validate character.yaml --warnings-as-errors

# Normalized output
ocd-validate character.yaml --print
```
