# Python Validator

The Python validator provides comprehensive validation, normalization, and diagnostics for OCD documents using Pydantic v2 and JSON Schema.

## Installation

```bash
pip install ocd
```

## Use Case Examples

The Python validator is essential for many OCD use cases. Here are practical examples of how to integrate it into different applications:

### Creative Applications

**Character Design Workflow Integration:**
```python
from ocd.ocd_validate import validate_and_normalize
from pathlib import Path

class CharacterDesignWorkflow:
    def __init__(self, character_dir: str):
        self.character_dir = Path(character_dir)
    
    def validate_character_design(self, character_file: str) -> dict:
        """Validate character design for creative workflow"""
        file_path = self.character_dir / character_file
        
        with open(file_path, 'r') as f:
            character_data = f.read()
        
        result = validate_and_normalize(character_data)
        
        if result["ok"]:
            print(f"✅ Character {character_file} is valid")
            return result["data"]
        else:
            print(f"❌ Character {character_file} has errors:")
            for error in result["errors"]:
                print(f"  - {error}")
            return None
    
    def batch_validate_characters(self) -> dict:
        """Validate all characters in a project"""
        results = {"valid": [], "invalid": []}
        
        for yaml_file in self.character_dir.glob("*.yaml"):
            result = self.validate_character_design(yaml_file.name)
            if result:
                results["valid"].append(yaml_file.name)
            else:
                results["invalid"].append(yaml_file.name)
        
        return results
```

### Technical Applications

**API Integration with Validation:**
```python
from fastapi import FastAPI, HTTPException
from ocd.ocd_validate import validate_and_normalize
from pydantic import BaseModel

app = FastAPI()

class CharacterCreate(BaseModel):
    ocd_data: dict

@app.post("/characters")
async def create_character(character: CharacterCreate):
    """Create character with validation"""
    # Validate OCD data
    result = validate_and_normalize(character.ocd_data)
    
    if not result["ok"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid OCD data: {result['errors']}"
        )
    
    # Store validated character
    character_id = store_character(result["data"])
    
    return {
        "id": character_id,
        "data": result["data"],
        "warnings": result.get("warnings", [])
    }

@app.get("/characters/{character_id}/validate")
async def validate_character(character_id: str):
    """Validate existing character"""
    character = get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    result = validate_and_normalize(character)
    
    return {
        "valid": result["ok"],
        "errors": result.get("errors", []),
        "warnings": result.get("warnings", [])
    }
```

**Procedural Generation with Validation:**
```python
import random
from ocd.ocd_validate import validate_and_normalize

class ProceduralCharacterGenerator:
    def __init__(self, trait_templates: dict):
        self.trait_templates = trait_templates
    
    def generate_character(self, species: str, archetype: str) -> dict:
        """Generate character with validation"""
        # Generate character data
        character_data = self._generate_character_data(species, archetype)
        
        # Validate generated character
        result = validate_and_normalize(character_data)
        
        if not result["ok"]:
            # Fix validation errors
            character_data = self._fix_validation_errors(character_data, result["errors"])
            result = validate_and_normalize(character_data)
        
        return result["data"]
    
    def _fix_validation_errors(self, character_data: dict, errors: list) -> dict:
        """Fix common validation errors in generated characters"""
        for error in errors:
            if "missing required field" in error.lower():
                field = error.split("'")[1]
                character_data[field] = self._get_default_value(field)
        
        return character_data
```

### Interactive & Storytelling Applications

**Game Engine Integration:**
```python
import json
from ocd.ocd_validate import validate_and_normalize

class GameCharacterImporter:
    def __init__(self, game_engine):
        self.game_engine = game_engine
    
    def import_character(self, ocd_file: str) -> bool:
        """Import OCD character into game engine"""
        # Load and validate OCD character
        with open(ocd_file, 'r') as f:
            character_data = f.read()
        
        result = validate_and_normalize(character_data)
        
        if not result["ok"]:
            print(f"Failed to import {ocd_file}: {result['errors']}")
            return False
        
        # Convert to game engine format
        game_character = self._convert_to_game_format(result["data"])
        
        # Import into game engine
        success = self.game_engine.create_character(game_character)
        
        if success:
            print(f"✅ Successfully imported {ocd_file}")
        else:
            print(f"❌ Failed to import {ocd_file} into game engine")
        
        return success
    
    def _convert_to_game_format(self, ocd_character: dict) -> dict:
        """Convert OCD character to game engine format"""
        # Extract personality traits for AI behavior
        traits = ocd_character.get("personality", {}).get("traits", [])
        
        game_character = {
            "id": ocd_character["id"],
            "name": ocd_character["names"]["canon"],
            "species": ocd_character["identity"]["species"],
            "ai_personality": self._extract_ai_traits(traits),
            "appearance": ocd_character.get("appearance", {}),
            "relationships": ocd_character.get("relationships", [])
        }
        
        return game_character
    
    def _extract_ai_traits(self, traits: list) -> dict:
        """Extract traits relevant to AI behavior"""
        ai_traits = {}
        
        for trait in traits:
            if trait["name"] == "introversion-extraversion":
                ai_traits["extraversion"] = trait["polarity"]
            elif trait["name"] == "combat-readiness":
                ai_traits["aggression"] = trait["value"]
            elif trait["name"] == "moral-uprightness":
                ai_traits["morality"] = trait["value"]
        
        return ai_traits
```

**AI Training Data Preparation:**
```python
from ocd.ocd_validate import validate_and_normalize
import json

class AITrainingDataBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.training_data = []
    
    def add_character_to_dataset(self, ocd_file: str, attribution: dict):
        """Add validated character to AI training dataset"""
        # Load and validate character
        with open(ocd_file, 'r') as f:
            character_data = f.read()
        
        result = validate_and_normalize(character_data)
        
        if not result["ok"]:
            print(f"Skipping invalid character {ocd_file}: {result['errors']}")
            return False
        
        # Add to training dataset with attribution
        training_entry = {
            "ocd_data": result["data"],
            "attribution": attribution,
            "validation_warnings": result.get("warnings", [])
        }
        
        self.training_data.append(training_entry)
        return True
    
    def export_training_dataset(self, format: str = "jsonl"):
        """Export training dataset in specified format"""
        if format == "jsonl":
            self._export_jsonl()
        elif format == "huggingface":
            self._export_huggingface()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_jsonl(self):
        """Export as JSONL for training"""
        output_file = self.output_dir / "training_data.jsonl"
        
        with open(output_file, 'w') as f:
            for entry in self.training_data:
                f.write(json.dumps(entry) + "\n")
        
        print(f"Exported {len(self.training_data)} characters to {output_file}")
```

### Community & Open Source Applications

**Character Library Management:**
```python
from ocd.ocd_validate import validate_and_normalize
from pathlib import Path
import yaml

class CharacterLibraryManager:
    def __init__(self, library_dir: str):
        self.library_dir = Path(library_dir)
    
    def add_character_to_library(self, character_file: str, metadata: dict):
        """Add character to community library with validation"""
        # Validate character
        with open(character_file, 'r') as f:
            character_data = f.read()
        
        result = validate_and_normalize(character_data)
        
        if not result["ok"]:
            raise ValueError(f"Invalid character: {result['errors']}")
        
        # Add library metadata
        validated_character = result["data"]
        validated_character["library_metadata"] = {
            "added_date": datetime.now().isoformat(),
            "contributor": metadata.get("contributor"),
            "license": metadata.get("license", "CC-BY-4.0"),
            "tags": metadata.get("tags", [])
        }
        
        # Save to library
        library_file = self.library_dir / f"{validated_character['id']}.yaml"
        with open(library_file, 'w') as f:
            yaml.dump(validated_character, f, default_flow_style=False)
        
        print(f"✅ Added {validated_character['id']} to library")
    
    def validate_library(self) -> dict:
        """Validate entire character library"""
        results = {"valid": [], "invalid": [], "warnings": []}
        
        for yaml_file in self.library_dir.glob("*.yaml"):
            with open(yaml_file, 'r') as f:
                character_data = f.read()
            
            result = validate_and_normalize(character_data)
            
            if result["ok"]:
                results["valid"].append(yaml_file.name)
                if result.get("warnings"):
                    results["warnings"].extend([
                        f"{yaml_file.name}: {warning}" 
                        for warning in result["warnings"]
                    ])
            else:
                results["invalid"].append({
                    "file": yaml_file.name,
                    "errors": result["errors"]
                })
        
        return results
```

## Usage

### CLI

```bash
# Validate a file (relaxed mode by default)
ocd-validate character.yaml

# Use strict validation mode
ocd-validate character.yaml --mode strict

# Use custom specification overlay
ocd-validate character.yaml --spec my-project-spec.ocd

# Combine mode and spec
ocd-validate character.yaml --mode strict --spec my-project-spec.ocd

# Print normalized output
ocd-validate character.yaml --print

# Treat warnings as errors
ocd-validate character.yaml --warnings-as-errors

# Force input format
ocd-validate character.yaml --format yaml
```

### Programmatic API

```python
from ocd.ocd_validate import validate_and_normalize

# Basic validation (relaxed mode)
result = validate_and_normalize(document)

# Strict validation mode
result = validate_and_normalize(document, mode="strict")

# With custom specification overlay
result = validate_and_normalize(document, spec_path="my-project-spec.ocd")

# Combine mode and spec
result = validate_and_normalize(document, mode="strict", spec_path="my-project-spec.ocd")

if result["ok"]:
    print("Valid:", result["data"])
    print("Warnings:", result["warnings"])
else:
    print("Errors:", result["errors"])
```

### CLI Options

```bash
ocd-validate [OPTIONS] PATH

Arguments:
  PATH  Path to an OCD document (YAML or JSON). Use '-' to read from standard input.

Options:
  --format [auto|json|yaml]  Force the input parser. Defaults to 'auto'.
  --mode [relaxed|strict]    Validation mode (default: relaxed).
  --spec PATH                Path to custom OCD specification overlay file.
  --print                    Print the normalized document to stdout on success.
  --indent INTEGER           Indent level to use when printing normalized JSON (default: 2).
  --warnings-as-errors       Exit with code 2 if any warnings are produced.
  --help                     Show this message and exit.
```

## API Reference

### `validate_and_normalize(doc: Any, mode: str = "relaxed", spec_path: str = None) -> Dict[str, Any]`

Validates and normalizes an OCD document.

**Parameters:**
- `doc`: The document to validate (dict, list, or primitive)
- `mode`: Validation mode - "relaxed" for structure-only, "strict" for full validation (default: "relaxed")
- `spec_path`: Optional path to custom OCD specification overlay file

**Returns:**
- `Dict[str, Any]`: Result object with the following structure:
  - `ok: bool`: Whether validation succeeded
  - `data?: dict`: Normalized document (if valid)
  - `errors?: list`: Validation errors (if invalid)
  - `warnings: list`: Linting warnings

**Example:**
```python
from ocd.ocd_validate import validate_and_normalize

document = {
    "kind": "CharacterDefinition",
    "ocd_version": "1.0.0",
    "id": "char-123",
    "slug": "example-character",
    "names": {"canon": "Example Character"},
    "identity": {"kind": "humanoid"},
    "meta": {"versioning": {"created_at": "2024-01-01T00:00:00Z", "last_modified": "2024-01-01T00:00:00Z"}}
}

result = validate_and_normalize(document)
```

## Normalization

The validator performs the following normalizations:

- **Bipolar trait names**: Canonicalize to `-` dash syntax
- **Tokens**: Lowercase and deduplicate arrays for `tags`, `genres`, `media`, `media_targets`
- **Slugs**: Normalize using consistent token rules
- **Axis names**: Standardize trait axis separators

## Diagnostics

The validator provides comprehensive linting with the following warning codes:

- `RATING_CONFLICT`: Conflicting content ratings
- `MISSING_SKILL_TAGS`: Skills without appropriate tags
- `UNRESOLVED_REF`: References that cannot be resolved
- `MISSING_CANON_NAME`: Missing canonical name
- `NONCANONICAL_CANON_NAME`: Non-canonical name formatting
- `DEFINITION_RUNTIME_FIELD`: Runtime fields in definition
- `COMPOSITE_CONTROL_SHARE_OVERFLOW`: Composite control share exceeds 1.0
- `COMPOSITE_SECRET_WITHOUT_IDENTITY`: Secret composite without identity
- `COMPOSITE_SECRET_IDENTITY_MISMATCH`: Secret identity mismatch
- `NORMALIZED_SLUG`: Slug normalization applied
- `NORMALIZED_AXIS`: Axis name normalization applied

## Dependencies

- `jsonschema>=4.22`: JSON Schema validation
- `pydantic>=2.7`: Data validation and parsing
- `pyyaml>=6.0`: YAML parsing support

## Source Files

- `src/ocd/ocd_validate.py` - Main validation logic
- `src/ocd/ocd_normalize.py` - Normalization functions
- `src/ocd/ocd_lint.py` - Linting rules
- `src/ocd/ocd_model.py` - Pydantic models
