# Step 2: Adding Personality

In this step, you'll learn about OCD's powerful trait model and add personality traits to your character.

## What You'll Build

A character with detailed personality traits using bipolar axes, scalar values, and behavioral patterns.

## Understanding the Trait Model

OCD supports three types of traits:

### Bipolar Traits
Traits that exist on a spectrum between two opposites, like `introversion-extraversion`.

### Scalar Traits
Single-dimension traits measured from 0 to 1, like `combat-readiness` or `empathy`.

### Flag Traits
Binary on/off traits, like `psionic` or `licensed-medic`.

## Adding Personality Traits

Let's enhance Rita with personality traits:

```yaml title="rita-personality.yaml"
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
    # Bipolar traits - Rita leans toward extraversion and cooperation
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
    
    # Scalar traits - Rita's abilities and tendencies
    - name: "combat-readiness"
      kind: "scalar"
      value: 0.7
    - name: "empathy"
      kind: "scalar"
      value: 0.8
    - name: "leadership"
      kind: "scalar"
      value: 0.6
    
    # Flag traits - Rita's special capabilities
    - name: "magic-sensitive"
      kind: "flag"
      value: true
    - name: "fearless"
      kind: "flag"
      value: true

  # Behavioral patterns and instincts
  instincts:
    - trigger: "Friend in danger"
      response: "Immediately rush to help, regardless of personal risk"
    - trigger: "Mysterious door or passage"
      response: "Investigate with curiosity, but check for traps first"
    - trigger: "Injustice or unfairness"
      response: "Speak up and take action to correct it"

  # Goals and motivations
  goals:
    short_term: ["Find the lost artifact", "Protect the village"]
    long_term: ["Become a legendary adventurer", "Discover her true heritage"]

  # Core values
  values: ["courage", "friendship", "justice", "discovery"]

meta:
  tags: ["adventurer", "hero", "fantasy"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
```

## Understanding Trait Values

### Bipolar Traits

Bipolar traits use two values:

- **`polarity`**: Range from -1 to 1
  - `-1` = strongly toward first term (introversion)
  - `0` = balanced between both
  - `1` = strongly toward second term (extraversion)
- **`intensity`**: Range from 0 to 1
  - `0` = trait has no influence
  - `1` = trait is very prominent

!!! tip "Reading Bipolar Traits"
    Rita's `introversion-extraversion: polarity 0.7, intensity 0.8` means she's quite extraverted (0.7 toward extraversion) and this trait is very prominent in her personality (0.8 intensity).

### Scalar Traits

Scalar traits use a single value from 0 to 1:

- **`value`**: Range from 0 to 1
  - `0` = no ability/tendency
  - `1` = maximum ability/tendency

### Flag Traits

Flag traits are simple boolean values:

- **`value`**: `true` or `false`

## Validation and Normalization

Run the validator on your enhanced character:

```bash
ocd-validate rita-personality.yaml
```

The validator will normalize trait names and values. For example:

- Bipolar trait separators are normalized to `-`
- Trait names are converted to lowercase
- Values are validated to be within correct ranges

## Common Trait Patterns

### The Hero Pattern

```yaml
traits:
  - name: "selfish-selfless"
    kind: "bipolar"
    polarity: 0.8
    intensity: 0.9
  - name: "cowardly-brave"
    kind: "bipolar"
    polarity: 0.9
    intensity: 0.8
  - name: "combat-readiness"
    kind: "scalar"
    value: 0.8
```

### The Scholar Pattern

```yaml
traits:
  - name: "intuition-logic"
    kind: "bipolar"
    polarity: 0.7
    intensity: 0.8
  - name: "knowledge"
    kind: "scalar"
    value: 0.9
  - name: "patience"
    kind: "scalar"
    value: 0.8
```

### The Trickster Pattern

```yaml
traits:
  - name: "serious-playful"
    kind: "bipolar"
    polarity: 0.8
    intensity: 0.9
  - name: "honest-deceptive"
    kind: "bipolar"
    polarity: -0.6
    intensity: 0.7
  - name: "charisma"
    kind: "scalar"
    value: 0.8
```

## Instincts and Behavioral Patterns

Instincts define how your character reacts to specific situations:

```yaml
instincts:
  - trigger: "Someone tells a joke"
    response: "Laugh genuinely and try to tell a better one"
  - trigger: "Conflict arises"
    response: "Try to mediate and find a peaceful solution"
  - trigger: "Danger approaches"
    response: "Assess the situation quickly and act decisively"
```

!!! note "Instincts vs Traits"
    Traits define *what* your character is like, while instincts define *how* they react to specific situations. Both work together to create consistent character behavior.

## Goals and Values

### Goals
Define what your character wants to achieve:

```yaml
goals:
  short_term: ["Complete the quest", "Learn new magic"]
  long_term: ["Save the kingdom", "Master all elements"]
```

### Values
Core principles that guide your character's decisions:

```yaml
values: ["honor", "family", "justice", "freedom"]
```

## Validation Tips

### Common Validation Errors

**Invalid polarity range:**
```yaml
- name: "introversion-extraversion"
  polarity: 1.5  # Error: must be between -1 and 1
```

**Invalid intensity range:**
```yaml
- name: "introversion-extraversion"
  intensity: 2.0  # Error: must be between 0 and 1
```

**Missing trait kind:**
```yaml
- name: "combat-readiness"
  value: 0.7  # Error: missing 'kind' field
```

## What's Next?

Great! You've added personality traits to Rita. In the next step, you'll learn about background information, relationships, and how characters connect to each other.

**Next:** [Step 3: Background & Relationships](background.md)

## Quick Reference

### Trait Types
- **Bipolar**: `polarity: [-1..1]`, `intensity: [0..1]`
- **Scalar**: `value: [0..1]`
- **Flag**: `value: true/false`

### Common Bipolar Axes
- `introversion-extraversion`
- `competitive-cooperative`
- `serious-playful`
- `selfish-selfless`
- `cowardly-brave`
- `intuition-logic`
- `honest-deceptive`

### Common Scalar Traits
- `combat-readiness`
- `empathy`
- `leadership`
- `knowledge`
- `charisma`
- `patience`
- `creativity`
