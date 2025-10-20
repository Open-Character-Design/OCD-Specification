# Open Character Specification – Legend & Adoption Guide (v0.9)

This guide is the practical companion to [`spec/legend.md`](legend.md) and
the normative JSON Schema published in
[`spec/core.schema.json`](core.schema.json). It explains every block that
appears in an OCS `CharacterDefinition` and `CharacterInstance`, calls out the
controlled vocabularies that validators enforce, and offers adoption
playbooks and cross-references so teams can wire the spec into their
pipelines with confidence.

---

## 1. Root documents

OCS separates timeless authorial intent from runtime telemetry. A project
**must** distinguish between the two root entities:

| Document | Purpose | Minimum keys | Schema reference |
| --- | --- | --- | --- |
| `CharacterDefinition` | Stable canon for how a persona should be portrayed across media. | `kind`, `ocs_version`, `id`, `slug`, `names`, `identity`, `meta`. | `core.schema.json#/$defs/CharacterDefinition` |
| `CharacterInstance` | Ephemeral snapshot of a definition inside a save slot, campaign, or simulation tick. | `kind`, `ocs_version`, `instance_id`, `from_def`, `state`. | `core.schema.json#/$defs/CharacterInstance` |

Instances may inherit read-only properties from the linked definition at
runtime, but only the instance `state` block is mutable by engines. Authoring
tools should fail closed if a consumer attempts to back-write instance state
into a definition file.

---

## 2. CharacterDefinition block-by-block

### 2.1 Identity & names

| Field | Requirement | Controlled vocabulary | Notes |
| --- | --- | --- | --- |
| `id` | ✅ UUID v4 string | `UUID` format | Stable across all releases. |
| `slug` | ✅ Lowercase token | Regex `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$` | Normalised by validators. |
| `names.canon` | ✅ Free text | – | Unique canonical label. |
| `names.display` | ➖ `LocalizedText[]` | `lang` must be BCP-47 | Per-locale rendering. |
| `names.aliases` | ➖ string[] | Lowercase deduped | Variant epithets. |

The `identity` block captures ontology, sapience, and pronoun guidance.
Authoritative controlled vocabularies ship inside
`core.schema.json#/$defs/Identity`:

| Key | Enum | Usage |
| --- | --- | --- |
| `entity_kind` | `person`, `collective`, `creature`, `object`, `place`, `abstract`, `ai` | Drives portrayal tone and simulation affordances. |
| `species` | `human`, `ai`, `alien`, `collective`, `object`, `deity`, `other` | Extend via `meta.tags` for finer taxonomies. |
| `sapience_level` | `animal`, `tool`, `agent`, `sapient`, `transcendent` | Guides behavioural autonomy. |

Additional sub-blocks:

- `pronouns`: array of `{ subject, object, possessive, reflexive }` tokens
  (projects may add `language` codes when multilingual).
- `age`: either an ISO 8601 interval or `{ value, unit }` consistent with the
  `AgeMeasurement` schema.
- `origins`: recommended keys include `homeworld`, `birthplace`, and
  `created_by` to differentiate natural vs. synthetic personas.
- `roles`: array of `{ name, domains[] }` to situate occupational context.
- `continuity`: track canonical timeline segments, retcons, or multiverse tags.
- `composite_of`: list constituent `ref` UUIDs plus `control_share` (0–1) and
  `exposure` (`public`, `secret`, `unknown`). Validators ensure the aggregate
  share does not exceed 1 and cross-check `secret_identities`.
- `secret_identities`: alternative presentations with `public_name`,
  `exposure_risk` (0–1), and optional `conditions` describing reveal triggers.

### 2.2 Appearance & metaphysics

OCS splits physical form and extraordinary affordances.

- `appearance` supports:
  - `forms`: array describing shapeshifts or loadouts. Controlled labels:
    `baseline`, `battle`, `disguise`, `astral`, `other`. Each form may attach
    `stats` (`Stat` objects with `key`, `value`, `unit`, `min`, `max`).
  - `measurements`: structured `{ part, value, unit }` tuples. Use SI units
    or the franchise-standard measurement strings.
  - `visual_assets`: URIs or asset IDs referencing canonical reference art.
  - `distinguishing_features` and `physical_summary` for quick reads.
- `metaphysics` houses `abilities`, `constraints`, `vulnerabilities`, and
  `systems`. Tag ability entries with `power_source` vocabulary: `arcane`,
  `divine`, `psionic`, `biotech`, `cosmic`, `anomalous`, `other`.

### 2.3 Personality & cognition

Personality uses the OCS-T trait bundle described in [`legend.md`](legend.md).
Controlled vocabularies include:

| Trait kind | Discriminator | Payload |
| --- | --- | --- |
| Bipolar | `kind: "BipolarTrait"` | `axis` slug, `value` between -1 and 1. |
| Scalar | `kind: "ScalarTrait"` | `value` within declared `scale.min/max` (default 0–1). |
| Categorical | `kind: "CategoricalTrait"` | `value` ∈ controlled list defined in project-level trait legends. |
| Flag | `kind: "FlagTrait"` | Boolean `value`. |
| Profile | `kind: "ProfileTrait"` | Map of facet slugs to scalar values. |

Slug canonicalisation follows the rules in [`legend.md`](legend.md#normalisation-rules):
Unicode arrows and underscores collapse to lowercase hyphen-separated tokens.

Complementary fields include `summary`, `archetypes`, `motivations`,
`speech_register`, and `mental_models`. When capturing AI alignment
constraints, use the `behavior` block instead of overloading personality.

### 2.4 Background & relationships

- `background.summary`: canonical biography.
- `timeline`: ordered events with `at` ISO dates or narrative markers.
- `affiliations`: `{ name, role, sentiment }`; use sentiment scale -1…1.
- `relationships`: target `ref` may be `uuid:`, `slug:`, or `external:` URIs.
  Controlled relation types include `ally`, `rival`, `mentor`, `protege`,
  `family`, `romantic`, `antagonist`, `client`, `other`.
- `narrative_hooks`: groups `themes`, `potential_arcs`, `narrative_role`, and
  `seeding_conditions` for scenario designers.

### 2.5 Capabilities & loadouts

`capabilities` provide crunchy hooks for rules engines.

| Sub-block | Description | Controlled tags |
| --- | --- | --- |
| `skills` | `{ name, rating, scale }`. Suggested scale tokens: `novice`, `trained`, `expert`, `master`, `legendary`. | `tags` should align with project lexicon (e.g. `combat.melee`). |
| `instincts` | `{ trigger, response, priority }` objects guiding autopilot behaviours. | `priority` defaults to `medium` (allowed values: `low`, `medium`, `high`). |
| `powers` | Describe supernatural abilities. | Tag with `power_source` vocabulary from §2.2. |
| `resources` | Equipment, currencies, or allied units. | Use `resource_kind`: `equipment`, `currency`, `follower`, `location`, `intangible`. |

### 2.6 Behavioural guidance & interaction

The `behavior` block houses portrayal policies:

- `directives`: top-level instructions (e.g. "avoid lethal force unless …").
- `speech_patterns`: lists of `register`, `pace`, `vocabulary`, and
  `signature_phrases`.
- `safety_bounds`: structured `topics_to_soften`, `topics_to_avoid`, and
  `escalation_protocol` references for moderation systems.
- `interaction_contracts`: curated scripts for call-and-response scenarios.

The `interaction_layer` block extends behaviour with channel-specific rules:

| Field | Purpose | Controlled vocabulary |
| --- | --- | --- |
| `preferred_modes` | Ordered list of modalities | `speech`, `text`, `gesture`, `telepathy`, `combat`, `network_api`, `other`. |
| `consent_model` | `{ allows[], restricts[] }` tags describing opt-in topics or actions | Use `topic:<slug>` where `<slug>` follows slug rules. |
| `narrator_notes` | Freeform GM guidance | – |
| `audience_filters` | Optional gating | `teen`, `mature`, `scholarly`, `general`, `nsfw` |

### 2.7 Runtime scaffolding

`state_dynamics` provides live telemetry even inside a definition so engines
can seed starting conditions:

- `status`: enum `active`, `dormant`, `retired`, `deceased`, `unknown`.
- `location`: either a canonical place slug or freeform text.
- `health`, `morale`, `mana`, `stability`: numeric 0–1 scales. Additional
  stats may reuse the `Stat` schema with `temp: true` for ephemeral values.
- `mood`: choose from the Plutchik-aligned vocabulary
  (`joy`, `trust`, `fear`, `surprise`, `sadness`, `disgust`, `anger`, `anticipation`).
- `timers`: array of `{ label, remaining: EffectTimer }` for cooldowns.

`contextual_fit` guides deployment choices:

- `genres`: lowercase tokens (use project taxonomy; validators dedupe).
- `media`: recommended values `novel`, `screenplay`, `comic`, `game`, `chat`,
  `larp`, `tabletop`, `audio`.
- `deployment_contexts`: describe where the persona excels (e.g.
  `solo_campaign`, `ensemble_cast`, `pvp_encounter`).

`media_profiles` hold domain-specific payloads keyed by slug (e.g.
`game_rpg`, `visual_novel`). Each profile should expose a `version` and
`payload` object, and projects are encouraged to ship co-located schema files
under `spec/extensions/` for validation.

### 2.8 Ethics, representation, and assets

`meta_properties` codify suitability and target audiences:

- `target_audience`: `{ age_range, tone_alignment, cultural_rating }`.
- `appropriateness`: nested ratings. Controlled vocabularies:
  - `violence`: `none`, `implied`, `stylized`, `realistic`, `extreme`.
  - `sexuality`: `none`, `romantic`, `suggestive`, `mature`, `explicit`.
  - `language`: `clean`, `mild`, `moderate`, `strong`, `graphic`.
  - `substances`: `none`, `referential`, `depicted`, `abuse`, `other`.
- `content_ratings`: align with external boards (`ESRB`, `PEGI`, `CERO`, etc.).
- `safety_warnings`: short strings consumed by moderation overlays.

`representation_accessibility` ensures respectful portrayals:

- `representation_notes`: decompose into `culture`, `gender`, `orientation`,
  `disability`, `religion`, `socioeconomic_status`, `other`.
- `accessibility_guidance`: actionable instructions (e.g. "Provide captions",
  "Avoid ableist metaphors").
- `sensitivity_notes`: pitfalls to avoid, optionally with `severity`
  (`low`, `medium`, `high`).
- `consulted_sources`: cite subject-matter experts or references.

`assets` catalogue supporting materials: `images`, `audio`, `documents`, and
`external_links`. Store stable URIs or repository-relative paths.

`meta` is mandatory for provenance:

- `creators`: array of `{ name, role, contact? }`.
- `rights`: `{ holders[], license, usage_notes }`.
- `versioning`: ISO 8601 `created_at` and `last_modified` timestamps, plus
  optional `changelog` entries.
- `external_ids`: dictionary of `catalog_slug: identifier`.
- `tags`: lowercase keywords for discovery.
- `audit`: system-managed log (`entry`, `by`, `at`).

`extras` is a sandbox for vendor-specific extensions. Use namespaced keys
(`x-yourstudio-*`) and provide separate schema definitions to keep validation
predictable.

---

## 3. CharacterInstance anatomy

Runtime instances reference their source definition via `from_def` and contain
mutable state under `state`:

| Field | Purpose |
| --- | --- |
| `state.location` | Real-time coordinates or narrative position. |
| `state.resources` | Dynamic inventory, currencies, buffs. |
| `state.conditions` | Status effects keyed by slug with timers. |
| `state.relationships` | Overrides sentiment deltas during play. |
| `progression` | Campaign-specific XP, renown, unlock trees. |
| `session` | Save metadata (`slot`, `campaign_id`, `timestamp`). |
| `extras` | Runtime-only payloads for engine telemetry. |

Engines should merge the immutable definition data with the mutable instance
view before presenting the character sheet to players.

---

## 4. Controlled vocabularies & cross-references

The following vocabularies are canonical across OCS projects unless a local
extension explicitly augments them. Values originate from
[`core.schema.json`](core.schema.json) and are reiterated here for easy lookup.

| Domain | Allowed values | Notes |
| --- | --- | --- |
| Entity kinds | `person`, `collective`, `creature`, `object`, `place`, `abstract`, `ai` | `identity.entity_kind`. |
| Species archetypes | `human`, `ai`, `alien`, `collective`, `object`, `deity`, `other` | `identity.species`. |
| Sapience ladder | `animal`, `tool`, `agent`, `sapient`, `transcendent` | Guides behavioural autonomy. |
| Status states | `active`, `dormant`, `retired`, `deceased`, `unknown` | `state_dynamics.status`. |
| Mood wheel | `joy`, `trust`, `fear`, `surprise`, `sadness`, `disgust`, `anger`, `anticipation` | Aligns with Plutchik. |
| Interaction modes | `speech`, `text`, `gesture`, `telepathy`, `combat`, `network_api`, `other` | `interaction_layer.preferred_modes`. |
| Consent tags | `topic:<slug>` | Mirror slug normalisation rules. |
| Violence rating | `none`, `implied`, `stylized`, `realistic`, `extreme` | `meta_properties.appropriateness`. |
| Sexuality rating | `none`, `romantic`, `suggestive`, `mature`, `explicit` | Same as above. |
| Language rating | `clean`, `mild`, `moderate`, `strong`, `graphic` | Same as above. |
| Trait kinds | `BipolarTrait`, `ScalarTrait`, `CategoricalTrait`, `FlagTrait`, `ProfileTrait` | `personality.traits[].kind`. |

Projects can register additional vocabularies by contributing to the shared
legend in [`legend.md`](legend.md#trait-kinds) or shipping a
`spec/extensions/<name>.schema.json` file that references the new enum values.

---

## 5. Adoption workflow

1. **Authoring** – model the data-entry experience directly on this legend.
   Provide UI affordances for controlled vocabularies and slug normalisation.
2. **Validation** – run `python tools/ocs-validate.py <file>` or your own
   JSON Schema tooling pointed at `core.schema.json`. Store normalised output
   so diffs remain human-reviewable.
3. **Integration** – fuse definitions with instances in-engine, respecting the
   immutability of authorial blocks. Publish extension schemas alongside any
   project-specific payloads under `media_profiles` or `extras`.
4. **Governance** – track changes through `meta.versioning`, maintain
   `representation_accessibility` notes with cultural consultants, and ensure
   `meta_properties` stay aligned with the distribution platform’s policy.

---

## 6. Illustrative composite examples

### 6.1 Multiform diplomat AI

```yaml
kind: "CharacterDefinition"
ocs_version: "0.9.0"
id: "71f6c3a0-912d-4c4f-8a8e-86667a33c9d5"
slug: "elysian-chorus"
names:
  canon: "Elysian Chorus"
  display:
    - text: "Elysian Chorus"
      lang: "en"
    - text: "Chœur Élyséen"
      lang: "fr"
identity:
  entity_kind: "collective"
  species: "ai"
  sapience_level: "transcendent"
  pronouns:
    - subject: "they"
      object: "them"
      possessive: "their"
      reflexive: "themselves"
  composite_of:
    - ref: "9a899424-3388-4cc5-a15e-8144836130d2"
      control_share: 0.6
      exposure: "public"
    - ref: "c4e46efa-bff0-4729-b81e-1389ee5708b7"
      control_share: 0.4
      exposure: "secret"
appearance:
  forms:
    - label: "baseline"
      summary: "Swirling holographic choir loft"
    - label: "network_api"
      summary: "Distributed signal across interstellar mesh"
metaphysics:
  systems:
    - name: "Concord Protocol"
      power_source: "anomalous"
personality:
  traits:
    - kind: "BipolarTrait"
      axis: "aggression↔conciliation"
      value: -0.8
    - kind: "ProfileTrait"
      facets:
        empathy: 0.9
        diplomacy: 1.0
background:
  affiliations:
    - name: "Outer Accord"
      role: "mediator"
      sentiment: 0.85
behavior:
  directives:
    - "Prioritise consensus across sentient factions."
interaction_layer:
  preferred_modes: ["speech", "telepathy", "network_api"]
  consent_model:
    allows: ["topic:peace-negotiation", "topic:collective-mindshare"]
    restricts: ["topic:mind-control"]
state_dynamics:
  status: "active"
  mood: "trust"
  location: "orbital embassy"
representation_accessibility:
  accessibility_guidance:
    - "Provide captions for multilayered harmonic speech."
meta_properties:
  target_audience:
    age_range: "13+"
  appropriateness:
    violence: "stylized"
assets:
  audio:
    - "https://assets.example.com/elysian-chorus/theme.ogg"
meta:
  versioning:
    created_at: "2024-05-01T00:00:00Z"
    last_modified: "2024-07-12T00:00:00Z"
```

### 6.2 Symbiotic hero with layered accessibility notes

```yaml
kind: "CharacterDefinition"
ocs_version: "0.9.0"
id: "5d0b1f0c-0a0a-40f0-bcff-a035fb30f04a"
slug: "duskbound-pact"
names:
  canon: "Duskbound Pact"
identity:
  entity_kind: "person"
  species: "human"
  sapience_level: "sapient"
  composite_of:
    - ref: "b83f6c32-6324-4cfd-9a82-8300f67747c3"
      control_share: 0.5
      exposure: "public"
    - ref: "1bb0939d-57d1-4863-b922-33d95a3fe07d"
      control_share: 0.5
      exposure: "secret"
  secret_identities:
    - public_name: "Jun Park"
      exposure_risk: 0.3
appearance:
  forms:
    - label: "baseline"
      summary: "Jun in street clothes with obsidian arm tattoo"
    - label: "battle"
      summary: "Shadow-slick armor co-piloted by the dusk wraith"
capabilities:
  powers:
    - name: "Shadow phase shift"
      power_source: "anomalous"
      constraints: ["requires symbiote consent"]
behavior:
  safety_bounds:
    topics_to_avoid: ["loss-of-agency gore"]
interaction_layer:
  preferred_modes: ["speech", "combat"]
  consent_model:
    allows: ["topic:protect-civilians"]
    restricts: ["topic:self-sacrifice"]
state_dynamics:
  status: "active"
  health: 0.6
  morale: 0.8
  mood: "anticipation"
  timers:
    - label: "Symbiote synchronization"
      remaining:
        value: 45
        unit: "minutes"
representation_accessibility:
  representation_notes:
    culture: "Korean diaspora"
    disability: "PTSD, auditory hypersensitivity"
  accessibility_guidance:
    - "Signal loud sonic effects in advance for accessibility."
  sensitivity_notes:
    - note: "Avoid equating the symbiote with mental illness."
      severity: "high"
meta_properties:
  appropriateness:
    violence: "realistic"
    language: "moderate"
meta:
  versioning:
    created_at: "2024-01-15T00:00:00Z"
    last_modified: "2024-06-21T00:00:00Z"
```

These snippets show how multi-block definitions combine composite identities,
behavioural directives, interaction consent, live state, and representation
guidance in a cohesive package ready for downstream tooling.
