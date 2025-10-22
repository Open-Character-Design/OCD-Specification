/** Evaluator module for applying validation operators to matched values. */

import type { ValidationRule } from './loader.js';
import type { PathMatch } from './matcher.js';
import { Diagnostic, Severity } from './result.js';

export class RuleEvaluator {
  private mode: string;

  constructor(mode: string = 'relaxed') {
    this.mode = mode;
  }

  evaluateRule(
    rule: ValidationRule,
    matches: PathMatch[],
    specId: string,
    schemaVersion: number
  ): Diagnostic[] {
    const diagnostics: Diagnostic[] = [];

    // Handle presence validation
    if (rule.presence) {
      const presenceDiags = this.evaluatePresence(rule, matches, specId, schemaVersion);
      diagnostics.push(...presenceDiags);
    }

    // Evaluate other operators on existing values
    for (const match of matches) {
      const { value, path } = match;

      // Skip if value is null/undefined and presence is optional
      if ((value === null || value === undefined) && rule.presence === 'optional') {
        continue;
      }

      // Evaluate type
      if (rule.type) {
        const typeDiag = this.evaluateType(rule, value, path, specId, schemaVersion);
        if (typeDiag) {
          diagnostics.push(typeDiag);
        }
      }

      // Evaluate enum
      if (rule.enum) {
        const enumDiag = this.evaluateEnum(rule, value, path, specId, schemaVersion);
        if (enumDiag) {
          diagnostics.push(enumDiag);
        }
      }

      // Evaluate const
      if (rule.const !== undefined) {
        const constDiag = this.evaluateConst(rule, value, path, specId, schemaVersion);
        if (constDiag) {
          diagnostics.push(constDiag);
        }
      }

      // Evaluate numeric constraints
      if (rule.min !== undefined || rule.max !== undefined) {
        const numericDiag = this.evaluateNumeric(rule, value, path, specId, schemaVersion);
        if (numericDiag) {
          diagnostics.push(numericDiag);
        }
      }

      // Evaluate string constraints
      if (rule.minLength !== undefined || rule.maxLength !== undefined || rule.pattern || rule.format) {
        const stringDiag = this.evaluateString(rule, value, path, specId, schemaVersion);
        if (stringDiag) {
          diagnostics.push(stringDiag);
        }
      }

      // Evaluate array constraints
      if (rule.uniqueItems !== undefined || rule.minItems !== undefined || rule.maxItems !== undefined) {
        const arrayDiag = this.evaluateArray(rule, value, path, specId, schemaVersion);
        if (arrayDiag) {
          diagnostics.push(arrayDiag);
        }
      }

      // Evaluate items/properties
      if (rule.items || rule.properties) {
        const nestedDiag = this.evaluateNested(rule, value, path, specId, schemaVersion);
        if (nestedDiag) {
          diagnostics.push(nestedDiag);
        }
      }

      // Evaluate dependent required
      if (rule.dependentRequired) {
        const depDiag = this.evaluateDependentRequired(rule, value, path, specId, schemaVersion);
        if (depDiag) {
          diagnostics.push(depDiag);
        }
      }

      // Evaluate compare
      if (rule.compare) {
        const compareDiag = this.evaluateCompare(rule, value, path, specId, schemaVersion);
        if (compareDiag) {
          diagnostics.push(compareDiag);
        }
      }
    }

    return diagnostics;
  }

  private evaluatePresence(
    rule: ValidationRule,
    matches: PathMatch[],
    specId: string,
    schemaVersion: number
  ): Diagnostic[] {
    const diagnostics: Diagnostic[] = [];
    const presence = rule.presence!;

    if (presence === 'required' && matches.length === 0) {
      diagnostics.push(new Diagnostic(
        'REQUIRED_FIELD_MISSING',
        Severity.ERROR,
        rule.message || 'Required field missing',
        rule.path,
        rule,
        specId,
        schemaVersion
      ));
    } else if (presence === 'forbidden' && matches.length > 0) {
      diagnostics.push(new Diagnostic(
        'FORBIDDEN_FIELD_PRESENT',
        Severity.ERROR,
        rule.message || 'Forbidden field present',
        rule.path,
        rule,
        specId,
        schemaVersion
      ));
    }

    return diagnostics;
  }

  private evaluateType(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    let expectedType = rule.type!;

    // Handle type references
    if (typeof expectedType === 'object' && expectedType.type) {
      expectedType = expectedType.type;
    }

    const actualType = this.getJavaScriptType(value);

    if (actualType !== expectedType) {
      const severity = this.getSeverity(rule, 'TYPE_MISMATCH');
      return new Diagnostic(
        'TYPE_MISMATCH',
        severity,
        rule.message || `Expected ${expectedType}, got ${actualType}`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    return null;
  }

  private evaluateEnum(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    const allowedValues = Array.isArray(rule.enum) ? rule.enum : [rule.enum];

    if (!allowedValues.includes(value)) {
      const severity = this.getSeverity(rule, 'INVALID_ENUM_VALUE');
      return new Diagnostic(
        'INVALID_ENUM_VALUE',
        severity,
        rule.message || `Value must be one of: ${allowedValues.join(', ')}`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    return null;
  }

  private evaluateConst(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    const expectedValue = rule.const;

    if (value !== expectedValue) {
      const severity = this.getSeverity(rule, 'CONST_MISMATCH');
      return new Diagnostic(
        'CONST_MISMATCH',
        severity,
        rule.message || `Value must be exactly: ${expectedValue}`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    return null;
  }

  private evaluateNumeric(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    if (typeof value !== 'number') {
      return null;
    }

    if (rule.min !== undefined && value < rule.min) {
      const severity = this.getSeverity(rule, 'VALUE_TOO_SMALL');
      return new Diagnostic(
        'VALUE_TOO_SMALL',
        severity,
        rule.message || `Value must be >= ${rule.min}`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    if (rule.max !== undefined && value > rule.max) {
      const severity = this.getSeverity(rule, 'VALUE_TOO_LARGE');
      return new Diagnostic(
        'VALUE_TOO_LARGE',
        severity,
        rule.message || `Value must be <= ${rule.max}`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    return null;
  }

  private evaluateString(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    if (typeof value !== 'string') {
      return null;
    }

    if (rule.minLength !== undefined && value.length < rule.minLength) {
      const severity = this.getSeverity(rule, 'STRING_TOO_SHORT');
      return new Diagnostic(
        'STRING_TOO_SHORT',
        severity,
        rule.message || `String must be at least ${rule.minLength} characters`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    if (rule.maxLength !== undefined && value.length > rule.maxLength) {
      const severity = this.getSeverity(rule, 'STRING_TOO_LONG');
      return new Diagnostic(
        'STRING_TOO_LONG',
        severity,
        rule.message || `String must be at most ${rule.maxLength} characters`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    if (rule.pattern) {
      const regex = new RegExp(rule.pattern);
      if (!regex.test(value)) {
        const severity = this.getSeverity(rule, 'PATTERN_MISMATCH');
        return new Diagnostic(
          'PATTERN_MISMATCH',
          severity,
          rule.message || 'String does not match required pattern',
          path,
          rule,
          specId,
          schemaVersion
        );
      }
    }

    if (rule.format) {
      const formatDiag = this.evaluateFormat(rule, value, path, specId, schemaVersion);
      if (formatDiag) {
        return formatDiag;
      }
    }

    return null;
  }

  private evaluateFormat(
    rule: ValidationRule,
    value: string,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    const formatType = rule.format!;

    if (formatType === 'email') {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailPattern.test(value)) {
        const severity = this.getSeverity(rule, 'INVALID_EMAIL_FORMAT');
        return new Diagnostic(
          'INVALID_EMAIL_FORMAT',
          severity,
          rule.message || 'Invalid email format',
          path,
          rule,
          specId,
          schemaVersion
        );
      }
    } else if (formatType === 'url') {
      const urlPattern = /^https?:\/\/.+/;
      if (!urlPattern.test(value)) {
        const severity = this.getSeverity(rule, 'INVALID_URL_FORMAT');
        return new Diagnostic(
          'INVALID_URL_FORMAT',
          severity,
          rule.message || 'Invalid URL format',
          path,
          rule,
          specId,
          schemaVersion
        );
      }
    }

    // Add more format validations as needed

    return null;
  }

  private evaluateArray(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    if (!Array.isArray(value)) {
      return null;
    }

    if (rule.minItems !== undefined && value.length < rule.minItems) {
      const severity = this.getSeverity(rule, 'ARRAY_TOO_SHORT');
      return new Diagnostic(
        'ARRAY_TOO_SHORT',
        severity,
        rule.message || `Array must have at least ${rule.minItems} items`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    if (rule.maxItems !== undefined && value.length > rule.maxItems) {
      const severity = this.getSeverity(rule, 'ARRAY_TOO_LONG');
      return new Diagnostic(
        'ARRAY_TOO_LONG',
        severity,
        rule.message || `Array must have at most ${rule.maxItems} items`,
        path,
        rule,
        specId,
        schemaVersion
      );
    }

    if (rule.uniqueItems === true) {
      const uniqueValues = new Set(value);
      if (value.length !== uniqueValues.size) {
        const severity = this.getSeverity(rule, 'ARRAY_NOT_UNIQUE');
        return new Diagnostic(
          'ARRAY_NOT_UNIQUE',
          severity,
          rule.message || 'Array items must be unique',
          path,
          rule,
          specId,
          schemaVersion
        );
      }
    }

    return null;
  }

  private evaluateNested(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    // This is a simplified implementation
    // In a full implementation, you'd recursively evaluate items/properties
    return null;
  }

  private evaluateDependentRequired(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    // This is a simplified implementation
    // In a full implementation, you'd check if required fields are present
    return null;
  }

  private evaluateCompare(
    rule: ValidationRule,
    value: any,
    path: string,
    specId: string,
    schemaVersion: number
  ): Diagnostic | null {
    // This is a simplified implementation
    // In a full implementation, you'd compare values based on the comparison type
    return null;
  }

  private getJavaScriptType(value: any): string {
    if (value === null) {
      return 'null';
    } else if (typeof value === 'boolean') {
      return 'boolean';
    } else if (typeof value === 'number') {
      return Number.isInteger(value) ? 'integer' : 'number';
    } else if (typeof value === 'string') {
      return 'string';
    } else if (Array.isArray(value)) {
      return 'array';
    } else if (typeof value === 'object') {
      return 'object';
    } else {
      return 'unknown';
    }
  }

  private getSeverity(rule: ValidationRule, defaultCode: string): Severity {
    if (rule.severity) {
      return rule.severity === 'error' ? Severity.ERROR : Severity.WARNING;
    }

    // Default severity based on mode
    return this.mode === 'strict' ? Severity.ERROR : Severity.WARNING;
  }
}
