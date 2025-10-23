# @ocd-tools/validator

The `@ocd-tools/validator` package delivers the Open Character Design Specification validator, parser, and command line tooling for Node.js consumers.

## Installation

```bash
npm install @ocd-tools/validator
# or
pnpm add @ocd-tools/validator
# or
yarn add @ocd-tools/validator
```

Node.js 18 or newer is required.

## Command Line Interface

The package exposes the `ocd-validate` executable. Use it directly or through `npx`:

```bash
# Validate a document and print the normalized output
npx @ocd-tools/validator --print examples/bruenor.yaml

# Use strict validation mode
npx @ocd-tools/validator --mode strict examples/bruenor.yaml

# Use custom specification overlay
npx @ocd-tools/validator --spec my-project-spec.ocd examples/bruenor.yaml

# Treat warnings as build failures
npx @ocd-tools/validator --warnings-as-errors examples/bruenor.yaml
```

CLI flags mirror the Python tooling:

- `-f, --format <auto|json|yaml>` – override format detection.
- `--mode <relaxed|strict>` – validation mode (default: relaxed).
- `--spec <path>` – path to custom OCD specification overlay file.
- `--print` – write normalized JSON to standard output.
- `--indent <n>` – adjust indentation when printing (default: 2).
- `--warnings-as-errors` – return exit code 2 when lint warnings are emitted.

Pass `-` as the path argument to read from standard input.

## Programmatic Usage

```ts
import { validateAndNormalize } from '@ocd-tools/validator';
import { readFile } from 'node:fs/promises';
import YAML from 'yaml';

const raw = await readFile('examples/bruenor.yaml', 'utf8');
const doc = YAML.parse(raw);

// Basic validation (relaxed mode)
const result = await validateAndNormalize(doc);

// Strict validation mode
const result = await validateAndNormalize(doc, 'strict');

// With custom specification overlay
const result = await validateAndNormalize(doc, 'relaxed', 'my-project-spec.ocd');

if (result.ok) {
  console.log('normalized character', result.data);
  console.log('warnings', result.warnings);
} else {
  console.error('validation errors', result.errors);
}
```

The package provides comprehensive validation with support for custom specification overlays.
