# Examples Gallery

Explore character examples from different genres, systems, and complexity levels. Each example demonstrates OCD features and best practices.

## Featured Characters

<div class="features-grid">

<div class="feature-card">

### 🛡️ [Bruenor Battlehammer](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/bruenor.yaml)

**D&D Warrior-King**

A legendary dwarven fighter from Forgotten Realms, showcasing D&D 5e integration with comprehensive stats, equipment, and background.

**Tags:** `dwarf`, `fighter`, `dnd5e`, `fantasy`, `warrior`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/bruenor.yaml)

</div>

<div class="feature-card">

### 🚀 [Commander Shepard](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/commander-shepard.yaml)

**Sci-Fi Protagonist**

The iconic Mass Effect hero, demonstrating sci-fi character creation with futuristic abilities and interstellar relationships.

**Tags:** `human`, `soldier`, `sci-fi`, `space`, `hero`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/commander-shepard.yaml)

</div>

<div class="feature-card">

### 🎮 [Crash Bandicoot](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/crash-bandicoot.yaml)

**Game Mascot**

A platformer hero showcasing how to represent video game characters with unique abilities and cartoonish personality.

**Tags:** `bandicoot`, `platformer`, `game`, `mascot`, `cartoon`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/crash-bandicoot.yaml)

</div>

<div class="feature-card">

### 🧙‍♀️ [Eve](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/eve.yaml)

**AI Assistant**

A helpful AI character demonstrating modern AI assistant capabilities with clear behavior directives and safety bounds.

**Tags:** `ai`, `assistant`, `helpful`, `modern`, `virtual`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/eve.yaml)

</div>

<div class="feature-card">

### 🤖 [Guilty Spark](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/guilty-spark.yaml)

**Sci-Fi AI**

A Halo AI construct showing how to represent artificial intelligence with complex motivations and technological capabilities.

**Tags:** `ai`, `construct`, `halo`, `sci-fi`, `villain`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/guilty-spark.yaml)

</div>

<div class="feature-card">

### 🐕 [Inuyasha](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/inuyasha.yaml)

**Anime Character**

A half-demon from anime, showcasing how to represent characters with dual natures and complex relationships.

**Tags:** `half-demon`, `anime`, `fantasy`, `warrior`, `romance`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/inuyasha.yaml)

</div>

<div class="feature-card">

### 💀 [Deadpool](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/deadpool.yaml)

**Anti-Hero**

The Merc with a Mouth, demonstrating how to represent chaotic characters with fourth-wall breaking abilities.

**Tags:** `mutant`, `anti-hero`, `comedy`, `marvel`, `chaotic`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/deadpool.yaml)

</div>

<div class="feature-card">

### 🎭 [Jake Sully](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/jake-sully.yaml)

**Sci-Fi Protagonist**

Avatar's protagonist showing how to represent characters with body-swapping abilities and environmental themes.

**Tags:** `human`, `avatar`, `sci-fi`, `environmental`, `hero`

[View Example →](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/jake-sully.yaml)

</div>

</div>

## Character Templates

### Minimal Character Template

Perfect for getting started:

```yaml title="minimal-template.yaml"
ocd_version: "0.0.1"
id: "char-template-minimal"
names:
  canon: "Template Character"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

### Complete Character Template

Full-featured template with all major blocks:

```yaml title="complete-template.yaml"
ocd_version: "0.0.1"
id: "char-template-complete"
names:
  canon: "Complete Character"
  aliases: ["Template", "Example"]
locale: "en-US"
media_targets: ["game", "novel"]

identity:
  kind: "humanoid"
  species: "Human"
  age: "25 years"
  pronouns: ["they/them"]
  locale: "Fantasy World"

appearance:
  body_type: "athletic"
  height: "5'8\""
  distinguishing_features: ["bright eyes", "confident posture"]
  physical_summary: "A determined individual with an adventurous spirit."

personality:
  summary: "Brave, curious, and always ready for adventure."
  traits:
    - name: "introversion-extraversion"
      kind: "bipolar"
      polarity: 0.5
      intensity: 0.7
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.6
  goals:
    short_term: ["Complete the quest"]
    long_term: ["Become a legend"]
  values: ["courage", "friendship", "justice"]

background:
  summary: "A hero's journey begins with a single step."
  timeline:
    - at: "childhood"
      event: "Born in a small village"
    - at: "present"
      event: "Ready for adventure"

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

behavior_directives:
  portrayal_tips: ["Play as confident but not arrogant"]
  dialogue_style:
    register: "heroic"
    pace: "decisive"
    vocabulary: ["by my honor", "let's do this"]

meta:
  tags: ["adventurer", "hero", "fantasy", "template"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Genre Examples

### Fantasy Characters

#### The Noble Paladin
```yaml title="paladin-example.yaml"
ocd_version: "0.0.1"
id: "char-paladin-example"
names:
  canon: "Sir Galahad"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  traits:
    - name: "selfish-selfless"
      kind: "bipolar"
      polarity: 0.9
      intensity: 0.9
    - name: "holy-power"
      kind: "scalar"
      value: 0.8
  values: ["honor", "justice", "protection"]
x-dnd5e:
  class: "Paladin"
  alignment: "Lawful Good"
  level: 10
```

#### The Mysterious Wizard
```yaml title="wizard-example.yaml"
ocd_version: "0.0.1"
id: "char-wizard-example"
names:
  canon: "Gandalf"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  traits:
    - name: "intuition-logic"
      kind: "bipolar"
      polarity: 0.7
      intensity: 0.8
    - name: "arcane-knowledge"
      kind: "scalar"
      value: 0.9
  quirks: ["speaks in riddles", "knows more than he reveals"]
x-dnd5e:
  class: "Wizard"
  subclass: "School of Divination"
  level: 15
```

### Sci-Fi Characters

#### The Space Marine
```yaml title="marine-example.yaml"
ocd_version: "0.0.1"
id: "char-marine-example"
names:
  canon: "Sergeant Johnson"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  traits:
    - name: "serious-playful"
      kind: "bipolar"
      polarity: -0.3
      intensity: 0.8
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.9
  instincts:
    - trigger: "Enemy detected"
      response: "Engage with overwhelming force"
x-sci-fi:
  system: "Space Marines"
  rank: "Sergeant"
  specialization: "Heavy Weapons"
```

#### The AI Companion
```yaml title="ai-example.yaml"
ocd_version: "0.0.1"
id: "char-ai-example"
names:
  canon: "Cortana"
identity:
  kind: "construct"
  species: "AI"
personality:
  traits:
    - name: "logic-emotion"
      kind: "bipolar"
      polarity: 0.6
      intensity: 0.7
    - name: "processing-power"
      kind: "scalar"
      value: 0.95
  quirks: ["calculates probabilities out loud", "shows concern for human welfare"]
x-sci-fi:
  system: "Halo"
  ai_type: "Smart AI"
  function: "Combat Support"
```

### Modern Characters

#### The Detective
```yaml title="detective-example.yaml"
ocd_version: "0.0.1"
id: "char-detective-example"
names:
  canon: "Detective Sarah Chen"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  traits:
    - name: "intuition-logic"
      kind: "bipolar"
      polarity: 0.4
      intensity: 0.8
    - name: "investigation"
      kind: "scalar"
      value: 0.9
  instincts:
    - trigger: "Crime scene discovered"
      response: "Systematically examine evidence"
x-modern:
  system: "Police Procedural"
  rank: "Detective"
  specialization: "Homicide"
```

#### The Superhero
```yaml title="superhero-example.yaml"
ocd_version: "0.0.1"
id: "char-superhero-example"
names:
  canon: "Captain Justice"
identity:
  kind: "humanoid"
  species: "Human"
personality:
  traits:
    - name: "selfish-selfless"
      kind: "bipolar"
      polarity: 0.8
      intensity: 0.9
    - name: "heroic-will"
      kind: "scalar"
      value: 0.9
  powers:
    - "Super strength"
    - "Flight"
    - "Energy projection"
x-superhero:
  system: "Marvel/DC Style"
  origin: "Accident"
  powers: ["Super Strength", "Flight", "Energy Blasts"]
```

## System Integration Examples

### D&D 5e Integration

See [Bruenor Battlehammer](https://github.com/Open-Character-Design/OCD-Specification/blob/main/examples/bruenor.yaml) for a complete D&D 5e character with:

- Complete ability scores and modifiers
- Spellcasting with known spells and slots
- Equipment and weapons
- Class features and racial traits
- Combat statistics

### Custom System Integration

Example of a custom game system extension:

```yaml title="custom-system-example.yaml"
ocd_version: "0.0.1"
id: "char-custom-example"
names:
  canon: "Custom Hero"
# ... standard OCD fields ...

x-my-fantasy-rpg:
  system: "MyFantasyRPG"
  version: "2.1"
  character_type: "Mage"
  power_level: "Heroic"
  abilities:
    - name: "Fireball"
      level: 3
      cost: 5
    - name: "Heal"
      level: 2
      cost: 3
  stats:
    magic: 18
    health: 45
    mana: 60
  equipment:
    weapon: "Staff of Power"
    armor: "Robe of Protection"
```

## Complex Character Examples

### The Shapeshifter

Demonstrates composite identity and complex relationships:

```yaml title="shapeshifter-example.yaml"
ocd_version: "0.0.1"
id: "char-shapeshifter-example"
names:
  canon: "Mystique"
identity:
  kind: "humanoid"
  species: "Mutant"
  composite_of:
    - identity: "char-mystique-base"
      control_share: 0.8
      exposure: "primary"
    - identity: "char-shapeshifted-form"
      control_share: 0.2
      exposure: "secondary"
personality:
  traits:
    - name: "honest-deceptive"
      kind: "bipolar"
      polarity: -0.7
      intensity: 0.8
    - name: "shapeshifting"
      kind: "flag"
      value: true
capabilities:
  powers:
    - "Perfect mimicry"
    - "Voice imitation"
    - "Form memory"
```

### The Hivemind

Shows how to represent collective consciousness:

```yaml title="hivemind-example.yaml"
ocd_version: "0.0.1"
id: "char-hivemind-example"
names:
  canon: "The Collective"
identity:
  kind: "construct"
  species: "Hivemind"
  composite_of:
    - identity: "char-drone-001"
      control_share: 0.3
    - identity: "char-drone-002"
      control_share: 0.3
    - identity: "char-drone-003"
      control_share: 0.4
personality:
  traits:
    - name: "individual-collective"
      kind: "bipolar"
      polarity: 0.9
      intensity: 0.9
    - name: "hive-intelligence"
      kind: "scalar"
      value: 0.95
capabilities:
  powers:
    - "Shared consciousness"
    - "Distributed processing"
    - "Collective memory"
```

## Validation Examples

### Valid Character
```yaml title="valid-example.yaml"
ocd_version: "0.0.1"
id: "char-valid-example"
names:
  canon: "Valid Character"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

**Validation Result:**
```
✅ Validation successful
📝 0 warnings
```

### Character with Warnings
```yaml title="warning-example.yaml"
ocd_version: "0.0.1"
id: "char_warning_example"  # Underscores will be normalized
names:
  canon: "Warning Character"
identity:
  kind: "humanoid"
  species: "Human"
meta:
  tags: ["ADVENTURER", "Hero", "adventurer"]  # Will be normalized
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

**Validation Result:**
```
✅ Validation successful
⚠️ 2 warnings:
  - NORMALIZED_SLUG: Slug 'char_warning_example' normalized to 'char-warning-example'
  - NORMALIZED_TAGS: Tags normalized to lowercase and deduplicated
```

### Invalid Character
```yaml title="invalid-example.yaml"
# Missing required fields
names:
  canon: "Invalid Character"
identity:
  kind: "invalid-kind"  # Not a valid identity kind
```

**Validation Result:**
```
❌ Validation failed
🚨 2 errors:
  - Missing required field: ocd_version
  - Invalid identity kind: 'invalid-kind'
```

## Download Examples

All examples are available in the [examples directory](https://github.com/Open-Character-Design/OCD-Specification/tree/main/examples) of the OCD repository.

### Quick Download
```bash
# Download all examples
git clone https://github.com/Open-Character-Design/OCD-Specification.git
cd OpenCharacter-Specification/examples

# Validate all examples
find . -name "*.yaml" -exec ocd-validate {} \;
```

### Individual Downloads
- [Bruenor Battlehammer](https://raw.githubusercontent.com/Open-Character-Design/OpenCharacter-Specification/main/examples/bruenor.yaml)
- [Commander Shepard](https://raw.githubusercontent.com/Open-Character-Design/OpenCharacter-Specification/main/examples/commander-shepard.yaml)
- [Crash Bandicoot](https://raw.githubusercontent.com/Open-Character-Design/OpenCharacter-Specification/main/examples/crash-bandicoot.yaml)
- [Eve](https://raw.githubusercontent.com/Open-Character-Design/OpenCharacter-Specification/main/examples/eve.yaml)

## Contributing Examples

We welcome community contributions! To add your character example:

1. **Follow the format** of existing examples
2. **Include comprehensive metadata** (tags, authorship, etc.)
3. **Validate your character** before submitting
4. **Document any custom extensions** you use
5. **Submit a pull request** with your example

### Example Guidelines

- **Complete characters**: Include all relevant blocks
- **Clear documentation**: Add comments explaining unique features
- **Proper validation**: Ensure your character passes validation
- **Diverse representation**: Show different genres, systems, and complexity levels

## What's Next?

- **[Tutorial](../tutorial/index.md)**: Learn to create characters step by step
- **[Writing Guide](writing-ocd-files.md)**: Best practices for authoring
- **[Specification](../spec/schema-overview.md)**: Technical details
- **[Integration](../integration/python-validator.md)**: Use OCD in your applications