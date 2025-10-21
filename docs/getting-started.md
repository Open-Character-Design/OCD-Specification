# Getting Started

Welcome to OCD! This guide will get you up and running with character validation in minutes.

## Who Uses OCD?

OCD is used by creators, developers, and organizations across industries:

<div class="features-grid">

<div class="feature-card">

🎨 **Creative Professionals**

Artists, writers, and designers who need consistent character development across multiple projects and mediums.

</div>

<div class="feature-card">

⚙️ **Technical Teams**

Developers, engineers, and data scientists building character-driven applications, AI systems, and procedural content.

</div>

<div class="feature-card">

🎮 **Game Studios**

Teams creating games, visual novels, and interactive experiences that require rich, consistent character systems.

</div>

<div class="feature-card">

🤖 **AI Platforms**

Companies building AI-powered character interactions, NPCs, and creative tools that need structured character data.

</div>

<div class="feature-card">

📚 **Educational Institutions**

Teachers and students learning character design, narrative development, and creative technology workflows.

</div>

<div class="feature-card">

🌐 **Open Source Communities**

Collaborative projects building shared character libraries and interoperable creative tools.

</div>

</div>

## Installation

Choose your preferred validator:

=== "Python"

    ```bash
    pip install ocd
    ```

    **System Requirements:**
    - Python 3.8 or higher
    - pip package manager

=== "Node.js"

    ```bash
    npm install @ocd-tools/validator
    ```

    **System Requirements:**
    - Node.js 16 or higher
    - npm package manager

=== "Global Installation"

    ```bash
    # Python
    pip install --global ocd

    # Node.js
    npm install --global @ocd-tools/validator
    ```

## Choose Your Path

OCD serves different needs for different types of users. Choose the path that best fits your goals:

<div class="features-grid">

<div class="feature-card">

### 🎨 **For Creative Professionals**

**Start with:** [Creative Applications](use-cases/creative.md)

- Learn how OCD transforms character design workflows
- Understand worldbuilding and collaborative character development
- Explore cross-media character portability

**Next Steps:**
1. Create your first character with [Tutorial: Your First Character](tutorial/first-character.md)
2. Learn advanced techniques in [Tutorial: Adding Personality](tutorial/personality.md)
3. Explore [Examples Gallery](authoring/examples.md) for inspiration

</div>

<div class="feature-card">

### ⚙️ **For Technical Teams**

**Start with:** [Technical Applications](use-cases/technical.md)

- Learn about metadata management and API integration
- Understand procedural generation and AI training datasets
- Explore version control and database integration

**Next Steps:**
1. Set up validation with [Python Validator](integration/python-validator.md) or [JavaScript/TypeScript Validator](integration/js-ts-validator.md)
2. Learn about [Extensions and Namespaces](integration/extensions-and-namespaces.md)
3. Explore [Technical Examples](authoring/examples.md) for implementation patterns

</div>

<div class="feature-card">

### 🎮 **For Game Developers**

**Start with:** [Interactive & Storytelling](use-cases/interactive.md)

- Learn about game engine integration (Unity, Unreal, Godot)
- Understand AI-driven NPC personalities and behavior systems
- Explore visual novel and RPG character systems

**Next Steps:**
1. Learn [Game Engine Integration](use-cases/interactive.md#game-engine-integration) patterns
2. Set up [Python Validator](integration/python-validator.md) for character import
3. Explore [Interactive Examples](authoring/examples.md) for game characters

</div>

<div class="feature-card">

### 🌐 **For Community Builders**

**Start with:** [Community & Open Source](use-cases/community.md)

- Learn about shared character libraries and collaboration
- Understand cross-media adaptation and open standardization
- Explore educational applications and community governance

**Next Steps:**
1. Learn about [Community Contribution](governance/contributing-to-spec.md)
2. Explore [Community Examples](authoring/examples.md) for shared characters
3. Join discussions on [GitHub](https://github.com/Open-Character-Design/OCD-Specification/discussions)

</div>

</div>

## Quick Validation

Let's validate your first character! Download this sample file:

```yaml title="sample-character.yaml"
ocd_version: "0.0.1"
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
    ocd-validate sample-character.yaml
    ```

=== "Node.js"

    ```bash
    npx @ocd-tools/validator sample-character.yaml
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
  - Missing required field: ocd_version
  - Invalid identity kind: 'invalid-kind'
```

## Your First Character

Let's create a complete character step by step:

### Step 1: Basic Information

```yaml title="my-hero.yaml"
ocd_version: "0.0.1"
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
ocd_version: "0.0.1"
id: "char-my-hero"
names:
  canon: "My Hero"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  summary: "Brave and determined adventurer"
  traits:
    - name: "introversion-extraversion"
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
ocd-validate my-hero-with-personality.yaml
```

!!! note "Understanding Traits"
    - **Bipolar traits**: Range from -1 to 1, with intensity 0 to 1
    - **Scalar traits**: Single value from 0 to 1
    - **Flag traits**: Boolean true/false

## Common Issues and Solutions

### Missing Required Fields

**Error:** `Missing required field: ocd_version`

**Solution:** Add the missing field:
```yaml
ocd_version: "0.0.1"
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
ocd-validate my-hero.yaml --print
```

This shows the normalized JSON output with:
- Trait names standardized
- Tags lowercased and deduplicated
- Slugs normalized

### Treat Warnings as Errors

For strict validation:

```bash
ocd-validate my-hero.yaml --warnings-as-errors
```

This will fail if any warnings are present.

### Force Input Format

Specify the input format explicitly:

```bash
ocd-validate my-hero.yaml --format yaml
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

Deep dive into the technical details of OCD structure.

</div>

<div class="feature-card">

### 🛠️ [Integration Guide](integration/python-validator.md)

Learn how to integrate OCD into your applications.

</div>

</div>

## Getting Help

If you run into issues:

1. **Check the [FAQ](faq.md)** for common questions
2. **Browse [Examples](authoring/examples.md)** for inspiration
3. **Read the [Specification](spec/schema-overview.md)** for detailed information
4. **Ask on [GitHub Discussions](https://github.com/Open-Character-Design/OCD-Specification/discussions)**

## Quick Reference

### Required Fields
- `ocd_version`: OCD specification version
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
ocd-validate character.yaml

# With normalized output
ocd-validate character.yaml --print

# Strict validation (warnings as errors)
ocd-validate character.yaml --warnings-as-errors
```
