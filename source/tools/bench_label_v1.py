"""CPU check of the label-renderer hooks (0x554A4 / 0x554DC, entered at 0x554D0) on a built label-batch ROM.

From each site with r0=root, r1=script run to the resume point (0x554B0 / 0x554E8). Expect:
r0 = chosen root + u16(root[2*script]) where chosen root is the clone for matching bytes and the
original root otherwise; r1 = the trampoline's return address (dead: the next original instruction at
0x554B0/0x554E8 is mov r1,sb); the replayed pushes (r8 or ip, then lr) on the stack; r2..r7 and sp otherwise preserved.
Usage: bench_label_v1.py ROM KEY [--out JSON]
"""
import argparse,json,sys,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha

SITES={0x554A4:0x080554B0,0x554D0:0x080554E8}   # 554D0 = real entry through the hooked 554DC


def run(rom,site,root,script,ram):
    mu=Uc(UC_ARCH_ARM,UC_MODE_THUMB);mu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);size=(len(rom)+0xFFFF)&~0xFFFF
    mu.mem_map(0x08000000,size);mu.mem_write(0x08000000,rom);mu.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
    mu.mem_map(0x02000000,0x40000);mu.mem_map(0x03000000,0x8000)
    if ram is not None:mu.mem_write(root,ram)
    sp=0x03007E00;regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7]
    init=[root,script,0x22222222,0x33333333,0x44444444,0x55555555,0x66666666,0x77777777]
    for r,v in zip(regs,init):mu.reg_write(r,v)
    mu.reg_write(UC_ARM_REG_SP,sp);mu.reg_write(UC_ARM_REG_R8,0x88888888);mu.reg_write(UC_ARM_REG_R12,0xCCCCCCCC);mu.reg_write(UC_ARM_REG_LR,0x08017755)
    stop=SITES[site];mu.emu_start(0x08000000+site|1,stop,count=20_000_000)
    if mu.reg_read(UC_ARM_REG_PC)!=stop:raise ValueError('no resume')
    out=[mu.reg_read(r) for r in regs];nsp=mu.reg_read(UC_ARM_REG_SP)
    if site==0x554A4:
        ok=out[1]==0x080554B1 and nsp==sp-8 and struct.unpack('<II',bytes(mu.mem_read(nsp,8)))==(0x88888888,0x08017755)
    else:
        ok=out[1]==0x080554E9 and nsp==sp-8 and struct.unpack('<II',bytes(mu.mem_read(nsp,8)))==(0xCCCCCCCC,0x08017755)
    ok=ok and out[2:]==init[2:] and mu.reg_read(UC_ARM_REG_R8)==0x88888888
    return out[0],ok


def main():
    p=argparse.ArgumentParser();p.add_argument('rom');p.add_argument('key');p.add_argument('--out');a=p.parse_args()
    rom=(ROOT/a.rom).read_bytes();meta=json.loads((ROOT/a.rom).with_suffix('.json').read_text(encoding='utf8'));n=meta['keyitem_rom'][a.key];fail=[];cases=0
    def u16(addr,i):return struct.unpack_from('<H',rom,addr-0x08000000+2*i)[0]
    for q in n['placements']:
        clone=q['clone'];ram=rom[q['match']-0x08000000:q['match']-0x08000000+q['match_length']] if q['match_sha256'] else None
        root=q['root'] or 0x02024000
        for site in SITES:
            for s in sorted({0,q['script_count']-1}):
                r0,ok=run(rom,site,root,s,ram);cases+=1
                if r0!=clone+u16(clone,s) or not ok:fail.append(('selected',site,q['archives'],s,hex(r0)))
            if ram is not None:
                bad=bytearray(ram);bad[len(bad)//2]^=0xFF;r0,ok=run(rom,site,root,0,bytes(bad));cases+=1
                if r0!=root+struct.unpack_from('<H',bad,0)[0] or not ok:fail.append(('corrupted',site,q['archives'],hex(r0)))
    rep=dict(passed=not fail,rom=a.rom,rom_sha256=sha(rom),key=a.key,descriptors=len(n['placements']),cases=cases,failures=fail[:20],scope='Label renderer entry->resume only; not the IWRAM parser, glyph supply or screen.')
    print(json.dumps(rep,ensure_ascii=False,indent=1))
    for r in SITES.values():
        if rom[r-0x08000000:r-0x08000000+2]!=bytes.fromhex('4946'):raise ValueError('resume instruction is not mov r1,sb')
    if a.out:(ROOT/a.out).write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sys.exit(0 if not fail else 1)


if __name__=='__main__':main()
