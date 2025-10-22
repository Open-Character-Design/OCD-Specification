/** Result module for diagnostic data structures and formatting. */

export enum Severity {
  WARNING = 'warning',
  ERROR = 'error'
}

export class Diagnostic {
  constructor(
    public code: string,
    public severity: Severity,
    public message: string,
    public path: string,
    public rule: any,
    public specId: string,
    public schemaVersion: number
  ) {}

  toObject(): Record<string, any> {
    return {
      code: this.code,
      severity: this.severity,
      message: this.message,
      path: this.path,
      rule: this.rule,
      specId: this.specId,
      schemaVersion: this.schemaVersion
    };
  }
}

export class ValidationResult {
  constructor(
    public ok: boolean,
    public diagnostics: Diagnostic[],
    public data?: any
  ) {}

  toObject(): Record<string, any> {
    return {
      ok: this.ok,
      diagnostics: this.diagnostics.map(diag => diag.toObject()),
      data: this.data
    };
  }

  getErrors(): Diagnostic[] {
    return this.diagnostics.filter(diag => diag.severity === Severity.ERROR);
  }

  getWarnings(): Diagnostic[] {
    return this.diagnostics.filter(diag => diag.severity === Severity.WARNING);
  }

  hasErrors(): boolean {
    return this.getErrors().length > 0;
  }

  hasWarnings(): boolean {
    return this.getWarnings().length > 0;
  }
}

export class ResultFormatter {
  static formatText(result: ValidationResult): string {
    if (result.ok) {
      if (result.hasWarnings()) {
        return `Validation succeeded with ${result.getWarnings().length} warning(s).`;
      } else {
        return 'Validation succeeded.';
      }
    } else {
      const errors = result.getErrors();
      const warnings = result.getWarnings();

      const lines: string[] = [];
      if (errors.length > 0) {
        lines.push(`Validation failed with ${errors.length} error(s):`);
        for (const error of errors) {
          lines.push(`  - ${error.path}: ${error.message}`);
        }
      }

      if (warnings.length > 0) {
        lines.push(`Validation produced ${warnings.length} warning(s):`);
        for (const warning of warnings) {
          lines.push(`  - ${warning.path}: ${warning.message}`);
        }
      }

      return lines.join('\n');
    }
  }

  static formatJson(result: ValidationResult): string {
    return JSON.stringify(result.toObject(), null, 2);
  }

  static formatSummary(result: ValidationResult): string {
    if (result.ok) {
      if (result.hasWarnings()) {
        return `✅ Validation passed with ${result.getWarnings().length} warning(s)`;
      } else {
        return '✅ Validation passed';
      }
    } else {
      const errors = result.getErrors();
      const warnings = result.getWarnings();
      let summary = `❌ Validation failed with ${errors.length} error(s)`;
      if (warnings.length > 0) {
        summary += ` and ${warnings.length} warning(s)`;
      }
      return summary;
    }
  }
}
