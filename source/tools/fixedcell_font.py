"""Deterministic candidate BDF -> native 8x16 4-bpp fixed-cell records.

The two 8x8 tiles are top then bottom. No resampling, invented strokes,
fallback characters, or silent clipping. This does not define an encoding.
"""
from __future__ import annotations

from pathlib import Path


def pack_pixels(pixels: list[list[int]]) -> bytes:
    if len(pixels) != 16 or any(len(row) != 8 for row in pixels):
        raise ValueError("expected 8x16 pixels")
    if any(type(p) is not int or not 0 <= p <= 15 for row in pixels for p in row):
        raise ValueError("4-bpp palette index out of range")
    return bytes(row[x] | row[x + 1] << 4 for row in pixels for x in range(0, 8, 2))


def unpack_pixels(record: bytes) -> list[list[int]]:
    if len(record) != 64:
        raise ValueError("expected 64-byte cell")
    return [[(record[y * 4 + x // 2] >> (4 * (x % 2))) & 15 for x in range(8)] for y in range(16)]


def rasterize(width: int, height: int, xoff: int, yoff: int, rows: list[int],
              *, baseline: int, background: int, ink: int, shadow: int) -> bytes:
    top = baseline - height - yoff
    if (width <= 0 or height <= 0 or len(rows) != height or xoff < 0 or top < 0
            or xoff + width + 1 > 8 or top + height + 1 > 16):
        raise ValueError("glyph and shadow do not fit the 8x16 cell")
    if len({background, ink, shadow}) != 3:
        raise ValueError("background, ink, and shadow must be distinct")
    bits = ((width + 7) // 8) * 8
    if any(type(row) is not int or not 0 <= row < (1 << bits) or row & ((1 << (bits - width)) - 1) for row in rows):
        raise ValueError("invalid BDF bitmap row or nonzero padding")
    points = {(x + xoff, y + top) for y, row in enumerate(rows) for x in range(width)
              if row & (1 << (bits - 1 - x))}
    if not points:
        raise ValueError("empty required glyph")
    grid = [[background] * 8 for _ in range(16)]
    for x, y in points:
        grid[y + 1][x + 1] = shadow
    for x, y in points:
        grid[y][x] = ink
    result = pack_pixels(grid)
    if unpack_pixels(result) != grid:
        raise ValueError("fixed-cell pixel roundtrip failed")
    return result


def bdf_cells(path: Path, wanted: set[str], profile: dict) -> dict[str, bytes]:
    found = {}
    for block in path.read_text(encoding="utf-8").split("STARTCHAR ")[1:]:
        lines = block.splitlines()
        char = chr(int(next(line.split()[1] for line in lines if line.startswith("ENCODING "))))
        if char not in wanted:
            continue
        if char in found:
            raise ValueError("duplicate BDF encoding")
        width, height, xoff, yoff = map(int, next(line for line in lines if line.startswith("BBX ")).split()[1:])
        start = lines.index("BITMAP") + 1
        rows = [int(row, 16) for row in lines[start:start + height]]
        found[char] = rasterize(width, height, xoff, yoff, rows, **profile)
    if set(found) != wanted:
        raise ValueError(f"missing fixed-cell glyphs: {wanted - set(found)}")
    return found
