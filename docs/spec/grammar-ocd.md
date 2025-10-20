# OCD-T Grammar

OCD-T is a compact textual authoring format that round-trips to JSON/YAML and
is fully described in the canonical grammar at `grammar/OCD-T-spec.md`. The
parser implementation is being iterated at `grammar/ocs-t.peggy`, so examples
below reference rule names from the finalized grammar to highlight the mapping
between syntax and parser behavior.

## Key points

- UTF-8, line and block comments, triple-quoted strings
- Trailing commas allowed in objects/arrays
- Duplicate keys **rejected**
- Trait `kind`: `bipolar | scalar | flag`
- `↔`, `-`, `_` accepted for axis; canonicalize to `↔`

## Annotated examples

### Multi-block characters

Multi-block characters are parsed by the `CharacterDocument` rule, which
permits multiple `CharacterBlock` entries separated by blank lines. Each block
collects localized metadata and trait declarations.

```ocst
# CharacterDocument → CharacterBlock+

character "Apex Operative" {
  id: "apex"
  traits: [
    { trait-id: "combat", kind: bipolar, axis: "↔" }
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

### Multiline strings

Triple-quoted strings feed into the `MultilineString` production and preserve
line breaks after the common indentation is stripped. They are useful for
structured text, such as monologues or lore excerpts.

```ocst
bio: """
  MultilineString → """ MultilineContent """

  Once a decorated knight,
  now a wandering sellsword.

  Known associates:
    • Cirian
    • Lys
"""
```

### Nested extensions

Extensions can contain further nested extension blocks as modeled by the
`ExtensionBlock` rule. Each nested block adds scoping metadata while inheriting
the parent character context.

```ocst
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

Refer back to `grammar/OCD-T-spec.md` for the authoritative description of the
rules referenced in each annotation.
