{
  const TRAIT_KINDS = new Set(['bipolar', 'scalar', 'flag']);
  const TRAITS_KEY = 'traits';

  function normalizeBipolarName(name) {
    if (typeof name !== 'string') {
      return name;
    }

    if (name.includes('↔')) {
      return name;
    }

    const trimmed = name.trim();
    const match = trimmed.match(/^(.*?)\s*(?:-|_)\s*(.*?)$/u);
    if (!match) {
      return name;
    }

    const left = match[1].trim();
    const right = match[2].trim();

    if (!left || !right) {
      return name;
    }

    return `${left}↔${right}`;
  }

  function normalizeTraitEntry(entry, loc) {
    if (typeof entry !== 'object' || entry === null || Array.isArray(entry)) {
      error('Traits must be objects', loc);
    }

    if (!Object.prototype.hasOwnProperty.call(entry, 'kind')) {
      error('Trait entries must declare a kind', loc);
    }

    const kindValue = entry.kind;
    if (typeof kindValue !== 'string' || !TRAIT_KINDS.has(kindValue)) {
      error('Trait kind must be one of "bipolar", "scalar", or "flag"', loc);
    }

    if (kindValue === 'bipolar' && typeof entry.name === 'string') {
      entry.name = normalizeBipolarName(entry.name);
    }

    return entry;
  }

  function normalizeTraits(value, loc) {
    if (!Array.isArray(value)) {
      error('Traits must be expressed as an array', loc);
    }

    return value.map((entry) => normalizeTraitEntry(entry, loc));
  }

  function processTripleString(body) {
    let text = body.replace(/\r\n?/g, '\n');

    if (text.startsWith('\n')) {
      text = text.slice(1);
    }

    const lines = text.split('\n');

    while (lines.length > 0 && lines[lines.length - 1].trim() === '') {
      lines.pop();
    }

    let minIndent = Infinity;
    for (const line of lines) {
      if (line.trim() === '') {
        continue;
      }
      const match = line.match(/^[ \t]*/u);
      const indent = match ? match[0].length : 0;
      if (indent < minIndent) {
        minIndent = indent;
      }
    }

    if (!Number.isFinite(minIndent)) {
      minIndent = 0;
    }

    if (minIndent > 0) {
      for (let i = 0; i < lines.length; i += 1) {
        lines[i] = lines[i].slice(minIndent);
      }
    }

    return lines.join('\n');
  }
}

start
  = WS doc:Document WS { return doc; }

Document
  = headerBlock:HeaderBlock WS body:Object {
      return {
        headers: headerBlock,
        body,
      };
    }

HeaderBlock
  = BlankLine* first:HeaderLine rest:(BlankLine* HeaderLine)* trailing:BlankLine* {
      const lines = [first, ...rest.map(([, line]) => line)];
      const headers = Object.create(null);
      const keyLocations = new Map();

      for (const entry of lines) {
        if (headers[entry.key] !== undefined) {
          error(`Duplicate header "${entry.key}"`, entry.loc);
        }
        headers[entry.key] = entry.value;
        keyLocations.set(entry.key, entry.loc);
      }

      if (headers['ocd-t'] === undefined) {
        const loc = lines.length > 0 ? lines[0].loc : location();
        error('Missing required "ocd-t" header', loc);
      }

      const revision = headers['ocd-t'];
      if (typeof revision !== 'number' || !Number.isInteger(revision)) {
        const loc = keyLocations.get('ocd-t') ?? location();
        error('"ocd-t" header must be an integer', loc);
      }

      let version;
      if (Object.prototype.hasOwnProperty.call(headers, 'ocs-version')) {
        const value = headers['ocs-version'];
        if (typeof value !== 'string') {
          const loc = keyLocations.get('ocs-version') ?? location();
          error('"ocs-version" header must be a string', loc);
        }
        version = value;
      }

      const extras = Object.create(null);
      for (const [key, value] of Object.entries(headers)) {
        if (key === 'ocd-t' || key === 'ocs-version') {
          continue;
        }
        extras[key] = value;
      }

      return {
        revision,
        version,
        extras: Object.keys(extras).length > 0 ? extras : undefined,
      };
    }

HeaderLine
  = key:HeaderKey OptInlineWS ':' OptInlineWS
    value:HeaderValue OptInlineWS Comment?
    Newline+
    {
      const loc = location();
      return { key, value, loc };
    }

HeaderKey
  = $([A-Za-z_][A-Za-z0-9_\-]*('-'[A-Za-z0-9_\-]+)*)

HeaderValue
  = TripleString
  / String
  / Number
  / Bareword

Object
  = '{' WS members:ObjectMembers? WS '}' {
      const obj = {};

      if (members) {
        for (const entry of members) {
          if (Object.prototype.hasOwnProperty.call(obj, entry.key)) {
            error(`Duplicate key "${entry.key}"`, entry.loc);
          }
          obj[entry.key] = entry.value;
        }
      }

      return obj;
    }

ObjectMembers
  = head:ObjectMember tail:(ListSeparator ObjectMember)* trailing:ListSeparator? {
      return [head, ...tail.map(([, member]) => member)];
    }

ObjectMember
  = key:Key OptInlineWS ':' OptInlineWS
    value:Value
    {
      const loc = location();
      const normalizedValue = key === TRAITS_KEY ? normalizeTraits(value, loc) : value;
      return { key, value: normalizedValue, loc };
    }

Array
  = '[' WS elements:ArrayElements? WS ']' { return elements ?? []; }

ArrayElements
  = head:ArrayElement tail:(ListSeparator ArrayElement)* trailing:ListSeparator? {
      return [head, ...tail.map(([, element]) => element)];
    }

ArrayElement
  = value:Value { return value; }

Value
  = Object
  / Array
  / TripleString
  / String
  / Number
  / Boolean
  / Null
  / Bareword

Key
  = String
  / Bareword

TripleString
  = '"""' body:TripleStringBody '"""' { return processTripleString(body); }

TripleStringBody
  = $((!('"""') [\s\S])*)

String
  = '"' chars:StringCharacter* '"' { return chars.join(''); }

StringCharacter
  = !('"' / '\\' / '\r' / '\n') char:. { return char; }
  / '\\' sequence:EscapeSequence { return sequence; }

EscapeSequence
  = '"' { return '"'; }
  / '\\' { return '\\'; }
  / '/' { return '/'; }
  / 'b' { return '\b'; }
  / 'f' { return '\f'; }
  / 'n' { return '\n'; }
  / 'r' { return '\r'; }
  / 't' { return '\t'; }
  / 'u' digits:$(HexDigit HexDigit HexDigit HexDigit) { return String.fromCharCode(parseInt(digits, 16)); }

Number
  = value:$('-'? Integer Fraction? Exponent?) { return parseFloat(value); }

Integer
  = '0'
  / [1-9] [0-9]*

Fraction
  = '.' [0-9]+

Exponent
  = [eE] [+-]? [0-9]+

Boolean
  = 'true' { return true; }
  / 'false' { return false; }

Null
  = 'null' { return null; }

Bareword
  = $([A-Za-z_][A-Za-z0-9_\-/.]*)
  / $([0-9][A-Za-z0-9_\-/.]*)

ListSeparator
  = OptInlineWS ',' OptWS
  / LineBreak

BlankLine
  = OptInlineWS Comment? Newline+

LineBreak
  = OptInlineWS Comment? Newline+ OptWS

OptInlineWS
  = InlineWS
  / ''

OptWS
  = WS
  / ''

InlineWS
  = (Space / Comment)*

WS
  = (Space / Comment / Newline)*

Space
  = [ \t\f\v]+

Comment
  = '#' (!Newline .)*

Newline
  = '\r\n'
  / '\n'
  / '\r'

HexDigit
  = [0-9A-Fa-f]
