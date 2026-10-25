"""Descriptor0/slot0 copy-call ABI candidate; NOT an installed ROM hook.

Entry r0=0200FC80,r1=020155F0,r2=32,LR=03006A4C selects compact76
at old source-44. All other calls tail-enter unchanged original0800094C.
Requires caller-selected new editor layout; no automatic format detection.
New route requires caller-owned41-byte cache and immutable table09000000.
Cache failure explicitly emits emptyE5; old copy live-outs and NZCV retained.
Own20+cache112=132 stack, plus original provider44=176 fixture depth.
"""
from hangul_mixed_cache_bridge import CODE as CACHE, scoped
from hangul_mixed_keyedit_thumb import assemble as assemble_code


CODE='''push {r4}
movs r3, #2
lsls r3, r3, #24
movs r4, #252
lsls r4, r4, #8
adds r3, r3, r4
adds r3, #128
cmp r0, r3
bne shim_legacy
cmp r2, #32
bne shim_legacy
movs r3, #2
lsls r3, r3, #24
movs r4, #1
lsls r4, r4, #16
adds r3, r3, r4
movs r4, #85
lsls r4, r4, #8
adds r3, r3, r4
adds r3, #240
cmp r1, r3
bne shim_legacy
movs r3, #3
lsls r3, r3, #24
movs r4, #106
lsls r4, r4, #8
adds r3, r3, r4
adds r3, #76
cmp lr, r3
bne shim_legacy
push {r0, r1, r5, lr}
movs r5, r1
subs r0, #44
movs r2, #41
lsls r2, r2, #16
adds r2, #76
movs r3, #9
lsls r3, r3, #24
bl shim_cache
cmp r0, #0
bne shim_finish
movs r0, #229
strb r0, [r5]
shim_finish:
pop {r0, r1, r5}
pop {r2}
mov lr, r2
pop {r4}
ldrb r3, [r0]
movs r2, #1
subs r2, #1
mov pc, lr
shim_legacy:
movs r3, #8
lsls r3, r3, #24
movs r4, #9
lsls r4, r4, #8
adds r3, r3, r4
adds r3, #77
pop {r4}
bx r3
shim_cache:
'''+scoped(CACHE,'ks_')


def assemble(address=0x08F03000):
    return assemble_code(address,CODE)
