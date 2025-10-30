# Step 5: Production Tips

In this final step, you'll learn best practices for production deployment, validation workflows, and maintaining OCD characters.

!!! tip "Production Case Studies"
    For real-world examples of OCD implementation in production environments, see our [Case Studies](../deep-dives/case-studies/index.md) section, including detailed accounts of game studio integrations and enterprise deployments.

!!! tip "AI Agent Production Configuration"
    For AI-powered characters, use OCD's `ai_agent` fields to configure production-ready AI behavior. This includes safety settings, memory configuration, and multi-agent orchestration. See our [AI Agent Fields Research](../deep-dives/research/ai-agent-fields-research.md) for comprehensive guidance on AI agent configuration best practices.

## What You'll Learn

- Production-ready character structure
- Validation workflows and CI/CD integration
- Normalization best practices
- Deployment strategies
- Maintenance and updates

## Production-Ready Character

Let's create a final, production-ready version of Rita:

```yaml title="rita-production.yaml"
ocd_version: "1.0.0"
id: "char-rita-adventurer"
names:
  canon: "Rita"
  aliases: ["Rita the Brave", "Adventurer Rita", "The Green-Eyed Mage"]
  display:
    en-US: "Rita"
    es-ES: "Alicia"
    fr-FR: "Rita"
locale: "en-US"
media_targets: ["game", "novel", "ai-platform"]

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

appearance:
  body_type: "athletic build"
  height: "5'6\""
  weight: "140 lbs"
  distinguishing_features: ["bright green eyes", "auburn hair", "small scar on left hand"]
  physical_summary: "A determined young woman with an adventurous spirit and kind eyes."
  metaphysicality:
    aura: "warm, magical energy"
    energy_type: "arcane magic"
    plane_of_origin: "Material Plane"
    traits: ["magic-sensitive", "blessed by fate"]

personality:
  summary: "Brave, curious, and always ready for adventure. A natural leader who puts others before herself."
  archetype: "heroic mage / reluctant leader"
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
    - name: "selfish-selfless"
      kind: "bipolar"
      polarity: 0.8
      intensity: 0.9
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
  quirks: ["taps fingers when thinking", "always checks for traps", "collects interesting rocks"]
  humor_styles: ["dry wit", "self-deprecating", "encouraging"]
  instincts:
    - trigger: "Friend in danger"
      response: "Immediately rush to help, regardless of personal risk"
    - trigger: "Mysterious door or passage"
      response: "Investigate with curiosity, but check for traps first"
    - trigger: "Injustice or unfairness"
      response: "Speak up and take action to correct it"
    - trigger: "Group needs direction"
      response: "Step up and take charge, even if reluctantly"
  goals:
    short_term: ["Find the lost artifact", "Protect the village", "Master new spells"]
    long_term: ["Become a legendary adventurer", "Discover her true heritage", "Establish a magical academy"]
  values: ["courage", "friendship", "justice", "discovery", "protection"]
  conflicts:
    internal: "Balancing personal safety with duty to help others"
    external: "Ancient evil threatening the kingdom"

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
    themes: ["discovery", "family", "magic", "heroism", "leadership"]
    potential_arcs: 
      - "Reveal of true magical heritage"
      - "Reunion with long-lost family"
      - "Final confrontation with Dark Lord Shadow"
      - "Establishment of magical academy"
    narrative_role: "protagonist"

capabilities:
  skills:
    - name: "Arcane Magic"
      level: 4
      tags: ["spellcasting", "evocation"]
    - name: "Leadership"
      level: 3
      tags: ["social", "tactics"]
    - name: "Investigation"
      level: 3
      tags: ["research", "analysis"]
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

interaction_layer:
  preferred_modes: ["speech", "magic", "leadership"]
  consent_model:
    allows: ["heroic violence", "magical effects", "emotional support"]
    restricts: ["romantic intimacy", "excessive gore"]
  narrator_notes: "Rita is the heart of the party - brave, caring, and magical. She leads through example and protects those she loves."

state_dynamics:
  status: "active"
  location: "Adventurer's Guild, Capital City"
  health: 0.9
  morale: 0.8
  mood: "determined, slightly worried about upcoming quest"

contextual_fit:
  genres: ["fantasy", "adventure", "heroic"]
  media: ["game", "novel", "ai-platform"]
  deployment_contexts: ["teen+ fantasy campaigns", "heroic adventures", "magical academy settings"]

meta_properties:
  target_audience:
    age_range: "13+"
    tone_alignment: "heroic fantasy"
  appropriateness:
    violence: "fantasy combat"
    sexuality: "minimal"
    language: "mild"
    cultural_sensitivity: ["respectful fantasy representation"]
  content_ratings:
    - system: "ESRB"
      rating: "T"
      notes: "Fantasy violence, mild language"
  safety_warnings: ["fantasy warfare", "magical dangers", "themes of sacrifice"]

representation_accessibility:
  representation_notes:
    culture: "fantasy human culture"
    disability: "none"
  accessibility_guidance: ["clear descriptions of magical effects", "avoid overly complex magical jargon"]
  sensitivity_notes: ["avoid magical stereotypes", "show diverse magical abilities"]

assets:
  images: []
  audio: []
  links: 
    - "https://example.com/rita-character-art"
    - "https://example.com/rita-backstory"

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
  tags: ["adventurer", "hero", "fantasy", "mage", "leader", "dnd5e", "protagonist"]
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

## Production Best Practices

### 1. Complete Metadata

Always include comprehensive metadata:

```yaml
meta:
  tags: ["adventurer", "hero", "fantasy", "mage", "leader"]
  authorship:
    created_by: "Your Name"
    source: "Original Creation"
    contributors: ["Contributor 1", "Contributor 2"]
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
    version: "1.0.0"
  canon_status: "official"
  license: "CC-BY-4.0"
```

### 2. Localization Support

Include display names for multiple languages:

```yaml
names:
  canon: "Rita"
  display:
    en-US: "Rita"
    es-ES: "Alicia"
    fr-FR: "Rita"
    de-DE: "Rita"
```

### 3. Content Rating and Appropriateness

For production deployment, always include comprehensive content rating information to ensure appropriate character deployment across different platforms and audiences.

!!! info "Content Rating Research"
    For detailed guidance on content rating systems and cultural sensitivity, see our [Content Ratings Research](../deep-dives/research/content-ratings-unified-schema.md) paper.

#### Basic Content Profile

```yaml
meta:
  character_content_profile:
    target_audience:
      age_range: "13+"
      demographics: "Teen and adult fantasy fans; RPG enthusiasts"
      tone_alignment: "heroic"
    
    appropriateness:
      violence_level: "realistic"      # none, cartoon, realistic, extreme
      sexuality_level: "none"          # none, implied, explicit
      language_level: "mild"           # clean, mild, strong, explicit
      cultural_sensitivity:
        - "Contains fantasy magic and supernatural elements"
        - "Themes of good vs evil may be sensitive to some groups"
    
    content_rating:
      - system: "ESRB"
        rating: "T for Teen"
        notes: "Fantasy violence, mild language, and suggestive themes"
      - system: "PEGI"
        rating: "12"
        notes: "Violence against fantasy characters"
      - system: "IARC"
        rating: "12+"
        notes: "Fantasy violence and mild language"
      - system: "MPA"
        rating: "PG-13"
        notes: "Fantasy action violence"
    
    deployment_contexts:
      - "teen fantasy RPG"
      - "streaming platform"
      - "fantasy novel adaptation"
    
    safety_warnings:
      - "Fantasy violence"
      - "Mild peril and danger"
      - "Supernatural themes"
```

#### Mature Content Profile

For characters with mature content:

```yaml
meta:
  character_content_profile:
    target_audience:
      age_range: "18+"
      demographics: "Adult gamers; mature fantasy fans"
      tone_alignment: "dark"
    
    appropriateness:
      violence_level: "extreme"
      sexuality_level: "implied"
      language_level: "strong"
      cultural_sensitivity:
        - "Contains graphic violence and horror elements"
        - "Themes of corruption and moral ambiguity"
        - "May trigger anxiety or fear responses"
    
    content_rating:
      - system: "ESRB"
        rating: "M for Mature"
        notes: "Blood and Gore, Intense Violence, Strong Language"
      - system: "PEGI"
        rating: "18"
        notes: "Extreme violence, strong language"
      - system: "MPA"
        rating: "R"
        notes: "Strong violence and language throughout"
    
    deployment_contexts:
      - "mature gaming platforms"
      - "adult streaming services"
      - "horror entertainment venues"
    
    safety_warnings:
      - "Extreme graphic violence"
      - "Strong language and profanity"
      - "Horror and psychological elements"
      - "Content not suitable for minors"
```

#### Rating System Selection

Choose appropriate rating systems based on your target markets:

- **ESRB**: North American gaming market
- **PEGI**: European gaming market
- **IARC**: Global digital content
- **MPA**: Film and video content
- **CERO**: Japanese market
- **USK**: German market
- **ACB**: Australian market

#### Cultural Sensitivity Guidelines

1. **Research Local Standards**: Understand regional content sensitivity
2. **Document Concerns**: List specific cultural sensitivity issues
3. **Consider Context**: Evaluate content within cultural context
4. **Regular Updates**: Keep abreast of changing cultural norms
5. **Expert Consultation**: Work with local cultural advisors when possible

## Validation Workflows

### Pre-Commit Validation

Set up validation before committing changes:

```bash
# Validate all characters
find . -name "*.yaml" -exec ocd-validate {} \;

# Validate with warnings as errors
ocd-validate character.yaml --warnings-as-errors
```

### CI/CD Integration

Add validation to your CI pipeline:

```yaml title=".github/workflows/validate.yml"
name: Validate OCD Characters

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install OCD validator
        run: pip install ocd
      - name: Validate characters
        run: |
          find . -name "*.yaml" -exec ocd-validate {} \;
```

### Batch Validation Script

Create a script for validating multiple characters:

```bash title="validate-all.sh"
#!/bin/bash

echo "Validating all OCD characters..."

# Find all YAML files
find . -name "*.yaml" -not -path "./node_modules/*" | while read file; do
  echo "Validating $file..."
  if ! ocd-validate "$file" --warnings-as-errors; then
    echo "❌ Validation failed for $file"
    exit 1
  fi
done

echo "✅ All characters validated successfully!"
```

## Normalization Best Practices

### 1. Consistent Naming

Use consistent naming conventions:

```yaml
# Good
id: "char-rita-adventurer"
tags: ["adventurer", "hero", "fantasy"]

# Avoid
id: "Rita_Adventurer_001"
tags: ["Adventurer", "HERO", "Fantasy"]
```

### 2. Standardized Timestamps

Always use ISO 8601 format:

```yaml
# Good
created_at: "2024-01-01T00:00:00Z"

# Avoid
created_at: "January 1, 2024"
created_at: "2024-01-01"
```

### 3. Consistent Trait Names

Use standardized trait names:

```yaml
# Good
- name: "introversion-extraversion"
- name: "combat-readiness"

# Avoid
- name: "Introversion vs Extraversion"
- name: "Combat Readiness"
```

## Deployment Strategies

### 1. Version Control

Use semantic versioning for characters:

```yaml
meta:
  versioning:
    version: "1.2.0"  # Major.Minor.Patch
```

### 2. Environment-Specific Deployments

Create different versions for different environments:

```yaml
# Development
meta:
  canon_status: "draft"
  tags: ["adventurer", "hero", "fantasy", "draft"]

# Production
meta:
  canon_status: "official"
  tags: ["adventurer", "hero", "fantasy"]
```

### 3. Asset Management

Include proper asset references:

```yaml
assets:
  images:
    - url: "https://cdn.example.com/rita-portrait.jpg"
      alt: "Rita portrait"
      license: "CC-BY-4.0"
  audio:
    - url: "https://cdn.example.com/rita-voice.mp3"
      description: "Rita's voice sample"
```

## Maintenance and Updates

### 1. Regular Validation

Set up regular validation checks:

```bash
# Weekly validation
0 0 * * 0 /path/to/validate-all.sh
```

### 2. Dependency Updates

Keep validators updated:

```bash
# Update Python validator
pip install --upgrade ocd

# Update Node.js validator
npm update @ocd-tools/validator
```

### 3. Schema Evolution

Plan for schema changes:

```yaml
# Include migration notes
meta:
  versioning:
    version: "2.0.0"
    migration_notes: "Updated trait model, added new personality fields"
```

## Common Production Issues

### 1. Unresolved References

Always check for unresolved references:

```bash
ocd-validate character.yaml
# Look for: UNRESOLVED_REF warnings
```

### 2. Content Rating Conflicts

Ensure consistency between traits and ratings:

```yaml
# This will cause RATING_CONFLICT warning
personality:
  traits:
    - name: "violent-pacifist"
      polarity: 0.8  # Leans violent
meta_properties:
  appropriateness:
    violence: "none"  # But rated as no violence
```

### 3. Timestamp Issues

Keep timestamps current:

```yaml
meta:
  versioning:
    last_modified: "2024-01-01T00:00:00Z"  # Update when you make changes
```

## What's Next?

Congratulations! You've completed the OCD Tutorial. You now have:

- ✅ A complete understanding of OCD structure
- ✅ A production-ready character definition
- ✅ Knowledge of validation workflows
- ✅ Best practices for deployment and maintenance

## Additional Resources

- **[Examples Gallery](../authoring/examples.md)**: Browse more character examples
- **[Specification](../spec/schema-overview.md)**: Deep dive into the technical details
- **[Integration Guide](../integration/python-validator.md)**: Learn about validator APIs
- **[FAQ](../faq.md)**: Common questions and answers
- **[Contributing](../governance/contributing-to-spec.md)**: Help improve OCD

## Quick Reference

### Production Checklist
- [ ] Complete metadata with authorship and versioning
- [ ] Localized display names
- [ ] Comprehensive character content profile with ratings
- [ ] Appropriate content rating for target markets
- [ ] Cultural sensitivity warnings documented
- [ ] Safety warnings included
- [ ] Proper asset references
- [ ] Validation passes without warnings
- [ ] All references resolved
- [ ] Consistent naming conventions
- [ ] Current timestamps

### Validation Commands
```bash
# Basic validation
ocd-validate character.yaml

# With warnings as errors
ocd-validate character.yaml --warnings-as-errors

# Print normalized output
ocd-validate character.yaml --print
```

### Common Extensions
- `x-dnd5e`: D&D 5th Edition
- `x-pf2e`: Pathfinder 2nd Edition
- `x-coc`: Call of Cthulhu
- `x-savage`: Savage Worlds

---

## TODO: Production Notes Update

**Status**: Pending  
**Last Updated**: 2024-12-19  
**Priority**: Medium

This section needs updates to reflect recent changes to the OpenCharacter Specification:

- [ ] Review and update content rating examples with latest schema
- [ ] Add new production deployment patterns
- [ ] Update validation commands and examples
- [ ] Incorporate feedback from production case studies
- [ ] Ensure all examples are current with latest OCD version