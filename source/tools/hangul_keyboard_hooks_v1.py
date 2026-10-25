"""Korean keyboard + format-A (hangul_record_v3) hooks for the native editor; supersedes hangul_display_hooks_v1/v2.

Sites (each a 12-byte push{r3}/ldr r3/bx r3 stub at a 4-aligned address; the hook pops r3 first):
  copy    0x08038BF8  record selector copy: native E5 copy, then signature [0x80, checksum] at dst+size (v1 rule)
  print   0x080517F8  F9 0C handler: format A -> F9FC/native bytes into the 128-byte print slot (v2 sources, v3 values;
                      work buffers may hold editor jamo and a 98 tail; profile records may carry a native/F9FC tail)
  commit  0x08035000  whole function (only caller BL 0x08034FA0): signed flat -> 0x80 record (jamo dropped; no
                      syllable left -> native marker-1 bytes); unsigned -> original behaviour; echo 0x02014E74 signed
  flatten 0x0803562C  whole leaf (callers 0x08034E4C per frame and others): Hangul words -> pairs + 98 tail + E5 +
                      signature at +30/31; otherwise the original copy and the signature byte cleared
  keys    0x080353B0  A/B handler (only caller BL 0x08034F08): page 0 grid A -> jamo composer on the word before
                      the cursor; B on a Hangul word -> one canonical jamo removal; everything else falls through to
                      the original body at 0x080353BC with the original prologue replayed
Values are hangul_record_v3 stored values (value + 1, 7+7 bits). Composer rules: hangul_editor_v1.
"""
from extended_dialogue import assemble_verified
import hangul_record_v3 as R
import hangul_editor_v1 as E
from hangul_display_hooks_v2 import far, INVERT

STATE, FLAT, ECHO, SCHEDULE = 0x0200FC40, 0x0200FC80, 0x02014E74, 0x02014E54
TABLE, COPY_FN, MEMCPY, PRINT_BUF, SOUND = 0x080526D0, 0x08032AC6, 0x0800094C, 0x02010AC0, 0x08000534
BUF_LO, BUF_HI, REC_LO, REC_HI = 0x020293E0, 0x02029520, 0x02000E51, 0x020011E2
SIG_XOR, WORK_SIG, WORK_LIMIT = 0xA5, 30, 28
SITES = dict(copy=(0x38BF8, '7178c9007a4a5158f9f761ff'), print=(0x517F8, 'db013f49c91802b4aff7a4f8'),
             commit=(0x35000, '10b5ea4b40215a18db690120'), flatten=(0x3562C, '474b4022d2181b6918781070'),
             keys=(0x353B0, '10b5e64c53465b685b880220'))
COPY_RET, PRINT_RET, KEYS_BODY = 0x08038C04, 0x08051804, 0x080353BC
SND_TYPE, SND_DELETE = 0x7E, 0x7F


def checksum(body):return (sum(body) & 0xFF) ^ SIG_XOR


def stub(target):return bytes.fromhex('08b4014b1847c046') + (target | 1).to_bytes(4, 'little')


def validate(tag, fail, limit_label, tail=False):
    """r4=src, r6=lim. Pairs of 7-bit bytes with 1 <= stored <= [limit_label]. Success: r7 = end of pairs
    (E5, or first byte >= 0x80 when tail=True), r3 = checksum. Clobbers r0..r3."""
    stop = f'cmp r0,#0x7F\nbhi {tag}end' if tail else f'cmp r0,#0x7F\nbhi {fail}'
    # records never hold lone jamo (stored 11401..11440); editor/flat buffers may (limit_label 'emax')
    jamo_check = f'ldr r1,jlo\ncmp r0,r1\nblo {tag}ok\nldr r1,jhi\ncmp r0,r1\nbls {fail}\n{tag}ok:\n' if limit_label == 'rmax' else ''
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
beq {fail}
ldr r1,vend
cmp r0,r1
bhi {fail}
{jamo_check}adds r7,#2
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
cmp r0,#{R.MARKER}
bne cnone
{validate('cv', 'cnone', 'rmax')}
adds r2,r6,#1
movs r0,#{R.MARKER}
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
    code = far(code, {'cnone', 'cdone'})
    return assemble_verified(code, address, dict(table=TABLE, copyfn=COPY_FN | 1, vend=R.VALUE_END, jlo=R.JAMO_BASE + 1, jhi=R.WIDE_BASE, ret=COPY_RET | 1))


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
cmp r0,#{R.MARKER}
bne pnative
{validate('bv', 'pnative', 'rmax')}
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
cmp r0,#{R.MARKER}
bne pnative
movs r6,#{WORK_LIMIT}
{validate('wv', 'pnative2', 'emax', tail=True)}
movs r2,#{WORK_SIG + 1}
ldrb r0,[r4,r2]
cmp r0,r3
bne pnative2
b ptailchk
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
cmp r0,#{R.MARKER}
bne pnative
{validate('rv', 'pnative', 'rmax', tail=True)}
ptailchk:
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
subs r0,#1
ldr r1,hcount
cmp r0,r1
blo dhangul
ldr r1,wbase
cmp r0,r1
bhs dwide
ldr r1,jbase
cmp r0,r1
bhs djamo
ldr r1,hcount
subs r0,r0,r1
strb r0,[r5]
adds r5,#1
b dloop
dwide:
subs r0,r0,r1
movs r1,#0xE4
strb r1,[r5]
strb r0,[r5,#1]
adds r5,#2
b dloop
djamo:
subs r0,r0,r1
ldr r1,jglyph
adds r0,r0,r1
dhangul:
movs r2,#0xF9
strb r2,[r5]
movs r2,#0xFC
strb r2,[r5,#1]
strb r0,[r5,#2]
lsrs r0,r0,#8
strb r0,[r5,#3]
adds r5,#4
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
    code = far(code, {'pnative', 'pnative2', 'pwork', 'pworkok', 'precord', 'pdecode', 'ptailchk', 'dtail', 'pdone', 'dloop', 'dhangul', 'djamo', 'dwide'})
    return assemble_verified(code, address, dict(printbuf=PRINT_BUF, buflo=BUF_LO, bufhi=BUF_HI, vend=R.VALUE_END, jlo=R.JAMO_BASE + 1, jhi=R.WIDE_BASE, wbase=R.WIDE_BASE,
                                                flat=FLAT, echo=ECHO, schedule=SCHEDULE, reclo=REC_LO, rechi=REC_HI, hcount=R.NATIVE_BASE,
                                                jbase=R.JAMO_BASE, jglyph=R.JAMO_GLYPH, memcpy=MEMCPY | 1, ret=PRINT_RET | 1))


def build_commit(address):
    """r4 = flat, r5 = destination record. Hangul path: count syllables; none -> native bytes."""
    code = f'''pop {{r3}}
push {{r4,r5,r6,r7,lr}}
ldr r4,state
ldr r5,[r4,#0x1C]
adds r4,#0x40
movs r2,#{WORK_SIG}
ldrb r0,[r4,r2]
cmp r0,#{R.MARKER}
bne knative
movs r6,#{WORK_LIMIT}
{validate('kv', 'knative', 'emax', tail=True)}
movs r2,#{WORK_SIG + 1}
ldrb r0,[r4,r2]
cmp r0,r3
bne knative
movs r2,#0
movs r3,#0
kcount:
cmp r2,r7
beq kcounted
ldrb r0,[r4,r2]
adds r2,#1
ldrb r1,[r4,r2]
adds r2,#1
lsls r0,r0,#7
orrs r0,r1
ldr r1,hcount
cmp r0,r1
bhi kcount
adds r3,#1
b kcount
kcounted:
movs r6,#1
cmp r3,#0
beq kmark
movs r6,#{R.MARKER}
kmark:
strb r6,[r5]
movs r2,#0
movs r3,#1
kloop:
cmp r2,r7
beq kend
ldrb r0,[r4,r2]
adds r2,#1
ldrb r1,[r4,r2]
adds r2,#1
push {{r0,r1}}
lsls r0,r0,#7
orrs r0,r1
subs r0,#1
ldr r1,jbase
cmp r0,r1
blo kkeep
ldr r1,wbase
cmp r0,r1
blo kskip
kkeep:
cmp r6,#{R.MARKER}
beq kpair
ldr r1,wbase
cmp r0,r1
bhs knwide
ldr r1,hcount
subs r0,r0,r1
strb r0,[r5,r3]
adds r3,#1
b kskip
knwide:
subs r0,r0,r1
movs r1,#0xE4
strb r1,[r5,r3]
adds r3,#1
strb r0,[r5,r3]
adds r3,#1
b kskip
kpair:
pop {{r0,r1}}
strb r0,[r5,r3]
adds r3,#1
strb r1,[r5,r3]
adds r3,#1
b kloop
kskip:
pop {{r0,r1}}
b kloop
kend:
movs r0,#0xE5
strb r0,[r5,r3]
adds r0,r5,#1
ldr r1,echo
ldr r3,copyfn
mov lr,pc
bx r3
ldr r1,echo
movs r2,#{WORK_SIG}
movs r0,#0
cmp r6,#{R.MARKER}
bne kecho
adds r0,r5,#1
movs r3,#0
movs r2,#0
ksum:
ldrb r7,[r0,r2]
cmp r7,#0xE5
beq ksumd
adds r3,r3,r7
adds r2,#1
b ksum
ksumd:
movs r0,#0xFF
ands r3,r0
movs r0,#{SIG_XOR}
eors r3,r0
movs r2,#{WORK_SIG + 1}
strb r3,[r1,r2]
subs r2,#1
movs r0,#{R.MARKER}
kecho:
strb r0,[r1,r2]
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
    code = far(code, {'knative', 'kdone', 'kcount', 'kloop', 'kcounted', 'kend', 'kecho', 'kpair', 'kmark', 'kkeep', 'kskip', 'knwide'})
    return assemble_verified(code, address, dict(state=STATE, vend=R.VALUE_END, hcount=R.NATIVE_BASE, jbase=R.JAMO_BASE, wbase=R.WIDE_BASE,
                                                echo=ECHO, copyfn=COPY_FN | 1))


def build_flatten(address):
    """Replaces leaf 0x0803562C (no stack use by callers' contract: r0..r3 scratch, returns via lr)."""
    code = f'''pop {{r3}}
push {{r4,r5,r6,lr}}
ldr r4,state
adds r5,r4,#0
adds r5,#0x40
ldr r4,[r4,#0x10]
movs r2,#0
fscan:
ldrh r0,[r4,r2]
movs r1,#0xFF
ands r1,r0
cmp r1,#0xE5
beq fnative
adds r2,#2
lsrs r3,r0,#15
beq fscan
cmp r1,#0x7F
bhi fscan
movs r2,#0
movs r3,#0
movs r6,#0
fhloop:
ldrh r0,[r4,r2]
adds r2,#2
movs r1,#0xFF
ands r1,r0
cmp r1,#0xE5
beq fhend
lsrs r0,r0,#8
cmp r1,#0xE4
beq fwide
lsrs r3,r0,#7
beq fnoth
cmp r1,#0x7F
bls fhword
b fblank
fnoth:
cmp r0,#0
bne fblank
cmp r1,#0x98
beq fblank
cmp r1,#0xE4
bhs fblank
ldr r0,nbase1
adds r0,r0,r1
b fsplit
fwide:
ldr r1,wbase1
adds r0,r0,r1
fsplit:
lsrs r1,r0,#7
movs r3,#0x7F
ands r0,r3
b fpair
fhword:
movs r3,#0x7F
ands r0,r3
fpair:
strb r1,[r5,r6]
adds r6,#1
strb r0,[r5,r6]
adds r6,#1
b fhloop
fblank:
movs r0,#0x98
strb r0,[r5,r6]
adds r6,#1
b fhloop
fhend:
strb r1,[r5,r6]
movs r2,#0
movs r3,#0
fsum:
ldrb r0,[r5,r2]
cmp r0,#0x7F
bhi fsumd
adds r3,r3,r0
adds r2,#1
b fsum
fsumd:
movs r0,#0xFF
ands r3,r0
movs r0,#{SIG_XOR}
eors r3,r0
movs r2,#{WORK_SIG + 1}
strb r3,[r5,r2]
subs r2,#1
movs r0,#{R.MARKER}
strb r0,[r5,r2]
b fdone
fnative:
movs r2,#0
fnloop:
ldrb r0,[r4]
strb r0,[r5,r2]
cmp r0,#0xE5
beq fnend
cmp r0,#0xE4
bne fnnext
ldrb r0,[r4,#1]
adds r2,#1
strb r0,[r5,r2]
fnnext:
adds r4,#2
adds r2,#1
b fnloop
fnend:
movs r2,#{WORK_SIG}
movs r0,#0
strb r0,[r5,r2]
fdone:
pop {{r4,r5,r6}}
pop {{r3}}
bx r3'''
    code = far(code, {'fnative', 'fdone', 'fscan', 'fhloop', 'fhend', 'fhword', 'fpair', 'fblank', 'fsum', 'fsumd', 'fnloop', 'fnnext', 'fnend', 'fwide', 'fnoth', 'fsplit'})
    return assemble_verified(code, address, dict(state=STATE, nbase1=R.NATIVE_BASE + 1, wbase1=R.WIDE_BASE + 1))


def build_keys(address, tables_at):
    """A/B handler. r4 = editor state, r5 = cursor, r6 = prev initial, r7 = key/jamo. Helpers are called with
    `mov lr,pc / b helper` and return with `mov pc,lr` (Thumb state kept, r0 untouched by the call itself).
    prev: r0 = 1 found (r6 = l, r1 = v or 0xFF for a lone initial, r2 = t), 0 none.
    value: r0 = l, r1 = v, r2 = t -> r0 = editor word for the syllable. put: r0 = word -> written at the cursor."""
    T = layout_tables();lit = {k: tables_at + v for k, v in T.items() if k != 'blob'}
    call = lambda f: f'mov lr,pc\nb {f}'
    code = f'''pop {{r3}}
push {{r4,r5,r6,r7,lr}}
ldr r4,state
mov r3,sl
ldr r3,[r3,#4]
ldrh r3,[r3,#2]
ldr r5,[r4,#0x14]
movs r0,#2
tst r3,r0
bne kb
movs r0,#1
tst r3,r0
beq knat
ldrb r0,[r4,#8]
cmp r0,#0
bne knat
ldrb r0,[r4,#6]
cmp r0,#15
bhs knat
b ka
knat:
pop {{r4,r5,r6,r7}}
pop {{r3}}
mov lr,r3
push {{r4,lr}}
ldr r4,state
mov r3,sl
ldr r3,[r3,#4]
ldrh r3,[r3,#2]
movs r0,#2
ldr r1,body
bx r1
kb:
{call('prev')}
cmp r0,#0
beq knat
cmp r1,#0xFF
beq kblone
cmp r2,#0
beq kbv
ldr r3,t_split
lsls r0,r2,#1
ldrb r2,[r3,r0]
b kbsyll
kbv:
ldr r3,t_mprev
ldrb r0,[r3,r1]
cmp r0,#0xFF
beq kbtolone
adds r1,r0,#0
movs r2,#0
kbsyll:
adds r0,r6,#0
{call('value')}
b kbstore
kbtolone:
adds r0,r6,#0
b kbjamo
kblone:
ldr r3,t_iprev
ldrb r0,[r3,r6]
cmp r0,#0xFF
beq kbdel
kbjamo:
ldr r1,jbase
adds r0,r0,r1
{call('word')}
kbstore:
subs r1,r5,#2
strh r0,[r1]
b kbsnd
kbdel:
ldr r1,[r4,#0x18]
adds r2,r5,#0
subs r3,r5,#2
str r3,[r4,#0x14]
kbmove:
cmp r2,r1
beq kbmoved
ldrh r0,[r2]
strh r0,[r3]
adds r2,#2
adds r3,#2
b kbmove
kbmoved:
str r3,[r4,#0x18]
kbsnd:
movs r0,#{SND_DELETE}
b ksound
ka:
ldrb r1,[r4,#7]
movs r2,#15
muls r1,r2,r1
ldrb r2,[r4,#6]
adds r1,r1,r2
cmp r1,#90
bhs kdone
ldr r3,t_sel
ldrb r7,[r3,r1]
cmp r7,#0xFF
beq kdone
{call('prev')}
cmp r7,#19
bhs kamedial
cmp r0,#0
beq kanew
cmp r1,#0xFF
bne kasyll
cmp r6,r7
bne kdone
ldr r3,t_tense
ldrb r0,[r3,r6]
cmp r0,#0xFF
beq kdone
b kajamo
kasyll:
cmp r2,#0
bne kafinal
ldr r3,t_fin
ldrb r2,[r3,r7]
cmp r2,#0xFF
beq kanew
b kaset
kafinal:
movs r0,#19
muls r0,r2,r0
adds r0,r0,r7
ldr r3,t_fmerge
ldrb r0,[r3,r0]
cmp r0,#0xFF
beq kanew
adds r2,r0,#0
kaset:
adds r0,r6,#0
{call('value')}
subs r1,r5,#2
strh r0,[r1]
b katyped
kanew:
{call('full')}
bne kdone
adds r0,r7,#0
kajamonew:
ldr r1,jbase
adds r0,r0,r1
{call('word')}
{call('put')}
b katyped
kajamo:
ldr r1,jbase
adds r0,r0,r1
{call('word')}
subs r1,r5,#2
strh r0,[r1]
b katyped
kamedial:
subs r7,#19
cmp r0,#0
beq kdone
cmp r1,#0xFF
beq kalone
cmp r2,#0
bne kasplit
movs r0,#21
muls r0,r1,r0
adds r0,r0,r7
ldr r3,t_mmerge
ldrb r1,[r3,r0]
cmp r1,#0xFF
beq kdone
movs r2,#0
b kaset
kalone:
adds r1,r7,#0
movs r2,#0
b kaset
kasplit:
{call('full')}
bne kdone
ldr r3,t_split
lsls r2,r2,#1
adds r3,r3,r2
ldrb r2,[r3]
ldrb r0,[r3,#1]
push {{r0}}
adds r0,r6,#0
{call('value')}
subs r1,r5,#2
strh r0,[r1]
pop {{r0}}
adds r1,r7,#0
movs r2,#0
{call('value')}
{call('put')}
katyped:
movs r0,#{SND_TYPE}
ksound:
ldr r3,sound
mov r1,pc
adds r1,#5
mov lr,r1
bx r3
kdone:
pop {{r4,r5,r6,r7}}
pop {{r3}}
movs r0,#1
bx r3
prev:
ldr r3,[r4,#0x10]
cmp r5,r3
beq pnone
subs r3,r5,#2
ldrh r0,[r3]
lsrs r1,r0,#15
beq pnone
movs r1,#0xFF
ands r1,r0
cmp r1,#0x7F
bhi pnone
lsls r1,r1,#7
lsrs r0,r0,#8
movs r2,#0x7F
ands r0,r2
orrs r0,r1
subs r0,#1
ldr r1,hcount
cmp r0,r1
blo psyll
ldr r1,jbase
subs r0,r0,r1
blo pnone
cmp r0,#19
bhs pnone
adds r6,r0,#0
movs r1,#0xFF
movs r2,#0
movs r0,#1
mov pc,lr
psyll:
movs r6,#0
ldr r1,n588
pl:
cmp r0,r1
blo pv
subs r0,r0,r1
adds r6,#1
b pl
pv:
movs r1,#0
pvl:
cmp r0,#28
blo pt
subs r0,#28
adds r1,#1
b pvl
pt:
adds r2,r0,#0
movs r0,#1
mov pc,lr
pnone:
movs r0,#0
mov pc,lr
value:
movs r3,#21
muls r0,r3,r0
adds r0,r0,r1
movs r3,#28
muls r0,r3,r0
adds r0,r0,r2
word:
adds r0,#1
movs r3,#0x7F
ands r3,r0
movs r1,#0x80
orrs r3,r1
lsls r3,r3,#8
lsrs r0,r0,#7
orrs r0,r3
mov pc,lr
full:
ldr r0,[r4,#0x18]
ldr r3,[r4,#0x10]
subs r0,r0,r3
lsrs r0,r0,#1
ldrb r3,[r4,#4]
cmp r0,r3
bhs ffull
movs r0,#0
cmp r0,#0
mov pc,lr
ffull:
movs r0,#1
cmp r0,#0
mov pc,lr
put:
ldr r3,[r4,#0x18]
cmp r5,r3
bne pw
adds r3,#2
str r3,[r4,#0x18]
pw:
strh r0,[r5]
adds r5,#2
str r5,[r4,#0x14]
mov pc,lr'''
    code = far(code, {'kb', 'knat', 'ka', 'kdone', 'katyped', 'kanew', 'kaset', 'kamedial', 'kasplit', 'kalone', 'kajamo', 'kbdel', 'kbsnd',
                      'kblone', 'kbv', 'kbsyll', 'kbtolone', 'kbjamo', 'kbstore', 'kbmove', 'kbmoved', 'ksound', 'kasyll', 'kafinal'})
    lits = dict(state=STATE, body=KEYS_BODY | 1, jbase=R.JAMO_BASE, sound=SOUND | 1, hcount=R.NATIVE_BASE, n588=588,
                t_sel=lit['selectors'], t_fin=lit['fin_of_cons'], t_fmerge=lit['final_merge'], t_split=lit['split'],
                t_mmerge=lit['medial_merge'], t_mprev=lit['medial_prev'], t_tense=lit['tense'], t_iprev=lit['initial_prev'])
    return assemble_verified(code, address, lits)


def layout_tables():
    t = E.tables();order = ['selectors', 'fin_of_cons', 'final_merge', 'split', 'medial_merge', 'medial_prev', 'tense', 'initial_prev']
    out = {};at = 0;blob = bytearray()
    for k in order:out[k] = at;blob += t[k];at = len(blob)
    out['blob'] = bytes(blob)
    return out


def build_all(base_offset):
    """Blobs laid out from ROM file offset base_offset: tables, then the five hooks. Returns (blob, entries)."""
    T = layout_tables();blob = bytearray(T['blob']);entries = {'tables': base_offset}
    def place(name, builder):
        blob.extend(b'\xff' * (-len(blob) % 4));at = base_offset + len(blob)
        code, _ = builder(0x08000000 + at);blob.extend(code);entries[name] = at
    place('copy', build_copy);place('print', build_print);place('commit', build_commit);place('flatten', build_flatten)
    place('keys', lambda a: build_keys(a, 0x08000000 + base_offset))
    return bytes(blob), entries


def patches(source, entries):
    out = []
    for name, (site, hexs) in SITES.items():
        if source[site:site + 12].hex() != hexs:raise ValueError('hook site drift %s %X' % (name, site))
        out.append((site, stub(0x08000000 + entries[name]), 'Hangul keyboard hook: ' + name))
    return out
