# Contributing to the Spec

OpenCharacter Specification (OCD) contributions follow a documented governance path to keep the core schema stable while allowing extensions to thrive. This page outlines the required steps depending on the type of change you would like to make.

## Core Specification Proposals

1. **Start with an issue** using the *Core Spec Proposal* template and describe the problem statement, proposed change, and alternatives considered.
2. **Attach design artefacts** such as schema diffs, rendered documentation, and updated fixtures. Proposals must include example payloads that demonstrate the change across at least two representative characters.
3. **Engage with the review cadence.** Core proposals are triaged weekly by the Core Approval Team (CAT) and move through three stages: _Draft_, _Candidate_, and _Accepted_. Advancement requires:
   - Draft: open discussion and assignment of a CAT sponsor.
   - Candidate: consensus within the CAT and at least one validator maintainer sign-off.
   - Accepted: two-thirds CAT approval plus validation of updated conformance fixtures.
4. **Submit a pull request** referencing the proposal issue once consensus is reached. PRs must include updated documentation, schema grammar, examples, and validator tests.

### Core Approval Team & Review Cadence

The Core Approval Team currently consists of:

- **Avery Chen** (Spec Editor)
- **Jordan Rivera** (Validator Lead)
- **Priya Singh** (Ecosystem Steward)

The CAT meets every Tuesday to triage new proposals and reviews active items asynchronously. Expect initial feedback within five business days and final acceptance decisions within two review cycles after a proposal reaches Candidate stage.

## `x-*` Extension Submissions

1. **Open an issue** using the *Extension Proposal* template describing the extension namespace (e.g., `x-awesome`), ownership, and versioning strategy.
2. **Document the schema** including required/optional fields, validation rules, and interoperability considerations with the core spec.
3. **Provide examples** of extension usage and link to any reference implementations.
4. **Register the namespace** by updating the extension registry once the proposal is approved by at least one CAT member and an ecosystem representative.
5. **Submit the implementation PR** with documentation, schema updates, and fixtures isolated under the extension namespace.

## Example & Fixture Requirements

All proposals must keep the examples directory and test fixtures in sync with the specification:

- Provide minimal and fully populated examples for new structures.
- Update validator fixtures to cover positive and negative cases.
- Include migration notes illustrating how existing content should adapt.

### Example Templates

To streamline submissions, reference the templates in `examples/templates/` when adding new payloads. Each template outlines required fields, recommended metadata, and naming conventions. Populate both the minimal (`*-lite.json`) and comprehensive (`*-full.json`) variants so downstream tooling can rely on consistent coverage.

## Breaking Change Policy

Breaking changes to the core schema or grammar are tightly controlled:

- Only allowed during major version increments following a documented migration path.
- Require an impact analysis covering downstream tooling, validators, and hosted services.
- Must ship with automated migration scripts or guidance where feasible.
- Demand unanimous CAT approval and sign-off from the validator leads of supported languages.

Extensions may introduce breaking changes within their namespace provided they follow semantic versioning and document upgrade instructions.

## Pull Request Expectations

- Reference the originating issue and proposal stage.
- Include documentation updates, changelog entries, and validator test results.
- Request reviews from the CAT sponsor and relevant validator maintainers.
- Respond to feedback within three business days to maintain momentum.
