#!/usr/bin/env python3

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "python" / "src"))
from ocs.ocs_validate import validate_and_normalize  # type: ignore  # noqa: E402
from ocs.yaml_loader import safe_load as load_yaml  # type: ignore  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: ocs-validate <file.(yaml|json)> [--print]")
        raise SystemExit(2)

    path = sys.argv[1]
    raw = Path(path).read_text(encoding="utf-8")

    if path.endswith((".yaml", ".yml")):
        doc = load_yaml(raw)
    else:
        doc = json.loads(raw)

    result = validate_and_normalize(doc)

    if not result["ok"]:
        print("INVALID")
        for err in result["errors"]:
            print("-", err)
        raise SystemExit(1)

    print("OK")
    warnings = result.get("warnings") or []
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning['code']} @ {warning['path']}: {warning['detail']}")

    if "--print" in sys.argv:
        print(json.dumps(result["data"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
