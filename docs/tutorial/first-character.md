# Step 1: Your First Character

In this step, you'll create your first OCD character and learn the fundamentals of validation.

## What You'll Build

A minimal but complete character definition that demonstrates the core OCD structure.

## Installation

First, let's install a validator so you can check your work:

=== "Python"

    ```bash
    pip install ocd
    ```

=== "Node.js"

    ```bash
    npm install @ocd-tools/validator
    ```

## Creating Your First Character

Let's start with the simplest possible character format. Create a new file called `virgil.yaml` with this minimal content:

```yaml title="virgil.yaml"
name: "Virgil Hawkins"
type: "humanoid"
summary: "A man with a passion for science and technology who can control electricity and magnetism."
```

This minimal format requires only three fields:
- **`name`**: The character's canonical name
- **`type`**: The entity type (must be one of: `person`, `collective`, `creature`, `object`, `place`, `abstract`, `ai`)
- **`summary`**: A brief description of the character

!!! note "Minimal Format"
    This minimal format is perfect for quick character creation. Future validator releases will automatically expand it to the full OCD format by adding required fields like `ocd_version`, `id`, and metadata.

## Understanding the Structure

Let's break down each field:

### Minimal Format Fields

- **`name`**: The character's canonical name (maps to `names.canon` in full format)
- **`type`**: The type of entity (maps to `identity.entity_kind` in full format)
- **`summary`**: A brief character description (becomes a top-level field in full format)

### Valid Type Values

The `type` field must be one of these values:
- `person` - Human-like beings
- `collective` - Groups or organizations
- `creature` - Non-human animals or beings
- `object` - Inanimate objects with character
- `place` - Locations with personality
- `abstract` - Concepts or ideas
- `ai` - Artificial intelligence entities

## Validating Your Character

Now let's validate your character:

=== "Python"

    ```bash
    ocd-validate virgil.yaml
    ```

=== "Node.js"

    ```bash
    npx @ocd-tools/validator virgil.yaml
    ```

You should see output like:

```
✅ Validation successful
📝 0 warnings
```

## Expanding to Full Format

For production use or when you need more detailed character information, you can expand to the full OCD format. Here's how Virgil would look in the complete format:

```yaml title="virgil-full.yaml"
ocd_version: "1.0.0"
id: "char-virgil-hawkins"
slug: "virgil-hawkins"
names:
  canon: "Virgil Hawkins"
identity:
  entity_kind: "person"
  sapience_level: "sapient"
  species: "human"
summary: "A man with a passion for science and technology who can control electricity and magnetism."
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Adding More Information

Let's enhance Rita with some additional details:

```yaml title="rita-enhanced.yaml"
ocd_version: "1.0.0"
id: "char-rita-adventurer"
names:
  canon: "Rita"
  aliases: ["Rita the Brave", "Adventurer Rita"]
locale: "en-US"
media_targets: ["game", "novel"]

identity:
  kind: "humanoid"
  species: "Human"
  age: "25 years"
  pronouns: ["she/her"]
  locale: "Fantasy Kingdom"

appearance:
  body_type: "athletic build"
  height: "5'6\""
  distinguishing_features: ["bright green eyes", "auburn hair"]
  physical_summary: "A determined young woman with an adventurous spirit."

personality:
  summary: "Brave, curious, and always ready for adventure."

meta:
  tags: ["adventurer", "hero", "fantasy"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Understanding Optional Fields

### Names Block
- **`aliases`**: Alternative names or titles
- **`locale`**: Language/region for localization

### Identity Block
- **`age`**: Character's age (can be specific or descriptive)
- **`pronouns`**: Preferred pronouns
- **`locale`**: Where the character is from

### Appearance Block
- **`body_type`**: Physical build description
- **`height`**: Character's height
- **`distinguishing_features`**: Notable physical characteristics
- **`physical_summary`**: Overall physical description

### Personality Block
- **`summary`**: Brief personality description

### Meta Block
- **`tags`**: Keywords for categorization and search

## Validation Results

Run the validator again on your enhanced character:

```bash
ocd-validate rita-enhanced.yaml
```

You should still see a successful validation. The validator will normalize some values (like converting tags to lowercase) but won't show warnings for valid optional fields.

## Common Mistakes

Here are some common issues you might encounter:

### Missing Required Fields

```yaml title="invalid-missing-fields.yaml"
# This will fail validation
names:
  canon: "Rita"
# Missing ocd_version, id, identity, and meta.versioning
```

**Error:** `Missing required field: ocd_version`

### Invalid Field Values

```yaml title="invalid-field-values.yaml"
ocd_version: "1.0.0"
id: "char-rita"
names:
  canon: "Rita"
identity:
  kind: "invalid-kind"  # Not a valid identity kind
meta:
  versioning:
    created_at: "not-a-date"  # Invalid ISO 8601 format
    last_modified: "2024-01-01T00:00:00Z"
```

**Error:** `Invalid identity kind: invalid-kind`

### Invalid Timestamp Format

```yaml title="invalid-timestamp.yaml"
meta:
  versioning:
    created_at: "January 1, 2024"  # Wrong format
    last_modified: "2024-01-01T00:00:00Z"
```

**Error:** `Invalid timestamp format. Use ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)`

## What's Next?

Congratulations! You've created your first OCD character. In the next step, you'll learn about the trait model and add personality traits to make Rita more interesting.

**Next:** [Step 2: Adding Personality](personality.md)

## Quick Reference

### Required Fields Checklist
- [ ] `ocd_version`
- [ ] `id` (with `char-` prefix)
- [ ] `names.canon`
- [ ] `identity.kind`
- [ ] `identity.species`
- [ ] `meta.versioning.created_at`
- [ ] `meta.versioning.last_modified`

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
Always use ISO 8601 format: `YYYY-MM-DDTHH:mm:ssZ`
Example: `2024-01-01T00:00:00Z`
