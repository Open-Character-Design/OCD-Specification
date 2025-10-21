# Open Character Specification (OCD) v1.0

OCD is a portable, machine-validated format for character definitions across games, film/TV, books, and AI role-play.

It ships with:
- **Core schema** (JSON Schema v1.0) and **Legend & Adoption Guide**
- **OCD-T**: a concise textual grammar for authoring with full parser support
- **Python validator** (Pydantic v2) with normalization & lint
- **TypeScript validator** (Ajv) with full feature parity
- **Examples** in YAML and OCD-T

## Quick Start

### Python

```bash
pip install ocd==1.0.0

# Validate a document and print the normalized JSON
ocd-validate examples/bruenor.yaml --print
```

### Node.js

```bash
npm install @ocd-tools/validator@1.0.0

# Validate using the packaged CLI
npx @ocd-tools/validator examples/bruenor.yaml --print

# Or install globally
npm install --global @ocd-tools/validator@1.0.0
ocd-validate examples/bruenor.yaml --print
```

Structure

spec/ – schemas and docs

grammar/ – OCD-T spec and grammar

python/ – validator library & CLI (publishable as `ocd`) and tests

node/ – JS/TS validator, parser, and CLI tooling (publishable as `@ocd-tools/validator`)

examples/ – sample characters (YAML/OCD-T)


Licensing

Code: Apache-2.0 (LICENSES/LICENSE-CODE-Apache-2.0.txt)

Specs & docs: CC-BY-4.0 (LICENSES/LICENSE-SPEC-CC-BY-4.0.txt)
