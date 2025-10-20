import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

import { type ErrorObject, type ValidateFunction } from 'ajv';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';

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

const ajv = new Ajv2020({
  strict: true,
  allErrors: true,
  allowUnionTypes: true,
});
addFormats(ajv);

let validatorPromise: Promise<ValidateFunction<CoreDocument>> | null = null;

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

export async function validateAndNormalize(doc: unknown): Promise<Result<CoreDocument>> {
  const validator = await loadValidator();
  const isValid = validator(doc);

  if (!isValid) {
    return {
      ok: false,
      warnings: [],
      errors: mapErrors(validator.errors),
    };
  }

  const cloned = JSON.parse(JSON.stringify(doc)) as CoreDocument;

  const semanticErrors = collectSemanticErrors(cloned);
  if (semanticErrors.length > 0) {
    return {
      ok: false,
      warnings: [],
      errors: semanticErrors,
    };
  }

  const warnings: Warning[] = [];
  normalizeInPlace(cloned as unknown as Record<string, unknown>, warnings);
  warnings.push(...lint(cloned as unknown as Record<string, unknown>));

  return {
    ok: true,
    data: cloned,
    warnings,
  };
}
