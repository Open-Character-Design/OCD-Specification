# Technical Applications

Build robust character systems with OCD's technical capabilities for metadata management, AI integration, and procedural generation.

OCD provides the technical foundation for sophisticated character-driven applications. From AI training datasets to procedural generation systems, OCD's structured approach enables powerful technical implementations that scale from individual projects to enterprise applications. The new `ai_agent` configuration fields provide standardized AI behavior modeling for human-interactive systems.

## Character Metadata Management

### Structured Data Architecture

OCD treats each character as a structured entity containing rich metadata, from appearance traits to psychological archetypes. This structured approach enables powerful data operations that would be impossible with unstructured character data.

### Database Integration Patterns

**Relational Database Mapping:**
```python
# Example: Mapping OCD character to database schema
class CharacterModel(BaseModel):
    id: str
    ocd_version: str
    names_canon: str
    identity_kind: str
    identity_species: str
    personality_summary: Optional[str]
    created_at: datetime
    last_modified: datetime

class TraitModel(BaseModel):
    character_id: str
    trait_name: str
    trait_kind: str
    trait_value: Optional[float]
    trait_polarity: Optional[float]
    trait_intensity: Optional[float]
```

**NoSQL Document Storage:**
```json
{
  "_id": "char-aria-swift",
  "ocd_version": "0.0.1",
  "names": {
    "canon": "Aria the Swift",
    "aliases": ["Wind Dancer", "Storm Runner"]
  },
  "personality": {
    "summary": "Agile and determined warrior",
    "traits": [
      {
        "name": "introversion-extraversion",
        "kind": "bipolar",
        "polarity": 0.3,
        "intensity": 0.8
      }
    ]
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "last_modified": "2024-01-01T00:00:00Z"
  }
}
```

### Search and Query Capabilities

**Trait-Based Filtering:**
```python
# Find all characters with high combat readiness
combat_ready_characters = db.characters.find({
    "personality.traits": {
        "$elemMatch": {
            "name": "combat-readiness",
            "value": {"$gte": 0.8}
        }
    }
})

# Find characters by personality archetype
introverted_characters = db.characters.find({
    "personality.traits": {
        "$elemMatch": {
            "name": "introversion-extraversion",
            "polarity": {"$lt": 0.0}
        }
    }
})
```

**Complex Relationship Queries:**
```python
# Find characters connected to a specific faction
faction_members = db.characters.find({
    "relationships": {
        "$elemMatch": {
            "target_ref": {"$regex": "faction-.*"},
            "role": "member"
        }
    }
})
```

### Analytics and Insights

**Character Diversity Analysis:**
```python
def analyze_character_diversity(characters):
    """Analyze character diversity across various dimensions"""
    diversity_metrics = {
        "species_distribution": {},
        "personality_archetypes": {},
        "age_ranges": {},
        "relationship_networks": {}
    }
    
    for char in characters:
        # Species analysis
        species = char.get("identity", {}).get("species", "unknown")
        diversity_metrics["species_distribution"][species] = \
            diversity_metrics["species_distribution"].get(species, 0) + 1
        
        # Personality analysis
        traits = char.get("personality", {}).get("traits", [])
        for trait in traits:
            if trait["name"] == "introversion-extraversion":
                polarity = trait.get("polarity", 0)
                archetype = "introverted" if polarity < -0.3 else "extraverted" if polarity > 0.3 else "ambivert"
                diversity_metrics["personality_archetypes"][archetype] = \
                    diversity_metrics["personality_archetypes"].get(archetype, 0) + 1
    
    return diversity_metrics
```

## Procedural Generation

### Trait-Based Character Generation

OCD's structured trait system enables sophisticated procedural character generation algorithms that maintain narrative consistency while creating diverse character variations.

### Generation Algorithms

**Weighted Trait Selection:**
```python
import random
from typing import Dict, List, Any

class CharacterGenerator:
    def __init__(self, trait_weights: Dict[str, float]):
        self.trait_weights = trait_weights
        self.species_traits = self._load_species_templates()
        self.personality_archetypes = self._load_archetype_templates()
    
    def generate_character(self, species: str, archetype: str) -> Dict[str, Any]:
        """Generate a character based on species and personality archetype"""
        base_traits = self.species_traits.get(species, {})
        archetype_traits = self.personality_archetypes.get(archetype, {})
        
        # Combine and weight traits
        combined_traits = self._combine_traits(base_traits, archetype_traits)
        
        # Generate character with weighted randomness
        character = {
            "ocd_version": "0.0.1",
            "id": f"char-generated-{random.randint(1000, 9999)}",
            "identity": {
                "kind": "humanoid",
                "species": species
            },
            "personality": {
                "traits": self._generate_trait_values(combined_traits)
            }
        }
        
        return character
    
    def _generate_trait_values(self, trait_templates: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actual trait values based on templates"""
        traits = []
        
        for trait_name, template in trait_templates.items():
            if template["kind"] == "bipolar":
                # Generate bipolar trait with weighted distribution
                base_polarity = template.get("base_polarity", 0)
                variance = template.get("variance", 0.3)
                polarity = random.normalvariate(base_polarity, variance)
                polarity = max(-1, min(1, polarity))  # Clamp to [-1, 1]
                
                intensity = random.uniform(0.5, 1.0)
                
                traits.append({
                    "name": trait_name,
                    "kind": "bipolar",
                    "polarity": round(polarity, 2),
                    "intensity": round(intensity, 2)
                })
            
            elif template["kind"] == "scalar":
                base_value = template.get("base_value", 0.5)
                variance = template.get("variance", 0.2)
                value = random.normalvariate(base_value, variance)
                value = max(0, min(1, value))  # Clamp to [0, 1]
                
                traits.append({
                    "name": trait_name,
                    "kind": "scalar",
                    "value": round(value, 2)
                })
        
        return traits
```

**Constraint-Based Generation:**
```python
class ConstrainedCharacterGenerator:
    def __init__(self, constraints: Dict[str, Any]):
        self.constraints = constraints
    
    def generate_with_constraints(self) -> Dict[str, Any]:
        """Generate character that satisfies given constraints"""
        # Example: Generate a character for a specific role
        role_constraints = self.constraints.get("role", {})
        
        if role_constraints.get("type") == "warrior":
            # Ensure high combat readiness
            combat_trait = {
                "name": "combat-readiness",
                "kind": "scalar",
                "value": random.uniform(0.7, 1.0)
            }
            
            # Ensure appropriate personality for warrior role
            personality_traits = self._generate_warrior_personality()
            personality_traits.append(combat_trait)
            
            return {
                "personality": {
                    "traits": personality_traits
                }
            }
```

### Template-Based Generation

**Species Templates:**
```yaml
# species_templates.yaml
species:
  human:
    base_traits:
      - name: "introversion-extraversion"
        kind: "bipolar"
        base_polarity: 0.0
        variance: 0.4
      - name: "combat-readiness"
        kind: "scalar"
        base_value: 0.5
        variance: 0.3
  
  elf:
    base_traits:
      - name: "nature-connection"
        kind: "scalar"
        base_value: 0.8
        variance: 0.2
      - name: "magical-aptitude"
        kind: "scalar"
        base_value: 0.7
        variance: 0.3
```

**Archetype Templates:**
```yaml
# archetype_templates.yaml
archetypes:
  hero:
    personality_traits:
      - name: "introversion-extraversion"
        kind: "bipolar"
        base_polarity: 0.2
        variance: 0.3
      - name: "moral-uprightness"
        kind: "scalar"
        base_value: 0.8
        variance: 0.2
  
  villain:
    personality_traits:
      - name: "introversion-extraversion"
        kind: "bipolar"
        base_polarity: -0.1
        variance: 0.4
      - name: "moral-uprightness"
        kind: "scalar"
        base_value: 0.2
        variance: 0.3
```

## AI Training Datasets

### Ethical Data Provenance

OCD provides a framework for creating ethically sourced, structured datasets for AI model training. Every trait, artwork, and description can be tagged with attribution and licensing metadata.

### Dataset Structure

**Character Dataset Schema:**
```json
{
  "dataset_metadata": {
    "name": "Fantasy Character Dataset v1.0",
    "version": "1.0.0",
    "license": "CC-BY-4.0",
    "created_at": "2024-01-01T00:00:00Z",
    "total_characters": 1000,
    "attribution": {
      "original_creators": ["Studio A", "Artist B", "Writer C"],
      "dataset_curator": "OCD Community",
      "license_chain": "verified"
    }
  },
  "characters": [
    {
      "ocd_data": { /* Full OCD character data */ },
      "attribution": {
        "creator": "Studio A",
        "created_at": "2024-01-01T00:00:00Z",
        "license": "CC-BY-4.0",
        "usage_rights": ["training", "inference", "derivative_works"]
      },
      "media_assets": [
        {
          "type": "concept_art",
          "url": "https://example.com/aria-concept.jpg",
          "attribution": "Artist B",
          "license": "CC-BY-4.0"
        }
      ]
    }
  ]
}
```

### Training Data Pipeline

**Data Validation and Normalization:**
```python
class AITrainingDatasetBuilder:
    def __init__(self, ocd_validator):
        self.validator = ocd_validator
        self.dataset = {
            "dataset_metadata": {},
            "characters": []
        }
    
    def add_character(self, ocd_character: Dict[str, Any], attribution: Dict[str, Any]):
        """Add a validated character to the training dataset"""
        # Validate OCD character
        validation_result = self.validator.validate(ocd_character)
        if not validation_result.is_valid:
            raise ValueError(f"Invalid OCD character: {validation_result.errors}")
        
        # Normalize character data
        normalized_character = validation_result.normalized_data
        
        # Add to dataset with attribution
        self.dataset["characters"].append({
            "ocd_data": normalized_character,
            "attribution": attribution
        })
    
    def export_for_training(self, format: str = "jsonl") -> str:
        """Export dataset in format suitable for AI training"""
        if format == "jsonl":
            return self._export_jsonl()
        elif format == "huggingface":
            return self._export_huggingface()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_jsonl(self) -> str:
        """Export as JSONL for training"""
        lines = []
        for character in self.dataset["characters"]:
            # Extract training-relevant data
            training_data = {
                "personality_traits": character["ocd_data"]["personality"]["traits"],
                "appearance": character["ocd_data"].get("appearance", {}),
                "relationships": character["ocd_data"].get("relationships", []),
                "attribution": character["attribution"]
            }
            lines.append(json.dumps(training_data))
        return "\n".join(lines)
```

### Model Training Integration

**Personality Prediction Model:**
```python
import torch
from transformers import AutoTokenizer, AutoModel

class PersonalityPredictor:
    def __init__(self, model_name: str = "bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.trait_classifier = self._build_trait_classifier()
    
    def predict_personality_traits(self, character_description: str) -> Dict[str, float]:
        """Predict personality traits from character description"""
        inputs = self.tokenizer(character_description, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            trait_predictions = self.trait_classifier(outputs.last_hidden_state.mean(dim=1))
        
        # Convert to OCD trait format
        traits = {}
        trait_names = ["introversion-extraversion", "combat-readiness", "moral-uprightness"]
        
        for i, trait_name in enumerate(trait_names):
            traits[trait_name] = {
                "kind": "bipolar" if "-" in trait_name else "scalar",
                "value": float(trait_predictions[0][i])
            }
        
        return traits
```

## API Integration

### RESTful API Design

OCD's structured data naturally maps to RESTful API endpoints, enabling seamless integration with any application or service.

### API Endpoints

**Character Management:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="OCD Character API", version="1.0.0")

class CharacterCreate(BaseModel):
    ocd_data: Dict[str, Any]

class CharacterResponse(BaseModel):
    id: str
    ocd_data: Dict[str, Any]
    created_at: datetime
    last_modified: datetime

@app.post("/characters", response_model=CharacterResponse)
async def create_character(character: CharacterCreate):
    """Create a new character from OCD data"""
    # Validate OCD data
    validation_result = ocd_validator.validate(character.ocd_data)
    if not validation_result.is_valid:
        raise HTTPException(status_code=400, detail=validation_result.errors)
    
    # Store in database
    character_id = await character_service.create(validation_result.normalized_data)
    
    return CharacterResponse(
        id=character_id,
        ocd_data=validation_result.normalized_data,
        created_at=datetime.now(),
        last_modified=datetime.now()
    )

@app.get("/characters/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: str):
    """Retrieve a character by ID"""
    character = await character_service.get(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return CharacterResponse(**character)

@app.get("/characters", response_model=List[CharacterResponse])
async def list_characters(
    species: Optional[str] = None,
    trait_name: Optional[str] = None,
    trait_value_min: Optional[float] = None,
    limit: int = 100
):
    """List characters with optional filtering"""
    filters = {}
    if species:
        filters["identity.species"] = species
    if trait_name and trait_value_min is not None:
        filters[f"personality.traits.{trait_name}"] = {"$gte": trait_value_min}
    
    characters = await character_service.list(filters, limit=limit)
    return [CharacterResponse(**char) for char in characters]
```

**Trait Analysis:**
```python
@app.get("/characters/{character_id}/traits")
async def get_character_traits(character_id: str):
    """Get detailed trait analysis for a character"""
    character = await character_service.get(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    traits = character["ocd_data"]["personality"]["traits"]
    
    # Analyze trait patterns
    analysis = {
        "primary_archetype": analyze_primary_archetype(traits),
        "trait_balance": analyze_trait_balance(traits),
        "personality_summary": generate_personality_summary(traits),
        "compatibility_scores": calculate_compatibility_scores(character_id, traits)
    }
    
    return analysis

@app.post("/characters/{character_id}/relationships")
async def add_relationship(
    character_id: str,
    target_character_id: str,
    relationship_data: Dict[str, Any]
):
    """Add a relationship between two characters"""
    # Validate both characters exist
    character = await character_service.get(character_id)
    target_character = await character_service.get(target_character_id)
    
    if not character or not target_character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Add relationship
    await relationship_service.create(character_id, target_character_id, relationship_data)
    
    return {"message": "Relationship created successfully"}
```

### GraphQL Integration

**Schema Definition:**
```graphql
type Character {
  id: ID!
  ocdVersion: String!
  names: CharacterNames!
  identity: CharacterIdentity!
  personality: CharacterPersonality
  appearance: CharacterAppearance
  relationships: [Relationship!]!
  createdAt: DateTime!
  lastModified: DateTime!
}

type CharacterNames {
  canon: String!
  aliases: [String!]
}

type CharacterIdentity {
  kind: String!
  species: String!
  age: Int
}

type CharacterPersonality {
  summary: String
  traits: [Trait!]!
}

type Trait {
  name: String!
  kind: String!
  value: Float
  polarity: Float
  intensity: Float
}

type Relationship {
  targetCharacter: Character!
  role: String!
  sentiment: Float!
  description: String
}

type Query {
  character(id: ID!): Character
  characters(
    species: String
    traitName: String
    traitValueMin: Float
    limit: Int = 100
  ): [Character!]!
  characterTraits(id: ID!): TraitAnalysis!
}

type Mutation {
  createCharacter(ocdData: JSON!): Character!
  updateCharacter(id: ID!, ocdData: JSON!): Character!
  addRelationship(
    characterId: ID!
    targetCharacterId: ID!
    relationshipData: JSON!
  ): Relationship!
}
```

## Version Control for Design Assets

### Git-Like Workflow for Characters

OCD incorporates principles from software versioning, applied to character design. This enables sophisticated version control workflows for character development.

### Version Control Operations

**Character Versioning:**
```python
class CharacterVersionControl:
    def __init__(self, repository_path: str):
        self.repo_path = repository_path
        self.git_repo = git.Repo(repository_path)
    
    def create_character_branch(self, character_id: str, branch_name: str) -> str:
        """Create a new branch for character development"""
        branch_ref = f"refs/heads/char-{character_id}-{branch_name}"
        self.git_repo.create_head(branch_ref)
        return branch_ref
    
    def commit_character_changes(self, character_id: str, changes: Dict[str, Any], message: str):
        """Commit character changes with detailed message"""
        # Update character file
        character_file = f"characters/{character_id}.yaml"
        with open(character_file, 'w') as f:
            yaml.dump(changes, f)
        
        # Stage and commit
        self.git_repo.index.add([character_file])
        commit = self.git_repo.index.commit(f"char-{character_id}: {message}")
        
        return commit.hexsha
    
    def get_character_history(self, character_id: str) -> List[Dict[str, Any]]:
        """Get version history for a character"""
        character_file = f"characters/{character_id}.yaml"
        
        commits = []
        for commit in self.git_repo.iter_commits(paths=character_file):
            commits.append({
                "hash": commit.hexsha,
                "message": commit.message.strip(),
                "author": commit.author.name,
                "date": commit.committed_datetime.isoformat(),
                "changes": self._get_commit_changes(commit, character_file)
            })
        
        return commits
    
    def diff_character_versions(self, character_id: str, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two versions of a character"""
        character_file = f"characters/{character_id}.yaml"
        
        # Get file content for each version
        content1 = self.git_repo.git.show(f"{version1}:{character_file}")
        content2 = self.git_repo.git.show(f"{version2}:{character_file}")
        
        # Parse and compare
        char1 = yaml.safe_load(content1)
        char2 = yaml.safe_load(content2)
        
        return self._deep_diff(char1, char2)
```

**Collaborative Workflow:**
```python
class CollaborativeCharacterWorkflow:
    def __init__(self, character_vc: CharacterVersionControl):
        self.vc = character_vc
    
    def start_character_collaboration(self, character_id: str, collaborators: List[str]):
        """Set up collaborative character development"""
        # Create main development branch
        main_branch = self.vc.create_character_branch(character_id, "main")
        
        # Create feature branches for each collaborator
        feature_branches = {}
        for collaborator in collaborators:
            branch_name = f"feature-{collaborator}"
            feature_branches[collaborator] = self.vc.create_character_branch(character_id, branch_name)
        
        return {
            "main_branch": main_branch,
            "feature_branches": feature_branches
        }
    
    def merge_character_changes(self, character_id: str, source_branch: str, target_branch: str):
        """Merge character changes between branches"""
        # Switch to target branch
        self.vc.git_repo.git.checkout(target_branch)
        
        # Merge source branch
        merge_result = self.vc.git_repo.git.merge(source_branch)
        
        # Handle merge conflicts if any
        if "CONFLICT" in merge_result:
            conflicts = self._resolve_character_conflicts(character_id)
            return {"status": "conflicts_resolved", "conflicts": conflicts}
        
        return {"status": "merged_successfully"}
    
    def _resolve_character_conflicts(self, character_id: str) -> List[Dict[str, Any]]:
        """Resolve conflicts in character data"""
        conflicts = []
        
        # Check for trait conflicts
        trait_conflicts = self._check_trait_conflicts(character_id)
        if trait_conflicts:
            conflicts.extend(trait_conflicts)
        
        # Check for relationship conflicts
        relationship_conflicts = self._check_relationship_conflicts(character_id)
        if relationship_conflicts:
            conflicts.extend(relationship_conflicts)
        
        return conflicts
```

### Production Integration

**CI/CD Pipeline for Characters:**
```yaml
# .github/workflows/character-validation.yml
name: Character Validation

on:
  push:
    paths:
      - 'characters/**'
  pull_request:
    paths:
      - 'characters/**'

jobs:
  validate-characters:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install OCD validator
      run: pip install ocd
    
    - name: Validate all characters
      run: |
        for file in characters/*.yaml; do
          echo "Validating $file"
          ocd-validate "$file" --warnings-as-errors
        done
    
    - name: Generate character report
      run: |
        ocd-validate characters/ --report-format json > character-report.json
    
    - name: Upload character report
      uses: actions/upload-artifact@v3
      with:
        name: character-validation-report
        path: character-report.json
```

## Getting Started with Technical OCD

### For Developers

1. **Choose Your Integration Path**: API integration, database storage, or procedural generation
2. **Set Up Validation**: Integrate OCD validators into your development workflow
3. **Design Your Schema**: Extend OCD with custom traits and relationships for your use case
4. **Build Your Pipeline**: Create automated workflows for character processing and validation

### For Data Scientists

1. **Prepare Your Dataset**: Use OCD's structured format for character data collection
2. **Implement Validation**: Ensure data quality with OCD's validation tools
3. **Build Analysis Tools**: Create custom analytics for character trait patterns
4. **Train Your Models**: Use OCD data for AI model training with proper attribution

### For DevOps Teams

1. **Set Up Version Control**: Implement Git-based workflows for character development
2. **Create CI/CD Pipelines**: Automate character validation and deployment
3. **Monitor Data Quality**: Set up alerts for character data inconsistencies
4. **Scale Your Infrastructure**: Design systems that can handle large character datasets

!!! tip "Ready to Build with OCD?"
    Start with our [Integration Guides](../integration/python-validator.md) to see how to integrate OCD into your applications, or explore our [Technical Examples](../authoring/examples.md) for implementation patterns.
