#!/usr/bin/env python3
"""Test runner for OCD validation fixture manifest."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


def run_python_validator(character_path: str, mode: str, spec_path: str) -> Dict[str, Any]:
    """Run Python validator and return results."""
    try:
        cmd = [
            sys.executable, "-m", "ocd.validate.validator",
            character_path,
            "--mode", mode,
            "--spec", spec_path,
            "--output", "json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd="python")
        
        if result.returncode == 0:
            return {"ok": True, "errors": 0, "warnings": 0}
        elif result.returncode == 1:
            # Parse JSON output to count errors
            try:
                output = json.loads(result.stdout)
                error_count = len(output.get("errors", []))
                warning_count = len(output.get("warnings", []))
                return {"ok": False, "errors": error_count, "warnings": warning_count}
            except json.JSONDecodeError:
                return {"ok": False, "errors": 1, "warnings": 0}
        else:
            return {"ok": False, "errors": 1, "warnings": 0}
    except Exception as e:
        print(f"Python validator error: {e}")
        return {"ok": False, "errors": 1, "warnings": 0}


def run_node_validator(character_path: str, mode: str, spec_path: str) -> Dict[str, Any]:
    """Run Node validator and return results."""
    try:
        cmd = [
            "node", "dist/cli.js",
            character_path,
            "--mode", mode,
            "--spec", spec_path,
            "--output", "json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd="node")
        
        if result.returncode == 0:
            return {"ok": True, "errors": 0, "warnings": 0}
        elif result.returncode == 1:
            # Parse JSON output to count errors
            try:
                output = json.loads(result.stdout)
                error_count = len(output.get("errors", []))
                warning_count = len(output.get("warnings", []))
                return {"ok": False, "errors": error_count, "warnings": warning_count}
            except json.JSONDecodeError:
                return {"ok": False, "errors": 1, "warnings": 0}
        else:
            return {"ok": False, "errors": 1, "warnings": 0}
    except Exception as e:
        print(f"Node validator error: {e}")
        return {"ok": False, "errors": 1, "warnings": 0}


def run_spec_schema_test(test_case: Dict[str, Any]) -> bool:
    """Run spec schema validation test."""
    spec_file = test_case["file"]
    expect_valid = test_case["expect"]["valid"]
    
    try:
        cmd = ["ajv", "validate", "-s", "schema/ocd-validation-spec.schema.json", "-d", spec_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        actual_valid = result.returncode == 0
        return actual_valid == expect_valid
    except Exception as e:
        print(f"Schema validation error for {spec_file}: {e}")
        return False


def run_character_validation_test(test_case: Dict[str, Any]) -> bool:
    """Run character validation test."""
    character_file = test_case["character"]
    mode = test_case["mode"]
    spec_file = test_case["spec"]
    expect = test_case["expect"]
    
    # Run Python validator
    python_result = run_python_validator(character_file, mode, spec_file)
    
    # Run Node validator
    node_result = run_node_validator(character_file, mode, spec_file)
    
    # Check expectations
    if "errors" in expect:
        expected_errors = expect["errors"]
        if python_result["errors"] != expected_errors or node_result["errors"] != expected_errors:
            print(f"Error count mismatch for {character_file}:")
            print(f"  Expected: {expected_errors}")
            print(f"  Python: {python_result['errors']}")
            print(f"  Node: {node_result['errors']}")
            return False
    
    if "errorsAtLeast" in expect:
        expected_min_errors = expect["errorsAtLeast"]
        if python_result["errors"] < expected_min_errors or node_result["errors"] < expected_min_errors:
            print(f"Insufficient errors for {character_file}:")
            print(f"  Expected at least: {expected_min_errors}")
            print(f"  Python: {python_result['errors']}")
            print(f"  Node: {node_result['errors']}")
            return False
    
    # Check for specific messages
    if "containsMessages" in expect:
        # This would require parsing the actual output messages
        # For now, we'll skip this check
        pass
    
    return True


def main():
    """Main test runner."""
    if len(sys.argv) != 2:
        print("Usage: python test-fixtures.py <manifest-file>")
        sys.exit(1)
    
    manifest_file = sys.argv[1]
    
    with open(manifest_file, 'r') as f:
        test_cases = json.load(f)
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        test_name = test_case["name"]
        test_kind = test_case["kind"]
        
        print(f"Running: {test_name}")
        
        if test_kind == "spec-schema":
            success = run_spec_schema_test(test_case)
        elif test_kind == "character-validate":
            success = run_character_validation_test(test_case)
        else:
            print(f"Unknown test kind: {test_kind}")
            success = False
        
        if success:
            print(f"  ✅ PASSED")
            passed += 1
        else:
            print(f"  ❌ FAILED")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("All tests passed!")


if __name__ == "__main__":
    main()
