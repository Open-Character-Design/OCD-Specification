---
title: Schema Updates - Core Fields Implementation
description: Documentation of schema changes to align with research findings on universal character definition fields
search:
  boost: 1.2
tags:
  - schema
  - core-fields
  - research-implementation
  - validation
---

# Schema Updates - Core Fields Implementation 📋

## Overview

This document outlines the updates made to the Open Character Design Specification core schema (`spec/core.schema.json`) to align with the research findings from [Common Character Definition Fields Across All Mediums](../research/common-character-fields.md). The updates ensure that OCD's validation system implements the universal character attributes identified through comprehensive cross-media analysis.

## Research Foundation

The schema updates are based on research that identified **6 core character definition categories** that appear consistently across all storytelling mediums:

1. **Identity Fields** - Name, aliases, species/race, age, gender
2. **Physical Characteristics** - Appearance, distinctive features, clothing style, body language  
3. **Psychological Profile** - Personality traits, motivations, fears, values, beliefs
4. **Background and History** - Origin, family, education, significant events, relationships
5. **Abilities and Skills** - Strengths, weaknesses, special abilities, skills
6. **Communication Style** - Speech patterns, vocabulary, tone, communication preferences

## Schema Changes

### New Schema Definitions

#### 1. Appearance Schema
```json
"Appearance": {
  "type": "object",
  "properties": {
    "physical_description": { "type": "string" },
    "distinctive_features": { "type": "array", "items": { "type": "string" } },
    "clothing_style": { "type": "string" },
    "body_language": { "type": "array", "items": { "type": "string" } },
    "height": { "$ref": "#/$defs/AgeMeasurement" },
    "weight": { "$ref": "#/$defs/AgeMeasurement" },
    "eye_color": { "type": "string" },
    "hair_color": { "type": "string" },
    "skin_tone": { "type": "string" }
  },
  "additionalProperties": true
}
```

**Purpose**: Structured representation of physical characteristics that maintain consistency across mediums.

#### 2. PsychologicalProfile Schema
```json
"PsychologicalProfile": {
  "type": "object",
  "properties": {
    "personality_traits": { "type": "array", "items": { "type": "string" } },
    "motivations": { "type": "array", "items": { "type": "string" } },
    "fears": { "type": "array", "items": { "type": "string" } },
    "values": { "type": "array", "items": { "type": "string" } },
    "beliefs": { "type": "array", "items": { "type": "string" } },
    "summary": { "type": "string" },
    "traits": { /* existing trait structure */ }
  },
  "additionalProperties": true
}
```

**Purpose**: Comprehensive psychological modeling based on research findings about universal character psychology.

#### 3. AbilitiesAndSkills Schema
```json
"AbilitiesAndSkills": {
  "type": "object",
  "properties": {
    "strengths": { "type": "array", "items": { "type": "string" } },
    "weaknesses": { "type": "array", "items": { "type": "string" } },
    "special_abilities": { "type": "array", "items": { "type": "string" } },
    "skills": { "type": "array", "items": { "type": "string" } },
    "powers": { "type": "array", "items": { "type": "string" } },
    "constraints": { "type": "array", "items": { "type": "string" } },
    "vulnerabilities": { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": true
}
```

**Purpose**: Structured representation of character capabilities and limitations.

#### 4. CommunicationStyle Schema
```json
"CommunicationStyle": {
  "type": "object",
  "properties": {
    "speech_patterns": { "type": "array", "items": { "type": "string" } },
    "vocabulary": { "type": "array", "items": { "type": "string" } },
    "tone": { "type": "array", "items": { "type": "string" } },
    "communication_preferences": { "type": "array", "items": { "type": "string" } },
    "catchphrases": { "type": "array", "items": { "type": "string" } },
    "speech_quirks": { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": true
}
```

**Purpose**: Captures communication patterns essential for AI persona modeling and cross-media consistency.

#### 5. Enhanced Background Schema
```json
"Background": {
  "type": "object",
  "properties": {
    "origin": { "type": "string" },
    "birthplace": { "type": "string" },
    "family": { "type": "array", "items": { /* family member object */ } },
    "education": { "type": "array", "items": { "type": "string" } },
    "significant_events": { "type": "array", "items": { /* event object */ } },
    "relationships": { "type": "array", "items": { /* relationship object */ } },
    "affiliations": { "type": "array", "items": { "type": "string" } },
    "milestones": { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": true
}
```

**Purpose**: Comprehensive background modeling supporting character development and relationship mapping.

### Enhanced Identity Schema

Updated the existing Identity schema to include:
- `gender` field for gender identity and expression
- Enhanced `origins` with `creation_context`
- Improved descriptions for better validation

### Updated CharacterDefinition Schema

The main CharacterDefinition schema now references the new structured schemas:

```json
"CharacterDefinition": {
  "properties": {
    "appearance": { "$ref": "#/$defs/Appearance" },
    "metaphysics": { "$ref": "#/$defs/AbilitiesAndSkills" },
    "personality": { "$ref": "#/$defs/PsychologicalProfile" },
    "background": { "$ref": "#/$defs/Background" },
    "communication": { "$ref": "#/$defs/CommunicationStyle" }
  }
}
```

## Validation Updates

### Default Specification Enhancements

Updated `spec/ocd-default-spec.ocd` to include validation rules for all new core fields:

- **Identity Fields**: Gender validation and enhanced identity checks
- **Physical Characteristics**: Appearance field validation with structured properties
- **Psychological Profile**: Comprehensive personality validation including motivations, fears, values, beliefs
- **Abilities and Skills**: Structured metaphysics validation
- **Communication Style**: New communication field validation
- **Background**: Enhanced background validation with structured relationships and events

### Validation Criteria Alignment

The validation rules now implement the research-based quality criteria:

1. **Completeness**: All core fields are validated for presence
2. **Consistency**: Cross-field validation ensures logical coherence
3. **Specificity**: Structured fields prevent vague descriptions
4. **Authenticity**: Validation rules ensure internal consistency

## Example Implementation

Created `examples/templates/character-research-example.json` demonstrating:

- Complete implementation of all 6 core field categories
- Proper use of structured schemas
- Cross-media consistency (Sherlock Holmes example)
- AI persona modeling compatibility
- Validation compliance

## Benefits

### Cross-Platform Interoperability
- Standardized core fields enable character sharing across different systems
- Consistent validation ensures compatibility

### AI Integration
- Structured fields provide optimal data for persona modeling
- Communication style fields enable consistent AI behavior
- Psychological profile supports character-consistent responses

### Quality Assurance
- Research-based validation criteria ensure character definition quality
- Structured schemas prevent incomplete or inconsistent definitions
- Cross-reference validation maintains logical coherence

### Creative Consistency
- Universal fields maintain character identity across adaptations
- Structured approach improves character development workflows
- Research foundation provides theoretical validation

## Migration Guide

### For Existing Characters

1. **Update Schema References**: Change `appearance`, `personality`, `background` from generic objects to structured schemas
2. **Add Missing Fields**: Include new core fields like `communication`, enhanced `identity.gender`
3. **Restructure Data**: Move existing data into new structured formats
4. **Validate**: Use updated validation to ensure compliance

### For New Characters

1. **Use New Templates**: Reference `character-research-example.json` for proper structure
2. **Follow Core Fields**: Ensure all 6 core categories are addressed
3. **Validate Early**: Use validation tools to check compliance during development

## Future Considerations

### Extensibility
- All new schemas use `additionalProperties: true` for future extensions
- Research-based foundation supports additional field categories
- Validation system can be extended with new rules

### Research Integration
- Schema directly implements research findings
- Validation criteria based on psychological and narrative theory
- Cross-media analysis informs field structure

## Conclusion

The schema updates successfully implement the research findings from "Common Character Definition Fields Across All Mediums," creating a robust, validated system for character definition that:

- Supports cross-platform interoperability
- Enables effective AI integration
- Ensures quality through research-based validation
- Maintains creative consistency across mediums

The updated schema provides the technical foundation for OCD's goal of standardized character representation while maintaining flexibility for diverse creative needs.

---

*For the complete research foundation, see [Common Character Definition Fields Across All Mediums](../research/common-character-fields.md). For implementation examples, see [character-research-example.json](../../examples/templates/character-research-example.json).*
