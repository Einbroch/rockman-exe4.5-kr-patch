"""Native page lookup/draw/enqueue/drain CPU execution with candidate assets.

Only display-config calls and BIOS CpuFastSet are modeled. IWRAM map writer,
fill, ROM page selection and deferred transfer queue execute original code.
The pointer replacement exists only in a CPU clone, not a product ROM.
"""
import json, struct
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB


def main():
    base=ROOT/'analysis/hangul_keyboard_v1'; out=base/'cpu_page_graphics'; out.mkdir(exist_ok=True)
    assets=base/'page_graphics'; report_path=assets/'report.json'
    a=json.loads(report_path.read_text(encoding='utf8'))
    if not a['passed'] or a['rom_integrated'] or a['candidate']['active_cells']!=40:
        raise ValueError('asset scope')
    for n,h in a['tools'].items(): require_hash(ROOT/'tools'/n,h)
    for n,h in a['artifacts'].items(): require_hash(assets/n,h)
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename']; require_hash(source,profile['sha256']); original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    require_hash(play,a['current_rom_sha256']); current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    scopes=[]; cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB); ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    # Literals deliberately excluded; original IWRAM body addresses retained.
    regions=[(0x35676,0x356BA,0x08035676),(0x356D0,0x356E2,0x080356D0),
             (0x8C8,0x8E0,0x080008C8),(0x7D4,0x846,0x080007D4),
             (0x848,0x880,0x08000848),(0x97C,0x98A,0x0800097C),
             (0xEC140,0xEC144,0x080EC140),(0x16D8,0x16E2,0x080016D8),
             (0x16F4,0x16FE,0x080016F4),(0x1EE994,0x1EE9CE,0x03005A94),
             (0x1EEA08,0x1EEA3E,0x03005B08),(0x352E6,0x35332,0x080352E6)]
    for start,end,pc in regions:
        data=original[start:end]; ins=list(cs.disasm(data,pc))
        if current[start:end]!=data or sum(i.size for i in ins)!=len(data): raise ValueError('native code extent/identity')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800): raise ValueError('Thumb1')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes: raise ValueError('native instruction roundtrip')
        scopes.append(dict(offset=start,bytes=len(data),execution_address=hex(pc),sha256=sha(data)))
    bank=(assets/'jamo_page0_tiles.bin').read_bytes(); mapping=(assets/'jamo_page0_map.bin').read_bytes()
    stats=dict(draws=0,enqueues=0,drains=0,saturation_rejections=0,candidate_page0_draws=0,candidate_page0_transfers=0,cursor_calls=0,jamo_cursor_alignment_cases=0)
    fixture_writes=[]
    for variant,image in [('source',original),('current',current),('candidate_CPU_clone',current)]:
        clone=bytearray(image)
        if variant=='candidate_CPU_clone':
            for offset,new in [(0x356C0,struct.pack('<I',0x09002000)),(0x356E8,struct.pack('<3I',0x09000000,0x06008000,len(bank)))]:
                fixture_writes.append(dict(offset=offset,expected_hex=image[offset:offset+len(new)].hex(),final_hex=new.hex()))
                clone[offset:offset+len(new)]=new
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        size=(len(clone)+4095)&~4095; u.mem_map(0x08000000,size); u.mem_write(0x08000000,bytes(clone)); u.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x09000000,0x3000);u.mem_write(0x09000000,bank);u.mem_write(0x09002000,mapping);u.mem_protect(0x09000000,0x3000,UC_PROT_READ)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        overlay=image[0x1EE700:0x1EFF74];u.mem_write(0x03005800,overlay);u.mem_protect(0x03005000,0x2000,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x06000000,0x20000);u.mem_map(0x0FF00000,4096)
        editor,glob,maps,sp,stop=0x0200FC40,0x02000200,0x02018000,0x03007F00,0x0FF00000
        counter,queue=0x02010724,0x02012730
        regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
        writes=[];config=[];bios=[];sprites=[]
        u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,at,n,v,user:writes.append((at,n)))
        def service(cpu,pc,n,user):
            if pc in (0x0803438A,0x08034364):
                config.append((pc,cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)))
                cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
            elif pc==0x080EC140:
                src,dst,words=[cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2)]
                if dst!=0x06008000 or words%8 or words*4>0x3000: raise ValueError('BIOS contract')
                bios.append((src,dst,words*4));cpu.mem_write(dst,bytes(cpu.mem_read(src,words*4)))
                cpu.reg_write(UC_ARM_REG_PC,0x080EC143)
            elif pc==0x08029538:
                sprites.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)))
                cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        u.hook_add(UC_HOOK_CODE,service)
        def call(pc,stack):
            u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
            saved=[editor if r==UC_ARM_REG_R5 else glob if r==UC_ARM_REG_R10 else 0x13579000+i for i,r in enumerate(regs)]
            for r,v in zip(regs,saved):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
            u.emu_start(pc|1,stop,count=30000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4: raise ValueError('page ABI/stack')
        def allow(ranges):
            if any(not any(lo<=at and at+n<=hi for lo,hi in ranges) for at,n in writes):raise ValueError('page unexpected CPU write')
        placements={(p['column'],p['row']):p for p in a['candidate']['placements']}
        for row in range(6):
            for col in range(16):
                for blink in (0,4,8,12):
                    u.mem_write(0x02000000,b'\xA7'*0x40000)
                    state=bytearray(96);state[6:8]=bytes([col,row]);state[15]=blink;u.mem_write(editor,bytes(state))
                    before=bytes(u.mem_read(0x02000000,0x40000));sprites.clear();call(0x080352E6,8)
                    dx=col*11+6*(col>=5)+6*(col>=10)+4*(col>=15)
                    origin,frames=struct.unpack_from('<I',image,0x35338 if col==15 else 0x35334)[0],struct.unpack_from('<I',image,0x35340 if col==15 else 0x3533C)[0]
                    packed=(origin+(dx<<16)+row*16)&0xFFFFFFFF
                    frame=frames+(16 if col==15 else 8)*((blink>>3)&1)
                    if sprites!=[(packed,frame,2,4)] or bytes(u.mem_read(0x02000000,0x40000))!=before:raise ValueError('native cursor placement')
                    allow([(sp-8,sp)]);stats['cursor_calls']+=1
                    if (col,row) in placements:
                        p=placements[col,row]
                        if p['x']!=((packed>>16)&0x7FFF)+1 or p['y']!=(packed&0x7FFF)+8:raise ValueError('jamo/cursor alignment')
                        stats['jamo_cursor_alignment_cases']+=1
        for page in range(3):
            p=a['pages'][page]
            use_candidate=variant=='candidate_CPU_clone' and page==0
            source_bank=0x09000000 if use_candidate else 0x08000000+p['bank_offset']
            length=len(bank) if use_candidate else p['bank_bytes']
            wanted_bank=bank if use_candidate else image[p['bank_offset']:p['bank_offset']+length]
            rawmap=mapping if use_candidate else image[p['map_offset']:p['map_offset']+1200]
            for yoffset in (-8,0,8,16):
                for qcount in (0,95,96):
                    u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(0x06000000,b'\xA7'*0x20000)
                    state=bytearray(96);struct.pack_into('<h',state,2,yoffset);state[8]=page
                    u.mem_write(editor,bytes(state));u.mem_write(glob+0x28,struct.pack('<I',maps))
                    u.mem_write(counter,struct.pack('<I',qcount));u.mem_write(queue,b'\xA7'*1920)
                    before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before)
                    # Original page draw clears BG2 then places30x20, clipping y.
                    at=maps+4096-0x02000000; expected[at:at+2048]=bytes(2048)
                    for row in range(20):
                        y=row+(yoffset>>3)
                        if 0<=y<32: expected[at+y*64:at+y*64+60]=rawmap[row*60:(row+1)*60]
                    config.clear(); call(0x08035676,32)
                    # Native map writer intentionally leaves r1 at end row.
                    if bytes(u.mem_read(0x02000000,0x40000))!=expected or config!=[(0x0803438A,yoffset&65535,1),(0x08034364,2,20+(yoffset>>3))]:raise ValueError('native page draw/config memory '+repr(config))
                    allow([(maps+4096,maps+6144),(sp-32,sp)])
                    stats['draws']+=1;stats['candidate_page0_draws']+=use_candidate
                    call(0x080356D0,40)
                    if qcount<96:
                        struct.pack_into('<I',expected,counter-0x02000000,qcount+1)
                        entry=struct.pack('<5I',source_bank,0x06008000,length,0xFFFFFFFF,2)
                        expected[queue-0x02000000+qcount*20:queue-0x02000000+(qcount+1)*20]=entry
                        stats['enqueues']+=1
                    else: stats['saturation_rejections']+=1
                    if bytes(u.mem_read(0x02000000,0x40000))!=expected or bytes(u.mem_read(0x06000000,0x20000))!=b'\xA7'*0x20000:raise ValueError('enqueue deferred/whole memory')
                    allow([(counter,counter+4),(queue+qcount*20,queue+(qcount+1)*20),(sp-40,sp)])
                    # Empty queue case proceeds without any HOST rewrite of
                    # queue/map/bank/editor. Other counts test enqueue only.
                    if qcount==0:
                        bios.clear(); call(0x080007DC,48);allow([(counter,counter+4),(sp-48,sp)])
                        struct.pack_into('<I',expected,counter-0x02000000,0)
                        vram=bytearray(b'\xA7'*0x20000);vram[0x8000:0x8000+length]=wanted_bank
                        if bios!=[(source_bank,0x06008000,length)] or bytes(u.mem_read(0x06000000,0x20000))!=vram or bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('native drain/BIOS pixels/whole memory')
                        stats['drains']+=1;stats['candidate_page0_transfers']+=use_candidate
    report=dict(passed=True,rom_integrated=False,source_sha256=profile['sha256'],current_rom_sha256=a['current_rom_sha256'],counts=stats,native_code=scopes,fixture_writes=fixture_writes,asset_report_sha256=sha(report_path.read_bytes()),draw_stack_bytes=32,enqueue_stack_bytes=40,drain_stack_bytes=48,BIOS_and_display_config_modeled=True,no_HOST_rewrite_between_draw_enqueue_drain=True,tools={Path(__file__).name:sha(Path(__file__).read_bytes())},limits=['CPU isolated fixtures, not natural game input, page transition lifetime, VBlank/scanout or actual Hangul emulator screenshot.','Page0 tile and map lookups changed only in CPU clone; no ROM install or free-space adoption.','Original IWRAM map copy/fill + ROM page lookup/enqueue/drain execute. BIOS CpuFastSet and display configuration are modeled.','Fixture stack bounds are not real game/IRQ budget. Queue95/96 exercise enqueue only, not unknown pre-existing entries.','40jamo grid only; command labels/Latin/space and saves remain unresolved.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']); require_hash(play,a['current_rom_sha256'])
    print('PASS native page draw/transfer CPU candidate',stats,flush=True)


if __name__=='__main__': main()
