# Schema Overview

The CharacterDefinition schema is the foundation of every OCD character.
It defines how creative and technical information fits together, ensuring that characters stay consistent across pipelines, runtimes, and teams.

## TL;DR

OCD schemas make your characters:

* ✅ **Consistent** — same identity across engines, languages, and platforms
* ⚙️ **Structured** — ready for AI, games, or analytics
* 🌍 **Portable** — usable by both humans and machines

---

## CharacterDefinition Structure

![CharacterDefinition block relationships](../assets/diagrams/blocks-overview.svg)

Below is the simplified map of a complete character sheet.

### 🧩 Core Schema Map

```
CharacterDefinition
├── Core Identifiers      # kind · ocd_version · id · slug
├── Names                 # canon · display · aliases
├── Identity              # species · pronouns · embodiment
├── Meta & Versioning     # tags · ratings · timestamps
├── Personality           # traits · instincts
├── Background            # timeline · relationships · affiliations
├── Behavior              # dialogue style · portrayal tips · safety
├── State Dynamics        # mood · health · resources
├── Appearance & Metaphysics  # visual traits · supernatural context
├── Media Profiles        # avatars · voice packs · handles
└── Extensions (x-*)      # project-specific mechanics
```

Each root block has a clear role and consistent validation expectations.

---

### 🧱 Core Blocks

* **Core Identifiers**
  `kind`, `ocd_version`, `id`, and `slug` define the identity and version of a character sheet. Validators use these to determine which profile and rules to apply.

* **Names**
  `names.canon` defines the main label shown to users. `names.display` and `names.aliases` allow localized or alternate representations.

* **Identity**
  Describes biological and metaphysical traits — `species`, `pronouns`, `embodiment`. This ensures downstream systems can generate consistent runtime descriptions.

* **Meta & Versioning**
  Holds metadata such as `tags`, `ratings`, and timestamps (`created_at`, `last_modified`) to track history and content maturity.

---

## Optional Blocks & Vocabularies

Each optional block expands what OCD can represent while maintaining structure.

| Block                | Purpose                                                   | Notes                                                                        |
| :------------------- | :-------------------------------------------------------- | :--------------------------------------------------------------------------- |
| **Personality**      | Defines traits and instincts using the OCD Trait Model.   | Align traits with controlled vocabularies to enable analytics and filtering. |
| **Background**       | Stores relationships, affiliations, and key events.       | Missing references raise `UNRESOLVED_REF` warnings.                          |
| **Behavior**         | Configures dialogue style, tone, and portrayal tips.      | Conflicts between tags and ratings trigger `RATING_CONFLICT` diagnostics.    |
| **State Dynamics**   | Tracks changeable state such as health, energy, or mood.  | Safe for runtime patching without altering identity.                         |
| **Extensions (x-*)** | Defines custom fields for project or engine-specific use. | Keeps the portable core schema clean.                                        |

---

## Authoring to Runtime Flow

OCD is designed to fit smoothly into both creative and technical pipelines.

```
Authoring Workspace
  ↓
Controlled Vocabularies
  ↓
Validation & Normalization
  ↓
Diagnostics Output ─────────→  (Warnings · Reports)
  ↓
Normalized CharacterDefinition JSON
  ↓
├─→ Prompt Templates (AI Personas)
├─→ Agent Memory Stores (RAG / Embeddings)
├─→ Game & Simulation config (State Machines / Behavior Trees)
└─→ Canon & continuity (Story writing / World building)
```

### Key Stages

1. **Authoring** — Narrative teams write structured OCD files in YAML or JSON format.
2. **Controlled Vocabularies** — Validation ensures consistent tags, registers, and rating terms.
3. **Validation & Normalization** — Validators check schema, align traits, and issue diagnostics.
4. **Runtime JSON** — Normalized data feeds into AI prompts, memory stores, or game logic systems.

---

## Example: CharacterDefinition Lifecycle

| Stage          | Input                | Output                                        |
| :------------- | :------------------- | :-------------------------------------------- |
| **Authoring**  | `my-character.ocd`   | Raw creative data                             |
| **Validation** | Validator pass       | Normalized JSON                               |
| **Runtime**    | Normalized JSON      | Used by AI agents, NPCs, and dialogue systems |

---

## Case Studies

### 🕵️ Sherlock Holmes (Investigative NPC)

* **Identity:** `kind: humanoid`, `species: human`
* **Meta:** `tags: [detective, victorian, consulting]`, `ratings.violence: moderate`
* **Behavior:** Formal tone and measured pacing drawn from controlled vocabularies.
* **Background:** `relationships[].target_ref: john-watson` ensures cross-character linkage.

### 🧬 Shuri (Tech-Forward Hero)

* **Names:** Canon `"Shuri"`, aliases `[Princess Shuri, Black Panther]`
* **Personality:** Traits `serious-playful: -0.2`, `logic-intuition: 0.8`
* **State Dynamics:** Tracks `focus: vibranium-research`, `stress` metrics for simulation.
* **Meta:** Content rating `violence: fantasy` for accessibility filters.

---

## OCD Trait Model

The OCD Trait Model provides a structured way to define character psychology using three types of traits:

### Bipolar Traits
Bipolar traits represent personality dimensions with two opposing poles and intensity:

```yaml
personality:
  traits:
    - name: "introversion-extraversion"
      kind: bipolar
      polarity: 0.2    # -1 (introverted) to +1 (extraverted)
      intensity: 0.6   # 0 (neutral) to 1 (strong)
    - name: "logic-intuition"
      kind: bipolar
      polarity: -0.8
      intensity: 0.9
```

### Scalar Traits
Scalar traits represent single values with optional units:

```yaml
personality:
  traits:
    - name: "patience"
      kind: scalar
      value: 0.7       # 0 to 1
      unit: "minutes"  # optional
    - name: "creativity"
      kind: scalar
      value: 0.9
```

### Flag Traits
Flag traits are simple boolean presence/absence indicators:

```yaml
personality:
  traits:
    - name: "optimistic"
      kind: flag
      value: true
    - name: "cynical"
      kind: flag
      value: false
```

### Trait Normalization
- Trait names use hyphens: `logic-intuition` (not `logic_intuition`)
- Polarity ranges from -1 to +1
- Intensity and scalar values range from 0 to 1
- All trait names are normalized to lowercase with hyphens

---

## Authoring Tips

* Always use **ISO 8601 timestamps**: `2025-01-01T00:00:00Z`
* Keep **traits normalized** (`logic-intuition`, not `logic_intuition`)
* Use **controlled vocabularies** for consistency across tools
* Store **custom data** under `x-*` namespaces (e.g., `x-unreal`, `x-ai`)
* Validate early and often. Warnings help catch inconsistencies before deployment

---
