/** Merger module for combining OCD validation specifications. */

import { createHash } from 'node:crypto';
import type { ValidationSpec, ValidationRule } from './loader.js';

export class SpecMerger {
  mergeSpecs(baseSpecs: ValidationSpec[]): ValidationSpec {
    if (baseSpecs.length === 0) {
      throw new Error('At least one specification must be provided');
    }

    let merged = { ...baseSpecs[0] };

    for (let i = 1; i < baseSpecs.length; i++) {
      merged = this.mergeSingle(merged, baseSpecs[i]);
    }

    return merged;
  }

  private mergeSingle(base: ValidationSpec, overlay: ValidationSpec): ValidationSpec {
    const merged: ValidationSpec = { ...base };

    // Merge metadata
    if (overlay.metadata) {
      merged.metadata = this.deepMerge(
        merged.metadata || {},
        overlay.metadata
      );
    }

    // Merge policy
    if (overlay.policy) {
      merged.policy = this.deepMerge(
        merged.policy || {},
        overlay.policy
      );
    }

    // Merge definitions
    if (overlay.definitions) {
      merged.definitions = this.mergeDefinitions(
        merged.definitions || {},
        overlay.definitions
      );
    }

    // Merge rules with de-duplication
    if (overlay.rules) {
      merged.rules = this.mergeRules(
        merged.rules || [],
        overlay.rules
      );
    }

    // Merge constraints
    if (overlay.constraints) {
      merged.constraints = this.mergeConstraints(
        merged.constraints || {},
        overlay.constraints
      );
    }

    return merged;
  }

  private deepMerge(base: Record<string, any>, overlay: Record<string, any>): Record<string, any> {
    const result = { ...base };

    for (const [key, value] of Object.entries(overlay)) {
      if (key in result && typeof result[key] === 'object' && typeof value === 'object' && result[key] !== null && value !== null) {
        result[key] = this.deepMerge(result[key], value);
      } else {
        result[key] = value;
      }
    }

    return result;
  }

  private mergeDefinitions(base: ValidationSpec['definitions'], overlay: ValidationSpec['definitions']): ValidationSpec['definitions'] {
    const merged = { ...base };

    if (overlay) {
      for (const section of ['enums', 'types', 'patterns'] as const) {
        if (overlay[section]) {
          if (merged[section]) {
            merged[section] = this.deepMerge(merged[section] as any, overlay[section] as any) as any;
          } else {
            (merged as any)[section] = { ...overlay[section]! };
          }
        }
      }
    }

    return merged;
  }

  private mergeRules(baseRules: ValidationRule[], overlayRules: ValidationRule[]): ValidationRule[] {
    // Create lookup for base rules
    const baseLookup = new Map<string, ValidationRule>();
    for (const rule of baseRules) {
      const key = this.ruleKey(rule);
      baseLookup.set(key, rule);
    }

    // Process overlay rules
    const mergedRules: ValidationRule[] = [];
    const overlayKeys = new Set<string>();

    for (const rule of overlayRules) {
      const key = this.ruleKey(rule);
      overlayKeys.add(key);
      mergedRules.push(rule);
    }

    // Add base rules that weren't overridden
    for (const rule of baseRules) {
      const key = this.ruleKey(rule);
      if (!overlayKeys.has(key)) {
        mergedRules.push(rule);
      }
    }

    return mergedRules;
  }

  private ruleKey(rule: ValidationRule): string {
    const path = rule.path || '';

    // Get all operator keys (excluding path, message, severity)
    const operatorKeys: string[] = [];
    for (const key of Object.keys(rule)) {
      if (!['path', 'message', 'severity'].includes(key)) {
        operatorKeys.push(key);
      }
    }

    operatorKeys.sort();
    const operatorHash = createHash('md5').update(JSON.stringify(operatorKeys)).digest('hex').substring(0, 8);

    return `${path}:${operatorHash}`;
  }

  private mergeConstraints(base: ValidationSpec['constraints'], overlay: ValidationSpec['constraints']): ValidationSpec['constraints'] {
    const merged = { ...base };

    if (overlay) {
      for (const constraintType of ['require', 'forbid', 'disallow', 'arrays'] as const) {
        if (overlay[constraintType]) {
          if (merged[constraintType]) {
            if (constraintType === 'arrays') {
              // Special handling for arrays constraints
              merged[constraintType] = this.mergeArrayConstraints(
                merged[constraintType] as any,
                overlay[constraintType] as any
              ) as any;
            } else {
              // For require/forbid/disallow, overlay replaces base
              merged[constraintType] = overlay[constraintType] as any;
            }
          } else {
            merged[constraintType] = overlay[constraintType] as any;
          }
        }
      }
    }

    return merged;
  }

  private mergeArrayConstraints(base: any, overlay: any): any {
    const merged = { ...base };

    if (overlay) {
      for (const arrayType of ['unique', 'minItems', 'maxItems'] as const) {
        if (overlay[arrayType]) {
          if (merged[arrayType]) {
            // Combine arrays
            merged[arrayType] = [...merged[arrayType], ...overlay[arrayType]];
          } else {
            merged[arrayType] = [...overlay[arrayType]];
          }
        }
      }
    }

    return merged;
  }

  resolveReferences(spec: ValidationSpec): ValidationSpec {
    const resolvedSpec = { ...spec };

    if (resolvedSpec.rules) {
      resolvedSpec.rules = resolvedSpec.rules.map(rule =>
        this.resolveRuleReferences(rule, spec.definitions || {})
      );
    }

    return resolvedSpec;
  }

  private resolveRuleReferences(rule: ValidationRule, definitions: ValidationSpec['definitions']): ValidationRule {
    const resolvedRule = { ...rule };

    if (definitions) {
      // Resolve enum references
      if (rule.enum && typeof rule.enum === 'string' && rule.enum.startsWith('@enums.')) {
        const enumName = rule.enum.substring(7); // Remove "@enums." prefix
        const enums = definitions.enums || {};
        if (enumName in enums) {
          resolvedRule.enum = enums[enumName];
        } else {
          throw new Error(`Enum reference not found: ${rule.enum}`);
        }
      }

      // Resolve type references
      if (rule.type && typeof rule.type === 'string' && rule.type.startsWith('@types.')) {
        const typeName = rule.type.substring(7); // Remove "@types." prefix
        const types = definitions.types || {};
        if (typeName in types) {
          resolvedRule.type = types[typeName];
        } else {
          throw new Error(`Type reference not found: ${rule.type}`);
        }
      }
    }

    return resolvedRule;
  }
}
