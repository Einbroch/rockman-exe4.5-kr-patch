"""Protected-literal adapter for canonical TextPet TPL exports.

This is not a replacement command parser. TextPet owns binary commands;
independent source-payload and binary-roundtrip checks guard this adapter.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass


TOKEN = re.compile(r'^script\s+(\d+)\s+(\w+)\s*\{|"""[\s\S]*?"""|"(?:[^"\\\r\n]|\\.)*"', re.MULTILINE)


@dataclass(frozen=True)
class Literal:
    key: str
    language: str
    start: int
    end: int
    text: str


def literals(tpl: str) -> list[Literal]:
    archive = re.search(r"^@archive\s+(\S+)\s*$", tpl, re.MULTILINE)
    if not archive:
        raise ValueError("missing archive identifier")
    script, language, index = None, None, 0
    seen = set()
    result = []
    for token in TOKEN.finditer(tpl):
        if token.group(1) is not None:
            script, language, index = int(token.group(1)), token.group(2), 0
            if script in seen:
                raise ValueError("duplicate script ID")
            seen.add(script)
            continue
        if script is None:
            raise ValueError("literal outside a script")
        raw = token.group()
        if raw.startswith('"""'):
            body = raw[3:-3]
            if not body.startswith("\n") or not re.search(r"\n[ \t]*$", body):
                raise ValueError("non-canonical multiline literal")
            value = textwrap.dedent(body[1:body.rfind("\n")])
        else:
            value = raw[1:-1]
        # Canonical TextPet uses a literal backslash-n for e.g. "text\\n\\n".
        # Keep all other escapes fail-closed until their binary semantics are
        # covered. Never run Python's broad unicode_escape over Japanese text.
        if re.search(r"\\(?!n)", value) or '"' in value:
            raise ValueError("unsupported TPL escape")
        value = value.replace("\\n", "\n")
        result.append(Literal(f"{archive.group(1)}:{script}:{index}", language,
                              token.start(), token.end(), value))
        index += 1
    return result


def serialize(value: str) -> str:
    if not value or any(ch in value for ch in ('"', "\\", "\r", "\t")):
        raise ValueError("empty or unsupported literal text")
    # TextPet alpha3 can drop a leading blank line before an extended glyph in
    # a triple-quoted literal. Explicit escapes preserve the E8 byte boundary.
    # Explicit leading label padding must not be removed by the canonical
    # multiline reader's dedent. TextPet supports the same escaped form.
    if value.startswith(("\n", " ")):
        return '"' + value.replace("\n", "\\n") + '"'
    if "\n" in value:
        return '"""\n\t' + value.replace("\n", "\n\t") + '\n\t"""'
    return '"' + value + '"'


def skeleton(tpl: str) -> str:
    parts, at = [], 0
    for item in literals(tpl):
        parts.extend((tpl[at:item.start], f"<literal:{item.key}>"))
        at = item.end
    parts.append(tpl[at:])
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def replace_literals(tpl: str, units: list[dict], *, language: str = "mmbn45", trailing_spaces: dict | None = None) -> str:
    if language not in ("mmbn45", "mmbn45s"):
        raise ValueError("unsupported Hangul consumer language")
    indexed = {u["id"]: u for u in units}
    if len(indexed) != len(units):
        raise ValueError("duplicate translation unit")
    edits, found = [], set()
    for item in literals(tpl):
        if item.key not in indexed:
            continue
        unit = indexed[item.key]
        if item.language != language:
            raise ValueError("unsupported Hangul consumer language")
        if unit["source"] != item.text:
            raise ValueError(f"protected source mismatch: {item.key}")
        if unit["state"] not in ("needs_review", "reviewed"):
            raise ValueError(f"unsupported development translation state: {item.key}")
        # Current scene policy keeps line/page controls and choice padding.
        # Wording can change within each line; no implicit layout redesign.
        target = unit["translation"]
        if (item.text.count("\n") != target.count("\n")
                or len(item.text) - len(item.text.lstrip("\n")) != len(target) - len(target.lstrip("\n"))
                or len(item.text) - len(item.text.rstrip("\n")) != len(target) - len(target.rstrip("\n"))
                or (trailing_spaces or {}).get(item.key,len(item.text) - len(item.text.rstrip(" "))) != len(target) - len(target.rstrip(" "))):
            raise ValueError(f"protected line/choice-padding policy changed: {item.key}")
        edits.append((item.start, item.end, serialize(unit["translation"])))
        found.add(item.key)
    if found != set(indexed):
        raise ValueError(f"missing source units: {set(indexed) - found}")
    output = tpl
    for start, end, value in reversed(edits):
        output = output[:start] + value + output[end:]
    if skeleton(tpl) != skeleton(output):
        raise ValueError("protected command structure changed")
    return output


def resolve_units(asset: dict) -> list[dict]:
    """Join explicit unit-to-wording links without source-text fuzzy matching."""
    if asset["schema"] == 1:
        return asset["units"]
    if asset["schema"] != 2:
        raise ValueError("unknown translation schema")
    wordings = {w["id"]: w for w in asset["wordings"]}
    if len(wordings) != len(asset["wordings"]):
        raise ValueError("duplicate wording identity")
    output, used = [], set()
    for unit in asset["units"]:
        if set(unit) != {"id", "source", "wording_id"}:
            raise ValueError("unexpected protected translation fields")
        wording = wordings[unit["wording_id"]]
        output.append({"id": unit["id"], "source": unit["source"],
                       "translation": wording["translation"], "state": wording["state"]})
        used.add(unit["wording_id"])
    if used != set(wordings):
        raise ValueError("unreferenced wording in selected translation asset")
    return output
