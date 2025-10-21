# OCD-T Authoring Guide

OCD-T is a concise textual notation that mirrors the JSON structure of an OCD document while remaining author-friendly. This guide covers both the grammar specification and practical authoring workflows.

## Overview

OCD-T is designed for approachable character writing that feeds the same canonical data consumed by JSON and YAML pipelines. It provides a deterministic mapping to JSON objects while maintaining human readability.

### Goals

- Provide a deterministic mapping to JSON objects
- Reject duplicate object keys (enforced via parser or post-pass)
- Preserve canonical trait axes using the Unicode double arrow (`-`)
- Support human-friendly authoring with comments and flexible formatting

## Document Structure

1. A header with `ocd-t: <integer>` indicating the grammar revision
2. An optional `ocd-version: "<semver>"` header
3. A root object enclosed in `{ ... }` using relaxed punctuation rules (commas are optional before newlines; trailing commas permitted)

Whitespace is insignificant. Comments use `# ...` to end of line.

## Values

- Strings use double quotes with standard JSON escape rules
- Bare identifiers are permitted for simple keys and enum-like values
- Numbers follow JSON number syntax
- Arrays are enclosed in `[ ... ]` and support trailing commas

## Trait Axis Normalization

When the parser encounters a bipolar trait `name`, it MUST normalize ASCII separators (`-`, `_`) to the Unicode double arrow if both sides of the separator contain text. Producers SHOULD already use `-`.

## Duplicate Key Policy

The grammar itself is lenient, but tooling MUST perform a duplicate-key check after parsing. Duplicated keys MUST raise a parse error with source spans identifying each duplicate occurrence.

## Key Grammar Points

- UTF-8, line and block comments, triple-quoted strings
- Trailing commas allowed in objects/arrays
- Duplicate keys **rejected**
- Trait `kind`: `bipolar | scalar | flag`
- `-`, `-`, `_` accepted for axis; canonicalize to `-`

## Authoring Workflow

1. **Start with a preamble** (optional) that declares document metadata:
   ```ocd
   ocd-t: 1
   ocd-version: 0.9
   ```

2. **Define your base character block** using `character "Name" { ... }`

3. **Add traits and stats** as objects or arrays. Trailing commas are allowed

4. **Attach extensions** with `character "Name" extension identifier { ... }` to layer campaign-specific or localized data

5. **Use multiline strings** for long-form biographies or scripts. The parser trims shared indentation while preserving internal newlines

6. **Validate against the grammar** by checking that each construct aligns with the corresponding production rules

## Grammar Examples

### Multi-block Characters

Multi-block characters are parsed by the `CharacterDocument` rule, which permits multiple `CharacterBlock` entries separated by blank lines. Each block collects localized metadata and trait declarations.

```ocd
# CharacterDocument → CharacterBlock+

character "Apex Operative" {
  id: "apex"
  traits: [
    { trait-id: "combat", kind: bipolar, axis: "-" }
  ]
}

character "Apex Operative" extension campaign {
  # CharacterBlock → CharacterHeader CharacterBody
  version: 2
  campaign-notes: "Operates covertly in the Reach."
}

character "Apex Operative" extension downtime {
  # Additional CharacterBlock appended to the document
  downtime-log: ["Patrol", "Intel gathering"]
}
```

### Multiline Strings

Triple-quoted strings feed into the `MultilineString` production and preserve line breaks after the common indentation is stripped. They are useful for structured text, such as monologues or lore excerpts.

```ocd
bio: """
  MultilineString → """ MultilineContent """

  Once a decorated knight,
  now a wandering sellsword.

  Known associates:
    • Cirian
    • Lys
"""
```

### Nested Extensions

Extensions can contain further nested extension blocks as modeled by the `ExtensionBlock` rule. Each nested block adds scoping metadata while inheriting the parent character context.

```ocd
character "Kestrel" {
  id: "kestrel"
}

character "Kestrel" extension seasonal {
  extension winter-court {
    # ExtensionBlock → "extension" Identifier CharacterBody
    court-role: "Envoy"

    extension mission {
      # Nested ExtensionBlock, still under CharacterDocument
      assignment: "Broker peace with the Mossguard"
    }
  }
}
```

## Step-by-Step Example

The following walk-through highlights how each section of an OCD-T file maps to the grammar:

```ocd
# Preamble → PreambleLine+
ocd-t: 1
ocd-version: 0.9

# CharacterDocument → CharacterBlock+
character "Kestrel" {
  id: "kestrel"
  traits: [
    { trait-id: "combat", kind: bipolar, axis: "-" },
    { trait-id: "tactics", kind: scalar, value: 5 }
  ]

  bio: """
    Field-tested scout with an eye for detail.
    Prefers swift strikes and minimal collateral.
  """
}

character "Kestrel" extension seasonal {
  extension winter-court {
    court-role: "Envoy"
  }
}
```

Each comment labels the rule that governs the following block, enabling a direct comparison to the grammar reference.

## Round-tripping between OCD-T and JSON/YAML

Because the grammar normalizes whitespace and ordering, OCD-T snippets round-trip losslessly to structured formats.

### OCD-T → JSON

```json
{
  "ocd-t": 1,
  "ocd-version": 0.9,
  "characters": [
    {
      "name": "Kestrel",
      "id": "kestrel",
      "traits": [
        { "trait-id": "combat", "kind": "bipolar", "axis": "-" },
        { "trait-id": "tactics", "kind": "scalar", "value": 5 }
      ],
      "bio": "Field-tested scout with an eye for detail.\nPrefers swift strikes and minimal collateral."
    },
    {
      "name": "Kestrel",
      "extension": [
        {
          "identifier": "seasonal",
          "body": {
            "extension": [
              {
                "identifier": "winter-court",
                "body": {
                  "court-role": "Envoy"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### OCD-T → YAML

```yaml
ocd-t: 1
ocd-version: 0.9
characters:
  - name: Kestrel
    id: kestrel
    traits:
      - trait-id: combat
        kind: bipolar
        axis: "-"
      - trait-id: tactics
        kind: scalar
        value: 5
    bio: |-
      Field-tested scout with an eye for detail.
      Prefers swift strikes and minimal collateral.
  - name: Kestrel
    extension:
      - identifier: seasonal
        body:
          extension:
            - identifier: winter-court
              body:
                court-role: Envoy
```

You can verify the round-trip by parsing the OCD-T file with the grammar and then serializing to JSON or YAML using your tooling of choice. When converting back into OCD-T, follow the authoring workflow above and cross-reference the grammar rules to ensure every construct aligns with its parser rule.

## Future Work (TODO)

- Implement complete Peggy grammar covering all constructs
- Emit structured diagnostics with line/column spans
- Support import/include directives
