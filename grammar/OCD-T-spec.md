# OCD-T Text Format (Draft)

OCD-T is a concise textual notation that mirrors the JSON structure of an
OCS document while remaining author friendly. This draft captures the
lexical expectations and normalisation rules that downstream parsers MUST
honour.

## Goals

- Provide a deterministic mapping to JSON objects.
- Reject duplicate object keys (enforced via parser or post-pass).
- Preserve canonical trait axes using the Unicode double arrow (`↔`).

## Document Structure

1. A header with `ocd-t: <integer>` indicating the grammar revision.
2. An optional `ocs-version: "<semver>"` header.
3. A root object enclosed in `{ ... }` using relaxed punctuation rules
   (commas are optional before newlines; trailing commas permitted).

Whitespace is insignificant. Comments use `# ...` to end of line.

## Values

- Strings use double quotes with standard JSON escape rules.
- Bare identifiers are permitted for simple keys and enum-like values.
- Numbers follow JSON number syntax.
- Arrays are enclosed in `[ ... ]` and support trailing commas.

## Trait Axis Normalisation

When the parser encounters a bipolar trait `name`, it MUST normalise
ASCII separators (`-`, `_`) to the Unicode double arrow if both sides of
the separator contain text. Producers SHOULD already use `↔`.

## Duplicate Key Policy

The grammar itself is lenient, but tooling MUST perform a duplicate-key
check after parsing. Duplicated keys MUST raise a parse error with source
spans identifying each duplicate occurrence.

## Future Work (TODO)

- Implement complete Peggy grammar covering all constructs.
- Emit structured diagnostics with line/column spans.
- Support import/include directives.
