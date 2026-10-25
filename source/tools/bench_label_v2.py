"""CPU check of the v2 cumulative label lookup (0x554A4 and 0x554D0->0x554DC) on a built ROM.

Positive: every ROM-table root and every RAM-table entry (its own payload placed at EWRAM) resumes with
r0 = clone + u16(clone[2*script]). Negative: every catalog LZ native that is not a mapped payload, placed in
EWRAM, resumes with r0 = root + its own table offset. Reports the maximum instruction count per call.
Usage: bench_label_v2.py ROM KEY [--out JSON]
"""
import argparse,json,sys,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_PROT_READ,UC_PROT_EXEC,UC_HOOK_CODE
from unicorn.arm_const import *
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SITES={0x554A4:(0x080554B0,0x080554B1),0x554D0:(0x080554E8,0x080554E9)}


def make(rom):
    mu=Uc(UC_ARCH_ARM,UC_MODE_THUMB);mu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);size=(len(rom)+0xFFFF)&~0xFFFF
    mu.mem_map(0x08000000,size);mu.mem_write(0x08000000,rom);mu.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
    mu.mem_map(0x02000000,0x40000);mu.mem_map(0x03000000,0x8000);n=[0];mu.hook_add(UC_HOOK_CODE,lambda uc,a,s,u:n.__setitem__(0,n[0]+1));return mu,n


def run(st,site,root,script,ram):
    mu,n=st;n[0]=0
    if ram is not None:mu.mem_write(0x02024000,b'\0'*0x8000);mu.mem_write(root,ram)
    init=[root,script,0x22222222,0x33333333,0x44444444,0x55555555,0x66666666,0x77777777]
    for i,v in enumerate(init):mu.reg_write(UC_ARM_REG_R0+i,v)
    sp=0x03007E00;mu.reg_write(UC_ARM_REG_SP,sp);mu.reg_write(UC_ARM_REG_R8,0x88888888);mu.reg_write(UC_ARM_REG_R12,0xCCCCCCCC);mu.reg_write(UC_ARM_REG_LR,0x08017755)
    stop,ret=SITES[site];mu.emu_start(0x08000000+site|1,stop,count=2_000_000)
    if mu.reg_read(UC_ARM_REG_PC)!=stop:raise ValueError('no resume')
    out=[mu.reg_read(UC_ARM_REG_R0+i) for i in range(8)];nsp=mu.reg_read(UC_ARM_REG_SP)
    pushed=struct.unpack('<II',bytes(mu.mem_read(nsp,8)));want=(0x88888888 if site==0x554A4 else 0xCCCCCCCC,0x08017755)
    ok=out[1]==ret and out[2:]==init[2:] and nsp==sp-8 and pushed==want
    return out[0],ok,n[0]


def main():
    p=argparse.ArgumentParser();p.add_argument('rom');p.add_argument('key');p.add_argument('--out');a=p.parse_args()
    rom=(ROOT/a.rom).read_bytes();meta=read(a.rom.replace('.gba','.json'));L=meta['keyitem_rom'][a.key]['label_lookup'];st=make(rom);fail=[];cases=0;worst=0
    def u16(addr,i,buf=None):return struct.unpack_from('<H',buf if buf is not None else rom,(0 if buf is not None else addr-0x08000000)+2*i)[0]
    mapped=set()
    for i in range(L['rom_entries']):
        root,clone,count=struct.unpack_from('<III',rom,L['romtab']-0x08000000+12*i)
        for site in SITES:
            for s in sorted({0,count-1}):
                r0,ok,c=run(st,site,root,s,None);cases+=1;worst=max(worst,c)
                if r0!=clone+u16(clone,s) or not ok:fail.append(('rom',hex(root),site,s,hex(r0)))
            r0,ok,c=run(st,site,root,count,None) if count<256 else (root+u16(root,0),True,0);cases+=1
    # RAM entries: find the mapped payload among every batch's match copies by the entry's own samples
    payloads={}
    for k,v in meta['keyitem_rom'].items():
        if k.startswith('typed') and k[5:].isdigit() and isinstance(v,dict) and 'placements' in v:
            for q in v['placements']:
                if q.get('match_sha256'):payloads.setdefault('all',[]).append(rom[q['match']-0x08000000:q['match']-0x08000000+q['match_length']])
    for i in range(L['ram_entries']):
        clone,count,_=struct.unpack_from('<IHH',rom,L['ramtab']-0x08000000+40*i)
        samples=[struct.unpack_from('<HBB',rom,L['ramtab']-0x08000000+40*i+8+4*j)[:2] for j in range(8)]
        body=next((b for b in payloads.get('all',[]) if all(o<len(b) and b[o]==v for o,v in samples)),None)
        if body is None:fail.append(('ram entry payload not found',hex(clone)));continue
        mapped.add(sha(body))
        for site in SITES:
            r0,ok,c=run(st,site,0x02024000,0,body);cases+=1;worst=max(worst,c)
            if r0!=clone+u16(clone,0) or not ok:fail.append(('ram',hex(clone),site,hex(r0)))
    cfg=read('project.json');src=(ROOT/cfg['source_profile']['filename']).read_bytes();neg=0
    for arc,row in {f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}.items():
        if not row['compressed']:continue
        body=payload_of(src,row)
        if sha(body)in mapped or len(body)>0x8000:continue
        r0,ok,c=run(st,0x554A4,0x02024000,0,body);cases+=1;neg+=1;worst=max(worst,c)
        if r0!=0x02024000+u16(0,0,body) or not ok:fail.append(('negative',arc,hex(r0)))
    rep=dict(passed=not fail,rom=a.rom,rom_sha256=sha(rom),key=a.key,rom_entries=L['rom_entries'],ram_entries=L['ram_entries'],negatives=neg,cases=cases,max_instructions_per_call=worst,failures=fail[:20],scope='Label renderer entry->resume only; not the IWRAM parser, glyph supply or screen.')
    print(json.dumps(rep,ensure_ascii=False,indent=1))
    if a.out:(ROOT/a.out).write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sys.exit(0 if not fail else 1)


if __name__=='__main__':main()
