# Getting Started

Welcome to OCD (Open Character Design), your open framework for structured, consistent, and interoperable character design.
In just a few minutes, you’ll be validating your first character and connecting creativity with data.

## Who Uses OCD?

Who Uses OCD?

OCD is built for everyone who designs, develops, or deploys characters across creative and technical pipelines.

- 🎨 Creative Professionals — Artists, writers, and designers who want consistent, well-documented characters that scale across projects.
- ⚙️ Technical Teams — Developers and engineers building AI systems, APIs, and tools that rely on structured character data.
- 🎮 Game Studios — Teams creating NPCs, dialogue systems, and interactive worlds powered by personality-driven design.
- 🤖 AI Platforms — Companies training AI personas, chat agents, and virtual beings that need reliable personality data.
- 📚 Educators & Students — Those teaching or learning worldbuilding, narrative structure, or creative coding.
- 🌐 Open Source Creators — Collaborators building shared character libraries, tools, and cross-media projects.

## Installation

Choose your preferred validator. OCD (will be) available for both **Python** and **Node.js**.

### 🐍 Python

```bash
pip install ocd-
```

**Requirements:** Python 3.8+ and `pip`

### 🟦 Node.js

```bash
npm install -g ocd-
```

## Choose Your Path

OCD adapts to your workflow — whether you’re sketching, scripting, or simulating.

### 🎨 For Creative Professionals

Start with [Creative Applications](use-cases/creative.md)
Learn how OCD supports character design, worldbuilding, and transmedia storytelling.
**Next:**

1. Try [Your First Character](tutorial/first-character.md)
2. Add depth with [Adding Personality](tutorial/personality.md)
3. Browse the [Examples Gallery](authoring/examples.md)

---

### ⚙️ For Technical Teams

Start with [Technical Applications](use-cases/technical.md)
Discover metadata management, validation pipelines, and API integration.
**Next:**

1. Set up the [Python Validator](integration/python-validator.md) or [TypeScript Validator](integration/js-ts-validator.md)
2. Explore [Extensions & Namespaces](integration/extensions-and-namespaces.md)
3. Review [Implementation Examples](authoring/examples.md)

---

### 🎮 For Game Developers

Start with [Interactive & Game Development](use-cases/interactive.md)
Learn how OCD powers NPCs, dialogue systems, and world simulation.
**Next:**

1. Integrate OCD with [Unity](use-cases/unity.md), [Unreal](use-cases/unreal.md), or [Godot](use-cases/godot.md)
2. Validate your character data with OCD
3. Check out [Game Examples](authoring/examples.md)

---

### 🌐 For Community Builders

Start with [Collaboration & Open Ecosystem](use-cases/community.md)
Learn how to contribute to open character libraries and shared creative projects.
**Next:**

1. Read the [Contribution Guide](governance/contributing-to-spec.md)
2. Explore [Community Examples](authoring/examples.md)
3. Join discussions on [GitHub](https://github.com/Open-Character-Design/OCD-Specification/discussions)

---

## Quick Validation

Let’s validate your first character file.

`sample-character.yaml`

```yaml
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

Run:

```bash
ocd-validate sample-character.yaml
```

You should see:

```
✅ Validation successful
📝 0 warnings
```

If you do — congrats! Your OCD validator is working.

---

## Understanding Validation Output

| Symbol | Meaning      | Example                               |
| :----- | :----------- | :------------------------------------ |
| ✅      | **Success**  | All fields valid                      |
| ⚠️     | **Warnings** | Normalizations or non-critical issues |
| ❌      | **Errors**   | Missing or invalid fields             |

Example:

```
❌ Validation failed
🚨 2 errors:
  - Missing required field: ocd_version
  - Invalid identity kind: 'invalid-kind'
```

---

## Common Issues

| Issue                   | Cause                         | Fix                                              |
| :---------------------- | :---------------------------- | :----------------------------------------------- |
| Missing Required Fields | `ocd_version` or `id` missing | Add the missing field                            |
| Invalid Values          | Wrong `identity.kind`         | Use a valid kind like `humanoid`, `animal`, etc. |
| Timestamp Format        | Invalid date                  | Use ISO 8601: `2024-01-01T00:00:00Z`             |
| Unresolved References   | Linked character not found    | Create or remove the reference                   |

---

## Advanced Validation

* **Print normalized output:**

  ```bash
  ocd-validate my-hero.yaml --print
  ```

* **Treat warnings as errors:**

  ```bash
  ocd-validate my-hero.yaml --warnings-as-errors
  ```

* **Force input format:**

  ```bash
  ocd-validate my-hero.yaml --format my-format.yaml
  ```

---

## Next Steps

Explore more once you’ve validated your first character:

* 📚 [Tutorial: Your First Character](tutorial/first-character.md)
* 🎭 [Examples Gallery](authoring/examples.md)
* 📖 [Specification Reference](spec/schema-overview.md)
* 🛠️ [Integration Guide](integration/python-validator.md)

---

## Getting Help

If you run into issues:

* Check the [FAQ](faq.md)
* Review the [Specification](spec/schema-overview.md)
* Browse examples or ask in [GitHub Discussions](https://github.com/Open-Character-Design/OCD-Specification/discussions)

---

### ✨ Tip

> OCD doesn’t replace your creativity — it organizes it.
> Think of it as structured imagination or version control for vision.

---
