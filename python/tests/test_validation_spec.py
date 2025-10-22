"""Unit tests for OCD validation spec system."""

import json
from pathlib import Path
import pytest
from ocd.validate.loader import SpecLoader
from ocd.validate.merger import SpecMerger
from ocd.validate.matcher import PathMatcher
from ocd.validate.evaluator import RuleEvaluator
from ocd.validate.validator import validate_and_normalize


class TestSpecLoader:
    """Test spec loading and schema validation."""
    
    def test_load_valid_default_spec(self):
        """Test loading the default spec."""
        loader = SpecLoader()
        spec = loader.load_spec("tests/specs/ocd-default-spec.ocd")
        assert spec["id"] == "ocd-default-spec"
        assert spec["type"] == "validationSpec"
    
    def test_load_invalid_spec_fails(self):
        """Test that invalid specs fail schema validation."""
        loader = SpecLoader()
        with pytest.raises(ValueError, match="Specification validation failed"):
            loader.load_spec("tests/specs/invalid-spec-missing-type.ocd")
    
    def test_load_character_file(self):
        """Test loading a character file."""
        loader = SpecLoader()
        char = loader.load_character("tests/characters/valid/hero_fantasy.yaml")
        assert char["id"] == "char-001"
        assert char["profile"]["name"] == "Aria Ironleaf"


class TestSpecMerger:
    """Test spec merging and extends resolution."""
    
    def test_merge_policy(self):
        """Test policy merging."""
        merger = SpecMerger()
        parent = {"policy": {"allowUnknownFields": True, "unknownFieldSeverity": "warning"}}
        child = {"policy": {"allowUnknownFields": False}}
        merged = merger.merge_specs([parent], child)
        assert merged["policy"]["allowUnknownFields"] is False
        assert merged["policy"]["unknownFieldSeverity"] == "warning"
    
    def test_merge_definitions(self):
        """Test definition merging."""
        merger = SpecMerger()
        parent = {"definitions": {"enums": {"Color": ["red", "blue"]}}}
        child = {"definitions": {"enums": {"Size": ["small", "large"]}}}
        merged = merger.merge_specs([parent], child)
        assert "Color" in merged["definitions"]["enums"]
        assert "Size" in merged["definitions"]["enums"]
    
    def test_merge_rules_deduplication(self):
        """Test that child rules override parent rules for same path."""
        merger = SpecMerger()
        parent = {"rules": [{"path": "id", "type": "string"}]}
        child = {"rules": [{"path": "id", "type": "string", "minLength": 10}]}
        merged = merger.merge_specs([parent], child)
        # Should have only one rule for "id" with minLength from child
        id_rules = [r for r in merged["rules"] if r["path"] == "id"]
        assert len(id_rules) == 1
        assert id_rules[0].get("minLength") == 10


class TestPathMatcher:
    """Test path matching."""
    
    def test_simple_path(self):
        """Test simple dot notation path."""
        matcher = PathMatcher()
        doc = {"profile": {"name": "Test"}}
        matches = matcher.find_matches(doc, "profile.name")
        assert len(matches) == 1
        assert matches[0]["value"] == "Test"
    
    def test_array_wildcard(self):
        """Test array wildcard matching."""
        matcher = PathMatcher()
        doc = {"tags": ["fantasy", "archer"]}
        matches = matcher.find_matches(doc, "tags[*]")
        assert len(matches) == 2
        assert matches[0]["value"] == "fantasy"
        assert matches[1]["value"] == "archer"
    
    def test_nested_array(self):
        """Test nested array paths."""
        matcher = PathMatcher()
        doc = {"equipment": [{"name": "Bow"}, {"name": "Sword"}]}
        matches = matcher.find_matches(doc, "equipment[*].name")
        assert len(matches) == 2
        assert matches[0]["value"] == "Bow"
        assert matches[1]["value"] == "Sword"


class TestRuleEvaluator:
    """Test validation rule evaluation."""
    
    def test_presence_required(self):
        """Test required field validation."""
        evaluator = RuleEvaluator(mode="strict")
        rule = {"path": "id", "presence": "required"}
        matches = []  # No matches = missing field
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "MISSING_REQUIRED"
    
    def test_type_validation(self):
        """Test type validation."""
        evaluator = RuleEvaluator(mode="strict")
        rule = {"path": "profile.name", "type": "string"}
        matches = [{"path": "profile.name", "value": 42}]
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "TYPE_MISMATCH"
    
    def test_enum_validation(self):
        """Test enum validation."""
        evaluator = RuleEvaluator(mode="strict")
        rule = {"path": "species", "enum": ["human", "elf", "dwarf"]}
        matches = [{"path": "species", "value": "android"}]
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "ENUM_VIOLATION"
    
    def test_pattern_validation(self):
        """Test pattern validation."""
        evaluator = RuleEvaluator(mode="strict")
        rule = {"path": "equipment[*].name", "pattern": "^((?!laser).)*$"}
        matches = [{"path": "equipment[0].name", "value": "Laser Pistol"}]
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "PATTERN_MISMATCH"
    
    def test_min_max_validation(self):
        """Test numeric min/max validation."""
        evaluator = RuleEvaluator(mode="strict")
        rule = {"path": "age", "min": 18, "max": 100}
        
        # Test below min
        matches = [{"path": "age", "value": 10}]
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "VALUE_TOO_LOW"
        
        # Test above max
        matches = [{"path": "age", "value": 150}]
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "VALUE_TOO_HIGH"
    
    def test_length_validation(self):
        """Test string length validation."""
        evaluator = RuleEvaluator(mode="strict")
        rule = {"path": "id", "minLength": 5, "maxLength": 20}
        
        # Test too short
        matches = [{"path": "id", "value": "abc"}]
        diags = evaluator.evaluate_rule(rule, matches, "test-spec", 1)
        assert len(diags) == 1
        assert diags[0].code == "STRING_TOO_SHORT"


class TestValidationIntegration:
    """Integration tests using full validation pipeline."""
    
    def test_valid_fantasy_character(self):
        """Test that valid fantasy character passes."""
        char = {
            "id": "char-001",
            "profile": {"name": "Aria Ironleaf"},
            "species": "elf",
            "tags": ["fantasy", "archer"],
            "equipment": [{"name": "Longbow"}]
        }
        result = validate_and_normalize(
            char, 
            mode="strict",
            spec_path="tests/specs/project-fantasy-spec.ocd"
        )
        assert result["ok"] is True
        assert len(result.get("errors", [])) == 0
    
    def test_scifi_character_fails_fantasy_spec(self):
        """Test that sci-fi character fails fantasy spec."""
        char = {
            "id": "char-002",
            "profile": {"name": "Zed Nova"},
            "species": "android",
            "tags": ["sci-fi", "space"],
            "equipment": [{"name": "Laser Pistol"}]
        }
        result = validate_and_normalize(
            char,
            mode="strict",
            spec_path="tests/specs/project-fantasy-spec.ocd"
        )
        assert result["ok"] is False
        assert len(result.get("errors", [])) >= 2
    
    def test_relaxed_vs_strict_mode(self):
        """Test that relaxed mode treats data errors as warnings."""
        char = {
            "id": "char-003",
            "profile": {"name": "Test"},
            "species": "invalid-species"
        }
        
        # Relaxed mode: data errors become warnings
        result_relaxed = validate_and_normalize(
            char,
            mode="relaxed",
            spec_path="tests/specs/project-fantasy-spec.ocd"
        )
        # Should pass but with warnings
        assert result_relaxed["ok"] is True
        assert len(result_relaxed.get("warnings", [])) > 0
        
        # Strict mode: data errors are errors
        result_strict = validate_and_normalize(
            char,
            mode="strict",
            spec_path="tests/specs/project-fantasy-spec.ocd"
        )
        assert result_strict["ok"] is False
        assert len(result_strict.get("errors", [])) > 0
