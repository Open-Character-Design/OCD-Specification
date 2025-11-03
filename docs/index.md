
# Open Character Design Specification

**A structured, portable format for defining characters across games, film/TV, books, and AI role-play.**

Transform your character development workflow with a unified specification that works everywhere.


## Quick Start

Choose a path that fits how you work:

<div class="features-grid">

<div class="feature-card">
<h3>🎨 Creative Design</h3>
<p>Structure your characters without changing your creative process.</p>
<p><em>Writers, artists, narrative designers</em></p>
<p><a href="use-cases/creative/">Explore Creative →</a></p>
</div>

<div class="feature-card">
<h3>🎮 Interactive & Game Dev</h3>
<p>Build consistent NPCs and agents across engines and tools.</p>
<p><em>Game developers, AI engineers</em></p>
<p><a href="use-cases/interactive/">Explore Interactive →</a></p>
</div>

<div class="feature-card">
<h3>🎬 Virtual & Real-Time Production</h3>
<p>Keep character identity aligned across scenes and pipelines.</p>
<p><em>Virtual production, real-time teams</em></p>
<p><a href="use-cases/virtual-production/">Explore Production →</a></p>
</div>

<div class="feature-card">
<h3>🌐 Collaboration & Open Ecosystem</h3>
<p>Share, remix, and evolve characters across teams and platforms.</p>
<p><em>Open-source, cross-media teams</em></p>
<p><a href="use-cases/community/">Explore Collaboration →</a></p>
</div>

</div>

### Try it in 60 seconds (no install)
Create a minimal character file and open it in your editor. You can validate later.

```yaml title="my-character.yaml"
ocd_version: "1.0.0"
id: "my-first-character"
names: { canon: "Rita" }
identity: { kind: "humanoid", species: "Human" }
personality: { summary: "Bold and fun socialite" }
meta:
  tags: [mentor, human, brave]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

[Create Your First Character](getting-started.md){ .md-button .md-button--primary }

Not sure where to start? [Choose Your Path](start-here/paths.md){ .md-button }

!!! note "Prefer to validate now?"
    Use the CLI validators under [Integration](integration/examples.md), or try the [In-Browser Playground (Preview)](validation/playground.md).


## Why OCD?

<p id="why-ocd-quip">Why OCD? Good question</p>

The Open Character Design bridges creativity and technology. It provides a structured, interoperable framework for defining, sharing, and evolving digital characters.
It helps creators maintain consistency, enhance collaboration, and connect characters across art, data, and interactive systems.

<!-- Consolidated: Use case cards already shown above in Quick Start -->
<p><a href="use-cases/">View all use cases →</a></p>

<!-- Removed duplicate "Your First Character" example (already provided above) -->

<!-- Streamlined: Next steps are already clear via primary/secondary buttons above -->

## Community

- **GitHub**: [OpenCharacter-Specification](https://github.com/Open-Character-Design/OCD-Specification)
- **Issues**: [Report bugs or request features](https://github.com/Open-Character-Design/OCD-Specification/issues)
- **Discussions**: [Ask questions and share examples](https://github.com/Open-Character-Design/OCD-Specification/discussions)
- **Contributing**: [Help improve the specification](governance/contributing-to-spec.md)

!!! note "Open Source"
    OCD is open source under Apache 2.0 (code) and CC-BY-4.0 (specification). Contributions welcome!
