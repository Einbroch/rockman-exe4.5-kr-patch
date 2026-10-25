"""Native page/Start/cancel and confirmation-list comparison CPU evidence.

No new handler or product changes. Services sound/page transfer/dialog/cursor
refresh are modeled; actual input handler, count and comparator execute ROM.
"""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';profile=read(ROOT/'project.json')['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(play,identity);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    regions=[];ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for a,b in [(0x35038,0x35086),(0x353B0,0x35582),(0x35620,0x3562C)]:
        data=rom[a:b]
        if current[a:b]!=data:raise ValueError('control source/current body drift')
        ins=list(cs.disasm(data,0x08000000+a))
        if sum(i.size for i in ins)!=len(data):raise ValueError('bounded code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800) or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('control ARMv4T roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(data)))
    ed,glob,keys,sp,stop=0x0200FC40,0x02000200,0x02000300,0x03007F00,0x0FF00000
    stats=dict(comparator_calls=0,command_calls=0,page_transitions=0,confirmation_requests=0,cancel_exits=0)
    evidence=[];lists=[]
    for variant,image in [('source',rom),('current',current)]:
        pool=struct.unpack_from('<I',image,0x353A8)[0];offset=pool-0x08000000
        if not 0<=offset<=len(image)-14:raise ValueError('comparison pool bounds')
        start=offset+struct.unpack_from('<H',image,offset+12)[0]
        terminator=image.find(b'\xE5',start,start+4096)
        if terminator<0:raise ValueError('bounded comparison list terminator')
        data=image[start:terminator+1];entries=data[:-1].split(b'\xE8')
        if not entries or any(len(e)>31 for e in entries):raise ValueError('comparison fixture flat32 bound')
        lists.append(dict(variant=variant,pool=hex(pool),start=hex(0x08000000+start),bytes=len(data),sha256=sha(data),entry_count=len(entries),entry_lengths=[len(e) for e in entries]))
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        size=(len(image)+4095)&~4095;u.mem_map(0x08000000,size);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(stop,4096)
        writes=[];services=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
        def service(cpu,pc,size,user):
            if pc==0x08000534:services.append(('sound',cpu.reg_read(UC_ARM_REG_R0)))
            elif pc==0x080356D0:services.append(('page_transfer',bytes(cpu.mem_read(ed+8,1))[0]))
            elif pc==0x08035086:services.append(('cursor_refresh',cpu.reg_read(UC_ARM_REG_R0)))
            elif pc==0x080322CC:services.append(('dialog',cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)))
            else:return
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        u.hook_add(UC_HOOK_CODE,service)
        regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
        def call(pc):
            u.mem_write(sp-28,b'\x5A'*28);u.reg_write(UC_ARM_REG_CPSR,0x30)
            saved=[ed if r==UC_ARM_REG_R5 else glob if r==UC_ARM_REG_R10 else 0x13579000+i for i,r in enumerate(regs)]
            for r,v in zip(regs,saved):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();services.clear();u.emu_start(pc|1,stop,count=40000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-28,4))!=b'\x5A'*4:raise ValueError('native control ABI/stack24')
            return u.reg_read(UC_ARM_REG_R0),bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)
        def setup(flat,mask=0,col=0,row=0,page=0,cancel_flag=1):
            u.mem_write(0x02000000,b'\xA7'*0x40000);state=bytearray(96);state[0]=12;state[4]=4;state[6:9]=bytes([col,row,page]);state[10]=1;state[14]=cancel_flag
            for at in (16,20,24):struct.pack_into('<I',state,at,ed+32)
            struct.pack_into('<I',state,28,0x020010A6);state[64:64+len(flat)]=flat
            u.mem_write(ed,bytes(state));u.mem_write(glob+4,struct.pack('<I',keys));u.mem_write(keys+2,struct.pack('<H',mask))
            return bytearray(u.mem_read(0x02000000,0x40000))
        # Exact raw entries and zero-interspersed variants execute comparator.
        positives=[]
        for entry in entries:
            if b'\0' in entry or b'\x98' in entry:continue
            for flat in (entry+b'\xE5',b'\0'.join(bytes([v]) for v in entry)+b'\x98'):
                if len(flat)>32:continue
                before=setup(flat);result,z=call(0x08035038)
                if result!=1 or z or bytes(u.mem_read(0x02000000,0x40000))!=before or any(not sp-12<=a and a+n<=sp for a,n in writes):raise ValueError('native positive comparator')
                positives.append(flat);stats['comparator_calls']+=1
        negative=b'\xFF\xE5';before=setup(negative);result,z=call(0x08035038)
        if result!=0 or not z or bytes(u.mem_read(0x02000000,0x40000))!=before:raise ValueError('native negative comparator')
        stats['comparator_calls']+=1
        if not positives:raise ValueError('no bounded positive comparator fixture '+repr(lists[-1])+' '+data.hex())
        for flat,matched in [(negative,False),(positives[0],True)]:
            for page in range(3):
                cases=[(1,15,0),(1,15,1),(1,15,5),(8,0,0),(8,15,5),(0x100,0,0),(0x200,0,0),(0x300,0,0),(0,0,0)]
                for mask,col,row in cases:
                    before=setup(flat,mask,col,row,page);expected=bytearray(before);services_expected=[];s=ed-0x02000000
                    if mask==1 and row in (0,1):
                        nextpage=(1 if page==0 else 0) if row==0 else (1 if page==2 else 2)
                        expected[s+8]=nextpage;services_expected=[('sound',466),('page_transfer',nextpage)];stats['page_transitions']+=1
                    elif mask&(0x100|0x200):
                        nextpage=(page-1)%3 if mask&0x200 else (page+1)%3
                        expected[s+8]=nextpage;services_expected=[('page_transfer',nextpage),('sound',466),('cursor_refresh',0)];stats['page_transitions']+=1
                    elif mask in (1,8) and col==15 and row==5:
                        expected[s:s+2]=bytes([16,4 if matched else 0]);services_expected=[('sound',105 if matched else 467),('dialog',11 if matched else 10,4 if matched else 0)];stats['confirmation_requests']+=1
                    elif mask==8:
                        expected[s+6:s+8]=bytes([15,5]);services_expected=[('sound',466)]
                    result,z=call(0x080353B0)
                    if result!=int(mask!=0) or z!=(mask==0) or services!=services_expected or bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError(f'command result {variant} {mask} {row} {page} {services}')
                    if any(not(sp-24<=a and a+n<=sp or ed<=a and a+n<=ed+16) for a,n in writes):raise ValueError('native command write intervals')
                    stats['command_calls']+=1
                    if variant=='source' and not matched:evidence.append(dict(mask=hex(mask),column=col,row=row,page_before=page,page_after=expected[s+8],state_after=expected[s],substate_after=expected[s+1],services=services_expected))
        for flag in (1,2):
            before=setup(negative,2,cancel_flag=flag);expected=bytearray(before)
            if flag==1:expected[ed-0x02000000]=20;expected[ed+10-0x02000000]=0;expected[ed+14-0x02000000]=2
            result,z=call(0x080353B0)
            if bytes(u.mem_read(0x02000000,0x40000))!=expected or services!=([('sound',127)] if flag==1 else []) or (result,z)!=((1,False) if flag==1 else (2,True)):raise ValueError('empty B cancellation semantics')
            stats['command_calls']+=1;stats['cancel_exits']+=flag==1
    report=dict(id='exe45.hangul-keyboard.control-routes.v1',passed=True,rom_integrated=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,native_code=regions,comparison_lists=lists,command_evidence=evidence,
        tools={'analyze_keyboard_control_routes.py':sha((ROOT/'tools/analyze_keyboard_control_routes.py').read_bytes())},
        limits=['Original handler/count/comparator CPU execution source/current; sound/page upload/cursor refresh/dialog services modeled. No full outer frame or natural game route.',
                'Comparator list is raw-byte E8-separated/E5-terminated; input0 bytes skipped,98/E5 stop input. Positive and negative fixtures verified, not full user-string membership or Korean policy adoption.',
                'Start first selects col15,row5; second press requests dialog. Matching list ->script11/substate4, nonmatch->script10/substate0. Exact native list content, not a presumed blacklist/content judgment.',
                'Empty B exits once with state14/callerValue0/cancelFlag2; repeated flag2 returnsr0=2/Z=1. Layout+10 preservation and flags matter.',
                'Page index controls3 states; original page assets are not proven Korean/Latin selector mappings. No new page/confirm/cancel hook, actual Korean pixels or save/reload.'])
    (base/'control_routes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS native page/Start/cancel/comparison control routes',stats,lists,flush=True)

if __name__=='__main__':main()
