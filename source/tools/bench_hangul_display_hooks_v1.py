"""CPU bench for hangul_display_hooks_v1 on the original ROM with only the two stubs + hook blobs installed.

Runs the real ARMv4T Thumb code from each stub site to the native continuation (copy: 0x08038BF8..0x08038C04,
print: 0x080517F8..0x08051804), including the native E5 copier and size memcpy they call. Expected bytes come
from hangul_record_v2 (independent host reference) or plain native semantics.
"""
import json,sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
import hangul_display_hooks_v1 as H
import hangul_record_v2 as R
from korean_codec import HANGUL_BASE, HANGUL_COUNT

COPY_AT, PRINT_AT = 0xF80000, 0xF80200
META, SENT = 0x0803B0D0, (0x11111111, 0x22222222, 0x33333333, 0x44444444)
SP0 = 0x03007E00


class Cpu:
    def __init__(self, rom):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        self.u.mem_map(0x08000000, 0x02000000);self.u.mem_write(0x08000000, rom)
        self.u.mem_map(0x02000000, 0x40000);self.u.mem_map(0x03000000, 0x8000)

    def run(self, start, until, regs):
        u = self.u
        for r, v in regs.items():u.reg_write(r, v)
        u.reg_write(UC_ARM_REG_SP, SP0)
        u.emu_start(start | 1, until, count=20000)
        if u.reg_read(UC_ARM_REG_PC) != until:raise AssertionError('did not reach continuation')
        return u


def setup():
    src = (ROOT / 'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
    rom = bytearray(src.ljust(0x01000000, b'\xff'))
    cb, cproof = H.build_copy(0x08000000 + COPY_AT);pb, pproof = H.build_print(0x08000000 + PRINT_AT)
    rom[COPY_AT:COPY_AT + len(cb)] = cb;rom[PRINT_AT:PRINT_AT + len(pb)] = pb
    for o, b, _ in H.patches(src, COPY_AT, PRINT_AT):rom[o:o + len(b)] = b
    return src, bytes(rom), cb, pb


def table(src):
    return [(int.from_bytes(src[0x526D0 + 8 * i:0x526D4 + 8 * i], 'little'), int.from_bytes(src[0x526D4 + 8 * i:0x526D8 + 8 * i], 'little')) for i in range(71)]


def rows(src):
    out = []
    for k in range(26):
        m = src[0x3B0D0 + 16 * k:0x3B0E0 + 16 * k]
        out.append(dict(row=k, count=m[0], desc=m[1], limit=m[2], base=0x02000950 + int.from_bytes(m[14:16], 'little')))
    return out


def native_record(limit, rnd):
    body = bytes(rnd.randrange(0, 0xE4) for _ in range(rnd.randrange(1, limit + 1)))
    return (b'\x01' + body + b'\xe5').ljust(2 * limit + 2, b'\0')


def main():
    src, rom, cb, pb = setup();cpu = Cpu(rom);u = cpu.u;tab = table(src);rnd = random.Random(45)
    stats = dict(copy_hangul=0, copy_native=0, copy_rejected=0, print_hangul=0, print_native=0, print_rejected=0)
    def check_regs():
        for r, v in zip((UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R7), (SENT[0], SENT[1], SENT[3])):
            if u.reg_read(r) != v:raise AssertionError('callee-saved register')
    def do_copy(row, slot, record):
        rec = row['base'] + slot * (2 * row['limit'] + 2);u.mem_write(rec, record)
        dst, size = tab[row['desc']];u.mem_write(dst, b'\x5a' * 32)
        u.mem_write(dst + size, b'\x80\x00')                       # stale signature must be replaced/cleared
        cpu.run(0x08038BF8, H.COPY_RET, {UC_ARM_REG_R0: rec + 1, UC_ARM_REG_R6: META + 16 * row['row'], UC_ARM_REG_R4: SENT[0], UC_ARM_REG_R5: SENT[1], UC_ARM_REG_R7: SENT[3]})
        check_regs()
        if u.reg_read(UC_ARM_REG_R6) != META + 16 * row['row'] or u.reg_read(UC_ARM_REG_SP) != SP0:raise AssertionError('r6/sp')
        end = record.index(0xE5, 1);out = bytes(u.mem_read(dst, 32))
        if out[:end] != record[1:end + 1]:raise AssertionError('native copy semantics')
        return dst, size, out[size:size + 2]
    def do_print(src_addr, size, counter):
        slot = H.PRINT_BUF + counter * 128;u.mem_write(slot, b'\x5a' * 128)
        cpu.run(0x080517F8, H.PRINT_RET, {UC_ARM_REG_R0: src_addr, UC_ARM_REG_R2: size, UC_ARM_REG_R3: counter, UC_ARM_REG_R4: SENT[0], UC_ARM_REG_R5: SENT[1], UC_ARM_REG_R6: SENT[2], UC_ARM_REG_R7: SENT[3]})
        check_regs()
        if u.reg_read(UC_ARM_REG_R6) != SENT[2] or u.reg_read(UC_ARM_REG_SP) != SP0 - 4 or int.from_bytes(u.mem_read(SP0 - 4, 4), 'little') != slot:raise AssertionError('print slot push')
        return bytes(u.mem_read(slot, 128))
    copy_rows = [r for r in rows(src) if H.BUF_LO <= tab[r['desc']][0] < H.BUF_HI]
    if len(copy_rows) != 10:raise AssertionError('copy rows')
    syll = [chr(HANGUL_BASE + i) for i in range(HANGUL_COUNT)]
    # 1. copy rows: every syllable in the last slot of a full field, copy then print through the copy buffer
    for row in ([r for r in copy_rows if r['limit'] == 6][:1] + [r for r in copy_rows if r['limit'] == 8][:1]):
        n = row['limit']
        for i, s in enumerate(syll):
            toks = ['가'] * (n - 1) + [s];rec = R.encode(toks, n)
            dst, size, sig = do_copy(row, i % row['count'], rec)
            if sig != bytes([0x80, H.checksum(rec[1:rec.index(0xE5, 1)])]):raise AssertionError('signature')
            out = do_print(dst, size, i % 16);disp = R.display(rec, n)
            if out[:len(disp)] != disp or out[len(disp):] != b'\x5a' * (128 - len(disp)):raise AssertionError('print expansion %s' % s)
            stats['copy_hangul'] += 1;stats['print_hangul'] += 1
    # 2. every copy row: mixed native/Hangul samples, native records, malformed Hangul records
    for row in copy_rows:
        n = row['limit'];dst, size = tab[row['desc']]
        for t in range(300):
            k = rnd.randrange(1, n + 1);toks = [rnd.choice(syll) if rnd.random() < 0.7 else rnd.randrange(0, 0xE4) for _ in range(k)]
            if not any(isinstance(x, str) for x in toks):toks[0] = '한'
            rec = R.encode(toks, n);_, _, sig = do_copy(row, rnd.randrange(row['count']), rec)
            out = do_print(dst, size, t % 16);disp = R.display(rec, n)
            if sig[0] != 0x80 or out[:len(disp)] != disp:raise AssertionError('mixed')
            stats['copy_hangul'] += 1;stats['print_hangul'] += 1
            rec = native_record(n, rnd);_, _, sig = do_copy(row, rnd.randrange(row['count']), rec)
            out = do_print(dst, size, t % 16)
            if sig[0] != 0 or out[:size] != bytes(u.mem_read(dst, size)) or out[size:] != b'\x5a' * (128 - size):raise AssertionError('native')
            stats['copy_native'] += 1;stats['print_native'] += 1
        good = R.encode(['가', '나'], n)
        bad = [b'\x80\x80\x00\xe5', b'\x80\x7f\x7f\xe5', b'\x80\x00\x01\x02\xe5', b'\x80\xe5']   # high byte, value range, odd end, empty
        for rec in bad:
            _, _, sig = do_copy(row, 0, rec.ljust(2 * n + 2, b'\0'))
            out = do_print(dst, size, 3)
            if sig[0] != 0 or out[:size] != bytes(u.mem_read(dst, size)):raise AssertionError('malformed copy %s' % rec.hex())
            stats['copy_rejected'] += 1;stats['print_rejected'] += 1
        # right body, wrong checksum -> native
        do_copy(row, 0, good);u.mem_write(dst + size + 1, bytes([H.checksum(good[1:5]) ^ 1]))
        out = do_print(dst, size, 4)
        if out[:size] != bytes(u.mem_read(dst, size)):raise AssertionError('checksum')
        stats['print_rejected'] += 1
    # 3. direct-record descriptors (pointer in the profile block): full sweep for one 6- and one 8-char field, samples elsewhere
    direct = [(i, p, s) for i, (p, s) in enumerate(tab) if H.REC_LO <= p < H.REC_HI]
    if not direct:raise AssertionError('direct descriptors')
    sweep = {next(i for i, p, s in direct if s == 13), next(i for i, p, s in direct if s == 17)}
    for i, p, s in direct:
        n = (s - 1) // 2
        for t, sy in enumerate(syll if i in sweep else rnd.sample(syll, 200)):
            rec = R.encode([sy] * n if t % 2 else [sy], n);u.mem_write(p - 1, rec)
            out = do_print(p, s, t % 16);disp = R.display(rec, n)
            if out[:len(disp)] != disp:raise AssertionError('direct %d' % i)
            stats['print_hangul'] += 1
        rec = native_record(n, rnd);u.mem_write(p - 1, rec);out = do_print(p, s, 1)
        if out[:s] != rec[1:1 + s]:raise AssertionError('direct native')
        stats['print_native'] += 1
    # 4. outside both areas a 0x80 byte before the source must not matter
    u.mem_write(0x02026080 - 1, b'\x80' + R.encode(['가'], 8)[1:]);out = do_print(0x02026080, 17, 2)
    if out[:17] != bytes(u.mem_read(0x02026080, 17)):raise AssertionError('outside area')
    stats['print_native'] += 1
    rep = dict(id='exe45.hangul-display-hooks.v1.cpu', passed=True, stats=stats, copy_hook_bytes=len(cb), print_hook_bytes=len(pb),
               copy_hook_sha256=sha(cb), print_hook_sha256=sha(pb), tool_sha256=sha(Path(H.__file__).read_bytes()),
               bench_sha256=sha(Path(__file__).read_bytes()), source_sha256=sha(src),
               scope='Independent CPU on the original ROM + stubs; real native copier/memcpy; host reference hangul_record_v2. Not a runtime/screen test.')
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_display_hooks_v1';out.mkdir(parents=True, exist_ok=True)
    (out / 'report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('통과', json.dumps(stats, ensure_ascii=False))


if __name__ == '__main__':main()
