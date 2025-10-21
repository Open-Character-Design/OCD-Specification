# Validator Implementation Roadmap - TODO

This document outlines the planned implementation of OpenCharacter Specification (OCD) validators across multiple programming languages and platforms. The goal is to provide comprehensive validation and normalization capabilities that maintain API consistency across all implementations.

## Priority Validators (v1.0 Required)

### JavaScript/TypeScript (Runtime) ,  Ajv

**Why**: Browsers, Node.js, and toolchains; fastest ecosystem boost.

**Library**: `ajv` with JSON Schema 2020-12 support

**Implementation Plan**:
- Bundle a tiny wrapper that also runs the normalization (JS port of our Python normalize)
- Use Ajv for schema validation with full 2020-12 support
- Port normalization logic from Python implementation
- Port diagnostics engine from Python implementation

**API Design**:
```typescript
validateAndNormalize(doc: any): Promise<Result>
// where Result = { valid: boolean, errors: Error[], warnings: Warning[] }
```

**Deliverables**:
- ✅ Basic scaffold exists at `node/src/validate.ts`
- [ ] Implement Ajv integration with OCD schema
- [ ] Port normalization functions from Python
- [ ] Port diagnostics/linting rules from Python
- [ ] Add comprehensive test suite
- [ ] Bundle for browser and Node.js environments
- [ ] Maintain API compatibility with Python version

**Notes**: Keep Zod types for developer experience, but Ajv is the runtime validator across JavaScript ecosystem.

## Post-1.0 Validators

### Go ,  github.com/santhosh-tekuri/jsonschema or invopop/jsonschema

**Why**: Servers, CLIs; lots of game tools use Go.

**Implementation Plan**:
- Create `ocdvalidate` CLI tool
- Support YAML/JSON input formats
- Implement validation → normalization → diagnostics pipeline
- Output machine-readable JSON diagnostics

**API Design**:
```go
func ValidateAndNormalize(doc interface{}) (*NormalizedDoc, []Diagnostic, error)
```

**Deliverables**:
- [ ] Evaluate JSON Schema libraries (santhosh-tekuri vs invopop)
- [ ] Create Go module structure
- [ ] Implement core validation logic
- [ ] Port normalization algorithms
- [ ] Create `ocdvalidate` CLI command
- [ ] Add YAML/JSON input support
- [ ] Implement machine-readable diagnostic output
- [ ] Add comprehensive test suite
- [ ] Create documentation and examples

**CLI Interface**:
```bash
ocdvalidate input.yaml --format json --output diagnostics.json
```

### Rust ,  jsonschema crate + serde

**Why**: Compile-to-WASM for browser/engine embedding; high performance.

**Implementation Plan**:
- Create `ocd_validate` Rust library
- Build WASM target for browser embedding
- Implement high-performance validation and normalization

**API Design**:
```rust
fn validate_and_normalize(doc: Value) -> Result<Normalized, Vec<Diagnostic>>
```

**WASM Interface**:
```javascript
validateAndNormalize(jsonString: string): { valid: boolean, data?: any, errors: Error[], warnings: Warning[] }
```

**Deliverables**:
- [ ] Create Rust crate structure
- [ ] Implement core validation with jsonschema crate
- [ ] Port normalization logic using serde
- [ ] Create diagnostic system
- [ ] Build WASM target with wasm-pack
- [ ] Create JavaScript bindings for WASM
- [ ] Add comprehensive test suite (native and WASM)
- [ ] Performance benchmarking
- [ ] Browser integration examples

### C#/.NET ,  JsonSchema.Net

**Why**: Unity and enterprise stacks.

**Library**: JsonSchema.Net (by Nick G.)

**Implementation Plan**:
- Create `Ocd.Validator` NuGet package
- Implement validation and normalization
- Include minimal normalize pass (arrow, tokens)

**API Design**:
```csharp
public static ValidationResult ValidateAndNormalize(JObject document)
// where ValidationResult contains: IsValid, Data, Errors, Warnings
```

**Deliverables**:
- [ ] Create .NET solution structure
- [ ] Implement JsonSchema.Net integration
- [ ] Port normalization algorithms from Python
- [ ] Create diagnostic system
- [ ] Build NuGet package
- [ ] Add Unity compatibility testing
- [ ] Create comprehensive test suite
- [ ] Add documentation and examples
- [ ] Consider .NET Standard 2.0 for broad compatibility

### Java/Kotlin ,  networknt/json-schema-validator

**Why**: JVM backends + Android tooling.

**Implementation Plan**:
- Create JVM library with Java and Kotlin APIs
- Support Android development workflows
- Provide idiomatic APIs for both languages

**Java API Design**:
```java
public static ValidationResult validateAndNormalize(JsonNode document)
```

**Kotlin Extension**:
```kotlin
fun JsonNode.validateAndNormalize(): ValidationResult
```

**Deliverables**:
- [ ] Create Gradle/Maven project structure
- [ ] Implement JSON Schema validation with networknt library
- [ ] Port normalization logic
- [ ] Create diagnostic system
- [ ] Add Kotlin extensions and idiomatic APIs
- [ ] Android compatibility testing
- [ ] Comprehensive test suite (JUnit + Kotlin test)
- [ ] Publish to Maven Central
- [ ] Create documentation and examples

## Optional Nice-to-Haves (Lower Priority)

### Swift ,  swift-jsonschema or Custom Implementation

**Why**: Server-side Swift + Apple toolchains.

**Implementation Plan**:
- Use swift-jsonschema or implement with Codable + JSON Schema validation
- Create minimal CLI tool
- Support both server-side Swift and iOS/macOS development

**Deliverables**:
- [ ] Evaluate swift-jsonschema vs custom implementation
- [ ] Create Swift Package Manager structure
- [ ] Implement validation and normalization
- [ ] Create CLI tool for server-side use
- [ ] iOS/macOS framework support
- [ ] Test suite with XCTest
- [ ] Documentation and examples

### Ruby ,  json_schemer

**Why**: Quick scripting and automation.

**Implementation Plan**:
- Create Ruby gem for validation and normalization
- Focus on scripting and automation use cases

**API Design**:
```ruby
OCD::Validator.validate_and_normalize(document)
```

**Deliverables**:
- [ ] Create Ruby gem structure
- [ ] Implement json_schemer integration
- [ ] Port normalization logic
- [ ] Create diagnostic system
- [ ] Publish to RubyGems
- [ ] Add RSpec test suite
- [ ] Documentation and examples

### PHP ,  opis/json-schema

**Why**: Web CMS integration and PHP-based tooling.

**Implementation Plan**:
- Create Composer package
- Focus on CMS and web application integration

**API Design**:
```php
OcsValidator::validateAndNormalize($document)
```

**Deliverables**:
- [ ] Create Composer package structure
- [ ] Implement opis/json-schema integration
- [ ] Port normalization logic
- [ ] Create diagnostic system
- [ ] Publish to Packagist
- [ ] Add PHPUnit test suite
- [ ] WordPress/Drupal integration examples

## Implementation Guidelines

### API Consistency

All validators should maintain consistent APIs:

**Input**: JSON/YAML document (language-appropriate data structure)
**Output**: Result object with:
- `valid`/`ok`: boolean
- `data`: normalized document (if valid)
- `errors`: array of error objects
- `warnings`: array of warning objects

### Normalization Requirements

All implementations must support:
- Canonicalize bipolar trait names to - dash syntax
- Lowercase and deduplicate tokens: tags, genres, media, media_targets
- Consistent formatting and structure normalization

### Diagnostic Categories

All implementations should support these diagnostic types:
- `RATING_CONFLICT`: Conflicting content ratings
- `MISSING_SKILL_TAGS`: Skills without appropriate tags
- `UNRESOLVED_REF`: References that cannot be resolved

### Testing Strategy

Each implementation should include:
- Unit tests for validation logic
- Integration tests with example documents
- Normalization behavior tests
- Diagnostic accuracy tests
- Performance benchmarks (where applicable)
- Cross-validation tests against Python reference implementation

## Dependencies and Coordination

### Schema Synchronization
- All validators must use the same JSON Schema version
- Schema updates should be coordinated across all implementations
- Maintain compatibility matrix document

### Reference Implementation
- Python validator serves as the reference implementation
- All other implementations should match Python behavior exactly
- Cross-validation testing against Python required

### Documentation
- Each validator needs language-specific documentation
- Maintain consistency in examples and API documentation
- Integration guides for popular frameworks in each language

## Progress Tracking

This document should be updated as implementations progress. Each language section should track:
- [ ] Design phase complete
- [ ] Implementation started
- [ ] Core validation working
- [ ] Normalization implemented
- [ ] Diagnostics implemented
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Published/Released

## Related Documents

- [Python Validator Documentation](python-validator.md)
- [JS/TS Validator Documentation](js-ts-validator.md)
- [Versioning & Roadmap](../governance/versioning-and-roadmap.md)