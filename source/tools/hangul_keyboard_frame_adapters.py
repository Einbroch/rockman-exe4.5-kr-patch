"""CPU-only glue for native frame/caret; no game placement adoption.

refresh veneer preserves LR for far ARMv4T call. Caret adapter consumes
native selector20 and editor96, queries compact state (108 nested stack).
Legacy pad/flatten have no valid role in new layout: shared no-op return.
"""
from extended_dialogue import assemble_verified


def assemble():
    veneer,vi=assemble_verified('ldr r3, target\nbx r3\n',0x08305000,dict(target=0x08F12001))
    noop,ni=assemble_verified('bx lr\n',0x08305100,{})
    caret,ci=assemble_verified('''push {r4, lr}
cmp r0, #20
bne caret_fail
ldr r1, editor
cmp r5, r1
bne caret_fail
movs r0, r5
adds r0, #20
movs r1, #20
movs r2, #76
ldr r3, table
ldr r4, query
mov lr, pc
bx r4
pop {r4, pc}
caret_fail:
movs r0, #0
movs r1, #0
pop {r4, pc}
''',0x08305200,dict(editor=0x0200FC40,table=0x09000000,query=0x08F11001))
    navigation,nav_isa=assemble_verified('''ldrb r1, [r5, #8]
cmp r1, #0
bne native_navigation
ldrb r1, [r5, #7]
cmp r1, #2
bne native_navigation
ldrb r1, [r5, #6]
cmp r1, #6
beq retain_jamo
cmp r1, #8
beq retain_jamo
native_navigation:
ldr r3, original
bx r3
retain_jamo:
bx lr
''',0x08305300,dict(original=0x08035087))
    return [(0x08305000,veneer,vi,'refresh_veneer.bin'),(0x08305100,noop,ni,'legacy_noop.bin'),(0x08305200,caret,ci,'caret.bin'),(0x08305300,navigation,nav_isa,'navigation.bin')]
