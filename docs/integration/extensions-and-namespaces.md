# Extensions & Namespaces

OCD supports custom extensions through the `x-*` namespace pattern, allowing you to add system-specific data while maintaining compatibility with the core specification.

## Extension Namespaces

Extensions use the `x-` prefix to avoid conflicts with core OCD fields:

```yaml title="character-with-extensions.yaml"
ocd_version: "1.0.0"
id: "char-example"
names:
  canon: "Example Character"

# Core OCD fields
identity:
  kind: "humanoid"
  species: "Human"

# Custom extensions
x-dnd5e:
  class: "Fighter"
  level: 8
  abilities:
    strength: 18
    dexterity: 12

x-my-game:
  system: "MyFantasyRPG"
  character_type: "Warrior"
  power_level: "Heroic"
```

## Creating Extensions

### 1. Choose a Namespace

Select a descriptive namespace that identifies your system:

```yaml
# Good examples
x-dnd5e:          # D&D 5th Edition
x-pathfinder:     # Pathfinder RPG
x-world-of-darkness: # World of Darkness
x-my-campaign:    # Custom campaign

# Avoid
x-data:           # Too generic
x-extra:          # Not descriptive
x-system:         # Too vague
```

### 2. Define Your Schema

Document the structure and validation rules:

```yaml title="x-my-system-schema.yaml"
x-my-system:
  # Required fields
  system: "MyFantasyRPG"        # System identifier
  version: "2.1"               # System version
  character_type: "Mage"       # Character class/type
  
  # Optional fields
  power_level: "Heroic"        # Power level (Novice, Heroic, Legendary)
  abilities:                   # System-specific abilities
    - name: "Fireball"
      level: 3
      cost: 5
    - name: "Heal"
      level: 2
      cost: 3
  
  stats:                       # System-specific stats
    magic: 18
    health: 45
    mana: 60
  
  equipment:                   # System-specific equipment
    weapon: "Staff of Power"
    armor: "Robe of Protection"
```

### 3. Document Your Extension

Create documentation for your extension:

```markdown
# MyFantasyRPG Extension (x-my-system)

## Overview
This extension adds support for MyFantasyRPG system mechanics.

## Required Fields
- `system`: Must be "MyFantasyRPG"
- `version`: System version (e.g., "2.1")
- `character_type`: Character class (Mage, Warrior, Rogue)

## Optional Fields
- `power_level`: Character power level
- `abilities`: List of character abilities
- `stats`: System-specific statistics
- `equipment`: Character equipment

## Examples
See examples/my-fantasy-character.yaml
```

## Popular Extensions

### D&D 5e Extension (`x-dnd5e`)

```yaml title="dnd5e-example.yaml"
x-dnd5e:
  class: "Wizard"
  subclass: "School of Evocation"
  level: 8
  abilities:
    strength: 10
    dexterity: 14
    constitution: 16
    intelligence: 18
    wisdom: 13
    charisma: 12
  hit_points: 64
  armor_class: 12
  speed: 30
  proficiencies:
    - "Arcana"
    - "History"
    - "Investigation"
  spells:
    known: 14
    prepared: 8
    slots:
      level_1: 4
      level_2: 3
      level_3: 3
      level_4: 1
```

### Pathfinder Extension (`x-pathfinder`)

```yaml title="pathfinder-example.yaml"
x-pathfinder:
  system: "Pathfinder 2e"
  version: "2.0"
  class: "Fighter"
  ancestry: "Human"
  background: "Soldier"
  level: 5
  abilities:
    strength: 18
    dexterity: 14
    constitution: 16
    intelligence: 10
    wisdom: 12
    charisma: 8
  hit_points: 80
  armor_class: 20
  saves:
    fortitude: 12
    reflex: 8
    will: 6
```

### Custom Campaign Extension

```yaml title="campaign-example.yaml"
x-my-campaign:
  campaign: "The Lost Realms"
  setting: "Fantasy"
  character_background: "Noble"
  faction: "The Silver Guard"
  reputation: 15
  contacts:
    - name: "Captain Marcus"
      relationship: "Mentor"
      location: "Capital City"
  quests:
    - name: "The Missing Artifact"
      status: "Active"
      priority: "High"
```

## Extension Best Practices

### 1. Avoid Core Field Duplication

Don't duplicate core OCD functionality:

```yaml
# ❌ Don't duplicate core fields
x-my-system:
  name: "Rita"  # Use names.canon instead
  species: "Human"  # Use identity.species instead

# ✅ Use extensions for system-specific data
x-my-system:
  class: "Mage"
  level: 8
  system_stats:
    magic_power: 18
    spell_points: 60
```

### 2. Use Consistent Naming

Follow consistent naming conventions:

```yaml
# ✅ Good: Consistent naming
x-my-system:
  character_class: "Warrior"
  character_level: 5
  character_stats:
    combat_rating: 15
    magic_rating: 8

# ❌ Avoid: Inconsistent naming
x-my-system:
  class: "Warrior"
  level: 5
  stats:
    combatRating: 15  # Mixed case
    magic_rating: 8
```

### 3. Version Your Extensions

Include version information for compatibility:

```yaml
x-my-system:
  extension_version: "1.2"  # Extension version
  system_version: "2.1"      # System version
  compatibility:
    min_ocd_version: "1.0.0"
    max_ocd_version: "1.0.0"
```

### 4. Document Validation Rules

Specify validation requirements:

```yaml
x-my-system:
  class: "Mage"
  level: 8  # Must be 1-20
  abilities:
    - name: "Fireball"
      level: 3  # Must be <= character level
      cost: 5   # Must be positive integer
```

## Extension Registry

### Community Extensions

Popular community extensions:

- **`x-dnd5e`**: D&D 5th Edition support
- **`x-pathfinder`**: Pathfinder RPG support
- **`x-world-of-darkness`**: World of Darkness support
- **`x-savage-worlds`**: Savage Worlds support

### Registering Your Extension

To register your extension:

1. **Document your schema** with examples
2. **Provide validation rules** and constraints
3. **Submit to the community registry** (coming soon)
4. **Follow naming conventions** (`x-system-name`)

## Validation and Extensions

### Core Validation

OCD validators don't validate extension content by default:

```bash
# Core validation passes
ocd-validate character.yaml
✅ Validation successful

# Extension validation requires custom tools
my-system-validate character.yaml
⚠️ Extension validation: Invalid class level
```

### Custom Validation

Create custom validators for your extensions:

```python
def validate_my_system_extension(data):
    """Validate x-my-system extension data."""
    if 'x-my-system' not in data:
        return True
    
    ext = data['x-my-system']
    
    # Validate required fields
    if 'class' not in ext:
        raise ValueError("Missing required field: class")
    
    # Validate field values
    if ext['level'] < 1 or ext['level'] > 20:
        raise ValueError("Level must be between 1 and 20")
    
    return True
```

## Migration and Compatibility

### Version Compatibility

Handle extension version changes:

```yaml
# Version 1.0
x-my-system:
  version: "1.0"
  class: "Mage"
  level: 8

# Version 2.0 (breaking change)
x-my-system:
  version: "2.0"
  character_class: "Mage"  # Renamed field
  character_level: 8       # Renamed field
  new_field: "value"       # Added field
```

### Migration Scripts

Provide migration tools for breaking changes:

```python
def migrate_extension_v1_to_v2(data):
    """Migrate x-my-system from v1.0 to v2.0."""
    if 'x-my-system' in data:
        ext = data['x-my-system']
        
        # Rename fields
        if 'class' in ext:
            ext['character_class'] = ext.pop('class')
        if 'level' in ext:
            ext['character_level'] = ext.pop('level')
        
        # Update version
        ext['version'] = '2.0'
    
    return data
```

## Examples and Templates

### Minimal Extension Template

```yaml title="extension-template.yaml"
ocd_version: "1.0.0"
id: "char-template"
names:
  canon: "Template Character"

# Core OCD fields
identity:
  kind: "humanoid"
  species: "Human"

# Extension template
x-my-system:
  system: "MySystem"
  version: "1.0"
  # Add your system-specific fields here
```

### Complete Extension Example

See the [Examples Gallery](../authoring/examples.md) for complete character examples with various extensions.

## Next Steps

- **[Examples Gallery](../authoring/examples.md)**: See extension examples in action
- **[Integration Guide](python-validator.md)**: Use extensions in applications
- **[Contributing Guide](../governance/contributing-to-spec.md)**: Contribute to core specification
- **[Community Discussions](https://github.com/Open-Character-Design/OCD-Specification/discussions)**: Share your extensions
