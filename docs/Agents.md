# Agents & OCD

## Purpose

Agents (AI-driven characters, NPCs, chatbots, or simulation entities) need structured grounding to behave consistently, safely, and immersively. OCD provides the **character blueprint** that an agent runtime can consume, interpret, and operationalize.

---

## 1. How Agents Use OCD

* **Identity & Appearance**
  Provide context for self-description, introductions, and consistent role-play.

* **Personality & Traits**
  Feed into prompt engineering or memory systems; define default stances and biases.

* **Behavior Directives**
  Offer guardrails for tone, improv style, and safety-sensitive topics.

* **Interaction Layer**
  Guides how the agent should communicate (voice, gestures, telepathy, etc.).

* **State Dynamics**
  Represent the evolving “status” of the character (location, mood, health).

* **Meta Properties**
  Allow filtering or runtime adaptation depending on audience or deployment scenario.

---

## 2. Agent Runtime Integration Patterns

### a) Prompt Composition

* Inject OCD data directly into system or developer prompts.
* Example: use `personality.traits` and `behavior_directives.dialogue_style` to build conversational style instructions.

### b) Memory Systems

* Store `background.timeline`, `relationships`, and `goals` in a vector DB for retrieval-augmented generation (RAG).
* Use OCD `id` as the stable key across memories.

### c) State Synchronization

* Periodically update `state_dynamics` (mood, health, morale) as the simulation runs.
* Let agents reflect these states in their dialogue or actions.

### d) Safety & Filtering

* Enforce `meta_properties.appropriateness` and `content_ratings` at runtime.
* Apply `representation_accessibility` to avoid harmful portrayals.

---

## 3. Agent Types Supported

* **Conversational Agents**

  * Chatbots, assistants, role-play companions.
  * OCD guides tone and persona.

* **NPCs in Games**

  * Use `capabilities` and `instincts` for AI behavior trees.
  * Sync with game stats and inventories via `resources` and extensions.

* **Simulation Entities**


  * Model morale, health, and affiliations dynamically with `state_dynamics` and `background`.

* **Narrative Agents**

  * DMs, narrators, or sidekicks using `narrator_notes` and `narrative_hooks`.

---

## 4. Best Practices

* **Normalize First**
  Always run the document through the validator and normalizer. This ensures consistent trait naming (`-` axis) and clean tags.

* **Keep Core + Extensions Separate**
  Core OCD defines portable persona; put system mechanics in `x-*` namespaces.

* **Monitor Warnings**
  Handle lints (`RATING_CONFLICT`, `UNRESOLVED_REF`, etc.) gracefully.

* **Adapt Responsively**
  Agents should treat OCD as guidance, not rigid rules, especially for improv guidelines and narrative hooks.

* **Update State Incrementally**
  Use OCD as both static character sheet and living document. Only mutate `state_dynamics`, not identity or meta.

---

## 5. Example: Grounding a Chat Agent

```yaml
ocd_version: "1.0.0"
id: npc-barkeep-01
names:
  canon: "Mira the Barkeep"
identity:
  kind: humanoid
  species: Human
personality:
  summary: "Witty, gossipy innkeeper with a warm heart"
  traits:
    - name: "serious-playful"
      kind: bipolar
      polarity: 0.7
      intensity: 0.8
behavior_directives:
  portrayal_tips: ["Share rumors freely, but keep a secret or two back"]
  dialogue_style:
    register: casual
    pace: lively
meta:
  tags: [npc, barkeep, inn]
  versioning:
    created_at: "2025-09-28T12:00:00Z"
    last_modified: "2025-10-01T12:00:00Z"
```

**Runtime usage:**

* Persona grounding: *“You are Mira, a playful innkeeper…”*
* Style injection: lively, casual register.
* Hooks: conversation starters drawn from `behavior_directives.portrayal_tips`.

**Tip:** Populate the top-level `names` block (`canon`, optional `display`/`aliases`) instead of relying on `identity.name`. The legacy field remains loadable for backward compatibility but should be treated as deprecated.

---

## 6. Future Directions

* **Agent SDKs**: Wrappers in Python/JS to auto-generate prompts from OCD docs.
* **Dynamic Linking**: Real-time updates of `state_dynamics` via pub/sub to agent frameworks.
* **Cross-Agent Consistency**: Multi-character systems where each NPC shares references via `relationships` and external IDs.
