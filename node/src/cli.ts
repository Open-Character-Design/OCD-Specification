#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import process from 'node:process';

import YAML from 'yaml';

import { validateAndNormalize, type Result, type ValidationError } from './validate.js';
import type { Warning } from './warnings.js';

type Format = 'auto' | 'json' | 'yaml';

interface CliOptions {
  path: string;
  format: Format;
  mode: 'relaxed' | 'strict';
  spec?: string;
  printNormalized: boolean;
  indent: number;
  warningsAsErrors: boolean;
}

interface CliParseResult {
  options: CliOptions | null;
  showHelp: boolean;
  showVersion: boolean;
}

const require = createRequire(import.meta.url);
const { version } = require('../package.json') as { version: string };

function createDefaultOptions(): CliOptions {
  return {
    path: '',
    format: 'auto',
    mode: 'relaxed',
    printNormalized: false,
    indent: 2,
    warningsAsErrors: false,
  };
}

function parseArgs(args: string[]): CliParseResult {
  const options = createDefaultOptions();
  let showHelp = false;
  let showVersion = false;

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === '-h' || arg === '--help') {
      showHelp = true;
      continue;
    }
    if (arg === '-v' || arg === '--version') {
      showVersion = true;
      continue;
    }
    if (arg === '--print') {
      options.printNormalized = true;
      continue;
    }
    if (arg === '--warnings-as-errors') {
      options.warningsAsErrors = true;
      continue;
    }
    if (arg === '--mode') {
      const next = args[++index];
      if (!next) {
        throw new Error('--mode requires a value');
      }
      if (next !== 'relaxed' && next !== 'strict') {
        throw new Error("--mode must be one of 'relaxed' or 'strict'");
      }
      options.mode = next;
      continue;
    }
    if (arg === '--spec') {
      const next = args[++index];
      if (!next) {
        throw new Error('--spec requires a value');
      }
      options.spec = next;
      continue;
    }
    if (arg === '--indent') {
      const next = args[++index];
      if (!next) {
        throw new Error('--indent requires a value');
      }
      const indent = Number.parseInt(next, 10);
      if (Number.isNaN(indent) || indent < 0) {
        throw new Error('--indent must be a non-negative integer');
      }
      options.indent = indent;
      continue;
    }
    if (arg === '-f' || arg === '--format') {
      const next = args[++index];
      if (!next) {
        throw new Error('--format requires a value');
      }
      if (next !== 'auto' && next !== 'json' && next !== 'yaml') {
        throw new Error("--format must be one of 'auto', 'json', or 'yaml'");
      }
      options.format = next;
      continue;
    }
    if (arg.startsWith('-')) {
      throw new Error(`unknown option: ${arg}`);
    }
    if (options.path) {
      throw new Error('multiple input paths provided');
    }
    options.path = arg;
  }

  return { options: options.path ? options : null, showHelp, showVersion };
}

function printHelp(): void {
  const scriptName = path.basename(process.argv[1] ?? 'ocd-validate');
  console.log(`Usage: ${scriptName} [options] <path | ->`);
  console.log('');
  console.log('Validate and normalize an Open Character Specification document.');
  console.log('');
  console.log('Options:');
  console.log('  -h, --help                 Show this help message and exit');
  console.log('  -v, --version              Print the CLI version and exit');
  console.log('  -f, --format <auto|json|yaml>  Force the input document parser');
  console.log('      --mode <relaxed|strict>  Validation mode (default: relaxed)');
  console.log('      --spec <path>          Path to custom OCD specification overlay');
  console.log('      --print                Emit normalized JSON to stdout on success');
  console.log('      --indent <n>           Indentation to use with --print (default: 2)');
  console.log('      --warnings-as-errors   Exit with code 2 if warnings are produced');
}

async function readStdin(): Promise<string> {
  const chunks: string[] = [];
  return await new Promise((resolve, reject) => {
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk: string | Buffer) => {
      chunks.push(typeof chunk === 'string' ? chunk : chunk.toString('utf8'));
    });
    process.stdin.on('end', () => resolve(chunks.join('')));
    process.stdin.on('error', (error) => reject(error));
  });
}

async function readInput(pathOrStdin: string): Promise<string> {
  if (pathOrStdin === '-') {
    return await readStdin();
  }
  return await readFile(pathOrStdin, 'utf8');
}

function parseDocument(text: string, format: Format, source: string): unknown {
  if (format === 'json') {
    return JSON.parse(text);
  }
  if (format === 'yaml') {
    return YAML.parse(text);
  }

  try {
    return JSON.parse(text);
  } catch {
    try {
      return YAML.parse(text);
    } catch (error) {
      throw new Error(`failed to parse ${source} as JSON or YAML: ${(error as Error).message}`);
    }
  }
}

function printErrors(errors: ValidationError[]): void {
  if (errors.length === 0) {
    return;
  }
  console.error(`Validation failed with ${errors.length} error(s):`);
  for (const error of errors) {
    const location = error.instancePath || '<root>';
    console.error(`  - ${location}: ${error.message}`);
  }
}

function printWarnings(warnings: Warning[]): void {
  if (warnings.length === 0) {
    return;
  }
  console.error(`Validation produced ${warnings.length} warning(s):`);
  for (const warning of warnings) {
    console.error(`  - ${warning.path}: [${warning.code}] ${warning.detail}`);
  }
}

async function run(options: CliOptions): Promise<number> {
  const source = options.path === '-' ? 'stdin' : options.path;
  let raw: string;
  try {
    raw = await readInput(options.path);
  } catch (error) {
    console.error(`Failed to read ${source}: ${(error as Error).message}`);
    return 2;
  }

  let document: unknown;
  try {
    document = parseDocument(raw, options.format, source);
  } catch (error) {
    console.error((error as Error).message);
    return 2;
  }

  const result: Result<unknown> = await validateAndNormalize(document, options.mode, options.spec);
  if (!result.ok) {
    printErrors(result.errors ?? []);
    return 1;
  }

  printWarnings(result.warnings ?? []);
  if ((result.warnings?.length ?? 0) > 0 && options.warningsAsErrors) {
    return 2;
  }

  if (options.printNormalized) {
    const indent = options.indent > 0 ? options.indent : undefined;
    console.log(JSON.stringify(result.data, null, indent));
  } else {
    console.log('Validation succeeded.');
  }

  return 0;
}

async function main(): Promise<number> {
  let parsed: CliParseResult;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error((error as Error).message);
    return 2;
  }

  if (parsed.showHelp) {
    printHelp();
    return 0;
  }

  if (parsed.showVersion) {
    console.log(version);
    return 0;
  }

  if (!parsed.options) {
    printHelp();
    return 2;
  }

  return await run(parsed.options);
}

main()
  .then((code) => {
    if (code !== 0) {
      process.exitCode = code;
    }
  })
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
