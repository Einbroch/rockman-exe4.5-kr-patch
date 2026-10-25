"""Display hooks for Hangul input records (format A, hangul_record_v2): copy-signature + print expansion.

Copy site 0x08038BF8 (record selector 0x08038B94): the 12 bytes `ldrb r1,[r6,#1] / lsls / ldr r2,=0x080526D0 /
ldr r1,[r2,r1] / bl 0x08032AC6` become a push{r3}/ldr/bx stub. The hook replays the descriptor lookup, runs the
native E5-terminated copy (format-A bodies contain no E5, so the copy is exact), then writes a two-byte
signature [0x80, checksum] right after the descriptor's declared size when the source record's marker is 0x80 and
its body validates; otherwise it clears that signature byte. Copy buffers are 0x020293E0 + 0x20*k (10 slots,
sizes 13/17), so the signature stays inside the slot. Other code reuses this area, hence the checksum.

Print site 0x080517F8 (F9 0C handler 0x080517D0): `lsls r3,#7 / ldr r1,=0x02010AC0 / adds / push {r1} /
bl 0x0800094C` becomes a stub. The hook rebuilds the 128-byte print slot address and either expands a valid
Hangul record into F9 FC + LE16 escapes (4N+1 <= 33 bytes) or runs the native size-byte copy. A source is a
Hangul record when it is a copy buffer carrying a matching signature, or lies in the profile record block
0x02000E51..0x020011E1 with marker byte 0x80 just before it. Any validation failure falls back to the native copy.
Callee-saved r4..r7 are restored; the stubs' pushed r3 is popped on entry.
"""
from extended_dialogue import assemble_verified
from korean_codec import HANGUL_COUNT
from hangul_record_v2 import MARKER, NATIVE_LIMIT

COPY_SITE, COPY_SOURCE_HEX, COPY_RET = 0x38BF8, '7178c9007a4a5158f9f761ff', 0x08038C04
PRINT_SITE, PRINT_SOURCE_HEX, PRINT_RET = 0x517F8, 'db013f49c91802b4aff7a4f8', 0x08051804
TABLE, COPY_FN, MEMCPY, PRINT_BUF = 0x080526D0, 0x08032AC6, 0x0800094C, 0x02010AC0
BUF_LO, BUF_HI, REC_LO, REC_HI = 0x020293E0, 0x02029520, 0x02000E51, 0x020011E2
VALUE_LIMIT = HANGUL_COUNT + NATIVE_LIMIT
SIG_XOR = 0xA5


def checksum(body):
    return (sum(body) & 0xFF) ^ SIG_XOR


def stub(target):
    return bytes.fromhex('08b4014b1847c046') + (target | 1).to_bytes(4, 'little')


def validate(tag, fail):
    """r4=src, r6=lim (2N). Success: r7 = E5 index (>0, even), r3 = checksum. Clobbers r0..r3."""
    return f'''movs r7,#0
movs r3,#0
{tag}loop:
ldrb r0,[r4,r7]
cmp r0,#0xE5
beq {tag}end
adds r1,r7,#2
cmp r1,r6
bhi {fail}
cmp r0,#0x7F
bhi {fail}
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
movs r0,#{SIG_XOR}
eors r3,r0'''


def build_copy(address):
    code = f'''pop {{r3}}
push {{r4,r5,r6,r7}}
ldrb r1,[r6,#1]
lsls r1,r1,#3
ldr r2,table
adds r2,r2,r1
ldr r1,[r2]
ldr r2,[r2,#4]
adds r4,r0,#0
adds r5,r1,#0
subs r6,r2,#1
ldr r3,copyfn
mov lr,pc
bx r3
subs r0,r4,#1
ldrb r0,[r0]
cmp r0,#{MARKER}
bne cnone
{validate('cv', 'cnone')}
adds r2,r6,#1
movs r0,#{MARKER}
strb r0,[r5,r2]
adds r2,#1
strb r3,[r5,r2]
b cdone
cnone:
adds r2,r6,#1
movs r0,#0
strb r0,[r5,r2]
cdone:
pop {{r4,r5,r6,r7}}
ldr r3,ret
bx r3'''
    return assemble_verified(code, address, dict(table=TABLE, copyfn=COPY_FN | 1, vmax=VALUE_LIMIT, ret=COPY_RET | 1))


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
blo precord
ldr r3,bufhi
cmp r4,r3
bhs precord
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
{validate('rv', 'pnative')}
pdecode:
movs r6,#0
dloop:
cmp r6,r7
beq dend
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
dend:
movs r0,#0xE5
strb r0,[r5]
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
    return assemble_verified(code, address, dict(printbuf=PRINT_BUF, buflo=BUF_LO, bufhi=BUF_HI, vmax=VALUE_LIMIT,
                                                reclo=REC_LO, rechi=REC_HI, hcount=HANGUL_COUNT, memcpy=MEMCPY | 1,
                                                ret=PRINT_RET | 1))


def patches(source, copy_at, print_at):
    """[(offset, final_bytes, reason)] for the two stub sites, checked against the original instructions."""
    out = []
    for site, hexs, target, why in ((COPY_SITE, COPY_SOURCE_HEX, copy_at, 'Hangul record copy signature hook'),
                                    (PRINT_SITE, PRINT_SOURCE_HEX, print_at, 'Hangul record print expansion hook')):
        if source[site:site + 12].hex() != hexs:raise ValueError('hook site drift %X' % site)
        out.append((site, stub(0x08000000 + target), why))
    return out
