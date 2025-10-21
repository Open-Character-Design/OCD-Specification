# Unity Integration


Integrate OCD characters seamlessly into Unity projects with structured data that automatically configures in-game attributes, behaviors, and visual systems.


Unity's flexible component system makes it ideal for importing and using OCD character data. This guide shows you how to create a complete character import system that maps OCD personality traits to Unity components and behaviors.

## Getting Started with Unity

### Prerequisites

- Unity 2022.3 LTS or newer
- Newtonsoft.Json package (via Package Manager)
- Basic understanding of Unity's component system

### Quick Setup

1. **Install Dependencies**: Add Newtonsoft.Json via Window → Package Manager
2. **Create Character Importer**: Add the OCDCharacterImporter script to your project
3. **Set Up Character Prefabs**: Create prefab templates for your characters
4. **Test Import**: Import your first OCD character file

## Character Import System

### Core Import Script

```csharp
using UnityEngine;
using System.Collections.Generic;
using Newtonsoft.Json;

public class OCDCharacterImporter : MonoBehaviour
{
    [System.Serializable]
    public class OCDCharacter
    {
        public string id;
        public OCDNames names;
        public OCDIdentity identity;
        public OCDPersonality personality;
        public OCDAppearance appearance;
    }
    
    [System.Serializable]
    public class OCDNames
    {
        public string canon;
        public string[] aliases;
        public string[] nicknames;
    }
    
    [System.Serializable]
    public class OCDIdentity
    {
        public string species;
        public int age;
        public string gender;
        public string[] roles;
    }
    
    [System.Serializable]
    public class OCDPersonality
    {
        public OCDTrait[] traits;
    }
    
    [System.Serializable]
    public class OCDTrait
    {
        public string name;
        public string kind;
        public float value;
        public float polarity;
        public float intensity;
    }
    
    [System.Serializable]
    public class OCDAppearance
    {
        public string[] physical_description;
        public string[] clothing;
        public string[] accessories;
    }
    
    public void ImportCharacter(string ocdJsonPath)
    {
        string jsonContent = System.IO.File.ReadAllText(ocdJsonPath);
        OCDCharacter ocdChar = JsonConvert.DeserializeObject<OCDCharacter>(jsonContent);
        
        // Create character GameObject
        GameObject character = new GameObject(ocdChar.names.canon);
        
        // Apply personality traits to components
        ApplyPersonalityTraits(character, ocdChar.personality.traits);
        
        // Configure appearance
        ConfigureAppearance(character, ocdChar.appearance);
        
        // Set up AI behavior
        SetupAIBehavior(character, ocdChar.personality.traits);
        
        // Set up dialogue system
        SetupDialogueSystem(character, ocdChar);
    }
    
    private void ApplyPersonalityTraits(GameObject character, OCDTrait[] traits)
    {
        // Add personality component
        PersonalityComponent personality = character.AddComponent<PersonalityComponent>();
        
        foreach (var trait in traits)
        {
            switch (trait.name)
            {
                case "introversion-extraversion":
                    personality.SetExtraversion(trait.polarity);
                    break;
                case "combat-readiness":
                    personality.SetCombatReadiness(trait.value);
                    break;
                case "moral-uprightness":
                    personality.SetMoralAlignment(trait.value);
                    break;
                case "magical-aptitude":
                    personality.SetMagicalAptitude(trait.value);
                    break;
                case "nature-connection":
                    personality.SetNatureConnection(trait.value);
                    break;
            }
        }
    }
    
    private void ConfigureAppearance(GameObject character, OCDAppearance appearance)
    {
        // Add appearance component
        AppearanceComponent appearanceComp = character.AddComponent<AppearanceComponent>();
        
        // Set physical description
        if (appearance.physical_description != null)
        {
            appearanceComp.SetPhysicalDescription(appearance.physical_description);
        }
        
        // Set clothing
        if (appearance.clothing != null)
        {
            appearanceComp.SetClothing(appearance.clothing);
        }
        
        // Set accessories
        if (appearance.accessories != null)
        {
            appearanceComp.SetAccessories(appearance.accessories);
        }
    }
    
    private void SetupAIBehavior(GameObject character, OCDTrait[] traits)
    {
        // Add AI behavior component
        AIBehaviorComponent ai = character.AddComponent<AIBehaviorComponent>();
        
        // Configure behavior based on personality
        foreach (var trait in traits)
        {
            if (trait.name == "introversion-extraversion")
            {
                ai.SetSocialBehavior(trait.polarity > 0 ? SocialBehavior.Extroverted : SocialBehavior.Introverted);
            }
            else if (trait.name == "combat-readiness")
            {
                ai.SetCombatBehavior(trait.value > 0.7f ? CombatBehavior.Aggressive : 
                                   trait.value < 0.3f ? CombatBehavior.Defensive : CombatBehavior.Balanced);
            }
        }
    }
    
    private void SetupDialogueSystem(GameObject character, OCDCharacter ocdChar)
    {
        // Add dialogue component
        DialogueComponent dialogue = character.AddComponent<DialogueComponent>();
        
        // Set character name
        dialogue.SetCharacterName(ocdChar.names.canon);
        
        // Set personality traits for dialogue generation
        Dictionary<string, float> traits = new Dictionary<string, float>();
        foreach (var trait in ocdChar.personality.traits)
        {
            if (trait.kind == "bipolar")
            {
                traits[trait.name] = trait.polarity;
            }
            else
            {
                traits[trait.name] = trait.value;
            }
        }
        dialogue.SetPersonalityTraits(traits);
    }
}
```

## Personality Component System

### Core Personality Component

```csharp
public class PersonalityComponent : MonoBehaviour
{
    [Header("Personality Traits")]
    public float extraversion = 0f; // -1 to 1
    public float combatReadiness = 0.5f; // 0 to 1
    public float moralAlignment = 0.5f; // 0 to 1
    public float magicalAptitude = 0.5f; // 0 to 1
    public float natureConnection = 0.5f; // 0 to 1
    
    [Header("Behavior Settings")]
    public float socialRadius = 5f;
    public float combatAggression = 1f;
    public float moralThreshold = 0.3f;
    public float magicPower = 1f;
    public float natureAffinity = 1f;
    
    [Header("Visual Settings")]
    public Color auraColor = Color.white;
    public float auraIntensity = 1f;
    
    public void SetExtraversion(float value)
    {
        extraversion = Mathf.Clamp(value, -1f, 1f);
        UpdateSocialBehavior();
    }
    
    public void SetCombatReadiness(float value)
    {
        combatReadiness = Mathf.Clamp01(value);
        UpdateCombatBehavior();
    }
    
    public void SetMoralAlignment(float value)
    {
        moralAlignment = Mathf.Clamp01(value);
        UpdateMoralBehavior();
    }
    
    public void SetMagicalAptitude(float value)
    {
        magicalAptitude = Mathf.Clamp01(value);
        UpdateMagicalBehavior();
    }
    
    public void SetNatureConnection(float value)
    {
        natureConnection = Mathf.Clamp01(value);
        UpdateNatureBehavior();
    }
    
    private void UpdateSocialBehavior()
    {
        // Adjust social interaction radius based on extraversion
        socialRadius = 3f + (extraversion + 1f) * 2f; // 3-7 units
        
        // Adjust conversation frequency
        ConversationAI conversationAI = GetComponent<ConversationAI>();
        if (conversationAI != null)
        {
            conversationAI.SetTalkativeness(extraversion);
        }
    }
    
    private void UpdateCombatBehavior()
    {
        // Adjust combat aggression based on readiness
        combatAggression = combatReadiness * 2f;
        
        // Adjust weapon proficiency
        CombatAI combatAI = GetComponent<CombatAI>();
        if (combatAI != null)
        {
            combatAI.SetWeaponSkill(combatReadiness);
        }
    }
    
    private void UpdateMoralBehavior()
    {
        // Adjust moral decision making
        DecisionAI decisionAI = GetComponent<DecisionAI>();
        if (decisionAI != null)
        {
            decisionAI.SetMoralThreshold(moralThreshold);
        }
    }
    
    private void UpdateMagicalBehavior()
    {
        // Adjust magical power
        magicPower = magicalAptitude * 2f;
        
        // Update visual effects
        MagicalEffects magicalEffects = GetComponent<MagicalEffects>();
        if (magicalEffects != null)
        {
            magicalEffects.SetPowerLevel(magicalAptitude);
        }
    }
    
    private void UpdateNatureBehavior()
    {
        // Adjust nature affinity
        natureAffinity = natureConnection * 2f;
        
        // Update nature-related abilities
        NatureAbilities natureAbilities = GetComponent<NatureAbilities>();
        if (natureAbilities != null)
        {
            natureAbilities.SetAffinity(natureConnection);
        }
    }
}
```

## AI Behavior Integration

### Behavior Tree Component

```csharp
public class AIBehaviorComponent : MonoBehaviour
{
    [Header("Behavior Settings")]
    public SocialBehavior socialBehavior = SocialBehavior.Balanced;
    public CombatBehavior combatBehavior = CombatBehavior.Balanced;
    public MoralBehavior moralBehavior = MoralBehavior.Neutral;
    
    [Header("AI Components")]
    public BehaviorTree behaviorTree;
    public Blackboard blackboard;
    public AIController aiController;
    
    public void SetSocialBehavior(SocialBehavior behavior)
    {
        socialBehavior = behavior;
        UpdateBehaviorTree();
    }
    
    public void SetCombatBehavior(CombatBehavior behavior)
    {
        combatBehavior = behavior;
        UpdateBehaviorTree();
    }
    
    public void SetMoralBehavior(MoralBehavior behavior)
    {
        moralBehavior = behavior;
        UpdateBehaviorTree();
    }
    
    private void UpdateBehaviorTree()
    {
        if (behaviorTree != null && blackboard != null)
        {
            // Update blackboard values
            blackboard.SetValueAsEnum("SocialBehavior", socialBehavior);
            blackboard.SetValueAsEnum("CombatBehavior", combatBehavior);
            blackboard.SetValueAsEnum("MoralBehavior", moralBehavior);
            
            // Restart behavior tree with new values
            behaviorTree.Restart();
        }
    }
}

public enum SocialBehavior
{
    Introverted,
    Balanced,
    Extroverted
}

public enum CombatBehavior
{
    Defensive,
    Balanced,
    Aggressive
}

public enum MoralBehavior
{
    Villainous,
    Neutral,
    Heroic
}
```

## Dialogue System Integration

### Dialogue Component

```csharp
public class DialogueComponent : MonoBehaviour
{
    [Header("Character Info")]
    public string characterName;
    public Dictionary<string, float> personalityTraits = new Dictionary<string, float>();
    
    [Header("Dialogue Settings")]
    public float responseDelay = 1f;
    public float personalityInfluence = 1f;
    
    private DialogueGenerator dialogueGenerator;
    
    public void SetCharacterName(string name)
    {
        characterName = name;
    }
    
    public void SetPersonalityTraits(Dictionary<string, float> traits)
    {
        personalityTraits = traits;
        InitializeDialogueGenerator();
    }
    
    private void InitializeDialogueGenerator()
    {
        dialogueGenerator = new DialogueGenerator(characterName, personalityTraits);
    }
    
    public string GenerateResponse(string playerInput, DialogueContext context)
    {
        if (dialogueGenerator == null)
        {
            return "I don't know what to say...";
        }
        
        return dialogueGenerator.GenerateResponse(playerInput, context);
    }
    
    public string GetGreeting()
    {
        if (dialogueGenerator == null)
        {
            return "Hello there.";
        }
        
        return dialogueGenerator.GetGreeting();
    }
}

public class DialogueGenerator
{
    private string characterName;
    private Dictionary<string, float> personalityTraits;
    
    public DialogueGenerator(string name, Dictionary<string, float> traits)
    {
        characterName = name;
        personalityTraits = traits;
    }
    
    public string GenerateResponse(string playerInput, DialogueContext context)
    {
        // Analyze player input
        float inputSentiment = AnalyzeSentiment(playerInput);
        
        // Get character's current emotional state
        float emotionalState = CalculateEmotionalState(context);
        
        // Select response based on personality
        return SelectResponse(inputSentiment, emotionalState, context);
    }
    
    public string GetGreeting()
    {
        float extraversion = personalityTraits.GetValueOrDefault("introversion-extraversion", 0f);
        
        if (extraversion > 0.3f)
        {
            return "Hey there! Great to meet you!";
        }
        else if (extraversion < -0.3f)
        {
            return "Hello...";
        }
        else
        {
            return "Hello there.";
        }
    }
    
    private float AnalyzeSentiment(string input)
    {
        // Simple sentiment analysis - in production, use a proper NLP library
        string lowerInput = input.ToLower();
        
        if (lowerInput.Contains("good") || lowerInput.Contains("great") || lowerInput.Contains("awesome"))
            return 0.5f;
        else if (lowerInput.Contains("bad") || lowerInput.Contains("terrible") || lowerInput.Contains("awful"))
            return -0.5f;
        
        return 0f;
    }
    
    private float CalculateEmotionalState(DialogueContext context)
    {
        // Calculate emotional state based on context and personality
        float baseState = 0f;
        
        // Modify based on personality traits
        float extraversion = personalityTraits.GetValueOrDefault("introversion-extraversion", 0f);
        float moralAlignment = personalityTraits.GetValueOrDefault("moral-uprightness", 0.5f);
        
        return baseState + (extraversion * 0.3f) + (moralAlignment - 0.5f) * 0.2f;
    }
    
    private string SelectResponse(float inputSentiment, float emotionalState, DialogueContext context)
    {
        // Select response based on personality and context
        float extraversion = personalityTraits.GetValueOrDefault("introversion-extraversion", 0f);
        float moralAlignment = personalityTraits.GetValueOrDefault("moral-uprightness", 0.5f);
        
        if (extraversion > 0.3f)
        {
            if (moralAlignment > 0.7f)
                return "That's wonderful! I'm so glad to hear that!";
            else
                return "Interesting! Tell me more about that.";
        }
        else if (extraversion < -0.3f)
        {
            if (moralAlignment > 0.7f)
                return "I understand. That's quite noble of you.";
            else
                return "I see. That's... interesting.";
        }
        else
        {
            return "I understand. Thank you for sharing that with me.";
        }
    }
}

public class DialogueContext
{
    public string location;
    public string timeOfDay;
    public string relationship;
    public Dictionary<string, object> additionalContext;
}
```

## Visual Effects Integration

### Appearance Component

```csharp
public class AppearanceComponent : MonoBehaviour
{
    [Header("Physical Description")]
    public string[] physicalDescription;
    
    [Header("Clothing")]
    public string[] clothing;
    
    [Header("Accessories")]
    public string[] accessories;
    
    [Header("Visual Effects")]
    public ParticleSystem auraEffect;
    public Light characterLight;
    public Material characterMaterial;
    
    public void SetPhysicalDescription(string[] description)
    {
        physicalDescription = description;
        UpdateVisualAppearance();
    }
    
    public void SetClothing(string[] clothingItems)
    {
        clothing = clothingItems;
        UpdateClothing();
    }
    
    public void SetAccessories(string[] accessoryItems)
    {
        accessories = accessoryItems;
        UpdateAccessories();
    }
    
    private void UpdateVisualAppearance()
    {
        // Apply physical description to character model
        // This would typically involve modifying the character's 3D model
        // or applying different materials/textures
    }
    
    private void UpdateClothing()
    {
        // Apply clothing items to character
        // This would typically involve enabling/disabling clothing meshes
        // or changing clothing materials
    }
    
    private void UpdateAccessories()
    {
        // Apply accessories to character
        // This would typically involve enabling/disabling accessory meshes
    }
}
```

## Best Practices

### Performance Optimization

1. **Object Pooling**: Use object pooling for frequently created/destroyed character instances
2. **LOD System**: Implement Level of Detail for character rendering based on distance
3. **Caching**: Cache frequently accessed personality trait values
4. **Async Loading**: Load character data asynchronously to avoid frame drops

### Memory Management

1. **Dispose Resources**: Properly dispose of JSON parsing resources
2. **Unload Unused**: Unload character data when not needed
3. **Reference Management**: Use weak references where appropriate

### Testing

1. **Unit Tests**: Test individual personality trait applications
2. **Integration Tests**: Test complete character import pipeline
3. **Performance Tests**: Profile character import and behavior systems

!!! tip "Ready to Integrate?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
