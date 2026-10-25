"""Checks for adopted monotone 16-bit relative script-offset archives.

This is not a general archive discovery parser: callers supply an established
script count. Empty entries stay empty; backwards/interior sharing is rejected.
"""

from __future__ import annotations

import hashlib


def script_spans(payload: bytes, count: int) -> list[bytes]:
    if not isinstance(count, int) or count <= 0 or len(payload) < count * 2:
        raise ValueError("invalid script table size")
    offsets = [int.from_bytes(payload[i * 2:i * 2 + 2], "little") for i in range(count)]
    if offsets[0] != count * 2 or offsets != sorted(offsets) or offsets[-1] > len(payload):
        raise ValueError("unsupported script boundaries or sharing")
    offsets.append(len(payload))
    return [payload[a:b] for a, b in zip(offsets, offsets[1:])]


def verify_untouched_scripts(source: bytes, target: bytes, count: int, changed: set[int]) -> list[dict]:
    if not changed <= set(range(count)):
        raise ValueError("selected script outside table")
    before, after = script_spans(source, count), script_spans(target, count)
    preserved = []
    for i, (old, new) in enumerate(zip(before, after)):
        if i in changed:
            continue
        if old != new:
            raise ValueError(f"unselected script bytes changed: {i}")
        preserved.append({"script": i, "bytes": len(old), "sha256": hashlib.sha256(old).hexdigest()})
    return preserved
