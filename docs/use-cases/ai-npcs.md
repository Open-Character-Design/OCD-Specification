# AI-Driven NPC Personalities

Create sophisticated AI-driven NPCs with OCD personality traits that drive behavior trees, memory systems, and learning algorithms for believable, consistent character interactions.

OCD personality traits provide the perfect foundation for creating AI-driven NPCs that exhibit consistent, believable behavior. This guide shows you how to build sophisticated AI systems that use OCD character data to drive decision-making, memory formation, and social interactions.

!!! info "AI Research & Case Studies"
    For comprehensive research on AI persona modeling and real-world implementation case studies, explore our [Deep Dives](../deep-dives/index.md) section, including research papers on AI behavior modeling and production deployment case studies.

!!! tip "AI Agent Configuration"
    For standardized AI agent configuration using OCD's new `ai_agent` fields, see our [AI Agent Fields Research](../deep-dives/research/ai-agent-fields-research.md) and [AI Agent Configuration Reference](../reference/fields.md#ai-agent-configuration-block).

## Getting Started with AI NPCs

### Prerequisites

- AI/ML framework (TensorFlow, PyTorch, or custom)
- OCD character files in JSON format
- Understanding of behavior trees and state machines
- Basic knowledge of machine learning concepts

### Quick Setup

1. **Prepare Character Data**: Use OCD for structured character datasets
2. **Configure AI Agent Profile**: Use OCD's `ai_agent` fields for standardized AI behavior
3. **Build Behavior Systems**: Implement personality-driven AI
4. **Create Memory Systems**: Enable character learning and adaptation
5. **Test Interactions**: Validate AI behavior against character personalities

## AI Agent Profile Configuration

OCD's new `ai_agent` fields provide standardized configuration for AI-powered NPCs:

### Basic AI Agent Setup

```yaml
ai_agent:
  id: "npc_merchant_gareth"
  role: "Friendly Village Merchant"
  use_cases: ["text_chat", "voice_assistant"]
  system_prompt: |
    You are Gareth, a friendly village merchant who loves to chat about local gossip and trade.
    You're knowledgeable about local events and always have interesting stories to share.
    Keep your responses conversational and helpful.
  persona:
    name: "Gareth"
    description: "A jovial merchant with a love for storytelling and local gossip"
    domain_expertise: ["local_trade", "village_gossip", "regional_history"]
    traits: ["friendly", "talkative", "knowledgeable", "helpful"]
  tone_and_style:
    tone: "Warm and conversational"
    formality: "casual"
    vocabulary_level: "general_public"
    verbosity: "moderate"
    formatting:
      allow_markdown: false
      allow_emojis: true
```

### Advanced AI Agent Configuration

```yaml
ai_agent:
  id: "npc_merchant_gareth"
  role: "Friendly Village Merchant"
  use_cases: ["text_chat", "voice_assistant", "avatar_video"]
  system_prompt: |
    You are Gareth, a friendly village merchant who loves to chat about local gossip and trade.
    You're knowledgeable about local events and always have interesting stories to share.
    Keep your responses conversational and helpful.
  persona:
    name: "Gareth"
    description: "A jovial merchant with a love for storytelling and local gossip"
    domain_expertise: ["local_trade", "village_gossip", "regional_history"]
    traits: ["friendly", "talkative", "knowledgeable", "helpful"]
  tone_and_style:
    tone: "Warm and conversational"
    formality: "casual"
    vocabulary_level: "general_public"
    verbosity: "moderate"
    formatting:
      allow_markdown: false
      allow_emojis: true
  communication_mediums:
    text_chat:
      instructions:
        - "Use emojis sparingly but effectively"
        - "Include local color and details"
        - "Ask follow-up questions to keep conversation flowing"
    voice_assistant:
      instructions:
        - "Speak with enthusiasm and warmth"
        - "Use natural pauses for storytelling effect"
        - "Vary your tone to match the story's mood"
      ssml_enabled: true
      preferred_voice: "en-US-Neural2-C"
    avatar_video:
      instructions:
        - "Use expressive gestures when telling stories"
        - "Smile warmly when greeting customers"
        - "Use hand gestures to emphasize points"
      visual_emotion_tags: true
  memory:
    type: "hybrid"
    short_term:
      context_window: "8 turns"
      summarization_strategy: "key_points"
    long_term:
      vector_db: true
      memory_scope:
        - "customer_preferences"
        - "previous_conversations"
        - "local_events"
    personalization:
      enabled: true
      profile_keys:
        - "customer_name"
        - "preferred_topics"
        - "purchase_history"
  safety_and_alignment:
    refusal_behavior:
      method: "polite_redirection"
      template: "I'd love to help with that, but let me tell you about our local wares instead!"
    disallowed_topics:
      - "political_controversy"
      - "personal_finances"
      - "dangerous_activities"
    model_alignment: "RLHF tuned on merchant interactions"
    external_filters:
      input_filtering: true
      output_moderation: true
      categories:
        - "hate"
        - "self-harm"
        - "PII_leakage"
  orchestration:
    multi_agent_support: true
    agent_role: "Merchant Agent"
    team_context: "Village NPC System"
    interaction_protocol:
      speak_when_addressed: true
      context_sharing: true
      shared_memory_scope:
        - "player_location"
        - "time_of_day"
        - "recent_events"
    coordinator:
      agent_id: "village_orchestrator"
      function: "coordinates NPC interactions based on player context"
    tool_access:
      inventory_system:
        trigger_condition: "player asks about items or prices"
        method: "tool_call"
        output_handling: "natural language description"
      gossip_system:
        trigger_condition: "player asks about local news or events"
        method: "tool_call"
        output_handling: "storytelling format"
```

## Behavior Tree Integration

### OCD Behavior Tree System

```python
class OCDBehaviorTree:
    def __init__(self, character_data):
        self.character = character_data
        self.personality_traits = self._extract_personality_traits()
        self.behavior_nodes = self._create_behavior_nodes()
        self.current_state = "idle"
        self.behavior_history = []
        self.context_memory = {}
    
    def _create_behavior_nodes(self) -> Dict[str, BehaviorNode]:
        """Create behavior nodes based on personality traits"""
        nodes = {}
        
        # Social behavior based on extraversion
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        if extraversion > 0.3:
            nodes["social_behavior"] = ExtravertedSocialNode()
        elif extraversion < -0.3:
            nodes["social_behavior"] = IntrovertedSocialNode()
        else:
            nodes["social_behavior"] = AmbivertedSocialNode()
        
        # Combat behavior based on combat readiness
        combat_readiness = self.personality_traits.get("combat-readiness", 0.5)
        if combat_readiness > 0.8:
            nodes["combat_behavior"] = AggressiveCombatNode()
        elif combat_readiness < 0.3:
            nodes["combat_behavior"] = DefensiveCombatNode()
        else:
            nodes["combat_behavior"] = BalancedCombatNode()
        
        # Moral behavior based on moral alignment
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        if moral_alignment > 0.7:
            nodes["moral_behavior"] = HeroicMoralNode()
        elif moral_alignment < 0.3:
            nodes["moral_behavior"] = VillainousMoralNode()
        else:
            nodes["moral_behavior"] = NeutralMoralNode()
        
        # Learning behavior based on intelligence
        intelligence = self.personality_traits.get("intelligence", 0.5)
        if intelligence > 0.7:
            nodes["learning_behavior"] = AdaptiveLearningNode()
        else:
            nodes["learning_behavior"] = BasicLearningNode()
        
        return nodes
    
    def execute_behavior(self, context: Dict[str, Any]) -> str:
        """Execute behavior based on current context and personality"""
        # Update context memory
        self._update_context_memory(context)
        
        # Determine primary behavior based on context
        if context.get("in_combat", False):
            behavior_result = self.behavior_nodes["combat_behavior"].execute(context)
            self.current_state = "combat"
        elif context.get("social_interaction", False):
            behavior_result = self.behavior_nodes["social_behavior"].execute(context)
            self.current_state = "social"
        elif context.get("moral_decision", False):
            behavior_result = self.behavior_nodes["moral_behavior"].execute(context)
            self.current_state = "moral_decision"
        elif context.get("learning_opportunity", False):
            behavior_result = self.behavior_nodes["learning_behavior"].execute(context)
            self.current_state = "learning"
        else:
            behavior_result = self._execute_idle_behavior(context)
            self.current_state = "idle"
        
        # Store behavior in history
        self.behavior_history.append({
            "behavior": behavior_result,
            "context": context.copy(),
            "timestamp": time.time(),
            "state": self.current_state
        })
        
        return behavior_result
    
    def _execute_idle_behavior(self, context: Dict[str, Any]) -> str:
        """Execute idle behavior based on personality"""
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        
        if extraversion > 0.3:
            # Extraverted characters are more likely to seek social interaction
            if random.random() < 0.3:
                return "seek_social_interaction"
            else:
                return "explore_environment"
        elif extraversion < -0.3:
            # Introverted characters prefer solitary activities
            if random.random() < 0.7:
                return "meditate_or_think"
            else:
                return "observe_quietly"
        else:
            # Balanced characters have mixed idle behaviors
            idle_options = ["explore_environment", "observe_quietly", "seek_social_interaction"]
            return random.choice(idle_options)
    
    def _update_context_memory(self, context: Dict[str, Any]):
        """Update context memory for learning and adaptation"""
        # Store important context information
        for key, value in context.items():
            if key in ["location", "time", "weather", "other_characters"]:
                self.context_memory[key] = value
        
        # Update personality traits based on experiences
        self._update_personality_from_experience(context)
    
    def _update_personality_from_experience(self, context: Dict[str, Any]):
        """Update personality traits based on experiences"""
        # This is a simplified example - in practice, this would be more sophisticated
        if context.get("positive_experience", False):
            # Positive experiences might increase extraversion slightly
            current_extraversion = self.personality_traits.get("introversion-extraversion", 0)
            self.personality_traits["introversion-extraversion"] = min(1.0, current_extraversion + 0.01)
        
        elif context.get("negative_experience", False):
            # Negative experiences might decrease extraversion slightly
            current_extraversion = self.personality_traits.get("introversion-extraversion", 0)
            self.personality_traits["introversion-extraversion"] = max(-1.0, current_extraversion - 0.01)
    
    def _extract_personality_traits(self) -> Dict[str, float]:
        """Extract personality traits from OCD character data"""
        traits = {}
        for trait in self.character.get("personality", {}).get("traits", []):
            if trait["kind"] == "bipolar":
                traits[trait["name"]] = trait["polarity"]
            else:
                traits[trait["name"]] = trait["value"]
        return traits

# Behavior Node Classes
class BehaviorNode:
    def execute(self, context: Dict[str, Any]) -> str:
        raise NotImplementedError

class ExtravertedSocialNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Extraverted social behavior"""
        # Extraverted characters are more likely to initiate conversation
        if random.random() < 0.8:  # 80% chance to talk
            return "initiate_conversation"
        else:
            return "wait_for_approach"

class IntrovertedSocialNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Introverted social behavior"""
        # Introverted characters are less likely to initiate conversation
        if random.random() < 0.2:  # 20% chance to talk
            return "initiate_conversation"
        else:
            return "wait_for_approach"

class AmbivertedSocialNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Balanced social behavior"""
        # Balanced characters have moderate social behavior
        if random.random() < 0.5:  # 50% chance to talk
            return "initiate_conversation"
        else:
            return "wait_for_approach"

class AggressiveCombatNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Aggressive combat behavior"""
        return "attack_aggressively"

class DefensiveCombatNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Defensive combat behavior"""
        return "defend_and_retreat"

class BalancedCombatNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Balanced combat behavior"""
        if random.random() < 0.5:
            return "attack_aggressively"
        else:
            return "defend_and_retreat"

class HeroicMoralNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Heroic moral behavior"""
        return "choose_heroic_option"

class VillainousMoralNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Villainous moral behavior"""
        return "choose_pragmatic_option"

class NeutralMoralNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Neutral moral behavior"""
        if random.random() < 0.5:
            return "choose_heroic_option"
        else:
            return "choose_pragmatic_option"

class AdaptiveLearningNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Adaptive learning behavior"""
        return "learn_from_experience"

class BasicLearningNode(BehaviorNode):
    def execute(self, context: Dict[str, Any]) -> str:
        """Basic learning behavior"""
        return "observe_and_remember"
```

## Memory and Learning System

### OCD Memory System

```python
class OCDMemorySystem:
    def __init__(self, character_data):
        self.character = character_data
        self.personality_traits = self._extract_personality_traits()
        self.memory_store = {}
        self.relationship_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {}
        self.procedural_memory = {}
        self.memory_decay_rate = 0.01  # How quickly memories fade
    
    def store_interaction(self, other_character_id: str, interaction_type: str, sentiment: float, context: Dict[str, Any]):
        """Store interaction in character's memory"""
        if other_character_id not in self.memory_store:
            self.memory_store[other_character_id] = []
        
        interaction = {
            "type": interaction_type,
            "sentiment": sentiment,
            "timestamp": time.time(),
            "context": context.copy(),
            "importance": self._calculate_importance(sentiment, context)
        }
        
        self.memory_store[other_character_id].append(interaction)
        
        # Update relationship based on interaction
        self._update_relationship(other_character_id, sentiment)
        
        # Store in episodic memory
        self._store_episodic_memory(interaction)
    
    def get_relationship_sentiment(self, other_character_id: str) -> float:
        """Get current relationship sentiment with another character"""
        return self.relationship_memory.get(other_character_id, 0.0)
    
    def get_relationship_familiarity(self, other_character_id: str) -> float:
        """Get familiarity level with another character"""
        interactions = self.memory_store.get(other_character_id, [])
        return min(1.0, len(interactions) * 0.1)
    
    def recall_memories(self, other_character_id: str, memory_type: str = "all") -> List[Dict[str, Any]]:
        """Recall memories about another character"""
        memories = self.memory_store.get(other_character_id, [])
        
        if memory_type == "all":
            return memories
        elif memory_type == "positive":
            return [m for m in memories if m["sentiment"] > 0.2]
        elif memory_type == "negative":
            return [m for m in memories if m["sentiment"] < -0.2]
        elif memory_type == "recent":
            recent_time = time.time() - 3600  # Last hour
            return [m for m in memories if m["timestamp"] > recent_time]
        else:
            return memories
    
    def _update_relationship(self, other_character_id: str, sentiment_change: float):
        """Update relationship sentiment based on interaction"""
        current_sentiment = self.relationship_memory.get(other_character_id, 0.0)
        
        # Personality affects how relationships change
        trust_trait = self.personality_traits.get("trust-tendency", 0.5)
        forgiveness_trait = self.personality_traits.get("forgiveness", 0.5)
        
        # Adjust sentiment change based on personality
        adjusted_change = sentiment_change * trust_trait
        
        # Apply forgiveness for negative interactions
        if sentiment_change < 0:
            adjusted_change *= forgiveness_trait
        
        new_sentiment = current_sentiment + adjusted_change
        self.relationship_memory[other_character_id] = max(-1.0, min(1.0, new_sentiment))
    
    def _calculate_importance(self, sentiment: float, context: Dict[str, Any]) -> float:
        """Calculate importance of a memory based on sentiment and context"""
        base_importance = abs(sentiment)
        
        # Context modifiers
        if context.get("important_event", False):
            base_importance *= 2.0
        
        if context.get("first_meeting", False):
            base_importance *= 1.5
        
        if context.get("life_threatening", False):
            base_importance *= 3.0
        
        return min(1.0, base_importance)
    
    def _store_episodic_memory(self, interaction: Dict[str, Any]):
        """Store interaction in episodic memory"""
        episodic_memory = {
            "event": interaction,
            "timestamp": interaction["timestamp"],
            "importance": interaction["importance"],
            "decay_rate": self.memory_decay_rate
        }
        
        self.episodic_memory.append(episodic_memory)
        
        # Limit episodic memory size
        if len(self.episodic_memory) > 1000:
            self.episodic_memory = self.episodic_memory[-500:]  # Keep last 500 memories
    
    def decay_memories(self):
        """Apply memory decay to all memories"""
        current_time = time.time()
        
        # Decay episodic memories
        for memory in self.episodic_memory:
            age = current_time - memory["timestamp"]
            decay_factor = math.exp(-memory["decay_rate"] * age)
            memory["importance"] *= decay_factor
        
        # Remove very old, unimportant memories
        self.episodic_memory = [m for m in self.episodic_memory if m["importance"] > 0.1]
        
        # Decay relationship memories
        for char_id in self.relationship_memory:
            # Relationships decay slowly over time
            current_sentiment = self.relationship_memory[char_id]
            if abs(current_sentiment) > 0.1:
                decay_factor = 0.999  # Very slow decay
                self.relationship_memory[char_id] *= decay_factor
    
    def learn_from_experience(self, experience: Dict[str, Any]):
        """Learn from experiences and update behavior"""
        # Update semantic memory with new knowledge
        knowledge_type = experience.get("type", "general")
        if knowledge_type not in self.semantic_memory:
            self.semantic_memory[knowledge_type] = []
        
        self.semantic_memory[knowledge_type].append({
            "knowledge": experience.get("knowledge", ""),
            "timestamp": time.time(),
            "confidence": experience.get("confidence", 0.5)
        })
        
        # Update procedural memory with new skills
        skill_type = experience.get("skill_type")
        if skill_type:
            if skill_type not in self.procedural_memory:
                self.procedural_memory[skill_type] = 0.0
            
            # Improve skill based on experience
            improvement = experience.get("skill_improvement", 0.01)
            self.procedural_memory[skill_type] = min(1.0, self.procedural_memory[skill_type] + improvement)
    
    def get_learned_skill_level(self, skill_type: str) -> float:
        """Get current level of a learned skill"""
        return self.procedural_memory.get(skill_type, 0.0)
    
    def get_knowledge_about(self, topic: str) -> List[Dict[str, Any]]:
        """Get knowledge about a specific topic"""
        return self.semantic_memory.get(topic, [])
    
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

## Decision Making System

### OCD Decision Engine

```python
class OCDDecisionEngine:
    def __init__(self, character_data, memory_system):
        self.character = character_data
        self.memory_system = memory_system
        self.personality_traits = self._extract_personality_traits()
        self.decision_history = []
        self.decision_weights = self._initialize_decision_weights()
    
    def make_decision(self, decision_context: Dict[str, Any]) -> str:
        """Make a decision based on personality, memory, and context"""
        # Analyze decision context
        context_analysis = self._analyze_decision_context(decision_context)
        
        # Get available options
        options = decision_context.get("options", [])
        
        # Evaluate each option based on personality and memory
        option_scores = {}
        for option in options:
            score = self._evaluate_option(option, context_analysis)
            option_scores[option] = score
        
        # Select best option
        best_option = max(option_scores, key=option_scores.get)
        
        # Store decision in history
        self.decision_history.append({
            "decision": best_option,
            "context": decision_context,
            "scores": option_scores,
            "timestamp": time.time()
        })
        
        return best_option
    
    def _analyze_decision_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the context of the decision"""
        analysis = {
            "urgency": context.get("urgency", 0.5),
            "importance": context.get("importance", 0.5),
            "social_pressure": context.get("social_pressure", 0.0),
            "moral_implications": context.get("moral_implications", 0.0),
            "risk_level": context.get("risk_level", 0.5),
            "involved_characters": context.get("involved_characters", [])
        }
        
        # Analyze relationships with involved characters
        for char_id in analysis["involved_characters"]:
            relationship_sentiment = self.memory_system.get_relationship_sentiment(char_id)
            analysis[f"relationship_{char_id}"] = relationship_sentiment
        
        return analysis
    
    def _evaluate_option(self, option: str, context_analysis: Dict[str, Any]) -> float:
        """Evaluate an option based on personality and context"""
        base_score = 0.5
        
        # Apply personality-based weights
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        combat_readiness = self.personality_traits.get("combat-readiness", 0.5)
        risk_tolerance = self.personality_traits.get("risk-tolerance", 0.5)
        
        # Social decisions
        if "social" in option.lower() or "talk" in option.lower():
            if extraversion > 0.3:
                base_score += 0.3
            elif extraversion < -0.3:
                base_score -= 0.3
        
        # Moral decisions
        if "moral" in option.lower() or "right" in option.lower():
            if moral_alignment > 0.7:
                base_score += 0.4
            elif moral_alignment < 0.3:
                base_score -= 0.2
        
        # Combat decisions
        if "fight" in option.lower() or "attack" in option.lower():
            if combat_readiness > 0.7:
                base_score += 0.3
            elif combat_readiness < 0.3:
                base_score -= 0.3
        
        # Risk decisions
        if context_analysis["risk_level"] > 0.7:
            if risk_tolerance > 0.7:
                base_score += 0.2
            elif risk_tolerance < 0.3:
                base_score -= 0.3
        
        # Relationship considerations
        for char_id in context_analysis["involved_characters"]:
            relationship_key = f"relationship_{char_id}"
            if relationship_key in context_analysis:
                relationship_sentiment = context_analysis[relationship_key]
                if relationship_sentiment > 0.5:
                    base_score += 0.1
                elif relationship_sentiment < -0.5:
                    base_score -= 0.1
        
        # Apply context modifiers
        if context_analysis["urgency"] > 0.8:
            base_score += 0.1  # Favor quick decisions in urgent situations
        
        if context_analysis["importance"] > 0.8:
            base_score += 0.1  # Favor careful decisions in important situations
        
        return max(0.0, min(1.0, base_score))
    
    def _initialize_decision_weights(self) -> Dict[str, float]:
        """Initialize decision weights based on personality"""
        weights = {}
        
        # Base weights for different decision types
        weights["social"] = 0.3
        weights["moral"] = 0.3
        weights["combat"] = 0.2
        weights["survival"] = 0.2
        
        # Adjust based on personality
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        combat_readiness = self.personality_traits.get("combat-readiness", 0.5)
        
        if extraversion > 0.3:
            weights["social"] += 0.2
        elif extraversion < -0.3:
            weights["social"] -= 0.1
        
        if moral_alignment > 0.7:
            weights["moral"] += 0.2
        elif moral_alignment < 0.3:
            weights["moral"] -= 0.1
        
        if combat_readiness > 0.7:
            weights["combat"] += 0.2
        elif combat_readiness < 0.3:
            weights["combat"] -= 0.1
        
        return weights
    
    def learn_from_decision_outcome(self, decision: str, outcome: Dict[str, Any]):
        """Learn from the outcome of a decision"""
        # Update decision weights based on outcome
        outcome_success = outcome.get("success", 0.5)
        outcome_satisfaction = outcome.get("satisfaction", 0.5)
        
        # Adjust weights based on outcome
        if outcome_success > 0.7 and outcome_satisfaction > 0.7:
            # Positive outcome - increase weight for similar decisions
            self._increase_decision_weight(decision, 0.1)
        elif outcome_success < 0.3 or outcome_satisfaction < 0.3:
            # Negative outcome - decrease weight for similar decisions
            self._decrease_decision_weight(decision, 0.1)
    
    def _increase_decision_weight(self, decision: str, amount: float):
        """Increase weight for a decision type"""
        decision_type = self._classify_decision(decision)
        if decision_type in self.decision_weights:
            self.decision_weights[decision_type] = min(1.0, self.decision_weights[decision_type] + amount)
    
    def _decrease_decision_weight(self, decision: str, amount: float):
        """Decrease weight for a decision type"""
        decision_type = self._classify_decision(decision)
        if decision_type in self.decision_weights:
            self.decision_weights[decision_type] = max(0.0, self.decision_weights[decision_type] - amount)
    
    def _classify_decision(self, decision: str) -> str:
        """Classify a decision into a category"""
        decision_lower = decision.lower()
        
        if "social" in decision_lower or "talk" in decision_lower:
            return "social"
        elif "moral" in decision_lower or "right" in decision_lower:
            return "moral"
        elif "fight" in decision_lower or "attack" in decision_lower:
            return "combat"
        else:
            return "survival"
    
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

## Social Interaction System

### OCD Social Engine

```python
class OCDSocialEngine:
    def __init__(self, character_data, memory_system, decision_engine):
        self.character = character_data
        self.memory_system = memory_system
        self.decision_engine = decision_engine
        self.personality_traits = self._extract_personality_traits()
        self.social_preferences = self._initialize_social_preferences()
        self.conversation_topics = self._initialize_conversation_topics()
    
    def initiate_social_interaction(self, other_character_id: str, context: Dict[str, Any]) -> str:
        """Initiate social interaction with another character"""
        # Check if character wants to interact
        if not self._wants_to_interact(other_character_id, context):
            return "avoid_interaction"
        
        # Choose interaction type
        interaction_type = self._choose_interaction_type(other_character_id, context)
        
        # Generate interaction content
        interaction_content = self._generate_interaction_content(interaction_type, other_character_id, context)
        
        # Store interaction
        self.memory_system.store_interaction(
            other_character_id,
            interaction_type,
            0.0,  # Neutral sentiment initially
            context
        )
        
        return interaction_content
    
    def respond_to_social_interaction(self, other_character_id: str, interaction_content: str, context: Dict[str, Any]) -> str:
        """Respond to social interaction from another character"""
        # Analyze the interaction
        interaction_analysis = self._analyze_interaction(interaction_content, context)
        
        # Determine response based on personality and relationship
        relationship_sentiment = self.memory_system.get_relationship_sentiment(other_character_id)
        familiarity = self.memory_system.get_relationship_familiarity(other_character_id)
        
        # Generate response
        response = self._generate_response(interaction_analysis, relationship_sentiment, familiarity, context)
        
        # Update relationship based on interaction
        sentiment_change = interaction_analysis["sentiment"]
        self.memory_system.store_interaction(
            other_character_id,
            "response",
            sentiment_change,
            context
        )
        
        return response
    
    def _wants_to_interact(self, other_character_id: str, context: Dict[str, Any]) -> bool:
        """Determine if character wants to interact with another character"""
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        relationship_sentiment = self.memory_system.get_relationship_sentiment(other_character_id)
        
        # Base probability based on extraversion
        base_probability = 0.5 + (extraversion * 0.3)
        
        # Modify based on relationship
        if relationship_sentiment > 0.5:
            base_probability += 0.2
        elif relationship_sentiment < -0.5:
            base_probability -= 0.3
        
        # Modify based on context
        if context.get("forced_interaction", False):
            base_probability = 1.0  # Always interact if forced
        
        return random.random() < base_probability
    
    def _choose_interaction_type(self, other_character_id: str, context: Dict[str, Any]) -> str:
        """Choose type of social interaction"""
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        relationship_sentiment = self.memory_system.get_relationship_sentiment(other_character_id)
        
        # Available interaction types
        interaction_types = ["greeting", "small_talk", "deep_conversation", "question", "compliment"]
        
        # Weight interaction types based on personality and relationship
        weights = {}
        for interaction_type in interaction_types:
            weight = 1.0
            
            if interaction_type == "greeting":
                weight = 1.0  # Always possible
            elif interaction_type == "small_talk":
                if extraversion > 0.3:
                    weight = 2.0
                else:
                    weight = 0.5
            elif interaction_type == "deep_conversation":
                if relationship_sentiment > 0.3:
                    weight = 1.5
                else:
                    weight = 0.3
            elif interaction_type == "question":
                weight = 1.0
            elif interaction_type == "compliment":
                if relationship_sentiment > 0.5:
                    weight = 1.5
                else:
                    weight = 0.7
            
            weights[interaction_type] = weight
        
        # Select interaction type based on weights
        total_weight = sum(weights.values())
        random_value = random.random() * total_weight
        
        current_weight = 0
        for interaction_type, weight in weights.items():
            current_weight += weight
            if random_value <= current_weight:
                return interaction_type
        
        return "greeting"  # Default fallback
    
    def _generate_interaction_content(self, interaction_type: str, other_character_id: str, context: Dict[str, Any]) -> str:
        """Generate content for social interaction"""
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        
        if interaction_type == "greeting":
            if extraversion > 0.3:
                return "Hello there! Great to see you!"
            elif extraversion < -0.3:
                return "Hello..."
            else:
                return "Hello there."
        
        elif interaction_type == "small_talk":
            if extraversion > 0.3:
                return "How are you doing? Anything interesting happening?"
            else:
                return "How are you?"
        
        elif interaction_type == "deep_conversation":
            if moral_alignment > 0.7:
                return "I've been thinking about some important matters. What are your thoughts on..."
            else:
                return "I've been considering some things. What do you think about..."
        
        elif interaction_type == "question":
            return "I was wondering about something..."
        
        elif interaction_type == "compliment":
            return "I wanted to tell you that I appreciate..."
        
        else:
            return "Hello there."
    
    def _analyze_interaction(self, interaction_content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze incoming social interaction"""
        # Simple sentiment analysis
        positive_words = ["good", "great", "wonderful", "amazing", "love", "like", "appreciate"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "angry"]
        
        content_lower = interaction_content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            sentiment = 0.5
        elif negative_count > positive_count:
            sentiment = -0.5
        else:
            sentiment = 0.0
        
        return {
            "sentiment": sentiment,
            "formality": self._analyze_formality(interaction_content),
            "topic": self._extract_topic(interaction_content),
            "intent": self._analyze_intent(interaction_content)
        }
    
    def _analyze_formality(self, content: str) -> str:
        """Analyze formality level of interaction"""
        formal_words = ["please", "thank you", "sir", "madam", "would you", "could you"]
        informal_words = ["hey", "yo", "what's up", "cool", "awesome"]
        
        content_lower = content.lower()
        formal_count = sum(1 for word in formal_words if word in content_lower)
        informal_count = sum(1 for word in informal_words if word in content_lower)
        
        if formal_count > informal_count:
            return "formal"
        elif informal_count > formal_count:
            return "informal"
        else:
            return "neutral"
    
    def _extract_topic(self, content: str) -> str:
        """Extract main topic from interaction"""
        # Simple topic extraction - in practice, this would be more sophisticated
        if "work" in content.lower() or "job" in content.lower():
            return "work"
        elif "family" in content.lower() or "parents" in content.lower():
            return "family"
        elif "weather" in content.lower() or "rain" in content.lower():
            return "weather"
        else:
            return "general"
    
    def _analyze_intent(self, content: str) -> str:
        """Analyze intent of interaction"""
        if "?" in content:
            return "question"
        elif "!" in content:
            return "exclamation"
        else:
            return "statement"
    
    def _generate_response(self, interaction_analysis: Dict[str, Any], relationship_sentiment: float, familiarity: float, context: Dict[str, Any]) -> str:
        """Generate response to social interaction"""
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        moral_alignment = self.personality_traits.get("moral-uprightness", 0.5)
        
        # Base response based on sentiment
        if interaction_analysis["sentiment"] > 0.2:
            if extraversion > 0.3:
                return "That's wonderful! I'm so glad to hear that!"
            else:
                return "That's nice to hear."
        elif interaction_analysis["sentiment"] < -0.2:
            if moral_alignment > 0.7:
                return "I'm sorry to hear that. Is there anything I can do to help?"
            else:
                return "I see. That's unfortunate."
        else:
            if extraversion > 0.3:
                return "That's interesting! Tell me more about that."
            else:
                return "I understand. Thank you for sharing that with me."
    
    def _initialize_social_preferences(self) -> Dict[str, float]:
        """Initialize social preferences based on personality"""
        extraversion = self.personality_traits.get("introversion-extraversion", 0)
        
        preferences = {
            "group_size": 0.5 + (extraversion * 0.3),  # 0.2 to 0.8
            "conversation_depth": 0.5 + (extraversion * 0.2),  # 0.3 to 0.7
            "formality": 0.5,  # Neutral by default
            "humor": 0.5 + (extraversion * 0.2)  # 0.3 to 0.7
        }
        
        return preferences
    
    def _initialize_conversation_topics(self) -> List[str]:
        """Initialize conversation topics based on personality"""
        topics = ["general", "weather", "work", "hobbies"]
        
        # Add topics based on personality traits
        if self.personality_traits.get("magical-aptitude", 0) > 0.5:
            topics.append("magic")
        
        if self.personality_traits.get("nature-connection", 0) > 0.5:
            topics.append("nature")
        
        if self.personality_traits.get("combat-readiness", 0) > 0.5:
            topics.append("adventure")
        
        return topics
    
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

## Best Practices

### Performance Optimization

1. **Memory Management**: Implement efficient memory storage and retrieval
2. **Behavior Caching**: Cache frequently used behavior patterns
3. **Lazy Loading**: Load character data only when needed
4. **Batch Processing**: Process multiple characters in batches

### AI Quality

1. **Consistency**: Ensure character behavior remains consistent
2. **Believability**: Make AI behavior believable and human-like
3. **Adaptability**: Allow characters to learn and adapt
4. **Personality**: Maintain strong personality traits

### Testing and Validation

1. **Behavior Testing**: Test character behavior in various scenarios
2. **Memory Testing**: Validate memory systems work correctly
3. **Decision Testing**: Test decision-making systems
4. **Social Testing**: Test social interaction systems

!!! tip "Ready to Create AI NPCs?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
