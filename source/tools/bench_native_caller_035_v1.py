"""Actual source BL entry, not a hand-assigned LR: current vs corrected fixture."""
import sys,struct,json
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R10,UC_ARM_REG_SP,UC_ARM_REG_LR
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from field_npc_rom_selector_035_v3 import wrap,source_population

def main():
    rp=ROOT/'poc/output/pending500_035_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    n=m['keyitem_rom']['npc035'];at=0x08000000+n['code_offset'];code,proof=wrap(source,at,m['keyitem_rom']['entry_address'],0x08000000+n['descriptor_offset'])
    old=rom[n['code_offset']:n['code_offset']+n['code_bytes']]
    diffs=[i for i,(a,b) in enumerate(zip(old,code)) if a!=b]
    if len(code)!=len(old) or proof['caller_lr']!=0x0804F773 or len(diffs)!=1:raise ValueError('single literal-byte correction constraint')
    pool=source_population(source,{p['source_archive'] for p in n['placements']});placements={p['source_archive']:p for p in n['placements']}
    exitpc=next(x['address'] for x in proof['proof']['instructions'] if x['mnemonic']=='pop' and 'r0' in x['operands'])
    results=[]
    for corrected in [False,True]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom)
        if corrected:u.mem_write(at,code)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);observed=[]
        def stop(uc,a,z,d):
            observed.append((struct.unpack('<I',uc.mem_read(uc.reg_read(UC_ARM_REG_SP),4))[0],uc.reg_read(UC_ARM_REG_LR)));uc.emu_stop()
        u.hook_add(UC_HOOK_CODE,stop,begin=exitpc,end=exitpc)
        count=0;selected=0
        for r in pool:
            for script in (range(255) if r['archive'] in placements else [0,254]):
                u.mem_write(0x02039800,r['payload']);u.mem_write(0x02000140,struct.pack('<I',0x02000200));u.mem_write(0x02000204,bytes([0xA0,r['sub']]))
                u.reg_write(UC_ARM_REG_R0,script);u.reg_write(UC_ARM_REG_R1,0);u.reg_write(UC_ARM_REG_R10,0x02000100);u.reg_write(UC_ARM_REG_SP,0x03007F00);u.reg_write(UC_ARM_REG_LR,0x08001001)
                observed.clear();u.emu_start(0x0804F765,0,count=100000)
                want=0x08000000+placements[r['archive']]['rom_offset'] if corrected and r['archive'] in placements else 0x02039800
                if observed!=[(want,0x0804F773)]:raise ValueError(('native caller/root failure',corrected,r['archive'],script,observed,hex(want)))
                count+=1;selected+=want!=0x02039800
        results.append({'corrected_fixture':corrected,'cases':count,'selected_clone':selected,'actual_BL_return_lr':0x0804F773})
    out=ROOT/'analysis/pending500_035_v1/native_caller_cause_v1.json'
    if out.exists():raise ValueError('report exists')
    report={'scope':'CPU instruction execution through original4F764 caller; corrected code only in bench memory, no game ROM mutation','source_sha256':sha(source),'rom_sha256':sha(rom),'actual_source_BL':'0804F76E','actual_return_lr':0x0804F773,'v1_guard_lr':n['wrapper']['caller_lr'],'cause':'v1 guard used BL instruction address|1 rather than return address; all selected native callers fall back','single_changed_file_offsets':[n['code_offset']+i for i in diffs],'results':results,'passed':True,'GBA_runtime_verified':False,'dependencies':{f'tools/{p}':sha((ROOT/'tools'/p).read_bytes()) for p in ['bench_native_caller_035_v1.py','field_npc_rom_selector_035_v3.py']}}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(report['results']))

if __name__=='__main__':main()
