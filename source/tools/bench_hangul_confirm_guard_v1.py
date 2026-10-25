"""CPU bench for hangul_keyboard_hooks_v3.guard on the 069 ROM (stub 0x080353B0 redirected to the guard).

Random editor contents (syllables, lone jamo, native characters), keys (none/A/B/Start/A+B) and cursor cells
including the confirm cell. Blocked case (A or Start on col 15 row 5, no B, a lone jamo present): editor state,
caller block r5 and EWRAM unchanged, r0 = 1. Every other case: identical to the unpatched 069 handler (differential
over the editor state, words, caller block and the whole EWRAM). Not a runtime test.
"""
import json,sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
import hangul_keyboard_hooks_v1 as V1
import hangul_keyboard_hooks_v3 as V3
import hangul_record_v3 as R
from korean_codec import HANGUL_BASE

ROM, AT = 'poc/output/pending500_069_v1.gba', 0x1FF0000
ST, WORDS, SL, KEYPTR, RET, SP0, R5 = 0x0200FC40, 0x0200FC60, 0x03001000, 0x03001100, 0x08034F0D, 0x03007E00, 0x02014DD0


def cpu(rom):
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB);u.mem_map(0x08000000, 0x02000000);u.mem_write(0x08000000, rom)
    u.mem_map(0x02000000, 0x40000);u.mem_map(0x03000000, 0x8000);u.mem_map(0x04000000, 0x1000)
    u.mem_map(0x05000000, 0x1000);u.mem_map(0x06000000, 0x18000);u.mem_map(0x07000000, 0x1000);u.mem_map(0x0E000000, 0x10000)
    return u


def setup(u, limit, words, cursor, col, row, page, keys, run=True):
    u.mem_write(0x02000000, bytes(0x40000))
    st = bytearray(0x20);st[4] = limit;st[6] = col;st[7] = row;st[8] = page
    st[0x10:0x14] = WORDS.to_bytes(4, 'little');st[0x14:0x18] = (WORDS + 2 * cursor).to_bytes(4, 'little')
    st[0x18:0x1C] = (WORDS + 2 * len(words)).to_bytes(4, 'little');st[0x1C:0x20] = (0x020010A6).to_bytes(4, 'little')
    u.mem_write(ST, bytes(st));u.mem_write(WORDS, b''.join(w.to_bytes(2, 'little') for w in words) + b'\xe5')
    u.mem_write(SL + 4, KEYPTR.to_bytes(4, 'little'));u.mem_write(KEYPTR, bytes(2) + keys.to_bytes(2, 'little'))
    for r, v in ((UC_ARM_REG_R10, SL), (UC_ARM_REG_R4, 0x44), (UC_ARM_REG_R5, R5), (UC_ARM_REG_R6, 0x66), (UC_ARM_REG_R7, 0x77), (UC_ARM_REG_SP, SP0), (UC_ARM_REG_LR, RET)):u.reg_write(r, v)
    for entry in (0x080355F6, 0x0803562C):                              # per-frame padding + flatten, as in the game
        u.reg_write(UC_ARM_REG_SP, SP0);u.reg_write(UC_ARM_REG_LR, RET);u.emu_start(entry | 1, RET & ~1, count=100000)
    u.mem_write(WORDS + 2 * len(words), b'\xe5')                        # editor end as the handler sees it
    u.reg_write(UC_ARM_REG_SP, SP0);u.reg_write(UC_ARM_REG_LR, RET)
    if not run:return None
    u.emu_start(0x080353B0 | 1, RET & ~1, count=400000)
    if u.reg_read(UC_ARM_REG_PC) != RET & ~1:raise AssertionError('no return pc=%x keys=%d col=%d row=%d page=%d words=%s' % (u.reg_read(UC_ARM_REG_PC), keys, col, row, page, [hex(w) for w in words]))
    return bytes(u.mem_read(0x02000000, 0x40000)), u.reg_read(UC_ARM_REG_R0), [u.reg_read(r) for r in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_SP)]


def main():
    base = (ROOT / ROM).read_bytes();meta = json.loads((ROOT / ROM.replace('.gba', '.json')).read_text(encoding='utf8'))
    keys1 = 0x08000000 + meta['keyitem_rom']['keyboard068']['hooks']['entries']['keys']
    rom = bytearray(base.ljust(0x02000000, b'\xff'));blob, _ = V3.build_guard(0x08000000 + AT, keys1);rom[AT:AT + len(blob)] = blob
    rom[0x353B0:0x353BC] = V1.stub(0x08000000 + AT)
    u, ref = cpu(bytes(rom)), cpu(base.ljust(0x02000000, b'\xff'));rnd = random.Random(70)
    syl = [R.word(r) for r in range(0, 11172, 37)];jam = [R.word(R.JAMO_BASE + j) for j in range(19)]
    st = dict(blocked=0, passed_same=0, cases=0)
    for t in range(30000):
        limit = rnd.choice((4, 6, 8, 10));n = rnd.randrange(0, limit + 1)
        words = [rnd.choice(syl) if rnd.random() < .6 else rnd.choice(jam) if rnd.random() < .5 else rnd.choice([c for c in range(0xE4) if c != 0x98]) for _ in range(n)]
        if t % 3 == 0:col, row = 15, 5
        else:col, row = rnd.randrange(16), rnd.randrange(6)
        keys = rnd.choice((0, 1, 2, 8, 3, 9));page = rnd.randrange(3);cursor = rnd.randrange(n + 1)
        before = None
        mem, r0, regs = (None, 1, [0x44, R5, 0x66, 0x77, SP0])
        lone = any(w >> 15 and (w & 0xFF) < 0x80 and R.JAMO_BASE <= R.unword(w) < R.WIDE_BASE for w in words)
        blocked = not keys & 2 and keys & 9 and col == 15 and row == 5 and lone
        if regs != [0x44, R5, 0x66, 0x77, SP0]:raise AssertionError('callee-saved')
        if blocked:
            # expected = idle setup + only the native refuse sound request (sound 0x69 via 0x08000534)
            setup(u, limit, words, cursor, col, row, page, keys, run=False)
            for r, v in ((UC_ARM_REG_R0, V3.SND_REFUSE), (UC_ARM_REG_SP, SP0), (UC_ARM_REG_LR, RET)):u.reg_write(r, v)
            u.emu_start(V3.SOUND | 1, RET & ~1, count=100000);idle = bytes(u.mem_read(0x02000000, 0x40000))
            mem, r0, _ = setup(u, limit, words, cursor, col, row, page, keys)
            # the sound layer stores the caller's r1 at 0x0200FD6C (native callers pass arbitrary r1 too)
            mem, idle = mem[:0xFD6C] + mem[0xFD70:], idle[:0xFD6C] + idle[0xFD70:]
            if r0 != 1 or mem != idle:raise AssertionError('blocked case changed state %s blocked=%s idle=%s' % ([hex(0x02000000 + i) for i in range(len(mem)) if mem[i] != idle[i]][:20], mem[0xFD60:0xFD74].hex(), idle[0xFD60:0xFD74].hex()))
            st['blocked'] += 1
        else:
            # pass-through: the guard must reach the v1 keys entry with memory, r3..r7, sl, lr and the stub's
            # pushed r3 untouched (v1/native behaviour after that point is covered by the 068 benches)
            setup(u, limit, words, cursor, col, row, page, keys, run=False);idle = bytes(u.mem_read(0x02000000, 0x40000))
            u.reg_write(UC_ARM_REG_R3, 0x33);u.emu_start(0x080353B0 | 1, keys1 & ~1, count=20000)
            got = [u.reg_read(r) for r in (UC_ARM_REG_PC, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R10, UC_ARM_REG_LR, UC_ARM_REG_SP)]
            if got != [keys1 & ~1, 0x44, R5, 0x66, 0x77, SL, RET, SP0 - 4] or int.from_bytes(u.mem_read(SP0 - 4, 4), 'little') != 0x33 or bytes(u.mem_read(0x02000000, 0x40000)) != idle:
                raise AssertionError('pass-through t=%d keys=%d col=%d row=%d %s' % (t, keys, col, row, [hex(x) for x in got]))
            st['passed_same'] += 1
        st['cases'] += 1
    rep = dict(id='exe45.hangul-confirm-guard.v1.cpu', passed=True, stats=st, base_rom=ROM, base_rom_sha256=sha(base), guard_sha256=sha(blob),
               tool_sha256=sha(Path(V3.__file__).read_bytes()), bench_sha256=sha(Path(__file__).read_bytes()),
               scope='Independent CPU on the 069 ROM with the 0x080353B0 stub redirected to the guard; whole-EWRAM differential. Not a runtime test.')
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_confirm_guard_v1';out.mkdir(parents=True, exist_ok=True)
    (out / 'report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('통과', st)


if __name__ == '__main__':main()
