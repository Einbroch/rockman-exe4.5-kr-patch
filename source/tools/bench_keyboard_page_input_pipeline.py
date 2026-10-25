"""Raw pressed keys -> control/edit -> native page upload/draw/drain CPU.

No installed hooks, VBlank or natural input. BIOS, sound/config/sprite calls
are modeled; page uploader/queue/map writers execute original machine code.
"""
import argparse,json,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import assemble_verified,Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB
from hangul_keyboard_control_shim import CODE,QUEUE_GUARD
from hangul_keyboard_raw_router import assemble as raw_assemble
from hangul_mixed_editor_init import initialize
from hangul_mixed_replay_state import MixedReplay,KEYS,apply
from prepare_keyboard_page_graphics import decode
from hangul_keyboard_refresh import assemble as refresh_assemble
from hangul_mixed_cache_bridge import stream
from hangul_native_tokens import to_native_word


def main(editfield=False,frame=False,kana=False,labels=False,latin=False):
    if frame and not editfield:raise ValueError('frame requires editfield')
    if kana and not frame:raise ValueError('kana replacement requires full frame/editfield')
    if labels and not kana:raise ValueError('labels require kana/frame/editfield')
    if latin and not labels:raise ValueError('Latin input requires labels/kana/frame/editfield')
    jamo_pages=(0,1) if kana else (0,)
    base=ROOT/'analysis/hangul_keyboard_v1';out=base/('cpu_latin_input' if latin else 'cpu_keyboard_labels' if labels else 'cpu_kana_frame' if kana else 'cpu_keyboard_frame' if frame else 'cpu_input_render_pipeline' if editfield else 'cpu_page_input_pipeline');out.mkdir(exist_ok=True)
    names=['cpu_keyboard_controls','cpu_keyboard_actions','cpu_composer','cpu_commit_bridge','cpu_page_graphics','page_graphics']
    if editfield:names+=['cpu_cache_pipeline','cpu_cache_bridge','cpu_editfield_parser']
    if kana:names+=['kana_replacement','cpu_kana_replacement']
    if labels:names+=['keyboard_labels']
    if latin:names+=['latin_input']
    deps={};reports={}
    for name in names:
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        reports[name]=d;deps[name+'/report.json']=sha(p.read_bytes())
    if not reports['cpu_keyboard_controls']['page_upload_queue_guard']:raise ValueError('guard prerequisite')
    require_hash(base/'page_graphics/report.json',reports['cpu_page_graphics']['asset_report_sha256'])
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=reports['page_graphics']['current_rom_sha256'];require_hash(play,identity);rom=play.read_bytes()
    glyph_identity=None;manifest=None
    if editfield:
        product=ROOT/'poc/output/exe45_ko_development_keyboard_glyphs_v1.gba';glyph_identity=reports['cpu_cache_pipeline']['product_sha256'];require_hash(product,glyph_identity);rom=product.read_bytes()
        manifest=read(product.with_suffix('.json'));require_hash(product.with_suffix('.json'),reports['cpu_editfield_parser']['manifest_sha256'])
        if sha(rom[0x1EE700:0x1EFF74])!=reports['cpu_editfield_parser']['overlay_origin']['sha256']:raise ValueError('glyph overlay origin')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    native=reports['cpu_page_graphics']['native_code']
    for r in native:
        a=r['offset'];b=a+r['bytes']
        if original[a:b]!=rom[a:b] or sha(rom[a:b])!=r['sha256']:raise ValueError('native code guard')
    site=reports['cpu_keyboard_actions']['native_caller'];pc=0x08000000+site['offset']
    raw_blob,raw_isa=raw_assemble()
    raw_path=base/'cpu_keyboard_raw_router/helper.bin'
    require_hash(raw_path,sha(raw_blob))
    if rom[site['offset']:site['offset']+6].hex()!=site['expected_hex']:raise ValueError('raw caller guard')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x8304000',pc)[0])
    ins=list(cs.disasm(patch,pc))
    if len(ins)!=1 or ins[0].mnemonic!='bl' or ins[0].op_str!='#0x8304000' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x8304000',pc)[0])!=patch:raise ValueError('placed BL profile')
    clone=bytearray(rom);fixture=[]
    bank=(base/'page_graphics/jamo_page0_tiles.bin').read_bytes();mapping=(base/'page_graphics/jamo_page0_map.bin').read_bytes()
    if labels:
        bank=(base/'keyboard_labels/page0_tiles.bin').read_bytes();mapping=(base/'keyboard_labels/page0_map.bin').read_bytes()
    for at,new in [(site['offset'],patch),(0x356C0,struct.pack('<I',0x09402000)),(0x356E8,struct.pack('<3I',0x09400000,0x06008000,len(bank)))]:
        fixture.append(dict(offset=at,expected_hex=rom[at:at+len(new)].hex(),final_hex=new.hex()));clone[at:at+len(new)]=new
    bank1=mapping1=None
    if kana:
        bank0=(base/'kana_replacement/page0_tiles.bin').read_bytes();map0=(base/'kana_replacement/page0_map.bin').read_bytes()
        if not labels and (bank0!=bank or map0!=mapping):raise ValueError('page0 candidate byte-equivalence')
        folder=base/('keyboard_labels' if labels else 'kana_replacement')
        bank1=(folder/'page1_tiles.bin').read_bytes();mapping1=(folder/'page1_map.bin').read_bytes()
        if len(bank1)>0x2000 or len(bank1)%32:raise ValueError('page1 fixture tile/map disjoint extent')
        for at,new in [(0x356C4,struct.pack('<I',0x09405000)),(0x356F8,struct.pack('<3I',0x09403000,0x06008000,len(bank1)))]:
            fixture.append(dict(offset=at,expected_hex=rom[at:at+len(new)].hex(),final_hex=new.hex()));clone[at:at+len(new)]=new
    bank2=mapping2=None
    if labels:
        bank2=(base/'keyboard_labels/page2_tiles.bin').read_bytes();mapping2=(base/'keyboard_labels/page2_map.bin').read_bytes()
        if len(bank2)>0x2000 or len(bank2)%32:raise ValueError('page2 fixture tile/map extent')
        for at,new in [(0x356C8,struct.pack('<I',0x09408000)),(0x35708,struct.pack('<3I',0x09406000,0x06008000,len(bank2)))]:
            fixture.append(dict(offset=at,expected_hex=rom[at:at+len(new)].hex(),final_hex=new.hex()));clone[at:at+len(new)]=new
    frame_blobs=[];frame_scopes=[]
    if frame:
        from hangul_keyboard_frame_adapters import assemble as frame_assemble
        if kana:from hangul_keyboard_kana_frame import assemble as frame_assemble
        frame_blobs=frame_assemble()
        for a,b in [(0x34E34,0x34E62),(0x34EFE,0x34F68),(0x35086,0x350D2),(0x35344,0x35376),(0x3564E,0x35664),(0x34C54,0x34CC0),(0x34D1E,0x34D36)]:
            data=original[a:b];decoded=list(cs.disasm(data,0x08000000+a))
            if rom[a:b]!=data or sum(i.size for i in decoded)!=len(data):raise ValueError('frame native scope')
            for i in decoded:
                if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('frame Thumb1 profile')
                if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('frame instruction roundtrip')
            frame_scopes.append(dict(offset=a,bytes=b-a,sha256=sha(data)))
        for at,target in [(0x34E48,0x08305100),(0x34E4C,0x08305100),(0x34E50,0x08305000),(0x35350,0x08305200),(0x34F5C,0x08305300)]:
            new=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl '+hex(target),0x08000000+at)[0]);ins=list(cs.disasm(new,0x08000000+at))
            if len(ins)!=1 or ins[0].mnemonic!='bl' or int(ins[0].op_str[1:],16)!=target:raise ValueError('frame final BL')
            fixture.append(dict(offset=at,expected_hex=rom[at:at+4].hex(),final_hex=new.hex()));clone[at:at+4]=new
    # Controlled unguarded variant reproduces the full-queue bug, not a game
    # release artifact. Both variants use the verified Thumb1 assembler path.
    if CODE.count(QUEUE_GUARD)!=1:raise ValueError('guard removal extent')
    old,old_isa=assemble_verified(CODE.replace(QUEUE_GUARD,''),0x08F10000,dict(editor=0x0200FC40,page=0x080356D1,sound=0x08000535,dialog=0x080322CD,table=0x09000000,query=0x08F11001,commit=0x08F06001,queue_count=0x02010724))
    (out/'unguarded_control.bin').write_bytes(old)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    size=(len(clone)+4095)&~4095;u.mem_map(0x08000000,size);u.mem_write(0x08000000,bytes(clone))
    for at,path in [(0x08304000,'cpu_keyboard_raw_router/helper.bin'),(0x08303000,'latin_input/shim.bin' if latin else 'keyboard_labels/shim.bin' if labels else 'kana_replacement/shim.bin' if kana else 'cpu_keyboard_actions/shim.bin')]:u.mem_write(at,(base/path).read_bytes())
    for at,b,info,name in frame_blobs:u.mem_write(at,b);(out/name).write_bytes(b)
    u.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
    helpers=[(0x08F0D000,'cpu_keyboard_actions/dispatch.bin'),(0x08F0E000,'cpu_keyboard_actions/keyedit.bin'),(0x08F0F000,'cpu_keyboard_actions/rebase.bin'),(0x08F10000,'cpu_keyboard_controls/helper.bin'),(0x08F11000,'cpu_keyboard_controls/query.bin'),(0x08F06000,'cpu_commit_bridge/helper.bin')]
    for at,path in helpers:u.mem_map(at,4096);u.mem_write(at,(base/path).read_bytes());u.mem_protect(at,4096,UC_PROT_READ|UC_PROT_EXEC)
    refresh_info=None
    if editfield:
        helper,guard,helper_isa,guard_isa=refresh_assemble();refresh_info=dict(helper=helper_isa,guard=guard_isa)
        for at,b,name in [(0x08F12000,helper,'refresh.bin'),(0x08F13000,guard,'guard.bin')]:
            (out/name).write_bytes(b);u.mem_map(at,4096);u.mem_write(at,b);u.mem_protect(at,4096,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x08F01000,4096);u.mem_write(0x08F01000,(base/'cpu_cache_bridge/helper.bin').read_bytes());u.mem_protect(0x08F01000,4096,UC_PROT_READ|UC_PROT_EXEC)
    for at,name in [(0x09000000,'transitions.bin'),(0x09200000,'deletions.bin')]:
        b=(base/'cpu_composer'/name).read_bytes();size=(len(b)+4095)&~4095;u.mem_map(at,size);u.mem_write(at,b);u.mem_protect(at,size,UC_PROT_READ)
    selectors=(base/'cpu_keyboard_actions/selectors.bin').read_bytes();u.mem_map(0x09300000,8192);u.mem_write(0x09300000,struct.pack('<4I',0x09000000,0x09200000,0x08F0E001,0x08F0F001));u.mem_write(0x09301000,selectors)
    if latin:u.mem_write(0x09301100,(base/'latin_input/selectors.bin').read_bytes())
    u.mem_protect(0x09300000,8192,UC_PROT_READ)
    u.mem_map(0x09400000,0x3000);u.mem_write(0x09400000,bank);u.mem_write(0x09402000,mapping);u.mem_protect(0x09400000,0x3000,UC_PROT_READ)
    if kana:
        u.mem_map(0x09403000,0x3000);u.mem_write(0x09403000,bank1);u.mem_write(0x09405000,mapping1);u.mem_protect(0x09403000,0x3000,UC_PROT_READ)
    if labels:
        u.mem_map(0x09406000,0x3000);u.mem_write(0x09406000,bank2);u.mem_write(0x09408000,mapping2);u.mem_protect(0x09406000,0x3000,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_write(0x03005800,rom[0x1EE700:0x1EFF74]);u.mem_protect(0x03005000,0x2000,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x06000000,0x20000);u.mem_map(0x0FF00000,4096)
    ed,glob,keys,maps,sp,stop=0x0200FC40,0x02000200,0x02000300,0x02018000,0x03007F00,0x0FF00000
    counter,queue=0x02010724,0x02012730;regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];sounds=[];bios=[];sprite_calls=[];frame_calls=[];end_pc=[stop]
    executed=[0];instruction_max={};instruction_cap=100000
    u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def service(cpu,at,n,user):
        executed[0]+=1
        # Reused native-frame translation blocks can include the old bounded
        # caller's POP. Stop before the requested boundary, not after it.
        if at==end_pc[0]:cpu.emu_stop();return
        if at==0x08000534:sounds.append(cpu.reg_read(UC_ARM_REG_R0))
        elif at in (0x0803438A,0x08034364):pass
        elif at==0x08029538:sprite_calls.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)))
        elif at==0x080EC140:
            src,dst,words=[cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2)]
            if dst not in ((0x06008000,0x0600B000) if editfield else (0x06008000,)) or words%8 or words*4>0x3000:raise ValueError('BIOS request')
            bios.append((src,dst,words*4));cpu.mem_write(dst,bytes(cpu.mem_read(src,words*4)));cpu.reg_write(UC_ARM_REG_PC,0x080EC143);return
        else:
            if frame and at in (0x08034EFE,0x08305100,0x08305000,0x08F12000,0x08305200):frame_calls.append(at)
            return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,service)
    stats=dict(input_calls=0,page_transitions=0,draws=0,drains=0,jamo_actions=0,backspaces=0,queue_rejections=0,unguarded_mismatch_reproduced=0,pending_transitions=0)
    if editfield:stats['caret_actions']=0
    if frame:stats.update(native_frames=0,navigation_cases=0,caret_sprite_cases=0,idle_retry_frames=0)
    if labels:stats.update(space_actions=0,space_boundary_cases=0,space_partial_cases=0)
    if latin:stats.update(latin_actions=0,latin_cell_cases=0,latin_boundary_cases=0,latin_partial_cases=0)
    render_stats=dict(refresh_calls=0,queued=0,deferred=0,latest_after_drain=0)
    pending_pixels=[None];dirty=[False]
    def call(start,end=stop,stack=220):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved=[ed if r==UC_ARM_REG_R5 else glob if r==UC_ARM_REG_R10 else 0x13579000+i for i,r in enumerate(regs)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();sounds.clear();sprite_calls.clear();frame_calls.clear()
        end_pc[0]=end;executed[0]=0
        try:u.emu_start(start|1,end,count=instruction_cap)
        except Exception as exc:raise RuntimeError(f'CPU call {start:08X}->{end:08X} failed at {u.reg_read(UC_ARM_REG_PC):08X}, SP={u.reg_read(UC_ARM_REG_SP):08X}') from exc
        if u.reg_read(UC_ARM_REG_PC)!=end:
            raise ValueError(f'CPU execution did not reach return boundary: PC={u.reg_read(UC_ARM_REG_PC):08X}, expected={end:08X}, SP={u.reg_read(UC_ARM_REG_SP):08X}, instruction cap={instruction_cap}')
        instruction_max[hex(start)]=max(instruction_max.get(hex(start),0),executed[0])
        if u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:
            changed=[(i,u.reg_read(r),v) for i,(r,v) in enumerate(zip(regs,saved)) if u.reg_read(r)!=v]
            raise ValueError(f'pipeline ABI/stack: SP={u.reg_read(UC_ARM_REG_SP):08X}, register changes={changed}, guard={bytes(u.mem_read(sp-stack-4,4)).hex()}')
    def check(before,regions,stack):
        expected=bytearray(before)
        for at,b in regions:expected[at-0x02000000:at-0x02000000+len(b)]=b
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM Expected Writes')
        if any(not(sp-stack<=at and at+n<=sp or any(a<=at and at+n<=a+len(b) for a,b in regions)) for at,n in writes):raise ValueError('CPU write interval')
    def asset(page):
        if page==0:return 0x09400000,bank,mapping
        if kana and page==1:return 0x09403000,bank1,mapping1
        if labels and page==2:return 0x09406000,bank2,mapping2
        p=reports['page_graphics']['pages'][page];a=p['bank_offset'];m=p['map_offset'];return 0x08000000+a,rom[a:a+p['bank_bytes']],rom[m:m+1200]
    def edit_pixels(raw):
        cells=MixedReplay.restore(raw).model.state.cells;result=bytearray()
        for w in cells+(None,)*(20-len(cells)):
            if w is None:at,index=0x619EF8,0
            elif w<11191:at,index=manifest['fixedcell_extension']['mono_provider']['font_offset'],w if w<11172 else w+1
            else:
                v=to_native_word(w);at,index=0x619EF8,(v>>8)+0xE4 if v&255==0xE4 else v
            result.extend(rom[at+index*64:at+(index+1)*64])
        if len(result)!=1280:raise ValueError('full editing field extent')
        return bytes(result)
    def refresh():
        before=bytes(u.mem_read(0x02000000,0x40000));q=struct.unpack('<I',u.mem_read(counter,4))[0]
        admit=q<96
        if admit:
            for i in range(q):
                src,_,n=struct.unpack('<3I',u.mem_read(queue+i*20,12))
                if n and (src+n>0xFFFFFFFF or src<0x0201ED00 and src+n>0x0201E800):admit=False
        raw=bytes(u.mem_read(ed+20,76));wanted=stream(raw);pixels=edit_pixels(raw);vram=bytes(u.mem_read(0x06000000,0x20000))
        call(0x08F12000,stack=144)
        if u.reg_read(UC_ARM_REG_R0)!=int(admit) or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)==admit or bytes(u.mem_read(0x06000000,0x20000))!=vram:raise ValueError('refresh status/deferred VRAM')
        regions=[]
        if admit:
            obj=bytearray(before[0x3000:0x3040]);obj[:3]=bytes([20,20,0])
            regions=[(0x020155F0,wanted),(0x0201E800,pixels),(0x0200FC10,bytes(4)),(0x02003000,bytes(obj)),(counter,struct.pack('<I',q+1)),(queue+q*20,struct.pack('<5I',0x0201E800,0x0600B000,1280,0xFFFFFFFF,2))]
            pending_pixels[0]=pixels;dirty[0]=False;render_stats['queued']+=1
        else:dirty[0]=True;render_stats['deferred']+=1
        check(before,regions,144);render_stats['refresh_calls']+=1
    def draw():
        page=bytes(u.mem_read(ed+8,1))[0];_,_,mp=asset(page);wanted=bytearray(2048)
        for row in range(20):wanted[row*64:row*64+60]=mp[row*60:(row+1)*60]
        before=bytes(u.mem_read(0x02000000,0x40000));call(0x08035676,stack=32);check(before,[(maps+4096,bytes(wanted))],32);stats['draws']+=1
        before=bytes(u.mem_read(0x02000000,0x40000));call(0x080352E6,stack=8);check(before,[],8)
        if editfield:refresh()
    def drain(retry=True):
        before=bytes(u.mem_read(0x02000000,0x40000));vram=bytearray(u.mem_read(0x06000000,0x20000));count=struct.unpack('<I',u.mem_read(counter,4))[0];want=[]
        for i in range(count):
            src,dst,n,mode,kind=struct.unpack('<5I',u.mem_read(queue+i*20,20))
            if dst not in ((0x06008000,0x0600B000) if editfield else (0x06008000,)) or mode!=0xFFFFFFFF or kind!=2:raise ValueError('queued page entry')
            at=dst-0x06000000;vram[at:at+n]=bytes(u.mem_read(src,n));want.append((src,dst,n))
        bios.clear();call(0x080007DC,stack=48);check(before,[(counter,bytes(4))],48)
        if bios!=want or bytes(u.mem_read(0x06000000,0x20000))!=vram:raise ValueError('VRAM consumption/source lifetime')
        page=bytes(u.mem_read(ed+8,1))[0];_,b,mp=asset(page)
        # Compare consumed pixels, not just bytes residing in fixture ROM.
        if decode(bytes(u.mem_read(0x06008000,len(b))),mp)!=decode(b,mp):raise ValueError('visible page mismatch')
        if editfield and pending_pixels[0] is not None and bytes(u.mem_read(0x0600B000,1280))!=pending_pixels[0]:raise ValueError('editing pixels consumption/lifetime')
        stats['drains']+=1
        if editfield and dirty[0] and retry:
            if frame:
                step(0,consume=False,physical=True);stats['idle_retry_frames']+=1
            else:refresh()
            render_stats['latest_after_drain']+=1;drain(False)
            if bytes(u.mem_read(0x0600B000,1280))!=edit_pixels(bytes(u.mem_read(ed+20,76))):raise ValueError('latest edit redisplay after deferred render')
    def setup(raw,page=0):
        u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(0x06000000,b'\xA7'*0x20000)
        ui=bytearray(initialize(struct.pack('<4I',raw[0]&15,33,0x020010A6,1)));ui[0]=12;ui[8]=page;ui[20:]=raw;u.mem_write(ed,bytes(ui))
        u.mem_write(glob+4,struct.pack('<I',keys));u.mem_write(glob+0x28,struct.pack('<I',maps));u.mem_write(counter,bytes(4))
        u.mem_write(keys+4,bytes(2))
        if editfield:
            u.mem_write(0x0200FBE0,bytes(64));u.mem_write(0x0200FC18,struct.pack('<I',0x02003000));u.mem_write(0x02003000,bytes(64));pending_pixels[0]=None;dirty[0]=False
        # Initial fixture crosses the page boundary before any raw input.
        before=bytes(u.mem_read(0x02000000,0x40000));src,b,_=asset(page);call(0x080356D0,stack=40)
        check(before,[(counter,struct.pack('<I',1)),(queue,struct.pack('<5I',src,0x06008000,len(b),0xFFFFFFFF,2))],40);draw();drain()
    def navigation(page,x,y,direction,adapted=True):
        if direction==0x40:y=(y-1)%6
        elif direction==0x80:y=(y+1)%6
        elif direction==0x20:x=(x-1)%16
        else:x=(x+1)%16
        if adapted and page in jamo_pages and (x,y) in ((6,2),(8,2)):return x,y
        off=struct.unpack_from('<I',rom,0x35148 if page==2 else 0x350D4)[0]-0x08000000
        while rom[off]!=255:
            entry=rom[off:off+12]
            if entry[:2]==bytes([x,y]):
                j={0x40:2,0x80:4,0x20:6,0x10:8}[direction];return tuple(entry[j:j+2])
            off+=12
        return x,y
    def step(mask,col=0,row=0,consume=True,repeat=0,physical=False):
        # Only physical key/cell selection is supplied. No HOST editor state,
        # queue, map or bank writes between raw processing and consumption.
        if physical:col,row=bytes(u.mem_read(ed+6,2))
        else:u.mem_write(ed+6,bytes([col,row]))
        u.mem_write(keys+2,struct.pack('<H',mask))
        if frame:u.mem_write(keys+4,struct.pack('<H',repeat))
        before=bytes(u.mem_read(0x02000000,0x40000));ui=bytearray(u.mem_read(ed,96));wanted=bytearray(ui);p=ui[8];q=struct.unpack('<I',u.mem_read(counter,4))[0];cmd=None;action=None
        if mask&2:action=('backspace',None)
        elif mask&1:
            if col==15 and row in (0,1):cmd=2 if row==0 else 3
            elif col==15 and row in (2,3):action=('move',1 if row==2 else -1)
            elif labels and col==15 and row==4:action=('native',b'\x00')
            elif col<15 and row<6 and p in jamo_pages and selectors[row*15+col]<40:action=('jamo',KEYS[selectors[row*15+col]])
            elif latin and p==2 and col<15 and row<6:
                cell=reports['latin_input']['cells'][row*15+col]
                if cell['active']:action=('native',bytes.fromhex(cell['token_hex']))
        elif mask&0x200:cmd=0
        elif mask&0x100:cmd=1
        if action:
            _,updated=apply(bytes(ui[20:]),*action);wanted[20:]=updated;stats['latin_actions' if latin and action[0]=='native' and col<15 else 'space_actions' if action[0]=='native' else 'caret_actions' if action[0]=='move' else 'backspaces' if mask&2 else 'jamo_actions']+=1
        extras=[];expected_sounds=[]
        if cmd is not None:
            if q<96:
                nxt=(p-1)%3 if cmd==0 else (p+1)%3 if cmd==1 else (1 if p==0 else 0) if cmd==2 else (1 if p==2 else 2)
                wanted[8]=nxt;src,b,_=asset(nxt);extras=[(counter,struct.pack('<I',q+1)),(queue+q*20,struct.pack('<5I',src,0x06008000,len(b),0xFFFFFFFF,2))];expected_sounds=[466];stats['page_transitions']+=1
            else:stats['queue_rejections']+=1
        if frame:
            consumed=bool(mask&0x30B)
            if not consumed and repeat&0xF0:
                direction=next(k for k in (0x40,0x80,0x20,0x10) if repeat&k)
                x,y=navigation(p,col,row,direction)
                wanted[6:8]=bytes([x,y]);expected_sounds=[125];stats['navigation_cases']+=1
            wanted[15]=(ui[15]+1)&255
            # Native draw fills32x32 then maps30x20, followed by two original
            # ten-column editing-field strips. Independent table interpreter.
            _,_,mp=asset(wanted[8]);drawn=bytearray(2048)
            for r in range(20):drawn[r*64:r*64+60]=mp[r*60:(r+1)*60]
            off=0x35668
            while rom[off]!=255:
                x,y,layer,width=rom[off:off+4];tile=struct.unpack_from('<H',rom,off+4)[0]
                if layer!=2:raise ValueError('native editing tilemap layer')
                x+=2;y+=3
                for j in range(width):
                    struct.pack_into('<H',drawn,y*64+(x+j)*2,(tile+2*j)&65535)
                    struct.pack_into('<H',drawn,(y+1)*64+(x+j)*2,(tile+2*j+1)&65535)
                off+=6
            qq=q+int(cmd is not None and q<96);admit=qq<96
            for i in range(q if q<96 else 0):
                src,_,n=struct.unpack('<3I',u.mem_read(queue+i*20,12))
                if n and (src+n>0xFFFFFFFF or src<0x0201ED00 and src+n>0x0201E800):admit=False
            raw=bytes(wanted[20:]);pixels=edit_pixels(raw)
            if admit:
                obj=bytearray(before[0x3000:0x3040]);obj[:3]=bytes([20,20,0])
                extras += [(0x020155F0,stream(raw)),(0x0201E800,pixels),(0x0200FC10,bytes(4)),(0x02003000,bytes(obj)),(counter,struct.pack('<I',qq+1)),(queue+qq*20,struct.pack('<5I',0x0201E800,0x0600B000,1280,0xFFFFFFFF,2))]
                pending_pixels[0]=pixels;dirty[0]=False;render_stats['queued']+=1
            else:dirty[0]=True;render_stats['deferred']+=1
            extras.append((maps+4096,bytes(drawn)))
            vram=bytes(u.mem_read(0x06000000,0x20000));call(0x08034E34,stack=248)
            if u.reg_read(UC_ARM_REG_R0)!=wanted[13] or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)!=(wanted[13]==0) or sounds!=expected_sounds or bytes(u.mem_read(0x06000000,0x20000))!=vram:raise ValueError(f'native frame result mask={mask:X}, cell={col},{row}, sounds={sounds}/{expected_sounds}')
            check(before,[(ed,bytes(wanted)),*extras],248)
            expected_calls=[0x08034EFE]
            # Original BLE is signed: low nibble8..15 yields a negative
            # shifted value and hides the caret, not unsigned >8.
            if 1<=ui[15]&15<=7:expected_calls.append(0x08305200)
            expected_calls += [0x08305100,0x08305100,0x08305000,0x08F12000]
            if frame_calls!=expected_calls:raise ValueError('native frame ordering '+str(frame_calls))
            if 0x08305200 in frame_calls:
                cursor=MixedReplay.restore(bytes(ui[20:])).model.state.cursor
                if sprite_calls[1][0]!=(0x80858018+(cursor*8<<16))&0xFFFFFFFF:raise ValueError('editing caret pixel position')
                stats['caret_sprite_cases']+=1
            stats['native_frames']+=1;stats['draws']+=1;stats['input_calls']+=1;render_stats['refresh_calls']+=1
            if consume:drain()
            return
        vram=bytes(u.mem_read(0x06000000,0x20000));call(pc,0x08034F66,220)
        if u.reg_read(UC_ARM_REG_R0)!=1 or u.reg_read(UC_ARM_REG_CPSR)&0x40000000 or sounds!=expected_sounds or bytes(u.mem_read(0x06000000,0x20000))!=vram:raise ValueError('raw priority/flags/deferred effects')
        check(before,[(ed,bytes(wanted)),*extras],220);stats['input_calls']+=1
        draw()
        if consume:drain()
    c=MixedReplay(4);empty=c.serialize();c.press('ㄱ');partial=c.serialize();c.press('ㅏ');complete=c.serialize()
    for rawstate in (empty,partial,complete):
        for page in range(3):
            for col,row in [(0,0),(15,0),(15,1)]:
                for mask in (0x100,0x200,0x300,0x101,0x201,0x301):setup(rawstate,page);step(mask,col,row)
    # Repeated transitions keep the CPU-composed text, queue and maps alive.
    positions={KEYS[v]:(i%15,i//15) for i,v in enumerate(selectors) if v<40}
    for key,(col,row) in positions.items():
        setup(complete);step(1,col,row)
        for mask in (0x100,0x100,0x100,0x200,0x200,0x200):step(mask)
        step(2,col,row)
    setup(partial)
    for mask in (0x100,0x100,0x100,0x200,0x200,0x200):step(mask,consume=False);stats['pending_transitions']+=1
    drain()
    # Fill all96 entries through CPU button processing, not HOST queue writes.
    # The97th page request stays on page0; jamo/delete must remain usable.
    setup(partial,1 if editfield else 0)
    for i in range(96-int(editfield)):step(0x100,consume=False);stats['pending_transitions']+=1
    step(0x100,consume=False)
    col,row=positions['ㅏ'];step(1,col,row,consume=False);step(2,col,row,consume=False)
    drain()
    if editfield:
        for text in ['ㄱㅜㄱㅇㅓ','ㄷㅏㄹㄱㅏ','ㄲㅗㅏㅣㄹㄱ']:
            c=MixedReplay(4);c.load((0,0,0));setup(c.serialize())
            for key in text:
                col,row=positions[key];step(1,col,row)
            step(0x100);step(0x200);step(1,15,3);step(1,15,2)
            for key in text:step(2)
    if frame:
        # Baseline graph retains the original Japanese skip table: exactly
        # two ACTIVE new jamo cells cannot be reached. Do not waive this.
        original_reachable={(0,0)};points=[(0,0)]
        for point in points:
            for direction in (0x10,0x80,0x20,0x40):
                nxt=navigation(0,*point,direction,adapted=False)
                if nxt not in original_reachable:original_reachable.add(nxt);points.append(nxt)
        unreachable=[key for key,point in positions.items() if point not in original_reachable]
        if unreachable!=['ㅕ','ㅗ']:raise ValueError('native skip-table counterexample population '+str(unreachable))
        print('REPRODUCED original navigation cannot select',unreachable,flush=True)
        for page in range(3):
            setup(complete,page)
            for row in range(6):
                for col in range(16):
                    for repeat in (0x10,0x20,0x40,0x80,0xF0):step(0,col,row,repeat=repeat)
        # One uninterrupted button-only route: no HOST grid/caret/editor
        # position writes between movement and all40 selector A/B actions.
        print('PASS frame boundary navigation1440; checking button-only40selectors',flush=True)
        setup(complete);physical_selectors=0;physical_moves=0
        def navigate_to(page,target):
            nonlocal physical_moves
            origin=tuple(u.mem_read(ed+6,2));paths=[(origin,[])];seen={origin}
            for point,path in paths:
                if point==target:break
                for direction in (0x10,0x80,0x20,0x40):
                    nxt=navigation(page,*point,direction)
                    if nxt not in seen:seen.add(nxt);paths.append((nxt,path+[direction]))
            else:raise ValueError('jamo unreachable through native navigation '+str(target))
            for direction in path:step(0,repeat=direction,physical=True);physical_moves+=1
            if tuple(u.mem_read(ed+6,2))!=target:raise ValueError('physical selection cursor')
        for page in jamo_pages:
            if page:step(0x100,physical=True)
            if bytes(u.mem_read(ed+8,1))!=bytes([page]):raise ValueError('physical page transition')
            for key,target in positions.items():
                navigate_to(page,target)
                prior=bytes(u.mem_read(ed+20,76));step(1,physical=True)
                # Invalid combinations are consumed, not a key to undo.
                if bytes(u.mem_read(ed+20,76))!=prior:step(2,physical=True)
                if bytes(u.mem_read(ed+20,76))!=prior:raise ValueError('physical selector undo')
                physical_selectors+=1
        stats.update(physical_selector_paths=physical_selectors,physical_navigation_moves=physical_moves)
        if kana:
            # One natural-in-fixture button route alternates the two pages;
            # neither compact state nor cursor coordinates are HOST rewritten.
            setup(complete);expected=bytes(u.mem_read(ed+20,76));cross_keys=0
            for key in 'ㄱㅗㅏㄹㄱ':
                page=bytes(u.mem_read(ed+8,1))[0];navigate_to(page,positions[key])
                _,expected=apply(expected,'jamo',key);step(1,physical=True)
                if bytes(u.mem_read(ed+20,76))!=expected:raise ValueError('cross-page physical composition')
                step(0x100 if page==0 else 0x200,physical=True);cross_keys+=1
            for _ in range(cross_keys):step(2,physical=True)
            if bytes(u.mem_read(ed+20,76))!=complete:raise ValueError('physical cross-page undo')
            stats['physical_cross_page_jamo_keys']=cross_keys
            stats['physical_navigation_moves']=physical_moves
    # Full/corrupt counters cannot alter page, queue, editor or VRAM. The
    # existing entries are unknown fixture data, so they are never drained.
    for count in (96,97,0xFFFFFFFF):
        for page in range(3):
            for mask,col,row in [(0x100,0,0),(0x200,0,0),(1,15,0),(1,15,1)]:
                setup(partial,page);u.mem_write(counter,struct.pack('<I',count));step(mask,col,row,consume=False)
    # Independent defect reproduction with the same CPU path minus guard.
    setup(partial);u.mem_write(counter,struct.pack('<I',96));u.mem_write(keys+2,struct.pack('<H',0x100));oldvram=bytes(u.mem_read(0x06000000,0x20000));oldqueue=bytes(u.mem_read(queue,1920))
    u.mem_protect(0x08F10000,4096,UC_PROT_READ|UC_PROT_EXEC|2);u.mem_write(0x08F10000,old);u.ctl_remove_cache(0x08F10000,0x08F11000);u.mem_protect(0x08F10000,4096,UC_PROT_READ|UC_PROT_EXEC)
    call(pc,0x08034F66,220)
    if bytes(u.mem_read(ed+8,1))!=b'\x01' or bytes(u.mem_read(queue,1920))!=oldqueue or bytes(u.mem_read(0x06000000,0x20000))!=oldvram:raise ValueError('unguarded full queue defect reproduction')
    draw();_,b,mp=asset(1)
    if decode(bytes(u.mem_read(0x06008000,len(b))),mp)==decode(b,mp):raise ValueError('counterexample did not discriminate')
    stats['unguarded_mismatch_reproduced']+=1
    guard_cases=0;editor_rejections=0
    if labels:
        from hangul_mixed_editor import Snapshot
        # Test append/overwrite and full-end rejection at every logical length
        # and cursor for all capacities1..10, on all three UI pages.
        for cap in range(1,11):
            for length in range(cap+1):
                for cursor in range(length+1):
                    c=MixedReplay(cap);c.load((0x8001,)*length)
                    c.model.state=Snapshot(c.model.state.cells,cursor,None);c._rebase()
                    raw=c.serialize();accepted,wanted=apply(raw,'native',b'\x00')
                    if accepted!=(cursor<cap):raise ValueError('space reference capacity')
                    for page in range(3):
                        setup(raw,page);step(1,15,4)
                        if bytes(u.mem_read(ed+20,76))!=wanted:raise ValueError('space append/overwrite/reject')
                        stats['space_boundary_cases']+=1
        for keys_text in ('ㄱ','ㄱㅏ','ㄱㅗㅏㄹㄱ'):
            c=MixedReplay(4)
            for key in keys_text:c.press(key)
            raw=c.serialize();accepted,wanted=apply(raw,'native',b'\x00')
            if not accepted:raise ValueError('space composition state')
            for page in range(3):
                setup(raw,page);step(1,15,4);stats['space_partial_cases']+=1
                actual=MixedReplay.restore(bytes(u.mem_read(ed+20,76)))
                if actual.serialize()!=wanted:raise ValueError('space partial state preservation')
                if keys_text=='ㄱ':
                    try:actual.candidate()
                    except ValueError:pass
                    else:raise ValueError('space silently commits partial initial')
    if latin:
        from hangul_mixed_editor import Snapshot
        cells=reports['latin_input']['cells'];active=[c for c in cells if c['active']]
        # Every real/blank/absent cell: append, overwrite, full-end rejection,
        # and insertion after a complete Hangul composition.
        for cell in cells:
            for kind in ('empty','overwrite','full','hangul'):
                c=MixedReplay(1 if kind=='full' else 4)
                if kind in ('overwrite','full'):
                    c.load((0x8001,));c.model.state=Snapshot(c.model.state.cells,int(kind=='full'),None);c._rebase()
                elif kind=='hangul':c.press('ㄱ');c.press('ㅏ')
                raw=c.serialize();setup(raw,2);step(1,cell['column'],cell['row']);stats['latin_cell_cases']+=1
                if not cell['active'] and bytes(u.mem_read(ed+20,76))!=raw:raise ValueError('inactive page2 cell edited')
        # All logical capacity/length/cursor boundaries for distinct single-
        # byte letter/digit and two-byte symbol selectors.
        for token in ('5e','02','e457'):
            cell=next(c for c in active if c['token_hex']==token)
            for cap in range(1,11):
                for length in range(cap+1):
                    for cursor in range(length+1):
                        c=MixedReplay(cap);c.load((0x8001,)*length)
                        c.model.state=Snapshot(c.model.state.cells,cursor,None);c._rebase()
                        raw=c.serialize();accepted,wanted=apply(raw,'native',bytes.fromhex(token))
                        if accepted!=(cursor<cap):raise ValueError('Latin reference capacity')
                        setup(raw,2);step(1,cell['column'],cell['row']);stats['latin_boundary_cases']+=1
                        if bytes(u.mem_read(ed+20,76))!=wanted:raise ValueError('Latin boundary bytes')
        for cell in active:
            for text in ('ㄱ','ㄱㅗㅏㄹㄱ'):
                c=MixedReplay(4)
                for key in text:c.press(key)
                raw=c.serialize();setup(raw,2);step(1,cell['column'],cell['row']);stats['latin_partial_cases']+=1
                if text=='ㄱ':
                    try:MixedReplay.restore(bytes(u.mem_read(ed+20,76))).candidate()
                    except ValueError:pass
                    else:raise ValueError('Latin selection silently committed partial initial')
        # One continuous physical-key route, no HOST compact/grid writes
        # between keys; native input followed by canonical B and page changes.
        setup(complete,2);selected=0;moves_before=physical_moves
        for cell in active:
            navigate_to(2,(cell['column'],cell['row']))
            prior=bytes(u.mem_read(ed+20,76));accepted,wanted=apply(prior,'native',bytes.fromhex(cell['token_hex']))
            if not accepted:raise ValueError('physical Latin setup')
            step(1,physical=True)
            if bytes(u.mem_read(ed+20,76))!=wanted:raise ValueError('physical Latin selection')
            _,deleted=apply(wanted,'backspace',None);step(2,physical=True)
            if bytes(u.mem_read(ed+20,76))!=deleted:raise ValueError('physical Latin canonical delete')
            # Return to page0 for a reversible jamo keystroke, then page2.
            step(0x100,physical=True);navigate_to(0,positions['ㄱ']);step(1,physical=True);step(2,physical=True);step(0x200,physical=True)
            if bytes(u.mem_read(ed+20,76))!=deleted:raise ValueError('Latin/jamo page transition rebase')
            selected+=1
        stats.update(physical_latin_selector_paths=selected,physical_latin_navigation_moves=physical_moves-moves_before)
        print('PASS Latin cells360, boundaries855, partial112, button-only56',flush=True)
    if editfield:
        # Guard scans every possible occupied position, interval edges and
        # overflow. These are separate precondition fixtures, not an input run.
        edge_cases=[(0x0201E7FF,1),(0x0201E7FF,2),(0x0201E800,0),(0x0201E800,1),(0x0201ECFF,1),(0x0201ED00,1),(0x0201ED01,1),(0x0201E000,2048),(0x0201E000,2049),(0x08000000,9600),(0xFFFFFFF0,16),(0xFFFFFFF0,15)]
        normal=struct.pack('<5I',0x08000000,0x06008000,9600,0xFFFFFFFF,2)
        for index in range(95):
            for src,n in edge_cases:
                u.mem_write(counter,struct.pack('<I',95));u.mem_write(queue,normal*95);u.mem_write(queue+index*20,struct.pack('<5I',src,0x06008000,n,0xFFFFFFFF,2))
                before=bytes(u.mem_read(0x02000000,0x40000));call(0x08F13000,stack=12)
                reject=n!=0 and (src+n>0xFFFFFFFF or src<0x0201ED00 and src+n>0x0201E800)
                if u.reg_read(UC_ARM_REG_R0)!=int(not reject) or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)!=reject:raise ValueError('stage interval guard')
                check(before,[],12);guard_cases+=1
        for offset,value in [(4,0),(4,11),(4,255),(4,6),(22,71),(95,0),(21,255)]:
            setup(complete);u.mem_write(ed+offset,bytes([value]))
            before=bytes(u.mem_read(0x02000000,0x40000));vram=bytes(u.mem_read(0x06000000,0x20000));call(0x08F12000,stack=144)
            if u.reg_read(UC_ARM_REG_R0)!=0 or not u.reg_read(UC_ARM_REG_CPSR)&0x40000000 or bytes(u.mem_read(0x06000000,0x20000))!=vram:raise ValueError('invalid editor refresh rejection')
            check(before,[],144);editor_rejections+=1
    result=dict(passed=True,rom_integrated=False,source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,raw_input_to_actual_page_uploader=True,no_HOST_editor_queue_map_bank_rewrites_between_CPU_stages=True,page_upload_queue_guard=True,dependencies=deps,raw_helper_sha256=sha(raw_blob),raw_ISA=raw_isa,native_code=native,fixture_writes=fixture,unguarded_ISA=old_isa,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in [Path(__file__).name,'hangul_keyboard_control_shim.py','hangul_keyboard_raw_router.py','hangul_mixed_replay_state.py','hangul_mixed_editor_init.py','prepare_keyboard_page_graphics.py']},artifacts={'unguarded_control.bin':sha(old)},limits=['CPU input and initial state fixtures, not natural gamepad/playthrough or actual installed ROM.','Original page upload/draw/map clear/queue enqueue/drain execute; sound/config/sprite/BIOS modeled. No VBlank/scanout or real-screen claim.','Page assets94xxxx/ROM helpers83xxxx are fixture locations, not adopted free space. Original outer-frame/edit-field refresh is not executed.','Guard rejects full/corrupt queue before UI mutation; no retry/feedback or concurrent IRQ reservation/lifetime adoption. Unknown preexisting full-queue entries are never drained.','Other-page letters remain unsupported; command labels Japanese. Save/persistence/format discrimination remain pending.'])
    result.update(CPU_instruction_cap=instruction_cap,maximum_instructions_per_call=instruction_max)
    if editfield:
        result.update(glyph_rom_sha256=glyph_identity,refresh_ISA=refresh_info,refresh_counts=render_stats,guard_interval_cases=guard_cases,refresh_rejected_editor_cases=editor_rejections,refresh_stack_bytes=144,raw_to_editfield_pixels=True)
        result['tools']['hangul_keyboard_refresh.py']=sha((ROOT/'tools/hangul_keyboard_refresh.py').read_bytes())
        for n in ['refresh.bin','guard.bin']:result['artifacts'][n]=sha((out/n).read_bytes())
        result['limits'][2]='Fixtures use original observed stage/context/target and candidate41byte cache; no game RAM/ROM placement/lifetime adoption. CPU wrapper executes cache->native parser/upload, but original complete outer-frame and glyph tilemap placement are not executed.'
        result['limits'].append('Refresh protects pending stage readers and queues latest state after drain only in sequential CPU scheduling. No VBlank/IRQ synchronization or real-screen/presentation proof. Native20cell pixels checked against fixed glyph ROM, not complete supported font aesthetic approval.')
    if frame:
        result.update(bounded_native_outer_frame=True,frame_stack_bytes=248,frame_native_code=frame_scopes,frame_ISA={name:info for _,_,info,name in frame_blobs},original_navigation_unreachable_jamo=unreachable,navigation_adapted_cells=[[6,2],[8,2]])
        result['tools']['hangul_keyboard_frame_adapters.py']=sha((ROOT/'tools/hangul_keyboard_frame_adapters.py').read_bytes())
        for _,b,_,name in frame_blobs:result['artifacts'][name]=sha(b)
        result['limits'][2]='Native outer frame034E34/input state12 executes in CPU clone, including caret/page/editor tilemap placement and refresh; coordinated old pad/flatten no-ops and new adapters are fixtures, not adopted game code/RAM.'
        result['limits'].append('Native034E34 outer frame executed only state12, with five extra BL replacements: legacy pad/flatten no-op, input-field render veneer, validated caret and page0 two-cell skip-table bypass. Other pages retain native navigation. Native navigation/draw/map decoration execute. Sprite submission/BIOS/config remain modeled. Initial setup and queue drain are fixtures; animation/confirmation/exit states, game/IRQ lifetime, actual screen and save not verified.')
    if kana:
        result.update(jamo_pages=list(jamo_pages),two_page_replacement=True,all_jamo_cells_button_reachable=True)
        result['tools']['hangul_keyboard_kana_frame.py']=sha((ROOT/'tools/hangul_keyboard_kana_frame.py').read_bytes())
        result['tools']['prepare_keyboard_kana_replacement.py']=sha((ROOT/'tools/prepare_keyboard_kana_replacement.py').read_bytes())
        result['limits'][4]='Both kana pages replaced in CPU clone; page2 Latin/symbol input and Japanese command labels unresolved. Save/persistence/format discrimination pending.'
        result['limits'][-1]='Native state12 frame/nav/upload/draw/refresh/drain execute with both pages and button-only selector routes. BIOS/sprite/audio modeled; fixture addresses not adopted ROM/RAM. No game/IRQ lifetime, scanout, natural runtime or save claim.'
    if labels:
        result.update(Korean_command_labels=18,native_space_key=True,
            action_ISA=reports['keyboard_labels']['ISA'])
        result['tools']['prepare_keyboard_labels.py']=sha((ROOT/'tools/prepare_keyboard_labels.py').read_bytes())
        result['limits'][4]='Korean labels and native00 space key connected in CPU fixtures. Page2 Latin/symbol selection, confirmation lifecycle, save/persistence remain unresolved.'
        result['limits'].append('Labels are technical candidates, not human wording/visual approval; all glyphs verified through native upload/map/VRAM bytes, not actual scanout.')
    if latin:
        result.update(page2_Latin_digit_symbol_input=True,active_page2_cells=56,inactive_page2_cells=34,
            action_ISA=reports['latin_input']['ISA'])
        result['tools']['prepare_keyboard_latin_input.py']=sha((ROOT/'tools/prepare_keyboard_latin_input.py').read_bytes())
        result['limits'][4]='All three keyboard pages and Korean command labels/space connected in CPU fixtures. Native confirmation lifecycle, post-confirm consumers, save/persistence remain unresolved.'
        result['limits'].append('Native selection rebases undo history; canonical B is reference-checked, not restoration of the entire pre-native composition history. Partial confirmation rejection here is host-model only.')
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');require_hash(source,profile['sha256']);require_hash(play,identity)
    if editfield:require_hash(product,glyph_identity);print('editing refresh',render_stats,flush=True)
    print('PASS raw keys -> native page assets/queue/draw/drain',stats,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--editfield',action='store_true');parser.add_argument('--frame',action='store_true')
    parser.add_argument('--kana',action='store_true')
    parser.add_argument('--labels',action='store_true')
    parser.add_argument('--latin',action='store_true')
    args=parser.parse_args();main(args.editfield,args.frame,args.kana,args.labels,args.latin)
