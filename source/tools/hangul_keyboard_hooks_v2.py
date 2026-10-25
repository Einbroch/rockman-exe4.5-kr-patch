"""Hooks v2: v1 (frozen with stage 068) + the fixed-cell parser's buffer-print copy.

The IWRAM fixed-cell parser (ROM image 0x1EF900 -> 0x03006A00 at boot) has its own F9 0C handler at 0x03006A1C:
descriptor table 0x080526D0, slot 0x020155F0 + n*128, and `ldr r3,=0x0800094D / mov lr,pc / bx r3` with the only
memcpy literal of the image at ROM 0x1EF96C. The keyboard input box (descriptor 0) and the profile confirmation
screen (descriptor 31) print through it, so format-A bytes showed as kana. 'fcopy' keeps memcpy's contract
(r0 src, r1 dst, r2 size; r4..r7 preserved; returns with `mov pc` because lr has no Thumb bit) and expands the
same sources as the v1 print hook; everything else is the native copy. The literal now points at fcopy.
"""
import inspect
from extended_dialogue import assemble_verified
import hangul_keyboard_hooks_v1 as V1
import hangul_record_v3 as R
from hangul_display_hooks_v2 import far

FCOPY_LITERAL, FCOPY_LITERAL_HEX = 0x1EF96C, '4d090008'


def _print_body():
    src = inspect.getsource(V1.build_print)
    return 'ldr r3,buflo' + src.split('ldr r3,buflo', 1)[1].split('pdone:', 1)[0]


def build_fcopy(address):
    body = _print_body().replace('{validate(', '{V1.validate(').replace('{R.MARKER}', str(R.MARKER)).replace('{WORK_SIG}', str(V1.WORK_SIG)) \
        .replace('{WORK_SIG + 1}', str(V1.WORK_SIG + 1)).replace('{WORK_LIMIT}', str(V1.WORK_LIMIT))
    body = eval('f' + repr(body), dict(V1=V1))
    code = f'''push {{r4,r5,r6,r7,lr}}
adds r4,r0,#0
adds r5,r1,#0
subs r6,r2,#1
{body}pdone:
pop {{r4,r5,r6,r7}}
pop {{r3}}
mov pc,r3'''
    code = far(code, {'pnative', 'pnative2', 'pwork', 'pworkok', 'precord', 'pdecode', 'ptailchk', 'dtail', 'pdone', 'dloop', 'dhangul', 'djamo', 'dwide'})
    return assemble_verified(code, address, dict(buflo=V1.BUF_LO, bufhi=V1.BUF_HI, vend=R.VALUE_END, jlo=R.JAMO_BASE + 1, jhi=R.WIDE_BASE, wbase=R.WIDE_BASE,
                                                flat=V1.FLAT, echo=V1.ECHO, schedule=V1.SCHEDULE, reclo=V1.REC_LO, rechi=V1.REC_HI, hcount=R.NATIVE_BASE,
                                                jbase=R.JAMO_BASE, jglyph=R.JAMO_GLYPH, memcpy=V1.MEMCPY | 1))


def patches(source, fcopy_at):
    if source[FCOPY_LITERAL:FCOPY_LITERAL + 4].hex() != FCOPY_LITERAL_HEX:raise ValueError('fixed-cell memcpy literal drift')
    return [(FCOPY_LITERAL, (0x08000000 + fcopy_at | 1).to_bytes(4, 'little'), 'fixed-cell buffer print copy -> fcopy')]
