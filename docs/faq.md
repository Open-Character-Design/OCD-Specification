# FAQ

Frequently asked questions about OCS (Open Character Specification).

## General Questions

### What is OCS?

OCS (Open Character Specification) is a structured, portable format for defining characters across games, film/TV, books, and AI role-play. It provides a unified way to represent character data that works across different platforms and systems.

### Why should I use OCS?

OCS offers several benefits:

- **Portability**: Characters work across games, AI platforms, and media
- **Consistency**: Standardized structure ensures reliable character representation
- **Validation**: Built-in schema validation catches errors before deployment
- **Extensibility**: Support for custom game systems via extension blocks
- **Interoperability**: Easy to convert between different platforms

### Is OCS free to use?

Yes! OCS is open source:
- **Code**: Licensed under Apache 2.0
- **Specification**: Licensed under CC-BY-4.0
- **Free for commercial and personal use**

## Technical Questions

### Do I have to use OCD-T?

No! You can use any of these formats:
- **YAML**: Human-readable, great for authoring
- **JSON**: Machine-readable, perfect for APIs
- **OCD-T**: Concise textual format for quick authoring

All formats validate to the same schema.

### How do I add custom game system data?

Use extension blocks with the `x-` prefix:

```yaml
x-dnd5e:
  class: "Wizard"
  level: 8
  # ... D&D specific data

x-my-game:
  system: "MyFantasyRPG"
  character_type: "Mage"
  # ... custom system data
```

### Can I validate files programmatically?

Yes! Both Python and JavaScript validators provide APIs:

=== "Python"

    ```python
    from ocs.ocs_validate import validate_and_normalize
    
    result = validate_and_normalize(document)
    if result["ok"]:
        print("Valid:", result["data"])
    else:
        print("Errors:", result["errors"])
    ```

=== "JavaScript"

    ```javascript
    import { validateAndNormalize } from '@ocs-tools/validator';
    
    const result = validateAndNormalize(document);
    if (result.ok) {
        console.log('Valid:', result.data);
    } else {
        console.log('Errors:', result.errors);
    }
    ```

### What validation errors should I watch for?

Common validation issues:

- **Missing required fields**: `ocs_version`, `id`, `names.canon`, etc.
- **Invalid field values**: Wrong identity kinds, malformed timestamps
- **Unresolved references**: `target_ref` pointing to non-existent characters
- **Content rating conflicts**: Traits contradicting appropriateness ratings

### How do I handle character relationships?

Use the `relationships` array in the background block:

```yaml
background:
  relationships:
    - target_ref: "char-other-character"
      role: "friend"
      sentiment: 0.8
      notes: "Close ally from childhood"
```

The validator will check that referenced characters exist.

## Integration Questions

### How do I integrate OCS with my AI platform?

See the [Agents & Runtime guide](integration/agents.md) for patterns including:
- LangChain integration
- LlamaIndex compatibility
- Runtime orchestration
- Memory management

### Can I use OCS with existing game systems?

Yes! OCS supports popular systems:
- **D&D 5e**: Via `x-dnd5e` extension
- **Pathfinder**: Via `x-pf2e` extension
- **Custom systems**: Create your own `x-*` extensions

### How do I convert from other character formats?

Conversion depends on your source format:

1. **From JSON**: Direct mapping with field translation
2. **From XML**: Parse and restructure to OCS format
3. **From proprietary**: Create mapping rules for your specific format

### Is there a character database or registry?

Not yet, but we're planning:
- Community character sharing
- Extension registry
- Validation service API

## Authoring Questions

### What's the difference between YAML, JSON, and OCD-T?

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **YAML** | Human authoring | Readable, comments | Larger file size |
| **JSON** | APIs, automation | Compact, universal | Less readable |
| **OCD-T** | Quick authoring | Concise, markdown-friendly | Learning curve |

### How do I handle character updates?

Use semantic versioning in metadata:

```yaml
meta:
  versioning:
    version: "1.2.0"  # Major.Minor.Patch
    last_modified: "2024-01-01T00:00:00Z"
```

### What are the best practices for trait naming?

Use standardized trait names for consistency:

```yaml
# Good
- name: "introversion↔extraversion"
- name: "combat-readiness"

# Avoid
- name: "Introversion vs Extraversion"
- name: "Combat Readiness"
```

### How do I handle localization?

Use the `display` field for multiple languages:

```yaml
names:
  canon: "Alice"
  display:
    en-US: "Alice"
    es-ES: "Alicia"
    fr-FR: "Alice"
```

## Validation Questions

### What does normalization do?

The validator normalizes:
- **Trait names**: Standardizes separators (`↔`)
- **Tags**: Lowercases and deduplicates
- **Slugs**: Normalizes separators
- **Timestamps**: Ensures ISO 8601 format

### How do I treat warnings as errors?

Use the `--warnings-as-errors` flag:

```bash
ocs-validate character.yaml --warnings-as-errors
```

### Can I validate multiple files at once?

Yes! Use shell commands:

```bash
# Validate all YAML files
find . -name "*.yaml" -exec ocs-validate {} \;

# Validate with error on warnings
find . -name "*.yaml" -exec ocs-validate {} --warnings-as-errors \;
```

### What's the difference between errors and warnings?

- **Errors**: Prevent validation (missing required fields, invalid values)
- **Warnings**: Suggest improvements (normalization applied, potential issues)

## Extension Questions

### How do I create custom extensions?

1. Choose a namespace: `x-my-system`
2. Define your schema
3. Document the fields
4. Use consistently across characters

```yaml
x-my-system:
  # Document your fields
  system: "MyFantasyRPG"
  version: "2.1"
  character_type: "Mage"
```

### Can I validate extension data?

OCS validators don't validate extension blocks (they're system-specific). Each game system would need its own validator for extension data.

### How do I share extensions with the community?

1. Document your extension schema
2. Provide examples
3. Submit to the community registry (coming soon)
4. Follow naming conventions (`x-system-name`)

## Troubleshooting

### My character validates but doesn't work in my game

This usually means:
1. **Missing extension data**: Add system-specific fields
2. **Wrong field values**: Check your game system's requirements
3. **Incomplete character**: Add missing personality/background details

### I'm getting "UNRESOLVED_REF" warnings

This means a `target_ref` points to a character that doesn't exist:

```yaml
# This will warn if char-friend doesn't exist
relationships:
  - target_ref: "char-friend"
    role: "ally"
```

**Solutions:**
1. Create the referenced character
2. Remove the reference
3. Use a placeholder ID

### My timestamps are invalid

Use ISO 8601 format:

```yaml
# Correct
created_at: "2024-01-01T00:00:00Z"

# Incorrect
created_at: "January 1, 2024"
created_at: "2024-01-01"
```

### The validator is too strict

OCS validation is designed to catch common issues. If you need to bypass validation:

1. **For development**: Use `--format` to force parsing
2. **For production**: Fix the validation issues
3. **For custom fields**: Use extension blocks

## Getting Help

### Where can I get help?

1. **Documentation**: Check the [Specification](spec/schema-overview.md)
2. **Examples**: Browse the [Examples Gallery](authoring/examples.md)
3. **Community**: Ask on [GitHub Discussions](https://github.com/eVirgil/OpenCharacter-Specification/discussions)
4. **Issues**: Report bugs on [GitHub Issues](https://github.com/eVirgil/OpenCharacter-Specification/issues)

### How do I contribute to OCS?

See the [Contributing guide](governance/contributing-to-spec.md) for:
- Code contributions
- Specification improvements
- Documentation updates
- Community support

### Can I suggest new features?

Yes! We welcome feature requests:
1. **Check existing issues** first
2. **Create a new issue** with detailed description
3. **Provide examples** of how it would work
4. **Consider contributing** the implementation

## Still Have Questions?

If you don't see your question here:

1. **Search the documentation** for related topics
2. **Check GitHub Issues** for similar questions
3. **Ask on Discussions** for community help
4. **Create an Issue** for bugs or feature requests

We're here to help make OCS work for your use case!
