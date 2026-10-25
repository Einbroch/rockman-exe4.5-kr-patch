"""24-byte reconstructed surface -> at most41 display bytes, not ROM ABI.

Surface is count/cap/history/active + ten LE uint16 ranks, already validated
by full keylog replay. History is bounded structurally, not checked here.
r0 surface24, r1 output, r2 available bytes, r3 edit0/commit1.
Return byte count including E5 or0 atomic reject. Byte-aligned regions OK.
"""
import struct
from hangul_editor_display import CODE as OLD_CODE, JAMO_INDICES, JAMO_BASE
from hangul_extended_composer_thumb import replace_once
from korean_codec import PREFIX, HANGUL_COUNT
from hangul_composer_thumb import KEYS, EMPTY


def display(raw, mode=0):
    if len(raw) != 24 or mode not in (0, 1):
        raise ValueError('surface ABI')
    count, cap, depth, active = raw[:4]
    if not 1 <= cap <= 10 or count > cap or depth > 70 or active > 1:
        raise ValueError('surface header')
    if count == 0 and (active or depth or mode):
        raise ValueError('empty state')
    indices = []
    for i, rank in enumerate(struct.unpack_from('<10H', raw, 4)):
        if i >= count:
            if rank != EMPTY:
                raise ValueError('unused rank')
        elif rank < HANGUL_COUNT:
            indices.append(rank)
        elif rank < HANGUL_COUNT + 19 and i == count - 1 and active and not mode:
            indices.append(JAMO_INDICES[KEYS[rank - HANGUL_COUNT]])
        else:
            raise ValueError('partial/invalid rank')
    return b''.join(PREFIX + i.to_bytes(2, 'little') for i in indices) + b'\xE5'


CODE = replace_once(OLD_CODE, 'cmp r0, #8', 'cmp r0, #10')
start = CODE.index('movs r0, r4\nadds r0, #62')
end = CODE.index('movs r0, r7', start)
CODE = CODE[:start] + CODE[end:]
CODE = replace_once(CODE, 'cmp r1, #56', 'cmp r1, #70')
CODE = replace_once(CODE, 'adds r1, #64', 'adds r1, #24')
CODE = replace_once(CODE, 'cmp r3, #8', 'cmp r3, #10')
