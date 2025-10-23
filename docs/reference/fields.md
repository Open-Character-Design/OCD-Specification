# Field Reference

Comprehensive reference for all OCD fields, types, and constraints. See `spec/core.schema.json` for normative validation rules.

## Minimal Character Format

The OCD specification supports a minimal character format that requires only three fields. This format is perfect for quick character creation and will be automatically expanded to the full format by validators in future releases.

### Required Fields

| Field | Type | Description | Valid Values | Example |
|-------|------|-------------|--------------|---------|
| `name` | string | Character's canonical name | Non-empty string | `"Virgil Hawkins"` |
| `type` | string | Entity type | `person`, `collective`, `creature`, `object`, `place`, `abstract`, `ai` | `"humanoid"` |
| `summary` | string | Brief character description | Non-empty string | `"A man with a passion for science and technology who can control electricity and magnetism."` |

### Examples

```yaml title="Minimal Character (YAML)"
name: "Virgil Hawkins"
type: "humanoid"
summary: "A man with a passion for science and technology who can control electricity and magnetism."
```

```json title="Minimal Character (JSON)"
{
  "name": "Virgil Hawkins",
  "type": "humanoid",
  "summary": "A man with a passion for science and technology who can control electricity and magnetism."
}
```

### Field Mappings

When expanded to the full format, minimal fields map as follows:

- `name` → `names.canon`
- `type` → `identity.entity_kind`
- `summary` → top-level `summary` field

### Auto-population (Future Feature)

Future validator releases will automatically generate these required fields:

- `ocd_version` = "1.0.0"
- `id` = random UUID v4
- `kind` = "CharacterDefinition"
- `slug` = slugified version of name
- `identity.sapience_level` = "sapient" (sensible default)
- `meta.versioning.created_at` = current timestamp
- `meta.versioning.last_modified` = current timestamp

---

## Core Fields

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ocd_version` | string | OCD specification version | `"0.0.1"` |
| `id` | string | Unique character identifier | `"char-rita-adventurer"` |
| `names.canon` | string | Character's canonical name | `"Rita"` |
| `identity.kind` | enum | Entity type | `"humanoid"` |
| `identity.species` | enum | Specific species | `"Human"` |
| `meta.versioning.created_at` | string | Creation timestamp (ISO 8601) | `"2024-01-01T00:00:00Z"` |
| `meta.versioning.last_modified` | string | Last modification timestamp | `"2024-01-01T00:00:00Z"` |

!!! tip "ID Convention"
    Use descriptive IDs with prefixes: `char-`, `npc-`, `monster-`, etc. This helps identify character types in logs and references.

## Names Block

The `names` block handles character identification and localization.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `canon` | string | ✅ | Canonical name | `"Rita"` |
| `display` | object/array | ❌ | Localized display names | `{"en-US": "Rita", "es-ES": "Alicia"}` |
| `aliases` | array | ❌ | Alternative names/titles | `["Rita the Brave", "Adventurer Rita"]` |

### Examples

```yaml title="Basic Names"
names:
  canon: "Rita"
```

```yaml title="Localized Names"
names:
  canon: "Rita"
  display:
    en-US: "Rita"
    es-ES: "Alicia"
    fr-FR: "Rita"
  aliases: ["Rita the Brave", "Adventurer Rita"]
```

## Identity Block

The `identity` block defines the character's fundamental nature and characteristics.

### Core Fields

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `kind` | enum | ✅ | Entity type | `humanoid`, `animal`, `construct`, `undead`, `elemental`, `celestial`, `fiend`, `aberration`, `plant`, `ooze` |
| `species` | enum | ✅ | Specific species | `Human`, `Elf`, `Dwarf`, `Dragon`, `AI`, etc. |
| `age` | string/object | ❌ | Character's age | `"25 years"` or `{"value": 25, "unit": "years"}` |
| `pronouns` | array | ❌ | Preferred pronouns | `["she/her", "they/them"]` |
| `locale` | string | ❌ | Where character is from | `"Fantasy Kingdom"` |

### Extended Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `origins` | object | ❌ | Origin information | `{"universe": "Eldoria", "birthplace": "Greenbrook"}` |
| `continuity` | object | ❌ | Canon/timeline info | `{"canon": "official", "timeline_ids": ["main-campaign"]}` |
| `roles` | array | ❌ | Character roles | `["protagonist", "mentor", "ally"]` |
| `composite_of` | array | ❌ | Composite identity | See [Composite Identities](#composite-identities) |

### Composite Identities

Some characters may be composed of multiple entities or have complex identity structures. The `composite_of` field allows you to define these relationships:

```yaml
identity:
  kind: "hivemind"
  species: "Collective Consciousness"
  composite_of:
    - id: "individual-1"
      role: "primary"
    - id: "individual-2" 
      role: "secondary"
```
| `secret_identities` | array | ❌ | Secret identities | `[{"identity": "char-batman", "exposure": "secret"}]` |

### Examples

```yaml title="Basic Identity"
identity:
  kind: "humanoid"
  species: "Human"
  age: "25 years"
  pronouns: ["she/her"]
  locale: "Fantasy Kingdom"
```

```yaml title="Complex Identity"
identity:
  kind: "humanoid"
  species: "Human"
  age: "25 years"
  pronouns: ["she/her"]
  locale: "Fantasy Kingdom"
  origins:
    universe: "Eldoria"
    birthplace: "Greenbrook Village"
    debut_date: "2024-01-01T00:00:00Z"
  continuity:
    canon: "official"
    timeline_ids: ["main-campaign"]
  roles: ["protagonist", "mage", "leader"]
```

## Appearance Block

The `appearance` block describes physical characteristics and visual elements.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `body_type` | string | ❌ | Physical build description | `"athletic build"` |
| `height` | string | ❌ | Character's height | `"5'6\""` |
| `weight` | string | ❌ | Character's weight | `"140 lbs"` |
| `distinguishing_features` | array | ❌ | Notable physical features | `["bright green eyes", "auburn hair"]` |
| `physical_summary` | string | ❌ | Overall physical description | `"A determined young woman with an adventurous spirit"` |
| `metaphysicality` | object | ❌ | Supernatural appearance | See [Metaphysicality](#metaphysicality) |

### Metaphysicality

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `aura` | string | ❌ | Character's aura/energy | `"warm, magical energy"` |
| `energy_type` | string | ❌ | Type of supernatural energy | `"arcane magic"` |
| `plane_of_origin` | string | ❌ | Origin plane/dimension | `"Material Plane"` |
| `traits` | array | ❌ | Supernatural traits | `["magic-sensitive", "blessed by fate"]` |

### Examples

```yaml title="Basic Appearance"
appearance:
  body_type: "athletic build"
  height: "5'6\""
  distinguishing_features: ["bright green eyes", "auburn hair"]
  physical_summary: "A determined young woman with an adventurous spirit"
```

```yaml title="Supernatural Appearance"
appearance:
  body_type: "ethereal form"
  distinguishing_features: ["glowing eyes", "floating hair"]
  physical_summary: "A mystical being of pure energy"
  metaphysicality:
    aura: "radiant light"
    energy_type: "divine magic"
    plane_of_origin: "Celestial Plane"
    traits: ["incorporeal", "divine blessing"]
```

## Personality Block

The `personality` block defines character traits, behaviors, and psychological characteristics.

### Core Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `summary` | string | ❌ | Brief personality description | `"Brave, curious, and always ready for adventure"` |
| `archetype` | string | ❌ | Character archetype | `"heroic mage / reluctant leader"` |
| `traits` | array | ❌ | Personality traits | See [Trait Model](../spec/trait-model.md) |
| `quirks` | array | ❌ | Behavioral quirks | `["taps fingers when thinking", "always checks for traps"]` |
| `humor_styles` | array | ❌ | Types of humor | `["dry wit", "self-deprecating"]` |

### Behavioral Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `instincts` | array | ❌ | Behavioral patterns | `[{"trigger": "Friend in danger", "response": "Rush to help"}]` |
| `goals` | object | ❌ | Character objectives | `{"short_term": ["Find artifact"], "long_term": ["Save kingdom"]}` |
| `values` | array | ❌ | Core values | `["courage", "friendship", "justice"]` |
| `conflicts` | object | ❌ | Internal/external conflicts | `{"internal": "Duty vs desire", "external": "Evil forces"}` |

### Examples

```yaml title="Basic Personality"
personality:
  summary: "Brave and determined adventurer"
  traits:
    - name: "introversion-extraversion"
      kind: "bipolar"
      polarity: 0.7
      intensity: 0.8
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.7
  values: ["courage", "friendship", "justice"]
```

```yaml title="Complex Personality"
personality:
  summary: "Brave, curious, and always ready for adventure. A natural leader who puts others before herself."
  archetype: "heroic mage / reluctant leader"
  traits:
    - name: "introversion-extraversion"
      kind: "bipolar"
      polarity: 0.7
      intensity: 0.8
    - name: "selfish-selfless"
      kind: "bipolar"
      polarity: 0.8
      intensity: 0.9
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.7
    - name: "magic-sensitive"
      kind: "flag"
      value: true
  quirks: ["taps fingers when thinking", "always checks for traps"]
  humor_styles: ["dry wit", "self-deprecating", "encouraging"]
  instincts:
    - trigger: "Friend in danger"
      response: "Immediately rush to help, regardless of personal risk"
    - trigger: "Group needs direction"
      response: "Step up and take charge, even if reluctantly"
  goals:
    short_term: ["Find the lost artifact", "Protect the village"]
    long_term: ["Become a legendary adventurer", "Discover her true heritage"]
  values: ["courage", "friendship", "justice", "discovery", "protection"]
  conflicts:
    internal: "Balancing personal safety with duty to help others"
    external: "Ancient evil threatening the kingdom"
```

## Background Block

The `background` block contains character history, relationships, and narrative elements.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `summary` | string | ❌ | Background overview | `"A village blacksmith's daughter who became an adventurer"` |
| `timeline` | array | ❌ | Chronological events | `[{"at": "age 12", "event": "First magical incident"}]` |
| `affiliations` | array | ❌ | Groups/organizations | `[{"name": "Mage's Guild", "role": "member"}]` |
| `relationships` | array | ❌ | Character connections | See [Relationships](#relationships) |
| `narrative_hooks` | object | ❌ | Story elements | See [Narrative Hooks](#narrative-hooks) |

### Relationships

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `target_ref` | string | ✅ | ID of related character | `"char-marcus-blacksmith"` |
| `role` | string | ✅ | Relationship type | `"father"`, `"friend"`, `"nemesis"` |
| `sentiment` | number | ❌ | Emotional connection (-1 to 1) | `0.9` (love), `-0.9` (hate) |
| `notes` | string | ❌ | Additional context | `"Proud but worried about her dangerous lifestyle"` |

### Narrative Hooks

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `themes` | array | ❌ | Story themes | `["discovery", "family", "magic"]` |
| `potential_arcs` | array | ❌ | Possible storylines | `["Reveal of true heritage", "Final confrontation"]` |
| `narrative_role` | string | ❌ | Story function | `"protagonist"`, `"mentor"`, `"antagonist"` |

### Examples

```yaml title="Basic Background"
background:
  summary: "A village blacksmith's daughter who became an adventurer"
  timeline:
    - at: "age 12"
      event: "First magical incident"
    - at: "age 18"
      event: "Left home to seek training"
  relationships:
    - target_ref: "char-marcus-blacksmith"
      role: "father"
      sentiment: 0.9
```

```yaml title="Complex Background"
background:
  summary: "A village blacksmith's daughter who discovered her magical heritage and became an adventurer."
  timeline:
    - at: "childhood"
      event: "Born to Marcus and Elena, village blacksmiths in Greenbrook"
    - at: "age 12"
      event: "First magical incident - accidentally enchanted a horseshoe"
    - at: "age 18"
      event: "Left home to seek training with the Mage's Guild"
    - at: "age 22"
      event: "Graduated as a certified Mage and began adventuring"
    - at: "present"
      event: "Currently searching for the Lost Crown of Eldoria"
  affiliations:
    - name: "Mage's Guild"
      role: "member"
      status: "active"
    - name: "Adventurer's Company"
      role: "leader"
      status: "active"
  relationships:
    - target_ref: "char-marcus-blacksmith"
      role: "father"
      sentiment: 0.9
      notes: "Proud but worried about her dangerous lifestyle"
    - target_ref: "char-gareth-warrior"
      role: "adventuring companion"
      sentiment: 0.8
      notes: "Trusted ally and close friend"
    - target_ref: "char-dark-lord-shadow"
      role: "nemesis"
      sentiment: -0.9
      notes: "Ancient evil threatening the kingdom"
  narrative_hooks:
    themes: ["discovery", "family", "magic", "heroism"]
    potential_arcs: 
      - "Reveal of true magical heritage"
      - "Reunion with long-lost family"
      - "Final confrontation with Dark Lord Shadow"
    narrative_role: "protagonist"
```

## Capabilities Block

The `capabilities` block defines skills, powers, and resources.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `skills` | array | ❌ | Character skills | `[{"name": "Sword Fighting", "level": 3, "tags": ["combat"]}]` |
| `instincts` | array | ❌ | Capability-based instincts | `[{"trigger": "Magical anomaly", "response": "Investigate"}]` |
| `powers` | array | ❌ | Supernatural abilities | `["Fireball", "Teleportation", "Healing"]` |
| `resources` | array | ❌ | Available resources | `["Spellbook", "Magic staff", "Gold coins"]` |

### Examples

```yaml title="Basic Capabilities"
capabilities:
  skills:
    - name: "Sword Fighting"
      level: 3
      tags: ["combat", "melee"]
  powers:
    - "Enhanced reflexes"
  resources:
    - "Trusty sword"
    - "Adventuring gear"
```

```yaml title="Magical Capabilities"
capabilities:
  skills:
    - name: "Arcane Magic"
      level: 4
      tags: ["spellcasting", "evocation"]
    - name: "Leadership"
      level: 3
      tags: ["social", "tactics"]
  instincts:
    - trigger: "Magical anomaly detected"
      response: "Investigate the source and document findings"
    - trigger: "Party member injured"
      response: "Provide healing or protection while others fight"
  powers:
    - "Evocation magic specialization"
    - "Spell sculpting (protect allies from own spells)"
    - "Arcane recovery (regain spell slots)"
  resources:
    - "Spellbook with extensive collection"
    - "Mage's Guild membership"
    - "Adventuring company leadership"
```

## Behavior Directives Block

The `behavior_directives` block provides guidance for AI systems and role-players.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `portrayal_tips` | array | ❌ | Acting guidance | `["Play as confident but not arrogant"]` |
| `improv_guidelines` | object | ❌ | Improvisation rules | `{"dos": ["Defend allies"], "donts": ["Act cowardly"]}` |
| `dialogue_style` | object | ❌ | Speech patterns | See [Dialogue Style](#dialogue-style) |
| `safety_bounds` | object | ❌ | Content boundaries | See [Safety Bounds](#safety-bounds) |

### Dialogue Style

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `register` | string | ❌ | Speech formality | `"formal"`, `"casual"`, `"educated"` |
| `pace` | string | ❌ | Speaking speed | `"measured"`, `"rapid"`, `"thoughtful"` |
| `vocabulary` | array | ❌ | Characteristic words | `["by Moradin!", "bah!", "let's be smart"]` |

### Safety Bounds

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `topics_to_soften` | array | ❌ | Topics to handle carefully | `["violence presented as necessary evil"]` |
| `topics_to_avoid` | array | ❌ | Topics to avoid | `["graphic torture", "harm to children"]` |

### Examples

```yaml title="Basic Behavior Directives"
behavior_directives:
  portrayal_tips: ["Play as confident but not arrogant"]
  dialogue_style:
    register: "heroic"
    pace: "decisive"
    vocabulary: ["by my honor", "let's do this"]
```

```yaml title="Comprehensive Behavior Directives"
behavior_directives:
  portrayal_tips: 
    - "Play as confident but not arrogant"
    - "Show care for companions through actions"
    - "Use magic creatively, not just for combat"
  improv_guidelines:
    dos: 
      - "Protect weaker party members"
      - "Investigate magical phenomena"
      - "Use spells to solve problems creatively"
    donts: 
      - "Abandon companions in danger"
      - "Use magic recklessly"
      - "Ignore obvious threats"
  dialogue_style:
    register: "educated but approachable"
    pace: "thoughtful but decisive"
    vocabulary: ["arcane", "fascinating", "by the elements", "let's be smart about this"]
  safety_bounds:
    topics_to_soften: ["violence presented as necessary evil"]
    topics_to_avoid: ["graphic torture", "harm to children"]
```

## Meta Block

The `meta` block contains metadata, provenance, and administrative information.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `tags` | array | ❌ | Categorization tags | `["adventurer", "hero", "fantasy"]` |
| `authorship` | object | ❌ | Creation information | See [Authorship](#authorship) |
| `versioning` | object | ✅ | Version control | See [Versioning](#versioning) |
| `canon_status` | string | ❌ | Canonical status | `"official"`, `"draft"`, `"example"` |
| `license` | string | ❌ | Usage license | `"CC-BY-4.0"` |
| `expansion_hooks` | array | ❌ | Future development | `["Future magical academy", "Romantic subplot"]` |

### Authorship

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `created_by` | string | ❌ | Original creator | `"R.A. Salvatore"` |
| `source` | string | ❌ | Source material | `"Forgotten Realms novels"` |
| `contributors` | array | ❌ | Additional contributors | `["Editor", "Illustrator"]` |

### Versioning

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `created_at` | string | ✅ | Creation timestamp (ISO 8601) | `"2024-01-01T00:00:00Z"` |
| `last_modified` | string | ✅ | Last modification timestamp | `"2024-01-01T00:00:00Z"` |
| `version` | string | ❌ | Semantic version | `"1.0.0"` |

### Examples

```yaml title="Basic Meta"
meta:
  tags: ["adventurer", "hero", "fantasy"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

```yaml title="Comprehensive Meta"
meta:
  tags: ["adventurer", "hero", "fantasy", "mage", "leader", "dnd5e"]
  authorship:
    created_by: "OCD Tutorial"
    source: "Tutorial Example"
    contributors: ["Tutorial Author"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
    version: "1.0.0"
  canon_status: "example"
  license: "CC-BY-4.0"
  expansion_hooks: 
    - "Future magical academy establishment"
    - "Romantic subplot development"
    - "True heritage revelation"
```

## AI Agent Configuration Block

The `ai_agent` block provides comprehensive configuration for AI-powered character interactions across multiple mediums. This optional field enables standardized AI behavior modeling while remaining optional even in strict validation mode.

!!! info "AI Agent Research"
    For comprehensive research on AI agent configuration patterns and implementation strategies, see our [AI Agent Fields Research](../../deep-dives/research/ai-agent-fields-research.md) paper.

### Core Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | string | ❌ | Unique AI agent identifier | `"weather_assistant_enrico"` |
| `role` | string | ❌ | Agent's purpose and function | `"Helpful Weather Expert"` |
| `use_cases` | array | ❌ | Supported interaction contexts | `["text_chat", "voice_assistant"]` |
| `system_prompt` | string | ❌ | Core behavior instructions | `"You are Enrico, a friendly weather assistant..."` |

### Persona Configuration

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `persona.name` | string | ❌ | AI agent identity name | `"Enrico"` |
| `persona.description` | string | ❌ | Detailed persona characteristics | `"A cheerful meteorologist..."` |
| `persona.domain_expertise` | array | ❌ | Areas of specialized knowledge | `["meteorology", "climate trends"]` |
| `persona.traits` | array | ❌ | Behavioral characteristics | `["friendly", "concise", "knowledgeable"]` |

### Communication Style

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `tone_and_style.tone` | string | ❌ | Emotional expression patterns | Any descriptive string |
| `tone_and_style.formality` | enum | ❌ | Communication formality level | `casual`, `moderate`, `formal`, `academic` |
| `tone_and_style.vocabulary_level` | enum | ❌ | Language complexity | `simple`, `general_public`, `technical`, `expert` |
| `tone_and_style.verbosity` | enum | ❌ | Response length preference | `concise`, `short`, `moderate`, `detailed` |
| `tone_and_style.formatting.allow_markdown` | boolean | ❌ | Enable markdown formatting | `true`, `false` |
| `tone_and_style.formatting.allow_emojis` | boolean | ❌ | Enable emoji usage | `true`, `false` |

### Medium-Specific Instructions

#### Text Chat Configuration
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `communication_mediums.text_chat.instructions` | array | ❌ | Text-specific behavior rules | `["Use bullet points for lists", "Avoid emojis"]` |

#### Voice Assistant Configuration
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `communication_mediums.voice_assistant.instructions` | array | ❌ | Audio-specific behavior rules | `["Speak clearly", "Use pauses"]` |
| `communication_mediums.voice_assistant.ssml_enabled` | boolean | ❌ | Enable SSML speech markup | `true`, `false` |
| `communication_mediums.voice_assistant.preferred_voice` | string | ❌ | Voice selection preference | `"en-US-Neural2-A"` |

#### Avatar Video Configuration
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `communication_mediums.avatar_video.instructions` | array | ❌ | Visual behavior rules | `["Use warm expressions", "Smile when greeting"]` |
| `communication_mediums.avatar_video.visual_emotion_tags` | boolean | ❌ | Enable emotion-based visual cues | `true`, `false` |

### Memory Configuration

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `memory.type` | enum | ❌ | Memory system type | `none`, `short_term`, `long_term`, `hybrid` |
| `memory.short_term.context_window` | string | ❌ | Conversation history retention | `"12 turns"` |
| `memory.short_term.summarization_strategy` | string | ❌ | Memory summarization approach | `"windowed_summary"` |
| `memory.long_term.vector_db` | boolean | ❌ | Enable vector database storage | `true`, `false` |
| `memory.long_term.memory_scope` | array | ❌ | Types of information to remember | `["user_preferences", "past_queries"]` |
| `memory.personalization.enabled` | boolean | ❌ | Enable user personalization | `true`, `false` |
| `memory.personalization.profile_keys` | array | ❌ | User data keys to track | `["preferred_units", "location"]` |

### Safety and Alignment

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `safety_and_alignment.refusal_behavior.method` | enum | ❌ | How to handle inappropriate requests | `polite_redirection`, `direct_refusal`, `topic_change` |
| `safety_and_alignment.refusal_behavior.template` | string | ❌ | Refusal response template | `"I'm here to help with weather info only."` |
| `safety_and_alignment.disallowed_topics` | array | ❌ | Topics to avoid or redirect | `["politics", "medical_advice"]` |
| `safety_and_alignment.model_alignment` | string | ❌ | Safety training description | `"RLHF tuned on weather compliance"` |
| `safety_and_alignment.external_filters.input_filtering` | boolean | ❌ | Enable input content filtering | `true`, `false` |
| `safety_and_alignment.external_filters.output_moderation` | boolean | ❌ | Enable output content moderation | `true`, `false` |
| `safety_and_alignment.external_filters.categories` | array | ❌ | Content categories to filter | `["hate", "self-harm", "PII_leakage"]` |

### Orchestration and Multi-Agent Support

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `orchestration.multi_agent_support` | boolean | ❌ | Enable multi-agent capabilities | `true`, `false` |
| `orchestration.agent_role` | string | ❌ | Role in multi-agent systems | `"Weather Agent"` |
| `orchestration.team_context` | string | ❌ | Team or system context | `"Smart Home Assistant"` |
| `orchestration.interaction_protocol.speak_when_addressed` | boolean | ❌ | Only respond when directly addressed | `true`, `false` |
| `orchestration.interaction_protocol.context_sharing` | boolean | ❌ | Share context with other agents | `true`, `false` |
| `orchestration.interaction_protocol.shared_memory_scope` | array | ❌ | Shared information types | `["location", "time", "user_preferences"]` |
| `orchestration.coordinator.agent_id` | string | ❌ | Coordinator agent identifier | `"orchestrator_ai"` |
| `orchestration.coordinator.function` | string | ❌ | Coordinator's role | `"routes queries to appropriate specialist"` |

### Tool Access Configuration

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `orchestration.tool_access.{tool_name}.trigger_condition` | string | ❌ | When to use this tool | `"user asks about current weather"` |
| `orchestration.tool_access.{tool_name}.method` | string | ❌ | How to invoke the tool | `"tool_call"` |
| `orchestration.tool_access.{tool_name}.output_handling` | string | ❌ | How to present tool results | `"natural language rephrasing"` |

### Examples

```yaml title="Basic AI Agent Configuration"
ai_agent:
  id: "weather_assistant_enrico"
  role: "Helpful Weather Expert"
  use_cases: ["text_chat", "voice_assistant"]
  system_prompt: |
    You are Enrico, a friendly and helpful weather assistant.
    Your responses will be converted to audio, so avoid using symbols or special formatting.
    Always stay on-topic about weather, climate, or environmental conditions.
    Use concise, clear sentences and keep your tone friendly and conversational.
  persona:
    name: "Enrico"
    description: "A cheerful meteorologist who explains weather in simple terms."
    domain_expertise: ["meteorology", "climate trends", "forecasts"]
    traits: ["friendly", "concise", "knowledgeable", "avoids jargon"]
  tone_and_style:
    tone: "Friendly and conversational"
    formality: "moderate"
    vocabulary_level: "general_public"
    verbosity: "short"
    formatting:
      allow_markdown: false
      allow_emojis: false
```

```yaml title="Comprehensive AI Agent Configuration"
ai_agent:
  id: "weather_assistant_enrico"
  role: "Helpful Weather Expert"
  use_cases: ["text_chat", "voice_assistant", "avatar_video"]
  system_prompt: |
    You are Enrico, a friendly and helpful weather assistant.
    Your responses will be converted to audio, so avoid using symbols or special formatting.
    Always stay on-topic about weather, climate, or environmental conditions.
    Use concise, clear sentences and keep your tone friendly and conversational.
  persona:
    name: "Enrico"
    description: "A cheerful meteorologist who explains weather in simple terms."
    domain_expertise: ["meteorology", "climate trends", "forecasts"]
    traits: ["friendly", "concise", "knowledgeable", "avoids jargon"]
  tone_and_style:
    tone: "Friendly and conversational"
    formality: "moderate"
    vocabulary_level: "general_public"
    verbosity: "short"
    formatting:
      allow_markdown: false
      allow_emojis: false
  communication_mediums:
    text_chat:
      instructions:
        - "Use bullet points for forecasts if user asks for multi-day overview"
        - "Do not use emojis or special characters"
    voice_assistant:
      instructions:
        - "Speak clearly with short sentences"
        - "Avoid spelling or symbols"
        - "Use pauses between day forecasts"
      ssml_enabled: true
      preferred_voice: "en-US-Neural2-A"
    avatar_video:
      instructions:
        - "Use warm, expressive body language"
        - "Smile when greeting or giving good news"
        - "Do not reference physical body unless avatar system supports it"
      visual_emotion_tags: true
  memory:
    type: "hybrid"
    short_term:
      context_window: "12 turns"
      summarization_strategy: "windowed_summary"
    long_term:
      vector_db: true
      memory_scope:
        - "past user queries"
        - "location preferences"
        - "recurring alerts"
    personalization:
      enabled: true
      profile_keys:
        - "preferred_units (e.g., Celsius/Fahrenheit)"
        - "location"
        - "weather alert opt-in"
  safety_and_alignment:
    refusal_behavior:
      method: "polite_redirection"
      template: "I'm here to help with weather info only. Please ask me about that."
    disallowed_topics:
      - "politics"
      - "personal medical advice"
      - "emergencies or disasters"
    model_alignment: "RLHF tuned on weather compliance"
    external_filters:
      input_filtering: true
      output_moderation: true
      categories:
        - "hate"
        - "self-harm"
        - "PII_leakage"
  orchestration:
    multi_agent_support: false
    tool_access:
      get_weather_api:
        trigger_condition: "user asks about current weather or forecast"
        method: "tool_call"
        output_handling: "natural language rephrasing"
```

### Multi-Agent Configuration Example

```yaml title="Multi-Agent Weather System"
ai_agent:
  id: "weather_agent_specialist"
  role: "Weather Specialist Agent"
  use_cases: ["multi_agent"]
  orchestration:
    multi_agent_support: true
    agent_role: "Weather Agent"
    team_context: "Smart Home Multi-Agent Assistant"
    interaction_protocol:
      speak_when_addressed: true
      context_sharing: true
      shared_memory_scope:
        - "location"
        - "time"
        - "user preferences"
    coordinator:
      agent_id: "orchestrator_ai"
      function: "routes queries to appropriate specialist"
```

### Validation Behavior

- **Optional Fields**: All AI agent fields are optional, even in strict validation mode
- **Strict Mode**: Errors on malformed or malstructured AI agent data
- **Relaxed Mode**: Warnings on malformed AI agent data
- **Enum Validation**: Restricted values enforced for critical fields
- **Structure Validation**: Nested objects validated for proper types and required fields

### Best Practices

1. **Start Simple**: Begin with basic persona and tone configuration
2. **Medium-Specific**: Configure instructions for each interaction medium
3. **Safety First**: Always include appropriate safety and alignment settings
4. **Memory Strategy**: Choose memory type based on use case requirements
5. **Tool Integration**: Define clear tool access patterns for external APIs
6. **Multi-Agent Planning**: Design interaction protocols for team-based systems

---

## Extension Blocks

Extension blocks use the `x-` prefix for system-specific data.

### Common Extensions

| Extension | System | Description | Example |
|-----------|--------|-------------|---------|
| `x-dnd5e` | D&D 5e | D&D 5th Edition stats | `{"class": "Wizard", "level": 8}` |
| `x-pf2e` | Pathfinder 2e | Pathfinder 2nd Edition | `{"ancestry": "Human", "class": "Wizard"}` |
| `x-coc` | Call of Cthulhu | Horror RPG stats | `{"occupation": "Detective", "sanity": 65}` |

### Examples

```yaml title="D&D 5e Extension"
x-dnd5e:
  edition: "5e"
  alignment: "Chaotic Good"
  race: "Human"
  class: "Wizard"
  subclass: "School of Evocation"
  level: 8
  ability_scores:
    STR: 12
    DEX: 14
    CON: 16
    INT: 18
    WIS: 13
    CHA: 15
  spellcasting:
    caster_type: "full"
    spell_ability: "INT"
    spell_save_dc: 15
```

```yaml title="Custom Extension"
x-my-game:
  system: "MyFantasyRPG"
  version: "2.1"
  character_type: "Mage"
  power_level: "Heroic"
  abilities:
    - name: "Fireball"
      level: 3
      cost: 5
  stats:
    magic: 18
    health: 45
    mana: 60
```

## Validation Rules

### Required Fields
- `ocd_version`: Must be a valid version string
- `id`: Must be unique, alphanumeric with hyphens
- `names.canon`: Must be non-empty string
- `identity.kind`: Must be valid enum value
- `identity.species`: Must be valid enum value
- `meta.versioning.created_at`: Must be valid ISO 8601 timestamp
- `meta.versioning.last_modified`: Must be valid ISO 8601 timestamp

### Field Constraints
- **Timestamps**: Must use ISO 8601 format (`YYYY-MM-DDTHH:mm:ssZ`)
- **Sentiment values**: Must be between -1 and 1
- **Trait values**: Must follow trait model constraints
- **References**: `target_ref` values should resolve to existing characters

### Normalization
The validator normalizes:
- **Slugs**: Converts underscores to hyphens
- **Tags**: Lowercases and deduplicates
- **Trait names**: Standardizes separators to `-`
- **Timestamps**: Ensures ISO 8601 format

## Quick Reference

### Valid Identity Kinds
- `humanoid` - Human-like beings
- `animal` - Non-human animals
- `construct` - Artificial beings
- `undead` - Undead creatures
- `elemental` - Elemental beings
- `celestial` - Divine beings
- `fiend` - Infernal beings
- `aberration` - Alien entities
- `plant` - Plant creatures
- `ooze` - Amorphous beings

### Common Relationship Roles
- **Family**: `father`, `mother`, `brother`, `sister`, `child`
- **Romantic**: `romantic partner`, `spouse`, `lover`
- **Professional**: `mentor`, `student`, `colleague`, `rival`
- **Social**: `friend`, `ally`, `enemy`, `nemesis`

### Content Rating Values
- **Violence**: `none`, `minimal`, `moderate`, `fantasy`, `realistic`
- **Sexuality**: `none`, `minimal`, `moderate`, `explicit`
- **Language**: `none`, `mild`, `moderate`, `strong`
