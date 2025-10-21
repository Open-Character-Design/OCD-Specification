from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from ocd.validate import validate_and_normalize, safe_load


EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"

VALID_EXPECTATIONS = {
    "valid_shapeshifter.yaml": "introversion-extroversion",
    "valid_hivemind.yaml": "empathy-sociopathy",
    "valid_symbiote.yaml": "dominant-persona",
    "valid_fourthwall.yaml": "fourth-wall_awareness",
}

INVALID_EXPECTATIONS = {
    "invalid_shapeshifter.yaml": "expected object",
    "invalid_hivemind.yaml": "control_share",
    "invalid_symbiote.yaml": "ref must be a uuid",
    "invalid_fourthwall.yaml": "Invalid isoformat string",
}


def load_example(name: str) -> dict:
    with (EXAMPLES_DIR / name).open("r", encoding="utf-8") as handle:
        return safe_load(handle.read())


def test_valid_edge_case_examples_round_trip() -> None:
    for filename, expected_trait in VALID_EXPECTATIONS.items():
        doc = load_example(filename)
        result = validate_and_normalize(doc)
        assert result["ok"], f"{filename} failed validation: {result.get('errors')}"

        data = result["data"]
        traits = data.get("personality", {}).get("traits", [])
        assert traits, f"{filename} missing personality traits"
        first_trait = traits[0]
        assert first_trait.get("key") == expected_trait

        assert not result.get("warnings"), f"{filename} emitted warnings: {result.get('warnings')}"


def test_invalid_edge_case_examples_fail_validation() -> None:
    for filename, expected_message in INVALID_EXPECTATIONS.items():
        doc = load_example(filename)
        result = validate_and_normalize(doc)
        assert not result["ok"], f"{filename} unexpectedly passed validation"
        messages = " ".join(error.get("msg", "") for error in result.get("errors", []))
        assert expected_message in messages


def test_symbiote_requires_secret_identity_for_hidden_members() -> None:
    base = load_example("valid_symbiote.yaml")
    mutated = deepcopy(base)
    mutated_identity = mutated.setdefault("identity", {})
    mutated_identity.pop("secret_identities", None)

    result = validate_and_normalize(mutated)
    assert result["ok"], result.get("errors")
    codes = {warning["code"] for warning in result.get("warnings", [])}
    assert "COMPOSITE_SECRET_WITHOUT_IDENTITY" in codes
