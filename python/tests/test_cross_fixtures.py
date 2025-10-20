from __future__ import annotations

import json
from pathlib import Path

import pytest

from ocs.ocs_validate import validate_and_normalize
from ocs.yaml_loader import safe_load

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "cross"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonicalize_warnings(warnings: list[dict[str, object]]) -> set[tuple[object, ...]]:
    normalized: set[tuple[object, ...]] = set()
    for warning in warnings:
        normalized.add(
            (
                warning.get("code"),
                warning.get("path"),
                warning.get("detail"),
            )
        )
    return normalized


@pytest.mark.parametrize("yaml_path", sorted(FIXTURE_DIR.glob("*.yaml"), key=lambda p: p.name))
def test_cross_fixture_normalization_matches_expectations(yaml_path: Path) -> None:
    expected_data = load_json(yaml_path.with_suffix(".normalized.json"))
    expected_warnings = load_json(yaml_path.with_suffix(".warnings.json"))

    with yaml_path.open("r", encoding="utf-8") as handle:
        document = safe_load(handle.read())

    result = validate_and_normalize(document)
    assert result["ok"], result.get("errors")
    assert result["data"] == expected_data

    actual_warnings = result.get("warnings", [])
    assert canonicalize_warnings(actual_warnings) == canonicalize_warnings(expected_warnings)
