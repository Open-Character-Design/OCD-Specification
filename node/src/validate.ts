import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

import { type ErrorObject, type ValidateFunction } from 'ajv';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import YAML from 'yaml';

import type { CharacterDefinition, CoreDocument } from './types.js';
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

const ajv = new Ajv2020({
  strict: true,
  allErrors: true,
  allowUnionTypes: true,
});
addFormats(ajv);

let validatorPromise: Promise<ValidateFunction<CoreDocument>> | null = null;
let defaultSpecPromise: Promise<Record<string, unknown>> | null = null;

async function readCoreSchema(): Promise<string> {
  const candidates = [
    new URL('../schema/core.schema.json', import.meta.url),
    new URL('../../spec/core.schema.json', import.meta.url),
  ];

  let lastError: Error | null = null;
  for (const url of candidates) {
    try {
      const schemaPath = fileURLToPath(url);
      return await readFile(schemaPath, 'utf8');
    } catch (error) {
      const err = error as NodeJS.ErrnoException;
      if (err.code === 'ENOENT') {
        lastError = err;
        continue;
      }
      throw err;
    }
  }

  if (lastError) {
    throw new Error('core.schema.json could not be located');
  }
  throw new Error('core.schema.json is missing');
}

async function readDefaultSpec(): Promise<Record<string, unknown>> {
  if (!defaultSpecPromise) {
    defaultSpecPromise = (async () => {
      const candidates = [
        new URL('../../spec/ocd-default-spec.ocd', import.meta.url),
        new URL('../../docs/examples/ocd-default-spec.ocd', import.meta.url),
      ];

      let lastError: Error | null = null;
      for (const url of candidates) {
        try {
          const specPath = fileURLToPath(url);
          const content = await readFile(specPath, 'utf8');
          return YAML.parse(content) as Record<string, unknown>;
        } catch (error) {
          const err = error as NodeJS.ErrnoException;
          if (err.code === 'ENOENT') {
            lastError = err;
            continue;
          }
          throw err;
        }
      }

      if (lastError) {
        throw new Error('ocd-default-spec.ocd could not be located');
      }
      throw new Error('ocd-default-spec.ocd is missing');
    })();
  }

  return defaultSpecPromise;
}

async function loadSpecOverlay(specPath: string): Promise<Record<string, unknown>> {
  const content = await readFile(specPath, 'utf8');
  return YAML.parse(content) as Record<string, unknown>;
}

function mergeSpecs(baseSpec: Record<string, unknown>, overlaySpec: Record<string, unknown>): Record<string, unknown> {
  const merged = { ...baseSpec };
  
  function deepMerge(base: Record<string, unknown>, overlay: Record<string, unknown>): void {
    for (const [key, value] of Object.entries(overlay)) {
      if (key in base && typeof base[key] === 'object' && typeof value === 'object' && base[key] !== null && value !== null) {
        deepMerge(base[key] as Record<string, unknown>, value as Record<string, unknown>);
      } else {
        base[key] = value;
      }
    }
  }
  
  deepMerge(merged, overlaySpec);
  return merged;
}

async function loadValidator(): Promise<ValidateFunction<CoreDocument>> {
  if (!validatorPromise) {
    validatorPromise = (async () => {
      const schemaContent = await readCoreSchema();
      const schema = JSON.parse(schemaContent);
      return ajv.compile<CoreDocument>(schema);
    })();
  }

  return validatorPromise;
}

function mapErrors(errors: ErrorObject[] | null | undefined): ValidationError[] {
  if (!errors) {
    return [];
  }

  return errors.map((err) => ({
    message: err.message ?? 'validation error',
    instancePath: err.instancePath,
    schemaPath: err.schemaPath,
    keyword: err.keyword,
    params: err.params as Record<string, unknown>,
  }));
}

function isMeasurement(value: unknown): boolean {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof (value as { value?: unknown }).value === 'number' &&
    typeof (value as { unit?: unknown }).unit === 'string'
  );
}

function collectSemanticErrors(doc: CoreDocument): ValidationError[] {
  const errors: ValidationError[] = [];

  if (doc.kind === 'CharacterDefinition') {
    errors.push(...checkAppearanceMeasurements(doc));
  }

  return errors;
}

function checkAppearanceMeasurements(doc: CharacterDefinition): ValidationError[] {
  const errors: ValidationError[] = [];
  const appearance = doc.appearance;
  if (!appearance || typeof appearance !== 'object') {
    return errors;
  }

  const baseline = (appearance as Record<string, unknown>).baseline;
  if (baseline && typeof baseline === 'object') {
    const height = (baseline as Record<string, unknown>).height;
    if (height !== undefined && !isMeasurement(height)) {
      errors.push({
        message: 'height must use { value, unit }',
        instancePath: '/appearance/baseline/height',
        schemaPath: '#/properties/appearance/properties/baseline/properties/height',
        keyword: 'semantic',
        params: { expected: '{ value, unit }' },
      });
    }
  }

  return errors;
}

export async function validateAndNormalize(
  doc: unknown,
  mode: ValidationMode = 'relaxed',
  specPath?: string
): Promise<Result<CoreDocument>> {
  // Load specification
  let spec: Record<string, unknown>;
  try {
    const baseSpec = await readDefaultSpec();
    if (specPath) {
      const overlaySpec = await loadSpecOverlay(specPath);
      spec = mergeSpecs(baseSpec, overlaySpec);
    } else {
      spec = baseSpec;
    }
  } catch (error) {
    return {
      ok: false,
      warnings: [],
      errors: [{
        message: `Failed to load specification: ${error}`,
        instancePath: '/spec',
        schemaPath: '#/spec',
        keyword: 'spec_error',
        params: { error: String(error) },
      }],
    };
  }

  // Override mode from spec if provided
  if (spec.validation && typeof spec.validation === 'object' && 'mode' in spec.validation) {
    const specMode = (spec.validation as Record<string, unknown>).mode;
    if (specMode === 'relaxed' || specMode === 'strict') {
      mode = specMode;
    }
  }

  const validator = await loadValidator();
  const isValid = validator(doc);

  if (!isValid) {
    const errors = mapErrors(validator.errors);
    
    // In relaxed mode, filter to only critical errors
    if (mode === 'relaxed') {
      const criticalErrors = errors.filter(error => 
        error.keyword === 'required' || error.keyword === 'type'
      );
      return {
        ok: false,
        warnings: [],
        errors: criticalErrors,
      };
    }
    
    return {
      ok: false,
      warnings: [],
      errors,
    };
  }

  const cloned = JSON.parse(JSON.stringify(doc)) as CoreDocument;

  const semanticErrors = collectSemanticErrors(cloned);
  if (semanticErrors.length > 0) {
    if (mode === 'strict') {
      return {
        ok: false,
        warnings: [],
        errors: semanticErrors,
      };
    }
    // In relaxed mode, convert semantic errors to warnings
  }

  const warnings: Warning[] = [];
  
  // Convert semantic errors to warnings in relaxed mode
  if (mode === 'relaxed' && semanticErrors.length > 0) {
    warnings.push(...semanticErrors.map(error => ({
      code: 'VALIDATION_WARNING',
      path: error.instancePath,
      detail: error.message,
    })));
  }
  
  normalizeInPlace(cloned as unknown as Record<string, unknown>, warnings);
  warnings.push(...lint(cloned as unknown as Record<string, unknown>));

  return {
    ok: true,
    data: cloned,
    warnings,
  };
}
