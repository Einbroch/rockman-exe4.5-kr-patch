"""Mixed current24 -> display bytes only; NOT save serialization.

count/cap/cursor/activeFF +10 LE words, no old depth/boolean flag interpretation.
Complete Hangul uses F9FC/rank; unfinished initials use declared jamo mapping
(index11172 remains comma). Native tags roundtrip their original token bytes.
Edit0 preserves partials anywhere; candidate1 rejects all partials and empty.
Structural native tags are not glyph/input eligibility proof; embedded98/E5
in E4 payload remains intact, but old byte-scanning save writer is unsafe.
Native r0surface24/r1dest/r2available/r3mode, return length including E5 or0.
Byte alignment allowed, r4..r11/SP preserved, stack36; caller owns extents and
stack disjointness. No game hooks/cache changes or committed record ABI.
"""
import struct
from hangul_mixed_editor import MixedEditor, Snapshot
from hangul_native_tokens import untag
from hangul_editor_display import JAMO_INDICES,JAMO_BASE
from hangul_composer_thumb import KEYS

if any(JAMO_INDICES[k] != JAMO_BASE + i for i, k in enumerate(KEYS[:19])):
    raise ValueError('jamo glyph identity drift')


def display(raw, mode=0):
    if type(raw) != bytes or len(raw) != 24 or type(mode) != int or mode not in (0, 1):
        raise ValueError('mixed display surface/mode')
    count, cap, cursor, active = raw[:4]
    if count > 10: raise ValueError('mixed display count')
    words = struct.unpack_from('<10H', raw, 4)
    if any(w != 65535 for w in words[count:]): raise ValueError('mixed display padding')
    m = MixedEditor(cap); m.state = Snapshot(tuple(words[:count]), cursor, None if active == 255 else active)
    m._validate(m.state)
    if mode: m.candidate()
    out = bytearray()
    for word in m.state.cells:
        if word < 11172:
            out.extend(b'\xF9\xFC' + word.to_bytes(2, 'little'))
        elif word < 11191:
            out.extend(b'\xF9\xFC' + (word + JAMO_BASE - 11172).to_bytes(2, 'little'))
        else:
            out.extend(untag(word))
    return bytes(out) + b'\xE5'


CODE = '''push {r4, r5, r6, r7, lr}
sub sp, #16
movs r4, r0
movs r5, r1
str r2, [sp]
str r3, [sp, #4]
cmp r3, #1
bhi reject
adds r0, #24
cmp r0, r4
blo reject
ldrb r0, [r4]
str r0, [sp, #12]
ldrb r1, [r4, #1]
cmp r1, #1
blo reject
cmp r1, #10
bhi reject
cmp r0, r1
bhi reject
ldrb r1, [r4, #2]
cmp r1, r0
bhi reject
ldrb r2, [r4, #3]
cmp r2, #255
beq active_ok
cmp r2, r0
bhs reject
adds r2, #1
cmp r2, r1
bne reject
active_ok:
cmp r0, #0
bne count_ok
cmp r3, #0
bne reject
count_ok:
movs r6, #1
movs r7, #0
validate_loop:
lsls r1, r7, #1
adds r1, #4
ldrb r0, [r4, r1]
adds r1, #1
ldrb r2, [r4, r1]
lsls r2, r2, #8
orrs r0, r2
ldr r1, [sp, #12]
cmp r7, r1
bhs empty_word
movs r1, #43
lsls r1, r1, #8
adds r1, #164
cmp r0, r1
blo four_bytes
adds r1, #19
cmp r0, r1
bhs native_word
ldr r1, [sp, #4]
cmp r1, #0
bne reject
b four_bytes
native_word:
ldrb r1, [r4, #3]
cmp r1, r7
beq reject
lsrs r1, r0, #8
cmp r1, #129
beq two_bytes
cmp r1, #128
bne reject
movs r1, #255
ands r0, r1
cmp r0, #227
bhi reject
adds r6, #1
b validated_word
two_bytes:
adds r6, #2
b validated_word
four_bytes:
adds r6, #4
b validated_word
empty_word:
adds r0, #1
lsls r0, r0, #16
cmp r0, #0
bne reject
validated_word:
adds r7, #1
cmp r7, #10
blo validate_loop
b size_check
reject:
movs r0, #0
add sp, #16
pop {r4, r5, r6, r7, pc}
size_check:
ldr r0, [sp]
cmp r0, r6
blo reject
adds r0, r5, r6
cmp r0, r5
blo reject
movs r1, r4
adds r1, #24
cmp r4, r0
bhs disjoint
cmp r5, r1
blo reject
disjoint:
movs r7, #0
movs r3, r5
emit_loop:
ldr r0, [sp, #12]
cmp r7, r0
bhs terminate
lsls r1, r7, #1
adds r1, #4
ldrb r0, [r4, r1]
adds r1, #1
ldrb r2, [r4, r1]
lsls r2, r2, #8
orrs r0, r2
movs r1, #43
lsls r1, r1, #8
adds r1, #164
cmp r0, r1
blo emit_hangul
adds r1, #19
cmp r0, r1
bhs emit_native
adds r0, #JAMO_OFFSET
emit_hangul:
movs r1, #249
strb r1, [r3]
movs r1, #252
strb r1, [r3, #1]
strb r0, [r3, #2]
lsrs r0, r0, #8
strb r0, [r3, #3]
adds r3, #4
b emitted
emit_native:
lsrs r1, r0, #8
cmp r1, #129
bne emit_single
movs r1, #228
strb r1, [r3]
adds r3, #1
emit_single:
strb r0, [r3]
adds r3, #1
emitted:
adds r7, #1
b emit_loop
terminate:
movs r0, #229
strb r0, [r3]
movs r0, r6
add sp, #16
pop {r4, r5, r6, r7, pc}
'''
if CODE.count('JAMO_OFFSET')!=1:raise ValueError('mixed jamo mapping anchor')
CODE=CODE.replace('JAMO_OFFSET',str(JAMO_BASE-11172))
