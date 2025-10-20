import type { Warning } from './warnings.js';
import { normalizeToken } from './normalize.js';

const ASCII_CANON_RE = /^[A-Za-z0-9 _\-]+$/;

function slugifyCanon(value: string): string {
  const slugSource = value.replace(/[^0-9A-Za-z]+/g, '-');
  return normalizeToken(slugSource);
}

type MutableRecord = Record<string, any>;

export function lint(doc: MutableRecord): Warning[] {
  const warnings: Warning[] = [];

  const kind = doc?.kind;

  if (kind === 'CharacterDefinition') {
    const names = doc.names as MutableRecord | undefined;
    if (!names || typeof names !== 'object' || !('canon' in names)) {
      warnings.push({
        code: 'MISSING_CANON_NAME',
        path: 'names',
        detail: 'CharacterDefinition is missing names.canon',
      });
    } else {
      const canon = names.canon;
      if (typeof canon !== 'string' || !canon.trim()) {
        warnings.push({
          code: 'MISSING_CANON_NAME',
          path: 'names.canon',
          detail: 'names.canon must be a non-empty string',
        });
      } else {
        const trimmed = canon.trim();
        if (trimmed !== canon) {
          warnings.push({
            code: 'NONCANONICAL_CANON_NAME',
            path: 'names.canon',
            detail: `names.canon contains leading/trailing whitespace: '${canon}' → '${trimmed}'`,
          });
        }
        const slug = doc.slug;
        if (typeof slug === 'string' && ASCII_CANON_RE.test(trimmed)) {
          const expectedSlug = slugifyCanon(trimmed);
          if (expectedSlug && slug !== expectedSlug) {
            warnings.push({
              code: 'NONCANONICAL_CANON_NAME',
              path: 'names.canon',
              detail: `slug '${slug}' does not match canonical name slug '${expectedSlug}'`,
            });
          }
        }
      }
    }

    for (const field of ['state', 'progression', 'session'] as const) {
      if (field in doc) {
        warnings.push({
          code: 'DEFINITION_RUNTIME_FIELD',
          path: field,
          detail: `'${field}' is reserved for CharacterInstance`,
        });
      }
    }
  }

  const identity = (doc.identity ?? {}) as MutableRecord;
  const composite = identity.composite_of;
  const secretIdentities = identity.secret_identities;
  if (Array.isArray(composite)) {
    let totalShare = 0;
    let hasSecretExposure = false;
    for (const member of composite as MutableRecord[]) {
      if (!member || typeof member !== 'object') {
        continue;
      }
      const share = member.control_share;
      if (typeof share === 'number') {
        totalShare += share;
      }
      if (member.exposure === 'secret') {
        hasSecretExposure = true;
      }
    }
    if (totalShare > 1.0 + 1e-6) {
      warnings.push({
        code: 'COMPOSITE_CONTROL_SHARE_OVERFLOW',
        path: 'identity.composite_of',
        detail: `composite control_share sum ${totalShare.toFixed(2)} exceeds 1.0`,
      });
    }

    const hasSecretIdentity = Array.isArray(secretIdentities) && secretIdentities.length > 0;
    if (hasSecretExposure && !hasSecretIdentity) {
      warnings.push({
        code: 'COMPOSITE_SECRET_WITHOUT_IDENTITY',
        path: 'identity.composite_of',
        detail: 'composite members marked as secret but no secret_identities defined',
      });
    }
    if (hasSecretIdentity && !hasSecretExposure) {
      warnings.push({
        code: 'COMPOSITE_SECRET_IDENTITY_MISMATCH',
        path: 'identity.composite_of',
        detail: 'secret_identities present but no composite members are marked secret',
      });
    }
  }

  const metaProps = (doc.meta_properties ?? {}) as MutableRecord;
  const target = (metaProps.target_audience ?? {}) as MutableRecord;
  const ageRange = target.age_range;
  const appropriateness = (metaProps.appropriateness ?? {}) as MutableRecord;
  const language = typeof appropriateness.language === 'string' ? appropriateness.language.toLowerCase() : '';
  if (typeof ageRange === 'string') {
    const parts = ageRange.split('+');
    const lower = Number.parseInt(parts[0] ?? '', 10);
    if (!Number.isNaN(lower) && lower < 13 && language === 'explicit') {
      warnings.push({
        code: 'RATING_CONFLICT',
        path: 'meta_properties.appropriateness.language',
        detail: `language=explicit with age_range=${ageRange}`,
      });
    }
  }

  const capabilities = (doc.capabilities ?? {}) as MutableRecord;
  const skills = capabilities.skills;
  if (Array.isArray(skills)) {
    skills.forEach((skill, index) => {
      if (skill && typeof skill === 'object') {
        const record = skill as MutableRecord;
        if (record.level && (!record.tags || (Array.isArray(record.tags) && record.tags.length === 0))) {
          warnings.push({
            code: 'MISSING_SKILL_TAGS',
            path: `capabilities.skills[${index}]`,
            detail: 'skill has level but empty/missing tags',
          });
        }
      }
    });
  }

  const background = (doc.background ?? {}) as MutableRecord;
  const relationships = background.relationships;
  if (Array.isArray(relationships)) {
    relationships.forEach((relation, index) => {
      if (relation && typeof relation === 'object') {
        const ref = (relation as MutableRecord).target_ref;
        if (typeof ref !== 'string' || !ref) {
          warnings.push({
            code: 'UNRESOLVED_REF',
            path: `background.relationships[${index}].target_ref`,
            detail: 'missing or non-string target_ref',
          });
        }
      }
    });
  }

  return warnings;
}
