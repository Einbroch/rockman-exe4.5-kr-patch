"""Internal mixed-cell identity candidate, NOT font/save/ROM ABI.

Hangul ranks0..11171 and partial initials11172..11190 stay unchanged.
Opaque native singles00..E3 use8000..80E3; E4 xx use8100..81FF.
Structural identity only: accepting a byte does not prove glyph validity or
safe native commit (native writer scans98/E5 even inside E4 sequences).
"""


def tag(token):
    if type(token) != bytes:
        raise ValueError('native token type')
    if len(token) == 1 and token[0] <= 0xE3:
        return 0x8000 + token[0]
    if len(token) == 2 and token[0] == 0xE4:
        return 0x8100 + token[1]
    raise ValueError('native token shape/control')


def untag(word):
    if type(word) != int:
        raise ValueError('native tag type')
    if 0x8000 <= word <= 0x80E3:
        return bytes([word - 0x8000])
    if 0x8100 <= word <= 0x81FF:
        return bytes([0xE4, word - 0x8100])
    raise ValueError('not an opaque native cell')


def from_native_word(word):
    if type(word) != int or not 0 <= word <= 0xFFFF:
        raise ValueError('native word width')
    if word & 0xFF == 0xE4:
        return tag(word.to_bytes(2, 'little'))
    if word <= 0xE3:
        return tag(bytes([word]))
    raise ValueError('noncanonical native word')


def to_native_word(word):
    return int.from_bytes(untag(word), 'little')


def verify_contract():
    tokens = [bytes([v]) for v in range(0xE4)] + [bytes([0xE4, v]) for v in range(256)]
    tags = {tag(t) for t in tokens}
    if len(tags) != 484 or tags & set(range(11191)):
        raise ValueError('mixed-cell identity collision')
    for t in tokens:
        w = tag(t)
        if untag(w) != t or from_native_word(to_native_word(w)) != w:
            raise ValueError('opaque identity roundtrip')
    for w in range(65536):
        try:
            raw = untag(w)
        except ValueError:
            if w in tags:
                raise
        else:
            if w not in tags or tag(raw) != w:
                raise ValueError('tag domain leakage')
    for raw in (b'', b'\xE4', b'\xE5', b'\xF9', b'\x00\x00', b'\xE4\x00\x00'):
        try:
            tag(raw)
        except ValueError:
            continue
        raise ValueError('invalid native token accepted')
    return dict(structural_tokens=484, full_uint16_tag_domain=65536, hangul_rank_collisions=0)
