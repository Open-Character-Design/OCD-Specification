/** Loader module for parsing OCD validation specs and character files. */

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { type ErrorObject, type ValidateFunction } from 'ajv';
import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import YAML from 'yaml';

export interface ValidationSpec {
  id: string;
  type: 'validationSpec';
  schemaVersion: number;
  extends?: string[];
  metadata?: {
    name?: string;
    description?: string;
    version?: string;
  };
  policy?: {
    allowUnknownFields?: boolean;
    allowUnknownTopLevel?: boolean;
    unknownFieldSeverity?: 'warning' | 'error';
  };
  definitions?: {
    enums?: Record<string, string[]>;
    types?: Record<string, any>;
    patterns?: Record<string, string>;
  };
  rules?: ValidationRule[];
  constraints?: {
    require?: (string | { path: string })[];
    forbid?: (string | { path: string })[];
    disallow?: {
      tags?: string[];
    };
    arrays?: {
      unique?: { path: string }[];
      minItems?: { path: string; value: number }[];
      maxItems?: { path: string; value: number }[];
    };
  };
}

export interface ValidationRule {
  path: string;
  presence?: 'required' | 'optional' | 'forbidden';
  type?: string | { type: string };
  enum?: string[] | string;
  const?: any;
  min?: number;
  max?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  format?: string;
  uniqueItems?: boolean;
  minItems?: number;
  maxItems?: number;
  items?: any;
  properties?: Record<string, any>;
  dependentRequired?: Record<string, string[]>;
  compare?: {
    equalTo?: string;
    notEqualTo?: string;
    greaterThan?: string;
    greaterOrEqual?: string;
    lessThan?: string;
    lessOrEqual?: string;
  };
  severity?: 'warning' | 'error';
  message?: string;
}

export class SpecLoader {
  private schemaValidator: ValidateFunction<ValidationSpec> | null = null;
  private schemaPath: string;

  constructor(schemaPath?: string) {
    this.schemaPath = schemaPath || 'schema/ocd-validation-spec.schema.json';
  }

  private async loadSchemaValidator(): Promise<ValidateFunction<ValidationSpec>> {
    if (!this.schemaValidator) {
      const ajv = new Ajv2020({
        strict: true,
        allErrors: true,
        allowUnionTypes: true,
      });
      addFormats(ajv);

      const candidates = [
        new URL(`../${this.schemaPath}`, import.meta.url),
        new URL(`../../${this.schemaPath}`, import.meta.url),
        new URL(`../../../${this.schemaPath}`, import.meta.url),
      ];

      let lastError: Error | null = null;
      for (const url of candidates) {
        try {
          const schemaPath = fileURLToPath(url);
          const schemaContent = await readFile(schemaPath, 'utf8');
          const schema = JSON.parse(schemaContent);
          this.schemaValidator = ajv.compile<ValidationSpec>(schema);
          break;
        } catch (error) {
          const err = error as NodeJS.ErrnoException;
          if (err.code === 'ENOENT') {
            lastError = err;
            continue;
          }
          throw err;
        }
      }

      if (!this.schemaValidator) {
        throw new Error('Validation spec schema could not be located');
      }
    }

    return this.schemaValidator;
  }

  async loadSpec(specPath: string): Promise<ValidationSpec> {
    const content = await readFile(specPath, 'utf8');
    
    let spec: ValidationSpec;
    try {
      spec = YAML.parse(content) as ValidationSpec;
    } catch (error) {
      throw new Error(`Failed to parse specification file: ${error}`);
    }

    // Validate against schema
    const validator = await this.loadSchemaValidator();
    const isValid = validator(spec);
    
    if (!isValid) {
      const errors = validator.errors || [];
      const errorMessages = errors.map(err => err.message).join(', ');
      throw new Error(`Specification validation failed: ${errorMessages}`);
    }

    return spec;
  }

  async loadCharacter(characterPath: string): Promise<any> {
    const content = await readFile(characterPath, 'utf8');
    
    try {
      return YAML.parse(content);
    } catch (error) {
      throw new Error(`Failed to parse character file: ${error}`);
    }
  }

  async resolveExtends(spec: ValidationSpec, baseDir?: string): Promise<ValidationSpec[]> {
    if (!spec.extends) {
      return [spec];
    }

    const baseDirPath = baseDir || '.';
    const extendedSpecs: ValidationSpec[] = [];

    for (const extendId of spec.extends) {
      const specFile = await this.findSpecById(extendId, baseDirPath);
      if (specFile) {
        const extendedSpec = await this.loadSpec(specFile);
        // Recursively resolve extends
        const resolvedSpecs = await this.resolveExtends(extendedSpec, baseDirPath);
        extendedSpecs.push(...resolvedSpecs);
      } else {
        throw new Error(`Could not find specification with ID: ${extendId}`);
      }
    }

    return [...extendedSpecs, spec];
  }

  private async findSpecById(specId: string, baseDir: string): Promise<string | null> {
    const basePath = new URL(`../${baseDir}`, import.meta.url);
    
    // Look in common locations
    const searchPaths = [
      new URL('tests/specs', basePath),
      new URL('specs', basePath),
      new URL('spec', basePath),
    ];

    for (const searchPath of searchPaths) {
      try {
        const searchPathStr = fileURLToPath(searchPath);
        const { readdir } = await import('node:fs/promises');
        const files = await readdir(searchPathStr);
        
        for (const file of files) {
          if (file.endsWith('.ocd')) {
            try {
              const specPath = fileURLToPath(new URL(file, searchPath));
              const spec = await this.loadSpec(specPath);
              if (spec.id === specId) {
                return specPath;
              }
            } catch {
              continue;
            }
          }
        }
      } catch {
        continue;
      }
    }

    return null;
  }
}
