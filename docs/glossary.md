# Glossary

**OCD** (Open Character Design Specification)  
The overall standard for defining character data in a structured, portable format.  

**Character Specification**  
A character file (YAML or JSON) that describes a character's attributes, traits, profile, and other properties according to the OCD format.

**OCD Validation Specification** (.ocd file)  
A validation rule file that defines constraints and requirements for character data. These files use the `.ocd` extension and follow the OCD Validation Spec schema.

**Validation Mode**  
The strictness level for validation:
- **Relaxed**: Structure errors are errors; data errors are warnings
- **Strict**: Both structure and data errors are errors


**Bipolar trait**  
A trait axis with two poles and `polarity`/`intensity` values.

**Scalar trait**  
A trait with a single normalized value (0..1).

**Spiky POV (Spiky Point of View)**  
A belief or perspective held with strong conviction that is debatable, distinctive, and intentionally non-neutral. Used to create clarity, differentiation, and memorability in ideas or products. Concept originally articulated by Wes Kao (2020), co-founder of Maven, in her essay "[Spiky point of view: Let's get a little controversial](https://www.weskao.com/blog/spiky-point-of-view-lets-get-a-little-controversial)".

**Flag trait**  
A boolean trait indicating presence/absence.

**Structure Error**  
Validation error related to required fields, types, or document structure. Always treated as errors regardless of mode.

**Data Error**  
Validation error related to data constraints (enums, patterns, ranges). Severity depends on validation mode unless overridden.
