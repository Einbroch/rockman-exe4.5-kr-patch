"""Emitted Thumb candidate-record decoder; standalone fixture, NOT ROM hook.

ABI r0=readable source(2*r1+2 bytes), r1=logical limit1..8,
r2=writable output(r3 bytes), r3=output capacity. Valid source/dest memory is
caller-owned; overlap is rejected. r0=output bytes including E5 or0 on reject.
Reject does not write output; callee registers/SP preserved. Flags unspecified.
"""
import json,sys
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha
from extended_dialogue import assemble_verified
from hangul_record_candidate import pack,unpack,display_bytes
sys.path.insert(0,str(ROOT/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *

CODE='''push {r4, r5, r6, r7, lr}
movs r4, r0
movs r5, r2
movs r6, r1
cmp r6, #1
blo reject
cmp r6, #8
bhi reject
ldrb r7, [r4]
subs r7, #128
cmp r7, #1
blo reject
cmp r7, r6
bhi reject
movs r0, r7
lsls r0, r0, #2
adds r0, #1
cmp r3, r0
blo reject
adds r2, r5, r0
bcs reject
movs r1, r6
lsls r1, r1, #1
adds r1, #2
adds r1, r1, r4
bcs reject
cmp r5, r1
bhs disjoint
cmp r2, r4
bls disjoint
b reject
disjoint:
movs r3, #0
adds r1, r4, #1
validate:
ldrb r0, [r1, #1]
lsls r0, r0, #8
ldrb r2, [r1]
orrs r2, r0
cmp r3, r7
bhs empty
movs r0, #43
lsls r0, r0, #8
adds r0, #164
cmp r2, r0
bhs reject
b next
empty:
movs r0, #255
lsls r0, r0, #8
adds r0, #255
cmp r2, r0
bne reject
next:
adds r1, #2
adds r3, #1
cmp r3, r6
blo validate
ldrb r0, [r1]
cmp r0, #229
bne reject
adds r1, r4, #1
movs r2, r5
movs r3, #0
emit:
movs r0, #249
strb r0, [r2]
movs r0, #252
strb r0, [r2, #1]
ldrb r0, [r1]
strb r0, [r2, #2]
ldrb r0, [r1, #1]
strb r0, [r2, #3]
adds r1, #2
adds r2, #4
adds r3, #1
cmp r3, r7
blo emit
movs r0, #229
strb r0, [r2]
movs r0, r7
lsls r0, r0, #2
adds r0, #1
pop {r4, r5, r6, r7, pc}
reject:
movs r0, #0
pop {r4, r5, r6, r7, pc}
'''

def main():
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    address=0x08000000;blob,isa=assemble_verified(CODE,address,{})
    allowed={'push','movs','cmp','blo','bhi','ldrb','subs','lsls','adds','bcs','bhs','bls','b','orrs','bne','strb','pop'}
    if any(i['mnemonic'] not in allowed or len(bytes.fromhex(i['hex']))!=2 for i in isa['instructions']):raise ValueError('Thumb-1 boundary')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(address,4096);u.mem_write(address,blob);u.mem_map(0x02000000,4096);u.mem_map(0x03007000,4096);u.mem_map(0x0ff00000,4096)
    src=0x02000101;dest=0x02000201;sp=0x03007f00;stop=0x0ff00000
    valid=invalid=0
    def run(record,limit,capacity,expected,output=dest):
        nonlocal valid,invalid
        u.mem_write(0x02000100,b'\xa7'*512);u.mem_write(src,record)
        before=bytes(u.mem_read(0x02000100,512))
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for reg,value in [(UC_ARM_REG_R0,src),(UC_ARM_REG_R1,limit),(UC_ARM_REG_R2,output),(UC_ARM_REG_R3,capacity),(UC_ARM_REG_SP,sp),(UC_ARM_REG_LR,stop|1)]:u.reg_write(reg,value)
        preserved=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
        for n,reg in enumerate(preserved):u.reg_write(reg,0x13579000+n)
        u.emu_start(address|1,stop,count=1000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_R0)!=(len(expected) if expected else 0):raise ValueError('return contract')
        if any(u.reg_read(reg)!=0x13579000+n for n,reg in enumerate(preserved)):raise ValueError('callee register')
        after=bytearray(before)
        if expected:after[output-0x02000100:output-0x02000100+len(expected)]=expected
        if bytes(u.mem_read(0x02000100,512))!=bytes(after):raise ValueError('output bounds/source/reject effects')
        if expected:valid+=1
        else:invalid+=1
    # Complete repertoire in every slot for both observed small fields and the
    # table's eight-character candidate maximum; other widths boundary samples.
    for limit in [4,8]:
        for slot in range(limit):
            for index in range(11172):
                text='가'*slot+chr(0xac00+index)+'힣'*(limit-slot-1);record=pack(text,limit)
                if unpack(record,limit)!=text:raise ValueError('host roundtrip')
                run(record,limit,4*limit+1,display_bytes(record,limit))
    for limit in range(1,9):
        for count in range(1,limit+1):
            record=pack('힣'*count,limit);expected=display_bytes(record,limit)
            run(record,limit,len(expected),expected)
            run(record,limit,len(expected),expected,output=src+len(record))
            run(record,limit,len(expected)-1,None)
            for offset in [-1,0,1,len(record)-1]:run(record,limit,33,None,output=src+offset)
        good=pack('가',limit)
        for marker in [0,1,0x80,0x80+limit+1,0xff]:run(bytes([marker])+good[1:],limit,33,None)
        for last in [0,0x98,0xe4,0xff]:run(good[:-1]+bytes([last]),limit,33,None)
        for slot in range(limit):
            bad=bytearray(good);bad[1+slot*2:3+slot*2]=b'\xa4\x2b' if slot==0 else b'\x00\x00';run(bytes(bad),limit,33,None)
    for limit in [0,9,0xffffffff]:run(pack('가',1),limit,33,None)
    out=ROOT/'analysis/hangul_keyboard_v1/cpu_record_decoder';out.mkdir(parents=True,exist_ok=True);(out/'helper.bin').write_bytes(blob)
    data=dict(id='exe45.hangul-keyboard.candidate-record-decoder.v1',passed=True,rom_integrated=False,format_adopted=False,valid_vectors=valid,rejected_vectors=invalid,helper_sha256=sha(blob),machine_code=isa,codec_tool_sha256=sha((ROOT/'tools/hangul_record_candidate.py').read_bytes()),tool_sha256=sha(Path(__file__).read_bytes()),limits=['Proposed marker0x81..88 has not been proven safe for legacy readers/save consumers.','Readable source and writable declared destination are fixture preconditions, not reserved game RAM.','No native hook/automatic composer installation or real game/save claim.','Full repertoire slots in capacity4/8; other capacity/invalid values are boundary samples.'])
    (out/'report.json').write_text(json.dumps(data,indent=2),encoding='utf8');print('PASS standalone candidate decoder',valid,'valid',invalid,'rejected vectors; NOT ROM integrated')

if __name__=='__main__':main()
