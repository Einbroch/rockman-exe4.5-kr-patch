"""Execute final provider and actual native copier; CPU, not GBA timing QA."""
import argparse
import json
import struct
import sys
from build_visibility_poc import ROOT,sha,require_hash
sys.path.insert(0,str(ROOT/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from bench_chip_library import REGS
from fixedcell_font import bdf_cells


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rom',required=True);ap.add_argument('--out',required=True);ap.add_argument('--keyboard-glyphs',action='store_true');args=ap.parse_args()
    rom_path=ROOT/args.rom;out=ROOT/args.out
    if out.exists(): raise ValueError('refuse report overwrite')
    m=json.loads(rom_path.with_suffix('.json').read_text());require_hash(rom_path,m['output_sha256'])
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256'])
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    if unicorn.__version__!='2.1.4': raise ValueError('CPU engine drift')
    blob=rom_path.read_bytes();native=source.read_bytes();f=m['fixedcell_extension'];mono=f['mono_provider']
    require_hash(ROOT/mono['spec_path'],mono['spec_sha256']);require_hash(ROOT/f['font']['path'],f['font']['sha256'])
    wanted={chr(0xAC00+i) for i in range(11172)}
    extra_order=[]
    if args.keyboard_glyphs:
        from hangul_editor_display import JAMO_INDICES
        from hangul_composer_thumb import KEYS
        extra_order=[',']+list(KEYS)
        k=m['hangul_keyboard_glyphs']
        if k['mapping']!=JAMO_INDICES or k['fixed_order']!=extra_order or not k['final_placement_verified'] or k['input_hooks_installed']:raise ValueError('keyboard supply scope')
        wanted.update(extra_order)
    banks={0x08601738:(f['font_offset'],bdf_cells(ROOT/f['font']['path'],wanted,f['raster'])),
           0x08619EF8:(mono['font_offset'],bdf_cells(ROOT/f['font']['path'],wanted,mono['raster']))}
    for at,cells in banks.values():
        order=[chr(0xAC00+i) for i in range(11172)]+extra_order
        if blob[at:at+len(order)*64]!=b''.join(cells[ch] for ch in order): raise ValueError('provider final font mismatch')
    uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB);uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    uc.mem_map(0x08000000,(len(blob)+4095)&~4095);uc.mem_write(0x08000000,blob)
    uc.mem_map(0x02000000,0x40000);uc.mem_map(0x03000000,0x8000);uc.mem_map(0x0FF00000,0x1000)
    uc.mem_write(0x03006800,native[0x1EF700:0x1EF800])
    stop=0x0FF00000;legacy=0x030069D8;copier_hits=[0];legacy_hits=[0];writes=[]
    def code_hook(engine,address,size,user):
        if address==stop: engine.emu_stop()
        elif address==0x0300689C: copier_hits[0]+=1
        elif address==legacy: legacy_hits[0]+=1;engine.emu_stop()
    def write_hook(engine,access,address,size,value,user): writes.append((address,size))
    uc.hook_add(UC_HOOK_CODE,code_hook);uc.hook_add(UC_HOOK_MEM_WRITE,write_hook)
    stream=0x02001000;stage=0x02002000;ctx=0x02003000;obj=0x02003100;sp=0x03007F00
    uc.mem_write(ctx+0x38,struct.pack('<I',obj))
    vectors=0
    def run(font,index,tint):
        nonlocal vectors
        before=[stream,0xA5A5,stage,1,7,2,font,0x12345678,0x87654321,3,ctx,0xABCDEF,0xFEDA,sp,stop|1]
        uc.reg_write(UC_ARM_REG_CPSR,0xF0000030)
        for reg,value in zip(REGS,before): uc.reg_write(reg,value)
        uc.mem_write(stream,bytes([0xF9,0xFC,index&255,index>>8]));uc.mem_write(obj+2,bytes([tint*4]))
        uc.mem_write(stage-4,bytes([0xA7])*72);writes.clear();hits=copier_hits[0]
        uc.emu_start(0x08000001+f['hook_offset'],stop,count=2000)
        expected=list(before);expected[0]+=4;expected[1]=0xFFFFFFFC;expected[2]+=64;expected[4]+=1;expected[5]+=1;expected[9]+=1
        expected[14]=next(i['address']+4 for i in f['machine_code']['instructions'] if i['mnemonic']=='mov' and i['operands']=='lr, pc')
        after=[uc.reg_read(reg) for reg in REGS]
        if after!=expected or copier_hits[0]!=hits+1: raise ValueError(f'provider/copier ABI {font:X}/{index}/{tint}: {after} != {expected}')
        ch=chr(0xAC00+index) if index<11172 else extra_order[index-11172]
        cell=banks[font][1][ch];add=0x44444444*tint
        transformed=b''.join(struct.pack('<I',(struct.unpack_from('<I',cell,i)[0]+add)&0xFFFFFFFF) for i in range(0,64,4))
        if bytes(uc.mem_read(stage,64))!=transformed or bytes(uc.mem_read(stage-4,4))!=bytes([0xA7])*4 or bytes(uc.mem_read(stage+64,4))!=bytes([0xA7])*4:
            raise ValueError('native copier pixel/bounds mismatch')
        if any(not (stage<=a and a+s<=stage+64 or sp-28<=a and a+s<=sp) for a,s in writes): raise ValueError('provider write outside stage/stack')
        vectors+=1
    for font in banks:
        for index in range(11172): run(font,index,0)
        for index in (0,1,27,28,587,11171):
            for tint in (1,2,3): run(font,index,tint)
        for index in range(11172,11172+len(extra_order)):
            for tint in range(4):run(font,index,tint)
    # Non-FC subcommands tail-call without selecting either new provider.
    for font in banks:
        for sub in (0,1,2,0xFD,0xFF):
            before=[stream,0xA5A5,stage,1,7,2,font,0x12345678,0x87654321,3,ctx,0xABCDEF,0xFEDA,sp,stop|1]
            uc.reg_write(UC_ARM_REG_CPSR,0x30)
            for reg,value in zip(REGS,before): uc.reg_write(reg,value)
            uc.mem_write(stream,bytes([0xF9,sub,0,0]));writes.clear();hits=legacy_hits[0]
            uc.emu_start(0x08000001+f['hook_offset'],stop,count=100)
            expected=list(before);expected[1]=legacy|1
            if [uc.reg_read(r) for r in REGS]!=expected or legacy_hits[0]!=hits+1 or writes: raise ValueError('legacy F9 tail-call changed')
            vectors+=1
    out.write_text(json.dumps({'rom_sha256':m['output_sha256'],'status':'PASS CPU provider selection, native copier, legacy tail-call; runtime pending',
        'vectors':vectors,'all_syllables_per_provider':11172,'boundary_tint_vectors':36,'legacy_vectors':10,
        'native_copier_executed':True,'font_offsets':{hex(k):v[0] for k,v in banks.items()},
        'keyboard_extra_characters':extra_order,'keyboard_extra_vectors':len(extra_order)*2*4,
        'tool_sha256':sha((ROOT/'tools/bench_fixedcell_mono_provider.py').read_bytes()),
        'limits':['CPU fixtures, not emulator scanout/timing or actual translated script evidence','legacy handler intercepted at native entry; no full legacy semantics claim']},indent=2),encoding='utf-8')
    print('PASS fixedcell big/mono selection and real native copier:',vectors,'CPU vectors')


if __name__=='__main__':
    main()
