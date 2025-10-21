
<div class="hero-section">
<h1>Open Character Specification</h1>
<p><strong>A structured, portable format for defining characters across games, film/TV, books, and AI role-play.</strong></p>
<p>Transform your character development workflow with a unified specification that works everywhere.</p>
<a href="getting-started.md" class="md-button md-button--primary">Get Started Now</a>
</div>

## Open Character Specification

## Quick Start

Get up and running in minutes with our validators:

=== "Python"

    ```bash
    pip install ocd
    ocd-validate examples/bruenor.yaml --print
    ```

=== "Node.js"

    ```bash
    npm install @ocd-tools/validator
    npx @ocd-tools/validator examples/bruenor.yaml --print
    ```

## Why OCD?

<div class="features-grid">

<div class="feature-card">

🌐 **Multi-Genre Support**

Works across fantasy, sci-fi, modern, and any genre. Define characters for games, AI platforms, and media with consistent structure.

*Perfect for: Game developers, writers, AI developers*

</div>

<div class="feature-card">

⚙️ **System Integration**

Built-in support for D&D 5e, custom game systems, and AI platforms. Extensible with `x-*` namespaces for any framework.

*Perfect for: Technical teams, system integrators*

</div>

<div class="feature-card">

✏️ **Author-Friendly Formats**

Choose from YAML, JSON, or OCD-T (our concise textual format). All formats validate to the same schema.

*Perfect for: Writers, artists, content creators*

</div>

<div class="feature-card">

✅ **Built-in Validation**

Python and JavaScript validators with normalization, linting, and comprehensive diagnostics. Catch issues before deployment.

*Perfect for: Developers, quality assurance teams*

</div>

<div class="feature-card">

🔗 **Portable & Interoperable**

Characters work across platforms. Export from your game, import to AI, share with collaborators, all with the same format.

*Perfect for: Cross-platform teams, collaborative projects*

</div>

<div class="feature-card">

🏭 **Production Ready**

Used in production by game studios, AI platforms, and content creators. Battle-tested with comprehensive tooling.

*Perfect for: Professional studios, enterprise teams*

</div>

</div>

## Use Cases

Transform your creative workflow with OCD's structured approach to character design across different applications and industries.

<div class="features-grid">

<div class="feature-card">

### 🎭 [Creative Applications](use-cases/creative.md)

**Character Design Framework & Worldbuilding**

Transform your creative process with structured character development that works across any medium. From concept art to final production, maintain consistency and enable true creative collaboration.

[Explore Creative Use Cases →](use-cases/creative.md)

</div>

<div class="feature-card">

### ⚙️ [Technical Applications](use-cases/technical.md)

**Metadata Management & AI Integration**

Build robust character systems with OCD's technical capabilities. Perfect for procedural generation, AI training datasets, API integration, and version control workflows.

[Explore Technical Use Cases →](use-cases/technical.md)

</div>

<div class="feature-card">

### 🎮 [Interactive & Storytelling](use-cases/interactive.md)

**Game Engines & AI-Driven Experiences**

Create immersive interactive experiences with OCD-powered characters. From game engines to AI NPCs, bring your characters to life in digital worlds.

[Explore Interactive Use Cases →](use-cases/interactive.md)

</div>

<div class="feature-card">

### 🌐 [Community & Open Source](use-cases/community.md)

**Collaboration & Cross-Media Adaptation**

Join the open creative ecosystem. Share characters, collaborate across teams, and adapt content seamlessly across different media and platforms.

[Explore Community Use Cases →](use-cases/community.md)

</div>

</div>

## Your First Character

Here's a minimal OCD character to get you started:

```yaml title="my-character.yaml"
ocd_version: "0.0.1"
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
    Save this as `my-character.yaml` and run `ocd-validate my-character.yaml` to see it in action!

## What's Next?

<div class="features-grid">

<div class="feature-card">

🚀 [Get Started](getting-started.md)

Install validators, create your first character, and understand the basics.

</div>

<div class="feature-card">

📖 [Browse Examples](authoring/examples.md)

Explore character examples from D&D warriors to sci-fi heroes. See OCD in action.

</div>

<div class="feature-card">

📝 [Read the Spec](spec/schema-overview.md)

Deep dive into the specification. Understand blocks, traits, and validation rules.

</div>

<div class="feature-card">

🔌 [Integration Guide](integration/python-validator.md)

Integrate OCD into your applications with our Python and JavaScript validators.

</div>

</div>

## Community

- **GitHub**: [OpenCharacter-Specification](https://github.com/Open-Character-Design/OCD-Specification)
- **Issues**: [Report bugs or request features](https://github.com/Open-Character-Design/OCD-Specification/issues)
- **Discussions**: [Ask questions and share examples](https://github.com/Open-Character-Design/OCD-Specification/discussions)
- **Contributing**: [Help improve the specification](governance/contributing-to-spec.md)

!!! note "Open Source"
    OCD is open source under Apache 2.0 (code) and CC-BY-4.0 (specification). Contributions welcome!
