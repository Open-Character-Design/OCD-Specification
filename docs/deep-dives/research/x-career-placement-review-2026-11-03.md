# Career placement in OCD — architectural review

> **Status:** Proposal / architectural research (non-normative)  
> **Reviewed:** 2026-11-03  
> **Source:** [Issue #2 — x-career](https://github.com/Open-Character-Design/OCD-Specification/issues/2)  
> **Decision:** Open; no approval, registry entry, schema promotion, or validator conformance implied  
> **Next review trigger:** Maintainer feedback, candidate conformance results, or a relevant core/extension schema change

## Question and stakes

Should a character's career belong under **Background**, **Roles**, a dedicated top-level **Career** component, or remain a separate extension? A useful answer needs to preserve character identity and continuity without confusing occupation, job engagement, narrative function, or current runtime state.

This review is a recommendation for discussion, **not an accepted architectural decision**. It does not change `spec/core.schema.json`, register `x-career`, or establish new normative semantics.

## Current repo evidence (2026-11-03)

- [Core schema](../../../spec/core.schema.json) (`spec/core.schema.json`, blob `4a3fba32091b60b022059ae2e02b3918bddee09c`) defines `identity.roles` as **narrative functions**, with enum `protagonist | antagonist | support | ensemble | npc | avatar`. It does not define occupational or employment roles.
- The same schema defines `background.education` as `string[]` and includes `background.significant_events`, `affiliations`, and `milestones`. `background` currently allows additional properties, but that alone does not standardize a career shape.
- `CharacterDefinition` rejects unrecognized top-level properties (`additionalProperties: false`) and permits open extension data in `extras`. Thus `extras["x-career"]` is the compatible **incubation path** for this core-schema version. Core validation does **not** establish validity of any extension payload.
- [Extension documentation](../../integration/extensions-and-namespaces.md) illustrates top-level `x-*` fields; this conflicts with `CharacterDefinition` validation and needs correction or explicit scoping. Do not silently change the core schema to match the examples.
- [Governance guidance](../../governance/contributing-to-spec.md) requires review before extension registration or core promotion. No sponsor or approval is established by this review.
- [Issue #2](https://github.com/Open-Character-Design/OCD-Specification/issues/2) describes an experimental `x-career` v0.3 and local tests. Those results are **reported by the proposer**, not independent upstream CI, official validator parity, or an accepted extension.

## Candidate semantic boundaries

| Concept | Meaning | Recommended owner / representation |
| --- | --- | --- |
| Narrative role | Character's function in a narrative or interaction | Existing `identity.roles` (unchanged) |
| Occupation / vocation | Professional or occupational identity, independent of particular jobs | `x-career.occupations[]` during incubation |
| Employment / engagement | A job or service engagement, potentially with employer, title, arrangement and scope | `x-career.employment[]` during incubation |
| Education / qualifications | Academic or professional credentials and study | `x-career.education[]` experimentally; reconcile with `background.education` |
| Career event | Hire, separation, retraining, career change, retirement | `x-career.career_events[]`, linked to continuity and narrative time |
| Occupational role *view* | A consumer-facing label such as "physician" or "baker" | Derive from career facts only where supported; not a second writable source |
| Runtime work status | Temporary, session-specific facts about a character | Runtime state; never silently promote to character canon |
| Provenance / uncertainty | Evidence and whether a claim is disputed, unknown or perspective-specific | Reuse or coordinate with a shared provenance/continuity scheme; do not duplicate competing canonical models |

Key invariants: **occupation ≠ employment ≠ narrative role**; **unknown employer ≠ no employer**; **no recorded employment ≠ unemployed**; a change in career must not automatically change canonical character identity. Compensations and occupational disclosures may require audience-specific handling.

## Options and tradeoffs

### A. Background-linked career component (provisional preference)

**Candidate eventual home:** `background.career`, or a structured reference from `background` to a reusable career component.

- **Pros:** The existing `background` already groups education, affiliations, events and milestones; career history naturally belongs to the character's life record. No change to narrative role semantics.
- **Cons:** Background can read as exclusively historical, while career also includes active employment, preferences, future aspirations and audience-sensitive compensation. Large subcomponents could overburden Background.
- **Compatibility:** Would require a specified schema, migration/projection from `extras["x-career"]`, and a policy for `background.education`; current permissive additional properties are not a substitute for validation.

### B. Roles-based career representation

**Candidate:** `roles.career` under a *newly designed* role taxonomy, **not** appending occupations to the existing narrative `identity.roles` enum.

- **Pros:** Supports a compact "what does this character do?" lookup and may generalize to social, civic, or organizational roles.
- **Cons:** A role label cannot represent education, employer engagements, compensation or multi-stage history without expanding Roles into an unrelated life-history system. Risks mixing narrative function with occupational identity.
- **Compatibility:** Alters role ontology, validators and consumers; must not repurpose existing enum values.

### C. Dedicated top-level career component

- **Pros:** Strong domain ownership and clean structure for rich career information, especially if actively used by non-narrative applications.
- **Cons:** Adds a core field and increases complexity for characters with no career information; needs evidence of cross-media generality and migration guidance.
- **Compatibility:** Potential additive future core change, subject to governance.

### D. Continue with optional `x-career` indefinitely

- **Pros:** No immediate core compatibility impact; enables experiments.
- **Cons:** Fragmentation and discoverability if multiple tools independently interpret career semantics; consistent validation and projection are still required.

## Proposed direction — not approved

1. **Incubate** in `CharacterDefinition.extras["x-career"]` while collecting evidence and conformance results. Keep every extension section optional; never fabricate records to fill templates.
2. **Prefer Background linkage over Roles** for the **full career domain**, since this is about a person's life, qualifications and history, not narrative function. Treat `background.career` only as a **candidate** later location, not a currently accepted core field.
3. **Preserve `identity.roles` untouched.** If occupational roles need cross-domain query support, design a derived read-only occupational view or a separate role ontology after defining its semantics.
4. **Do not decide the final physical path before testing.** Reevaluate a dedicated top-level `career` component if active/future-oriented use cases prove that `background` is an artificial container.
5. **One source of truth per fact.** If `background.education` is retained for legacy consumers, define a deterministic, clearly lossy projection from structured education rather than bidirectionally editable copies. Do not silently override deliberate creator-authored data.
6. **Keep temporal/continuity claims explicit:** current vs historical vs aspirational, canonical timeline vs adaptation, dated vs story-scoped; facts inferred or generated by AI remain unconfirmed unless deliberately accepted.
7. **Separate content from disclosure.** Compensation and confidential work histories should not imply public exposure merely because a schema accepts them.

## Experimental fixture and conformance plan

Companion **non-normative** samples:
- [Minimal baker](../../../examples/experimental/x-career/minimal-baker.json) — occupation without an employer, education or invented timeline.
- [Scoped scientist](../../../examples/experimental/x-career/scoped-scientist.json) — structured education and a career transition in different narrative scopes.
- [Unpaid caregiver](../../../examples/experimental/x-career/unpaid-caregiver.json) — an occupation/vocation without paid employment.

These files are deliberately not placed in the official conformance fixture directory. They are candidates for independent review. **No official validator parity or x-career v0.3 extension conformance is claimed here.**

| Test / user case | Expected behavior |
| --- | --- |
| Basic occupation, no employer | Valid sparse payload; do not invent employment |
| Self-employed, unpaid caregiver, student, retired | Differentiate roles and transitions without mandating an organization |
| Known position, unknown employer | Preserve the known position without hallucinating an employer |
| Two simultaneous jobs | No uniqueness rule that forbids overlapping engagements |
| Multiple timelines or adaptations | Do not collapse incompatible scoped claims into one canonical present |
| Hire, separation, return, retraining | Chronology and scope remain attributable, not overwritten by the latest event |
| Unknown, disputed, inferred facts | Preserve status and provenance according to shared OCD conventions |
| Education duplicated in core and extension | Define authoritative source, projection, conflict handling, lossiness |
| Sensitive compensation | Require explicit audience/presentation policy outside base recording |
| Minimal / full schema | Validate root `CharacterDefinition` against pinned upstream core |
| Extension payload | Validate independently against a pinned, published experimental `x-career` schema |
| Invalid mutations | Reject wrong data types, invalid states and malformed chronology according to proposed extension rules |
| Official implementation parity | Compare Python / TypeScript (and future languages) on positive/negative tests |

### Gates before candidate advancement

- [ ] Confirm namespace placement and external extension-schema discovery/version pinning.
- [ ] Review the full experimental v0.3 schema and publish it with its source revision.
- [ ] Validate byte-for-byte samples against pinned core schema and experimental extension schema.
- [ ] Add independent negative cases; record commands, environment, exact results and date.
- [ ] Resolve education data ownership and temporal/provenance representation.
- [ ] Demonstrate utility for at least two media/application domains and minimal-data use.
- [ ] Obtain documented maintainer review, agreed sponsor if applicable, compatibility plan, and migration guidance.

## Decision record (pending)

- **ID:** PROPOSED-CAREER-PLACEMENT-2026-11-03
- **Status:** proposed; not accepted
- **Question:** Full Career domain: Background, Roles, standalone core component, or extension-only?
- **Provisional recommendation:** Background-linked domain; keep current representation `extras["x-career"]`.
- **Alternatives:** Roles taxonomy, top-level Career, extension-only.
- **Compatibility:** Additive experimental representation only today; any core promotion requires review/migration.
- **Open risks:** The distinction between active/current employment and background history; ambiguous career-vs-role semantics; education duplication; provenance and privacy; unverified extension validator claims.
- **Decision owner:** Not assigned. Do not infer a Core Approval Team sponsor or acceptance.
- **Review trigger:** Substantive feedback on Issue #2, conformance evidence, or core schema/registry decisions.
