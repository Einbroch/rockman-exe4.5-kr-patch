"""Actual product delta and exhaustive helper ABI; no emulator/timing claim."""
import json
from build_visibility_poc import ROOT,require_hash,sha
from report_chip_library_runtime import read,require
from bench_chip_library import REGS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,__version__
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T


def main():
    rom=ROOT/'poc/output/exe45_ko_development_battle_names_v1.gba';m=read(rom.with_suffix('.json'));build=m['output_sha256']
    for suffix in ('','_repro'): require_hash(ROOT/f'poc/output/exe45_ko_development_battle_names_v1{suffix}.gba',build)
    base_path=ROOT/'poc/output/exe45_ko_development_chip_mono_batch03_v1.gba';base_m=read(base_path.with_suffix('.json'));require_hash(base_path,base_m['output_sha256'])
    source_path=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source_path,m['source_sha256']);native=source_path.read_bytes()
    base=base_path.read_bytes();blob=rom.read_bytes();ext=m['chip_battle_name_extension'];ids=set(ext['selected_scripts'])
    require(ids==set(range(1,91)) and m['translated_units']==base_m['translated_units']==249,'unit/scope denominator')
    delta=[i for i,(a,b) in enumerate(zip(base,blob)) if a!=b]
    require(delta==list(range(0x1F7D4,0x1F7DC)) and blob[0x800000:len(base)]==base[0x800000:] and len(blob)==len(base)+68,'source/payload delta exceeded')
    require(ext['clone_offset']==m['chip_library_extension']['clone_offset']==base_m['chip_library_extension']['clone_offset'],'actual clone location changed')
    require(m['translation_assets']==[dict(a,scope=(a['scope']+'; caller-gated native8x1 battle name reuse; wording counted once')) if a['archive']=='765190' else a for a in base_m['translation_assets']],'translation assets/prose changed')
    require(all(p['final_placement_roundtrip'] for p in ext['machine_code']),'machine-code placement proof')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    require(__version__=='2.1.4','CPU engine drift')
    engines=[];stop=[0]
    for data in (native,blob):
        uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB);uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        uc.mem_map(0x08000000,0x1000000);uc.mem_write(0x08000000,data);uc.mem_map(0x03000000,0x8000)
        uc.hook_add(UC_HOOK_CODE,lambda u,a,s,d:u.emu_stop() if a==stop[0] else None);engines.append(uc)
    vectors=0;selected=0;callers=[0x08000000+x+5 for x in (0x15BC2,0x166A8,0x17500,0x1F53A,0x1F65E,0x20C80)]
    for caller in callers:
        stop[0]=caller&~1
        for raw in list(range(512))+[0xFFFFFFFF,0x12345601,0x12345701,0x1000001D,0x80000000]:
            results=[];values=[raw,0x11223344]+[0x10203040+i for i in range(2,13)]+[0x03007F00,caller]
            for uc in engines:
                uc.mem_write(0x03007EF4,bytes([0xA7])*24);uc.reg_write(UC_ARM_REG_CPSR,0xA0000030)
                for reg,value in zip(REGS,values): uc.reg_write(reg,value)
                uc.emu_start(0x0801F7D5,stop[0],count=120)
                require(uc.reg_read(UC_ARM_REG_PC)==stop[0],'helper return')
                require(bytes(uc.mem_read(0x03007EF4,4))==bytes([0xA7])*4 and bytes(uc.mem_read(0x03007F00,12))==bytes([0xA7])*12,'helper stack boundary')
                results.append([uc.reg_read(reg) for reg in REGS]+[uc.reg_read(UC_ARM_REG_CPSR)])
            expected=list(results[0])
            if caller==0x080166AD and raw&511 in ids: expected[0]=0x08000000+ext['clone_offset'];selected+=1
            require(results[1]==expected,'helper registers/SP/CPSR or source fallback differs');vectors+=1
    out=ROOT/'analysis/exe45_battle_names_build_cpu_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'status':'PASS product delta/repro and CPU native-helper differential; runtime pending',
        'rom_sha256':build,'base_rom_sha256':base_m['output_sha256'],'tool_sha256':sha((ROOT/'tools/verify_battle_name_build.py').read_bytes()),
        'source_changed_offsets':delta,'append_bytes':68,'existing_payloads_byte_identical':True,
        'vectors':vectors,'selected_vectors':selected,'other_vectors_native':vectors-selected,'callers':callers,
        'registers_flags_stack_match':True,'limits':['CPU helper fixture, not runtime reachability/font/pixel or audio/hardware timing proof','no computed interior entry exclusion','wordings needs_review; not complete-game release']},indent=2),encoding='utf-8')
    print('PASS actual battle-name product delta/repro and',vectors,'helper CPU vectors')


if __name__=='__main__': main()
