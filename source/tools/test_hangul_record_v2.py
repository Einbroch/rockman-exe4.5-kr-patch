"""Exhaustive host checks for hangul_record_v2 (record format 'A안')."""
import itertools
import hangul_record_v2 as R
from korean_codec import HANGUL_BASE, HANGUL_COUNT, decode_character

LIMITS = (4, 6, 8)
FORBIDDEN = {0x98, R.TERMINATOR} | set(range(0xE4, 0x100))


def check_record(rec, tokens, limit):
    assert len(rec) == 2 * limit + 2 and rec[0] == R.MARKER
    body = rec[1:1 + 2 * len(tokens)]
    assert not FORBIDDEN & set(body), rec.hex()
    assert R.decode(rec, limit) == list(tokens)
    disp = R.display(rec, limit);i = 0;out = []
    while disp[i] != R.TERMINATOR:
        if disp[i:i + 2] == b'\xF9\xFC':ch, i = decode_character(disp, i);out.append(ch)
        else:out.append(disp[i]);i += 1
    assert out == list(tokens) and i == len(disp) - 1 and len(disp) <= 4 * limit + 1


def main():
    n = 0
    syllables = [chr(HANGUL_BASE + r) for r in range(HANGUL_COUNT)]
    natives = list(range(R.NATIVE_LIMIT))
    for limit in LIMITS:
        for s in syllables:                       # every syllable alone and in the last slot of a full field
            check_record(R.encode([s], limit), [s], limit)
            full = ['가'] * (limit - 1) + [s];check_record(R.encode(full, limit), full, limit);n += 2
        for c in natives:                         # every native byte next to a syllable, both orders
            for t in (['한', c], [c, '한']):check_record(R.encode(t, limit), t, limit);n += 1
    # every 2-byte slot value round-trips; no value encodes a forbidden byte
    for v in range(HANGUL_COUNT + R.NATIVE_LIMIT):
        assert R.value_of(R.token_of(v)) == v and v >> 7 < 0x80;n += 1
    # rejections
    bad = 0
    for limit in LIMITS:
        for tokens in ([], [0x10], ['가'] * (limit + 1)):
            try:R.encode(tokens, limit)
            except ValueError:bad += 1
            else:raise AssertionError(tokens)
        good = R.encode(['가', '나'], limit)
        mutants = [b'\x01' + good[1:], good[:-1], good + b'\0', good[:5] + b'\x01' + good[6:],
                   good[:1] + b'\x80' + good[2:], good[:1] + bytes([R.TERMINATOR]) + good[2:]]
        mutants += [good[:1] + bytes([0x7F, 0x7F]) + good[3:]]             # value beyond the native range
        for m in mutants:
            try:R.decode(m, limit)
            except ValueError:bad += 1
            else:raise AssertionError(m.hex())
    print('통과: 왕복 %d건, 거부 %d건' % (n, bad))


if __name__ == '__main__':main()
