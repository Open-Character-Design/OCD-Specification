---
title: Authoring Playbook
description: Best practices for structuring OCD files across YAML, JSON, and OCD-T formats.
search:
  boost: 2
tags:
  - authoring
  - best-practices
  - workflow
---

# Writing OCD Files

This guide covers best practices for authoring OCD files in YAML, JSON, and OCD-T formats.

## Format Selection

Choose the format that best fits your workflow:

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **YAML** | Human authoring | Readable, comments, flexible | Larger file size |
| **JSON** | APIs, automation | Compact, universal, strict | Less readable |
| **OCD-T** | Quick authoring | Concise, markdown-friendly | Learning curve |

## YAML Authoring Guidelines

### Basic Structure

```yaml title="character.yaml"
ocd_version: "0.0.1"
id: "char-example"
names:
  canon: "Example Character"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Best Practices

- **Quote strings**: Use quotes for sentences and descriptive text
- **Bare words**: Use unquoted values for enums, tags, and identifiers
- **Ordered arrays**: Keep arrays in logical order (most important first)
- **Consistent indentation**: Use 2 spaces for indentation
- **Comments**: Add comments to explain complex sections

```yaml title="best-practices.yaml"
# Character metadata
ocd_version: "0.0.1"
id: "char-alice-adventurer"  # Use descriptive IDs

names:
  canon: "Alice"  # Primary name
  aliases: ["Al", "Adventurer Alice"]  # Alternative names

personality:
  summary: "Brave and curious adventurer"  # Quote descriptive text
  traits:
    - name: "introversion-extraversion"  # Use standard trait names
      kind: "bipolar"
      polarity: 0.7  # Bare numbers
      intensity: 0.8
```

### Common Mistakes

```yaml title="avoid-this.yaml"
# ❌ Don't do this
ocd_version: 0.0.1  # Missing quotes
id: "Alice"  # Not descriptive enough
names:
  canon: Alice  # Missing quotes
personality:
  summary: Brave adventurer  # Missing quotes
  traits:
    - name: "Introversion vs Extraversion"  # Non-standard naming
      polarity: 1.5  # Out of range
```

## JSON Authoring Guidelines

### Basic Structure

```json title="character.json"
{
  "ocd_version": "0.0.1",
  "id": "char-example",
  "names": {
    "canon": "Example Character"
  },
  "identity": {
    "kind": "humanoid",
    "species": "Human"
  },
  "meta": {
    "versioning": {
      "created_at": "2024-01-01T00:00:00Z",
      "last_modified": "2024-01-01T00:00:00Z"
    }
  }
}
```

### Best Practices

- **Consistent formatting**: Use 2-space indentation
- **String quotes**: Always use double quotes
- **No comments**: JSON doesn't support comments
- **Validation**: Always validate JSON syntax

## OCD-T Authoring Guidelines

OCD-T is a concise textual format for quick character authoring:

```ocd title="character.ocd"
ocd-t: 1
ocd-version: 0.0.1

character "Alice" {
  id: "char-alice-adventurer"
  
  personality {
    summary: "Brave and curious adventurer"
    traits: [
      { name: "introversion-extraversion", kind: bipolar, polarity: 0.7, intensity: 0.8 }
    ]
  }
}
```

### OCD-T Features

- **Concise syntax**: Less verbose than YAML/JSON
- **Markdown-friendly**: Easy to embed in documentation
- **Multiline strings**: Support for long descriptions
- **Extension blocks**: Easy to add system-specific data

## Validation Workflow

### Early Validation

Validate your files early and often:

```bash
# Validate single file
ocd-validate character.yaml

# Validate with warnings as errors
ocd-validate character.yaml --warnings-as-errors

# Print normalized output
ocd-validate character.yaml --print
```

### Common Validation Issues

1. **Missing required fields**
   ```bash
   ❌ Missing required field: ocd_version
   ```
   **Fix**: Add `ocd_version: "0.0.1"`

2. **Invalid field values**
   ```bash
   ❌ Invalid identity kind: 'invalid-kind'
   ```
   **Fix**: Use valid identity kinds like `"humanoid"`, `"animal"`, etc.

3. **Timestamp format issues**
   ```bash
   ❌ Invalid timestamp format
   ```
   **Fix**: Use ISO 8601 format: `"2024-01-01T00:00:00Z"`

4. **Unresolved references**
   ```bash
   ⚠️ UNRESOLVED_REF: Reference 'char-friend' not found
   ```
   **Fix**: Create the referenced character or remove the reference

## File Organization

### Directory Structure

```
characters/
├── protagonists/
│   ├── alice.yaml
│   └── bob.yaml
├── antagonists/
│   └── villain.yaml
└── npcs/
    ├── merchant.yaml
    └── guard.yaml
```

### Naming Conventions

- **Files**: Use descriptive names: `alice-adventurer.yaml`
- **IDs**: Use consistent prefixes: `char-alice-adventurer`
- **Tags**: Use lowercase with hyphens: `["fantasy", "adventurer", "hero"]`

## Advanced Techniques

### Conditional Fields

Use extension blocks for system-specific data:

```yaml title="dnd-character.yaml"
# Core OCD data
ocd_version: "0.0.1"
id: "char-bruenor"
names:
  canon: "Bruenor Battlehammer"

# D&D 5e specific data
x-dnd5e:
  class: "Fighter"
  level: 8
  abilities:
    strength: 18
    dexterity: 12
    constitution: 16
    intelligence: 10
    wisdom: 13
    charisma: 14
```

### Template Usage

Create reusable templates:

```yaml title="template-minimal.yaml"
ocd_version: "0.0.1"
id: "char-template"
names:
  canon: "Template Character"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Tools and Editors

### Recommended Editors

- **VS Code**: With YAML extension for syntax highlighting
- **Vim/Neovim**: With YAML syntax support
- **Emacs**: With YAML mode
- **Online**: JSON/YAML validators for quick checks

### Useful Extensions

- **YAML**: Syntax highlighting and validation
- **JSON**: Formatting and validation
- **OCD**: Custom syntax highlighting (if available)

## Next Steps

- **[Examples Gallery](examples.md)**: See real character examples.
- **[OCD Specification Format](../spec/ocd-specification-format.md)**: Review the canonical document structure.
- **[Validation Diagnostics](../reference/diagnostics.md)**: Understand error messages.
- **[Python Validator Integration](../integration/python-validator.md)**: Use OCD in applications.
