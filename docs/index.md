<div class="hero-section">

# Open Character Specification

**A structured, portable format for defining characters across games, film/TV, books, and AI role-play.**

Transform your character development workflow with a unified specification that works everywhere.

</div>

## Quick Start

Get up and running in minutes with our validators:

=== "Python"

    ```bash
    pip install ocs==1.0.0
    ocs-validate examples/bruenor.yaml --print
    ```

=== "Node.js"

    ```bash
    npm install @ocs-tools/validator@1.0.0
    npx @ocs-tools/validator examples/bruenor.yaml --print
    ```

## Why OCS?

<div class="features-grid">

<div class="feature-card">

<span class="emoji">🎭</span>

### Multi-Genre Support

Works across fantasy, sci-fi, modern, and any genre. Define characters for games, AI platforms, and media with consistent structure.

</div>

<div class="feature-card">

<span class="emoji">🔧</span>

### System Integration

Built-in support for D&D 5e, custom game systems, and AI platforms. Extensible with `x-*` namespaces for any framework.

</div>

<div class="feature-card">

<span class="emoji">📝</span>

### Author-Friendly Formats

Choose from YAML, JSON, or OCD-T (our concise textual format). All formats validate to the same schema.

</div>

<div class="feature-card">

<span class="emoji">✅</span>

### Built-in Validation

Python and JavaScript validators with normalization, linting, and comprehensive diagnostics. Catch issues before deployment.

</div>

<div class="feature-card">

<span class="emoji">🔄</span>

### Portable & Interoperable

Characters work across platforms. Export from your game, import to AI, share with collaborators—all with the same format.

</div>

<div class="feature-card">

<span class="emoji">🎯</span>

### Production Ready

Used in production by game studios, AI platforms, and content creators. Battle-tested with comprehensive tooling.

</div>

</div>

## Your First Character

Here's a minimal OCS character to get you started:

```yaml title="my-character.yaml"
ocs_version: "0.0.1"
id: "my-first-character"
names:
  canon: "Alice"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  summary: "Brave and curious adventurer"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

!!! tip "Try It Now"
    Save this as `my-character.yaml` and run `ocs-validate my-character.yaml` to see it in action!

## What's Next?

<div class="features-grid">

<div class="feature-card">

### 🚀 [Get Started](getting-started.md)

Install validators, create your first character, and understand the basics.

</div>

<div class="feature-card">

### 📚 [Browse Examples](authoring/examples.md)

Explore character examples from D&D warriors to sci-fi heroes. See OCS in action.

</div>

<div class="feature-card">

### 📖 [Read the Spec](spec/schema-overview.md)

Deep dive into the specification. Understand blocks, traits, and validation rules.

</div>

<div class="feature-card">

### 🛠️ [Integration Guide](integration/python-validator.md)

Integrate OCS into your applications with our Python and JavaScript validators.

</div>

</div>

## Community

- **GitHub**: [OpenCharacter-Specification](https://github.com/eVirgil/OpenCharacter-Specification)
- **Issues**: Report bugs or request features
- **Discussions**: Ask questions and share examples
- **Contributing**: Help improve the specification

!!! note "Open Source"
    OCS is open source under Apache 2.0 (code) and CC-BY-4.0 (specification). Contributions welcome!