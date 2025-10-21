# JavaScript/TypeScript Validator

The JavaScript/TypeScript validator provides comprehensive validation, normalization, and diagnostics for OCD documents using Ajv and JSON Schema.

## Installation

Choose your preferred package manager:

=== "npm"

    ```bash
    npm install @ocd-tools/validator@1.0.0
    ```

=== "yarn"

    ```bash
    yarn add @ocd-tools/validator@1.0.0
    ```

=== "pnpm"

    ```bash
    pnpm add @ocd-tools/validator@1.0.0
    ```

=== "Global Installation"

    ```bash
    npm install --global @ocd-tools/validator@1.0.0
    ```

## Use Case Examples

The JavaScript/TypeScript validator is perfect for web applications, Node.js backends, and modern development workflows. Here are practical examples of how to integrate it into different applications:

### Creative Applications

**Web-Based Character Design Tool:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, ValidationResult } from './types';

class WebCharacterDesigner {
  private characters: Map<string, Character> = new Map();
  
  async createCharacter(characterData: any): Promise<ValidationResult> {
    // Validate character data
    const result = await validateAndNormalize(characterData);
    
    if (result.ok) {
      // Store validated character
      this.characters.set(result.data.id, result.data);
      
      // Update UI
      this.updateCharacterList();
      
      return {
        success: true,
        character: result.data,
        warnings: result.warnings || []
      };
    } else {
      return {
        success: false,
        errors: result.errors || []
      };
    }
  }
  
  async validateCharacter(characterId: string): Promise<ValidationResult> {
    const character = this.characters.get(characterId);
    if (!character) {
      return { success: false, errors: ['Character not found'] };
    }
    
    const result = await validateAndNormalize(character);
    return {
      success: result.ok,
      character: result.data,
      warnings: result.warnings || [],
      errors: result.errors || []
    };
  }
  
  private updateCharacterList(): void {
    // Update UI with character list
    const characterList = Array.from(this.characters.values());
    this.renderCharacterList(characterList);
  }
  
  private renderCharacterList(characters: Character[]): void {
    // Render characters in UI
    const container = document.getElementById('character-list');
    if (container) {
      container.innerHTML = characters.map(char => 
        `<div class="character-card" data-id="${char.id}">
          <h3>${char.names.canon}</h3>
          <p>${char.identity.species}</p>
        `
      ).join('');
    }
  }
}
```

### Technical Applications

**Node.js API with Validation:**
```typescript
import express from 'express';
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, CreateCharacterRequest } from './types';

const app = express();
app.use(express.json());

// Character storage (in production, use a database)
const characters: Map<string, Character> = new Map();

app.post('/api/characters', async (req: CreateCharacterRequest, res) => {
  try {
    // Validate OCD data
    const result = await validateAndNormalize(req.body.ocdData);
    
    if (!result.ok) {
      return res.status(400).json({
        error: 'Invalid OCD data',
        details: result.errors
      });
    }
    
    // Store character
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

app.get('/api/characters/:id/validate', async (req, res) => {
  const character = characters.get(req.params.id);
  
  if (!character) {
    return res.status(404).json({ error: 'Character not found' });
  }
  
  const result = await validateAndNormalize(character);
  
  res.json({
    valid: result.ok,
    errors: result.errors || [],
    warnings: result.warnings || []
  });
});

app.listen(3000, () => {
  console.log('Character API server running on port 3000');
});
```

**Procedural Generation with Validation:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, TraitTemplate } from './types';

class ProceduralCharacterGenerator {
  private traitTemplates: Map<string, TraitTemplate[]> = new Map();
  
  constructor() {
    this.loadTraitTemplates();
  }
  
  async generateCharacter(species: string, archetype: string): Promise<Character | null> {
    // Generate character data
    const characterData = this.generateCharacterData(species, archetype);
    
    // Validate generated character
    const result = await validateAndNormalize(characterData);
    
    if (!result.ok) {
      // Try to fix validation errors
      const fixedData = this.fixValidationErrors(characterData, result.errors || []);
      const fixedResult = await validateAndNormalize(fixedData);
      
      if (!fixedResult.ok) {
        console.error('Failed to generate valid character:', fixedResult.errors);
        return null;
      }
      
      return fixedResult.data;
    }
    
    return result.data;
  }
  
  private generateCharacterData(species: string, archetype: string): any {
    const speciesTraits = this.traitTemplates.get(species) || [];
    const archetypeTraits = this.traitTemplates.get(archetype) || [];
    
    return {
      ocd_version: "0.0.1",
      id: `char-generated-${Date.now()}`,
      names: {
        canon: this.generateName(species, archetype)
      },
      identity: {
        kind: "humanoid",
        species: species
      },
      personality: {
        traits: [...speciesTraits, ...archetypeTraits].map(template => ({
          name: template.name,
          kind: template.kind,
          value: this.generateTraitValue(template),
          polarity: template.kind === 'bipolar' ? this.generatePolarity() : undefined,
          intensity: this.generateIntensity()
        }))
      },
      meta: {
        versioning: {
          created_at: new Date().toISOString(),
          last_modified: new Date().toISOString()
        }
      }
    };
  }
  
  private fixValidationErrors(characterData: any, errors: string[]): any {
    // Fix common validation errors
    for (const error of errors) {
      if (error.includes('missing required field')) {
        const field = error.match(/'([^']+)'/)?.[1];
        if (field) {
          characterData[field] = this.getDefaultValue(field);
        }
      }
    }
    
    return characterData;
  }
}
```

### Interactive & Storytelling Applications

**Game Engine Integration (Unity/Unreal):**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, GameCharacter } from './types';

class GameCharacterImporter {
  private gameEngine: any; // Game engine interface
  
  constructor(gameEngine: any) {
    this.gameEngine = gameEngine;
  }
  
  async importCharacter(ocdFile: string): Promise<boolean> {
    try {
      // Load OCD file
      const characterData = await this.loadOCDFile(ocdFile);
      
      // Validate character
      const result = await validateAndNormalize(characterData);
      
      if (!result.ok) {
        console.error(`Failed to import ${ocdFile}:`, result.errors);
        return false;
      }
      
      // Convert to game format
      const gameCharacter = this.convertToGameFormat(result.data);
      
      // Import into game engine
      const success = await this.gameEngine.createCharacter(gameCharacter);
      
      if (success) {
        console.log(`✅ Successfully imported ${ocdFile}`);
      } else {
        console.error(`❌ Failed to import ${ocdFile} into game engine`);
      }
      
      return success;
    } catch (error) {
      console.error(`Error importing ${ocdFile}:`, error);
      return false;
    }
  }
  
  private convertToGameFormat(ocdCharacter: Character): GameCharacter {
    const traits = ocdCharacter.personality?.traits || [];
    
    return {
      id: ocdCharacter.id,
      name: ocdCharacter.names.canon,
      species: ocdCharacter.identity.species,
      aiPersonality: this.extractAITraits(traits),
      appearance: ocdCharacter.appearance || {},
      relationships: ocdCharacter.relationships || []
    };
  }
  
  private extractAITraits(traits: any[]): Record<string, number> {
    const aiTraits: Record<string, number> = {};
    
    for (const trait of traits) {
      switch (trait.name) {
        case 'introversion-extraversion':
          aiTraits.extraversion = trait.polarity || 0;
          break;
        case 'combat-readiness':
          aiTraits.aggression = trait.value || 0;
          break;
        case 'moral-uprightness':
          aiTraits.morality = trait.value || 0;
          break;
      }
    }
    
    return aiTraits;
  }
}
```

**Visual Novel Character System:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, DialogueResponse } from './types';

class VisualNovelCharacterSystem {
  private characters: Map<string, Character> = new Map();
  
  async loadCharacter(characterData: any): Promise<boolean> {
    const result = await validateAndNormalize(characterData);
    
    if (!result.ok) {
      console.error('Invalid character data:', result.errors);
      return false;
    }
    
    this.characters.set(result.data.id, result.data);
    return true;
  }
  
  generateDialogueResponse(characterId: string, playerInput: string, context: any): DialogueResponse {
    const character = this.characters.get(characterId);
    if (!character) {
      throw new Error(`Character ${characterId} not found`);
    }
    
    const traits = character.personality?.traits || [];
    const extraversion = this.getTraitValue(traits, 'introversion-extraversion');
    const moralAlignment = this.getTraitValue(traits, 'moral-uprightness');
    
    // Generate response based on personality
    const response = this.generatePersonalityResponse(extraversion, moralAlignment, playerInput, context);
    
    return {
      characterId,
      response,
      emotion: this.determineEmotion(character, playerInput),
      expression: this.getExpression(character, response)
    };
  }
  
  private getTraitValue(traits: any[], traitName: string): number {
    const trait = traits.find(t => t.name === traitName);
    return trait?.value || trait?.polarity || 0;
  }
  
  private generatePersonalityResponse(extraversion: number, morality: number, input: string, context: any): string {
    // Generate response based on personality traits
    if (extraversion > 0.3) {
      return this.generateExtravertedResponse(input, context);
    } else if (extraversion < -0.3) {
      return this.generateIntrovertedResponse(input, context);
    } else {
      return this.generateNeutralResponse(input, context);
    }
  }
}
```

### Community & Open Source Applications

**Character Library Web App:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';
import { Character, LibraryMetadata } from './types';

class CharacterLibraryApp {
  private characters: Map<string, Character> = new Map();
  private libraryMetadata: Map<string, LibraryMetadata> = new Map();
  
  async addCharacter(characterData: any, metadata: LibraryMetadata): Promise<boolean> {
    try {
      // Validate character
      const result = await validateAndNormalize(characterData);
      
      if (!result.ok) {
        throw new Error(`Invalid character: ${result.errors?.join(', ')}`);
      }
      
      // Add library metadata
      const character = {
        ...result.data,
        library_metadata: {
          added_date: new Date().toISOString(),
          contributor: metadata.contributor,
          license: metadata.license || 'CC-BY-4.0',
          tags: metadata.tags || []
        }
      };
      
      // Store character
      this.characters.set(character.id, character);
      this.libraryMetadata.set(character.id, metadata);
      
      console.log(`✅ Added ${character.id} to library`);
      return true;
    } catch (error) {
      console.error('Failed to add character:', error);
      return false;
    }
  }
  
  async validateLibrary(): Promise<{ valid: string[], invalid: any[] }> {
    const results = { valid: [], invalid: [] };
    
    for (const [id, character] of this.characters) {
      const result = await validateAndNormalize(character);
      
      if (result.ok) {
        results.valid.push(id);
      } else {
        results.invalid.push({
          id,
          errors: result.errors
        });
      }
    }
    
    return results;
  }
  
  searchCharacters(query: string, filters: any = {}): Character[] {
    let results = Array.from(this.characters.values());
    
    // Filter by search query
    if (query) {
      results = results.filter(char => 
        char.names.canon.toLowerCase().includes(query.toLowerCase()) ||
        char.identity.species.toLowerCase().includes(query.toLowerCase())
      );
    }
    
    // Filter by species
    if (filters.species) {
      results = results.filter(char => char.identity.species === filters.species);
    }
    
    // Filter by tags
    if (filters.tags && filters.tags.length > 0) {
      results = results.filter(char => 
        char.library_metadata?.tags?.some((tag: string) => 
          filters.tags.includes(tag)
        )
      );
    }
    
    return results;
  }
}
```

## Usage

### CLI

```bash
# Validate a file
npx @ocd-tools/validator character.yaml

# Print normalized output
npx @ocd-tools/validator character.yaml --print

# Treat warnings as errors
npx @ocd-tools/validator character.yaml --warnings-as-errors

# Force input format
npx @ocd-tools/validator character.yaml --format yaml
```

### Programmatic API

=== "TypeScript"

    ```typescript
    import { validateAndNormalize } from '@ocd-tools/validator';
    
    // Validate a document
    const result = validateAndNormalize(document);
    
    if (result.ok) {
        console.log('Valid:', result.data);
        console.log('Warnings:', result.warnings);
    } else {
        console.log('Errors:', result.errors);
    }
    ```

=== "JavaScript"

    ```javascript
    const { validateAndNormalize } = require('@ocd-tools/validator');
    
    // Validate a document
    const result = validateAndNormalize(document);
    
    if (result.ok) {
        console.log('Valid:', result.data);
        console.log('Warnings:', result.warnings);
    } else {
        console.log('Errors:', result.errors);
    }
    ```

=== "ES Modules"

    ```javascript
    import { validateAndNormalize } from '@ocd-tools/validator';
    
    const result = await validateAndNormalize(document);
    ```

### CLI Options

```bash
@ocd-tools/validator [OPTIONS] PATH

Arguments:
  PATH  Path to an OCD document (YAML or JSON). Use '-' to read from standard input.

Options:
  --format [auto|json|yaml]  Force the input parser. Defaults to 'auto'.
  --print                    Print the normalized document to stdout on success.
  --indent INTEGER           Indent level to use when printing normalized JSON (default: 2).
  --warnings-as-errors       Exit with code 2 if any warnings are produced.
  --help                     Show this message and exit.
```

## API Reference

### `validateAndNormalize(doc: any): ValidationResult`

Validates and normalizes an OCD document.

**Parameters:**
- `doc`: The document to validate (object, array, or primitive)

**Returns:**
- `ValidationResult`: Result object with the following structure:
  - `ok: boolean`: Whether validation succeeded
  - `data?: object`: Normalized document (if valid)
  - `errors?: ValidationError[]`: Validation errors (if invalid)
  - `warnings: ValidationWarning[]`: Linting warnings

**TypeScript Types:**
```typescript
interface ValidationResult {
  ok: boolean;
  data?: any;
  errors?: ValidationError[];
  warnings: ValidationWarning[];
}

interface ValidationError {
  code: string;
  message: string;
  path: string;
  value: any;
}

interface ValidationWarning {
  code: string;
  message: string;
  path: string;
  value: any;
}
```

**Example:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

const document = {
  ocd_version: "1.0.0",
  id: "char-123",
  names: { canon: "Example Character" },
  identity: { kind: "humanoid", species: "Human" },
  meta: {
    versioning: {
      created_at: "2024-01-01T00:00:00Z",
      last_modified: "2024-01-01T00:00:00Z"
    }
  }
};

const result = validateAndNormalize(document);
```

## Framework Integration

### Express.js

```typescript
import express from 'express';
import { validateAndNormalize } from '@ocd-tools/validator';

const app = express();

app.post('/api/characters/validate', (req, res) => {
  const result = validateAndNormalize(req.body);
  
  if (result.ok) {
    res.json({ 
      success: true, 
      data: result.data,
      warnings: result.warnings 
    });
  } else {
    res.status(400).json({ 
      success: false, 
      errors: result.errors 
    });
  }
});
```

### Next.js API Route

```typescript
// pages/api/validate-character.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { validateAndNormalize } from '@ocd-tools/validator';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const result = validateAndNormalize(req.body);
  
  if (result.ok) {
    res.json({ 
      success: true, 
      data: result.data,
      warnings: result.warnings 
    });
  } else {
    res.status(400).json({ 
      success: false, 
      errors: result.errors 
    });
  }
}
```

### React Hook

```typescript
import { useState, useCallback } from 'react';
import { validateAndNormalize } from '@ocd-tools/validator';

export function useCharacterValidation() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const validateCharacter = useCallback(async (character: any) => {
    setLoading(true);
    try {
      const validationResult = validateAndNormalize(character);
      setResult(validationResult);
      return validationResult;
    } finally {
      setLoading(false);
    }
  }, []);

  return { result, loading, validateCharacter };
}
```

### Vue.js Composition API

```typescript
import { ref, computed } from 'vue';
import { validateAndNormalize } from '@ocd-tools/validator';

export function useCharacterValidation() {
  const result = ref(null);
  const loading = ref(false);

  const validateCharacter = async (character: any) => {
    loading.value = true;
    try {
      const validationResult = validateAndNormalize(character);
      result.value = validationResult;
      return validationResult;
    } finally {
      loading.value = false;
    }
  };

  const isValid = computed(() => result.value?.ok ?? false);
  const errors = computed(() => result.value?.errors ?? []);
  const warnings = computed(() => result.value?.warnings ?? []);

  return {
    result,
    loading,
    isValid,
    errors,
    warnings,
    validateCharacter
  };
}
```

## Advanced Usage

### Custom Validation Rules

```typescript
import { validateAndNormalize, addCustomValidator } from '@ocd-tools/validator';

// Add custom validation rule
addCustomValidator('custom-rule', (value, path) => {
  if (value === 'forbidden') {
    return {
      code: 'CUSTOM_FORBIDDEN',
      message: 'This value is forbidden',
      path,
      value
    };
  }
  return null;
});

const result = validateAndNormalize(document);
```

### Batch Validation

```typescript
import { validateAndNormalize } from '@ocd-tools/validator';
import fs from 'fs';
import path from 'path';

async function validateAllCharacters(directory: string) {
  const files = fs.readdirSync(directory);
  const results = [];

  for (const file of files) {
    if (file.endsWith('.yaml') || file.endsWith('.json')) {
      const content = fs.readFileSync(path.join(directory, file), 'utf8');
      const document = file.endsWith('.yaml') 
        ? require('js-yaml').load(content)
        : JSON.parse(content);
      
      const result = validateAndNormalize(document);
      results.push({ file, result });
    }
  }

  return results;
}
```

### Async Validation

```typescript
import { validateAndNormalizeAsync } from '@ocd-tools/validator';

// For large documents or complex validation
const result = await validateAndNormalizeAsync(document);
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

## Error Handling

### Try-Catch Pattern

```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

try {
  const result = validateAndNormalize(document);
  
  if (result.ok) {
    console.log('Validation successful');
    console.log('Normalized data:', result.data);
    console.log('Warnings:', result.warnings);
  } else {
    console.error('Validation failed');
    console.error('Errors:', result.errors);
  }
} catch (error) {
  console.error('Unexpected error:', error);
}
```

### Promise-Based Error Handling

```typescript
import { validateAndNormalizeAsync } from '@ocd-tools/validator';

validateAndNormalizeAsync(document)
  .then(result => {
    if (result.ok) {
      console.log('Success:', result.data);
    } else {
      console.error('Errors:', result.errors);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

## Performance Considerations

### Large Documents

For large character documents:

```typescript
import { validateAndNormalizeAsync } from '@ocd-tools/validator';

// Use async validation for large documents
const result = await validateAndNormalizeAsync(largeDocument);
```

### Memory Usage

```typescript
// For memory-constrained environments
import { validateAndNormalize, setMemoryLimit } from '@ocd-tools/validator';

setMemoryLimit(50 * 1024 * 1024); // 50MB limit
const result = validateAndNormalize(document);
```

## Dependencies

- `ajv>=8.0`: JSON Schema validation
- `js-yaml>=4.0`: YAML parsing support
- `@types/js-yaml`: TypeScript definitions

## Source Files

- `src/validate.ts` - Main validation logic
- `src/normalize.ts` - Normalization functions
- `src/warnings.ts` - Linting rules
- `src/types.ts` - TypeScript type definitions

## Migration from Python Validator

If migrating from the Python validator:

1. **API Differences**: JavaScript uses camelCase, Python uses snake_case
2. **Error Format**: Both use similar error codes but different object structures
3. **Async Support**: JavaScript validator supports async validation
4. **Type Safety**: TypeScript provides compile-time type checking

## Troubleshooting

### Common Issues

**Module not found:**
```bash
npm install @ocd-tools/validator
```

**TypeScript errors:**
```bash
npm install @types/node
```

**YAML parsing errors:**
```bash
npm install js-yaml
```

### Debug Mode

```typescript
import { validateAndNormalize, setDebugMode } from '@ocd-tools/validator';

setDebugMode(true);
const result = validateAndNormalize(document);
```

## What's Next?

- **[Python Validator](python-validator.md)**: Compare with Python implementation
- **[Agents & Runtime](agents.md)**: Integration with AI platforms
- **[Extensions](extensions-and-namespaces.md)**: Custom system support
- **[Examples](../authoring/examples.md)**: Character examples and templates
