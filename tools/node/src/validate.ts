/** Main validator module using the new OCD validation spec pipeline. */

import { SpecLoader } from './loader.js';
import { SpecMerger } from './merger.js';
import { PathMatcher } from './matcher.js';
import { RuleEvaluator } from './evaluator.js';
import { Diagnostic, ValidationResult, Severity } from './result.js';
import { normalizeInPlace } from './normalize.js';
import { lint } from './lint.js';
import type { Warning } from './warnings.js';

export type { Warning } from './warnings.js';

export interface ValidationError {
  message: string;
  instancePath: string;
  schemaPath: string;
  keyword: string;
  params: Record<string, unknown>;
}

export interface Result<T> {
  ok: boolean;
  data?: T;
  errors?: ValidationError[];
  warnings: Warning[];
}

export type ValidationMode = 'relaxed' | 'strict';

export async function validateAndNormalize(
  doc: unknown,
  mode: ValidationMode = 'relaxed',
  specPath?: string
): Promise<Result<any>> {
  try {
    // Load specifications
    const loader = new SpecLoader();
    let specsToMerge;
    
    // Load custom spec if provided
    if (specPath) {
      try {
        const customSpec = await loader.loadSpec(specPath);
        specsToMerge = [customSpec];
      } catch (error) {
        return {
          ok: false,
          warnings: [],
          errors: [{
            message: `Failed to load custom spec: ${error}`,
            instancePath: '/spec',
            schemaPath: '#/spec',
            keyword: 'spec_error',
            params: { error: String(error) }
          }]
        };
      }
    } else {
      // Load default spec only if no custom spec provided
      const defaultSpecPath = 'tests/specs/ocd-default-spec.ocd';
      
      try {
        const defaultSpec = await loader.loadSpec(defaultSpecPath);
        specsToMerge = [defaultSpec];
      } catch (error) {
        // Try alternative path
        try {
          const altSpecPath = 'spec/ocd-default-spec.ocd';
          const defaultSpec = await loader.loadSpec(altSpecPath);
          specsToMerge = [defaultSpec];
        } catch {
          return {
            ok: false,
            warnings: [],
            errors: [{
              message: 'Default specification not found',
              instancePath: '/spec',
              schemaPath: '#/spec',
              keyword: 'spec_error',
              params: { error: String(error) }
            }]
          };
        }
      }
    }
    
    // Merge specifications
    const merger = new SpecMerger();
    const mergedSpec = merger.mergeSpecs(specsToMerge);
    const resolvedSpec = merger.resolveReferences(mergedSpec);
    
    // Initialize components
    const matcher = new PathMatcher();
    const evaluator = new RuleEvaluator(mode);
    
    // Collect diagnostics
    const allDiagnostics: Diagnostic[] = [];
    
    // Evaluate rules
    if (resolvedSpec.rules) {
      for (const rule of resolvedSpec.rules) {
        const matches = matcher.findMatches(doc, rule.path);
        const ruleDiagnostics = evaluator.evaluateRule(
          rule, matches, resolvedSpec.id || 'unknown', resolvedSpec.schemaVersion || 1
        );
        allDiagnostics.push(...ruleDiagnostics);
      }
    }
    
    // Evaluate constraints
    if (resolvedSpec.constraints) {
      const constraintDiagnostics = evaluateConstraints(
        resolvedSpec.constraints, doc, matcher, evaluator, resolvedSpec.id || 'unknown', resolvedSpec.schemaVersion || 1
      );
      allDiagnostics.push(...constraintDiagnostics);
    }
    
    // Determine if validation passed
    const errors = allDiagnostics.filter(d => d.severity === Severity.ERROR);
    const warnings = allDiagnostics.filter(d => d.severity === Severity.WARNING);
    
    const validationPassed = errors.length === 0;
    
    // Normalize data if validation passed
    let normalizedData;
    if (validationPassed) {
      normalizedData = JSON.parse(JSON.stringify(doc)); // Deep copy
      const normalizeWarnings: Warning[] = [];
      normalizeInPlace(normalizedData, normalizeWarnings);
      
      // Add linter warnings
      const linterWarnings = lint(normalizedData);
      normalizeWarnings.push(...linterWarnings);
      
      // Convert to legacy format for compatibility
      return {
        ok: true,
        data: normalizedData,
        warnings: normalizeWarnings
      };
    }
    
    // Convert to legacy format for compatibility
    return {
      ok: false,
      warnings: warnings.map(w => ({
        code: w.code,
        path: w.path,
        detail: w.message
      })),
      errors: errors.map(e => ({
        message: e.message,
        instancePath: e.path,
        schemaPath: '#/validation',
        keyword: e.code,
        params: {}
      }))
    };
    
  } catch (error) {
    return {
      ok: false,
      warnings: [],
      errors: [{
        message: `Validation error: ${error}`,
        instancePath: '/validation',
        schemaPath: '#/validation',
        keyword: 'validation_error',
        params: { error: String(error) }
      }]
    };
  }
}

function evaluateConstraints(
  constraints: any,
  doc: any,
  matcher: PathMatcher,
  evaluator: RuleEvaluator,
  specId: string,
  schemaVersion: number
): Diagnostic[] {
  const diagnostics: Diagnostic[] = [];
  
  // Evaluate require constraints
  if (constraints.require) {
    for (const req of constraints.require) {
      const path = typeof req === 'string' ? req : req.path;
      
      if (!matcher.pathExists(doc, path)) {
        diagnostics.push(new Diagnostic(
          'REQUIRED_CONSTRAINT_MISSING',
          Severity.ERROR,
          `Required path missing: ${path}`,
          path,
          { path, presence: 'required' },
          specId,
          schemaVersion
        ));
      }
    }
  }
  
  // Evaluate forbid constraints
  if (constraints.forbid) {
    for (const forbid of constraints.forbid) {
      const path = typeof forbid === 'string' ? forbid : forbid.path;
      
      if (matcher.pathExists(doc, path)) {
        diagnostics.push(new Diagnostic(
          'FORBIDDEN_CONSTRAINT_PRESENT',
          Severity.ERROR,
          `Forbidden path present: ${path}`,
          path,
          { path, presence: 'forbidden' },
          specId,
          schemaVersion
        ));
      }
    }
  }
  
  // Evaluate disallow constraints
  if (constraints.disallow) {
    const disallow = constraints.disallow;
    if (disallow.tags) {
      const forbiddenTags = disallow.tags;
      const tagMatches = matcher.findMatches(doc, 'meta.tags');
      
      for (const match of tagMatches) {
        if (Array.isArray(match.value)) {
          for (const tag of match.value) {
            if (forbiddenTags.includes(tag)) {
              diagnostics.push(new Diagnostic(
                'DISALLOWED_TAG',
                Severity.ERROR,
                `Tag "${tag}" not allowed`,
                match.path,
                { path: match.path, disallow: { tags: forbiddenTags } },
                specId,
                schemaVersion
              ));
            }
          }
        }
      }
    }
  }
  
  return diagnostics;
}