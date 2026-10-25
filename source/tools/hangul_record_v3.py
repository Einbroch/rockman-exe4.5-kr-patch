"""Hangul input format A, v3 (supersedes hangul_record_v2 before any ROM install).

Change from v2: a slot stores value+1, so no character is ever the pair 00 00. The native empty-input check
(0x08035038 family) skips 0x00 bytes, which made a lone '가' (value 0) look like an empty answer.

value: syllable rank 0..11171 | 11172 + native single-byte code (0x00..0xE3) | 11400 + jamo index (editor only:
ㄱ..ㅎ 0..18, ㅏ..ㅣ 19..39, the 065 keyboard glyph order) | 11440 + xx for the native two-byte character E4 xx
(keyboard page 2 symbols). stored = value + 1 split into (hi7, lo7).
Record (field limit N, 2N+2 bytes): 0x80 | pairs | E5 | 00 padding; jamo never appear in a committed record.
Editor cell word (0x0200FC60.., 16-bit): ((0x80 | lo7) << 8) | hi7. Native words have a zero high byte or low
byte E4, so the two never coincide.
Display: syllable -> F9 FC LE16(rank); native -> its byte; jamo j -> F9 FC LE16(11174 + j); wide -> E4 xx.
Tokens: syllable/jamo str, native int 0..0xE3, wide int 0xE400 | xx.
"""
from korean_codec import HANGUL_BASE, HANGUL_COUNT, PREFIX

MARKER = 0x80
TERMINATOR = 0xE5
BLANK = 0x98
NATIVE_BASE, NATIVE_LIMIT = HANGUL_COUNT, 0xE4
JAMO_BASE = NATIVE_BASE + NATIVE_LIMIT            # 11400
JAMO = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
JAMO_GLYPH = 11174                                # F9FC index of 'ㄱ' in the supplied keyboard glyphs
WIDE_BASE = JAMO_BASE + len(JAMO)                 # 11440
VALUE_END = WIDE_BASE + 256                       # 11696; editor/flat buffers accept every value below
RECORD_LIMIT = JAMO_BASE                          # records: below this, or WIDE_BASE..VALUE_END-1
EDITOR_LIMIT = VALUE_END


def value_of(token):
    if isinstance(token, str):
        if len(token) == 1 and 0 <= ord(token) - HANGUL_BASE < HANGUL_COUNT:return ord(token) - HANGUL_BASE
        if token in JAMO:return JAMO_BASE + JAMO.index(token)
        raise ValueError('not a syllable/jamo: %r' % token)
    if token >> 8 == 0xE4:return WIDE_BASE + (token & 0xFF)
    if not 0 <= token < NATIVE_LIMIT:raise ValueError('not a native single-byte character: %r' % token)
    return NATIVE_BASE + token


def token_of(value):
    if 0 <= value < HANGUL_COUNT:return chr(HANGUL_BASE + value)
    if value < JAMO_BASE:return value - NATIVE_BASE
    if value < WIDE_BASE:return JAMO[value - JAMO_BASE]
    if value < VALUE_END:return 0xE400 | (value - WIDE_BASE)
    raise ValueError('value out of range: %d' % value)


def pair(value):
    s = value + 1;return bytes([s >> 7, s & 0x7F])


def unpair(hi, lo):
    if hi >= 0x80 or lo >= 0x80:raise ValueError('not a 7-bit pair')
    return (hi << 7 | lo) - 1


def word(value):
    s = value + 1;return ((0x80 | (s & 0x7F)) << 8) | (s >> 7)


def unword(w):
    if not (w >> 15) or (w & 0xFF) >= 0x80:raise ValueError('not a Hangul editor word')
    return ((w & 0x7F) << 7 | (w >> 8 & 0x7F)) - 1


def is_syllable(t):return isinstance(t, str) and len(t) == 1 and 0 <= ord(t) - HANGUL_BASE < HANGUL_COUNT


def encode(tokens, limit):
    tokens = list(tokens)
    if not 1 <= len(tokens) <= limit:raise ValueError('length %d outside 1..%d' % (len(tokens), limit))
    if not any(is_syllable(t) for t in tokens) or any(isinstance(t, str) and not is_syllable(t) for t in tokens):raise ValueError('record needs syllables and no jamo')
    out = bytearray([MARKER])
    for t in tokens:out += pair(value_of(t))
    out.append(TERMINATOR)
    return bytes(out.ljust(2 * limit + 2, b'\0'))


def decode(record, limit):
    if len(record) != 2 * limit + 2 or record[0] != MARKER:raise ValueError('not a Hangul record of this size')
    tokens = [];i = 1
    while record[i] != TERMINATOR:
        if i + 2 > 2 * limit + 1:raise ValueError('no terminator')
        v = unpair(record[i], record[i + 1])
        if not (0 <= v < RECORD_LIMIT or WIDE_BASE <= v < VALUE_END):raise ValueError('value out of record range')
        tokens.append(token_of(v));i += 2
    if not tokens or any(record[i + 1:]) or not any(is_syllable(t) for t in tokens):raise ValueError('bad terminator/padding')
    return tokens


def display_tokens(tokens):
    out = bytearray()
    for t in tokens:
        if is_syllable(t):out += PREFIX + (ord(t) - HANGUL_BASE).to_bytes(2, 'little')
        elif isinstance(t, str):out += PREFIX + (JAMO_GLYPH + JAMO.index(t)).to_bytes(2, 'little')
        elif t >> 8 == 0xE4:out += bytes([0xE4, t & 0xFF])
        else:out.append(t)
    return bytes(out)


def display(record, limit):
    return display_tokens(decode(record, limit)) + bytes([TERMINATOR])
