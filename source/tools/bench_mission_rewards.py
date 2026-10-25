"""Execute native EE38/684B0 with every catalog reward and HP-owned branch."""
import argparse,json,struct
from build_visibility_poc import ROOT,require_hash,sha
from mission_reward_model import model
from bench_chip_library import REGS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('preserve bench evidence')
    rp=ROOT/a.rom;m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();proof=model(source)
    for r in proof['producer_ranges']:
        if rom[r['start']:r['end']]!=source[r['start']:r['end']]:raise ValueError('native reward code/table modified')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx=0x0200FA20;cmd=0x02038000;stack=0x03007F00;stop=0x08050000;branches=[];writes=[];owned=False
    def hook(uc,at,n,user):
        if at==stop:uc.emu_stop()
        elif at==0x08000FC2:
            flags=uc.reg_read(UC_ARM_REG_CPSR);flags=(flags&~(1<<30)) if owned else (flags|(1<<30));uc.reg_write(UC_ARM_REG_CPSR,flags);uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
        elif at==0x0804FD18:
            branches.append(uc.reg_read(REGS[1]));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,acc,at,n,value,user:writes.append((at,n)))
    cases=[]
    for row in proof['catalog']:
        for reward in row['rewards']:
            for owned in ([False,True] if reward['kind']==1 else [False]):
                state=bytearray(20);state[7]=reward['kind'];struct.pack_into('<H',state,18,reward['amount']);u.mem_write(0x02000000,bytes(state));u.mem_write(ctx,bytes(216));u.mem_write(cmd,bytes.fromhex('ee38ff1d1e'));u.mem_write(stack-64,bytes(64))
                for i,r in enumerate(REGS):u.reg_write(r,0x1000+i)
                u.reg_write(REGS[4],cmd);u.reg_write(REGS[5],ctx);u.reg_write(REGS[13],stack);u.reg_write(REGS[14],stop|1);u.reg_write(UC_ARM_REG_CPSR,0x33);branches.clear();writes.clear();u.emu_start(0x08050ED5,0,count=200)
                expected=1000 if owned else reward['amount'];kind=2 if owned else reward['kind'];target=[] if kind==1 else [29 if kind==2 else 30]
                if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[0])!=1 or u.reg_read(REGS[13])!=stack or int.from_bytes(u.mem_read(ctx+84,4),'little')!=expected or branches!=target or bytes(u.mem_read(0x02000000,20))!=state:raise ValueError(f'native reward amount/branch/ABI: {reward},owned={owned},pc={u.reg_read(UC_ARM_REG_PC):08X},r0={u.reg_read(REGS[0])},sp={u.reg_read(REGS[13]):08X},buffer={int.from_bytes(u.mem_read(ctx+84,4),"little")},branches={branches}')
                if any(not (at==ctx+84 and n==4 or stack-32<=at and at+n<=stack) for at,n in writes):raise ValueError('native reward write escaped context/stack')
                cases.append(dict(group=row['group'],mission=row['mission'],input=reward,hp_already_owned=owned,buffer3=expected,branch=target))
    result=dict(passed=True,rom_sha256=sha(rom),vectors=len(cases),model=proof,cases=cases,scope='Synthetic native EE38 and reward-state reader execution. HP-ownership flag query and script-jump destination substituted; not acquisition, GBA rendering or grant/save proof.')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS native mission reward amounts/branches',len(cases),'vectors')

if __name__=='__main__':main()
