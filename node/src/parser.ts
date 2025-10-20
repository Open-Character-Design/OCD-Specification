import { parse as generateParse } from './generated/ocs-t-parser.js';

export interface OcstHeaders {
  revision: number;
  version?: string;
  extras?: Record<string, unknown>;
}

export interface OcstParseResult {
  headers: OcstHeaders;
  body: unknown;
}

type GeneratedParse = (input: string) => OcstParseResult;

const parseImpl = generateParse as GeneratedParse;

export function parseOcst(input: string): OcstParseResult {
  return parseImpl(input);
}
