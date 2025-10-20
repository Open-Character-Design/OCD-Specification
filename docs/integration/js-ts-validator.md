# JavaScript/TypeScript Validator

The JavaScript/TypeScript validator provides comprehensive validation, normalization, and diagnostics for OCS documents using Ajv and JSON Schema.

## Installation

Choose your preferred package manager:

=== "npm"

    ```bash
    npm install @ocs-tools/validator@1.0.0
    ```

=== "yarn"

    ```bash
    yarn add @ocs-tools/validator@1.0.0
    ```

=== "pnpm"

    ```bash
    pnpm add @ocs-tools/validator@1.0.0
    ```

=== "Global Installation"

    ```bash
    npm install --global @ocs-tools/validator@1.0.0
    ```

## Usage

### CLI

```bash
# Validate a file
npx @ocs-tools/validator character.yaml

# Print normalized output
npx @ocs-tools/validator character.yaml --print

# Treat warnings as errors
npx @ocs-tools/validator character.yaml --warnings-as-errors

# Force input format
npx @ocs-tools/validator character.yaml --format yaml
```

### Programmatic API

=== "TypeScript"

    ```typescript
    import { validateAndNormalize } from '@ocs-tools/validator';
    
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
    const { validateAndNormalize } = require('@ocs-tools/validator');
    
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
    import { validateAndNormalize } from '@ocs-tools/validator';
    
    const result = await validateAndNormalize(document);
    ```

### CLI Options

```bash
@ocs-tools/validator [OPTIONS] PATH

Arguments:
  PATH  Path to an OCS document (YAML or JSON). Use '-' to read from standard input.

Options:
  --format [auto|json|yaml]  Force the input parser. Defaults to 'auto'.
  --print                    Print the normalized document to stdout on success.
  --indent INTEGER           Indent level to use when printing normalized JSON (default: 2).
  --warnings-as-errors       Exit with code 2 if any warnings are produced.
  --help                     Show this message and exit.
```

## API Reference

### `validateAndNormalize(doc: any): ValidationResult`

Validates and normalizes an OCS document.

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
import { validateAndNormalize } from '@ocs-tools/validator';

const document = {
  ocs_version: "1.0.0",
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
import { validateAndNormalize } from '@ocs-tools/validator';

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
import { validateAndNormalize } from '@ocs-tools/validator';

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
import { validateAndNormalize } from '@ocs-tools/validator';

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
import { validateAndNormalize } from '@ocs-tools/validator';

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
import { validateAndNormalize, addCustomValidator } from '@ocs-tools/validator';

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
import { validateAndNormalize } from '@ocs-tools/validator';
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
import { validateAndNormalizeAsync } from '@ocs-tools/validator';

// For large documents or complex validation
const result = await validateAndNormalizeAsync(document);
```

## Normalization

The validator performs the following normalizations:

- **Bipolar trait names**: Canonicalize to `↔` arrow syntax
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
import { validateAndNormalize } from '@ocs-tools/validator';

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
import { validateAndNormalizeAsync } from '@ocs-tools/validator';

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
import { validateAndNormalizeAsync } from '@ocs-tools/validator';

// Use async validation for large documents
const result = await validateAndNormalizeAsync(largeDocument);
```

### Memory Usage

```typescript
// For memory-constrained environments
import { validateAndNormalize, setMemoryLimit } from '@ocs-tools/validator';

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
npm install @ocs-tools/validator
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
import { validateAndNormalize, setDebugMode } from '@ocs-tools/validator';

setDebugMode(true);
const result = validateAndNormalize(document);
```

## What's Next?

- **[Python Validator](python-validator.md)**: Compare with Python implementation
- **[Agents & Runtime](agents.md)**: Integration with AI platforms
- **[Extensions](extensions-and-namespaces.md)**: Custom system support
- **[Examples](../authoring/examples.md)**: Character examples and templates