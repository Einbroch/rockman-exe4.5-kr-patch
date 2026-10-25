"""Adopted Hangul input record format (user decision 2026-10-25, 'A안').

A native input field with logical limit N occupies 2N+2 bytes: marker, body, E5. Native records use marker 1 and
one byte per kana (E4-prefixed two-byte characters also exist). A Hangul record uses:

    MARKER (0x80) | N slots of two 7-bit bytes (hi, lo) | E5 | 00 padding to 2N+2

value = syllable rank (0..11171, ch - U+AC00) or HANGUL_COUNT + native single-byte code (0x00..0xE3) for the
keyboard's Latin/digit/symbol/space characters. Both bytes are < 0x80, so a slot never contains E5 (terminator),
98 (input blank) or any E4..FF control; an unhooked native reader shows kana noise instead of stopping early.
A record is Hangul only if it holds at least one syllable; otherwise the native form is written.
The original reader loop treats any non-zero marker as a used record (record_markers.json).

Display expansion: syllable -> F9 FC + LE16 rank (korean_codec), native value -> its single byte; then E5.
"""
from korean_codec import HANGUL_BASE, HANGUL_COUNT, PREFIX

MARKER = 0x80
NATIVE_MARKER = 0x01
TERMINATOR = 0xE5
NATIVE_LIMIT = 0xE4          # single-byte native characters 0x00..0xE3


def value_of(token):
    """token: one Hangul syllable (str) or a native single-byte code (int)."""
    if isinstance(token, str):
        rank = ord(token) - HANGUL_BASE
        if len(token) != 1 or not 0 <= rank < HANGUL_COUNT:raise ValueError('not a Hangul syllable: %r' % token)
        return rank
    if not 0 <= token < NATIVE_LIMIT:raise ValueError('not a native single-byte character: %r' % token)
    return HANGUL_COUNT + token


def token_of(value):
    if value < HANGUL_COUNT:return chr(HANGUL_BASE + value)
    code = value - HANGUL_COUNT
    if not 0 <= code < NATIVE_LIMIT:raise ValueError('value out of range: %d' % value)
    return code


def encode(tokens, limit):
    """Hangul record bytes (length 2*limit+2) for 1..limit tokens containing at least one syllable."""
    tokens = list(tokens)
    if not 1 <= len(tokens) <= limit:raise ValueError('length %d outside 1..%d' % (len(tokens), limit))
    if not any(isinstance(t, str) for t in tokens):raise ValueError('no Hangul: use the native record form')
    out = bytearray([MARKER])
    for t in tokens:
        v = value_of(t);out += bytes([v >> 7, v & 0x7F])
    out.append(TERMINATOR)
    return bytes(out.ljust(2 * limit + 2, b'\0'))


def is_hangul_record(record):
    return len(record) >= 1 and record[0] == MARKER


def decode(record, limit):
    """Tokens of a Hangul record; strict: exact size, 7-bit slots, terminator, zero padding."""
    if len(record) != 2 * limit + 2 or record[0] != MARKER:raise ValueError('not a Hangul record of this size')
    tokens = [];i = 1
    while record[i] != TERMINATOR:
        if i + 2 > 2 * limit + 1 or record[i] >= 0x80 or record[i + 1] >= 0x80:raise ValueError('bad slot at %d' % i)
        tokens.append(token_of(record[i] << 7 | record[i + 1]));i += 2
    if not tokens or any(record[i + 1:]) or not any(isinstance(t, str) for t in tokens):raise ValueError('bad terminator/padding')
    return tokens


def display(record, limit):
    """Bytes the native printer understands: F9FC escapes / native bytes, then E5. At most 4*limit+1 bytes."""
    out = bytearray()
    for t in decode(record, limit):
        out += PREFIX + (ord(t) - HANGUL_BASE).to_bytes(2, 'little') if isinstance(t, str) else bytes([t])
    out.append(TERMINATOR)
    return bytes(out)
