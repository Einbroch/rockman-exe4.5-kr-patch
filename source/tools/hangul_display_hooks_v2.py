"""Hangul record hooks v2: v1 copy signature + print expansion with tails/work buffers + input commit.

Print (site 0x080517F8, as v1) recognises three kinds of format-A sources:
  * copy buffers 0x020293E0..0x0202951F: signature [0x80, checksum] at src+size (written by the v1 copy hook);
  * 32-byte work buffers 0x0200FC80 (editor flat text, descriptor 0), 0x02014E54 (schedule, 67) and 0x02014E74
    (commit echo, 68): signature at src+30/31, strict body;
  * profile records 0x02000E51..0x020011E1 with marker 0x80 at src-1. Here the pair run may end at a byte >= 0x80
    that is not E5: the rest up to E5 is a native/F9FC tail copied verbatim. The nickname builder 0x08038F60
    copies the name record (marker included) to 0x02000E5E and appends the suffix (F9FC since batch 065) there.
Commit (site 0x08035000, whole function; only caller BL at 0x08034FA0): when the editor flat buffer 0x0200FC80
carries a signature, the destination record [state+0x1C] becomes 0x80 + body + E5 and the echo copy at 0x02014E74
gets a signature; otherwise the original marker-1 copy (stops at E5 or 98) runs and the echo signature is cleared.
"""
from extended_dialogue import assemble_verified
from korean_codec import HANGUL_COUNT
from hangul_record_v2 import MARKER
import hangul_display_hooks_v1 as V1

PRINT_SITE, PRINT_SOURCE_HEX, PRINT_RET = V1.PRINT_SITE, V1.PRINT_SOURCE_HEX, V1.PRINT_RET
COPY_SITE = V1.COPY_SITE
COMMIT_SITE, COMMIT_SOURCE_HEX = 0x35000, '10b5ea4b40215a18db690120'
STATE, FLAT, ECHO, SCHEDULE = 0x0200FC40, 0x0200FC80, 0x02014E74, 0x02014E54
WORK_SIG = 30                      # signature offset inside a 32-byte work buffer
WORK_LIMIT = 28                    # last allowed E5 index in a work buffer body
checksum, VALUE_LIMIT = V1.checksum, V1.VALUE_LIMIT
INVERT = dict(beq='bne', bne='beq', bhi='bls', bls='bhi', bhs='blo', blo='bhs', bgt='ble', ble='bgt', bge='blt', blt='bge')


def far(code, labels):
    """Conditional branches to the given (distant) labels become `inverse skip / b label` (Thumb-1 b reaches 2 KiB);
    keystone otherwise silently emits a Thumb-2 .w branch with a wrong fixup."""
    out = [];n = 0
    for line in code.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0] in INVERT and parts[1] in labels:
            n += 1;out += [f'{INVERT[parts[0]]} far{n}', f'b {parts[1]}', f'far{n}:']
        else:out.append(line)
    return '\n'.join(out)


def validate(tag, fail, tail=False):
    """r4=src, r6=lim. Success: r7 = end of pairs (E5, or tail start when tail=True), r3 = checksum."""
    stop = f'''cmp r0,#0x7F
bhi {fail}''' if not tail else f'''cmp r0,#0x7F
bhi {tag}end'''
    return f'''movs r7,#0
movs r3,#0
{tag}loop:
ldrb r0,[r4,r7]
cmp r0,#0xE5
beq {tag}end
adds r1,r7,#2
cmp r1,r6
bhi {fail}
{stop}
adds r1,r7,#1
ldrb r1,[r4,r1]
cmp r1,#0x7F
bhi {fail}
adds r3,r3,r0
adds r3,r3,r1
lsls r0,r0,#7
orrs r0,r1
ldr r1,vmax
cmp r0,r1
bhs {fail}
adds r7,#2
b {tag}loop
{tag}end:
cmp r7,#0
beq {fail}
movs r0,#0xFF
ands r3,r0
movs r0,#{V1.SIG_XOR}
eors r3,r0'''


def build_print(address):
    code = f'''pop {{r3}}
lsls r3,r3,#7
ldr r1,printbuf
adds r1,r1,r3
push {{r1}}
push {{r4,r5,r6,r7}}
adds r4,r0,#0
adds r5,r1,#0
subs r6,r2,#1
ldr r3,buflo
cmp r4,r3
blo pwork
ldr r3,bufhi
cmp r4,r3
bhs pwork
adds r2,r6,#1
ldrb r0,[r4,r2]
cmp r0,#{MARKER}
bne pnative
{validate('bv', 'pnative')}
adds r2,r6,#2
ldrb r0,[r4,r2]
cmp r0,r3
bne pnative
b pdecode
pwork:
ldr r3,flat
cmp r4,r3
beq pworkok
ldr r3,echo
cmp r4,r3
beq pworkok
ldr r3,schedule
cmp r4,r3
bne precord
pworkok:
movs r2,#{WORK_SIG}
ldrb r0,[r4,r2]
cmp r0,#{MARKER}
bne pnative
movs r6,#{WORK_LIMIT}
{validate('wv', 'pnative2')}
movs r2,#{WORK_SIG + 1}
ldrb r0,[r4,r2]
cmp r0,r3
bne pnative2
b pdecode
pnative2:
movs r6,#31
b pnative
precord:
ldr r3,reclo
cmp r4,r3
blo pnative
ldr r3,rechi
cmp r4,r3
bhs pnative
subs r0,r4,#1
ldrb r0,[r0]
cmp r0,#{MARKER}
bne pnative
{validate('rv', 'pnative', tail=True)}
adds r2,r7,#0
ptail:
cmp r2,r6
bhi pnative
ldrb r0,[r4,r2]
adds r2,#1
cmp r0,#0xE5
bne ptail
pdecode:
movs r6,#0
dloop:
cmp r6,r7
beq dtail
ldrb r0,[r4,r6]
adds r6,#1
ldrb r1,[r4,r6]
adds r6,#1
lsls r0,r0,#7
orrs r0,r1
ldr r1,hcount
cmp r0,r1
bhs dnative
movs r2,#0xF9
strb r2,[r5]
movs r2,#0xFC
strb r2,[r5,#1]
strb r0,[r5,#2]
lsrs r0,r0,#8
strb r0,[r5,#3]
adds r5,#4
b dloop
dnative:
subs r0,r0,r1
strb r0,[r5]
adds r5,#1
b dloop
dtail:
ldrb r0,[r4,r6]
strb r0,[r5]
adds r6,#1
adds r5,#1
cmp r0,#0xE5
bne dtail
b pdone
pnative:
adds r0,r4,#0
adds r1,r5,#0
adds r2,r6,#1
ldr r3,memcpy
mov lr,pc
bx r3
pdone:
pop {{r4,r5,r6,r7}}
ldr r3,ret
bx r3'''
    code = far(code, {'pnative', 'pnative2', 'pwork', 'pworkok', 'precord', 'pdecode', 'dtail'})
    return assemble_verified(code, address, dict(printbuf=V1.PRINT_BUF, buflo=V1.BUF_LO, bufhi=V1.BUF_HI, vmax=VALUE_LIMIT,
                                                flat=FLAT, echo=ECHO, schedule=SCHEDULE, reclo=V1.REC_LO, rechi=V1.REC_HI,
                                                hcount=HANGUL_COUNT, memcpy=V1.MEMCPY | 1, ret=PRINT_RET | 1))


def build_commit(address):
    code = f'''pop {{r3}}
push {{r4,r5,r6,r7,lr}}
ldr r4,state
ldr r5,[r4,#0x1C]
adds r4,#0x40
movs r2,#{WORK_SIG}
ldrb r0,[r4,r2]
cmp r0,#{MARKER}
bne knative
movs r6,#{WORK_LIMIT}
{validate('kv', 'knative')}
movs r2,#{WORK_SIG + 1}
ldrb r0,[r4,r2]
cmp r0,r3
bne knative
movs r0,#{MARKER}
strb r0,[r5]
movs r2,#0
kcopy:
ldrb r0,[r4,r2]
adds r1,r2,#1
strb r0,[r5,r1]
adds r2,#1
cmp r0,#0xE5
bne kcopy
adds r6,r3,#0
adds r0,r5,#1
ldr r1,echo
ldr r3,copyfn
mov lr,pc
bx r3
ldr r1,echo
movs r2,#{WORK_SIG}
movs r0,#{MARKER}
strb r0,[r1,r2]
adds r2,#1
strb r6,[r1,r2]
b kdone
knative:
movs r0,#1
strb r0,[r5]
movs r2,#0
nloop:
ldrb r0,[r4,r2]
cmp r0,#0xE5
beq nend
cmp r0,#0x98
beq nend
adds r1,r2,#1
strb r0,[r5,r1]
adds r2,#1
b nloop
nend:
adds r1,r2,#1
movs r0,#0xE5
strb r0,[r5,r1]
adds r0,r5,#1
ldr r1,echo
ldr r3,copyfn
mov lr,pc
bx r3
ldr r1,echo
movs r2,#{WORK_SIG}
movs r0,#0
strb r0,[r1,r2]
kdone:
pop {{r4,r5,r6,r7}}
pop {{r3}}
bx r3'''
    code = far(code, {'knative', 'kdone'})
    return assemble_verified(code, address, dict(state=STATE, vmax=VALUE_LIMIT, echo=ECHO, copyfn=V1.COPY_FN | 1))


def build_copy(address):
    return V1.build_copy(address)


def patches(source, copy_at, print_at, commit_at):
    out = V1.patches(source, copy_at, print_at)
    if source[COMMIT_SITE:COMMIT_SITE + 12].hex() != COMMIT_SOURCE_HEX:raise ValueError('commit site drift')
    out.append((COMMIT_SITE, V1.stub(0x08000000 + commit_at), 'Hangul record commit hook'))
    return out
