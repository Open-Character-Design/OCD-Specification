from __future__ import annotations
import re
from typing import Any, Dict, List

from .ocs_normalize import normalize_token


ASCII_CANON_RE = re.compile(r"^[A-Za-z0-9 _\-]+$")


def _slugify_canon(value: str) -> str:
    slug_source = re.sub(r"[^0-9A-Za-z]+", "-", value)
    return normalize_token(slug_source)


def lint(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    warnings: List[Dict[str, Any]] = []

    kind = doc.get("kind")

    if kind == "CharacterDefinition":
        names = doc.get("names")
        if not isinstance(names, dict) or "canon" not in names:
            warnings.append(
                {
                    "code": "MISSING_CANON_NAME",
                    "path": "names",
                    "detail": "CharacterDefinition is missing names.canon",
                }
            )
        else:
            canon = names.get("canon")
            if not isinstance(canon, str) or not canon.strip():
                warnings.append(
                    {
                        "code": "MISSING_CANON_NAME",
                        "path": "names.canon",
                        "detail": "names.canon must be a non-empty string",
                    }
                )
            else:
                trimmed = canon.strip()
                if trimmed != canon:
                    warnings.append(
                        {
                            "code": "NONCANONICAL_CANON_NAME",
                            "path": "names.canon",
                            "detail": f"names.canon contains leading/trailing whitespace: '{canon}' → '{trimmed}'",
                        }
                    )
                slug = doc.get("slug")
                if (
                    isinstance(slug, str)
                    and ASCII_CANON_RE.match(trimmed)
                ):
                    expected_slug = _slugify_canon(trimmed)
                    if expected_slug and slug != expected_slug:
                        warnings.append(
                            {
                                "code": "NONCANONICAL_CANON_NAME",
                                "path": "names.canon",
                                "detail": f"slug '{slug}' does not match canonical name slug '{expected_slug}'",
                            }
                        )

        for field in ("state", "progression", "session"):
            if field in doc:
                warnings.append(
                    {
                        "code": "DEFINITION_RUNTIME_FIELD",
                        "path": field,
                        "detail": f"'{field}' is reserved for CharacterInstance",
                    }
                )

    identity = doc.get("identity") or {}
    composite = identity.get("composite_of")
    secret_identities = identity.get("secret_identities")
    if isinstance(composite, list):
        total_share = 0.0
        has_secret_exposure = False
        for member in composite:
            if not isinstance(member, dict):
                continue
            share = member.get("control_share")
            if isinstance(share, (int, float)):
                total_share += share
            exposure = member.get("exposure")
            if exposure == "secret":
                has_secret_exposure = True
        if total_share > 1.0 + 1e-6:
            warnings.append(
                {
                    "code": "COMPOSITE_CONTROL_SHARE_OVERFLOW",
                    "path": "identity.composite_of",
                    "detail": f"composite control_share sum {total_share:.2f} exceeds 1.0",
                }
            )

        has_secret_identity = isinstance(secret_identities, list) and len(secret_identities) > 0
        if has_secret_exposure and not has_secret_identity:
            warnings.append(
                {
                    "code": "COMPOSITE_SECRET_WITHOUT_IDENTITY",
                    "path": "identity.composite_of",
                    "detail": "composite members marked as secret but no secret_identities defined",
                }
            )
        if has_secret_identity and not has_secret_exposure:
            warnings.append(
                {
                    "code": "COMPOSITE_SECRET_IDENTITY_MISMATCH",
                    "path": "identity.composite_of",
                    "detail": "secret_identities present but no composite members are marked secret",
                }
            )

    # rating vs audience sanity (best effort)
    meta = doc.get("meta_properties") or {}
    target = meta.get("target_audience") or {}
    age = target.get("age_range")
    appropriateness = meta.get("appropriateness") or {}
    language = (appropriateness.get("language") or "").lower()
    if isinstance(age, str):
        try:
            lower_bound = int(age.split("+")[0])
            if lower_bound < 13 and language == "explicit":
                warnings.append(
                    {
                        "code": "RATING_CONFLICT",
                        "path": "meta_properties.appropriateness.language",
                        "detail": f"language=explicit with age_range={age}",
                    }
                )
        except Exception:
            pass

    # skills with no tags
    capabilities = doc.get("capabilities") or {}
    skills = capabilities.get("skills") or []
    for index, skill in enumerate(skills):
        if isinstance(skill, dict) and skill.get("level") and not skill.get("tags"):
            warnings.append(
                {
                    "code": "MISSING_SKILL_TAGS",
                    "path": f"capabilities.skills[{index}]",
                    "detail": "skill has level but empty/missing tags",
                }
            )

    # unresolved relationship refs (presence only)
    background = doc.get("background") or {}
    relationships = background.get("relationships") or []
    for index, relation in enumerate(relationships):
        if isinstance(relation, dict):
            ref = relation.get("target_ref")
            if not ref or not isinstance(ref, str):
                warnings.append(
                    {
                        "code": "UNRESOLVED_REF",
                        "path": f"background.relationships[{index}].target_ref",
                        "detail": "missing or non-string target_ref",
                    }
                )

    return warnings
