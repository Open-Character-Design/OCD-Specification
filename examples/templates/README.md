# Example Payload Templates

Use these templates as starting points when introducing new examples or fixtures to the repository. Each template highlights the
minimum fields required by the specification along with optional metadata that improves interoperability across tooling.

## Minimal Character Format

The OCD specification supports a minimal character format that requires only three fields. This format is perfect for quick character creation and will be automatically expanded to the full format by validators in future releases.

- `character-lite.json`: Minimal JSON payload with only `name`, `type`, and `summary` fields.
- `character-lite.yaml`: Minimal YAML payload with only `name`, `type`, and `summary` fields.

### Minimal Format Fields

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `name` | string | Character's canonical name | Non-empty string |
| `type` | string | Entity type | `person`, `collective`, `creature`, `object`, `place`, `abstract`, `ai` |
| `summary` | string | Brief character description | Non-empty string |

### Field Mappings

When expanded to the full format, minimal fields map as follows:

- `name` → `names.canon`
- `type` → `identity.entity_kind`
- `summary` → top-level `summary` field

### Auto-population (Future Feature)

Future validator releases will automatically generate these required fields:

- `ocd_version` = "1.0.0"
- `id` = random UUID v4
- `kind` = "CharacterDefinition"
- `slug` = slugified version of name
- `identity.sapience_level` = "sapient" (sensible default)
- `meta.versioning.created_at` = current timestamp
- `meta.versioning.last_modified` = current timestamp

## Full Format Templates

- `character-full.json`: Comprehensive payload exercising optional and extension fields.

## Contributing Guidelines

When contributing new examples:

1. **For minimal characters**: Use `character-lite.json` or `character-lite.yaml` as your starting point.
2. **For full characters**: Copy the appropriate template (`character-lite.json` for minimal, `character-full.json` for comprehensive).
3. Replace placeholder values with realistic data representing your scenario.
4. Update extension sections if your proposal introduces `x-*` fields.
5. Validate the payload with the official tooling before opening a pull request.
