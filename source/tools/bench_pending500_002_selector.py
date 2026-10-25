"""Four-body selector analysis in synthetic CPU memory; no ROM output."""
import argparse
import json
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from keyitem_rom_selector import construct,INSTALL,EXPECTED,CALLERS
from verify_tpi_index import lz77_decompress
from bench_chip_library import REGS
from prepare_pending_batch500_002 import BASE,BASE_SHA
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--audit',default='analysis/pending_insertion_500_002_capacity_v1/report.json')
    p.add_argument('--out',default='analysis/pending_insertion_500_002_capacity_v1/selector_cpu.json')
    args=p.parse_args()
    out=ROOT/args.out
    if out.exists():raise ValueError('Preserve previous CPU evidence')
    audit_path=ROOT/args.audit
    audit=json.loads(audit_path.read_text(encoding='utf8'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source_path=ROOT/cfg['source_profile']['filename'];require_hash(source_path,audit['source_sha256'])
    source=source_path.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes()
    baseline=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'))
    meta=baseline['keyitem_rom']
    proof=audit['four_body_selector']['proof']
    guards=proof['mission_guards'];hook=proof['hook_address']
    stub,code,current=construct(source,bytes.fromhex(meta['guard_header_hex']),meta['clone_address'],
        hook,meta['rom_bytes'],meta['mail_guard'],guards)
    if current!=proof:raise ValueError('Virtual selector identity drift')
    require_hash(audit_path.parent/'virtual_selector.bin',sha(code))
    raw=(audit_path.parent/'compiled/6E01AC.msg').read_bytes()
    if sha(raw)!=audit['cumulative_destruction']['compiled_sha256']:raise ValueError('Cumulative binding')
    pre_path=ROOT/audit.get('preflight_path','analysis/pending_insertion_500_002_r3/preflight.json')
    shadow_path=pre_path.parent/'6DED88/compiled/6DED88.msg'
    shadow=shadow_path.read_bytes()
    require_hash(pre_path,audit['preflight_sha256'])
    pre=json.loads(pre_path.read_text(encoding='utf8'))
    sr=next(r for r in pre['archives'] if r['archive']=='6DED88')
    if sha(shadow)!=sr['compiled_sha256']:raise ValueError('Shadow binding')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU engine drift')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(hook+len(code)-0x08000000+4095)&~4095)
    u.mem_write(0x08000000,rom)
    u.mem_write(guards[2]['clone_address'],raw);u.mem_write(guards[3]['clone_address'],shadow)
    u.mem_write(hook,code)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    immutable_tail=bytes(u.mem_read(0x08800000,hook+len(code)-0x08800000))
    writes=[];clears=[];ctx=0x0200FA20;glob=0x02000100;stack=0x03007F00;stop=0x0804FB90
    def callback(uc,address,size,user):
        if address==stop:uc.emu_stop()
        elif address==0x0800090C:
            at,n=uc.reg_read(REGS[0]),uc.reg_read(REGS[1])
            if (at,n)!=(ctx,216):raise ValueError('Unexpected native zero-helper contract')
            clears.append((at,n));uc.mem_write(at,bytes(n));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,callback)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,a,at,n,value,user:writes.append((at,n)))
    cases=[]
    def execute(root,script,caller,blob,patched):
        u.mem_write(0x08000000+INSTALL,stub if patched else EXPECTED)
        u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(root,blob);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(ctx,bytes([0xA7])*216)
        u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB))
        u.mem_write(stack-128,bytes([0xCC])*128)
        regs=[0x1000+i*0x101 for i in range(15)]
        regs[0]=root;regs[1]=script;regs[10]=glob;regs[13]=stack;regs[14]=caller
        for r,v in zip(REGS,regs):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
        writes.clear();clears.clear();u.emu_start(0x08000000+INSTALL+1,0,count=1000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('Native continuation')
        if any(not(ctx<=at and at+n<=ctx+216 or stack-64<=at and at+n<=stack) for at,n in writes):raise ValueError('Unexpected memory write')
        if bytes(u.mem_read(root,len(blob)))!=blob:raise ValueError('Native RAM body changed')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    def case(kind,root,script,caller,blob,clone):
        nr,nc,nf=execute(root,script,caller,blob,False)
        pr,pc,pf=execute(root,script,caller,blob,True)
        chosen=clone or root
        offset=int.from_bytes(u.mem_read(chosen+script*2,2),'little')
        expected=nr[:];expected[1]=offset
        context=bytearray(nc)
        for at,v in ((0x30,chosen),(0x2c,chosen+offset),(0x34,chosen+offset)):struct.pack_into('<I',context,at,v)
        if pr!=expected or pc!=bytes(context) or pf!=nf:raise ValueError('ABI/context/flags mismatch '+kind+'/'+str(script))
        cases.append(dict(kind=kind,root=root,script=script,caller=caller,chosen_root=chosen))
    for pointer in range(0x40658,0x4066C,4):
        address=struct.unpack_from('<I',source,pointer)[0]
        blob=lz77_decompress(source,address-0x08000000)[0]
        count=int.from_bytes(blob[:2],'little')//2
        matches=[g for g in guards if g['guard_header_hex']==blob[:16].hex()]
        if len(matches)>1:raise ValueError('Guard collision')
        clone=matches[0]['clone_address'] if matches else None
        for s in range(count):case('selected-body' if clone else 'retained-registration',0x0202B2F4,s,0x0804F7BD,blob,clone)
        for b in range(16):
            changed=bytearray(blob);changed[b]^=1
            for s in (0,count-1):case('changed-header',0x0202B2F4,s,0x0804F7BD,bytes(changed),None)
        for s in (count,127,255):case('out-of-scope',0x0202B2F4,s,0x0804F7BD,blob,None)
        for caller in (0x08012345,0x0804F7BF,0x0803497D):
            for s in (0,count-1):case('wrong-caller',0x0202B2F4,s,caller,blob,None)
        case('wrong-root',0x02038000,0,0x0804F7BD,blob,None)
    bodies={r['archive']:lz77_decompress(rom,r['rom_offset'])[0] for r in baseline['archives'] if r['archive'] in ('709408','6DD9AC')}
    for root,count,callers,blob,clone in [
        (0x0202B2F4,32,(0x0804F7BD,),bodies['6DD9AC'],meta['mail_guard']['clone_address']),
        *[(root,49,callers,bodies['709408'],meta['clone_address']) for root,callers in CALLERS.items()]]:
        for caller in callers:
            for s in range(count):case('retained-common-reader',root,s,caller,blob,clone)
    if bytes(u.mem_read(0x08800000,len(immutable_tail)))!=immutable_tail:raise ValueError('ROM tail changed')
    require_hash(ROOT/BASE,BASE_SHA)
    report=dict(passed=True,scope='synthetic CPU memory only; native216-byte zero helper substituted; NOT integrated ROM/GBA renderer/load/acquisition/save proof',
        baseline_rom_sha256=BASE_SHA,source_sha256=sha(source),capacity_audit_sha256=sha(audit_path.read_bytes()),
        selector_sha256=sha(code),vectors=len(cases),case_counts=dict(Counter(c['kind'] for c in cases)),cases=cases,
        registers_flags_context_passed=True,original_ram_payloads_preserved=True,rom_written=False,rom_applied_units=0,release_eligible=False)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS virtual four-body selector',len(cases),'CPU vectors; no ROM written')


if __name__=='__main__':main()
