from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Tuple

try:  # pragma: no cover - exercised when dependency available
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore

Line = Tuple[int, str]


def safe_load(text: str) -> Any:
    if yaml is not None:  # pragma: no branch - simple runtime check
        return yaml.safe_load(text)
    parser = _MiniYamlParser(_normalize(_preprocess(text), 0))
    value, _ = parser.parse_block(0, 0)
    return value


def _preprocess(text: str) -> List[Line]:
    lines: List[Line] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    return lines


def _normalize(lines: Sequence[Line], base: int) -> List[Line]:
    return [(indent - base, content) for indent, content in lines]


@dataclass
class _MiniYamlParser:
    lines: List[Line]

    def parse_block(self, index: int, indent: int) -> Tuple[Any, int]:
        mapping: dict[str, Any] = {}
        sequence: List[Any] | None = None
        length = len(self.lines)

        while index < length:
            current_indent, content = self.lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                break

            if content.startswith("-"):
                if mapping:
                    raise ValueError("cannot mix mapping and sequence at same indent")
                if sequence is None:
                    sequence = []
                value_text = content[2:].strip()
                index += 1
                next_index = index
                while next_index < length and self.lines[next_index][0] > current_indent:
                    next_index += 1
                subset = self.lines[index:next_index]
                value = self._parse_sequence_item(value_text, subset, current_indent)
                sequence.append(value)
                index = next_index
                continue

            if sequence is not None:
                raise ValueError("cannot mix sequence and mapping entries")

            key, value_text = _split_key_value(content)
            index += 1
            if value_text is None:
                value, index = self.parse_block(index, current_indent + 2)
            else:
                value = _parse_value(value_text, current_indent)
            mapping[key] = value

        if sequence is not None:
            return sequence, index
        return mapping, index

    def _parse_sequence_item(self, value_text: str, subset: Sequence[Line], current_indent: int) -> Any:
        if not subset and value_text and _is_simple_scalar(value_text):
            return _parse_scalar(value_text)

        local: List[Line] = []
        if value_text:
            local.append((current_indent + 2, value_text))
        local.extend(subset)
        if not local:
            return None
        normalized = _normalize(local, current_indent + 2)
        nested = _MiniYamlParser(normalized)
        value, _ = nested.parse_block(0, 0)
        return value


def _split_key_value(content: str) -> Tuple[str, Optional[str]]:
    if ":" not in content:
        return content.strip(), None
    key, rest = content.split(":", 1)
    key = key.strip()
    rest = rest.strip()
    return key, rest or None


def _parse_value(token: str, current_indent: int) -> Any:
    if token.startswith("[") and token.endswith("]"):
        return _parse_inline_list(token)
    if token.startswith("{") and token.endswith("}"):
        return _parse_inline_map(token, current_indent)
    return _parse_scalar(token)


def _parse_inline_list(token: str) -> List[Any]:
    inner = token[1:-1].strip()
    if not inner:
        return []
    parts = _split_top_level(inner, ",")
    return [_parse_scalar(part.strip()) for part in parts]


def _parse_inline_map(token: str, current_indent: int) -> dict[str, Any]:
    inner = token[1:-1].strip()
    if not inner:
        return {}
    parts = _split_top_level(inner, ",")
    lines = [(current_indent + 2, part.strip()) for part in parts if part.strip()]
    normalized = _normalize(lines, current_indent + 2)
    parser = _MiniYamlParser(normalized)
    value, _ = parser.parse_block(0, 0)
    if not isinstance(value, dict):
        raise ValueError("inline map did not produce mapping")
    return value


def _split_top_level(text: str, delimiter: str) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    depth_brace = depth_bracket = 0
    in_single = in_double = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif not in_single and not in_double:
            if ch == "{":
                depth_brace += 1
            elif ch == "}":
                depth_brace = max(0, depth_brace - 1)
            elif ch == "[":
                depth_bracket += 1
            elif ch == "]":
                depth_bracket = max(0, depth_bracket - 1)
            elif ch == delimiter and depth_brace == 0 and depth_bracket == 0:
                parts.append("".join(buf))
                buf = []
                i += 1
                continue
        buf.append(ch)
        i += 1
    if buf:
        parts.append("".join(buf))
    return parts


def _parse_scalar(token: str) -> Any:
    if (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
        try:
            return ast.literal_eval(token)
        except Exception:
            return token[1:-1]
    lowered = token.lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    if lowered in {"null", "none", "~"}:
        return None
    try:
        if token.startswith("0") and token != "0" and not token.startswith("0."):
            raise ValueError
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


def _is_simple_scalar(token: str) -> bool:
    if token.startswith(("[", "{")):
        return False
    return ":" not in token
