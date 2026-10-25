"""Controlled finite-counter fixtures, distinct from actual036 corpus CPU QA."""
import struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from field_npc_rom_selector_036_v1 import wrap
from extended_dialogue import assemble_verified


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code_at,table,copies,targets=0x080F0000,0x080C0000,0x080D0000,0x08080000
    root,glob,scene_at,stack=0x02039800,0x02000100,0x02000200,0x03007F00
    counts=[1,2,20,254,255];vectors=0;writes=[];isa=[]
    for count in counts:
        code,proof=wrap(source,code_at,0x08001001,table,count)
        end=next(x['address'] for x in proof['proof']['instructions'] if x['mnemonic']=='pop' and 'r0' in x['operands'])
        stub,_=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x0804FB4C,dict(target=code_at+1))
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,0x100000);u.mem_write(0x08000000,source[:0x100000]);u.mem_write(code_at,code);u.mem_write(0x0804FB4C,stub)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        u.mem_write(copies,b''.join(bytes([0x42,i,0,0xA5]) for i in range(count)))
        u.mem_write(glob+64,struct.pack('<I',scene_at))
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=end,end=end)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        for scene in range(256):
            descriptors=b''.join(struct.pack('<4I',targets+i*4,copies+i*4,4,scene) for i in range(count))
            u.mem_write(table,descriptors);u.mem_write(scene_at+4,bytes([scene]))
            cases=[('first',0),('none',None)]+([('last',count-1)] if count>1 else [])
            for kind,index in cases:
                blob=bytes([0x42,index,0,0xA5]) if index is not None else b'\x43\x00\x00\xA5'
                u.mem_write(root-4,b'\xAD'*4+blob+b'\xAD'*4);u.mem_write(stack-64,b'\xCC'*64)
                values=[0x1100+i*0x101 for i in range(15)];values[0]=root;values[1]=0;values[10]=glob;values[13]=stack;values[14]=0x0804F773
                for r,v in zip(REGS,values):u.reg_write(r,v)
                writes.clear();u.emu_start(0x0804FB4D,0,count=20000)
                expected=values[:8];expected[0]=root if index is None else targets+index*4
                if u.reg_read(REGS[13])!=stack-32 or list(struct.unpack('<8I',u.mem_read(stack-32,32)))!=expected:raise ValueError(('036 counter/result/saved register fixture',count,scene,kind))
                if any(not(stack-32<=a and a+n<=stack) for a,n in writes) or bytes(u.mem_read(stack-64,32))!=b'\xCC'*32 or bytes(u.mem_read(root-4,12))!=b'\xAD'*4+blob+b'\xAD'*4:raise ValueError('036 counter fixture memory bounds')
                vectors+=1
        isa.append(dict(count=count,code_sha256=sha(code),proof=proof))
        print('PASS036 counter',count,'all256 scenes',flush=True)
    refused=[]
    for value in [0,-1,256,True,1.5]:
        try:wrap(source,code_at,0x08001001,table,value)
        except ValueError:refused.append(repr(value))
        else:raise ValueError('036 invalid descriptor count accepted')
    arithmetic=0
    for scene in range(256):
        for count in range(1,256):
            r=(scene<<8)+count
            for remaining in range(count,0,-1):
                if r>>8!=scene or r&255!=remaining:raise ValueError('Packed counter domain')
                r-=1;arithmetic+=1
            if r&255:raise ValueError('Packed counter termination')
    result=dict(passed=True,scope='Synthetic counter boundary fixtures, not actual product/runtime evidence',source_sha256=sha(source),CPU_vectors=vectors,all_scene_bytes=256,descriptor_counts=counts,first_last_no_match_cases=True,arithmetic_states_checked=arithmetic,invalid_counts_rejected=refused,isa=isa,tool_sha256=sha((ROOT/'tools/bench_npc_selector_036_boundaries_v1.py').read_bytes()),selector_sha256=sha((ROOT/'tools/field_npc_rom_selector_036_v1.py').read_bytes()),rom_written=False,new_units_applied=0,runtime_tested=False,release_eligible=False,limits=['Four-byte synthetic source records isolate packed counter/control flow and saved low registers; real255-script source/header/caller behavior is covered separately by corpus8423-vector CPU report.','Execution stops before predecessor handoff; full035 reader/ABI regression is a separate corpus test.'])
    frozen_write(ROOT/'analysis/pending_insertion_500_036_selector_cpu_v1/boundaries_v1.json',result)
    print('PASS036 boundary CPU',vectors,'vectors and',arithmetic,'packed states;NO ROM')


if __name__=='__main__':main()
