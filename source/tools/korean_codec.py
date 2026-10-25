"""Small reversible codec for the EXE4.5 dialogue Hangul escape.

textpet_korean.py derives the production development plugin from pinned source
inputs. This independent codec supplies test vectors; find_escapes is only a
collision-search aid, not a script parser (command arguments are not skipped).
"""

from __future__ import annotations


PREFIX = b"\xF9\xFC"
HANGUL_BASE = 0xAC00
HANGUL_COUNT = 11172
# Stable extension indices after the complete Hangul syllable block.
# These are only supplied to the font when selected translations need them.
EXTRA_CHARACTER_METRICS = {",": {"index": HANGUL_COUNT, "vertical_shift": -1, "advance": 12},
                           "·": {"index": HANGUL_COUNT + 1, "vertical_shift": 0, "advance": 12}}
EXTRA_CHARACTER_INDICES = {ch: m["index"] for ch, m in EXTRA_CHARACTER_METRICS.items()}


def encode_syllable(ch: str) -> bytes:
    if len(ch) != 1:
        raise ValueError("expected one character")
    index = ord(ch) - HANGUL_BASE
    if not 0 <= index < HANGUL_COUNT:
        raise ValueError(f"not a precomposed Hangul syllable: {ch!r}")
    return PREFIX + index.to_bytes(2, "little")


def encode_hangul(text: str) -> bytes:
    return b"".join(encode_syllable(ch) for ch in text)


def encode_character(ch: str) -> bytes:
    if ch in EXTRA_CHARACTER_INDICES:
        return PREFIX + EXTRA_CHARACTER_INDICES[ch].to_bytes(2, "little")
    return encode_syllable(ch)


def decode_character(data: bytes, offset: int = 0) -> tuple[str, int]:
    if offset < 0 or data[offset:offset + 2] != PREFIX or offset + 4 > len(data):
        raise ValueError("not a complete F9 FC character escape")
    index = int.from_bytes(data[offset + 2:offset + 4], "little")
    for ch, extra_index in EXTRA_CHARACTER_INDICES.items():
        if index == extra_index:
            return ch, offset + 4
    return decode_syllable(data, offset)


def decode_syllable(data: bytes, offset: int = 0) -> tuple[str, int]:
    if offset < 0 or data[offset:offset + 2] != PREFIX or offset + 4 > len(data):
        raise ValueError("not a complete F9 FC Hangul escape")
    index = int.from_bytes(data[offset + 2:offset + 4], "little")
    if not 0 <= index < HANGUL_COUNT:
        raise ValueError(f"Hangul index out of range: {index}")
    return chr(HANGUL_BASE + index), offset + 4


def find_escapes(data: bytes) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    start = 0
    while True:
        at = data.find(PREFIX, start)
        if at < 0:
            break
        item: dict[str, object] = {"offset": at}
        try:
            ch, _ = decode_syllable(data, at)
            item.update({"valid_hangul": True, "character": ch,
                         "index": ord(ch) - HANGUL_BASE})
        except ValueError as exc:
            item.update({"valid_hangul": False, "error": str(exc)})
        hits.append(item)
        start = at + 2
    return hits
