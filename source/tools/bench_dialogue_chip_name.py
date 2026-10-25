"""Final hook bytes versus native six-instruction effects; synthetic CPU only."""
import json,struct
from report_roll_pet import ROOT,read,sha
from build_visibility_poc import require_hash
from bench_chip_library import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,REGS
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
import unicorn

def main(stem,outdir):
    if unicorn.__version__!='2.1.4':raise ValueError('CPU engine drift')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1');require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    rp=ROOT/f'poc/output/{stem}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();h=m['dialogue_chip_name'];cases=[]
    def execute(blob,before,buffer,cpsr):
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(blob)+4095)&~4095);u.mem_write(0x08000000,blob);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_write(before[5]+100,struct.pack('<H',buffer));u.reg_write(UC_ARM_REG_CPSR,cpsr)
        for r,v in zip(REGS,before):u.reg_write(r,v)
        reached=[]
        def stop(engine,address,size,user):
            if address==0x08051638:reached.append(address);engine.emu_stop()
        u.hook_add(UC_HOOK_CODE,stop);u.emu_start(0x0805162D,0,count=150)
        if reached!=[0x08051638]:raise ValueError('name hook did not reach native continuation')
        return [u.reg_read(r) for r in REGS],u.reg_read(UC_ARM_REG_CPSR)
    variants=['selected','other_stream','other_context','other_name']
    if 'gutsman_command_stream' in h:variants+=['guts_selected','guts_other_stream','guts_other_context','guts_other_name']
    for variant in variants:
        for buffer in [0,1,7,255]:
            for flags in [0,0xF0000000]:
                before=[0x1000+i*0x101 for i in range(15)];before[0]=0x08765190;before[1]=h['native_name_stream']-before[0];before[4]=h['command_stream'];before[5]=h['context'];before[13]=0x03007F00;before[14]=0x08051583
                if variant.startswith('guts_'):before[4]=h['gutsman_command_stream']
                if variant.endswith('other_stream'):before[4]+=4
                if variant.endswith('other_context'):before[5]+=0x100
                if variant.endswith('other_name'):before[1]+=1
                native,nf=execute(source,before,buffer,flags|0xF3);actual,af=execute(rom,before,buffer,flags|0xF3);expected=list(native)
                if variant in ['selected','guts_selected']:expected[0]=0x08000000+h['name_offset']
                if actual!=expected or af!=nf:raise ValueError('printChip ABI/register/SP/LR/CPSR or fallback fixture')
                cases.append({'variant':variant,'buffer_index':buffer,'initial_flags':flags,'all_registers_match_native_except_selected_r0':True,'cpsr_matches_native':True})
    result={'policy':'synthetic CPU bench; not GBA gameplay or audio/timing','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'vectors':len(cases),'cases':cases};out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);(out/'selector_bench.json').write_text(json.dumps(result,indent=2),encoding='utf-8');return result
