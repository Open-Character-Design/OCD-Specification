# Visual Novels & RPG Systems


Create immersive visual novels and RPG experiences with OCD-powered characters that drive personality-based dialogue trees, expression systems, and emotional state management.


OCD characters excel in visual novel and RPG contexts where personality-driven interactions are crucial. This guide shows you how to build sophisticated dialogue systems, expression management, and character progression systems using OCD character data.

## Getting Started with Visual Novels

### Prerequisites

- Visual novel engine (Ren'Py, Unity, Godot, or custom)
- OCD character files in JSON format
- Basic understanding of dialogue systems
- Familiarity with character progression mechanics

### Quick Setup

1. **Design Character Profiles**: Create rich OCD character profiles
2. **Set Up Dialogue Systems**: Integrate personality-driven dialogue
3. **Build Expression Systems**: Connect emotions to character expressions
4. **Test Branching Narratives**: Use OCD to drive story decisions

## Dialogue System Integration

### Personality-Driven Dialogue Engine

```python
class OCDDialogueSystem:
    def __init__(self, character_data):
        self.character = character_data
        self.personality_traits = self._extract_personality_traits()
        self.dialogue_options = self._load_dialogue_templates()
        self.emotional_state = self._initialize_emotional_state()
        self.relationship_memory = {}
    
    def generate_dialogue_response(self, player_input: str, context: Dict[str, Any]) -> str:
        """Generate character response based on personality and context"""
        # Analyze player input sentiment
        input_sentiment = self._analyze_sentiment(player_input)
        
        # Get character's current emotional state
        current_emotional_state = self._calculate_emotional_state(context)
        
        # Select appropriate dialogue template
        dialogue_template = self._select_dialogue_template(
            input_sentiment, current_emotional_state, context
        )
        
        # Customize dialogue based on personality
        customized_dialogue = self._customize_dialogue(dialogue_template, context)
        
        # Update emotional state based on interaction
        self._update_emotional_state(input_sentiment, context)
        
        return customized_dialogue
    
    def _extract_personality_traits(self) -> Dict[str, float]:
        """Extract personality traits from OCD character data"""
        traits = {}
        for trait in self.character.get("personality", {}).get("traits", []):
            if trait["kind"] == "bipolar":
                traits[trait["name"]] = trait["polarity"]
            else:
                traits[trait["name"]] = trait["value"]
        return traits
    
    def _analyze_sentiment(self, input_text: str) -> float:
        """Analyze sentiment of player input"""
        # Simple sentiment analysis - in production, use a proper NLP library
        positive_words = ["good", "great", "awesome", "wonderful", "amazing", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible"]
        
        input_lower = input_text.lower()
        positive_count = sum(1 for word in positive_words if word in input_lower)
        negative_count = sum(1 for word in negative_words if word in input_lower)
        
        if positive_count > negative_count:
            return 0.5
        elif negative_count > positive_count:
            return -0.5
        else:
            return 0.0
    
    def _calculate_emotional_state(self, context: Dict[str, Any]) -> str:
        """Calculate current emotional state based on context and personality"""
        base_state = "neutral"
        
        # Modify based on personality traits
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        combat_readiness = self.personality_traits.get("combat-readiness", 0.5)
        
        # Context-based modifications
        if context.get("in_combat", False):
            if combat_readiness > 0.7:
                base_state = "excited"
            elif combat_readiness < 0.3:
                base_state = "fearful"
            else:
                base_state = "focused"
        elif context.get("social_interaction", False):
            if extraversion > 0.3:
                base_state = "cheerful"
            elif extraversion < -0.3:
                base_state = "reserved"
            else:
                base_state = "neutral"
        elif context.get("moral_decision", False):
            if moral_alignment > 0.7:
                base_state = "determined"
            elif moral_alignment < 0.3:
                base_state = "calculating"
            else:
                base_state = "thoughtful"
        
        return base_state
    
    def _select_dialogue_template(self, input_sentiment: float, emotional_state: str, context: Dict[str, Any]) -> str:
        """Select dialogue template based on personality and context"""
        # Get character's extraversion level
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        
        # Get character's moral alignment
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        
        # Select template based on personality and emotional state
        if emotional_state == "excited":
            if extraversion > 0.3:
                template = self.dialogue_options["extraverted_excited"]
            else:
                template = self.dialogue_options["introverted_excited"]
        elif emotional_state == "fearful":
            if moral_alignment > 0.7:
                template = self.dialogue_options["heroic_fearful"]
            else:
                template = self.dialogue_options["neutral_fearful"]
        elif emotional_state == "cheerful":
            if extraversion > 0.3:
                template = self.dialogue_options["extraverted_cheerful"]
            else:
                template = self.dialogue_options["introverted_cheerful"]
        else:
            # Default to personality-based selection
            if extraversion > 0.3:
                if moral_alignment > 0.7:
                    template = self.dialogue_options["extraverted_heroic"]
                else:
                    template = self.dialogue_options["extraverted_neutral"]
            else:
                if moral_alignment > 0.7:
                    template = self.dialogue_options["introverted_heroic"]
                else:
                    template = self.dialogue_options["introverted_neutral"]
        
        return template
    
    def _customize_dialogue(self, template: str, context: Dict[str, Any]) -> str:
        """Customize dialogue based on specific personality traits"""
        customized = template
        
        # Apply character-specific speech patterns
        combat_readiness = self.personality_traits.get("combat-readiness", 0)
        if combat_readiness > 0.8:
            customized = customized.replace("[greeting]", "Ready for action!")
            customized = customized.replace("[response]", "Let's do this!")
        else:
            customized = customized.replace("[greeting]", "Hello there.")
            customized = customized.replace("[response]", "I understand.")
        
        # Apply extraversion-based modifications
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        if extraversion > 0.5:
            customized = customized.replace("[enthusiasm]", "That's fascinating! Tell me more!")
            customized = customized.replace("[agreement]", "Absolutely! I completely agree!")
        elif extraversion < -0.5:
            customized = customized.replace("[enthusiasm]", "I see. That's interesting.")
            customized = customized.replace("[agreement]", "I suppose so.")
        else:
            customized = customized.replace("[enthusiasm]", "That's quite interesting.")
            customized = customized.replace("[agreement]", "I agree.")
        
        # Apply moral alignment modifications
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        if moral_alignment > 0.7:
            customized = customized.replace("[moral_choice]", "We must do what's right!")
            customized = customized.replace("[disapproval]", "I cannot condone such actions.")
        elif moral_alignment < 0.3:
            customized = customized.replace("[moral_choice]", "We must do what's necessary.")
            customized = customized.replace("[disapproval]", "That's not very practical.")
        else:
            customized = customized.replace("[moral_choice]", "We must consider all options.")
            customized = customized.replace("[disapproval]", "I'm not sure about that.")
        
        return customized
    
    def _update_emotional_state(self, input_sentiment: float, context: Dict[str, Any]):
        """Update character's emotional state based on interaction"""
        # Simple emotional state tracking
        if input_sentiment > 0.3:
            self.emotional_state["happiness"] = min(1.0, self.emotional_state.get("happiness", 0.5) + 0.1)
        elif input_sentiment < -0.3:
            self.emotional_state["happiness"] = max(0.0, self.emotional_state.get("happiness", 0.5) - 0.1)
        
        # Update relationship memory
        if "player_id" in context:
            player_id = context["player_id"]
            if player_id not in self.relationship_memory:
                self.relationship_memory[player_id] = {"sentiment": 0.0, "familiarity": 0.0}
            
            self.relationship_memory[player_id]["sentiment"] += input_sentiment * 0.1
            self.relationship_memory[player_id]["familiarity"] += 0.05
    
    def _initialize_emotional_state(self) -> Dict[str, float]:
        """Initialize character's emotional state"""
        return {
            "happiness": 0.5,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
            "sadness": 0.0
        }
    
    def _load_dialogue_templates(self) -> Dict[str, str]:
        """Load dialogue templates for different personality combinations"""
        return {
            "extraverted_heroic": "[greeting] [enthusiasm] [moral_choice]",
            "extraverted_neutral": "[greeting] [enthusiasm] [agreement]",
            "introverted_heroic": "[greeting] [moral_choice] I believe we can make a difference.",
            "introverted_neutral": "[greeting] [agreement] I understand your perspective.",
            "extraverted_excited": "This is amazing! [enthusiasm] Let's go!",
            "introverted_excited": "This is... quite exciting. I'm ready.",
            "heroic_fearful": "I'm afraid, but we must be brave. [moral_choice]",
            "neutral_fearful": "This is concerning. We should be careful.",
            "extraverted_cheerful": "What a wonderful day! [enthusiasm]",
            "introverted_cheerful": "It's nice to see you. [agreement]"
        }
```

## Expression System Integration

### OCD Expression System

```python
class OCDExpressionSystem:
    def __init__(self, character_data):
        self.character = character_data
        self.expression_mapping = self._load_expression_mapping()
        self.personality_traits = self._extract_personality_traits()
        self.current_expression = "neutral"
        self.expression_history = []
    
    def get_expression_for_emotion(self, emotion: str, intensity: float) -> str:
        """Get character expression based on emotion and personality"""
        # Get base expression
        base_expression = self.expression_mapping.get(emotion, "neutral")
        
        # Modify based on personality
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        combat_readiness = self.personality_traits.get("combat-readiness", 0.5)
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        
        # Extraverted characters show more exaggerated expressions
        if extraversion > 0.3:
            intensity *= 1.2
        
        # Combat-ready characters have more intense expressions
        if combat_readiness > 0.8:
            intensity *= 1.1
        
        # High moral characters show more determined expressions
        if moral_alignment > 0.7:
            intensity *= 1.05
        
        # Select appropriate expression variant
        expression_variant = self._select_expression_variant(base_expression, intensity)
        
        # Update current expression
        self.current_expression = expression_variant
        self.expression_history.append({
            "expression": expression_variant,
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": time.time()
        })
        
        return expression_variant
    
    def _select_expression_variant(self, base_expression: str, intensity: float) -> str:
        """Select expression variant based on intensity"""
        if intensity > 0.8:
            return f"{base_expression}_intense"
        elif intensity > 0.5:
            return f"{base_expression}_moderate"
        else:
            return f"{base_expression}_subtle"
    
    def get_expression_for_dialogue(self, dialogue_text: str, context: Dict[str, Any]) -> str:
        """Get expression based on dialogue content and context"""
        # Analyze dialogue sentiment
        sentiment = self._analyze_dialogue_sentiment(dialogue_text)
        
        # Determine emotion from context
        emotion = self._determine_emotion_from_context(context)
        
        # Calculate intensity based on personality and context
        intensity = self._calculate_expression_intensity(sentiment, emotion, context)
        
        return self.get_expression_for_emotion(emotion, intensity)
    
    def _analyze_dialogue_sentiment(self, dialogue_text: str) -> float:
        """Analyze sentiment of dialogue text"""
        positive_words = ["good", "great", "wonderful", "amazing", "love", "happy", "excited"]
        negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "fearful"]
        
        dialogue_lower = dialogue_text.lower()
        positive_count = sum(1 for word in positive_words if word in dialogue_lower)
        negative_count = sum(1 for word in negative_words if word in dialogue_lower)
        
        if positive_count > negative_count:
            return 0.5
        elif negative_count > positive_count:
            return -0.5
        else:
            return 0.0
    
    def _determine_emotion_from_context(self, context: Dict[str, Any]) -> str:
        """Determine emotion from context"""
        if context.get("in_combat", False):
            return "determined"
        elif context.get("romantic_scene", False):
            return "happy"
        elif context.get("sad_scene", False):
            return "sad"
        elif context.get("tense_scene", False):
            return "worried"
        else:
            return "neutral"
    
    def _calculate_expression_intensity(self, sentiment: float, emotion: str, context: Dict[str, Any]) -> float:
        """Calculate expression intensity based on personality and context"""
        base_intensity = abs(sentiment)
        
        # Modify based on personality
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        if extraversion > 0.3:
            base_intensity *= 1.2
        elif extraversion < -0.3:
            base_intensity *= 0.8
        
        # Modify based on context
        if context.get("important_scene", False):
            base_intensity *= 1.3
        
        return min(1.0, base_intensity)
    
    def _load_expression_mapping(self) -> Dict[str, str]:
        """Load expression mapping for different emotions"""
        return {
            "happy": "smile",
            "sad": "frown",
            "angry": "scowl",
            "surprised": "wide_eyes",
            "fearful": "worried",
            "determined": "focused",
            "confused": "puzzled",
            "excited": "grin",
            "worried": "concerned",
            "neutral": "calm"
        }
    
    def _extract_personality_traits(self) -> Dict[str, float]:
        """Extract personality traits from OCD character data"""
        traits = {}
        for trait in self.character.get("personality", {}).get("traits", []):
            if trait["kind"] == "bipolar":
                traits[trait["name"]] = trait["polarity"]
            else:
                traits[trait["name"]] = trait["value"]
        return traits
```

## RPG Character Progression

### OCD RPG Character System

```python
class OCDRPGCharacter:
    def __init__(self, ocd_character_data):
        self.ocd_data = ocd_character_data
        self.stats = self._generate_stats_from_traits()
        self.skills = self._generate_skills_from_traits()
        self.abilities = self._generate_abilities_from_traits()
        self.level = 1
        self.experience = 0
        self.character_class = self._determine_character_class()
    
    def _generate_stats_from_traits(self) -> Dict[str, int]:
        """Generate RPG stats from OCD personality traits"""
        stats = {}
        
        # Map personality traits to RPG stats
        trait_mapping = {
            "combat-readiness": "strength",
            "introversion-extraversion": "charisma",
            "magical-aptitude": "intelligence",
            "nature-connection": "wisdom",
            "agility": "dexterity",
            "endurance": "constitution"
        }
        
        for trait in self.ocd_data.get("personality", {}).get("traits", []):
            trait_name = trait["name"]
            trait_value = trait.get("value", trait.get("polarity", 0))
            
            if trait_name in trait_mapping:
                stat_name = trait_mapping[trait_name]
                # Convert trait value (0-1 or -1 to 1) to RPG stat (1-20)
                if trait["kind"] == "bipolar":
                    # Bipolar traits: -1 to 1 -> 1 to 20
                    stats[stat_name] = int((trait_value + 1) * 9.5 + 1)
                else:
                    # Scalar traits: 0 to 1 -> 1 to 20
                    stats[stat_name] = int(trait_value * 19 + 1)
        
        return stats
    
    def _generate_skills_from_traits(self) -> Dict[str, int]:
        """Generate skills based on personality traits"""
        skills = {}
        
        # Map traits to skills
        skill_mapping = {
            "combat-readiness": ["sword_fighting", "archery", "tactics", "leadership"],
            "magical-aptitude": ["spellcasting", "magic_research", "enchanting", "rituals"],
            "nature-connection": ["survival", "animal_handling", "herbalism", "tracking"],
            "introversion-extraversion": ["persuasion", "intimidation", "deception", "performance"],
            "moral-uprightness": ["healing", "protection", "justice", "diplomacy"],
            "agility": ["stealth", "acrobatics", "thievery", "reflexes"]
        }
        
        for trait in self.ocd_data.get("personality", {}).get("traits", []):
            trait_name = trait["name"]
            trait_value = trait.get("value", abs(trait.get("polarity", 0)))
            
            if trait_name in skill_mapping:
                for skill in skill_mapping[trait_name]:
                    # Convert trait value to skill level (0-100)
                    skills[skill] = int(trait_value * 100)
        
        return skills
    
    def _generate_abilities_from_traits(self) -> List[str]:
        """Generate special abilities based on personality traits"""
        abilities = []
        
        for trait in self.ocd_data.get("personality", {}).get("traits", []):
            trait_name = trait["name"]
            trait_value = trait.get("value", abs(trait.get("polarity", 0)))
            
            if trait_name == "combat-readiness" and trait_value > 0.7:
                abilities.append("Berserker Rage")
                abilities.append("Weapon Mastery")
            elif trait_name == "magical-aptitude" and trait_value > 0.7:
                abilities.append("Spell Mastery")
                abilities.append("Mana Efficiency")
            elif trait_name == "nature-connection" and trait_value > 0.7:
                abilities.append("Animal Companion")
                abilities.append("Nature's Blessing")
            elif trait_name == "introversion-extraversion" and trait_value > 0.5:
                abilities.append("Inspire Allies")
                abilities.append("Leadership")
            elif trait_name == "moral-uprightness" and trait_value > 0.7:
                abilities.append("Divine Protection")
                abilities.append("Healing Touch")
        
        return abilities
    
    def _determine_character_class(self) -> str:
        """Determine character class based on dominant traits"""
        trait_scores = {}
        
        for trait in self.ocd_data.get("personality", {}).get("traits", []):
            trait_name = trait["name"]
            trait_value = trait.get("value", abs(trait.get("polarity", 0)))
            trait_scores[trait_name] = trait_value
        
        # Determine class based on highest scoring traits
        if trait_scores.get("combat-readiness", 0) > 0.7:
            return "Warrior"
        elif trait_scores.get("magical-aptitude", 0) > 0.7:
            return "Mage"
        elif trait_scores.get("nature-connection", 0) > 0.7:
            return "Druid"
        elif trait_scores.get("introversion-extraversion", 0) > 0.5:
            return "Bard"
        elif trait_scores.get("moral-uprightness", 0) > 0.7:
            return "Paladin"
        else:
            return "Adventurer"
    
    def level_up(self):
        """Level up the character"""
        self.level += 1
        self._improve_stats()
        self._improve_skills()
        self._learn_new_abilities()
    
    def _improve_stats(self):
        """Improve stats on level up"""
        for stat in self.stats:
            # Small random improvement
            improvement = random.randint(0, 2)
            self.stats[stat] = min(20, self.stats[stat] + improvement)
    
    def _improve_skills(self):
        """Improve skills on level up"""
        for skill in self.skills:
            # Small random improvement
            improvement = random.randint(0, 5)
            self.skills[skill] = min(100, self.skills[skill] + improvement)
    
    def _learn_new_abilities(self):
        """Learn new abilities on level up"""
        # Chance to learn new ability based on level
        if random.random() < 0.3:  # 30% chance
            new_ability = self._generate_random_ability()
            if new_ability and new_ability not in self.abilities:
                self.abilities.append(new_ability)
    
    def _generate_random_ability(self) -> str:
        """Generate a random ability based on character traits"""
        # This would be expanded with a proper ability generation system
        ability_templates = [
            "Enhanced {stat}",
            "Improved {skill}",
            "Special {trait} ability"
        ]
        return random.choice(ability_templates)
```

## Branching Narrative System

### OCD Story Branch Generator

```python
class OCDStoryBranchGenerator:
    def __init__(self, character_database):
        self.characters = character_database
        self.story_templates = self._load_story_templates()
        self.personality_effects = self._load_personality_effects()
    
    def generate_story_branch(self, current_scene: str, involved_characters: List[str], player_choice: str) -> str:
        """Generate next story branch based on character personalities and player choice"""
        # Analyze involved characters' personalities
        character_analysis = self._analyze_character_personalities(involved_characters)
        
        # Determine how characters would react to player choice
        character_reactions = self._predict_character_reactions(
            involved_characters, player_choice, character_analysis
        )
        
        # Generate story branch based on reactions
        story_branch = self._generate_branch_from_reactions(
            current_scene, character_reactions, player_choice
        )
        
        return story_branch
    
    def _analyze_character_personalities(self, character_ids: List[str]) -> Dict[str, Dict[str, float]]:
        """Analyze personality traits of involved characters"""
        analysis = {}
        
        for char_id in character_ids:
            character = self.characters.get(char_id)
            if character:
                traits = self._extract_personality_traits(character)
                analysis[char_id] = traits
        
        return analysis
    
    def _predict_character_reactions(self, character_ids: List[str], player_choice: str, analysis: Dict[str, Dict[str, float]]) -> Dict[str, str]:
        """Predict how each character would react to player choice"""
        reactions = {}
        
        for char_id in character_ids:
            traits = analysis.get(char_id, {})
            
            # Predict reaction based on personality
            if traits.get("moral-uprightness", 0.5) > 0.7:
                # High moral characters
                if "lie" in player_choice.lower() or "deceive" in player_choice.lower():
                    reactions[char_id] = "disapproval"
                elif "help" in player_choice.lower() or "save" in player_choice.lower():
                    reactions[char_id] = "approval"
                else:
                    reactions[char_id] = "neutral"
            
            elif traits.get("introversion-extraversion", 0) > 0.3:
                # Extraverted characters
                if "social" in player_choice.lower() or "talk" in player_choice.lower():
                    reactions[char_id] = "enthusiasm"
                else:
                    reactions[char_id] = "neutral"
            
            else:
                # Default reaction
                reactions[char_id] = "neutral"
        
        return reactions
    
    def _generate_branch_from_reactions(self, current_scene: str, reactions: Dict[str, str], player_choice: str) -> str:
        """Generate story branch from character reactions"""
        # This would be expanded with a proper story generation system
        branch_template = f"Based on your choice to {player_choice}, "
        
        # Add character reactions
        for char_id, reaction in reactions.items():
            if reaction == "approval":
                branch_template += f"{char_id} nods approvingly. "
            elif reaction == "disapproval":
                branch_template += f"{char_id} frowns disapprovingly. "
            elif reaction == "enthusiasm":
                branch_template += f"{char_id} seems excited by your choice. "
            else:
                branch_template += f"{char_id} remains neutral. "
        
        return branch_template
    
    def _extract_personality_traits(self, character: Dict[str, Any]) -> Dict[str, float]:
        """Extract personality traits from character data"""
        traits = {}
        for trait in character.get("personality", {}).get("traits", []):
            if trait["kind"] == "bipolar":
                traits[trait["name"]] = trait["polarity"]
            else:
                traits[trait["name"]] = trait["value"]
        return traits
    
    def _load_story_templates(self) -> Dict[str, str]:
        """Load story templates for different scenarios"""
        return {
            "combat_scene": "The battle begins...",
            "social_scene": "The conversation continues...",
            "moral_choice": "A difficult decision must be made...",
            "romance_scene": "The moment becomes intimate...",
            "mystery_scene": "The plot thickens..."
        }
    
    def _load_personality_effects(self) -> Dict[str, Dict[str, str]]:
        """Load personality effects on story progression"""
        return {
            "heroic": {
                "combat": "fights with honor",
                "social": "speaks with conviction",
                "moral": "chooses the right path"
            },
            "villainous": {
                "combat": "fights ruthlessly",
                "social": "manipulates others",
                "moral": "chooses the pragmatic path"
            },
            "neutral": {
                "combat": "fights efficiently",
                "social": "speaks diplomatically",
                "moral": "weighs all options"
            }
        }
```

## Best Practices

### Performance Optimization

1. **Dialogue Caching**: Cache frequently used dialogue templates
2. **Expression Preloading**: Preload character expressions
3. **Memory Management**: Efficiently manage character data
4. **Lazy Loading**: Load character data only when needed

### Character Consistency

1. **Trait Validation**: Validate personality traits regularly
2. **Dialogue Consistency**: Ensure dialogue matches character personality
3. **Expression Coherence**: Maintain expression consistency
4. **Story Continuity**: Track character development over time

### User Experience

1. **Clear Choices**: Make player choices clear and meaningful
2. **Character Feedback**: Provide clear character reactions
3. **Story Pacing**: Maintain appropriate story pacing
4. **Emotional Impact**: Create meaningful emotional moments

!!! tip "Ready to Create Visual Novels?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
