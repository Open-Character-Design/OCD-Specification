import type { OcdtHeaders, OcdtParseResult } from './parser.js';

type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue };

type HeaderValue = string | number | boolean | null | JsonValue;

function formatHeaderValue(value: HeaderValue): string {
  if (typeof value === 'string') {
    return JSON.stringify(value);
  }

  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value);
  }

  if (value === null) {
    return 'null';
  }

  return JSON.stringify(value);
}

function serializeHeaders(headers: OcdtHeaders): string {
  const lines: string[] = [`ocd-t: ${headers.revision}`];

  if (headers.version !== undefined) {
    lines.push(`ocd-version: ${JSON.stringify(headers.version)}`);
  }

  if (headers.extras) {
    const entries = Object.entries(headers.extras).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0));
    for (const [key, value] of entries) {
      lines.push(`${key}: ${formatHeaderValue(value as HeaderValue)}`);
    }
  }

  return lines.join('\n');
}

function sortObjectKeys(value: JsonValue): JsonValue {
  if (Array.isArray(value)) {
    return value.map((entry) => sortObjectKeys(entry as JsonValue)) as JsonValue;
  }

  if (value && typeof value === 'object') {
    const entries = Object.entries(value as Record<string, JsonValue>);
    entries.sort(([a], [b]) => a.localeCompare(b));
    const sorted: Record<string, JsonValue> = {};
    for (const [key, entry] of entries) {
      sorted[key] = sortObjectKeys(entry as JsonValue);
    }
    return sorted;
  }

  return value;
}

export function stringifyOcdt(doc: OcdtParseResult): string {
  const headerBlock = serializeHeaders(doc.headers);
  const normalizedBody = sortObjectKeys(doc.body as JsonValue);
  const bodyBlock = JSON.stringify(normalizedBody, null, 2);
  return `${headerBlock}\n${bodyBlock}\n`;
}
