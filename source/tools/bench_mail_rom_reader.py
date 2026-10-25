"""Integrated selector ABI CPU bench; not GBA rendering/acquisition evidence."""
import argparse,json,struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import lz77_decompress
from keyitem_rom_selector import INSTALL,EXPECTED,CALLERS
from keyitem_rom_data import verify_final
from bench_chip_library import REGS
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('preserve CPU evidence')
    rp=ROOT/a.rom;m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=ROOT/json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    meta=m['keyitem_rom'];verify_final(native,rom,meta);mail=meta['mail_rom_reader']
    mission_sizes={g['clone_address']:g['payload_bytes'] for g in meta.get('mission_guards') or []}
    mission_sizes.update({g['clone_address']:g['payload_bytes'] for g in meta.get('equipment_guards') or []})
    bodies={x['archive']:lz77_decompress(rom,x['rom_offset'])[0] for x in m['archives'] if x['archive'] in ('6DD9AC','709408')}
    roots={0x0202B2F4:(bodies['6DD9AC'],mail['clone_address'],32,(0x0804F7BD,)),
           **{root:(bodies['709408'],0x08000000+meta['rom_offset'],49,callers) for root,callers in CALLERS.items()}}
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version drift')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx=0x0200FA20;glob=0x02000100;stack=0x03007F00;stop=0x0804FB90;writes=[];clears=[];cases=[]
    def callback(uc,address,size,user):
        if address==stop:uc.emu_stop()
        elif address==0x0800090C:
            at=uc.reg_read(REGS[0]);n=uc.reg_read(REGS[1]);clears.append((at,n))
            if (at,n)!=(ctx,216):raise ValueError('native zero-helper contract')
            uc.mem_write(at,bytes(n));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,callback)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,at,n,value,user:writes.append((at,n)))
    stub=rom[INSTALL:INSTALL+12]
    def execute(root,script,caller,blob,patched,navi=255):
        u.mem_write(0x08000000+INSTALL,stub if patched else EXPECTED);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(root,blob);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(ctx,bytes([0xA7])*216)
        u.mem_write(glob+64,struct.pack('<I',0x02000200));u.mem_write(0x02000201,bytes([navi]))
        u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-128,bytes([0xCC])*128)
        regs=[0x1000+i*0x101 for i in range(15)];regs[0]=root;regs[1]=script;regs[10]=glob;regs[13]=stack;regs[14]=caller
        for r,v in zip(REGS,regs):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();u.emu_start(0x08000000+INSTALL+1,0,count=1000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('native continuation')
        if any(not(ctx<=at and at+n<=ctx+216 or stack-64<=at and at+n<=stack) for at,n in writes):raise ValueError('write escaped native context/stack')
        if bytes(u.mem_read(root,len(blob)))!=blob:raise ValueError('text RAM mutated')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    def case(kind,root,script,caller,blob,clone,navi=255):
        nr,nc,nf=execute(root,script,caller,blob,False,navi);pr,pc,pf=execute(root,script,caller,blob,True,navi)
        chosen=clone or root
        payload=bytes(u.mem_read(clone,mission_sizes.get(clone,mail['payload_bytes'] if root==0x0202B2F4 else meta['rom_bytes']))) if clone else blob
        offset=struct.unpack_from('<H',payload,script*2)[0];expected=nr[:];expected[1]=offset
        context=bytearray(nc)
        for at,value in ((0x30,chosen),(0x2c,chosen+offset),(0x34,chosen+offset)):struct.pack_into('<I',context,at,value)
        if pr!=expected or pc!=bytes(context) or pf!=nf:raise ValueError(f'ABI/context/flags: {kind}/{script}/{caller:08X}')
        cases.append(dict(kind=kind,root=root,script=script,caller=caller,chosen_root=chosen,stream=chosen+offset))
    if meta.get('equipment_guards'):
        selected_gear={g['navi_index']:g for g in meta['equipment_guards']}
        for index in range(23):
            address=struct.unpack_from('<I',native,0x3C5BC+index*4)[0]
            blob=lz77_decompress(native,address-0x08000000)[0]
            g=selected_gear.get(index)
            for script in range(76):
                translated=g is not None and script in (60,61,62,70,71,72,73,74,75)
                case('gear-selected-normal' if translated else 'gear-retained-native',0x0202BA7C,script,0x0804F7BD,blob,g['clone_address'] if translated else None,index)
            if g:
                for byte in list(range(16))+list(range(136,152)):
                    modified=bytearray(blob);modified[byte]^=1
                    for script in (60,70,75):case('gear-changed-table-guard',0x0202BA7C,script,0x0804F7BD,bytes(modified),None,index)
                for script in (76,127,255,256,257):case('gear-out-of-range',0x0202BA7C,script,0x0804F7BD,blob,None,index)
                for caller in (0x08012345,0x0804F7BF,0x0803497D):
                    for script in (60,70,75):case('gear-wrong-caller',0x0202BA7C,script,caller,blob,None,index)
                for bad_index in (0,1,8,255):
                    for script in (60,70,75):case('gear-wrong-navi',0x0202BA7C,script,0x0804F7BD,blob,None,bad_index)
                for script in (60,70,75):case('gear-wrong-root',0x02038000,script,0x0804F7BD,blob,None,index)
    for root,(blob,clone,count,callers) in roots.items():
        for caller in callers:
            for s in range(count):case('known-mail' if root==0x0202B2F4 else 'retained-keyitem',root,s,caller,blob,clone)
            for b in range(16):
                changed=bytearray(blob);changed[b]^=1
                for s in (0,count-1):case('changed-header',root,s,caller,bytes(changed),None)
            for s in (count,127,255):case('out-of-scope-script',root,s,caller,blob,None)
            if root!=0x0202B2F4:
                alternate=lz77_decompress(native,0x709704)[0]
                for s in range(45):case('alternate-keyitem-archive',root,s,caller,alternate,None)
        for caller in (0x08012345,0x0804F7BF,0x0803497D):
            for s in (0,count-1):case('unknown-caller',root,s,caller,blob,None)
    case('unknown-root',0x02038000,0,0x0804F7BD,bodies['6DD9AC'],None)
    # The same loader/consumer selects five other archives for extended Navi IDs.
    # Their first offset is not64, so they must never select the mail clone.
    alternate_mail=[]
    for at in range(0x40658,0x4066C,4):
        address=struct.unpack_from('<I',native,at)[0];blob=lz77_decompress(native,address-0x08000000)[0]
        count=int.from_bytes(blob[:2],'little')//2
        if blob[:16]==bytes.fromhex(mail['guard_header_hex']):raise ValueError('alternate mail guard collision')
        alternate_mail.append(dict(pointer=at,address=address,script_count=count,guard_distinct=True))
        guards=[g for g in meta.get('mission_guards') or [] if bytes.fromhex(g['guard_header_hex'])==blob[:16]]
        if len(guards)>1:raise ValueError('mission guard collision')
        clone=guards[0]['clone_address'] if guards else None
        for s in range(count):case('selected-mission' if clone else 'alternate-mail-archive',0x0202B2F4,s,0x0804F7BD,blob,clone)
        if clone:
            for b in range(16):
                changed=bytearray(blob);changed[b]^=1
                for s in (0,count-1):case('changed-mission-header',0x0202B2F4,s,0x0804F7BD,bytes(changed),None)
            for s in (count,127,255):case('out-of-scope-mission',0x0202B2F4,s,0x0804F7BD,blob,None)
            for caller in (0x08012345,0x0804F7BF,0x0803497D):
                for s in (0,count-1):case('unknown-mission-caller',0x0202B2F4,s,caller,blob,None)
    # The full appended tail is read-only in all trials, including both clones/code.
    if bytes(u.mem_read(0x08000000+len(native),len(rom)-len(native)))!=rom[len(native):]:raise ValueError('ROM tail mutated')
    result=dict(passed=True,rom_sha256=sha(rom),source_sha256=sha(native),vectors=len(cases),case_counts=dict(Counter(c['kind'] for c in cases)),cases=cases,alternate_mail_archives=alternate_mail,scope='Synthetic CPU ABI bench; native216-byte zero helper substituted; NOT GBA runtime or acquisition proof',native_registers_flags_context_preserved_except_declared_rom_root=True,no_new_persistent_ram=True)
    out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS composed mail/keyitem selector ABI',len(cases),'vectors')

if __name__=='__main__':main()
