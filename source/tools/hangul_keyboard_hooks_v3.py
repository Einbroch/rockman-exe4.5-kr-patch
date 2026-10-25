"""Hooks v3: confirm guard in front of the v1 A/B handler (user decision 2026-10-25: block confirming a lone jamo).

The 0x080353B0 stub now enters 'guard'. When B is not pressed, A or Start is pressed, the cursor is on the confirm
cell (column 15, row 5) and any editor word is a lone jamo (stored value 11401..11440), the press is consumed with
the error sound and r0 = 1 (Z = 0, the native 'handled' result); nothing else changes. Otherwise it jumps to the v1
keys entry with the stub's pushed r3 still on the stack, so v1/native behaviour is untouched.
"""
from extended_dialogue import assemble_verified
import hangul_record_v3 as R
from hangul_display_hooks_v2 import far

STATE, SOUND, SND_REFUSE = 0x0200FC40, 0x08000534, 0x69
CONFIRM_COL, CONFIRM_ROW = 15, 5


def build_guard(address, keys_v1):
    code = f'''mov r2,sl
ldr r2,[r2,#4]
ldrh r2,[r2,#2]
movs r1,#2
tst r2,r1
bne gpass
movs r1,#9
tst r2,r1
beq gpass
ldr r0,state
ldrb r1,[r0,#6]
cmp r1,#{CONFIRM_COL}
bne gpass
ldrb r1,[r0,#7]
cmp r1,#{CONFIRM_ROW}
bne gpass
ldr r1,[r0,#0x10]
ldr r2,[r0,#0x18]
gloop:
cmp r1,r2
beq gpass
ldrh r3,[r1]
adds r1,#2
lsrs r0,r3,#15
beq gloop
movs r0,#0xFF
ands r0,r3
cmp r0,#0x7F
bhi gloop
lsls r0,r0,#7
lsrs r3,r3,#8
push {{r1}}
movs r1,#0x7F
ands r3,r1
pop {{r1}}
orrs r0,r3
ldr r3,jlo
cmp r0,r3
blo gloop
ldr r3,jhi
cmp r0,r3
bhi gloop
push {{lr}}
movs r0,#{SND_REFUSE}
ldr r3,sound
mov r1,pc
adds r1,#5
mov lr,r1
bx r3
pop {{r3}}
mov lr,r3
pop {{r3}}
movs r0,#1
bx lr
gpass:
ldr r0,keys
bx r0'''
    code = far(code, {'gpass', 'gloop'})
    return assemble_verified(code, address, dict(state=STATE, jlo=R.JAMO_BASE + 1, jhi=R.WIDE_BASE, sound=SOUND | 1, keys=keys_v1 | 1))
