
# Open Character Design Specification

**A structured, portable format for defining characters across games, film/TV, books, and AI role-play.**

Transform your character development workflow with a unified specification that works everywhere.


## Quick Start

Get up and running in minutes with our validators:

=== "Python"

    ```bash
    pip install ocd-validate
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

Transform your creative and technical workflows with OCD's unified character design framework.

From storytelling to simulation, OCD connects creativity, data, and collaboration across five core domains:

<div class="features-grid">

<div class="feature-card">

<h3>🎨 <a href="use-cases/creative/">Creative Design</a></h3>

<p>Bring structure and depth to your creative process. OCD enables consistent character development from concept to implementation, supporting visual artists, writers, and transmedia creators in building cohesive worlds.</p>

<p><em>For: Writers, artists, content creators</em></p>

</div>

<div class="feature-card">

<h3>⚙️ <a href="use-cases/technical/">Technical Integration & Data Systems</a></h3>

<p>Bridge creativity and computation. OCD provides a structured metadata layer for character systems—ideal for AI datasets, API integration, procedural pipelines, and version control in complex productions.</p>

<p><em>For: Developers, data engineers, AI researchers</em></p>

</div>

<div class="feature-card">

<h3>🎮 <a href="use-cases/interactive/">Interactive & Game Development</a></h3>

<p>Design and deploy interactive characters for games, simulations, and virtual worlds. OCD ensures your NPCs, avatars, and agents maintain personality consistency across gameplay and updates.</p>

<p><em>For: Game developers, AI engineers</em></p>

</div>

<div class="feature-card">

<h3>🎬 <a href="use-cases/virtual-production/">Virtual & Real-Time Production</a></h3>

<p>Integrate OCD characters into film, TV, and live digital production. Manage character consistency across real-time rendering pipelines and virtual performance systems.</p>

<p><em>For: Film studios, virtual production teams</em></p>

</div>

<div class="feature-card">

<h3>🌐 <a href="use-cases/community/">Collaboration & Open Ecosystem</a></h3>

<p>Join a shared creative standard. OCD's open specification enables creators to exchange, remix, and evolve characters across projects, teams, and platforms.</p>

<p><em>For: Open-source collaborators, cross-media teams</em></p>

</div>

</div>

## Your First Character

Here's a minimal OCD character to get you started:

```yaml title="my-character.yaml"
ocd_version: "0.0.1"
id: "my-first-character"
names:
  canon: "Rita"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  summary: "Bold and fun socialite"
meta:
  tags: [mentor, human, brave]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

!!! tip "Try It Now"
    Save this as `my-character.yaml` and run `ocd-validate my-character.yaml` to see it in action!

## What's Next?

<div class="features-grid">

<div class="feature-card">

<h3>🚀 <a href="getting-started">Get Started</a></h3>

<p>Install validators, create your first character, and understand the basics.</p>

<p><em>For: New users, quick setup</em></p>

</div>

<div class="feature-card">

<h3>📖 <a href="authoring/examples/">Browse Examples</a></h3>

<p>Explore character examples from D&D warriors to sci-fi heroes. See OCD in action.</p>

<p><em>For: Learning by example, inspiration</em></p>

</div>

<div class="feature-card">

<h3>📝 <a href="spec/schema-overview/">Read the Spec</a></h3>

<p>Deep dive into the specification. Understand blocks, traits, and validation rules.</p>

<p><em>For: Technical implementation, detailed understanding</em></p>

</div>

<div class="feature-card">

<h3>🔌 <a href="integration/python-validator/">Integration Guide</a></h3>

<p>Integrate OCD into your applications with our Python and JavaScript validators.</p>

<p><em>For: Developers, system integration</em></p>

</div>

</div>

## Community

- **GitHub**: [OpenCharacter-Specification](https://github.com/Open-Character-Design/OCD-Specification)
- **Issues**: [Report bugs or request features](https://github.com/Open-Character-Design/OCD-Specification/issues)
- **Discussions**: [Ask questions and share examples](https://github.com/Open-Character-Design/OCD-Specification/discussions)
- **Contributing**: [Help improve the specification](governance/contributing-to-spec.md)

!!! note "Open Source"
    OCD is open source under Apache 2.0 (code) and CC-BY-4.0 (specification). Contributions welcome!
