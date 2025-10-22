# Glossary

**OCD** (Open Character Specification) - The overall standard for defining character data in a structured, portable format.

**Character Specification** - A character file (YAML or JSON) that describes a character's attributes, traits, profile, and other properties according to the OCD format.

**OCD Validation Specification** (.ocd file) - A validation rule file that defines constraints and requirements for character data. These files use the `.ocd` extension and follow the OCD Validation Spec schema.

**Validation Mode** - The strictness level for validation:
- **Relaxed**: Structure errors are errors; data errors are warnings
- **Strict**: Both structure and data errors are errors

**Bipolar trait** - A trait axis with two poles and `polarity`/`intensity` values.

**Scalar trait** - A trait with a single normalized value (0..1).

**Flag trait** - A boolean trait indicating presence/absence.

**Structure Error** - Validation error related to required fields, types, or document structure. Always treated as errors regardless of mode.

**Data Error** - Validation error related to data constraints (enums, patterns, ranges). Severity depends on validation mode unless overridden.