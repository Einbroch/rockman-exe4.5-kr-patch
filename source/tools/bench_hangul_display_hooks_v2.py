"""CPU bench for hangul_display_hooks_v2 on the 066 product ROM (Korean nickname suffixes since 065) + 3 stubs.

* print: every v1 case again (copy buffers through the real v1 copy hook, direct records, native, malformed),
  work buffers 0x0200FC80/0x02014E54/0x02014E74 with signatures, and the real nickname builder 0x08038F60;
* commit: differential against the unpatched 066 commit function for native/unsigned/bad-checksum flat
  buffers, and format-A records + echo signature for signed Hangul flat buffers (then printed through descriptor 68).
Not a runtime/screen test.
"""
import json,sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
import hangul_display_hooks_v2 as H
import hangul_display_hooks_v1 as V1
import hangul_record_v2 as R
from korean_codec import HANGUL_BASE, HANGUL_COUNT, encode_character

BASE_ROM = 'poc/output/pending500_066_v1.gba'
COPY_AT, PRINT_AT, COMMIT_AT = 0x1F80000, 0x1F80200, 0x1F80600
META, SENT, SP0, RET = 0x0803B0D0, (0x11111111, 0x22222222, 0x33333333, 0x44444444), 0x03007E00, 0x08034FA4


def cpu(rom):
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    u.mem_map(0x08000000, 0x02000000);u.mem_write(0x08000000, rom)
    u.mem_map(0x02000000, 0x40000);u.mem_map(0x03000000, 0x8000)
    return u


def run(u, start, until, regs):
    for r, v in regs.items():u.reg_write(r, v)
    u.reg_write(UC_ARM_REG_SP, SP0)
    u.emu_start(start | 1, until, count=40000)
    if u.reg_read(UC_ARM_REG_PC) != until:raise AssertionError('did not reach continuation %x' % u.reg_read(UC_ARM_REG_PC))


def main():
    base = (ROOT / BASE_ROM).read_bytes();src = (ROOT / 'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
    rom = bytearray(base.ljust(0x02000000, b'\xff'))
    cb, _ = H.build_copy(0x08000000 + COPY_AT);pb, _ = H.build_print(0x08000000 + PRINT_AT);kb, _ = H.build_commit(0x08000000 + COMMIT_AT)
    for at, b in ((COPY_AT, cb), (PRINT_AT, pb), (COMMIT_AT, kb)):rom[at:at + len(b)] = b
    for o, b, _ in H.patches(base, COPY_AT, PRINT_AT, COMMIT_AT):rom[o:o + len(b)] = b
    u = cpu(bytes(rom));ref = cpu(base.ljust(0x02000000, b'\xff'));rnd = random.Random(4502)
    tab = [(int.from_bytes(base[0x526D0 + 8 * i:0x526D4 + 8 * i], 'little'), int.from_bytes(base[0x526D4 + 8 * i:0x526D8 + 8 * i], 'little')) for i in range(71)]
    rows = [dict(row=k, count=base[0x3B0D0 + 16 * k], desc=base[0x3B0D1 + 16 * k], limit=base[0x3B0D2 + 16 * k], base=0x02000950 + int.from_bytes(base[0x3B0DE + 16 * k:0x3B0E0 + 16 * k], 'little')) for k in range(26)]
    syll = [chr(HANGUL_BASE + i) for i in range(HANGUL_COUNT)]
    st = dict(print_hangul=0, print_native=0, print_rejected=0, nickname=0, commit_hangul=0, commit_native_diff=0, work_buffer=0)

    def regs_ok(sp):
        for r, v in zip((UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7), SENT):
            if u.reg_read(r) != v:raise AssertionError('callee-saved')
        if u.reg_read(UC_ARM_REG_SP) != sp:raise AssertionError('sp')

    def do_print(src_addr, size, counter=5):
        slot = V1.PRINT_BUF + counter * 128;u.mem_write(slot, b'\x5a' * 128)
        run(u, 0x080517F8, V1.PRINT_RET, {UC_ARM_REG_R0: src_addr, UC_ARM_REG_R2: size, UC_ARM_REG_R3: counter, UC_ARM_REG_R4: SENT[0], UC_ARM_REG_R5: SENT[1], UC_ARM_REG_R6: SENT[2], UC_ARM_REG_R7: SENT[3]})
        regs_ok(SP0 - 4)
        return bytes(u.mem_read(slot, 128))

    def do_copy(row, slot, record):
        rec = row['base'] + slot * (2 * row['limit'] + 2);u.mem_write(rec, record)
        dst, size = tab[row['desc']];u.mem_write(dst, b'\x5a' * 32)
        run(u, 0x08038BF8, V1.COPY_RET, {UC_ARM_REG_R0: rec + 1, UC_ARM_REG_R6: META + 16 * row['row'], UC_ARM_REG_R4: SENT[0], UC_ARM_REG_R5: SENT[1], UC_ARM_REG_R7: SENT[3]})
        return dst, size

    # 1. copy rows -> print (all syllables in the last slot for one 6- and one 8-char row; samples for every row)
    copy_rows = [r for r in rows if V1.BUF_LO <= tab[r['desc']][0] < V1.BUF_HI]
    for row in copy_rows:
        n = row['limit'];full = n in (6, 8) and row is next(r for r in copy_rows if r['limit'] == n)
        for i, s in enumerate(syll if full else rnd.sample(syll, 300)):
            toks = ['가'] * (n - 1) + [s] if i % 2 else [s, rnd.randrange(0, 0xE4)][:1 + (n > 1)]
            rec = R.encode(toks, n);dst, size = do_copy(row, i % row['count'], rec)
            out = do_print(dst, size, i % 16);d = R.display(rec, n)
            if out[:len(d)] != d or out[len(d):] != b'\x5a' * (128 - len(d)):raise AssertionError('copy row print')
            st['print_hangul'] += 1
        nat = (b'\x01' + bytes(rnd.randrange(0, 0xE4) for _ in range(n)) + b'\xe5').ljust(2 * n + 2, b'\0')
        dst, size = do_copy(row, 0, nat);out = do_print(dst, size)
        if out[:size] != bytes(u.mem_read(dst, size)):raise AssertionError('copy row native')
        st['print_native'] += 1
    # 2. direct records, strict + malformed
    direct = [(i, p, s) for i, (p, s) in enumerate(tab) if V1.REC_LO <= p < V1.REC_HI]
    for i, p, s in direct:
        n = (s - 1) // 2
        for t, sy in enumerate(rnd.sample(syll, 400)):
            rec = R.encode([sy] * (1 + t % n), n);u.mem_write(p - 1, rec)
            out = do_print(p, s);d = R.display(rec, n)
            if out[:len(d)] != d:raise AssertionError('direct %d' % i)
            st['print_hangul'] += 1
        for bad in (b'\x80\x7f\x7f\xe5', b'\x80\x00\x01\x02\xe5', b'\x80\xe5'):
            rec = bad.ljust(2 * n + 2, b'\0');u.mem_write(p - 1, rec);out = do_print(p, s)
            if out[:s] != rec[1:1 + s]:raise AssertionError('direct malformed %d' % i)
            st['print_rejected'] += 1
    # 3. nickname: real builder 0x08038F60 copies the name record + Korean suffix, then descriptor 1 prints it
    nick, nsize = tab[1]
    for t in range(3000):
        n = 6;toks = [rnd.choice(syll) for _ in range(rnd.randrange(1, n + 1))]
        if t < 64:toks = [syll[(t * 997 + k) % HANGUL_COUNT] for k in range(n)]
        name = R.encode(toks, n);u.mem_write(0x02000E50, name);u.mem_write(0x02000E5E, b'\x5a' * 23)
        # enter after the two state getters (gender/time) with r4 = suffix index; the frame holds {r4, pc}
        u.mem_write(SP0 - 8, SENT[0].to_bytes(4, 'little') + (RET | 1).to_bytes(4, 'little'))
        for r, v in ((UC_ARM_REG_R4, t % 4),):u.reg_write(r, v)
        u.reg_write(UC_ARM_REG_SP, SP0 - 8);u.emu_start(0x08038F6E | 1, RET, count=40000)
        if u.reg_read(UC_ARM_REG_PC) != RET:raise AssertionError('nickname builder did not return')
        built = bytes(u.mem_read(0x02000E5E, 23));tail = built[1 + 2 * len(toks):built.index(0xE5, 1 + 2 * len(toks)) + 1]
        if built[:1 + 2 * len(toks)] != name[:1 + 2 * len(toks)] or tail[:2] != b'\xf9\xfc':raise AssertionError('nickname builder layout')
        out = do_print(nick, nsize);d = R.display(name, n)[:-1] + tail
        if out[:len(d)] != d:raise AssertionError('nickname print %s' % ''.join(toks))
        st['nickname'] += 1
    # 4. commit: signed Hangul flat -> format A + echo signature; everything else identical to the original function
    for t in range(6000):
        fieldrow = rnd.choice(rows);n = fieldrow['limit'];dest = fieldrow['base'] + (rnd.randrange(fieldrow['count'])) * (2 * n + 2)
        old = bytes(rnd.randrange(256) for _ in range(2 * n + 2))
        for c in (u, ref):c.mem_write(dest, old);c.mem_write(0x0200FC40 + 0x1C, (dest).to_bytes(4, 'little'));c.mem_write(H.ECHO, b'\x5a' * 32)
        kind = t % 4
        if kind == 0:
            toks = [rnd.choice(syll) if rnd.random() < .8 else rnd.randrange(0, 0xE4) for _ in range(rnd.randrange(1, n + 1))]
            if not any(isinstance(x, str) for x in toks):toks[0] = '한'
            rec = R.encode(toks, n);body = rec[1:rec.index(0xE5, 1) + 1]
            flat = body.ljust(32, b'\x98')[:30] + bytes([0x80, V1.checksum(body[:-1])])
        else:
            body = bytes(rnd.randrange(0, 0xE4) for _ in range(rnd.randrange(0, n + 1))) + rnd.choice([b'\xe5', b'\x98'])
            flat = body.ljust(32, b'\x98')
            if kind == 2:flat = flat[:30] + bytes([0x80, V1.checksum(body[:-1]) ^ 1])        # signature with wrong checksum
            if kind == 3:flat = flat[:30] + b'\x80' + flat[31:]
        for c in (u, ref):c.mem_write(0x0200FC80, flat)
        run(u, 0x08035000, RET, {UC_ARM_REG_LR: RET | 1, UC_ARM_REG_R4: SENT[0], UC_ARM_REG_R5: SENT[1], UC_ARM_REG_R6: SENT[2], UC_ARM_REG_R7: SENT[3]})
        regs_ok(SP0)
        got = bytes(u.mem_read(dest, 2 * n + 2)), bytes(u.mem_read(H.ECHO, 32))
        if kind == 0:
            if got[0] != rec[:len(body) + 1] + old[len(body) + 1:] or got[1][:len(body)] != body or got[1][30:32] != bytes([0x80, V1.checksum(body[:-1])]):raise AssertionError('commit hangul')
            out = do_print(H.ECHO, 32);d = R.display(rec, n)
            if out[:len(d)] != d:raise AssertionError('echo print')
            st['commit_hangul'] += 1
        else:
            run(ref, 0x08035000, RET, {UC_ARM_REG_LR: RET | 1})
            want = bytes(ref.mem_read(dest, 2 * n + 2)), bytes(ref.mem_read(H.ECHO, 32))
            if got[0] != want[0] or got[1][:30] != want[1][:30] or got[1][30] != 0:raise AssertionError('commit native diff %d' % kind)
            st['commit_native_diff'] += 1
    # 5. work buffers: flat (descriptor 0) and schedule (67) with signatures
    for addr in (H.FLAT, H.SCHEDULE):
        for t in range(2000):
            toks = [rnd.choice(syll) for _ in range(rnd.randrange(1, 11))];rec = R.encode(toks, 10);body = rec[1:rec.index(0xE5, 1) + 1]
            u.mem_write(addr, body.ljust(30, b'\x98') + bytes([0x80, V1.checksum(body[:-1])]))
            out = do_print(addr, 32);d = R.display(rec, 10)
            if out[:len(d)] != d:raise AssertionError('work buffer')
            st['work_buffer'] += 1
        u.mem_write(addr, b'\x01\x02\xe5'.ljust(30, b'\x98') + b'\x80\x00');out = do_print(addr, 32)
        if out[:32] != bytes(u.mem_read(addr, 32)):raise AssertionError('work native')
        st['print_rejected'] += 1
    rep = dict(id='exe45.hangul-display-hooks.v2.cpu', passed=True, stats=st, base_rom=BASE_ROM, base_rom_sha256=sha(base),
               copy_hook_sha256=sha(cb), print_hook_sha256=sha(pb), commit_hook_sha256=sha(kb), print_hook_bytes=len(pb), commit_hook_bytes=len(kb),
               tool_sha256=sha(Path(H.__file__).read_bytes()), bench_sha256=sha(Path(__file__).read_bytes()),
               scope='Independent CPU on the 066 ROM + 3 stubs; real copier/memcpy/nickname builder; commit differential vs unpatched 066. Not a runtime/screen test.')
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_display_hooks_v2';out.mkdir(parents=True, exist_ok=True)
    (out / 'report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('통과', json.dumps(st, ensure_ascii=False))


if __name__ == '__main__':main()
