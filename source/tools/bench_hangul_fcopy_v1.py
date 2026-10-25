"""Differential CPU bench: hangul_keyboard_hooks_v2.fcopy vs the already-verified v1 print hook on the 068 ROM.

For each case the same source bytes are printed through the 068 print stub (0x080517F8 -> slot 0x02010AC0) and
copied by fcopy (called like the IWRAM parser: lr without the Thumb bit, return by mov pc); outputs must match
byte for byte, and r4..r7/sp must be preserved. Cases: format-A records with tails (nickname), copy buffers with
signatures, work buffers with jamo/98 tails, native strings, malformed data.
"""
import json,sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
import hangul_keyboard_hooks_v1 as V1
import hangul_keyboard_hooks_v2 as V2
import hangul_record_v3 as R
from korean_codec import HANGUL_BASE, HANGUL_COUNT

ROM, AT, SP0, RET = 'poc/output/pending500_068_v1.gba', 0x1FF0000, 0x03007E00, 0x03006A4C
SLOT, DST = 0x02010AC0, 0x020155F0


def main():
    base = (ROOT / ROM).read_bytes();rom = bytearray(base.ljust(0x02000000, b'\xff'))
    blob, _ = V2.build_fcopy(0x08000000 + AT);rom[AT:AT + len(blob)] = blob
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB);u.mem_map(0x08000000, 0x02000000);u.mem_write(0x08000000, bytes(rom))
    u.mem_map(0x02000000, 0x40000);u.mem_map(0x03000000, 0x8000);u.mem_map(0x04000000, 0x1000)
    u.mem_write(RET, b'\x00\xbf' * 4)
    rnd = random.Random(69);syll = [chr(HANGUL_BASE + i) for i in range(HANGUL_COUNT)];n = 0;kinds = {}
    def via_print(src, size):
        u.mem_write(SLOT, b'\x5a' * 128)
        for r, v in ((UC_ARM_REG_R0, src), (UC_ARM_REG_R2, size), (UC_ARM_REG_R3, 0)):u.reg_write(r, v)
        u.reg_write(UC_ARM_REG_SP, SP0);u.emu_start(0x080517F8 | 1, V1.PRINT_RET, count=100000)
        return bytes(u.mem_read(SLOT, 128))
    def via_fcopy(src, size):
        u.mem_write(DST, b'\x5a' * 128)
        for r, v in ((UC_ARM_REG_R0, src), (UC_ARM_REG_R1, DST), (UC_ARM_REG_R2, size), (UC_ARM_REG_R4, 0x44), (UC_ARM_REG_R5, 0x55), (UC_ARM_REG_R6, 0x66), (UC_ARM_REG_R7, 0x77), (UC_ARM_REG_LR, RET)):u.reg_write(r, v)
        u.reg_write(UC_ARM_REG_SP, SP0);u.emu_start(0x08000000 + AT | 1, RET, count=100000)
        if u.reg_read(UC_ARM_REG_PC) != RET or u.reg_read(UC_ARM_REG_SP) != SP0 or [u.reg_read(r) for r in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7)] != [0x44, 0x55, 0x66, 0x77]:raise AssertionError('fcopy contract')
        return bytes(u.mem_read(DST, 128))
    def case(kind, src, data, size):
        nonlocal n
        u.mem_write(src - 1, data);a = via_print(src, size);b = via_fcopy(src, size)
        if a != b:raise AssertionError('%s %s\n%s\n%s' % (kind, data.hex(), a.hex(), b.hex()))
        n += 1;kinds[kind] = kinds.get(kind, 0) + 1
    for t in range(20000):
        k = t % 6
        if k == 0:                                   # name record (descriptor 31) / nickname with F9FC tail
            toks = [rnd.choice(syll) for _ in range(rnd.randrange(1, 7))];rec = R.encode(toks, 6)
            if t % 12 == 0:rec = rec[:rec.index(0xE5, 1)] + b'\xf9\xfc\x70\x01\xe5';case('nickname', 0x02000E5F, rec + b'\0' * 8, 21)
            else:case('record', 0x02000E51, rec, 13)
        elif k == 1:                                 # copy buffer with signature
            toks = [rnd.choice(syll) for _ in range(rnd.randrange(1, 9))];rec = R.encode(toks, 8);body = rec[1:rec.index(0xE5, 1) + 1]
            case('copybuf', 0x02029480, b'\0' + body.ljust(17, b'\0') + bytes([0x80, V1.checksum(body[:-1])]), 17)
        elif k == 2:                                 # flat buffer: syllables + jamo + 98 tail + signature
            toks = [rnd.choice(syll + list(R.JAMO)) for _ in range(rnd.randrange(1, 9))];pairs = b''.join(R.pair(R.value_of(x)) for x in toks)
            flat = (pairs + b'\x98' * (10 - len(toks)) + b'\xe5').ljust(30, b'\0') + bytes([0x80, V1.checksum(pairs)])
            case('flat', V1.FLAT, b'\0' + flat, 32)
        elif k == 3:                                 # native strings anywhere
            src = rnd.choice((0x02000E51, 0x02029480, V1.FLAT, 0x02026080));size = rnd.choice((13, 17, 32))
            case('native', src, b'\x01' + bytes(rnd.randrange(0, 0xE4) for _ in range(size - 1)) + b'\xe5' + b'\0' * 4, size)
        elif k == 4:                                 # malformed format A
            src = rnd.choice((0x02000E51, V1.FLAT));size = 13 if src != V1.FLAT else 32
            case('malformed', src, b'\x80' + bytes(rnd.randrange(256) for _ in range(size)) + b'\x80\x00', size)
        else:                                        # 2-byte native symbol mixed in
            toks = ['가', 0xE457, rnd.choice(syll)];rec = R.encode(toks, 6);case('wide', 0x02000E51, rec, 13)
    rep = dict(id='exe45.hangul-fcopy.v1.cpu', passed=True, cases=n, kinds=kinds, base_rom=ROM, base_rom_sha256=sha(base), fcopy_sha256=sha(blob),
               tool_sha256=sha(Path(V2.__file__).read_bytes()), bench_sha256=sha(Path(__file__).read_bytes()),
               scope='Differential CPU: fcopy vs the verified v1 print hook on identical sources. Not a runtime/screen test.')
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_fcopy_v1';out.mkdir(parents=True, exist_ok=True)
    (out / 'report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('통과', n, kinds)


if __name__ == '__main__':main()
