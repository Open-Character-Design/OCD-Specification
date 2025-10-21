# OCD-T Authoring Guide

OCD-T is designed for approachable character writing that still feeds the same
canonical data consumed by JSON and YAML pipelines. For the full grammar rules
refer to [OCD-T Grammar](../spec/grammar-ocd.md), which annotates examples with
production names from `grammar/OCD-T-spec.md` so you can map what you type to
what the parser expects.

## Authoring workflow

1. **Start with a preamble** (optional) that declares document metadata.
   ```ocd
   ocd-t: 1
   ocd-version: 0.9
   ```
2. **Define your base character block** using `character "Name" { ... }`.
3. **Add traits and stats** as objects or arrays. Trailing commas are allowed.
4. **Attach extensions** with `character "Name" extension identifier { ... }` to
   layer campaign-specific or localized data.
5. **Use multiline strings** for long-form biographies or scripts. The parser
   trims shared indentation while preserving internal newlines.
6. **Validate against the grammar** by checking that each construct aligns with
   the corresponding production in `grammar/OCD-T-spec.md` (for example,
   `CharacterBody`, `TraitObject`, or `ExtensionBlock`).

## Step-by-step example

The following walk-through highlights how each section of an OCD-T file maps to
the grammar.

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

Each comment labels the rule that governs the following block, enabling a direct
comparison to the grammar reference.

## Round-tripping between OCD-T and JSON/YAML

Because the grammar normalizes whitespace and ordering, the OCD-T snippet above
round-trips losslessly to structured formats.

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

You can verify the round-trip by parsing the OCD-T file with the grammar and
then serializing to JSON or YAML using your tooling of choice. When converting
back into OCD-T, follow the authoring workflow above and cross-reference the
[OCD-T Grammar](../spec/grammar-ocd.md) to ensure every construct aligns with
its parser rule.
