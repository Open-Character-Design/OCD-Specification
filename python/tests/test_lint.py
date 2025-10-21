from __future__ import annotations

from ocd.validate import lint


def extract_codes(warnings):
    return {w["code"] for w in warnings}


def test_missing_names_canon_warns() -> None:
    doc = {"kind": "CharacterDefinition", "names": {}}

    warnings = lint(doc)

    assert "MISSING_CANON_NAME" in extract_codes(warnings)


def test_noncanonical_names_trim_warns() -> None:
    doc = {
        "kind": "CharacterDefinition",
        "slug": "bruenor",
        "names": {"canon": " Bruenor "},
    }

    warnings = lint(doc)

    assert "NONCANONICAL_CANON_NAME" in extract_codes(warnings)


def test_runtime_fields_warn() -> None:
    doc = {
        "kind": "CharacterDefinition",
        "names": {"canon": "Bruenor"},
        "state": {},
        "progression": {},
        "session": {},
    }

    warnings = lint(doc)

    codes = extract_codes(warnings)
    assert "DEFINITION_RUNTIME_FIELD" in codes
    # ensure each reserved field triggers a warning
    assert len([w for w in warnings if w["code"] == "DEFINITION_RUNTIME_FIELD"]) == 3


def test_composite_control_share_overflow_warns() -> None:
    doc = {
        "identity": {
            "composite_of": [
                {"control_share": 0.6, "exposure": "public"},
                {"control_share": 0.5, "exposure": "secret"},
            ]
        }
    }

    warnings = lint(doc)

    assert "COMPOSITE_CONTROL_SHARE_OVERFLOW" in extract_codes(warnings)


def test_composite_secret_mismatch_warns() -> None:
    doc_missing_secret_id = {
        "identity": {
            "composite_of": [
                {"control_share": 0.4, "exposure": "secret"},
            ]
        }
    }

    missing_secret_warnings = lint(doc_missing_secret_id)
    assert "COMPOSITE_SECRET_WITHOUT_IDENTITY" in extract_codes(missing_secret_warnings)

    doc_missing_secret_exposure = {
        "identity": {
            "composite_of": [
                {"control_share": 0.5, "exposure": "public"},
            ],
            "secret_identities": [
                {"public_name": "Mask", "exposure_risk": 0.8},
            ],
        }
    }

    mismatch_warnings = lint(doc_missing_secret_exposure)
    assert "COMPOSITE_SECRET_IDENTITY_MISMATCH" in extract_codes(mismatch_warnings)
