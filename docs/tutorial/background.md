# Step 3: Background & Relationships

In this step, you'll add rich background information and relationships to create a more complete character.

## What You'll Build

A character with detailed background, timeline events, affiliations, and relationships to other characters.

## Adding Background Information

Let's enhance Rita with background details:

```yaml title="rita-background.yaml"
ocd_version: "1.0.0"
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

# New background section
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

meta:
  tags: ["adventurer", "hero", "fantasy", "mage", "leader"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Understanding Background Components

### Summary
A brief overview of the character's background story.

### Timeline
Key events in the character's life, organized chronologically:

```yaml
timeline:
  - at: "age 12"
    event: "First magical incident - accidentally enchanted a horseshoe"
  - at: "age 18"
    event: "Left home to seek training with the Mage's Guild"
```

!!! tip "Timeline Tips"
    Use descriptive time markers like "childhood", "age 12", "present", or specific dates. This helps AI systems understand character development over time.

### Affiliations
Organizations, groups, or institutions the character belongs to:

```yaml
affiliations:
  - name: "Mage's Guild"
    role: "member"
    status: "active"
```

### Relationships
Connections to other characters with sentiment scores:

```yaml
relationships:
  - target_ref: "char-marcus-blacksmith"
    role: "father"
    sentiment: 0.9
    notes: "Proud but worried about her dangerous lifestyle"
```

#### Understanding Sentiment Scores
- **`1.0`**: Deep love, absolute trust
- **`0.5`**: Positive relationship, friendship
- **`0.0`**: Neutral, indifferent
- **`-0.5`**: Negative relationship, dislike
- **`-1.0`**: Hatred, mortal enemies

#### Target References
The `target_ref` field should reference other character IDs. The validator will check if these references exist and warn about unresolved references.

### Narrative Hooks
Elements that can drive story development:

```yaml
narrative_hooks:
  themes: ["discovery", "family", "magic", "heroism"]
  potential_arcs: 
    - "Reveal of true magical heritage"
    - "Reunion with long-lost family"
  narrative_role: "protagonist"
```

## Creating Related Characters

To make relationships work properly, you need to create the referenced characters. Here's Marcus, Rita's father:

```yaml title="marcus-blacksmith.yaml"
ocd_version: "1.0.0"
id: "char-marcus-blacksmith"
names:
  canon: "Marcus Ironforge"
  aliases: ["Marcus", "Master Ironforge"]
locale: "en-US"

identity:
  kind: "humanoid"
  species: "Human"
  age: "52 years"
  pronouns: ["he/him"]
  locale: "Greenbrook Village"

appearance:
  body_type: "stocky, muscular"
  height: "5'10\""
  distinguishing_features: ["calloused hands", "graying beard", "kind eyes"]
  physical_summary: "A sturdy blacksmith with kind eyes and strong hands."

personality:
  summary: "Hardworking, protective father who worries about his adventurous daughter."
  traits:
    - name: "introversion-extraversion"
      kind: "bipolar"
      polarity: -0.3
      intensity: 0.6
    - name: "competitive-cooperative"
      kind: "bipolar"
      polarity: 0.8
      intensity: 0.7
    - name: "serious-playful"
      kind: "bipolar"
      polarity: -0.2
      intensity: 0.5
    - name: "craftsmanship"
      kind: "scalar"
      value: 0.9
    - name: "patience"
      kind: "scalar"
      value: 0.8

background:
  summary: "Village blacksmith who raised Rita after her magical abilities emerged."
  timeline:
    - at: "youth"
      event: "Apprenticed to his father as a blacksmith"
    - at: "age 25"
      event: "Married Elena, the village healer"
    - at: "age 27"
      event: "Rita was born"
    - at: "age 39"
      event: "Rita's first magical incident - helped her understand her gift"
    - at: "age 45"
      event: "Rita left for Mage's Guild - proud but worried"
    - at: "present"
      event: "Continues blacksmithing, awaits Rita's visits"

  relationships:
    - target_ref: "char-rita-adventurer"
      role: "daughter"
      sentiment: 0.9
      notes: "Proud of her achievements but worried about her safety"
    - target_ref: "char-elena-healer"
      role: "wife"
      sentiment: 0.95
      notes: "Deeply loving marriage"

meta:
  tags: ["blacksmith", "father", "villager", "craftsman"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Validation and Reference Resolution

When you validate Rita's character, the validator will check if the referenced characters exist:

```bash
ocd-validate rita-background.yaml
```

If Marcus's file is in the same directory or accessible, the validator will confirm the relationship references are valid.

!!! warning "Unresolved References"
    If a `target_ref` points to a character that doesn't exist, you'll get an `UNRESOLVED_REF` warning. This helps ensure your character relationships are properly defined.

## Common Background Patterns

### The Orphan Hero
```yaml
background:
  summary: "Orphaned at a young age, raised by mentors, seeks to discover their true heritage."
  timeline:
    - at: "age 5"
      event: "Parents killed in mysterious circumstances"
    - at: "age 6"
      event: "Taken in by wise mentor"
    - at: "present"
      event: "Questing to discover the truth about parents"
```

### The Reluctant Hero
```yaml
background:
  summary: "Ordinary person thrust into extraordinary circumstances."
  timeline:
    - at: "youth"
      event: "Normal, peaceful life"
    - at: "age 20"
      event: "Chosen by ancient artifact"
    - at: "present"
      event: "Learning to accept heroic destiny"
```

### The Reformed Villain
```yaml
background:
  summary: "Former villain seeking redemption through heroic deeds."
  timeline:
    - at: "youth"
      event: "Corrupted by dark forces"
    - at: "age 25"
      event: "Realized the error of their ways"
    - at: "present"
      event: "Seeking redemption through good deeds"
```

## Relationship Dynamics

### Family Relationships
```yaml
relationships:
  - target_ref: "char-parent"
    role: "father"
    sentiment: 0.8
  - target_ref: "char-sibling"
    role: "brother"
    sentiment: 0.6
```

### Romantic Relationships
```yaml
relationships:
  - target_ref: "char-love-interest"
    role: "romantic partner"
    sentiment: 0.9
    notes: "Deeply in love, planning future together"
```

### Professional Relationships
```yaml
relationships:
  - target_ref: "char-mentor"
    role: "teacher"
    sentiment: 0.7
  - target_ref: "char-rival"
    role: "professional rival"
    sentiment: -0.3
```

### Antagonistic Relationships
```yaml
relationships:
  - target_ref: "char-villain"
    role: "nemesis"
    sentiment: -0.9
    notes: "Mortal enemies, destined to clash"
```

## What's Next?

Excellent! You've added rich background and relationships to Rita. In the next step, you'll learn how to integrate OCD with specific game systems using extension blocks.

**Next:** [Step 4: System Extensions](extensions.md)

## Quick Reference

### Background Structure
- **`summary`**: Brief background overview
- **`timeline`**: Chronological events
- **`affiliations`**: Groups and organizations
- **`relationships`**: Character connections
- **`narrative_hooks`**: Story elements

### Relationship Fields
- **`target_ref`**: ID of related character
- **`role`**: Relationship type
- **`sentiment`**: Emotional connection (-1 to 1)
- **`notes`**: Additional context

### Common Roles
- Family: `father`, `mother`, `brother`, `sister`, `child`
- Romantic: `romantic partner`, `spouse`, `lover`
- Professional: `mentor`, `student`, `colleague`, `rival`
- Social: `friend`, `ally`, `enemy`, `nemesis`
