
# Open Character Design Specification

**A structured, portable format for defining characters across games, film/TV, books, and AI role-play.**

Transform your character development workflow with a unified specification that works everywhere.


## Quick Start

Get up and running in minutes with our validators (WIP - Not actually ready yet):

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

[Get Started Now](getting-started.md){ .md-button .md-button--primary }


## Why OCD?

<p id="why-ocd-quip">Why OCD? Good question</p>

The Open Character Design bridges creativity and technology — providing a structured, interoperable framework for defining, sharing, and evolving digital characters.
It helps creators maintain consistency, enhance collaboration, and connect characters across art, data, and interactive systems.

## Use Cases

Transform your creative and technical workflows with OCD’s unified character design framework.

From storytelling to simulation, OCD connects creativity, data, and collaboration across five core domains:

### 🎨 [Creative Design](use-cases/creative.md)

**Character Design Framework & Worldbuilding**

Bring structure and depth to your creative process. OCD enables consistent character development from concept to implementation, supporting visual artists, writers, and transmedia creators in building cohesive worlds.

*For: Writers, artists, content creators*

### ⚙️ [Technical Integration & Data Systems](use-cases/technical.md)

Bridge creativity and computation. OCD provides a structured metadata layer for character systems—ideal for AI datasets, API integration, procedural pipelines, and version control in complex productions.

*For: Developers, data engineers, AI researchers*


### 🎮 [Interactive & Game Development](use-cases/interactive.md)

**Games & Interactive Experiences**

Design and deploy interactive characters for games, simulations, and virtual worlds. OCD ensures your NPCs, avatars, and agents maintain personality consistency across gameplay and updates.

*For: Game developers, AI engineers*

### 🎬 [Virtual & Real-Time Production](use-cases/virtual-production.md)

**Real-time Character Rendering**

Integrate OCD characters into film, TV, and live digital production. Manage character consistency across real-time rendering pipelines and virtual performance systems.

*For: Film studios, virtual production teams*

### 🌐 [Collaboration & Open Ecosystem](use-cases/community.md)

**Collaboration & Cross-Media Adaptation**

Join a shared creative standard. OCD’s open specification enables creators to exchange, remix, and evolve characters across projects, teams, and platforms.

*For: Open-source collaborators, cross-media teams*

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
  tags: [adventurer, human, brave]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

!!! tip "Try It Now"
    Save this as `my-character.yaml` and run `ocd-validate my-character.yaml` to see it in action!

## What's Next?

### 🚀 [Get Started](getting-started.md)

Install validators, create your first character, and understand the basics.

*For: New users, quick setup*

### 📖 [Browse Examples](authoring/examples.md)

Explore character examples from D&D warriors to sci-fi heroes. See OCD in action.

*For: Learning by example, inspiration*

### 📝 [Read the Spec](spec/schema-overview.md)

Deep dive into the specification. Understand blocks, traits, and validation rules.

*For: Technical implementation, detailed understanding*

### 🔌 [Integration Guide](integration/python-validator.md)

Integrate OCD into your applications with our Python and JavaScript validators.

*For: Developers, system integration*

## Community

- **GitHub**: [OpenCharacter-Specification](https://github.com/Open-Character-Design/OCD-Specification)
- **Issues**: [Report bugs or request features](https://github.com/Open-Character-Design/OCD-Specification/issues)
- **Discussions**: [Ask questions and share examples](https://github.com/Open-Character-Design/OCD-Specification/discussions)
- **Contributing**: [Help improve the specification](governance/contributing-to-spec.md)

!!! note "Open Source"
    OCD is open source under Apache 2.0 (code) and CC-BY-4.0 (specification). Contributions welcome!
