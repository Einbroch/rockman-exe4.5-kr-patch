"""Exhaustive host checks for hangul_record_v3."""
import hangul_record_v3 as R
from korean_codec import HANGUL_BASE, HANGUL_COUNT, decode_character

FORBIDDEN = {R.BLANK, R.TERMINATOR} | set(range(0xE4, 0x100))


def main():
    n = 0
    for v in range(R.EDITOR_LIMIT):                           # every value: pair/word round trip, no 00 00, no forbidden byte
        t = R.token_of(v);p = R.pair(v)
        assert R.value_of(t) == v and R.unpair(*p) == v and p != b'\0\0' and not FORBIDDEN & set(p)
        w = R.word(v);assert R.unword(w) == v and w >> 15 and (w & 0xFF) < 0x80 and (w & 0xFF) != 0xE4;n += 1
    for native in range(0x100):                                 # native words are never Hangul words
        for hi in range(0x100):
            w = hi << 8 | native
            if native != 0xE4 and hi:continue
            try:R.unword(w)
            except ValueError:n += 1
            else:raise AssertionError(hex(w))
    for limit in (4, 6, 8, 10):
        for r in range(HANGUL_COUNT):
            s = chr(HANGUL_BASE + r)
            for toks in ([s], ['가'] * (limit - 1) + [s]):
                rec = R.encode(toks, limit);assert R.decode(rec, limit) == toks
                d = R.display(rec, limit);i = 0;out = []
                while d[i] != R.TERMINATOR:
                    if d[i:i + 2] == b'\xF9\xFC':ch, i = decode_character(d, i);out.append(ch)
                    else:out.append(d[i]);i += 1
                assert out == toks;n += 1
        rec = R.encode(['가', 0xE457, 0x41], limit);assert R.decode(rec, limit) == ['가', 0xE457, 0x41] and R.display(rec, limit)[4:6] == bytes([0xE4, 0x57]);n += 1
        for bad in (['ㄱ'], ['가', 'ㄱ'], [0x10], []):
            try:R.encode(bad, limit)
            except ValueError:n += 1
            else:raise AssertionError(bad)
    assert R.display_tokens(['ㄱ', 'ㅣ']) == b'\xF9\xFC' + (11174).to_bytes(2, 'little') + b'\xF9\xFC' + (11213).to_bytes(2, 'little')
    print('통과 %d건' % n)


if __name__ == '__main__':main()
