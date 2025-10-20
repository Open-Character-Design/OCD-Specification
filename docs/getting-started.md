# Getting Started

Welcome to OCS! This guide will get you up and running with character validation in minutes.

## Installation

Choose your preferred validator:

=== "Python"

    ```bash
    pip install ocs==1.0.0
    ```

    **System Requirements:**
    - Python 3.8 or higher
    - pip package manager

=== "Node.js"

    ```bash
    npm install @ocs-tools/validator@1.0.0
    ```

    **System Requirements:**
    - Node.js 16 or higher
    - npm package manager

=== "Global Installation"

    ```bash
    # Python
    pip install --global ocs==1.0.0

    # Node.js
    npm install --global @ocs-tools/validator@1.0.0
    ```

## Quick Validation

Let's validate your first character! Download this sample file:

```yaml title="sample-character.yaml"
ocs_version: "0.0.1"
id: "char-sample-hero"
names:
  canon: "Sample Hero"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

Save it as `sample-character.yaml` and run:

=== "Python"

    ```bash
    ocs-validate sample-character.yaml
    ```

=== "Node.js"

    ```bash
    npx @ocs-tools/validator sample-character.yaml
    ```

You should see:

```
✅ Validation successful
📝 0 warnings
```

!!! tip "Success!"
    If you see this output, your validator is working correctly and the character is valid!

## Understanding Validation Output

The validator provides three types of feedback:

### ✅ Success
```
✅ Validation successful
📝 0 warnings
```

### ⚠️ Warnings
```
✅ Validation successful
⚠️ 1 warning:
  - NORMALIZED_SLUG: Slug 'my_character' normalized to 'my-character'
```

### ❌ Errors
```
❌ Validation failed
🚨 2 errors:
  - Missing required field: ocs_version
  - Invalid identity kind: 'invalid-kind'
```

## Your First Character

Let's create a complete character step by step:

### Step 1: Basic Information

```yaml title="my-hero.yaml"
ocs_version: "0.0.1"
id: "char-my-hero"
names:
  canon: "My Hero"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Step 2: Add Personality

```yaml title="my-hero-with-personality.yaml"
ocs_version: "0.0.1"
id: "char-my-hero"
names:
  canon: "My Hero"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  summary: "Brave and determined adventurer"
  traits:
    - name: "introversion↔extraversion"
      kind: "bipolar"
      polarity: 0.5
      intensity: 0.7
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.8
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Step 3: Validate and Test

```bash
ocs-validate my-hero-with-personality.yaml
```

!!! note "Understanding Traits"
    - **Bipolar traits**: Range from -1 to 1, with intensity 0 to 1
    - **Scalar traits**: Single value from 0 to 1
    - **Flag traits**: Boolean true/false

## Common Issues and Solutions

### Missing Required Fields

**Error:** `Missing required field: ocs_version`

**Solution:** Add the missing field:
```yaml
ocs_version: "0.0.1"
```

### Invalid Field Values

**Error:** `Invalid identity kind: 'invalid-kind'`

**Solution:** Use a valid identity kind:
```yaml
identity:
  kind: "humanoid"  # Valid options: humanoid, animal, construct, etc.
```

### Timestamp Format Issues

**Error:** `Invalid timestamp format`

**Solution:** Use ISO 8601 format:
```yaml
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"  # Correct format
    last_modified: "2024-01-01T00:00:00Z"
```

### Unresolved References

**Warning:** `UNRESOLVED_REF: Reference 'char-other-character' not found`

**Solution:** Create the referenced character or remove the reference:
```yaml
relationships:
  - target_ref: "char-other-character"  # This character must exist
    role: "friend"
    sentiment: 0.8
```

## Advanced Validation Options

### Print Normalized Output

See how the validator normalizes your character:

```bash
ocs-validate my-hero.yaml --print
```

This shows the normalized JSON output with:
- Trait names standardized
- Tags lowercased and deduplicated
- Slugs normalized

### Treat Warnings as Errors

For strict validation:

```bash
ocs-validate my-hero.yaml --warnings-as-errors
```

This will fail if any warnings are present.

### Force Input Format

Specify the input format explicitly:

```bash
ocs-validate my-hero.yaml --format yaml
```

## Next Steps

Now that you have the basics, explore further:

<div class="features-grid">

<div class="feature-card">

### 📚 [Tutorial](tutorial/index.md)

Complete step-by-step guide to creating production-ready characters.

</div>

<div class="feature-card">

### 🎭 [Examples Gallery](authoring/examples.md)

Browse character examples from D&D warriors to sci-fi heroes.

</div>

<div class="feature-card">

### 📖 [Specification](spec/schema-overview.md)

Deep dive into the technical details of OCS structure.

</div>

<div class="feature-card">

### 🛠️ [Integration Guide](integration/python-validator.md)

Learn how to integrate OCS into your applications.

</div>

</div>

## Getting Help

If you run into issues:

1. **Check the [FAQ](faq.md)** for common questions
2. **Browse [Examples](authoring/examples.md)** for inspiration
3. **Read the [Specification](spec/schema-overview.md)** for detailed information
4. **Ask on [GitHub Discussions](https://github.com/eVirgil/OpenCharacter-Specification/discussions)**

## Quick Reference

### Required Fields
- `ocs_version`: OCS specification version
- `id`: Unique character identifier
- `names.canon`: Character's canonical name
- `identity.kind`: Entity type (humanoid, animal, etc.)
- `identity.species`: Specific species
- `meta.versioning.created_at`: Creation timestamp
- `meta.versioning.last_modified`: Last modification timestamp

### Valid Identity Kinds
- `humanoid`
- `animal`
- `construct`
- `undead`
- `elemental`
- `celestial`
- `fiend`
- `aberration`
- `plant`
- `ooze`

### Timestamp Format
Always use ISO 8601: `YYYY-MM-DDTHH:mm:ssZ`
Example: `2024-01-01T00:00:00Z`

### Validation Commands
```bash
# Basic validation
ocs-validate character.yaml

# With normalized output
ocs-validate character.yaml --print

# Strict validation (warnings as errors)
ocs-validate character.yaml --warnings-as-errors
```
