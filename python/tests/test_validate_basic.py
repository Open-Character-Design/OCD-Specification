from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from ocs.ocs_validate import validate_and_normalize
from ocs.yaml_loader import safe_load


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_basic_bruenor() -> None:
    with (FIXTURE_DIR / "bruenor.yaml").open("r", encoding="utf-8") as handle:
        doc = safe_load(handle.read())
    result = validate_and_normalize(doc)
    assert result["ok"], result.get("errors")
    assert result["data"]["names"]["canon"] == "Bruenor"
    assert result["data"]["meta"]["tags"] == ["test"]
    traits = result["data"]["personality"]["traits"]
    assert any(trait.get("key") == "introversion↔extraversion" for trait in traits)


def test_normalization_slug_and_profile_facets() -> None:
    with (FIXTURE_DIR / "bruenor.yaml").open("r", encoding="utf-8") as handle:
        base = safe_load(handle.read())

    base["slug"] = "bruenor--battle"
    profile_trait = {
        "kind": "profile",
        "key": "temperament_introvert-extrovert",
        "facets": {
            "introversion-extraversion": 0.5,
            "thinking_feeling": 0.25,
        },
    }
    base.setdefault("personality", {}).setdefault("traits", []).append(profile_trait)

    result = validate_and_normalize(base)
    assert result["ok"], result.get("errors")
    assert result["data"]["slug"] == "bruenor-battle"

    normalized_profile = next(
        (trait for trait in result["data"]["personality"]["traits"] if trait.get("kind") == "profile"),
        None,
    )
    assert normalized_profile is not None
    assert "introversion↔extraversion" in normalized_profile["facets"]
    assert "thinking↔feeling" in normalized_profile["facets"]
    assert normalized_profile["key"] == "temperament_introvert↔extrovert"


def test_missing_last_modified_invalid() -> None:
    with (FIXTURE_DIR / "invalid_missing_last_modified.yaml").open("r", encoding="utf-8") as handle:
        doc = safe_load(handle.read())
    result = validate_and_normalize(doc)
    assert not result["ok"]
    assert any(
        tuple(error.get("loc", []))[-1:] == ("last_modified",)
        for error in result.get("errors", [])
    )


def test_missing_names_canon_invalid() -> None:
    with (FIXTURE_DIR / "invalid_missing_names_canon.yaml").open("r", encoding="utf-8") as handle:
        doc = safe_load(handle.read())
    result = validate_and_normalize(doc)
    assert not result["ok"]
    assert any(error.get("loc", []) and error.get("loc", [])[-1] == "canon" for error in result.get("errors", []))


def test_scalar_trait_range_enforced() -> None:
    with (FIXTURE_DIR / "bruenor.yaml").open("r", encoding="utf-8") as handle:
        base_doc = safe_load(handle.read())

    doc = deepcopy(base_doc)
    doc["personality"]["traits"][1]["value"] = 2.0

    result = validate_and_normalize(doc)
    assert not result["ok"]
    assert any(
        error.get("loc", []) and error["loc"][-1] == "value" for error in result.get("errors", [])
    )
    assert any(
        error.get("ctx", {}).get("model") == "ScalarTrait" and error.get("type") == "value_error"
        for error in result.get("errors", [])
    )

    doc["personality"]["traits"][1]["value"] = 1.5
    doc["personality"]["traits"][1]["scale"] = {"min": 0.0, "max": 2.0}

    result = validate_and_normalize(doc)
    assert result["ok"], result.get("errors")


def test_schema_validation_errors_surface() -> None:
    result = validate_and_normalize("not a valid document")
    assert not result["ok"]
    assert any(
        str(error.get("type", "")).startswith("jsonschema.") for error in result.get("errors", [])
    )
