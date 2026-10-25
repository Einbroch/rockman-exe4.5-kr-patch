"""Caller-selected import -> baseline24 candidate. NOT adopted save/game ABI.

Experimental record width2*cap+2; marker80|count, complete LE ranks, FFFF
padding, E5. Cap1..10. Import decision is explicit, never inferred from0.
r0 record, r1 cap | (import_selected <<8), r2 output, r3 output bytes>=24.
Return1 baseline24,2 legacy route without writes,0 atomic reject. All pointer
extents caller-owned; byte alignment permitted. Legacy0/1 are NOT validated
or decoded here; caller must preserve and handle their original text.
"""
import struct
from hangul_baseline_bridge import CODE as OLD_CODE
from hangul_extended_composer_thumb import replace_once


def check_limit(cap):
    if type(cap) != int or not 1 <= cap <= 10:
        raise ValueError('ten-cell candidate capacity')


def pack(text, cap):
    check_limit(cap)
    if type(text) != str or not 1 <= len(text) <= cap or any(not 0xAC00 <= ord(c) <= 0xD7A3 for c in text):
        raise ValueError('complete nonempty Hangul only')
    return bytes([0x80 | len(text)]) + b''.join((ord(c) - 0xAC00).to_bytes(2, 'little') for c in text) + b'\xFF\xFF' * (cap - len(text)) + b'\xE5'


def unpack(record, cap):
    check_limit(cap)
    if type(record) != bytes or len(record) != 2 * cap + 2:
        raise ValueError('candidate extent')
    count = record[0] - 0x80
    if not 1 <= count <= cap or record[-1] != 0xE5:
        raise ValueError('candidate header/terminator')
    words = struct.unpack_from('<' + 'H' * cap, record, 1)
    if any(w >= 11172 for w in words[:count]) or any(w != 0xFFFF for w in words[count:]):
        raise ValueError('candidate ranks/padding')
    return ''.join(chr(0xAC00 + w) for w in words[:count])


def baseline(record, cap, import_selected):
    check_limit(cap)
    if type(import_selected) != bool or type(record) != bytes or len(record) != 2 * cap + 2:
        raise ValueError('baseline request')
    if not import_selected:
        text = ''
    elif record[0] in (0, 1):
        return 2, None
    else:
        text = unpack(record, cap)
    words = [ord(c) - 0xAC00 for c in text] + [0xFFFF] * (10 - len(text))
    return 1, bytes([len(text), cap, 0, int(bool(text))]) + struct.pack('<10H', *words)


CODE = replace_once(OLD_CODE, 'movs r6, r1', '''movs r6, r1
lsrs r0, r1, #9
cmp r0, #0
bne reject
lsrs r7, r1, #8
movs r0, #255
ands r6, r0''')
CODE = replace_once(CODE, 'cmp r6, #8', 'cmp r6, #10')
CODE = replace_once(CODE, 'cmp r3, #20', 'cmp r3, #24')
CODE = replace_once(CODE, 'adds r0, #20', 'adds r0, #24')
CODE = replace_once(CODE, '''disjoint:
ldrb r7, [r4]
cmp r7, #1
beq legacy
cmp r7, #0
beq emit_header''', '''disjoint:
cmp r7, #0
beq no_import
ldrb r7, [r4]
cmp r7, #1
bls legacy''')
CODE = replace_once(CODE, 'emit_header:\n', 'no_import:\nmovs r7, #0\nemit_header:\n')
CODE = replace_once(CODE, 'cmp r3, #8', 'cmp r3, #10')
