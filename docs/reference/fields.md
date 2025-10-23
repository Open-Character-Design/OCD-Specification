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
