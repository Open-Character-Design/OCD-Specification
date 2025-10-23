# Trait Model

The trait model captures how a character expresses tendencies, aptitudes, and toggles that feed into runtime prompt
conditioning. Validators normalize values and ensure trait names align with the
[controlled vocabularies](../reference/vocabularies.md) so cross-title analytics remain consistent.

!!! info "Deep Dive: Trait Model Design"
    For comprehensive technical analysis of the trait model architecture and design decisions, see the [Trait Model Design Rationale](../../deep-dives/white-papers/trait-model-design.md) white paper.

!!! tip "Research Foundation"
    The trait model is based on research into universal character definition fields across all mediums. See [Common Character Definition Fields Across All Mediums](../../deep-dives/research/common-character-fields.md) for the theoretical foundation.

## Kinds

- **Bipolar**: `{ name, kind: bipolar, polarity: [-1..1], intensity: [0..1] }`
  - Use for axes like `introversion-extraversion` or `logic-intuition` where positive polarity leans toward the second
    term.
- **Scalar**: `{ name, kind: scalar, value: [0..1], unit? }`
  - Ideal for proficiencies (`empathy`, `combat-readiness`) or environmental tolerances.
- **Flag**: `{ name, kind: flag, value: boolean }`
  - Encodes binary capabilities such as `psionic`, `licensed-medic`, or `spoiler-reveal-enabled`.

## Normalization & Validation

- Use `-` between bipolar poles (e.g., `introversion-extraversion`). Validators accept `-` and `_` separators but emit the
  canonical `-` separator during normalization to avoid diff churn.
- Validators lower-case trait names, dedupe repeats, and enforce value ranges. See
  [Python validator](../integration/python-validator.md) and
  [JS/TS validator](../integration/js-ts-validator.md) behavior notes for normalization specifics.
- Diagnostics such as `RATING_CONFLICT` surface when trait-driven tone (e.g., `violent-pacifist` leaning violent) is at
  odds with `meta.appropriateness`. Review the [diagnostics reference](../reference/diagnostics.md) when tuning
  personas.

## Modeling Strategies

- **Anchor to motivations.** Combine bipolar traits with scalar goals to represent tensions (e.g., `duty-desire` with a
  scalar `loyalty` score).
- **Bundle instincts.** Use `personality.instincts[]` to capture if/then reflexes ("crack a joke when tension is high")
  that complement numeric traits.
- **Expose toggles explicitly.** Flags provide runtime switches ("may break fourth wall") that orchestrators can flip.

## Case Studies

### Diana Prince / Wonder Woman

- **Bipolar Axes.** `compassion-indifference: polarity 0.85`, `tradition-innovation: polarity 0.3`. High compassion paired
  with a moderate tilt toward tradition guides tone, particularly when dialogue style references the
  [behavior register vocabulary](../reference/vocabularies.md).
- **Scalar Competencies.** `combat-readiness: 0.95`, `diplomacy: 0.8` offer knobs for encounter balancing. Validators
  ensure scalar values stay within `[0..1]` and surface lint if units are mismatched.
- **Flags.** `lasso-of-truth-enabled: true` allows rule systems to branch when the signature tool is accessible.

### Bruce Wayne / Batman

- **Dual Identity Calibration.** Traits split between personas using tags (e.g., `tags: [bruce-wayne]`) so orchestration
  layers can swap in `confidence-doubt: polarity 0.6` for Bruce while Batman leans toward `justice-vengeance: polarity
  0.75` with `intensity 0.9`.
- **Validator Feedback.** If a designer pairs a `violence` leaning trait with a `violence: none` rating, the validators
  emit `RATING_CONFLICT`, prompting either trait adjustment or rating escalation.
- **Integration.** Scalar `detective-insight: 0.92` feeds [agent memory retrieval pipelines](../integration/python-validator.md)
  that weight investigative leads more heavily during prompt assembly.
