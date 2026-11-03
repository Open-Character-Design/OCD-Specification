# Experimental x-career review fixtures (non-normative)

Source proposal: [OCD Issue #2](https://github.com/Open-Character-Design/OCD-Specification/issues/2). Placement review: [2026-11-03 architectural review](../../../docs/deep-dives/research/x-career-placement-review-2026-11-03.md).

These JSON files are **full-character, candidate core-schema examples** with the proposed `extras["x-career"]` namespace. Their extension fields illustrate the issue's experimental model. They are **not registered extensions, accepted conformance fixtures, or evidence of official Python/TypeScript validator parity**.

- `minimal-baker.json`: only a known occupation; unknown employer and education must not be invented.
- `scoped-scientist.json`: narrative-scoped engagements and education. `story_scope` is experimental, not an accepted time/continuity reference.
- `unpaid-caregiver.json`: nontraditional unpaid occupation without presumed employer, contract or earnings.

## Expected review checks

1. Independently run `jsonschema.Draft202012Validator.check_schema` and validate each full file against the pinned `spec/core.schema.json` commit recorded in the placement review.
2. Validate `extras["x-career"]` separately against the actual **published and pinned** experimental extension schema. That schema is not part of these fixtures; do not claim extension conformance in its absence.
3. Add negative mutations, contradictory evidence cases, multiple simultaneous jobs, missing employer, retrospective and prospective claims.
4. Record test results and exact versions before moving fixtures to an official conformance suite.

**Do not auto-promote these samples into normative core examples.**
