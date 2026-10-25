"""Read-only compact76 -> bounded edit stream cache, CPU candidate only.

r0 compact76,r1 cache,r2 inputAvailable(low16)|cacheAvailable(high16),
r3 pinned transition table. Requires cacheAvailable>=41; returns byte length
includingE5 or0. r4..r11/SP preserved. Only successful cache bytes are written.
Own44+nested replay68=112 stack (display36 is sequential). Caller owns
source/cache/table extents, identities, disjoint stack and cache lifetime.
No original descriptor/copy ABI, RAM reservation, hook or queue lifetime adoption.
"""
import re, struct
from hangul_mixed_replay_thumb import CODE as REPLAY
from hangul_mixed_display import CODE as DISPLAY, display
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_keyedit_thumb import assemble as assemble_code


def stream(raw):
    c=MixedReplay.restore(raw);s=c.model.state
    surface=bytes([len(s.cells),c.model.capacity,s.cursor,255 if s.active is None else s.active])+struct.pack('<10H',*(s.cells+(65535,)*(10-len(s.cells))))
    return display(surface,0)


def scoped(code,prefix):
    labels=re.findall(r'^(\w+):',code,re.M)
    return re.sub(r'\b('+'|'.join(labels)+r')\b',lambda m:prefix+m.group(0),code)


CODE='''push {r4, r5, lr}
sub sp, #32
movs r4, r0
movs r5, r1
lsrs r0, r2, #16
cmp r0, #41
blo cache_fail
str r0, [sp, #24]
lsls r2, r2, #16
lsrs r2, r2, #16
cmp r2, #76
blo cache_fail
movs r0, r4
adds r0, #76
cmp r0, r4
blo cache_fail
movs r1, r5
adds r1, #41
cmp r1, r5
blo cache_fail
cmp r4, r1
bhs cache_disjoint
cmp r5, r0
blo cache_fail
cache_disjoint:
movs r1, #24
lsls r1, r1, #16
orrs r2, r1
movs r0, r4
mov r1, sp
bl cache_decode
cmp r0, #0
beq cache_fail
mov r0, sp
movs r1, r5
ldr r2, [sp, #24]
movs r3, #0
bl cache_display
b cache_return
cache_fail:
movs r0, #0
cache_return:
add sp, #32
pop {r4, r5, pc}
cache_decode:
'''+scoped(REPLAY,'cb_replay_')+'''cache_display:
'''+scoped(DISPLAY,'cb_display_')


def assemble(address=0x08F01000):
    return assemble_code(address,CODE)
