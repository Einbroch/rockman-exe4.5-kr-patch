"""BIOS SWI 11h type-10 literal-only writer, not a general compressor.

GBATEK BIOS decompression: 24-bit byte count, MSB-first flags, 4-byte
source alignment and zero padding. Source streams remain independently
decoded by verify_tpi_index; this decoder accepts only our literal variant.
"""


def encode(payload: bytes, *, limit: int) -> bytes:
    if not 0 < len(payload) <= min(limit, 0xFFFFFF):
        raise ValueError("LZ10 output size outside declared buffer")
    out = bytearray(b"\x10" + len(payload).to_bytes(3, "little"))
    for at in range(0, len(payload), 8):
        out.append(0)
        out.extend(payload[at:at + 8])
    out.extend(b"\0" * (-len(out) % 4))
    return bytes(out)


def decode(blob: bytes, *, limit: int) -> bytes:
    if len(blob) < 4 or blob[0] != 0x10 or len(blob) % 4:
        raise ValueError("invalid padded LZ10 literal stream")
    size = int.from_bytes(blob[1:4], "little")
    if not 0 < size <= min(limit, 0xFFFFFF):
        raise ValueError("LZ10 output size outside declared buffer")
    out, at = bytearray(), 4
    while len(out) < size:
        if at >= len(blob) or blob[at] != 0:
            raise ValueError("truncated or non-literal LZ10 flag")
        count = min(8, size - len(out))
        at += 1
        if at + count > len(blob):
            raise ValueError("truncated LZ10 literal block")
        out.extend(blob[at:at + count])
        at += count
    if len(blob) != ((at + 3) & ~3) or any(blob[at:]):
        raise ValueError("invalid LZ10 alignment padding")
    return bytes(out)
