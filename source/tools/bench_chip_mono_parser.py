"""Actual native fixed-cell parser at9x3/10x3; bounded stage transfer stub only."""
import argparse
import json
import struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells
from tpl_literals import resolve_units
from bench_chip_library import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,REGS
from unicorn.arm_const import *


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rom',required=True);ap.add_argument('--origin',required=True);ap.add_argument('--step',type=int,required=True);ap.add_argument('--asset',required=True);ap.add_argument('--out',required=True);args=ap.parse_args()
    rom_path=ROOT/args.rom;m=read(rom_path.with_suffix('.json'));build=m['output_sha256'];require_hash(rom_path,build)
    p=ROOT/args.origin;verify_route(p,build,set());prefix=f'step_{args.step:03d}'
    iw=(p/f'{prefix}_gbaIntWorkRam.bin').read_bytes();ew=(p/f'{prefix}_gbaExtWorkRam.bin').read_bytes();f=m['fixedcell_extension'];mono=f['mono_provider']
    require(struct.unpack_from('<I',iw,0x67FC)[0]==0x08000001+f['hook_offset'],'observed F9 dispatch does not match ROM')
    asset=ROOT/args.asset;record=next(a for a in m['translation_assets'] if a['archive']=='76937C');require_hash(asset,record['sha256']);units=resolve_units(read(asset))
    wanted={ch for u in units for ch in u['translation'] if '\uac00'<=ch<='\ud7a3'};cells=bdf_cells(ROOT/mono['font']['path'],wanted,mono['raster'])
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes();blob=rom_path.read_bytes()
    table={v:int(k,16) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    ar=next(r for r in m['archives'] if r['archive']=='76937C');base=ar['rom_offset'];ctx=0x0200F2C0;obj=struct.unpack_from('<I',ew,0xF2F8)[0]
    require(0x02000000<=obj<=0x0203FFB0,'observed font state bounds')
    helper=struct.unpack_from('<I',iw,0x6894)[0]&~1;require(helper==0x08000850,'native upload helper drift')
    uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB);uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    uc.mem_map(0x08000000,(len(blob)+4095)&~4095);uc.mem_write(0x08000000,blob)
    uc.mem_map(0x02000000,0x40000);uc.mem_map(0x03000000,0x8000);uc.mem_map(0x06000000,0x18000);uc.mem_map(0x0FF00000,0x1000)
    stop=0x0FF00000;stage=0x02018000;target=0x06012800;sp=0x03007F00;writes=[];transfers=[];glyphs=[]
    def code_hook(engine,address,size,user):
        if address==stop: engine.emu_stop()
        elif address==0x0300689C:
            glyphs.append((engine.reg_read(UC_ARM_REG_R6),engine.reg_read(UC_ARM_REG_R1),engine.reg_read(UC_ARM_REG_R2)))
        elif address==helper:
            src,dst,count=[engine.reg_read(r) for r in REGS[:3]]
            if src!=stage or dst!=target or count not in (1728,1920): raise ValueError('unbounded stage upload contract')
            engine.mem_write(dst,bytes(engine.mem_read(src,count)));transfers.append((src,dst,count))
            engine.reg_write(UC_ARM_REG_PC,engine.reg_read(UC_ARM_REG_LR)|1)
    def write_hook(engine,access,address,size,value,user): writes.append((address,size))
    uc.hook_add(UC_HOOK_CODE,code_hook);uc.hook_add(UC_HOOK_MEM_WRITE,write_hook);records=[]
    for width in (9,10):
        for u in units:
            script=int(u['id'].split(':')[1]);start=0x08000000+base+struct.unpack_from('<H',blob,base+script*2)[0]
            uc.mem_write(0x02000000,ew);uc.mem_write(0x03000000,iw);uc.mem_write(stage-4,bytes([0xA7])*(width*3*64+8))
            uc.mem_write(target-4,bytes([0xA7])*(width*3*64+8));uc.reg_write(UC_ARM_REG_CPSR,0x30)
            values=[start,0,stage,target,width,3,0x08619EF8,0,0x87654321,0x12345678,ctx,0xABCDEF,0xFEDA,sp,stop|1]
            for reg,value in zip(REGS,values): uc.reg_write(reg,value)
            writes.clear();transfers.clear();glyphs.clear();uc.emu_start(0x03006825,stop,count=30000)
            require(uc.reg_read(UC_ARM_REG_PC)==stop and uc.reg_read(UC_ARM_REG_SP)==sp,'native parser did not return/balanced stack')
            lines=u['translation'].split('\n');expected=[];expected_glyphs=[]
            for line in lines+['']*(3-len(lines)):
                require(len(line)<=width,'literal width exceeds parser fixture')
                for ch in line.ljust(width):
                    if ch in cells: cell=cells[ch];font=0x08000000+mono['font_offset'];index=ord(ch)-0xAC00
                    else:
                        index=table[ch];font=0x08619EF8;cell=native[0x619EF8+index*64:0x619EF8+(index+1)*64]
                    expected.append(cell);expected_glyphs.append((font,index,stage+(len(expected)-1)*64))
            require(glyphs==expected_glyphs,'native parser/provider glyph cursor sequence')
            payload=b''.join(expected)
            actual=bytes(uc.mem_read(stage,len(payload)))
            mismatch=next((i for i,(a,b) in enumerate(zip(actual,payload)) if a!=b),None)
            require(actual==payload and bytes(uc.mem_read(target,len(payload)))==payload,
                f'native parser stage/upload bytes script={script} width={width} mismatch={mismatch} actual={actual[:16].hex()} target={bytes(uc.mem_read(target,16)).hex()} transfers={transfers} expected={payload[:16].hex()} fontstate={bytes(uc.mem_read(obj,4)).hex()} tinttable={bytes(uc.mem_read(0x03006814,16)).hex()}')
            require(transfers==[(stage,target,width*3*64)],'native parser upload denominator')
            require(uc.reg_read(UC_ARM_REG_R0)==sum(len(line) for line in lines),'native decoded literal-cell count')
            require(bytes(uc.mem_read(stage-4,4))==bytes([0xA7])*4 and bytes(uc.mem_read(stage+len(payload),4))==bytes([0xA7])*4,'native stage out-of-bounds')
            require(all(stage<=a and a+s<=stage+len(payload) or obj<=a and a+s<=obj+0x40 or sp-128<=a and a+s<=sp for a,s in writes),'native parser write outside stage/fontstate/stack')
            records.append({'script':script,'width':width,'rows':3,'stage_bytes':len(payload),'glyphs':len(glyphs),'decoded_cells':sum(len(line) for line in lines),'stage_sha256':sha(payload)})
    out=ROOT/args.out;require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS CPU native parser9x3/10x3 plus provider/copier; not other consumer runtime proof',
        'vectors':len(records),'records':records,'origin_result_sha256':sha((p/'result.json').read_bytes()),
        'tool_sha256':sha((ROOT/'tools/bench_chip_mono_parser.py').read_bytes()),
        'stage_transfer':'native helper08000850 replaced with bounded exact byte-copy contract; no DMA/BIOS/timing claim',
        'limits':['CPU fixture context; not normal battle/tooltip reachability or palette/OBJ proof','shared pointer2165C/D2B58 runtime still required']},indent=2),encoding='utf-8')
    print('PASS actual native mono parser at9x3 and10x3:',len(records),'CPU script vectors')


if __name__=='__main__': main()
