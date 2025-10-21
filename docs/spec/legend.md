# Legend & Adoption Guide (v0.2)

> Source of truth is maintained in the repo’s legend doc. This page mirrors and summarizes it.

- **Blocks**: see [`spec/legend.md`](legend.md) for the full
  explanation of root entities, required keys, and optional payloads.
- **Traits**: OCD supports `bipolar`, `scalar`, `categorical`, `flag`, and
  `profile` trait kinds; consult the legend for value ranges and
  normalisation rules.
- **Composite identities**: `identity.composite_of` encodes pilot/mech,
  symbiote, and hivemind arrangements with control shares and exposure
  metadata.
- **Normalization**: validators canonicalise slugs (`⇒`/`_` → `-`), dedupe
  array tokens, and require ISO 8601 timestamps under `meta.versioning`.
- **Conformance**: use `python tools/ocd-validate.py` (and the forthcoming
  Node CLI) to check schema compliance and lint feedback.

Refer to `spec/legend-and-adoption-guide.md` for adoption checklists,
example workflows, and validator onboarding tips.
