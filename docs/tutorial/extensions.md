# Step 4: System Extensions

In this step, you'll learn how to integrate OCD with specific game systems using extension blocks.

## What You'll Build

A character with D&D 5e stats, abilities, and equipment using the `x-dnd5e` extension block.

## Understanding Extensions

OCD uses `x-*` namespaces to add system-specific data without cluttering the core specification. This allows you to:

- Keep the core OCD portable across systems
- Add detailed game mechanics when needed
- Maintain compatibility with different platforms

## Adding D&D 5e Integration

Let's enhance Rita with D&D 5e stats:

```yaml title="rita-dnd5e.yaml"
ocd_version: "0.0.1"
id: "char-rita-adventurer"
names:
  canon: "Rita"
  aliases: ["Rita the Brave", "Adventurer Rita"]
locale: "en-US"
media_targets: ["game", "novel"]

identity:
  kind: "humanoid"
  species: "Human"
  age: "25 years"
  pronouns: ["she/her"]
  locale: "Fantasy Kingdom"

appearance:
  body_type: "athletic build"
  height: "5'6\""
  distinguishing_features: ["bright green eyes", "auburn hair"]
  physical_summary: "A determined young woman with an adventurous spirit."

personality:
  summary: "Brave, curious, and always ready for adventure."
  traits:
    - name: "introversion-extraversion"
      kind: "bipolar"
      polarity: 0.7
      intensity: 0.8
    - name: "competitive-cooperative"
      kind: "bipolar"
      polarity: 0.6
      intensity: 0.7
    - name: "serious-playful"
      kind: "bipolar"
      polarity: 0.3
      intensity: 0.6
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.7
    - name: "empathy"
      kind: "scalar"
      value: 0.8
    - name: "leadership"
      kind: "scalar"
      value: 0.6
    - name: "magic-sensitive"
      kind: "flag"
      value: true
    - name: "fearless"
      kind: "flag"
      value: true
  instincts:
    - trigger: "Friend in danger"
      response: "Immediately rush to help, regardless of personal risk"
    - trigger: "Mysterious door or passage"
      response: "Investigate with curiosity, but check for traps first"
    - trigger: "Injustice or unfairness"
      response: "Speak up and take action to correct it"
  goals:
    short_term: ["Find the lost artifact", "Protect the village"]
    long_term: ["Become a legendary adventurer", "Discover her true heritage"]
  values: ["courage", "friendship", "justice", "discovery"]

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
    - at: "age 24"
      event: "Met her adventuring companions during the Goblin War"
    - at: "present"
      event: "Currently searching for the Lost Crown of Eldoria"
  affiliations:
    - name: "Mage's Guild"
      role: "member"
      status: "active"
    - name: "Greenbrook Village"
      role: "native"
      status: "honorary citizen"
    - name: "Adventurer's Company"
      role: "leader"
      status: "active"
  relationships:
    - target_ref: "char-marcus-blacksmith"
      role: "father"
      sentiment: 0.9
      notes: "Proud but worried about her dangerous lifestyle"
    - target_ref: "char-elena-healer"
      role: "mother"
      sentiment: 0.95
      notes: "Supports her dreams but wishes she'd visit more often"
    - target_ref: "char-gareth-warrior"
      role: "adventuring companion"
      sentiment: 0.8
      notes: "Trusted ally and close friend"
    - target_ref: "char-malachi-wizard"
      role: "mentor"
      sentiment: 0.7
      notes: "Former teacher, now occasional advisor"
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

# D&D 5e Extension Block
x-dnd5e:
  edition: "5e"
  alignment: "Chaotic Good"
  race: "Human"
  class: "Wizard"
  subclass: "School of Evocation"
  level: 8
  background: "Sage"
  proficiency_bonus: 3
  
  ability_scores:
    STR: 12  # +1
    DEX: 14  # +2
    CON: 16  # +3
    INT: 18  # +4
    WIS: 13  # +1
    CHA: 15  # +2
  
  saving_throws:
    proficient: ["INT", "WIS"]
    bonuses: {}
  
  combat_block:
    armor_class: 12  # Mage Armor + Dex
    initiative: "+2"
    speed: "30 ft"
    hit_dice: "8d6"
    hit_points: 52  # 8d6 + 24 (CON mod)
    senses: ["passive Perception 11"]
    resistances: []
    conditions_immunities: []
    damage_immunities: []
  
  languages: ["Common", "Draconic", "Elvish", "Celestial"]
  
  skills:
    proficient: ["Arcana", "History", "Investigation", "Insight"]
    expertise: []
    notes: "Arcana expertise from Sage background"
  
  tools:
    proficient: ["Alchemist's supplies", "Calligrapher's supplies"]
  
  features_traits:
    racial:
      - "Human: +1 to all ability scores"
      - "Human: Extra language"
      - "Human: Extra skill proficiency"
    class:
      - "Spellcasting (Wizard)"
      - "Arcane Recovery"
      - "Evocation Savant"
      - "Sculpt Spells"
      - "Potent Cantrip"
    background:
      - "Researcher"
      - "Sage: Library Access"
    feats:
      - "War Caster"
      - "Resilient (Constitution)"
  
  spellcasting:
    caster_type: "full"
    spell_ability: "INT"
    spell_save_dc: 15  # 8 + 3 (prof) + 4 (INT)
    spell_attack_bonus: "+7"
    slots:
      "1st": 4
      "2nd": 3
      "3rd": 3
      "4th": 2
    known_spells:
      cantrips: ["Fire Bolt", "Mage Hand", "Prestidigitation", "Shocking Grasp"]
      "1st": ["Mage Armor", "Magic Missile", "Shield", "Detect Magic"]
      "2nd": ["Misty Step", "Scorching Ray", "Suggestion"]
      "3rd": ["Fireball", "Counterspell", "Fly"]
      "4th": ["Polymorph", "Wall of Fire"]
  
  equipment:
    armor: ["Mage Armor (spell)"]
    weapons: ["Quarterstaff", "Dagger"]
    tools: ["Alchemist's supplies", "Calligrapher's supplies"]
    other: 
      - "Spellbook"
      - "Component pouch"
      - "Scholar's pack"
      - "Bottle of black ink"
      - "Quill"
      - "Small knife"
      - "Letter from colleague"
      - "Common clothes"
      - "Pouch with 10 gp"
  
  resources_tracking:
    short_rest:
      arcane_recovery: "1/short rest"
    long_rest:
      spell_slots: "regain all"
      arcane_recovery: "regain use"
  
  notes:
    rulings:
      - "Evocation Savant: Half time and cost to copy evocation spells"
      - "Sculpt Spells: Allies automatically succeed on saves vs evocation spells"
      - "War Caster: Advantage on concentration saves, can cast spells as opportunity attacks"
    provenance: "Standard point buy with racial bonuses, optimized for spellcasting"

meta:
  tags: ["adventurer", "hero", "fantasy", "mage", "leader", "dnd5e"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Understanding Extension Blocks

### Extension Namespace
The `x-dnd5e` block contains all D&D 5e specific data:

```yaml
x-dnd5e:
  edition: "5e"
  alignment: "Chaotic Good"
  race: "Human"
  class: "Wizard"
  # ... more D&D data
```

!!! tip "Extension Naming"
    Always use `x-` prefix for extensions. This keeps system-specific data separate from the core OCD specification.

### Core D&D Fields

**Basic Information:**
- `edition`: D&D edition (usually "5e")
- `alignment`: Character alignment
- `race`: Character race
- `class`: Primary class
- `subclass`: Class archetype
- `level`: Character level
- `background`: Background type

**Ability Scores:**
```yaml
ability_scores:
  STR: 12  # +1
  DEX: 14  # +2
  CON: 16  # +3
  INT: 18  # +4
  WIS: 13  # +1
  CHA: 15  # +2
```

**Combat Information:**
```yaml
combat_block:
  armor_class: 12
  initiative: "+2"
  speed: "30 ft"
  hit_dice: "8d6"
  hit_points: 52
```

### Spellcasting

For spellcasting classes, include detailed spell information:

```yaml
spellcasting:
  caster_type: "full"  # full, half, third, or none
  spell_ability: "INT"
  spell_save_dc: 15
  spell_attack_bonus: "+7"
  slots:
    "1st": 4
    "2nd": 3
    "3rd": 3
    "4th": 2
  known_spells:
    cantrips: ["Fire Bolt", "Mage Hand", "Prestidigitation"]
    "1st": ["Mage Armor", "Magic Missile", "Shield"]
    "2nd": ["Misty Step", "Scorching Ray"]
```

## Other System Extensions

### Pathfinder 2e
```yaml
x-pf2e:
  edition: "2e"
  ancestry: "Human"
  heritage: "Versatile"
  background: "Scholar"
  class: "Wizard"
  level: 8
  # ... Pathfinder specific data
```

### Custom Game System
```yaml
x-my-game:
  system: "MyFantasyRPG"
  version: "2.1"
  character_type: "Mage"
  power_level: "Heroic"
  # ... custom system data
```

## Validation with Extensions

The OCD validator will validate the core fields but won't validate extension blocks (since they're system-specific):

```bash
ocd-validate rita-dnd5e.yaml
```

You should see successful validation of the core OCD fields. Extension blocks are preserved but not validated by the OCD validator.

!!! note "Extension Validation"
    Extension blocks are not validated by OCD validators. Each game system would need its own validator to check extension data.

## Best Practices for Extensions

### Keep Core Data Separate
```yaml
# Core OCD data
personality:
  traits:
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.7

# System-specific data
x-dnd5e:
  combat_block:
    armor_class: 12
    hit_points: 52
```

### Use Consistent Naming
```yaml
x-dnd5e:  # Good - clear system identifier
x-my-rpg: # Good - descriptive name
x-game:   # Avoid - too generic
```

### Document Extension Schemas
If you create custom extensions, document their structure:

```yaml
x-my-game:
  # Custom extension for MyFantasyRPG
  # Fields:
  #   - system: Game system name
  #   - version: System version
  #   - character_type: Character archetype
  #   - power_level: Character power tier
  system: "MyFantasyRPG"
  version: "2.1"
  character_type: "Mage"
  power_level: "Heroic"
```

## Common Extension Patterns

### Martial Character
```yaml
x-dnd5e:
  class: "Fighter"
  subclass: "Battle Master"
  level: 8
  ability_scores:
    STR: 18
    DEX: 14
    CON: 16
    INT: 10
    WIS: 12
    CHA: 13
  combat_block:
    armor_class: 18  # Plate armor
    hit_points: 80
```

### Skill-Based Character
```yaml
x-dnd5e:
  class: "Rogue"
  subclass: "Arcane Trickster"
  level: 8
  skills:
    proficient: ["Stealth", "Sleight of Hand", "Investigation", "Perception"]
    expertise: ["Stealth", "Sleight of Hand"]
```

### Support Character
```yaml
x-dnd5e:
  class: "Cleric"
  subclass: "Life Domain"
  level: 8
  spellcasting:
    caster_type: "full"
    spell_ability: "WIS"
    known_spells:
      "1st": ["Cure Wounds", "Bless", "Healing Word"]
      "2nd": ["Lesser Restoration", "Spiritual Weapon"]
```

## What's Next?

Perfect! You've integrated Rita with D&D 5e using extension blocks. In the final step, you'll learn best practices for production deployment and validation workflows.

**Next:** [Step 5: Production Tips](production.md)

## Quick Reference

### Extension Structure
- Use `x-` prefix for all extensions
- Keep core OCD data separate from system data
- Document custom extension schemas

### Common Extensions
- `x-dnd5e`: D&D 5th Edition
- `x-pf2e`: Pathfinder 2nd Edition
- `x-coc`: Call of Cthulhu
- `x-savage`: Savage Worlds

### D&D 5e Key Fields
- `edition`, `alignment`, `race`, `class`, `level`
- `ability_scores`, `combat_block`, `spellcasting`
- `equipment`, `features_traits`, `skills`
