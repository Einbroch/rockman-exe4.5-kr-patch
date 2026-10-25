"""Validated compact76 -> logical caret/count query, CPU candidate only.

r0 compact, r1 original selector20(caret)/24(count), r2 available0..65535,
r3 pinned transition table. Returns r0 value/r1=1; reject r0=r1=0.
Does not expose legacy pointers or compute pixel advances. Full replay is
required: compact header contains baseline count/caret, not current values.
Byte alignment allowed, r4..r11/SP preserved, own32+nested68=100 stack.
Read-only input; only stack output. No adopted game RAM/hook/IRQ budget.
Caller owns source extent, pinned table and disjoint function stack.
This is a new query ABI, not original pointer_count register live-out ABI.
"""
from hangul_mixed_replay_thumb import CODE as REPLAY
from hangul_mixed_keyedit_thumb import assemble as assemble_code
from hangul_mixed_replay_state import MixedReplay


def count(raw, selector):
    if type(selector)!=int or selector not in (20,24):raise ValueError('count selector')
    state=MixedReplay.restore(raw).model.state
    return state.cursor if selector==20 else len(state.cells)


CODE='''push {r4, lr}
sub sp, #24
movs r4, r1
cmp r4, #20
beq query_extent
cmp r4, #24
bne query_fail
query_extent:
lsrs r1, r2, #16
bne query_fail
movs r1, #24
lsls r1, r1, #16
orrs r2, r1
mov r1, sp
bl query_decode
cmp r0, #0
beq query_fail
mov r1, sp
cmp r4, #20
bne query_count
ldrb r0, [r1, #2]
b query_success
query_count:
ldrb r0, [r1]
query_success:
movs r1, #1
b query_return
query_fail:
movs r0, #0
movs r1, #0
query_return:
add sp, #24
pop {r4, pc}
query_decode:
'''+REPLAY


def assemble(address=0x08802000):
    return assemble_code(address,CODE)
