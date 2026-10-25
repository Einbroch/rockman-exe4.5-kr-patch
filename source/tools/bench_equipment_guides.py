"""Final Thumb byte CPU fixtures, not GBA gameplay or timing evidence."""
import json,struct
from build_visibility_poc import ROOT,require_hash
from bench_chip_library import REGS
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T

def main(stem='exe45_ko_development_equipment_guides_v1',outdir='equipment_guides_v1'):
    rp=ROOT/f'poc/output/{stem}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU engine drift')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    writes=[]
    def cb(uc,address,size,user):
        if address in [0x0804F7B6,0x08012344]:uc.emu_stop()
    u.hook_add(UC_HOOK_CODE,cb);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,a,address,size,value,user:writes.append((address,size)))
    u.mem_write(0x02000140,struct.pack('<I',0x02000200));root=0x08000000+m['equipment_guides']['archive']['rom_offset'];cases=[]
    for navi in list(range(23))+[255]:
        for selection in range(3):
            before=[0x1000+i*0x101 for i in range(15)];before[0]=selection;before[10]=0x02000100;before[13]=0x03007F00;before[14]=0x08012345
            for r,v in zip(REGS,before):u.reg_write(r,v)
            u.mem_write(0x02000201,bytes([navi]));writes.clear();u.emu_start(0x0803C479,0,count=200)
            after=[u.reg_read(r) for r in REGS]
            expected_root=root if navi in [0,13,14] else 0x08000000+m['equipment_guides']['roll_archive']['rom_offset'] if navi==1 and 'roll_archive' in m['equipment_guides'] else 0x0202BA7C
            if after[0]!=expected_root or after[1]!=selection+60 or after[2:12]!=before[2:12] or after[13]!=before[13]-4 or after[14]!=0x0803C485 or struct.unpack('<I',u.mem_read(after[13],4))[0]!=before[14]:raise ValueError('guide ABI/selection fixture')
            if any(not before[13]-12<=a<=before[13]-s for a,s in writes):raise ValueError('guide unexpected memory write')
            u.emu_start(0x0803C485,0,count=4)
            if u.reg_read(REGS[13])!=before[13]:raise ValueError('native return stack')
            cases.append({'navi':navi,'selection':selection,'root':after[0],'script':after[1],'stack_restore':True,'preserved_r2_r11':True,'writes_stack_only':True})
    result={'policy':'synthetic CPU bench, not GBA execution/timing','rom_sha256':m['output_sha256'],'passed':True,'vectors':len(cases),'cases':cases,'normal_dialogue_call_not_executed':True}
    p=ROOT/'analysis'/outdir;p.mkdir(parents=True,exist_ok=True);(p/'bench.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(p/'bench.json')

if __name__=='__main__':main()
