import type { Warning } from './warnings.js';

export const ARROW = '↔';

const TOKEN_MAP: Record<string, string> = {
  '⇒': '-',
  _: '-',
};

export function canonicalAxis(name: string): string {
  for (const sep of [ARROW, '-', '_'] as const) {
    if (name.includes(sep)) {
      const index = name.indexOf(sep);
      const left = name.slice(0, index).trim();
      const right = name.slice(index + sep.length).trim();
      if (left && right) {
        return `${left}${ARROW}${right}`;
      }
    }
  }
  return name.trim();
}

export function normalizeToken(token: string | undefined | null): string {
  let out = token ?? '';
  for (const [src, dest] of Object.entries(TOKEN_MAP)) {
    out = out.split(src).join(dest);
  }
  out = out.trim();
  while (out.includes('--')) {
    out = out.replace(/--+/g, '-');
  }
  out = out.replace(/^-+/, '').replace(/-+$/, '');
  return out.toLowerCase();
}

export function lowerDedupe(arr?: string[] | null): string[] {
  const source = Array.isArray(arr) ? arr : [];
  const seen = new Set<string>();
  const out: string[] = [];
  for (const value of source) {
    const normalized = (value ?? '').trim().toLowerCase();
    if (normalized && !seen.has(normalized)) {
      seen.add(normalized);
      out.push(normalized);
    }
  }
  return out;
}

type MutableRecord = Record<string, any>;

export function normalizeInPlace(doc: MutableRecord, warnings: Warning[]): void {
  if (!doc || typeof doc !== 'object') {
    return;
  }

  const slug = doc.slug;
  if (typeof slug === 'string') {
    const normalizedSlug = normalizeToken(slug);
    if (normalizedSlug !== slug) {
      doc.slug = normalizedSlug;
      warnings.push({
        code: 'NORMALIZED_SLUG',
        path: 'slug',
        detail: `'${slug}' → '${normalizedSlug}'`,
      });
    }
  }

  const meta = doc.meta;
  if (meta && typeof meta === 'object') {
    const tags = (meta as MutableRecord).tags;
    if (Array.isArray(tags)) {
      (meta as MutableRecord).tags = lowerDedupe(tags);
    }
  }

  if (Array.isArray(doc.media_targets)) {
    doc.media_targets = lowerDedupe(doc.media_targets);
  }

  const contextualFit = doc.contextual_fit;
  if (contextualFit && typeof contextualFit === 'object') {
    const cf = contextualFit as MutableRecord;
    if (Array.isArray(cf.genres)) {
      cf.genres = lowerDedupe(cf.genres);
    }
    if (Array.isArray(cf.media)) {
      cf.media = lowerDedupe(cf.media);
    }
  }

  const personality = (doc.personality ?? {}) as MutableRecord;
  if (Array.isArray(personality.traits)) {
    const newTraits: MutableRecord[] = [];
    for (const trait of personality.traits as MutableRecord[]) {
      if (trait && typeof trait === 'object') {
        for (const field of ['axis', 'key', 'label', 'name'] as const) {
          const value = trait[field];
          if (typeof value === 'string') {
            const canonical = canonicalAxis(value);
            if (canonical !== value) {
              trait[field] = canonical;
              warnings.push({
                code: 'NORMALIZED_AXIS',
                path: `personality.traits[].${field}`,
                detail: `'${value}' → '${canonical}'`,
              });
            }
            break;
          }
        }

        if (trait.kind === 'profile' && trait.facets && typeof trait.facets === 'object' && !Array.isArray(trait.facets)) {
          const facets = trait.facets as MutableRecord;
          const normalizedFacets: MutableRecord = {};
          for (const [key, value] of Object.entries(facets)) {
            const canonical = canonicalAxis(key);
            if (canonical !== key) {
              warnings.push({
                code: 'NORMALIZED_AXIS',
                path: 'personality.traits[].facets',
                detail: `'${key}' → '${canonical}'`,
              });
            }
            normalizedFacets[canonical] = value;
          }
          trait.facets = normalizedFacets;
        }
      }
      newTraits.push(trait);
    }
    personality.traits = newTraits;
    doc.personality = personality;
  }

  const identity = (doc.identity ?? {}) as MutableRecord;
  if (Array.isArray(identity.composite_of)) {
    for (const member of identity.composite_of as MutableRecord[]) {
      if (member && typeof member === 'object' && typeof member.key === 'string') {
        const original = member.key;
        const canonical = canonicalAxis(original);
        if (canonical !== original) {
          member.key = canonical;
          warnings.push({
            code: 'NORMALIZED_AXIS',
            path: 'identity.composite_of[].key',
            detail: `'${original}' → '${canonical}'`,
          });
        }
      }
    }
  }
}
