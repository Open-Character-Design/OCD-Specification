# Open Character Specification (OCD) – Legend & Adoption Guide v0.2

## Purpose

The OCD defines a **structured, portable character format** for human authors, AI systems, and machine validation. This guide explains the fields, vocabularies, scales, and extensibility model for adopting OCD in your own projects.

---

## 1) Core Concepts

* **OCD is data‑centric**: every character is a structured object with defined fields.
* **Human + AI friendly**: readable as YAML/JSON or OCD‑T (compact textual grammar).
* **Schema validated**: type and range checks ensure quality.
* **Extensible**: any project‑specific or system‑specific block can be namespaced under `x-*`.
* **Traits support three kinds**: bipolar (axes with polarity/intensity), scalar (single value with optional unit), and flag (boolean presence/absence).

---

## 2) Required Fields

Every valid OCD file must include:

* `ocd_version` – the schema version string.
* `names` – canonical and presentation names (`canon`, `display`, `aliases`).
* `identity` – core descriptors (kind, species, age, etc.).
* `personality` – core character psychology (summary, traits, values).
* `behavior_directives` – portrayal guidance and safety.
* `meta` – tags, authorship, and required versioning timestamps.

---

## 3) Identity

Defines **who/what** the character is.

* `name` – free text *(legacy/back-compat; prefer `names.canon`/`names.display`).*
* `kind` – enum: `humanoid | creature | machine | entity`.
* `species` / `breed` – free text.
* `age` – number or string (supports approximations like "~200+").
* `pronouns` – string.
* `locale` – language or cultural context (ISO‑639‑1 preferred).

**ID convention**: `id` must match `^[a-z0-9][a-z0-9-_:.]{2,64}$`.

---

## 4) Appearance & Metaphysicality

* `body_type` – enums suggested: `humanoid | quadruped | avian | serpentine | amorphous | mechanical_orb | incorporeal | other`.
* `distinguishing_features` – array of strings.
* `physical_summary` – prose.
* `metaphysicality`:

  * `aura`, `energy_type`, `plane_of_origin` – free strings.
  * `traits` – array of metaphysical or ontological notes.

---

## 5) Personality

### Required

* `summary` – prose snapshot.

### Optional

* `archetype` – free label (e.g., "mentor", "trickster").
* `traits` – array of objects, each with a `kind`:

  * **Bipolar**: `{ name, kind: bipolar, polarity [-1..1], intensity [0..1] }`
  * **Scalar**: `{ name, kind: scalar, value [0..1], unit? }`
  * **Flag**: `{ name, kind: flag, value: boolean }`
* `quirks` – string list.
* `humor_styles` – string list.
* `goals` – split into `short_term` and `long_term` arrays.
* `values` – array of guiding principles.
* `conflicts` – internal/external tensions.

**Normalization**: bipolar trait names accept `-`, `_`, or `-`. Canonical form is `-`.

---

## 6) Background

* `summary` – prose history.
* `timeline` – array of `{ at, event }`.
* `affiliations` – groups/orgs.
* `relationships` – `{ target_ref, role, sentiment }`:

  * `target_ref` – must be a valid OCD id or external URI.
  * `sentiment` – float [-1, 1].
* `narrative_hooks` – themes, arcs, roles.

---

## 7) Capabilities

* `skills` – `{ name, level (0..5), tags }`.
* `instincts` – `{ trigger, response }`.
* `powers` – free list.
* `resources` – equipment/items.

---

## 8) Behavior Directives

Defines **how to portray** the character.

* `portrayal_tips` – free text guidance.
* `improv_guidelines` – `dos` and `donts` arrays.
* `dialogue_style` – `{ register, pace, vocabulary[] }`.
* `safety_bounds` – `{ topics_to_soften[], topics_to_avoid[] }`.

---

## 9) Interaction Layer

* `preferred_modes` – e.g., `speech`, `gesture`, `telepathy`.
* `consent_model` – `{ allows[], restricts[] }` (tags, e.g., `violence: defensive only`).
* `narrator_notes` – meta commentary for guides/DMs.

---

## 10) State Dynamics

* `status` – `active | inactive | unknown`.
* `location` – free text.
* `health`, `morale` – float 0..1.
* `mood` – string.

---

## 11) Contextual Fit

* `genres` – lowercase tokens (e.g., `sci-fi`, `fantasy`).
* `media` – target media types (`game`, `novel`, `film`, `chat`).
* `deployment_contexts` – guidance for scenarios.

---

## 12) Meta Properties

* `target_audience`: `{ age_range, tone_alignment }`.
* `appropriateness`:

  * `violence`: `none | cartoon | fantasy | realistic | extreme`
  * `sexuality`: `none | implied | moderate | explicit`
  * `language`: `clean | mild | moderate | explicit`
* `content_ratings`: `[ { system, rating, notes } ]`
* `safety_warnings`: string list.

---

## 13) Representation & Accessibility

* `representation_notes`: identity/culture/orientation details.
* `accessibility_guidance`: play/portrayal safeguards.
* `sensitivity_notes`: pitfalls to avoid.

---

## 14) Assets

* `images`, `audio`, `links` – URLs or references.

---

## 15) Meta

* `tags` – lowercase tokens.
* `authorship`: `{ created_by, source }`.
* `versioning`: `{ created_at, last_modified }` – both ISO‑8601 UTC strings and required.
* `version` – free string.
* `canon_status` – `official | unofficial | alt | fanon`.
* `license` – SPDX or free string.
* `expansion_hooks` – optional roadmap notes.

---

## 16) Extensions

* Any field starting `x-*` is reserved for system‑specific extensions.
* Example: `x-dnd5e`, `x-srd`, `x-game-balance`.
* Extensions may define their own schema, but should be documented separately.

---

## 17) Conformance & Error Policy

* **Reject**: duplicate keys, malformed IDs, invalid enums, out-of-range values.
* **Warn**: unresolved refs, barewords in prose fields, rating conflicts.
* **Normalize**: trim, lowercase, dedupe arrays, coerce numeric/text hybrids.

---

## 18) Adoption Guidance

* **For Authors**: start simple (identity, personality, behavior_directives, meta). Add depth iteratively.
* **For Engineers**: validate via JSON Schema, Zod, or Pydantic; normalize before ingest.
* **For AI Systems**: use `behavior_directives` and `interaction_layer` to guide persona response; apply `meta_properties` for safety filters.
* **For Game Designers**: slot in system extensions (`x-dnd5e`, `x-narrative-arcs`) for sheet data.

---

## 19) Quick Example

```yaml
ocd_version: "0.0.1"
id: char-bruenor
names:
  canon: "Bruenor Battlehammer"
identity:
  kind: humanoid
  species: Dwarf
personality:
  summary: "Gruff but loyal dwarven king"
  traits:
    - name: "introversion-extraversion"
      kind: bipolar
      polarity: 0.2
      intensity: 0.6
behavior_directives:
  portrayal_tips: ["Temper bluster with heart"]
  dialogue_style:
    register: gruff
meta:
  tags: [dwarf, king]
  versioning:
    created_at: "2025-09-25T16:00:00Z"
    last_modified: "2025-09-26T16:00:00Z"
```

---

## 20) Legend Symbols

* - in trait names: bipolar spectrum dimension. Equivalent to `-` or `_` during parse.
* `x-*`: extension namespace.
* `{}`: object, `[]`: array.
* Strings with sentences always quoted. Barewords only for enums/tags.
