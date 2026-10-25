"""Controlled CPU mapping regression for mixed initial glyphs after adding middle dot."""
import json,struct
from build_visibility_poc import ROOT,sha
from bench_hangul_composer_thumb import *
from hangul_mixed_display import CODE,display
from hangul_editor_display import JAMO_INDICES,JAMO_BASE
from hangul_composer_thumb import KEYS
from korean_codec import encode_character,decode_character

def main():
    out=ROOT/'analysis/middle_dot_v1/mapping_cpu.json'
    if out.exists():raise ValueError('Preserve evidence')
    blob,isa=assemble_verified(CODE,0x08001000,{})
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for at,size in ((0x08000000,8192),(0x02000000,8192),(0x03007000,4096),(0x0FF00000,4096)):u.mem_map(at,size)
    u.mem_write(0x08001000,blob);src,dst,sp,stop=0x02000100,0x02001100,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11];vectors=0
    for partial in range(19):
        for slot in range(10):
            words=[0]*10;words[slot]=11172+partial;raw=bytes([10,10,slot,255])+struct.pack('<10H',*words)
            expected=b''.join(bytes.fromhex('f9fc')+struct.pack('<H',JAMO_INDICES[KEYS[partial]] if i==slot else 0) for i in range(10))+b'\xe5'
            if display(raw,0)!=expected:raise ValueError('Host jamo mapping')
            for mode in (0,1):
                u.mem_write(0x02000000,b'\xa7'*8192);u.mem_write(src,raw)
                u.reg_write(UC_ARM_REG_CPSR,0x30)
                for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(src,dst,41,mode)):u.reg_write(r,v)
                for i,r in enumerate(regs):u.reg_write(r,0x12340000+i)
                u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);u.emu_start(0x08001001,stop,count=25000)
                n=u.reg_read(UC_ARM_REG_R0)
                if n!=(41 if mode==0 else 0) or u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x12340000+i for i,r in enumerate(regs)):raise ValueError('CPU mapping/ABI')
                if bytes(u.mem_read(src,24))!=raw or bytes(u.mem_read(dst,41))!=(expected if not mode else b'\xa7'*41):raise ValueError('Atomic output/source')
                vectors+=1
    if encode_character(',').hex()!='f9fca42b' or encode_character('·').hex()!='f9fca52b' or decode_character(encode_character('·'))!=('·',4):raise ValueError('Stable extras')
    result=dict(passed=True,vectors=vectors,normal_text_middle_dot_index=11173,preserved_comma_index=11172,jamo_base=JAMO_BASE,jamo_mapping=JAMO_INDICES,machine_code=isa,helper_sha256=sha(blob),rom_integrated=False,limits='Synthetic mixed-editor display helper mapping/ABI only; no keyboard/save integration.')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS mixed partial mapping',vectors,'CPU vectors')

if __name__=='__main__':main()
