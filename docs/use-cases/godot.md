# Godot Integration


Integrate OCD characters into Godot projects using GDScript's flexible scripting system and Godot's powerful node architecture for dynamic character behavior.


Godot's node-based architecture and GDScript's simplicity make it perfect for creating dynamic character systems. This guide shows you how to build a complete OCD character integration system that leverages Godot's strengths.

## Getting Started with Godot

### Prerequisites

- Godot 4.2 or newer
- Basic understanding of GDScript
- OCD character files in JSON format
- Familiarity with Godot's node system

### Quick Setup

1. **Create Character Classes**: Set up OCD character resource classes
2. **Create Import System**: Build character import functionality
3. **Set Up Behavior System**: Implement personality-driven behavior
4. **Test Integration**: Import and test your first character

## Core Character System

### OCD Character Resource

```gdscript
# OCDCharacter.gd
class_name OCDCharacter
extends Resource

@export var id: String
@export var names: OCDNames
@export var identity: OCDIdentity
@export var personality: OCDPersonality
@export var appearance: OCDAppearance

func load_from_json(file_path: String) -> bool:
    var file = FileAccess.open(file_path, FileAccess.READ)
    if file == null:
        print("Failed to open file: ", file_path)
        return false
    
    var json_string = file.get_as_text()
    file.close()
    
    var json = JSON.new()
    var parse_result = json.parse(json_string)
    
    if parse_result != OK:
        print("Failed to parse JSON: ", json.get_error_message())
        return false
    
    var data = json.get_data()
    
    # Parse basic character info
    id = data.get("id", "")
    
    # Parse names
    var names_data = data.get("names", {})
    names = OCDNames.new()
    names.canon = names_data.get("canon", "")
    names.aliases = names_data.get("aliases", [])
    names.nicknames = names_data.get("nicknames", [])
    
    # Parse identity
    var identity_data = data.get("identity", {})
    identity = OCDIdentity.new()
    identity.species = identity_data.get("species", "")
    identity.age = identity_data.get("age", 0)
    identity.gender = identity_data.get("gender", "")
    identity.roles = identity_data.get("roles", [])
    
    # Parse personality
    var personality_data = data.get("personality", {})
    personality = OCDPersonality.new()
    personality.traits = []
    
    var traits_data = personality_data.get("traits", [])
    for trait_data in traits_data:
        var trait = OCDTrait.new()
        trait.name = trait_data.get("name", "")
        trait.kind = trait_data.get("kind", "")
        trait.value = trait_data.get("value", 0.0)
        trait.polarity = trait_data.get("polarity", 0.0)
        trait.intensity = trait_data.get("intensity", 0.0)
        personality.traits.append(trait)
    
    # Parse appearance
    var appearance_data = data.get("appearance", {})
    appearance = OCDAppearance.new()
    appearance.physical_description = appearance_data.get("physical_description", [])
    appearance.clothing = appearance_data.get("clothing", [])
    appearance.accessories = appearance_data.get("accessories", [])
    
    return true

func get_trait_value(trait_name: String) -> float:
    for trait in personality.traits:
        if trait.name == trait_name:
            return trait.value
    return 0.0

func get_trait_polarity(trait_name: String) -> float:
    for trait in personality.traits:
        if trait.name == trait_name:
            return trait.polarity
    return 0.0

func has_trait(trait_name: String) -> bool:
    for trait in personality.traits:
        if trait.name == trait_name:
            return true
    return false

func get_character_name() -> String:
    return names.canon if names else ""

func get_species() -> String:
    return identity.species if identity else ""

func get_age() -> int:
    return identity.age if identity else 0
```

### Supporting Data Classes

```gdscript
# OCDNames.gd
class_name OCDNames
extends Resource

@export var canon: String
@export var aliases: Array[String]
@export var nicknames: Array[String]

func _init():
    canon = ""
    aliases = []
    nicknames = []
```

```gdscript
# OCDIdentity.gd
class_name OCDIdentity
extends Resource

@export var species: String
@export var age: int
@export var gender: String
@export var roles: Array[String]

func _init():
    species = ""
    age = 0
    gender = ""
    roles = []
```

```gdscript
# OCDPersonality.gd
class_name OCDPersonality
extends Resource

@export var traits: Array[OCDTrait]

func _init():
    traits = []
```

```gdscript
# OCDTrait.gd
class_name OCDTrait
extends Resource

@export var name: String
@export var kind: String
@export var value: float
@export var polarity: float
@export var intensity: float

func _init():
    name = ""
    kind = ""
    value = 0.0
    polarity = 0.0
    intensity = 0.0
```

```gdscript
# OCDAppearance.gd
class_name OCDAppearance
extends Resource

@export var physical_description: Array[String]
@export var clothing: Array[String]
@export var accessories: Array[String]

func _init():
    physical_description = []
    clothing = []
    accessories = []
```

## Character Controller System

### OCD Character Controller

```gdscript
# OCDCharacterController.gd
class_name OCDCharacterController
extends CharacterBody3D

@export var ocd_character: OCDCharacter
@export var ai_controller: Node
@export var dialogue_system: Node
@export var appearance_system: Node

# Personality components
var personality_component: OCDPersonalityComponent
var behavior_component: OCDBehaviorComponent
var dialogue_component: OCDDialogueComponent

func _ready():
    if ocd_character:
        setup_character_behavior()

func setup_character_behavior():
    # Create personality component
    personality_component = OCDPersonalityComponent.new()
    add_child(personality_component)
    
    # Create behavior component
    behavior_component = OCDBehaviorComponent.new()
    add_child(behavior_component)
    
    # Create dialogue component
    dialogue_component = OCDDialogueComponent.new()
    add_child(dialogue_component)
    
    # Apply personality traits
    apply_personality_traits()
    
    # Configure appearance
    configure_appearance()
    
    # Set up AI behavior
    setup_ai_behavior()
    
    # Set up dialogue system
    setup_dialogue_system()

func apply_personality_traits():
    if not ocd_character or not personality_component:
        return
    
    for trait in ocd_character.personality.traits:
        match trait.name:
            "introversion-extraversion":
                personality_component.set_extraversion(trait.polarity)
            "combat-readiness":
                personality_component.set_combat_readiness(trait.value)
            "moral-uprightness":
                personality_component.set_moral_alignment(trait.value)
            "magical-aptitude":
                personality_component.set_magical_aptitude(trait.value)
            "nature-connection":
                personality_component.set_nature_connection(trait.value)

func configure_appearance():
    if not ocd_character or not appearance_system:
        return
    
    # Set physical description
    if ocd_character.appearance.physical_description.size() > 0:
        appearance_system.set_physical_description(ocd_character.appearance.physical_description)
    
    # Set clothing
    if ocd_character.appearance.clothing.size() > 0:
        appearance_system.set_clothing(ocd_character.appearance.clothing)
    
    # Set accessories
    if ocd_character.appearance.accessories.size() > 0:
        appearance_system.set_accessories(ocd_character.appearance.accessories)

func setup_ai_behavior():
    if not ocd_character or not behavior_component:
        return
    
    # Configure behavior based on personality
    var extraversion = ocd_character.get_trait_polarity("introversion-extraversion")
    var combat_readiness = ocd_character.get_trait_value("combat-readiness")
    var moral_alignment = ocd_character.get_trait_value("moral-uprightness")
    
    # Set social behavior
    if extraversion > 0.3:
        behavior_component.set_social_behavior(OCDBehaviorComponent.SocialBehavior.EXTROVERTED)
    elif extraversion < -0.3:
        behavior_component.set_social_behavior(OCDBehaviorComponent.SocialBehavior.INTROVERTED)
    else:
        behavior_component.set_social_behavior(OCDBehaviorComponent.SocialBehavior.BALANCED)
    
    # Set combat behavior
    if combat_readiness > 0.7:
        behavior_component.set_combat_behavior(OCDBehaviorComponent.CombatBehavior.AGGRESSIVE)
    elif combat_readiness < 0.3:
        behavior_component.set_combat_behavior(OCDBehaviorComponent.CombatBehavior.DEFENSIVE)
    else:
        behavior_component.set_combat_behavior(OCDBehaviorComponent.CombatBehavior.BALANCED)
    
    # Set moral behavior
    if moral_alignment > 0.7:
        behavior_component.set_moral_behavior(OCDBehaviorComponent.MoralBehavior.HEROIC)
    elif moral_alignment < 0.3:
        behavior_component.set_moral_behavior(OCDBehaviorComponent.MoralBehavior.VILLAINOUS)
    else:
        behavior_component.set_moral_behavior(OCDBehaviorComponent.MoralBehavior.NEUTRAL)

func setup_dialogue_system():
    if not ocd_character or not dialogue_component:
        return
    
    # Set character name
    dialogue_component.set_character_name(ocd_character.get_character_name())
    
    # Set personality traits for dialogue generation
    var traits = {}
    for trait in ocd_character.personality.traits:
        if trait.kind == "bipolar":
            traits[trait.name] = trait.polarity
        else:
            traits[trait.name] = trait.value
    
    dialogue_component.set_personality_traits(traits)
```

## Personality Component System

### OCD Personality Component

```gdscript
# OCDPersonalityComponent.gd
class_name OCDPersonalityComponent
extends Node

# Personality traits
@export var extraversion: float = 0.0  # -1 to 1
@export var combat_readiness: float = 0.5  # 0 to 1
@export var moral_alignment: float = 0.5  # 0 to 1
@export var magical_aptitude: float = 0.5  # 0 to 1
@export var nature_connection: float = 0.5  # 0 to 1

# Behavior settings
@export var social_radius: float = 5.0
@export var combat_aggression: float = 1.0
@export var moral_threshold: float = 0.3
@export var magic_power: float = 1.0
@export var nature_affinity: float = 1.0

# Visual settings
@export var aura_color: Color = Color.WHITE
@export var aura_intensity: float = 1.0

func set_extraversion(value: float):
    extraversion = clamp(value, -1.0, 1.0)
    update_social_behavior()

func set_combat_readiness(value: float):
    combat_readiness = clamp(value, 0.0, 1.0)
    update_combat_behavior()

func set_moral_alignment(value: float):
    moral_alignment = clamp(value, 0.0, 1.0)
    update_moral_behavior()

func set_magical_aptitude(value: float):
    magical_aptitude = clamp(value, 0.0, 1.0)
    update_magical_behavior()

func set_nature_connection(value: float):
    nature_connection = clamp(value, 0.0, 1.0)
    update_nature_behavior()

func update_social_behavior():
    # Adjust social interaction radius based on extraversion
    social_radius = 3.0 + (extraversion + 1.0) * 2.0  # 3-7 units
    
    # Adjust conversation frequency
    var conversation_ai = get_node("../ConversationAI")
    if conversation_ai:
        conversation_ai.set_talkativeness(extraversion)

func update_combat_behavior():
    # Adjust combat aggression based on readiness
    combat_aggression = combat_readiness * 2.0
    
    # Adjust weapon proficiency
    var combat_ai = get_node("../CombatAI")
    if combat_ai:
        combat_ai.set_weapon_skill(combat_readiness)

func update_moral_behavior():
    # Adjust moral decision making
    var decision_ai = get_node("../DecisionAI")
    if decision_ai:
        decision_ai.set_moral_threshold(moral_threshold)

func update_magical_behavior():
    # Adjust magical power
    magic_power = magical_aptitude * 2.0
    
    # Update visual effects
    var magical_effects = get_node("../MagicalEffects")
    if magical_effects:
        magical_effects.set_power_level(magical_aptitude)

func update_nature_behavior():
    # Adjust nature affinity
    nature_affinity = nature_connection * 2.0
    
    # Update nature-related abilities
    var nature_abilities = get_node("../NatureAbilities")
    if nature_abilities:
        nature_abilities.set_affinity(nature_connection)
```

## Behavior Component System

### OCD Behavior Component

```gdscript
# OCDBehaviorComponent.gd
class_name OCDBehaviorComponent
extends Node

enum SocialBehavior {
    INTROVERTED,
    BALANCED,
    EXTROVERTED
}

enum CombatBehavior {
    DEFENSIVE,
    BALANCED,
    AGGRESSIVE
}

enum MoralBehavior {
    VILLAINOUS,
    NEUTRAL,
    HEROIC
}

@export var social_behavior: SocialBehavior = SocialBehavior.BALANCED
@export var combat_behavior: CombatBehavior = CombatBehavior.BALANCED
@export var moral_behavior: MoralBehavior = MoralBehavior.NEUTRAL

# AI components
@export var behavior_tree: Node
@export var blackboard: Node

func set_social_behavior(behavior: SocialBehavior):
    social_behavior = behavior
    update_behavior_tree()

func set_combat_behavior(behavior: CombatBehavior):
    combat_behavior = behavior
    update_behavior_tree()

func set_moral_behavior(behavior: MoralBehavior):
    moral_behavior = behavior
    update_behavior_tree()

func update_behavior_tree():
    update_blackboard_values()
    
    if behavior_tree:
        behavior_tree.restart()

func update_blackboard_values():
    if blackboard:
        blackboard.set_value("SocialBehavior", social_behavior)
        blackboard.set_value("CombatBehavior", combat_behavior)
        blackboard.set_value("MoralBehavior", moral_behavior)
```

## Dialogue System Integration

### OCD Dialogue Component

```gdscript
# OCDDialogueComponent.gd
class_name OCDDialogueComponent
extends Node

@export var character_name: String
@export var personality_traits: Dictionary = {}
@export var response_delay: float = 1.0
@export var personality_influence: float = 1.0

var dialogue_generator: OCDDialogueGenerator
var dialogue_history: Array = []

func set_character_name(name: String):
    character_name = name

func set_personality_traits(traits: Dictionary):
    personality_traits = traits
    initialize_dialogue_generator()

func initialize_dialogue_generator():
    dialogue_generator = OCDDialogueGenerator.new(character_name, personality_traits)

func generate_response(player_input: String, context: Dictionary = {}) -> String:
    if not dialogue_generator:
        return "I don't know what to say..."
    
    var response = dialogue_generator.generate_response(player_input, context)
    
    # Store dialogue in history
    dialogue_history.append({
        "player_input": player_input,
        "response": response,
        "context": context,
        "timestamp": Time.get_unix_time_from_system()
    })
    
    return response

func get_greeting() -> String:
    if not dialogue_generator:
        return "Hello there."
    
    return dialogue_generator.get_greeting()

func get_dialogue_history() -> Array:
    return dialogue_history
```

### Dialogue Generator

```gdscript
# OCDDialogueGenerator.gd
class_name OCDDialogueGenerator
extends RefCounted

var character_name: String
var personality_traits: Dictionary

func _init(name: String, traits: Dictionary):
    character_name = name
    personality_traits = traits

func generate_response(player_input: String, context: Dictionary = {}) -> String:
    # Analyze player input
    var input_sentiment = analyze_sentiment(player_input)
    
    # Get character's current emotional state
    var emotional_state = calculate_emotional_state(context)
    
    # Select response based on personality
    return select_response(input_sentiment, emotional_state, context)

func get_greeting() -> String:
    var extraversion = personality_traits.get("introversion-extraversion", 0.0)
    
    if extraversion > 0.3:
        return "Hey there! Great to meet you!"
    elif extraversion < -0.3:
        return "Hello..."
    else:
        return "Hello there."

func analyze_sentiment(input: String) -> float:
    var lower_input = input.to_lower()
    
    if lower_input.contains("good") or lower_input.contains("great") or lower_input.contains("awesome"):
        return 0.5
    elif lower_input.contains("bad") or lower_input.contains("terrible") or lower_input.contains("awful"):
        return -0.5
    
    return 0.0

func calculate_emotional_state(context: Dictionary) -> float:
    var base_state = 0.0
    
    # Modify based on personality traits
    var extraversion = personality_traits.get("introversion-extraversion", 0.0)
    var moral_alignment = personality_traits.get("moral-uprightness", 0.5)
    
    return base_state + (extraversion * 0.3) + (moral_alignment - 0.5) * 0.2

func select_response(input_sentiment: float, emotional_state: float, context: Dictionary) -> String:
    var extraversion = personality_traits.get("introversion-extraversion", 0.0)
    var moral_alignment = personality_traits.get("moral-uprightness", 0.5)
    
    if extraversion > 0.3:
        if moral_alignment > 0.7:
            return "That's wonderful! I'm so glad to hear that!"
        else:
            return "Interesting! Tell me more about that."
    elif extraversion < -0.3:
        if moral_alignment > 0.7:
            return "I understand. That's quite noble of you."
        else:
            return "I see. That's... interesting."
    else:
        return "I understand. Thank you for sharing that with me."
```

## Visual Effects Integration

### OCD Appearance System

```gdscript
# OCDAppearanceSystem.gd
class_name OCDAppearanceSystem
extends Node

@export var physical_description: Array[String] = []
@export var clothing: Array[String] = []
@export var accessories: Array[String] = []

# Visual effects
@export var aura_effect: GPUParticles3D
@export var character_light: Light3D
@export var character_material: StandardMaterial3D

func set_physical_description(description: Array[String]):
    physical_description = description
    update_visual_appearance()

func set_clothing(clothing_items: Array[String]):
    clothing = clothing_items
    update_clothing()

func set_accessories(accessory_items: Array[String]):
    accessories = accessory_items
    update_accessories()

func update_visual_appearance():
    # Apply physical description to character model
    # This would typically involve modifying the character's 3D model
    # or applying different materials/textures
    pass

func update_clothing():
    # Apply clothing items to character
    # This would typically involve enabling/disabling clothing meshes
    # or changing clothing materials
    pass

func update_accessories():
    # Apply accessories to character
    # This would typically involve enabling/disabling accessory meshes
    pass
```

## Utility Functions

### OCD Utility Functions

```gdscript
# OCDUtils.gd
class_name OCDUtils
extends RefCounted

static func import_character_from_file(file_path: String) -> OCDCharacter:
    var character = OCDCharacter.new()
    if character.load_from_json(file_path):
        return character
    return null

static func import_character_from_string(json_string: String) -> OCDCharacter:
    var character = OCDCharacter.new()
    var file = FileAccess.open("user://temp_character.json", FileAccess.WRITE)
    if file:
        file.store_string(json_string)
        file.close()
        
        var success = character.load_from_json("user://temp_character.json")
        
        # Clean up temp file
        DirAccess.remove_absolute("user://temp_character.json")
        
        if success:
            return character
    return null

static func validate_character(character: OCDCharacter) -> bool:
    if not character:
        return false
    
    if character.id.is_empty():
        return false
    
    if not character.names or character.names.canon.is_empty():
        return false
    
    if not character.personality or character.personality.traits.is_empty():
        return false
    
    return true

static func get_trait_summary(character: OCDCharacter) -> Dictionary:
    var summary = {}
    
    if not character or not character.personality:
        return summary
    
    for trait in character.personality.traits:
        summary[trait.name] = {
            "value": trait.value,
            "polarity": trait.polarity,
            "intensity": trait.intensity,
            "kind": trait.kind
        }
    
    return summary
```

## Best Practices

### Performance Optimization

1. **Resource Management**: Use Godot's resource system for character data
2. **Object Pooling**: Implement object pooling for frequently spawned characters
3. **LOD System**: Use Level of Detail for character rendering
4. **Caching**: Cache frequently accessed trait values

### Memory Management

1. **Resource Cleanup**: Properly dispose of character resources when not needed
2. **Weak References**: Use weak references where appropriate
3. **Scene Management**: Unload character scenes when not needed

### Code Organization

1. **Modular Design**: Keep character systems modular and reusable
2. **Signal Usage**: Use Godot's signal system for character events
3. **Documentation**: Add comments and documentation to your code
4. **Testing**: Create unit tests for character systems

### Godot-Specific Tips

1. **Use Scenes**: Create character scenes for easy reuse
2. **Export Variables**: Use @export for easy editor configuration
3. **Groups**: Use Godot's group system for character management
4. **Autoloads**: Use autoloads for global character systems

!!! tip "Ready to Integrate?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
