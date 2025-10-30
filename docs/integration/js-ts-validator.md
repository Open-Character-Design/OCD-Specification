# JavaScript/TypeScript Validator

The JavaScript/TypeScript validator provides validation, normalization, and diagnostics for OCD documents using the validation spec pipeline with Ajv and JSON Schema.

## Installation

Choose your preferred package manager:

=== "npm"

    ```bash
    npm install @ocd-tools/validator
    ```

=== "yarn"

    ```bash
    yarn add @ocd-tools/validator
    ```

=== "pnpm"

    ```bash
    pnpm add @ocd-tools/validator
    ```

=== "Global"

    ```bash
    npm install --global @ocd-tools/validator
    ```

Requires Node.js 18 or newer.

## Overview

The validator uses a flexible `.ocd` specification system that allows you to define custom validation rules. It supports two validation modes and provides comprehensive diagnostics through an evaluator-based pipeline.

### Validation Spec System

Validation uses `.ocd` specification files that define:
- **Rules**: Path-based validation rules with operators like `type`, `enum`, `presence`, etc.
- **Constraints**: High-level constraints like `require`, `forbid`, `disallow`
- **Definitions**: Reusable enums and types referenced with `@enums.Name` and `@types.Name`
- **Policy**: Controls how unknown fields and errors are handled

The validator pipeline includes:
1. **SpecLoader**: Loads and validates `.ocd` spec files (async)
2. **SpecMerger**: Merges multiple specs and resolves references
3. **PathMatcher**: Finds matching paths in documents using dot notation
4. **RuleEvaluator**: Evaluates rules and constraints, produces diagnostics
5. **Normalizer**: Normalizes trait names, slugs, tokens, etc.
6. **Linter**: Provides additional diagnostic warnings

## CLI Usage

```bash
# Validate a file (relaxed mode by default)
npx @ocd-tools/validator character.yaml

# Use strict validation mode
npx @ocd-tools/validator character.yaml --mode strict

# Use custom specification overlay
npx @ocd-tools/validator character.yaml --spec my-project-spec.ocd

# Combine mode and spec
npx @ocd-tools/validator character.yaml --mode strict --spec my-project-spec.ocd

# Print normalized output
npx @ocd-tools/validator character.yaml --print

# Treat warnings as errors
npx @ocd-tools/validator character.yaml --warnings-as-errors

# Force input format
npx @ocd-tools/validator character.yaml --format yaml

# Read from stdin
cat character.yaml | npx @ocd-tools/validator - --print
```

### CLI Options

```bash
@ocd-tools/validator [OPTIONS] PATH

Arguments:
  PATH  Path to an OCD document (YAML or JSON). Use '-' to read from standard input.

Options:
  -f, --format [auto|json|yaml]  Force the input parser. Defaults to 'auto'.
  --mode [relaxed|strict]        Validation mode (default: relaxed).
  --spec PATH                    Path to custom OCD specification overlay file.
  --output [text|json]           Output format for diagnostics (default: text).
  --print                        Print the normalized document to stdout on success.
  --indent INTEGER               Indent level to use when printing normalized JSON (default: 2).
  --warnings-as-errors           Exit with code 2 if any warnings are produced.
  -h, --help                     Show this message and exit.
  -v, --version                  Print the CLI version and exit.
```

### Exit Codes

- `0`: Validation succeeded
- `1`: Validation failed with errors
- `2`: Warnings were produced (when using `--warnings-as-errors`)

## Programmatic API

=== "TypeScript"

    ```typescript
    import { validateAndNormalize } from '@ocd-tools/validator';
    import { readFile } from 'node:fs/promises';
    import YAML from 'yaml';

    // Load a YAML document
    const raw = await readFile('character.yaml', 'utf8');
    const document = YAML.parse(raw);
    
    // Basic validation (relaxed mode)
    const result = await validateAndNormalize(document);
    
    // Strict validation mode
    const result = await validateAndNormalize(document, 'strict');
    
    // With custom specification overlay
    const result = await validateAndNormalize(document, 'relaxed', 'my-project-spec.ocd');
    
    // Combine mode and spec
    const result = await validateAndNormalize(document, 'strict', 'my-project-spec.ocd');
    
    if (result.ok) {
        console.log('Valid:', result.data);
        console.log('Warnings:', result.warnings);
    } else {
        console.log('Errors:', result.errors);
    }
    ```

=== "JavaScript (ESM)"

    ```javascript
    import { validateAndNormalize } from '@ocd-tools/validator';
    import { readFile } from 'node:fs/promises';
    import YAML from 'yaml';

    // Load and validate
    const raw = await readFile('character.yaml', 'utf8');
    const document = YAML.parse(raw);
    const result = await validateAndNormalize(document);
    ```

=== "JavaScript (CommonJS)"

    ```javascript
    const { validateAndNormalize } = require('@ocd-tools/validator');
    const fs = require('node:fs');
    const YAML = require('yaml');

    // Note: validateAndNormalize is async, wrap in async function
    async function validateCharacter() {
      const raw = fs.readFileSync('character.yaml', 'utf8');
      const document = YAML.parse(raw);
      const result = await validateAndNormalize(document);
    
    if (result.ok) {
        console.log('Valid:', result.data);
    } else {
        console.log('Errors:', result.errors);
    }
    }
```

## API Reference

### `validateAndNormalize(doc: any, mode?: 'relaxed' | 'strict', specPath?: string): Promise<Result<any>>`

Validates and normalizes an OCD document using the validation spec system.

**Parameters:**
- `doc`: The document to validate (object, array, or primitive)
- `mode`: Validation mode - "relaxed" (warnings for data errors) or "strict" (errors for all violations). Default: "relaxed"
- `specPath`: Optional path to custom `.ocd` specification file

**Returns:**
- `Promise<Result<any>>`: Result object with the following properties:
  - `ok: boolean`: Whether validation succeeded (no errors)
  - `data?: object`: Normalized document (present if `ok` is true)
  - `errors?: ValidationError[]`: Validation errors with `message`, `instancePath`, `schemaPath`, `keyword`, and `params` properties
  - `warnings: Warning[]`: Diagnostic warnings with `code`, `path`, and `detail` properties

**Type Definitions:**

```typescript
interface Result<T> {
  ok: boolean;
  data?: T;
  errors?: ValidationError[];
  warnings: Warning[];
}

interface ValidationError {
  message: string;
  instancePath: string;
  schemaPath: string;
  keyword: string;
  params: Record<string, unknown>;
}

interface Warning {
  code: string;
  path: string;
  detail: string;
}
```

**Example:**

```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

const document = {
  kind: "CharacterDefinition",
  ocd_version: "0.0.1",
  id: "char-123",
  slug: "example-character",
  names: { canon: "Example Character" },
  identity: {
    entity_kind: "person",
    sapience_level: "sapient"
  },
  meta: {
    versioning: {
      created_at: "2024-01-01T00:00:00Z",
      last_modified: "2024-01-01T00:00:00Z"
    }
  }
};

const result = await validateAndNormalize(document);
```

## Validation Modes

### Relaxed Mode (Default)

In relaxed mode:
- **Structure errors**: Always treated as errors (missing required fields, type mismatches)
- **Data errors**: Treated as warnings (enum violations, pattern mismatches, etc.)
- **Use case**: Development, prototyping, gradual validation adoption

### Strict Mode

In strict mode:
- **Structure errors**: Treated as errors
- **Data errors**: Treated as errors
- **Use case**: Production, CI/CD pipelines, strict compliance

## Custom Validation Specs

Create custom `.ocd` files to extend or override validation rules:

```yaml
id: my-project-spec
type: validationSpec
schemaVersion: 1
metadata:
  name: "My Project Validation"
  description: "Custom validation rules for my project"

policy:
  allowUnknownFields: true
  unknownFieldSeverity: warning

definitions:
  enums:
    Species: ["human", "elf", "dwarf", "orc"]

rules:
  - path: "identity.species"
    type: string
    enum: "@enums.Species"
    message: "Species must be from the allowed list"

constraints:
  require:
    - "names.canon"
    - "identity.entity_kind"
  
  disallow:
    tags: ["test", "draft"]
```

Use your custom spec:

```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

const result = await validateAndNormalize(document, 'relaxed', 'my-project-spec.ocd');
```

## Normalization

The validator performs the following normalizations automatically:

- **Bipolar trait names**: Canonicalize to `-` dash syntax (e.g., `introversion_extraversion` → `introversion-extraversion`)
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

## Integration Examples

### Express.js API

```typescript
import express from 'express';
import { validateAndNormalize } from '@ocd-tools/validator';
import { readFile } from 'node:fs/promises';
import YAML from 'yaml';

const app = express();
app.use(express.json());

app.post('/api/characters/validate', async (req, res) => {
  try {
    const result = await validateAndNormalize(req.body);
    
    if (result.ok) {
      return res.json({ 
        success: true,
        data: result.data,
        warnings: result.warnings 
      });
    } else {
      return res.status(400).json({ 
        success: false, 
        errors: result.errors 
      });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Validation failed', details: error });
  }
});

app.listen(3000);
```

### Next.js API Route

```typescript
// pages/api/validate-character.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { validateAndNormalize } from '@ocd-tools/validator';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const result = await validateAndNormalize(req.body);
    
    if (result.ok) {
      return res.json({ 
        success: true, 
        data: result.data,
        warnings: result.warnings 
      });
    } else {
      return res.status(400).json({ 
        success: false, 
        errors: result.errors 
      });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Validation failed' });
  }
}
```

### Batch Validation

```typescript
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { validateAndNormalize } from '@ocd-tools/validator';
import YAML from 'yaml';

async function validateDirectory(directory: string) {
  const results = { valid: [] as string[], invalid: [] as any[] };
  const files = await readdir(directory);
  
  for (const file of files) {
    if (file.endsWith('.yaml') || file.endsWith('.yml')) {
      const filePath = join(directory, file);
      const raw = await readFile(filePath, 'utf8');
      const document = YAML.parse(raw);
      const result = await validateAndNormalize(document);
      
      if (result.ok) {
        results.valid.push(file);
      } else {
        results.invalid.push({
          file,
          errors: result.errors
        });
      }
    }
  }
  
  return results;
}
```

## Dependencies

- `ajv>=8.17`: JSON Schema validation
- `ajv-formats>=2.1`: Format validation support
- `yaml>=2.4`: YAML parsing support
- `jsonpath-plus>=8.0`: Path matching for validation rules

## What's Next?

- **[Python Validator](python-validator.md)**: Compare with Python implementation
- **[Validation System](../validation/index.md)**: Learn about the validation spec system
- **[Spec Format Reference](../spec/ocd-specification-format.md)**: Details on `.ocd` file format
- **[Examples](../authoring/examples.md)**: Character examples and templates
