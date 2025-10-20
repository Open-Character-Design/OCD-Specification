# Step 1: Your First Character

In this step, you'll create your first OCS character and learn the fundamentals of validation.

## What You'll Build

A minimal but complete character definition that demonstrates the core OCS structure.

## Installation

First, let's install a validator so you can check your work:

=== "Python"

    ```bash
    pip install ocs==1.0.0
    ```

=== "Node.js"

    ```bash
    npm install @ocs-tools/validator@1.0.0
    ```

## Creating Your First Character

Create a new file called `alice.yaml` with this content:

```yaml title="alice.yaml"
ocs_version: "0.0.1"
id: "char-alice-adventurer"
names:
  canon: "Alice"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Understanding the Structure

Let's break down each field:

### Required Fields

- **`ocs_version`**: The version of the OCS specification this character uses
- **`id`**: A unique identifier for this character (use `char-` prefix)
- **`names.canon`**: The character's canonical name
- **`identity.kind`**: The type of entity (`humanoid`, `animal`, `construct`, etc.)
- **`identity.species`**: The specific species or type
- **`meta.versioning`**: Timestamps for tracking changes

!!! tip "ID Convention"
    Use descriptive IDs like `char-alice-adventurer` or `char-bruenor-battlehammer`. This helps identify characters in logs and references.

## Validating Your Character

Now let's validate your character:

=== "Python"

    ```bash
    ocs-validate alice.yaml
    ```

=== "Node.js"

    ```bash
    npx @ocs-tools/validator alice.yaml
    ```

You should see output like:

```
✅ Validation successful
📝 0 warnings
```

## Adding More Information

Let's enhance Alice with some additional details:

```yaml title="alice-enhanced.yaml"
ocs_version: "0.0.1"
id: "char-alice-adventurer"
names:
  canon: "Alice"
  aliases: ["Alice the Brave", "Adventurer Alice"]
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
ocs-validate alice-enhanced.yaml
```

You should still see a successful validation. The validator will normalize some values (like converting tags to lowercase) but won't show warnings for valid optional fields.

## Common Mistakes

Here are some common issues you might encounter:

### Missing Required Fields

```yaml title="invalid-missing-fields.yaml"
# This will fail validation
names:
  canon: "Alice"
# Missing ocs_version, id, identity, and meta.versioning
```

**Error:** `Missing required field: ocs_version`

### Invalid Field Values

```yaml title="invalid-field-values.yaml"
ocs_version: "0.0.1"
id: "char-alice"
names:
  canon: "Alice"
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

Congratulations! You've created your first OCS character. In the next step, you'll learn about the trait model and add personality traits to make Alice more interesting.

**Next:** [Step 2: Adding Personality](personality.md)

## Quick Reference

### Required Fields Checklist
- [ ] `ocs_version`
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
