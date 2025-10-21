# Interactive Storytelling Tools


Create dynamic, adaptive storytelling experiences with OCD-powered characters that drive narrative generation, branching storylines, and contextual dialogue systems.


OCD characters excel in interactive storytelling where personality-driven narratives create engaging, personalized experiences. This guide shows you how to build sophisticated storytelling systems that adapt narratives based on character personalities and player choices.

## Getting Started with Interactive Storytelling

### Prerequisites

- Storytelling engine or framework
- OCD character files in JSON format
- Understanding of narrative structures
- Basic knowledge of procedural generation

### Quick Setup

1. **Design Character Database**: Create rich OCD character profiles
2. **Set Up Story Engine**: Build narrative generation system
3. **Create Branching Logic**: Implement personality-driven story branches
4. **Test Story Generation**: Validate narrative consistency

## Dynamic Narrative Generation

### OCD Story Engine

```python
class OCDStoryEngine:
    def __init__(self, character_database):
        self.characters = character_database
        self.story_templates = self._load_story_templates()
        self.personality_effects = self._load_personality_effects()
        self.story_state = self._initialize_story_state()
        self.narrative_history = []
        self.relationship_network = self._build_relationship_network()
    
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
        
        # Update story state
        self._update_story_state(involved_characters, character_reactions, player_choice)
        
        # Store narrative history
        self.narrative_history.append({
            "scene": current_scene,
            "characters": involved_characters,
            "player_choice": player_choice,
            "character_reactions": character_reactions,
            "story_branch": story_branch,
            "timestamp": time.time()
        })
        
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
            
            elif traits.get("combat-readiness", 0.5) > 0.7:
                # Combat-ready characters
                if "fight" in player_choice.lower() or "attack" in player_choice.lower():
                    reactions[char_id] = "excitement"
                else:
                    reactions[char_id] = "neutral"
            
            else:
                # Default reaction
                reactions[char_id] = "neutral"
        
        return reactions
    
    def _generate_branch_from_reactions(self, current_scene: str, reactions: Dict[str, str], player_choice: str) -> str:
        """Generate story branch from character reactions"""
        # Get base story template
        story_template = self._select_story_template(current_scene, reactions)
        
        # Customize template based on character reactions
        customized_story = self._customize_story_template(story_template, reactions, player_choice)
        
        # Add character-specific dialogue
        character_dialogue = self._generate_character_dialogue(reactions)
        
        # Combine story and dialogue
        final_story = f"{customized_story}\n\n{character_dialogue}"
        
        return final_story
    
    def _select_story_template(self, current_scene: str, reactions: Dict[str, str]) -> str:
        """Select appropriate story template based on scene and reactions"""
        # Determine overall reaction tone
        positive_reactions = sum(1 for r in reactions.values() if r in ["approval", "enthusiasm", "excitement"])
        negative_reactions = sum(1 for r in reactions.values() if r in ["disapproval", "anger", "fear"])
        
        if positive_reactions > negative_reactions:
            tone = "positive"
        elif negative_reactions > positive_reactions:
            tone = "negative"
        else:
            tone = "neutral"
        
        # Select template based on scene and tone
        template_key = f"{current_scene}_{tone}"
        return self.story_templates.get(template_key, self.story_templates.get("default", "The story continues..."))
    
    def _customize_story_template(self, template: str, reactions: Dict[str, str], player_choice: str) -> str:
        """Customize story template based on character reactions"""
        customized = template
        
        # Replace placeholders with actual content
        customized = customized.replace("[player_choice]", player_choice)
        
        # Add character-specific reactions
        for char_id, reaction in reactions.items():
            if reaction == "approval":
                customized = customized.replace(f"[{char_id}_reaction]", f"{char_id} nods approvingly.")
            elif reaction == "disapproval":
                customized = customized.replace(f"[{char_id}_reaction]", f"{char_id} frowns disapprovingly.")
            elif reaction == "enthusiasm":
                customized = customized.replace(f"[{char_id}_reaction]", f"{char_id} seems excited by your choice.")
            elif reaction == "excitement":
                customized = customized.replace(f"[{char_id}_reaction]", f"{char_id} looks ready for action.")
            else:
                customized = customized.replace(f"[{char_id}_reaction]", f"{char_id} remains neutral.")
        
        return customized
    
    def _generate_character_dialogue(self, reactions: Dict[str, str]) -> str:
        """Generate character dialogue based on reactions"""
        dialogue_parts = []
        
        for char_id, reaction in reactions.items():
            character = self.characters.get(char_id)
            if character:
                dialogue = self._generate_character_specific_dialogue(character, reaction)
                if dialogue:
                    dialogue_parts.append(f"{char_id}: \"{dialogue}\"")
        
        return "\n".join(dialogue_parts)
    
    def _generate_character_specific_dialogue(self, character: Dict[str, Any], reaction: str) -> str:
        """Generate dialogue specific to a character's personality"""
        traits = self._extract_personality_traits(character)
        extraversion = traits.get("introversion-extraversion", 0)
        moral_alignment = traits.get("moral-uprightness", 0.5)
        combat_readiness = traits.get("combat-readiness", 0.5)
        
        if reaction == "approval":
            if moral_alignment > 0.7:
                return "That's the right thing to do. I'm proud of you."
            elif extraversion > 0.3:
                return "Great choice! I love your thinking!"
            else:
                return "I agree with that decision."
        
        elif reaction == "disapproval":
            if moral_alignment > 0.7:
                return "I can't support that. It's not right."
            elif extraversion > 0.3:
                return "I don't think that's a good idea, but it's your call."
            else:
                return "I'm not sure about that."
        
        elif reaction == "enthusiasm":
            if extraversion > 0.3:
                return "That sounds amazing! Let's do it!"
            else:
                return "That's quite interesting. I'd like to hear more."
        
        elif reaction == "excitement":
            if combat_readiness > 0.7:
                return "Finally! I was hoping for some action!"
            else:
                return "This is getting exciting!"
        
        else:
            return "I see. That's an option."
    
    def _update_story_state(self, involved_characters: List[str], reactions: Dict[str, str], player_choice: str):
        """Update story state based on current events"""
        # Update character relationships
        for char_id in involved_characters:
            if char_id not in self.story_state["character_states"]:
                self.story_state["character_states"][char_id] = {
                    "mood": "neutral",
                    "trust_level": 0.5,
                    "last_interaction": time.time()
                }
            
            # Update mood based on reaction
            reaction = reactions.get(char_id, "neutral")
            if reaction in ["approval", "enthusiasm", "excitement"]:
                self.story_state["character_states"][char_id]["mood"] = "positive"
            elif reaction in ["disapproval", "anger", "fear"]:
                self.story_state["character_states"][char_id]["mood"] = "negative"
            
            # Update trust level
            if reaction == "approval":
                self.story_state["character_states"][char_id]["trust_level"] = min(1.0, 
                    self.story_state["character_states"][char_id]["trust_level"] + 0.1)
            elif reaction == "disapproval":
                self.story_state["character_states"][char_id]["trust_level"] = max(0.0, 
                    self.story_state["character_states"][char_id]["trust_level"] - 0.1)
        
        # Update story progression
        self.story_state["current_scene"] = self._determine_next_scene(involved_characters, reactions)
        self.story_state["story_progression"] += 1
    
    def _determine_next_scene(self, involved_characters: List[str], reactions: Dict[str, str]) -> str:
        """Determine next scene based on current events"""
        # Simple scene progression logic
        current_scene = self.story_state.get("current_scene", "opening")
        
        # Check for major story events
        if any(reaction in ["disapproval", "anger"] for reaction in reactions.values()):
            return "conflict_scene"
        elif any(reaction in ["enthusiasm", "excitement"] for reaction in reactions.values()):
            return "action_scene"
        elif all(reaction == "approval" for reaction in reactions.values()):
            return "harmony_scene"
        else:
            return "neutral_scene"
    
    def _build_relationship_network(self) -> Dict[str, Dict[str, float]]:
        """Build relationship network between characters"""
        network = {}
        
        for char_id in self.characters:
            network[char_id] = {}
            for other_char_id in self.characters:
                if char_id != other_char_id:
                    # Initialize relationship based on character personalities
                    relationship = self._calculate_base_relationship(char_id, other_char_id)
                    network[char_id][other_char_id] = relationship
        
        return network
    
    def _calculate_base_relationship(self, char1_id: str, char2_id: str) -> float:
        """Calculate base relationship between two characters"""
        char1 = self.characters.get(char1_id)
        char2 = self.characters.get(char2_id)
        
        if not char1 or not char2:
            return 0.0
        
        char1_traits = self._extract_personality_traits(char1)
        char2_traits = self._extract_personality_traits(char2)
        
        # Calculate compatibility based on personality traits
        compatibility = 0.0
        
        # Extraversion compatibility
        extraversion1 = char1_traits.get("introversion-extraversion", 0)
        extraversion2 = char2_traits.get("introversion-extraversion", 0)
        compatibility += 1.0 - abs(extraversion1 - extraversion2) / 2.0
        
        # Moral alignment compatibility
        moral1 = char1_traits.get("moral-uprightness", 0.5)
        moral2 = char2_traits.get("moral-uprightness", 0.5)
        compatibility += 1.0 - abs(moral1 - moral2)
        
        # Combat readiness compatibility
        combat1 = char1_traits.get("combat-readiness", 0.5)
        combat2 = char2_traits.get("combat-readiness", 0.5)
        compatibility += 1.0 - abs(combat1 - combat2)
        
        return compatibility / 3.0  # Average compatibility
    
    def _initialize_story_state(self) -> Dict[str, Any]:
        """Initialize story state"""
        return {
            "current_scene": "opening",
            "story_progression": 0,
            "character_states": {},
            "world_state": {
                "time_of_day": "morning",
                "weather": "clear",
                "mood": "neutral"
            }
        }
    
    def _load_story_templates(self) -> Dict[str, str]:
        """Load story templates for different scenarios"""
        return {
            "opening_positive": "The story begins with hope and optimism. [player_choice] sets the tone for what's to come.",
            "opening_negative": "The story begins with tension and uncertainty. [player_choice] creates an ominous atmosphere.",
            "opening_neutral": "The story begins with a sense of normalcy. [player_choice] marks the first step in the journey.",
            "conflict_scene": "Tensions rise as [player_choice] creates conflict. [character_reactions]",
            "action_scene": "The pace quickens as [player_choice] leads to action. [character_reactions]",
            "harmony_scene": "The group works together as [player_choice] brings them closer. [character_reactions]",
            "neutral_scene": "The story continues as [player_choice] moves things forward. [character_reactions]",
            "default": "The story continues..."
        }
    
    def _load_personality_effects(self) -> Dict[str, Dict[str, str]]:
        """Load personality effects on story progression"""
        return {
            "heroic": {
                "combat": "fights with honor and courage",
                "social": "speaks with conviction and inspires others",
                "moral": "chooses the right path even when difficult"
            },
            "villainous": {
                "combat": "fights ruthlessly and efficiently",
                "social": "manipulates others for personal gain",
                "moral": "chooses the pragmatic path regardless of ethics"
            },
            "neutral": {
                "combat": "fights efficiently without unnecessary cruelty",
                "social": "speaks diplomatically and seeks compromise",
                "moral": "weighs all options before deciding"
            }
        }
    
    def _extract_personality_traits(self, character: Dict[str, Any]) -> Dict[str, float]:
        """Extract personality traits from character data"""
        traits = {}
        for trait in character.get("personality", {}).get("traits", []):
            if trait["kind"] == "bipolar":
                traits[trait["name"]] = trait["polarity"]
            else:
                traits[trait["name"]] = trait["value"]
        return traits
```

## Adaptive Dialogue System

### OCD Dialogue Engine

```python
class OCDDialogueEngine:
    def __init__(self, character_data):
        self.character = character_data
        self.personality_traits = self._extract_personality_traits()
        self.dialogue_history = []
        self.relationship_context = {}
        self.conversation_topics = self._initialize_conversation_topics()
        self.speech_patterns = self._initialize_speech_patterns()
    
    def generate_dialogue(self, speaker_id: str, listener_id: str, context: Dict[str, Any]) -> str:
        """Generate dialogue based on speaker's personality and relationship with listener"""
        # Get speaker's personality
        speaker_traits = self.personality_traits if speaker_id == self.character["id"] else self._get_other_character_traits(speaker_id)
        
        # Get relationship context
        relationship = self.relationship_context.get(listener_id, {"sentiment": 0.0, "familiarity": 0.0})
        
        # Generate dialogue based on personality and relationship
        dialogue = self._generate_personality_dialogue(speaker_traits, relationship, context)
        
        # Store dialogue in history
        self.dialogue_history.append({
            "speaker": speaker_id,
            "listener": listener_id,
            "dialogue": dialogue,
            "context": context,
            "timestamp": time.time()
        })
        
        return dialogue
    
    def _generate_personality_dialogue(self, traits: Dict[str, float], relationship: Dict[str, float], context: Dict[str, Any]) -> str:
        """Generate dialogue based on personality traits and relationship"""
        # Get base dialogue template
        template = self._select_dialogue_template(context)
        
        # Modify based on personality
        extraversion = traits.get("introversion-extraversion", 0)
        moral_alignment = traits.get("moral-uprightness", 0.5)
        combat_readiness = traits.get("combat-readiness", 0.5)
        
        # Apply personality modifications
        if extraversion > 0.3:
            template = self._make_dialogue_extraverted(template)
        elif extraversion < -0.3:
            template = self._make_dialogue_introverted(template)
        
        if moral_alignment > 0.7:
            template = self._make_dialogue_heroic(template)
        elif moral_alignment < 0.3:
            template = self._make_dialogue_villainous(template)
        
        # Apply relationship modifications
        sentiment = relationship.get("sentiment", 0.0)
        familiarity = relationship.get("familiarity", 0.0)
        
        if sentiment > 0.5:
            template = self._make_dialogue_friendly(template)
        elif sentiment < -0.5:
            template = self._make_dialogue_hostile(template)
        
        if familiarity > 0.7:
            template = self._make_dialogue_familiar(template)
        elif familiarity < 0.3:
            template = self._make_dialogue_formal(template)
        
        # Apply speech patterns
        template = self._apply_speech_patterns(template, traits)
        
        return template
    
    def _select_dialogue_template(self, context: Dict[str, Any]) -> str:
        """Select dialogue template based on context"""
        scene_type = context.get("scene_type", "general")
        emotional_tone = context.get("emotional_tone", "neutral")
        
        template_key = f"{scene_type}_{emotional_tone}"
        return self.conversation_topics.get(template_key, self.conversation_topics.get("general_neutral", "Hello there."))
    
    def _make_dialogue_extraverted(self, template: str) -> str:
        """Make dialogue more extraverted"""
        extraverted_modifications = {
            "Hello there.": "Hey there! Great to see you!",
            "I understand.": "That's fascinating! Tell me more!",
            "I see.": "Wow, that's really interesting!",
            "Thank you.": "Thanks so much! That's awesome!"
        }
        
        for original, modified in extraverted_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_introverted(self, template: str) -> str:
        """Make dialogue more introverted"""
        introverted_modifications = {
            "Hello there.": "Hello...",
            "I understand.": "I see. That's interesting.",
            "That's fascinating!": "That's... quite interesting.",
            "Thanks so much!": "Thank you."
        }
        
        for original, modified in introverted_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_heroic(self, template: str) -> str:
        """Make dialogue more heroic"""
        heroic_modifications = {
            "I understand.": "I understand. We must do what's right.",
            "That's interesting.": "That's interesting. I believe we can make a difference.",
            "Thank you.": "Thank you. Together we can overcome this."
        }
        
        for original, modified in heroic_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_villainous(self, template: str) -> str:
        """Make dialogue more villainous"""
        villainous_modifications = {
            "I understand.": "I understand. We must do what's necessary.",
            "That's interesting.": "That's interesting. How can we use this to our advantage?",
            "Thank you.": "Thank you. This will serve our purposes well."
        }
        
        for original, modified in villainous_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_friendly(self, template: str) -> str:
        """Make dialogue more friendly"""
        friendly_modifications = {
            "Hello there.": "Hello there, friend!",
            "I understand.": "I understand completely, my friend.",
            "Thank you.": "Thank you, my dear friend."
        }
        
        for original, modified in friendly_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_hostile(self, template: str) -> str:
        """Make dialogue more hostile"""
        hostile_modifications = {
            "Hello there.": "What do you want?",
            "I understand.": "I understand, but I don't care.",
            "Thank you.": "I don't need your thanks."
        }
        
        for original, modified in hostile_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_familiar(self, template: str) -> str:
        """Make dialogue more familiar"""
        familiar_modifications = {
            "Hello there.": "Hey!",
            "I understand.": "I get it.",
            "Thank you.": "Thanks!"
        }
        
        for original, modified in familiar_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _make_dialogue_formal(self, template: str) -> str:
        """Make dialogue more formal"""
        formal_modifications = {
            "Hey!": "Hello there.",
            "I get it.": "I understand.",
            "Thanks!": "Thank you."
        }
        
        for original, modified in formal_modifications.items():
            if original in template:
                template = template.replace(original, modified)
        
        return template
    
    def _apply_speech_patterns(self, template: str, traits: Dict[str, float]) -> str:
        """Apply character-specific speech patterns"""
        # Add character-specific speech quirks based on personality
        if traits.get("combat-readiness", 0) > 0.7:
            # Combat-ready characters might use more direct language
            template = template.replace("I think", "I know")
            template = template.replace("maybe", "definitely")
        
        if traits.get("magical-aptitude", 0) > 0.7:
            # Magical characters might use more mystical language
            template = template.replace("I understand", "I sense")
            template = template.replace("I see", "I perceive")
        
        if traits.get("nature-connection", 0) > 0.7:
            # Nature-connected characters might use more organic language
            template = template.replace("I understand", "I feel")
            template = template.replace("I see", "I sense")
        
        return template
    
    def _initialize_conversation_topics(self) -> Dict[str, str]:
        """Initialize conversation topics based on personality"""
        return {
            "general_neutral": "Hello there.",
            "general_positive": "What a wonderful day!",
            "general_negative": "This is concerning.",
            "combat_neutral": "I'm ready for action.",
            "combat_positive": "Let's show them what we're made of!",
            "combat_negative": "This is going to be dangerous.",
            "social_neutral": "How are you doing?",
            "social_positive": "It's great to see you!",
            "social_negative": "I'm not in the mood for conversation.",
            "moral_neutral": "We need to make a decision.",
            "moral_positive": "We must do what's right!",
            "moral_negative": "We need to be practical about this."
        }
    
    def _initialize_speech_patterns(self) -> Dict[str, str]:
        """Initialize speech patterns based on personality"""
        return {
            "greeting": "Hello there.",
            "agreement": "I understand.",
            "disagreement": "I don't think so.",
            "question": "What do you think?",
            "exclamation": "That's amazing!",
            "concern": "I'm worried about this."
        }
    
    def _get_other_character_traits(self, character_id: str) -> Dict[str, float]:
        """Get traits for other characters (placeholder for multi-character system)"""
        # This would be implemented to get traits from other characters
        return {}
    
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

## Story Branching System

### OCD Branch Generator

```python
class OCDBranchGenerator:
    def __init__(self, character_database):
        self.characters = character_database
        self.branch_templates = self._load_branch_templates()
        self.personality_effects = self._load_personality_effects()
        self.story_arcs = self._initialize_story_arcs()
    
    def generate_branch(self, current_scene: str, involved_characters: List[str], player_choice: str, story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate story branch with multiple possible outcomes"""
        # Analyze character personalities
        character_analysis = self._analyze_character_personalities(involved_characters)
        
        # Predict character reactions
        character_reactions = self._predict_character_reactions(involved_characters, player_choice, character_analysis)
        
        # Generate multiple possible outcomes
        outcomes = self._generate_outcomes(current_scene, character_reactions, player_choice, story_context)
        
        # Select best outcome based on story coherence
        best_outcome = self._select_best_outcome(outcomes, story_context)
        
        # Generate consequences
        consequences = self._generate_consequences(best_outcome, involved_characters, story_context)
        
        return {
            "outcome": best_outcome,
            "consequences": consequences,
            "character_reactions": character_reactions,
            "next_scene": self._determine_next_scene(best_outcome, story_context),
            "story_impact": self._calculate_story_impact(best_outcome, story_context)
        }
    
    def _generate_outcomes(self, current_scene: str, character_reactions: Dict[str, str], player_choice: str, story_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate multiple possible outcomes for the story branch"""
        outcomes = []
        
        # Generate positive outcome
        positive_outcome = self._generate_positive_outcome(current_scene, character_reactions, player_choice, story_context)
        outcomes.append(positive_outcome)
        
        # Generate negative outcome
        negative_outcome = self._generate_negative_outcome(current_scene, character_reactions, player_choice, story_context)
        outcomes.append(negative_outcome)
        
        # Generate neutral outcome
        neutral_outcome = self._generate_neutral_outcome(current_scene, character_reactions, player_choice, story_context)
        outcomes.append(neutral_outcome)
        
        # Generate unexpected outcome
        unexpected_outcome = self._generate_unexpected_outcome(current_scene, character_reactions, player_choice, story_context)
        outcomes.append(unexpected_outcome)
        
        return outcomes
    
    def _generate_positive_outcome(self, current_scene: str, character_reactions: Dict[str, str], player_choice: str, story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate positive outcome for the story branch"""
        return {
            "type": "positive",
            "description": f"Your choice to {player_choice} leads to a positive outcome. The characters react positively and the situation improves.",
            "character_impact": {char_id: "positive" for char_id in character_reactions.keys()},
            "story_progression": 1,
            "relationship_changes": {char_id: 0.1 for char_id in character_reactions.keys()},
            "probability": 0.3
        }
    
    def _generate_negative_outcome(self, current_scene: str, character_reactions: Dict[str, str], player_choice: str, story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate negative outcome for the story branch"""
        return {
            "type": "negative",
            "description": f"Your choice to {player_choice} leads to complications. The characters react negatively and the situation becomes more difficult.",
            "character_impact": {char_id: "negative" for char_id in character_reactions.keys()},
            "story_progression": 0.5,
            "relationship_changes": {char_id: -0.1 for char_id in character_reactions.keys()},
            "probability": 0.2
        }
    
    def _generate_neutral_outcome(self, current_scene: str, character_reactions: Dict[str, str], player_choice: str, story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate neutral outcome for the story branch"""
        return {
            "type": "neutral",
            "description": f"Your choice to {player_choice} leads to a neutral outcome. The characters react neutrally and the situation remains unchanged.",
            "character_impact": {char_id: "neutral" for char_id in character_reactions.keys()},
            "story_progression": 0.7,
            "relationship_changes": {char_id: 0.0 for char_id in character_reactions.keys()},
            "probability": 0.4
        }
    
    def _generate_unexpected_outcome(self, current_scene: str, character_reactions: Dict[str, str], player_choice: str, story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate unexpected outcome for the story branch"""
        return {
            "type": "unexpected",
            "description": f"Your choice to {player_choice} leads to an unexpected turn of events. The characters react with surprise and the situation takes an unexpected direction.",
            "character_impact": {char_id: "surprised" for char_id in character_reactions.keys()},
            "story_progression": 1.5,
            "relationship_changes": {char_id: 0.05 for char_id in character_reactions.keys()},
            "probability": 0.1
        }
    
    def _select_best_outcome(self, outcomes: List[Dict[str, Any]], story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Select the best outcome based on story coherence and character personalities"""
        # Weight outcomes based on story context and character personalities
        weighted_outcomes = []
        
        for outcome in outcomes:
            weight = outcome["probability"]
            
            # Adjust weight based on story context
            if story_context.get("tone") == "positive" and outcome["type"] == "positive":
                weight *= 1.5
            elif story_context.get("tone") == "negative" and outcome["type"] == "negative":
                weight *= 1.5
            elif story_context.get("tone") == "neutral" and outcome["type"] == "neutral":
                weight *= 1.5
            
            # Adjust weight based on story progression needs
            if story_context.get("needs_progression") and outcome["story_progression"] > 1:
                weight *= 1.3
            
            weighted_outcomes.append((outcome, weight))
        
        # Select outcome based on weighted probability
        total_weight = sum(weight for _, weight in weighted_outcomes)
        random_value = random.random() * total_weight
        
        current_weight = 0
        for outcome, weight in weighted_outcomes:
            current_weight += weight
            if random_value <= current_weight:
                return outcome
        
        return outcomes[0]  # Fallback to first outcome
    
    def _generate_consequences(self, outcome: Dict[str, Any], involved_characters: List[str], story_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consequences of the chosen outcome"""
        consequences = {
            "immediate": [],
            "long_term": [],
            "character_development": {},
            "world_changes": []
        }
        
        # Generate immediate consequences
        if outcome["type"] == "positive":
            consequences["immediate"].append("The situation improves immediately.")
            consequences["immediate"].append("Characters feel more confident.")
        elif outcome["type"] == "negative":
            consequences["immediate"].append("The situation becomes more difficult.")
            consequences["immediate"].append("Characters feel more stressed.")
        elif outcome["type"] == "unexpected":
            consequences["immediate"].append("The situation takes an unexpected turn.")
            consequences["immediate"].append("Characters are surprised by the development.")
        
        # Generate long-term consequences
        if outcome["story_progression"] > 1:
            consequences["long_term"].append("The story progresses significantly.")
        elif outcome["story_progression"] < 0.5:
            consequences["long_term"].append("The story progression is slowed.")
        
        # Generate character development consequences
        for char_id in involved_characters:
            impact = outcome["character_impact"].get(char_id, "neutral")
            if impact == "positive":
                consequences["character_development"][char_id] = "Character grows and develops positively."
            elif impact == "negative":
                consequences["character_development"][char_id] = "Character faces challenges and grows through adversity."
            elif impact == "surprised":
                consequences["character_development"][char_id] = "Character learns something new about themselves."
        
        return consequences
    
    def _determine_next_scene(self, outcome: Dict[str, Any], story_context: Dict[str, Any]) -> str:
        """Determine next scene based on outcome"""
        if outcome["type"] == "positive":
            return "success_scene"
        elif outcome["type"] == "negative":
            return "challenge_scene"
        elif outcome["type"] == "unexpected":
            return "twist_scene"
        else:
            return "continuation_scene"
    
    def _calculate_story_impact(self, outcome: Dict[str, Any], story_context: Dict[str, Any]) -> float:
        """Calculate overall impact of the outcome on the story"""
        base_impact = outcome["story_progression"]
        
        # Adjust based on outcome type
        if outcome["type"] == "unexpected":
            base_impact *= 1.5
        elif outcome["type"] == "negative":
            base_impact *= 0.8
        
        # Adjust based on story context
        if story_context.get("critical_moment"):
            base_impact *= 2.0
        
        return min(3.0, base_impact)  # Cap at 3.0
    
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
                if "lie" in player_choice.lower() or "deceive" in player_choice.lower():
                    reactions[char_id] = "disapproval"
                elif "help" in player_choice.lower() or "save" in player_choice.lower():
                    reactions[char_id] = "approval"
                else:
                    reactions[char_id] = "neutral"
            elif traits.get("introversion-extraversion", 0) > 0.3:
                if "social" in player_choice.lower() or "talk" in player_choice.lower():
                    reactions[char_id] = "enthusiasm"
                else:
                    reactions[char_id] = "neutral"
            else:
                reactions[char_id] = "neutral"
        
        return reactions
    
    def _load_branch_templates(self) -> Dict[str, str]:
        """Load branch templates for different scenarios"""
        return {
            "positive_outcome": "Your choice leads to a positive outcome...",
            "negative_outcome": "Your choice leads to complications...",
            "neutral_outcome": "Your choice leads to a neutral outcome...",
            "unexpected_outcome": "Your choice leads to an unexpected turn of events..."
        }
    
    def _load_personality_effects(self) -> Dict[str, Dict[str, str]]:
        """Load personality effects on story progression"""
        return {
            "heroic": {
                "positive": "The heroic choice leads to inspiration and hope.",
                "negative": "The heroic choice leads to sacrifice and hardship.",
                "neutral": "The heroic choice leads to moral clarity.",
                "unexpected": "The heroic choice leads to unexpected allies."
            },
            "villainous": {
                "positive": "The villainous choice leads to power and control.",
                "negative": "The villainous choice leads to isolation and mistrust.",
                "neutral": "The villainous choice leads to calculated advantage.",
                "unexpected": "The villainous choice leads to unexpected consequences."
            },
            "neutral": {
                "positive": "The neutral choice leads to stability and balance.",
                "negative": "The neutral choice leads to missed opportunities.",
                "neutral": "The neutral choice leads to maintaining the status quo.",
                "unexpected": "The neutral choice leads to unexpected revelations."
            }
        }
    
    def _initialize_story_arcs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize story arcs for different character types"""
        return {
            "heroic_arc": {
                "beginning": "The hero's journey begins with a call to adventure.",
                "middle": "The hero faces trials and tribulations.",
                "end": "The hero achieves victory through courage and sacrifice."
            },
            "villainous_arc": {
                "beginning": "The villain's path begins with a desire for power.",
                "middle": "The villain manipulates and schemes.",
                "end": "The villain either achieves their goals or faces downfall."
            },
            "neutral_arc": {
                "beginning": "The neutral character begins with a balanced perspective.",
                "middle": "The neutral character navigates complex situations.",
                "end": "The neutral character finds their own path."
            }
        }
    
    def _extract_personality_traits(self, character: Dict[str, Any]) -> Dict[str, float]:
        """Extract personality traits from character data"""
        traits = {}
        for trait in character.get("personality", {}).get("traits", []):
            if trait["kind"] == "bipolar":
                traits[trait["name"]] = trait["polarity"]
            else:
                traits[trait["name"]] = trait["value"]
        return traits
```

## Best Practices

### Story Coherence

1. **Character Consistency**: Maintain consistent character personalities throughout the story
2. **Plot Logic**: Ensure story branches follow logical progression
3. **Relationship Dynamics**: Track and maintain character relationships
4. **World Building**: Keep world state consistent across story branches

### Performance Optimization

1. **Template Caching**: Cache frequently used story templates
2. **Character Analysis**: Pre-analyze character personalities
3. **Branch Pruning**: Remove unlikely story branches early
4. **Memory Management**: Efficiently manage story state and history

### User Experience

1. **Meaningful Choices**: Ensure player choices have significant impact
2. **Character Feedback**: Provide clear character reactions to choices
3. **Story Pacing**: Maintain appropriate story pacing
4. **Emotional Impact**: Create meaningful emotional moments

### Testing and Validation

1. **Story Testing**: Test story branches for coherence and interest
2. **Character Testing**: Validate character consistency
3. **Choice Testing**: Test that choices lead to meaningful outcomes
4. **Performance Testing**: Ensure story generation is efficient

!!! tip "Ready to Create Interactive Stories?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
