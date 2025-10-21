# Interactive & Storytelling Applications

<div class="hero-section">
Create immersive interactive experiences with OCD-powered characters that bring your stories to life in digital worlds.
</div>

OCD bridges the gap between creative character design and technical implementation, enabling rich interactive experiences across games, visual novels, AI-driven narratives, and virtual production. Whether you're building the next blockbuster game or creating an AI-powered storytelling platform, OCD provides the structured foundation your interactive characters need.

## Game Engine Integration

### [Unity Integration](unity.md)
Integrate OCD characters seamlessly into Unity projects with structured data that automatically configures in-game attributes, behaviors, and visual systems. Includes C# scripts for character import, personality components, and AI behavior integration.

### [Unreal Engine Integration](unreal.md)
Build sophisticated character systems in Unreal Engine using Blueprint-friendly C++ classes and visual scripting. Features comprehensive data structures, behavior components, and Blueprint integration examples.

### [Godot Integration](godot.md)
Leverage Godot's node-based architecture and GDScript's simplicity for dynamic character systems. Includes resource classes, character controllers, and dialogue system integration.

## Creative Applications

### [Visual Novels & RPG Systems](visual-novels.md)
Create immersive visual novels and RPG experiences with personality-driven dialogue trees, expression systems, and character progression. Features dialogue engines, expression management, and branching narrative systems.

### [AI-Driven NPC Personalities](ai-npcs.md)
Build sophisticated AI-driven NPCs with behavior trees, memory systems, and learning algorithms. Includes personality-driven decision making, social interaction systems, and adaptive behavior patterns.

### [Interactive Storytelling Tools](storytelling.md)
Create dynamic, adaptive storytelling experiences with narrative generation, branching storylines, and contextual dialogue systems. Features story engines, dialogue systems, and story branching logic.

## Production Workflows

### [Virtual Production](virtual-production.md)
Integrate OCD characters into virtual production pipelines for real-time character management, cross-platform synchronization, and live production workflows. Includes character managers, sync systems, and production tools.

## Getting Started

Choose your development path based on your project needs:

### Game Development

- **[Unity Integration](unity.md)** - C# scripts and component systems
- **[Unreal Engine Integration](unreal.md)** - C++ classes and Blueprint integration  
- **[Godot Integration](godot.md)** - GDScript and node-based architecture

### Creative Applications

- **[Visual Novels & RPGs](visual-novels.md)** - Dialogue systems and character progression
- **[AI NPCs](ai-npcs.md)** - Behavior trees and learning systems
- **[Interactive Storytelling](storytelling.md)** - Dynamic narrative generation

### Production Workflows

- **[Virtual Production](virtual-production.md)** - Real-time character management and cross-platform sync

## Quick Start Examples

### Basic Character Import

```python
import json

# Load OCD character data
with open('character.ocd', 'r') as f:
    character_data = json.load(f)

# Extract personality traits
traits = {}
for trait in character_data['personality']['traits']:
    if trait['kind'] == 'bipolar':
        traits[trait['name']] = trait['polarity']
    else:
        traits[trait['name']] = trait['value']

# Use traits in your application
extraversion = traits.get('introversion-extraversion', 0)
if extraversion > 0.3:
    print("Character is extraverted!")
```

### Unity C# Integration

```csharp
// Import character in Unity
public void ImportCharacter(string ocdJsonPath)
{
    string jsonContent = File.ReadAllText(ocdJsonPath);
    OCDCharacter ocdChar = JsonConvert.DeserializeObject<OCDCharacter>(jsonContent);
    
    // Create character GameObject
    GameObject character = new GameObject(ocdChar.names.canon);
    
    // Apply personality traits
    ApplyPersonalityTraits(character, ocdChar.personality.traits);
}
```

### Godot GDScript Integration

```gdscript
# Load character in Godot
func load_character(file_path: String) -> bool:
    var file = FileAccess.open(file_path, FileAccess.READ)
    if file == null:
        return false
    
    var json_string = file.get_as_text()
    var json = JSON.new()
    var parse_result = json.parse(json_string)
    
    if parse_result != OK:
        return false
    
    var data = json.get_data()
    # Process character data...
    return true
```

!!! tip "Ready to Build Interactive Experiences?"
    Start with our [Integration Guides](../integration/python-validator.md) to see how to integrate OCD into your applications, or explore our [Interactive Examples](../authoring/examples.md) for implementation patterns.
