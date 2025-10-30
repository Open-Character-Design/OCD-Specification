use once_cell::sync::Lazy;
use serde::{Deserialize, Serialize};
use serde_json::Value as JsonValue;
use thiserror::Error;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum Severity {
    Warning,
    Error,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Diagnostic {
    pub code: String,
    pub severity: Severity,
    pub message: String,
    pub path: String,
    /// Minimal rule context that produced the diagnostic
    #[serde(default)]
    pub rule: JsonValue,
    pub spec_id: String,
    pub schema_version: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidationResult {
    pub ok: bool,
    #[serde(default)]
    pub diagnostics: Vec<Diagnostic>,
    /// Present only when ok=true
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<JsonValue>,
}

#[derive(Debug, Error)]
pub enum ValidatorError {
    #[error("schema initialization failed: {0}")]
    SchemaInit(String),
    #[error("invalid input: {0}")]
    InvalidInput(String),
    #[error("internal error: {0}")]
    Internal(String),
}

static CORE_SCHEMA: Lazy<JsonValue> = Lazy::new(|| {
    // Placeholder: will embed spec/core.schema.json
    JsonValue::Null
});

static VALIDATION_SCHEMA: Lazy<JsonValue> = Lazy::new(|| {
    // Placeholder: will embed schema/ocd-validation-spec.schema.json
    JsonValue::Null
});

pub fn validate(input: &JsonValue) -> Result<ValidationResult, ValidatorError> {
    // TODO: Implement schema validation + custom rules
    let result = ValidationResult {
        ok: true,
        diagnostics: Vec::new(),
        data: Some(input.clone()),
    };
    Ok(result)
}

pub fn normalize(input: &mut JsonValue, diagnostics: &mut Vec<Diagnostic>) {
    // TODO: Implement normalization; push warnings into diagnostics as needed
    let _ = (input, diagnostics);
}


