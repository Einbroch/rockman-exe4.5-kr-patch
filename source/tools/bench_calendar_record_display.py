"""Native detail consumer -> NEW record decoder -> current count/pixels CPU.

Detail heading and confirmation sprite services modeled. Native fixed-cell
parser executes for representative streams; transfer is intercepted, no VRAM.
No automatic discrimination, save data migration or ROM installation.
"""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB
from hangul_calendar_display_shim import assemble
from hangul_mixed_record import pack_surface
from hangul_mixed_record_display import stream
from hangul_native_tokens import to_native_word

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';reports={};deps={}
    for name in ('cpu_record_display','cpu_editfield_parser','cpu_calendar_record_transfer'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        reports[name]=d;deps[name+'/report.json']=sha(p.read_bytes())
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=reports['cpu_calendar_record_transfer']['current_rom_sha256'];require_hash(play,identity)
    product=ROOT/'poc/output/exe45_ko_development_keyboard_glyphs_v1.gba';glyph_identity=reports['cpu_editfield_parser']['product_sha256'];require_hash(product,glyph_identity);rom=product.read_bytes();manifest=read(product.with_suffix('.json'))
    require_hash(product.with_suffix('.json'),reports['cpu_editfield_parser']['manifest_sha256'])
    overlay=rom[0x1EE700:0x1EFF74]
    if sha(overlay)!=reports['cpu_editfield_parser']['overlay_origin']['sha256']:raise ValueError('native parser overlay identity')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    a,b=0x33C94,0x33CB8;raw=original[a:b];cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ins=list(cs.disasm(raw,0x08000000+a))
    if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('detail native source')
    for i in ins:
        if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('native Thumb1 profile')
        if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native roundtrip')
    if list(cs.disasm(rom[0x33C9A:0x33C9E],0x08033C9A))[0].op_str!='#0x8032ac6':raise ValueError('detail BL guard')
    blob,isa=assemble();patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x8307000',0x08033C9A)[0])
    if len(patch)!=4 or list(cs.disasm(patch,0x08033C9A))[0].op_str!='#0x8307000':raise ValueError('final BL')
    clone=bytearray(rom);clone[0x33C9A:0x33C9E]=patch;clone[0x307000:0x307000+len(blob)]=blob
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    size=(len(clone)+4095)&~4095;u.mem_map(0x08000000,size);u.mem_write(0x08000000,bytes(clone));u.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08F09000,4096);u.mem_write(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes());u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_write(0x03005800,overlay);u.mem_protect(0x03005000,0x2000,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x0FF00000,4096)
    src,pool,ctx,obj,sp,stop=0x0200131A,0x02026080,0x02000400,0x02000500,0x03007EFC,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];heads=[];sprites=[];transfers=[]
    def hook(cpu,a,n,user):
        if a==stop:cpu.emu_stop();return
        if a==0x080554A4:heads.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7)))
        elif a==0x080291C4:
            p=cpu.reg_read(UC_ARM_REG_R2);sprites.append((cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1),bytes(cpu.mem_read(p,6))))
        elif a==0x08000850:transfers.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2)))
        else:return
        cpu.reg_write(UC_ARM_REG_R0,0);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(detail_calls=0,syllable_routes=0,accepted=0,rejected=0,confirmation_counts=0,pixel_consumptions=0,heading_skips=0,whole_EWRAM_checks=0,format_collision_cases=0)
    def packed(words):return pack_surface(bytes([len(words),10,0,255])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words)))))
    def execute(pc,args,stack,preserve=True):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved=[0x13579000+i for i in range(8)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();heads.clear();sprites.clear();transfers.clear()
        u.emu_start(pc|1,stop,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or preserve and any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('native consumer ABI/stack')
    def check(before,regions,stack):
        expected=bytearray(before)
        for a,b in regions:expected[a-0x02000000:a-0x02000000+len(b)]=b
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM/record headers/neighbor fields')
        if any(not(sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(b) for s,b in regions)) for a,n in writes):raise ValueError('write interval')
        stats['whole_EWRAM_checks']+=1
    def pixels(words,row,head):
        # The heading service is modeled. Feed the produced pool stream to
        # the real fixed-cell parser separately, with no HOST stream writes.
        stage,target,font=head[2],head[3],head[6]
        u.mem_write(ctx,bytes(64));u.mem_write(ctx+0x38,struct.pack('<I',obj));u.mem_write(obj,bytes(64))
        before=bytes(u.mem_read(0x02000000,0x40000));u.mem_write(sp-44,b'\x5A'*44);u.reg_write(UC_ARM_REG_CPSR,0x30)
        args=[pool,0xA5,stage,target,10,1,font,0,0,0,ctx,0x1234,0x5678,sp,stop|1]
        rr=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,*regs,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR]
        for r,v in zip(rr,args):u.reg_write(r,v)
        writes.clear();transfers.clear();u.emu_start(0x03006825,stop,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_R0)!=len(words) or bytes(u.mem_read(sp-44,4))!=b'\x5A'*4:raise ValueError('parser ABI/count/stack')
        cells=bytearray()
        for w in tuple(words)+(None,)*(10-len(words)):
            if w is None:at,index=font-0x08000000,0
            elif w<11172:at,index=manifest['fixedcell_extension']['mono_provider']['font_offset'],w
            else:
                v=to_native_word(w);at,index=font-0x08000000,(v>>8)+228 if v&255==228 else v
            cells.extend(rom[at+index*64:at+(index+1)*64])
        wantedobj=bytearray(before[obj-0x02000000:obj-0x02000000+64]);wantedobj[:3]=bytes([10,10,0])
        if transfers!=[(stage,target,640)]:raise ValueError('native transfer request')
        check(before,[(stage,bytes(cells)),(ctx+0x30,bytes(4)),(obj,bytes(wantedobj))],40)
        stats['pixel_consumptions']+=1
    def run(raw,row=0,pixel=False):
        try:wanted=stream(raw,10);valid=True;words=struct.unpack_from('<10H',raw,1)[:raw[0]-128]
        except ValueError:wanted=b'';valid=False;words=()
        u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(src,raw);before=bytes(u.mem_read(0x02000000,0x40000))
        execute(0x08033C94,[src,row],108);check(before,[(pool,wanted)] if valid else [],108)
        if valid:
            archive,stage,target,font=struct.unpack_from('<4I',rom,0x33CB8)
            expectedhead=(archive,72,stage+(row<<10),target+(row<<10),10,1,font,0)
            if heads!=[expectedhead]:raise ValueError('heading consumer request')
            # Existing F9FC-aware counter reads same emitted pool, not fixture.
            before=bytes(u.mem_read(0x02000000,0x40000));execute(0x08032F7C,[10,20],36);check(before,[],36)
            if len(sprites)!=1 or sprites[0][:2]!=(130-4*len(words),20) or sprites[0][2][:2]!=bytes([len(words),1]) or sprites[0][2][4:]!=b'\x02\0':raise ValueError('confirmation count/placement')
            stats['confirmation_counts']+=1
            if pixel:pixels(words,row,expectedhead)
        elif heads:raise ValueError('invalid record consumed stale pool')
        else:stats['heading_skips']+=1
        stats['detail_calls']+=1;stats['accepted' if valid else 'rejected']+=1
    for rank in range(11172):
        run(packed([0]*9+[rank]),rank%2,pixel=rank in (0,229,11171));stats['syllable_routes']+=1
        if rank%2048==0:print('calendar redisplay syllable',rank,flush=True)
    for row in (0,1):
        for count in range(1,11):
            for word in (229,11171,0x80E3,0x81E5):run(packed([word]*count),row,pixel=True)
    good=packed([229]*10)
    for i in range(22):
        bad=bytearray(good);bad[i]^=255;run(bytes(bad))
    for raw in (bytes(22),b'\x80'+b'\xFF'*20+b'\xE5'):run(raw)
    # This valid binary record also has a valid legacy one-byte string prefix
    # 81 E5. Padding validity does not establish automatic format ownership.
    collision=packed([229]);run(collision,pixel=True)
    if collision[:2]!=b'\x81\xE5' or stream(collision,10)==collision[:2]:raise ValueError('format collision not distinguished')
    stats['format_collision_cases']+=1
    out=base/'cpu_calendar_record_display';out.mkdir(exist_ok=True);(out/'shim.bin').write_bytes(blob)
    report=dict(id='exe45.hangul-keyboard.calendar-record-display-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,glyph_rom_sha256=glyph_identity,counts=stats,detail_stack_bytes=108,counter_stack_bytes=36,parser_stack_bytes=40,
        selected_new_format_required=True,heading_and_sprite_and_transfer_modeled=True,no_HOST_pool_rewrite_between_detail_count_pixels=True,
        native_detail=dict(offset=a,bytes=b-a,sha256=sha(original[a:b])),ISA=isa,
        fixture_BL=dict(offset=0x33C9A,expected_hex=rom[0x33C9A:0x33C9E].hex(),final_hex=patch.hex()),
        dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_calendar_display_shim.py','bench_calendar_record_display.py')},artifacts={'shim.bin':sha(blob)},
        limits=['Native33C94 detail wrapper resumes heading after cap10 record->41byte string decode. Invalid records skip heading without rewriting pool or saved-record fixture. Source field22+headers and neighboring fields preserved.',
                'All11172 last-slot Hangul reach same pool and current native F9FC logical counter. Representative fixed parser calls generate exact640byte padded pixels using actual heading mono font arguments; heading/TPL-buffer lookup, sprites and transfer service modeled.',
                'Record source is HOST fixture at observed field0200131A. No actual new-format disk save/reload; row0/1 are bounded fixtures, not full calendar routes.',
                '81 E5 prefix collision proves marker/structural validation alone cannot select format. Caller-selected new-format dispatch unresolved; no global/automatic hook or legacy migration.',
                'No installed ROM code, queue/VRAM/scanout or screenshot; no full pool/default/provider/calendar storage ownership/IRQ budget. Failure skips heading but row clearing/visible error feedback are not established. Existing whole-memory NOT PASS/release false remain.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity);require_hash(product,glyph_identity)
    print('PASS selected calendar detail/count/pixels CPU; NOT screen/save',stats,flush=True)

if __name__=='__main__':main()
