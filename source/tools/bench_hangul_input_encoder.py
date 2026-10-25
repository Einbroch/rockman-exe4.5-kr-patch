"""Emitted Thumb helper proof; isolated CPU fixtures, NOT an installed ROM hook."""
import json,struct,sys
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha
from extended_dialogue import assemble_verified
from korean_codec import encode_syllable
sys.path.insert(0,str(ROOT/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *

CODE='''cmp r0, #19
bhs reject
cmp r1, #21
bhs reject
cmp r2, #28
bhs reject
push {r4, lr}
movs r4, #21
muls r0, r4, r0
adds r0, r0, r1
movs r4, #28
muls r0, r4, r0
adds r0, r0, r2
movs r1, #0xf9
strb r1, [r3]
movs r1, #0xfc
strb r1, [r3, #1]
strb r0, [r3, #2]
lsrs r0, r0, #8
strb r0, [r3, #3]
movs r0, #4
pop {r4, pc}
reject:
movs r0, #0
bx lr
'''

def main():
    out=ROOT/'analysis/hangul_keyboard_v1/cpu_encoder';out.mkdir(parents=True,exist_ok=True)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    address=0x08000000;blob,isa=assemble_verified(CODE,address,{})
    if any(i['mnemonic'] not in {'cmp','bhs','push','movs','muls','adds','strb','lsrs','pop','bx'} or len(bytes.fromhex(i['hex']))!=2 for i in isa['instructions']):raise ValueError('unexpected Thumb-1 emitted instruction')
    uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB);uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    uc.mem_map(address,4096);uc.mem_write(address,blob);uc.mem_map(0x02000000,4096);uc.mem_map(0x03007000,4096);uc.mem_map(0x0ff00000,4096)
    dest=0x02000100;stack=0x03007f00;stop=0x0ff00000;count=0
    def run(l,v,t,expected):
        nonlocal count
        uc.mem_write(dest-4,b'\xa7'*12)
        uc.reg_write(UC_ARM_REG_CPSR,0x30)
        for reg,value in [(UC_ARM_REG_R0,l),(UC_ARM_REG_R1,v),(UC_ARM_REG_R2,t),(UC_ARM_REG_R3,dest),(UC_ARM_REG_R4,0x13579bdf),(UC_ARM_REG_R5,0x2468ace0),(UC_ARM_REG_SP,stack),(UC_ARM_REG_LR,stop|1)]:uc.reg_write(reg,value)
        uc.emu_start(address|1,stop,count=100)
        if uc.reg_read(UC_ARM_REG_PC)!=stop or uc.reg_read(UC_ARM_REG_R0)!=(4 if expected else 0) or uc.reg_read(UC_ARM_REG_R4)!=0x13579bdf or uc.reg_read(UC_ARM_REG_R5)!=0x2468ace0 or uc.reg_read(UC_ARM_REG_SP)!=stack:raise ValueError('helper ABI/return')
        if bytes(uc.mem_read(dest-4,12))!=b'\xa7'*4+(expected or b'\xa7'*4)+b'\xa7'*4:raise ValueError('encoder bytes/bounds/rejected writes')
        count+=1
    for l in range(19):
        for v in range(21):
            for t in range(28):run(l,v,t,encode_syllable(chr(0xac00+l*588+v*28+t)))
    for bad in [19,21,28,255,65535,0xffffffff]:
        for slot in range(3):
            args=[0,0,0];args[slot]=bad
            if args[slot]<(19,21,28)[slot]:continue
            run(*args,None)
    (out/'helper.bin').write_bytes(blob)
    report=dict(passed=True,scope='isolated Thumb encode(L,V,T)->F9FC+syllable_index; no native ABI or ROM hook installation',vectors=count,all_modern_syllables=11172,helper_sha256=sha(blob),machine_code=isa,tool_sha256=sha(Path(__file__).read_bytes()),limits=['Host composer state machine not compiled or installed by this helper.','Output pointer is a bounded CPU fixture; no project RAM reservation inferred.','No committed record format/save/keyboard glyph/cell-selection verification.','Invalid vector samples only; not exhaustive entire32-bit invalid input domain.'])
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('PASS emitted Thumb encoder',count,'vectors; no ROM integration')
if __name__=='__main__':main()
