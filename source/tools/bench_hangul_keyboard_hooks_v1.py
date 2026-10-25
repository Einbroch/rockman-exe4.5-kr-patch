"""CPU bench for hangul_keyboard_hooks_v1 on the 066 ROM + all five stubs (hooks at ROM offset 0x1F80000).

Typing sessions on the real A/B handler 0x080353B0 (stub -> composer), real native padding 0x080355F6, the flatten
hook, the print hook on descriptor 0 and the commit hook. Hangul behaviour is checked against hangul_editor_v1 /
hangul_record_v3 (host references); every native fall-through is checked against the unpatched 066 ROM on a second
CPU with identical state (differential). Not a runtime/screen test.
"""
import json,sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
import hangul_keyboard_hooks_v1 as H
import hangul_record_v3 as R
import hangul_editor_v1 as E
from korean_codec import HANGUL_BASE

BASE_ROM = 'poc/output/pending500_066_v1.gba'
AT = 0x1F80000
ST, WORDS, FLAT = 0x0200FC40, 0x0200FC60, 0x0200FC80
SL, KEYPTR, RET, SP0 = 0x03001000, 0x03001100, 0x08034F0D, 0x03007E00
A_KEY, B_KEY = 1, 2


def cpu(rom):
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    u.mem_map(0x08000000, 0x02000000);u.mem_write(0x08000000, rom)
    u.mem_map(0x02000000, 0x40000);u.mem_map(0x03000000, 0x8000);u.mem_map(0x04000000, 0x1000)
    return u


def call(u, entry, regs=None, sp=SP0):
    for r, v in (regs or {}).items():u.reg_write(r, v)
    u.reg_write(UC_ARM_REG_SP, sp);u.reg_write(UC_ARM_REG_LR, RET)
    u.emu_start(entry | 1, RET & ~1, count=200000)
    if u.reg_read(UC_ARM_REG_PC) != RET & ~1:raise AssertionError('no return from %x' % entry)


def set_state(u, limit, words, cursor, page, col, row, pressed):
    u.mem_write(ST, bytes(96))
    st = bytearray(0x20);st[4] = limit;st[6] = col;st[7] = row;st[8] = page
    st[0x10:0x14] = WORDS.to_bytes(4, 'little');st[0x14:0x18] = (WORDS + 2 * cursor).to_bytes(4, 'little')
    st[0x18:0x1C] = (WORDS + 2 * len(words)).to_bytes(4, 'little');st[0x1C:0x20] = (0x020010A6).to_bytes(4, 'little')
    u.mem_write(ST, bytes(st));u.mem_write(WORDS, b''.join(w.to_bytes(2, 'little') for w in words) + b'\xe5')
    u.mem_write(SL + 4, KEYPTR.to_bytes(4, 'little'));u.mem_write(KEYPTR, bytes(2) + pressed.to_bytes(2, 'little'))
    u.reg_write(UC_ARM_REG_R10, SL)


def get_state(u):
    st = bytes(u.mem_read(ST, 0x20));start = int.from_bytes(st[0x10:0x14], 'little')
    cur = (int.from_bytes(st[0x14:0x18], 'little') - start) // 2;end = (int.from_bytes(st[0x18:0x1C], 'little') - start) // 2
    words = [int.from_bytes(u.mem_read(start + 2 * i, 2), 'little') for i in range(end)]
    return words, cur, st


def is_hangul_word(w):return bool(w >> 15) and (w & 0xFF) < 0x80


def tok(w):
    """Token a flattened word stands for in Korean mode ('blank' for padding/unencodable)."""
    if is_hangul_word(w):return R.token_of(R.unword(w))
    if (w & 0xFF) == 0xE4:return 0xE400 | w >> 8
    if w >> 8 == 0 and (w & 0xFF) < 0xE4 and w != 0x98:return w & 0xFF
    return ('blank', w)


def native_bytes(t):return bytes([0xE4, t & 0xFF]) if isinstance(t, int) and t >> 8 == 0xE4 else bytes([t])


def expected_flat(words, limit):
    toks = [];hangul = False
    for w in words + [0x98] * (limit - len(words)):
        t = tok(w);toks.append(t);hangul |= is_hangul_word(w)
    if not hangul:return None
    body = bytearray()
    for t in toks:
        if isinstance(t, tuple):body.append(0x98)
        else:body += R.pair(R.value_of(t))
    pairs = bytes(b for b in body if b < 0x80)
    return bytes(body) + b'\xe5', bytes([0x80, H.checksum(pairs)])


def main():
    base = (ROOT / BASE_ROM).read_bytes();rom = bytearray(base.ljust(0x02000000, b'\xff'))
    blob, entries = H.build_all(AT);rom[AT:AT + len(blob)] = blob
    for o, b, _ in H.patches(base, entries):rom[o:o + len(b)] = b
    u = cpu(bytes(rom));ref = cpu(base.ljust(0x02000000, b'\xff'));rnd = random.Random(4545)
    st = dict(sessions=0, hangul_keys=0, accepted=0, rejected=0, hangul_b=0, native_diff=0, flatten=0, print_flat=0, commit=0)
    for session in range(4000):
        limit = rnd.choice((4, 6, 8, 10));ed = E.Editor(limit)
        if session % 5 == 0:                                            # start from native content too
            ed.words = [rnd.choice([c for c in range(0xE4) if c != 0x98]) for _ in range(rnd.randrange(0, limit))];ed.cursor = len(ed.words)   # 0x98 is padding only
        for step in range(rnd.randrange(5, 40)):
            if ed.words and rnd.random() < .15:ed.cursor = rnd.randrange(0, len(ed.words) + 1)
            r = rnd.random()
            if r < .7:page, row, col, pressed = 0, rnd.randrange(6), rnd.randrange(15), A_KEY
            elif r < .9:page, row, col, pressed = rnd.randrange(3), rnd.randrange(6), rnd.randrange(15), B_KEY
            else:
                page, pressed = rnd.choice((1, 2)), A_KEY;i = rnd.randrange((85, 75)[page - 1]);row, col = divmod(i, 15)   # page strings hold 85/75 cells
            set_state(u, limit, ed.words, ed.cursor, page, col, row, pressed)
            call(u, 0x080353B0, {UC_ARM_REG_R4: 0x44, UC_ARM_REG_R5: 0x02014DD0, UC_ARM_REG_R6: 0x66, UC_ARM_REG_R7: 0x77})
            got, gcur, _ = get_state(u)
            if u.reg_read(UC_ARM_REG_R4) != 0x44 or u.reg_read(UC_ARM_REG_R6) != 0x66 or u.reg_read(UC_ARM_REG_R7) != 0x77 or u.reg_read(UC_ARM_REG_SP) != SP0:raise AssertionError('callee-saved/sp')
            handled = False
            if pressed == A_KEY and page == 0:
                sel = E.SELECTORS[row * 15 + col];st['hangul_keys'] += 1;handled = True
                if sel != 0xFF:
                    ok = ed.press(sel);st['accepted' if ok else 'rejected'] += 1
                if u.reg_read(UC_ARM_REG_R0) != 1:raise AssertionError('consumed flag')
            elif pressed == B_KEY:
                handled = ed.backspace()
                if handled:st['hangul_b'] += 1
            if not handled:                                             # native fall-through: differential
                set_state(ref, limit, ed.words, ed.cursor, page, col, row, pressed);ref.reg_write(UC_ARM_REG_R5, 0x02014DD0)
                call(ref, 0x080353B0);want, wcur, _ = get_state(ref);ed.words, ed.cursor = want, wcur;st['native_diff'] += 1
                if u.reg_read(UC_ARM_REG_R0) != ref.reg_read(UC_ARM_REG_R0):raise AssertionError('native return value')
            if any((w & 0xFF) == 0xE5 for w in ed.words):raise AssertionError('E5 word after page %d row %d col %d key %d handled %s words %s cur %d limit %d' % (page, row, col, pressed, handled, [hex(x) for x in ed.words], ed.cursor, limit))
            if (got, gcur) != (ed.words, ed.cursor):raise AssertionError('session %d step %d: %s/%d vs %s/%d' % (session, step, [hex(x) for x in got], gcur, [hex(x) for x in ed.words], ed.cursor))
            # per-frame: native padding then the flatten hook; print descriptor 0 through the print hook
            set_state(u, limit, ed.words, ed.cursor, 0, 0, 0, 0);u.mem_write(FLAT, b'\x5a' * 32)
            call(u, 0x080355F6);call(u, 0x0803562C);flat = bytes(u.mem_read(FLAT, 32));st['flatten'] += 1
            exp = expected_flat(list(ed.words), limit)
            if exp is None:
                ref_words = list(ed.words);set_state(ref, limit, ref_words, ed.cursor, 0, 0, 0, 0);ref.mem_write(FLAT, b'\x5a' * 32)
                call(ref, 0x080355F6);call(ref, 0x0803562C);want = bytes(ref.mem_read(FLAT, 32))
                n = want.index(0xE5) + 1
                if flat[:n] != want[:n] or flat[30] != 0:raise AssertionError('native flatten')
            else:
                body, sig = exp
                if flat[:len(body)] != body or flat[30:32] != sig:raise AssertionError('flatten %s vs %s limit %d words %s cur %d' % (flat.hex(), body.hex(), limit, [hex(x) for x in ed.words], ed.cursor))
                slot = 0x02010AC0
                for r, v in ((UC_ARM_REG_R0, FLAT), (UC_ARM_REG_R2, 32), (UC_ARM_REG_R3, 0)):u.reg_write(r, v)
                u.reg_write(UC_ARM_REG_SP, SP0);u.emu_start(0x080517F8 | 1, H.PRINT_RET, count=200000)
                if u.reg_read(UC_ARM_REG_PC) != H.PRINT_RET or int.from_bytes(u.mem_read(SP0 - 4, 4), 'little') != slot:raise AssertionError('print continuation')
                out = bytes(u.mem_read(slot, 128))
                toks = [tok(w) for w in ed.words]
                want = R.display_tokens(toks) + b'\x98' * (limit - len(ed.words)) + b'\xe5'
                if out[:len(want)] != want:raise AssertionError('print flat %s vs %s' % (out[:len(want)].hex(), want.hex()))
                st['print_flat'] += 1
                # commit: jamo dropped; no syllable -> native bytes
                dest = 0x020010A6;u.mem_write(dest, b'\x77' * 22);u.mem_write(0x02014E74, b'\x5a' * 32)
                call(u, 0x08035000);rec = bytes(u.mem_read(dest, 22))
                keep = [t for t in toks if not (isinstance(t, str) and t in R.JAMO)]
                if any(R.is_syllable(t) for t in keep):want = bytes([0x80]) + b''.join(R.pair(R.value_of(t)) for t in keep) + b'\xe5'
                else:want = b'\x01' + b''.join(native_bytes(k) for k in keep) + b'\xe5'
                if rec[:len(want)] != want:raise AssertionError('commit %s vs %s' % (rec.hex(), want.hex()))
                echo = bytes(u.mem_read(0x02014E74, 32))
                if echo[:len(want) - 1] != want[1:] or (echo[30] == 0x80) != (want[0] == 0x80):raise AssertionError('echo')
                st['commit'] += 1
        st['sessions'] += 1
    rep = dict(id='exe45.hangul-keyboard-hooks.v1.cpu', passed=True, stats=st, base_rom=BASE_ROM, base_rom_sha256=sha(base), hooks_offset=hex(AT),
               blob_sha256=sha(blob), entries={k: hex(v) for k, v in entries.items()}, tool_sha256=sha(Path(H.__file__).read_bytes()),
               bench_sha256=sha(Path(__file__).read_bytes()),
               scope='Independent CPU: real A/B handler entry, native padding/flatten callers, print/commit hooks; host references + unpatched-066 differential. Not a runtime/screen test.')
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_keyboard_hooks_v1';out.mkdir(parents=True, exist_ok=True)
    (out / 'report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('통과', json.dumps(st, ensure_ascii=False))


if __name__ == '__main__':main()
