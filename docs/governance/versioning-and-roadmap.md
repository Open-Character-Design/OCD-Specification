# Versioning & Roadmap

The OpenCharacter Specification (OCD) uses semantic versioning to communicate stability and upgrade expectations. This page clarifies how version numbers are assigned, the roadmap to v1.0, and the release management process.

## Semantic Versioning

- The `ocd_version` field follows `MAJOR.MINOR.PATCH` semantics.
- Patch releases contain backwards-compatible fixes to the schema, grammar, or validator guidance.
- Minor releases may add optional fields or extension hooks but cannot remove or repurpose existing behavior.
- Major releases may introduce breaking changes after the process outlined in the [Breaking Change Policy](./contributing-to-spec.md#breaking-change-policy).

## v1.0 Freeze Plan

The path to the v1.0 release includes a feature freeze to ensure stability:

1. **Feature Cut (T-6 weeks):** No new feature proposals are accepted for v1.0. Open proposals must target v1.1 unless granted an exception by the Core Approval Team (CAT).
2. **Schema Freeze (T-4 weeks):** All grammar and schema changes must be merged. Only bug fixes or clarifications are allowed.
3. **Validator Freeze (T-3 weeks):** Official validators (Python and JavaScript) must pass the full conformance suite. Fixes require CAT approval and must include regression tests. Go validator is planned for post-1.0.
4. **Documentation Freeze (T-2 weeks):** Docs, examples, and migration guides are finalized. Only editorial updates permitted.
5. **Release Candidate (T-1 week):** Publish a tagged release candidate build, circulate release notes, and open the public verification window.
6. **General Availability (Launch):** Promote the release candidate to `v1.0.0` pending sign-off from CAT and validator maintainers.

## Backwards-Compatibility Guarantees

- **Core Schema:** Fields marked as required will not be removed or have their semantics altered in minor or patch releases.
- **Serialization Grammar:** Token shapes and ordering remain stable outside of major releases.
- **Extensions:** Registered `x-*` namespaces must document compatibility expectations. Core-managed extensions follow the same guarantees as the core schema.
- **Validators:** Official validators maintain support for the previous major version for at least 12 months after a new major release.
- **Deprecations:** Features slated for removal are marked deprecated at least one minor release prior to removal and ship with migration guidance.

## Release Checklist

Before cutting any release, complete the following checklist:

1. Update changelog entries and confirm all merged PRs are categorized.
2. Verify conformance fixtures pass across all official validators.
3. Run documentation build and link checkers.
4. Ensure example payloads match the latest schema changes.
5. Tag the release commit and publish versioned documentation.
6. Announce availability on the community channels with upgrade guidance.
7. Create follow-up issues for post-release improvements or known gaps.

## Roadmap Highlights

- Core blocks stabilization and schema governance improvements.
- Validator parity across Rust/WASM, .NET, and JVM ecosystems (see [Validator Roadmap](../integration/validator-roadmap-todo.md)).
- Go validator implementation planned for post-1.0.
- Expanded conformance fixtures and automated regression pipelines.
