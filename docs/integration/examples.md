# Integration Examples

This guide provides practical examples of integrating the Open Character Design Specification validation system into various applications and workflows.

## Web Applications

### React Character Editor

```tsx
import React, { useState, useCallback } from 'react';
import { validateAndNormalize } from '@ocd-tools/validator';

interface CharacterEditorProps {
  initialCharacter: any;
  onSave: (character: any) => void;
}

export function CharacterEditor({ initialCharacter, onSave }: CharacterEditorProps) {
  const [character, setCharacter] = useState(initialCharacter);
  const [validationResult, setValidationResult] = useState(null);
  const [mode, setMode] = useState<'relaxed' | 'strict'>('relaxed');
  const [specPath, setSpecPath] = useState<string>('');

  const validateCharacter = useCallback(async () => {
    try {
      const result = await validateAndNormalize(character, mode, specPath);
      setValidationResult(result);
      return result.ok;
    } catch (error) {
      console.error('Validation error:', error);
      return false;
    }
  }, [character, mode, specPath]);

  const handleSave = useCallback(async () => {
    const isValid = await validateCharacter();
    if (isValid) {
      onSave(validationResult.data);
    }
  }, [validateCharacter, validationResult, onSave]);

  return (
    <div className="character-editor">
      <div className="validation-controls">
        <label>
          Mode:
          <select value={mode} onChange={(e) => setMode(e.target.value as 'relaxed' | 'strict')}>
            <option value="relaxed">Relaxed</option>
            <option value="strict">Strict</option>
          </select>
        </label>
        <label>
          Specification:
          <input
            type="text"
            value={specPath}
            onChange={(e) => setSpecPath(e.target.value)}
            placeholder="Path to custom spec file"
          />
        </label>
        <button onClick={validateCharacter}>Validate</button>
      </div>

      {validationResult && (
        <div className={`validation-results ${validationResult.ok ? 'success' : 'error'}`}>
          {validationResult.ok ? (
            <div>
              <h3>✅ Validation Successful</h3>
              {validationResult.warnings.length > 0 && (
                <div className="warnings">
                  <h4>Warnings:</h4>
                  <ul>
                    {validationResult.warnings.map((warning, index) => (
                      <li key={index}>
                        <strong>{warning.code}:</strong> {warning.detail}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div>
              <h3>❌ Validation Failed</h3>
              <ul>
                {validationResult.errors.map((error, index) => (
                  <li key={index}>
                    <strong>{error.instancePath}:</strong> {error.message}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <button onClick={handleSave} disabled={!validationResult?.ok}>
        Save Character
      </button>
    </div>
  );
}
```

### Vue.js Character Library

```vue
<template>
  <div class="character-library">
    <div class="filters">
      <select v-model="validationMode">
        <option value="relaxed">Relaxed</option>
        <option value="strict">Strict</option>
      </select>
      <input v-model="specPath" placeholder="Custom spec path" />
      <button @click="validateAll">Validate All</button>
    </div>

    <div class="characters">
      <div
        v-for="character in characters"
        :key="character.id"
        :class="['character-card', getValidationClass(character)]"
      >
        <h3>{{ character.names.canon }}</h3>
        <p>{{ character.identity.species }}</p>
        <div v-if="character.validation" class="validation-status">
          <span v-if="character.validation.ok" class="success">✅ Valid</span>
          <span v-else class="error">❌ Invalid</span>
          <div v-if="character.validation.warnings?.length" class="warnings">
            {{ character.validation.warnings.length }} warnings
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { validateAndNormalize } from '@ocd-tools/validator';

const characters = ref([]);
const validationMode = ref<'relaxed' | 'strict'>('relaxed');
const specPath = ref('');

const getValidationClass = (character: any) => {
  if (!character.validation) return 'unvalidated';
  return character.validation.ok ? 'valid' : 'invalid';
};

const validateAll = async () => {
  for (const character of characters.value) {
    try {
      const result = await validateAndNormalize(character, validationMode.value, specPath.value);
      character.validation = result;
    } catch (error) {
      character.validation = {
        ok: false,
        errors: [{ message: `Validation error: ${error}` }],
        warnings: []
      };
    }
  }
};
</script>
```

## Backend APIs

### Express.js Character API

```typescript
import express from 'express';
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, CreateCharacterRequest, ValidationResult } from './types';

const app = express();
app.use(express.json());

// Character storage (in production, use a database)
const characters: Map<string, Character> = new Map();

// Create character with validation
app.post('/api/characters', async (req: CreateCharacterRequest, res) => {
  try {
    const { characterData, validationMode = 'relaxed', specPath } = req.body;
    
    // Validate character data
    const result = await validateAndNormalize(characterData, validationMode, specPath);
    
    if (!result.ok) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.errors,
        warnings: result.warnings
      });
    }
    
    // Store validated character
    const character = result.data;
    characters.set(character.id, character);
    
    res.json({
      id: character.id,
      data: character,
      warnings: result.warnings || []
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Validate existing character
app.post('/api/characters/:id/validate', async (req, res) => {
  const character = characters.get(req.params.id);
  
  if (!character) {
    return res.status(404).json({ error: 'Character not found' });
  }
  
  const { mode = 'relaxed', specPath } = req.body;
  const result = await validateAndNormalize(character, mode, specPath);
  
  res.json({
    valid: result.ok,
    errors: result.errors || [],
    warnings: result.warnings || []
  });
});

// Get character with validation status
app.get('/api/characters/:id', async (req, res) => {
  const character = characters.get(req.params.id);
  
  if (!character) {
    return res.status(404).json({ error: 'Character not found' });
  }
  
  const { validate = false, mode = 'relaxed', specPath } = req.query;
  
  if (validate) {
    const result = await validateAndNormalize(character, mode as 'relaxed' | 'strict', specPath as string);
    return res.json({
      character,
      validation: result
    });
  }
  
  res.json({ character });
});

app.listen(3000, () => {
  console.log('Character API server running on port 3000');
});
```

### FastAPI Character Service

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ocd.validate import validate_and_normalize

app = FastAPI()

# Character storage (in production, use a database)
characters: Dict[str, Dict[str, Any]] = {}

class CreateCharacterRequest(BaseModel):
    character_data: Dict[str, Any]
    validation_mode: str = "relaxed"
    spec_path: Optional[str] = None

class ValidationRequest(BaseModel):
    mode: str = "relaxed"
    spec_path: Optional[str] = None

@app.post("/api/characters")
async def create_character(request: CreateCharacterRequest):
    """Create character with validation"""
    try:
        # Validate character data
        result = validate_and_normalize(
            request.character_data,
            mode=request.validation_mode,
            spec_path=request.spec_path
        )
        
        if not result["ok"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Validation failed",
                    "details": result["errors"],
                    "warnings": result.get("warnings", [])
                }
            )
        
        # Store validated character
        character = result["data"]
        characters[character["id"]] = character
        
        return {
            "id": character["id"],
            "data": character,
            "warnings": result.get("warnings", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/characters/{character_id}/validate")
async def validate_character(character_id: str, request: ValidationRequest):
    """Validate existing character"""
    if character_id not in characters:
        raise HTTPException(status_code=404, detail="Character not found")
    
    character = characters[character_id]
    result = validate_and_normalize(
        character,
        mode=request.mode,
        spec_path=request.spec_path
    )
    
    return {
        "valid": result["ok"],
        "errors": result.get("errors", []),
        "warnings": result.get("warnings", [])
    }

@app.get("/api/characters/{character_id}")
async def get_character(
    character_id: str,
    validate: bool = Query(False),
    mode: str = Query("relaxed"),
    spec_path: Optional[str] = Query(None)
):
    """Get character with optional validation"""
    if character_id not in characters:
        raise HTTPException(status_code=404, detail="Character not found")
    
    character = characters[character_id]
    
    if validate:
        result = validate_and_normalize(character, mode=mode, spec_path=spec_path)
        return {
            "character": character,
            "validation": result
        }
    
    return {"character": character}
```

## Game Engines

### Unity Character System

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;

[System.Serializable]
public class CharacterData
{
    public string id;
    public Names names;
    public Identity identity;
    public Personality personality;
    // ... other fields
}

public class CharacterValidator : MonoBehaviour
{
    [SerializeField] private string validationMode = "relaxed";
    [SerializeField] private string specPath = "";
    
    public async System.Threading.Tasks.Task<ValidationResult> ValidateCharacter(CharacterData character)
    {
        try
        {
            // Convert to JSON for validation
            string json = JsonConvert.SerializeObject(character);
            
            // Call validation API or use local validation
            var result = await ValidateCharacterAsync(json, validationMode, specPath);
            
            return result;
        }
        catch (Exception e)
        {
            Debug.LogError($"Validation error: {e.Message}");
            return new ValidationResult
            {
                ok = false,
                errors = new[] { new ValidationError { message = e.Message } }
            };
        }
    }
    
    private async System.Threading.Tasks.Task<ValidationResult> ValidateCharacterAsync(
        string json, string mode, string specPath)
    {
        // Implementation would call your validation service
        // or use a local validation library
        throw new NotImplementedException();
    }
}

[System.Serializable]
public class ValidationResult
{
    public bool ok;
    public CharacterData data;
    public ValidationError[] errors;
    public ValidationWarning[] warnings;
}

[System.Serializable]
public class ValidationError
{
    public string message;
    public string instancePath;
    public string schemaPath;
    public string keyword;
}

[System.Serializable]
public class ValidationWarning
{
    public string code;
    public string path;
    public string detail;
}
```

### Unreal Engine Character System

```cpp
// CharacterValidator.h
#pragma once

#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "CharacterValidator.generated.h"

USTRUCT(BlueprintType)
struct FValidationResult
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    bool bOk = false;

    UPROPERTY(BlueprintReadOnly)
    FString Data;

    UPROPERTY(BlueprintReadOnly)
    TArray<FString> Errors;

    UPROPERTY(BlueprintReadOnly)
    TArray<FString> Warnings;
};

UCLASS(BlueprintType)
class MYGAME_API UCharacterValidator : public UObject
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Character Validation")
    FValidationResult ValidateCharacter(const FString& CharacterJson, 
                                       const FString& Mode = TEXT("relaxed"),
                                       const FString& SpecPath = TEXT(""));

    UFUNCTION(BlueprintCallable, Category = "Character Validation")
    void SetValidationMode(const FString& Mode) { ValidationMode = Mode; }

    UFUNCTION(BlueprintCallable, Category = "Character Validation")
    void SetSpecPath(const FString& Path) { SpecPath = Path; }

private:
    UPROPERTY(EditAnywhere, Category = "Validation")
    FString ValidationMode = TEXT("relaxed");

    UPROPERTY(EditAnywhere, Category = "Validation")
    FString SpecPath = TEXT("");
};
```

## CLI Tools

### Batch Validation Script

```bash
#!/bin/bash
# validate-characters.sh

MODE=${1:-relaxed}
SPEC_PATH=${2:-""}
CHARACTER_DIR=${3:-"./characters"}

echo "Validating characters in $CHARACTER_DIR with mode: $MODE"
if [ -n "$SPEC_PATH" ]; then
    echo "Using specification: $SPEC_PATH"
fi

VALID_COUNT=0
INVALID_COUNT=0
WARNING_COUNT=0

for file in "$CHARACTER_DIR"/*.yaml "$CHARACTER_DIR"/*.json; do
    if [ -f "$file" ]; then
        echo "Validating $file..."
        
        if [ -n "$SPEC_PATH" ]; then
            result=$(ocd-validate "$file" --mode "$MODE" --spec "$SPEC_PATH" 2>&1)
        else
            result=$(ocd-validate "$file" --mode "$MODE" 2>&1)
        fi
        
        exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            echo "✅ $file - Valid"
            ((VALID_COUNT++))
        elif [ $exit_code -eq 2 ]; then
            echo "⚠️  $file - Valid with warnings"
            ((VALID_COUNT++))
            ((WARNING_COUNT++))
        else
            echo "❌ $file - Invalid"
            echo "$result"
            ((INVALID_COUNT++))
        fi
    fi
done

echo ""
echo "Validation Summary:"
echo "Valid: $VALID_COUNT"
echo "Invalid: $INVALID_COUNT"
echo "With Warnings: $WARNING_COUNT"

if [ $INVALID_COUNT -gt 0 ]; then
    exit 1
fi
```

### Git Hook for Character Validation

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating character files..."

# Check for YAML/JSON files in characters directory
CHARACTER_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(yaml|json)$' | grep '^characters/')

if [ -z "$CHARACTER_FILES" ]; then
    echo "No character files to validate"
    exit 0
fi

VALIDATION_FAILED=false

for file in $CHARACTER_FILES; do
    echo "Validating $file..."
    
    # Use strict mode for committed files
    if ! ocd-validate "$file" --mode strict; then
        echo "❌ $file failed validation"
        VALIDATION_FAILED=true
    else
        echo "✅ $file passed validation"
    fi
done

if [ "$VALIDATION_FAILED" = true ]; then
    echo ""
    echo "❌ Some character files failed validation. Please fix the errors before committing."
    exit 1
fi

echo "✅ All character files passed validation"
exit 0
```

## Testing

### Jest Test Suite

```javascript
// character-validation.test.js
import { validateAndNormalize } from '@ocd-tools/validator';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Character Validation', () => {
  const testCharacters = [
    'valid-character.yaml',
    'invalid-character.yaml',
    'warning-character.yaml'
  ];

  testCharacters.forEach(filename => {
    describe(filename, () => {
      const characterPath = join(__dirname, 'fixtures', filename);
      const characterData = JSON.parse(
        readFileSync(characterPath, 'utf8')
      );

      test('should validate in relaxed mode', async () => {
        const result = await validateAndNormalize(characterData, 'relaxed');
        
        expect(result).toHaveProperty('ok');
        expect(result).toHaveProperty('warnings');
        
        if (filename === 'valid-character.yaml') {
          expect(result.ok).toBe(true);
        }
      });

      test('should validate in strict mode', async () => {
        const result = await validateAndNormalize(characterData, 'strict');
        
        expect(result).toHaveProperty('ok');
        expect(result).toHaveProperty('warnings');
        
        if (filename === 'invalid-character.yaml') {
          expect(result.ok).toBe(false);
          expect(result.errors).toBeDefined();
          expect(result.errors.length).toBeGreaterThan(0);
        }
      });

      test('should work with custom specification', async () => {
        const specPath = join(__dirname, 'fixtures', 'custom-spec.ocd');
        const result = await validateAndNormalize(characterData, 'strict', specPath);
        
        expect(result).toHaveProperty('ok');
        expect(result).toHaveProperty('warnings');
      });
    });
  });
});
```

### Python Test Suite

```python
# test_character_validation.py
import pytest
import json
from pathlib import Path
from ocd.validate import validate_and_normalize

class TestCharacterValidation:
    @pytest.fixture
    def valid_character(self):
        return {
            "ocd_version": "1.0.0",
            "id": "test-001",
            "names": {"canon": "Test Character"},
            "identity": {
                "entity_kind": "person",
                "species": "human",
                "sapience_level": "sapient"
            },
            "meta": {
                "versioning": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "last_modified": "2024-01-01T00:00:00Z"
                }
            }
        }

    @pytest.fixture
    def invalid_character(self):
        return {
            "ocd_version": "1.0.0",
            "id": "test-002",
            # Missing required fields
            "identity": {
                "entity_kind": "invalid-kind",  # Invalid enum
                "species": "human"
            }
        }

    def test_relaxed_mode_valid(self, valid_character):
        result = validate_and_normalize(valid_character, mode="relaxed")
        assert result["ok"] is True
        assert "warnings" in result

    def test_strict_mode_valid(self, valid_character):
        result = validate_and_normalize(valid_character, mode="strict")
        assert result["ok"] is True
        assert "warnings" in result

    def test_relaxed_mode_invalid(self, invalid_character):
        result = validate_and_normalize(invalid_character, mode="relaxed")
        # Should succeed with warnings in relaxed mode
        assert result["ok"] is True
        assert len(result["warnings"]) > 0

    def test_strict_mode_invalid(self, invalid_character):
        result = validate_and_normalize(invalid_character, mode="strict")
        assert result["ok"] is False
        assert "errors" in result
        assert len(result["errors"]) > 0

    def test_custom_specification(self, valid_character):
        spec_path = Path(__file__).parent / "fixtures" / "custom-spec.ocd"
        result = validate_and_normalize(valid_character, spec_path=str(spec_path))
        assert result["ok"] is True
