import { parse as generateParse } from './generated/ocd-t-parser.js';

export interface OcdtHeaders {
  revision: number;
  version?: string;
  extras?: Record<string, unknown>;
}

export interface OcdtParseResult {
  headers: OcdtHeaders;
  body: unknown;
}

type GeneratedParse = (input: string) => OcdtParseResult;

const parseImpl = generateParse as GeneratedParse;

export function parseOcdt(input: string): OcdtParseResult {
  return parseImpl(input);
}
