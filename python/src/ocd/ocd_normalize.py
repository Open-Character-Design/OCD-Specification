from __future__ import annotations

from typing import Any, Dict, List

ARROW = "↔"
TOKEN_MAP = {
    "↔": "-",
    "⇒": "-",
    "_": "-",
}


def canonical_axis(name: str) -> str:
    """
    Normalize bipolar axis names:
    - accept '-', '_' or '↔' as separators
    - canonicalize to the dash '-' separator
    """
    for sep in (ARROW, "-", "_"):
        if sep in name:
            left, right = name.split(sep, 1)
            left = left.strip()
            right = right.strip()
            if left and right:
                return f"{left}-{right}"
    return name.strip()


def normalize_token(token: str) -> str:
    out = token or ""
    for src, dest in TOKEN_MAP.items():
        out = out.replace(src, dest)
    out = out.strip()
    while "--" in out:
        out = out.replace("--", "-")
    out = out.strip("-")
    return out.lower()


def lower_dedupe(strings: List[str]) -> List[str]:
    out: List[str] = []
    seen = set()
    for s in strings or []:
        t = (s or "").strip().lower()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def normalize_in_place(doc: Dict[str, Any], warnings: List[Dict[str, Any]]) -> None:
    # slug normalization
    slug = doc.get("slug")
    if isinstance(slug, str):
        normalized_slug = normalize_token(slug)
        if normalized_slug != slug:
            doc["slug"] = normalized_slug
            warnings.append(
                {
                    "code": "NORMALIZED_SLUG",
                    "path": "slug",
                    "detail": f"'{slug}' → '{normalized_slug}'",
                }
            )

    # meta.tags
    if isinstance(doc.get("meta"), dict):
        tags = doc["meta"].get("tags")
        if isinstance(tags, list):
            doc["meta"]["tags"] = lower_dedupe(tags)

    # media_targets
    if isinstance(doc.get("media_targets"), list):
        doc["media_targets"] = lower_dedupe(doc["media_targets"])

    # contextual_fit tokens
    cf = doc.get("contextual_fit")
    if isinstance(cf, dict):
        if isinstance(cf.get("genres"), list):
            cf["genres"] = lower_dedupe(cf["genres"])
        if isinstance(cf.get("media"), list):
            cf["media"] = lower_dedupe(cf["media"])
        doc["contextual_fit"] = cf

    # traits
    personality = doc.get("personality") or {}
    traits = personality.get("traits")
    if isinstance(traits, list):
        new_traits: List[Dict[str, Any]] = []
        for trait in traits:
            if isinstance(trait, dict):
                for field in ("axis", "key", "label", "name"):
                    if isinstance(trait.get(field), str):
                        original = trait[field]
                        canonical = canonical_axis(trait[field])
                        if canonical != original:
                            trait[field] = canonical
                            warnings.append(
                                {
                                    "code": "NORMALIZED_AXIS",
                                    "path": f"personality.traits[].{field}",
                                    "detail": f"'{original}' → '{canonical}'",
                                }
                            )
                        break
                if trait.get("kind") == "profile" and isinstance(trait.get("facets"), dict):
                    facets = trait["facets"]
                    normalized_facets: Dict[str, Any] = {}
                    for key, value in facets.items():
                        if isinstance(key, str):
                            canonical = canonical_axis(key)
                            if canonical != key:
                                warnings.append(
                                    {
                                        "code": "NORMALIZED_AXIS",
                                        "path": "personality.traits[].facets",
                                        "detail": f"'{key}' → '{canonical}'",
                                    }
                                )
                            normalized_facets[canonical] = value
                        else:
                            normalized_facets[key] = value
                    trait["facets"] = normalized_facets
            new_traits.append(trait)
        personality["traits"] = new_traits
        doc["personality"] = personality

    identity = doc.get("identity") or {}
    composite = identity.get("composite_of")
    if isinstance(composite, list):
        for member in composite:
            if isinstance(member, dict) and isinstance(member.get("key"), str):
                original = member["key"]
                canonical = canonical_axis(original)
                if canonical != original:
                    member["key"] = canonical
                    warnings.append(
                        {
                            "code": "NORMALIZED_AXIS",
                            "path": "identity.composite_of[].key",
                            "detail": f"'{original}' → '{canonical}'",
                        }
                    )
