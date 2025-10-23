# Frequently Asked Questions

## General Questions

### What is the Open Character Design Specification (OCD)?

The Open Character Design Specification is a standardized format for describing characters in a structured, machine-readable way. It's designed to be flexible enough for creative use cases while providing enough structure for technical applications like AI systems, game engines, and APIs.

### Why should I use OCD instead of other character formats?

OCD provides several advantages:

- **Standardization**: Consistent format across different tools and platforms
- **Validation**: Built-in validation ensures data quality and consistency
- **Flexibility**: Supports both simple and complex character descriptions
- **Extensibility**: Custom specifications allow project-specific requirements
- **Interoperability**: Works with multiple programming languages and tools
- **Future-proof**: Designed to evolve with changing needs

### What file formats does OCD support?

OCD supports both YAML and JSON formats for character data. The specification itself uses a YAML-like format (`.ocd` files) for defining validation rules.

### Is OCD free to use?

Yes, OCD is completely free and open source. It's released under the Apache 2.0 license for code and CC BY 4.0 for the specification.

## Validation Questions

### What are the different validation modes?

OCD provides two validation modes:

- **Relaxed Mode (Default)**: Structure-only validation, soft enums, allows unknown fields
- **Strict Mode**: Complete validation with strict type checking and enum enforcement

### When should I use relaxed mode vs strict mode?

- **Use Relaxed Mode** for:
  - Development and prototyping
  - Creative workflows
  - Legacy data migration
  - When flexibility is important

- **Use Strict Mode** for:
  - Production systems
  - Data quality assurance
  - Team consistency
  - Final validation before deployment

### How do I create custom validation rules?

Create a custom specification file (`.ocd`) with your validation rules:

```yaml
id: my-project-spec
type: validationSpec
metadata:
  name: My Project Validation Rules

validation:
  mode: strict
  rules:
    custom_validation:
      - code: MINIMUM_TRAITS
        condition: "personality.traits.length >= 3"
        message: "Characters must have at least 3 personality traits"
        severity: error
```

Then use it with:
```bash
ocd-validate character.yaml --spec my-project-spec.ocd
```

### Can I override the validation mode in a custom specification?

Yes, you can set the default mode in your custom specification:

```yaml
validation:
  mode: strict  # This becomes the default mode
  constraints:
    allowUnknownFields: false
```

You can still override it with the `--mode` flag:
```bash
ocd-validate character.yaml --spec my-spec.ocd --mode relaxed
```

## Technical Questions

### What programming languages are supported?

Currently, OCD validators are available for:

- **Python**: `ocd-validate` package
- **Node.js/TypeScript**: `@ocd-tools/validator` package

More languages may be added in the future based on community demand.

### How do I integrate OCD into my application?

Integration depends on your platform:

**Web Applications:**
```typescript
import { validateAndNormalize } from '@ocd-tools/validator';

const result = await validateAndNormalize(characterData, 'strict');
if (result.ok) {
  // Use validated character data
  console.log(result.data);
} else {
  // Handle validation errors
  console.error(result.errors);
}
```

**Python Applications:**
```python
from ocd.validate import validate_and_normalize

result = validate_and_normalize(character_data, mode="strict")
if result["ok"]:
    # Use validated character data
    print(result["data"])
else:
    # Handle validation errors
    print(result["errors"])
```

**CLI Integration:**
```bash
# Validate single character
ocd-validate character.yaml

# Validate with custom spec
ocd-validate character.yaml --spec my-spec.ocd

# Batch validation
for file in characters/*.yaml; do
  ocd-validate "$file" --mode strict
done
```

### Can I use OCD with game engines like Unity or Unreal?

Yes, OCD can be integrated with game engines. The validation can be done at build time or runtime, and the validated character data can be used to drive game systems like dialogue, AI behavior, or character customization.

See [Integration Examples](integration/examples.md) for specific implementation examples.

### How do I handle validation errors in my application?

Handle validation errors gracefully:

```typescript
try {
  const result = await validateAndNormalize(characterData, 'strict');
  
  if (result.ok) {
    // Success - use validated data
    processCharacter(result.data);
  } else {
    // Validation failed - show errors to user
    showValidationErrors(result.errors);
  }
} catch (error) {
  // Unexpected error - log and handle
  console.error('Validation error:', error);
  showGenericError();
}
```

## Data Questions

### What's the difference between a character and a validation specification?

- **Character**: Contains actual character data (names, personality, background, etc.)
- **Validation Specification**: Defines rules for validating character data

Characters are typically stored as `.yaml` or `.json` files, while specifications are stored as `.ocd` files.

### Can I add custom fields to my characters?

Yes, in relaxed mode you can add custom fields. In strict mode, only fields defined in the schema are allowed.

```yaml
# This works in relaxed mode
ocd_version: "0.9.0"
id: "my-character"
names:
  canon: "My Character"
# Custom field
custom_field: "custom value"
```

### How do I migrate from other character formats?

Migration depends on your source format:

1. **Identify the mapping** between your format and OCD
2. **Create a conversion script** to transform the data
3. **Validate the converted data** using OCD validators
4. **Test thoroughly** with both relaxed and strict modes

### Can I use OCD for non-human characters?

Yes, OCD supports various entity types:

```yaml
identity:
  entity_kind: "creature"  # For animals, monsters, etc.
  species: "dragon"
  sapience_level: "sapient"
```

Or for AI characters:

```yaml
identity:
  entity_kind: "ai"
  species: "artificial"
  sapience_level: "transcendent"
```

## Performance Questions

### How fast is OCD validation?

Validation speed depends on:

- **Character complexity**: More fields = longer validation
- **Validation mode**: Strict mode is slower than relaxed mode
- **Custom specifications**: Complex rules slow down validation
- **File size**: Larger files take longer to process

For typical character files, validation should complete in milliseconds.

### Can I validate large numbers of characters?

Yes, but consider:

- **Batch processing**: Validate multiple characters in a single operation
- **Parallel processing**: Use multiple processes/threads for large datasets
- **Caching**: Cache validation results when possible
- **Incremental validation**: Only validate changed characters

### How much memory does OCD validation use?

Memory usage depends on:

- **Character file size**: Larger files use more memory
- **Validation mode**: Strict mode uses more memory
- **Custom specifications**: Complex rules increase memory usage

For typical character files, memory usage should be minimal.

## Troubleshooting Questions

### My validation is failing but I don't know why. What should I do?

1. **Check the error messages** - they usually indicate the specific problem
2. **Try relaxed mode** - this often reveals if it's a strict validation issue
3. **Validate with a minimal example** - start with the simplest possible character
4. **Check the documentation** - see [Troubleshooting Guide](troubleshooting.md)
5. **Ask for help** - use GitHub Issues or Discussions

### Why is my custom specification not working?

Common issues:

1. **Invalid YAML syntax** - check for proper indentation and formatting
2. **Missing required fields** - ensure `id`, `type`, and `validation` are present
3. **Invalid rule syntax** - check condition expressions and rule structure
4. **File path issues** - ensure the specification file exists and is readable

### Can I validate characters without installing the validators?

Yes, you can use online validation tools or integrate validation into your existing workflow. However, for production use, we recommend installing the appropriate validator package.

## Community Questions

### How can I contribute to OCD?

There are many ways to contribute:

1. **Report bugs** - use GitHub Issues
2. **Suggest features** - use GitHub Discussions
3. **Submit pull requests** - contribute code improvements
4. **Write documentation** - help improve the docs
5. **Share examples** - contribute character examples
6. **Help others** - answer questions in Discussions

### Where can I get help?

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community discussion
- **Documentation**: Check the guides and reference materials
- **Examples**: Look at the example characters and integration examples

### Is there a community Discord or Slack?

Currently, community discussion happens on GitHub Discussions. We may add other platforms in the future based on community needs.

### Can I use OCD in commercial projects?

Yes, OCD is free to use in commercial projects. The code is licensed under Apache 2.0 and the specification under CC BY 4.0, both of which allow commercial use.

### How often is OCD updated?

OCD follows semantic versioning and is updated based on community needs and feedback. Major updates are announced on GitHub and in the changelog.

## Advanced Questions

### Can I extend OCD with my own field types?

Yes, you can create custom specifications that define additional field types and validation rules. However, for maximum compatibility, we recommend using the standard field types when possible.

### How do I handle versioning of character data?

OCD includes built-in versioning support:

```yaml
meta:
  versioning:
    created_at: "2024-01-01T00:00:00Z"
    last_modified: "2024-01-01T00:00:00Z"
    version: "1.0.0"
```

You can also use external version control systems like Git for more advanced versioning needs.

### Can I use OCD with databases?

Yes, OCD character data can be stored in databases. The validation can be done:

- **At insertion time** - validate before storing
- **At retrieval time** - validate when loading from database
- **Asynchronously** - validate in background processes

### How do I handle large-scale character management?

For large-scale character management:

1. **Use databases** for storage and indexing
2. **Implement caching** for frequently accessed characters
3. **Use batch validation** for bulk operations
4. **Consider sharding** for very large datasets
5. **Implement search** and filtering capabilities

### Can I use OCD with AI/ML systems?

Yes, OCD is designed to work well with AI/ML systems:

- **Structured data** makes it easy to extract features
- **Validation ensures data quality** for training
- **Flexible schema** allows for custom fields
- **Standardized format** enables data sharing

### How do I handle internationalization?

OCD supports internationalization through:

- **Unicode support** in all text fields
- **Custom field names** in different languages
- **Localized validation messages** in custom specifications
- **Character encoding** support (UTF-8)

### Can I use OCD with real-time systems?

Yes, OCD can be used in real-time systems:

- **Fast validation** - typically completes in milliseconds
- **Caching** - validate once, use many times
- **Incremental validation** - only validate changed fields
- **Async validation** - validate in background threads

### How do I handle character relationships and references?

OCD supports character relationships through:

- **Reference fields** - link to other character IDs
- **Relationship objects** - define specific relationship types
- **Validation of references** - ensure referenced characters exist
- **Circular reference handling** - prevent infinite loops

### Can I use OCD with version control systems?

Yes, OCD works well with version control:

- **Text-based format** - easy to diff and merge
- **Structured data** - clear conflict resolution
- **Validation** - ensure data integrity after merges
- **Git hooks** - validate on commit

### How do I handle character data migration?

For character data migration:

1. **Map source fields** to OCD fields
2. **Create conversion scripts** to transform data
3. **Validate converted data** using OCD validators
4. **Test thoroughly** with sample data
5. **Implement rollback** procedures for safety

### Can I use OCD with cloud services?

Yes, OCD can be used with cloud services:

- **API integration** - validate characters via REST APIs
- **Cloud storage** - store character data in cloud databases
- **Serverless functions** - validate characters in serverless environments
- **CDN integration** - serve validated character data via CDN

### How do I handle character data backup and recovery?

For backup and recovery:

1. **Regular backups** - backup character data regularly
2. **Validation on restore** - validate data after recovery
3. **Version control** - use Git for character data
4. **Incremental backups** - only backup changed characters
5. **Testing** - regularly test backup and recovery procedures