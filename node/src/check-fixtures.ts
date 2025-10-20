import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { parse } from 'yaml';

import { parseOcst } from './parser.js';
import { stringifyOcst } from './serializer.js';
import { validateAndNormalize, type Warning } from './validate.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

const EXAMPLES_DIR = path.join(ROOT, 'examples');
const PY_FIXTURES_DIR = path.join(ROOT, 'python', 'tests', 'fixtures');
const CROSS_FIXTURES_DIR = path.join(ROOT, 'fixtures', 'cross');

interface FixtureExpectation {
  path: string;
  shouldPass: boolean;
}

async function listFixtures(dir: string, predicate: (file: string) => boolean, shouldPass: boolean): Promise<FixtureExpectation[]> {
  const entries = await readdir(dir);
  return entries
    .filter((file) => predicate(file))
    .map((file) => ({
      path: path.join(dir, file),
      shouldPass,
    }));
}

async function loadYaml(filePath: string): Promise<unknown> {
  const raw = await readFile(filePath, 'utf8');
  return parse(raw);
}

async function loadJsonFile<T>(filePath: string): Promise<T> {
  const raw = await readFile(filePath, 'utf8');
  return JSON.parse(raw) as T;
}

function canonicalWarningKey(warning: Warning | Record<string, unknown>): string {
  const code = (warning as Record<string, unknown>).code ?? null;
  const pathValue = (warning as Record<string, unknown>).path ?? null;
  const detail = (warning as Record<string, unknown>).detail ?? null;
  return JSON.stringify({ code, path: pathValue, detail });
}

function warningsEqual(actual: Warning[], expected: Warning[]): boolean {
  const actualKeys = actual.map((warning) => canonicalWarningKey(warning)).sort();
  const expectedKeys = expected.map((warning) => canonicalWarningKey(warning)).sort();
  if (actualKeys.length !== expectedKeys.length) {
    return false;
  }
  return actualKeys.every((value, index) => value === expectedKeys[index]);
}

function describeWarnings(warnings: Warning[]): string {
  if (warnings.length === 0) {
    return '[]';
  }
  const entries = warnings
    .map((warning) => canonicalWarningKey(warning))
    .map((key) => JSON.parse(key) as { code: unknown; path: unknown; detail: unknown });
  return JSON.stringify(entries, null, 2);
}

function pruneNulls(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map((entry) => pruneNulls(entry));
  }

  if (value && typeof value === 'object') {
    const result: Record<string, unknown> = {};
    for (const [key, entry] of Object.entries(value as Record<string, unknown>)) {
      if (entry === null || entry === undefined) {
        continue;
      }
      result[key] = pruneNulls(entry);
    }
    return result;
  }

  return value;
}

interface NormalizationResult {
  failures: number;
  warnings: Warning[];
}

async function checkNormalizedExpectations(
  label: string,
  document: unknown,
  expectedData: unknown,
  expectedWarnings: Warning[],
): Promise<NormalizationResult> {
  const result = await validateAndNormalize(document);
  if (!result.ok) {
    console.error(`❌ ${label} failed validation.`);
    for (const err of result.errors ?? []) {
      console.error(`   - ${err.instancePath || '<root>'}: ${err.message}`);
    }
    return { failures: 1, warnings: [] };
  }

  let failures = 0;

  try {
    const canonicalActual = pruneNulls(result.data);
    const canonicalExpected = pruneNulls(expectedData);
    assert.deepStrictEqual(canonicalActual, canonicalExpected);
  } catch (err) {
    failures += 1;
    console.error(`❌ ${label} normalized data mismatch.`);
    console.error(err instanceof Error ? err.message : String(err));
  }

  if (!warningsEqual(result.warnings, expectedWarnings)) {
    failures += 1;
    console.error(`❌ ${label} warning set mismatch.`);
    console.error('Expected warnings:', describeWarnings(expectedWarnings));
    console.error('Actual warnings  :', describeWarnings(result.warnings));
  }

  if (failures === 0) {
    console.log(`✅ ${label}`);
  }

  return { failures, warnings: result.warnings };
}

async function runStandardFixtures(): Promise<number> {
  const fixtures: FixtureExpectation[] = [
    ...(await listFixtures(EXAMPLES_DIR, (file) => file.startsWith('valid_') && file.endsWith('.yaml'), true)),
    ...(await listFixtures(EXAMPLES_DIR, (file) => file.startsWith('invalid_') && file.endsWith('.yaml'), false)),
    ...(await listFixtures(PY_FIXTURES_DIR, (file) => file.endsWith('.yaml') && !file.startsWith('invalid_'), true)),
    ...(await listFixtures(PY_FIXTURES_DIR, (file) => file.startsWith('invalid_') && file.endsWith('.yaml'), false)),
  ];

  let failures = 0;

  for (const fixture of fixtures) {
    const doc = await loadYaml(fixture.path);
    const result = await validateAndNormalize(doc);

    if (fixture.shouldPass && !result.ok) {
      failures += 1;
      console.error(`❌ ${fixture.path} expected to validate but failed.`);
      for (const err of result.errors ?? []) {
        console.error(`   - ${err.instancePath || '<root>'}: ${err.message}`);
      }
    } else if (!fixture.shouldPass && result.ok) {
      failures += 1;
      console.error(`❌ ${fixture.path} expected to fail validation but passed.`);
    } else {
      console.log(`✅ ${fixture.path}`);
    }
  }

  return failures;
}

async function runCrossFixtures(): Promise<number> {
  let failures = 0;
  const entries = (await readdir(CROSS_FIXTURES_DIR)).filter((file) => file.endsWith('.yaml')).sort();

  for (const entry of entries) {
    const baseName = entry.replace(/\.yaml$/, '');
    const yamlPath = path.join(CROSS_FIXTURES_DIR, `${baseName}.yaml`);
    const ocdPath = path.join(CROSS_FIXTURES_DIR, `${baseName}.ocd`);
    const expectedData = pruneNulls(
      await loadJsonFile<unknown>(path.join(CROSS_FIXTURES_DIR, `${baseName}.normalized.json`)),
    );
    const expectedWarnings = await loadJsonFile<Warning[]>(path.join(CROSS_FIXTURES_DIR, `${baseName}.warnings.json`));

    const yamlDoc = await loadYaml(yamlPath);
    const yamlOutcome = await checkNormalizedExpectations(`${baseName}.yaml`, yamlDoc, expectedData, expectedWarnings);
    failures += yamlOutcome.failures;

    let parsedOcst;
    try {
      const ocdSource = await readFile(ocdPath, 'utf8');
      parsedOcst = parseOcst(ocdSource);
    } catch (err) {
      failures += 1;
      console.error(`❌ ${baseName}.ocd failed to parse:`, err instanceof Error ? err.message : String(err));
      continue;
    }

    const ocdOutcome = await checkNormalizedExpectations(
      `${baseName}.ocd`,
      parsedOcst.body,
      expectedData,
      expectedWarnings,
    );
    failures += ocdOutcome.failures;

    if (ocdOutcome.failures === 0) {
      try {
        const canonicalText = stringifyOcst({ headers: parsedOcst.headers, body: expectedData });
        const reparsed = parseOcst(canonicalText);
        assert.deepStrictEqual(reparsed.headers, parsedOcst.headers);
        assert.deepStrictEqual(reparsed.body, expectedData);

        const roundTripResult = await validateAndNormalize(reparsed.body);
        if (!roundTripResult.ok) {
          failures += 1;
          console.error(`❌ ${baseName}.ocd round-trip failed validation.`);
          for (const err of roundTripResult.errors ?? []) {
            console.error(`   - ${err.instancePath || '<root>'}: ${err.message}`);
          }
        } else {
          console.log(`✅ ${baseName}.ocd round-trip`);
        }
      } catch (err) {
        failures += 1;
        console.error(`❌ ${baseName}.ocd round-trip mismatch.`);
        console.error(err instanceof Error ? err.message : String(err));
      }
    }
  }

  return failures;
}

async function main(): Promise<void> {
  let failures = 0;
  failures += await runStandardFixtures();
  failures += await runCrossFixtures();

  if (failures > 0) {
    throw new Error(`${failures} fixture(s) did not meet expectations.`);
  }
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
