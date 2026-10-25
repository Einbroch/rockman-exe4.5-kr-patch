"""CPU check of the041 composed selector on the built ROM (Unicorn, Thumb-1).

Entry at common4FB4C stub with real r0/r1/lr; stop at the040 wrapper entry.
Positive: every descriptor with its declared bytes at root swaps r0 to clone.
Negative: script>=count, one corrupted byte, foreign root stay unchanged.
r1,r2,r4..r7,lr and sp preserved; original r3 is on the stack as040 expects.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
from keyitem_rom_selector import INSTALL

REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7]


def run(rom,stop,root,script,ram_bytes,lr=0x0804F7BD):
    mu=Uc(UC_ARCH_ARM,UC_MODE_THUMB);mu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);size=(len(rom)+0xFFFF)&~0xFFFF
    mu.mem_map(0x08000000,size);mu.mem_write(0x08000000,rom);mu.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
    mu.mem_map(0x02000000,0x40000);mu.mem_map(0x03000000,0x8000)
    if ram_bytes is not None:mu.mem_write(root,ram_bytes)
    sp=0x03007E00;mu.reg_write(UC_ARM_REG_SP,sp)
    init=[root,script,0x22222222,0x33333333,0x44444444,0x55555555,0x66666666,0x77777777]
    for r,v in zip(REGS,init):mu.reg_write(r,v)
    mu.reg_write(UC_ARM_REG_LR,lr)
    mu.emu_start(0x08000000+INSTALL|1,stop&~1,count=20_000_000)
    if mu.reg_read(UC_ARM_REG_PC)!=stop&~1:raise ValueError('did not reach040 entry')
    out=[mu.reg_read(r) for r in REGS];nsp=mu.reg_read(UC_ARM_REG_SP);pushed=int.from_bytes(mu.mem_read(nsp,4),'little')
    ok=out[1]==script and out[2]==0x22222222 and out[4:]==init[4:] and mu.reg_read(UC_ARM_REG_LR)==lr and nsp==sp-4 and pushed==0x33333333
    if ram_bytes is not None and bytes(mu.mem_read(root,len(ram_bytes)))!=ram_bytes:ok=False
    return out[0],ok


def main():
    p=argparse.ArgumentParser();p.add_argument('rom');p.add_argument('--key',default='typed041');p.add_argument('--out');a=p.parse_args()
    rom=(ROOT/a.rom).read_bytes();meta=json.loads((ROOT/a.rom).with_suffix('.json').read_text(encoding='utf8'));n=meta['keyitem_rom'][a.key]
    stop=n['previous_wrapper_address'];cases=dict(selected=0,out_of_range=0,corrupted=0,foreign=0);fail=[]
    def body(p):
        at=p['match']-0x08000000;return rom[at:at+p['match_length']]
    for q in n['placements']:
      for root in ([0x02024000,0x0203F000-((q['match_length']+3)&~3)] if q['root']==0 else [q['root']]):
        p=dict(q,root=root);ram=body(p) if p['match_sha256'] else None
        for script in sorted({0,p['script_count']-1}):
            r0,ok=run(rom,stop,p['root'],script,ram)
            if r0!=p['clone'] or not ok:fail.append(('selected',p['archives'],script,hex(r0)))
            cases['selected']+=1
        r0,ok=run(rom,stop,p['root'],p['script_count'],ram)
        if r0!=p['root'] or not ok:fail.append(('out_of_range',p['archives'],hex(r0)))
        cases['out_of_range']+=1
        if ram is not None:
            for at in sorted({0,len(ram)//2,len(ram)-1}):
                bad=bytearray(ram);bad[at]^=0xFF;r0,ok=run(rom,stop,p['root'],0,bytes(bad))
                if r0!=p['root'] or not ok:fail.append(('corrupted',p['archives'],at,hex(r0)))
                cases['corrupted']+=1
            fr=p['root']+0x100 if q['root'] else 0x03000100
            r0,ok=run(rom,stop,fr,0,ram if q['root'] else None)
            if r0!=fr or not ok:fail.append(('foreign',p['archives'],hex(r0)))
            cases['foreign']+=1
    report=dict(passed=not fail,rom=a.rom,rom_sha256=sha(rom),descriptors=len(n['placements']),cases=cases,failures=fail,scope='Selector entry->040 wrapper entry only; not renderer/runtime/UI.')
    print(json.dumps(report,ensure_ascii=False,indent=1))
    if a.out:(ROOT/a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sys.exit(0 if not fail else 1)


if __name__=='__main__':main()
