# OCD Validation Spec — Test Fixtures

## Validate the *validation spec* files against the JSON Schema
- `tests/specs/ocd-default-spec.ocd` ✅ should pass
- `tests/specs/project-fantasy-spec.ocd` ✅ should pass
- `tests/specs/invalid-spec-missing-type.ocd` ❌ should fail

## Validate *character* files using the specs
- Relaxed mode treats data issues as warnings by default; structure issues still error.
- Strict mode treats data and structure issues as errors.

## Example CLI
```bash
# Spec schema check (implement both Python/Node flavors)
ajv validate -s schema/ocd-validation-spec.schema.json -d tests/specs/ocd-default-spec.ocd

# Character validation (your validator)
ocd-validate tests/characters/valid/hero_fantasy.yaml --mode strict --spec tests/specs/project-fantasy-spec.ocd
```
