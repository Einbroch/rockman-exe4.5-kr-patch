"""Mixed display -> actual fixed-cell parser/dispatch/copier CPU boundary.

Uses exact existing glyph-only ROM, not a new playable build. Transfer helper
08000850 is intercepted after staging; no VRAM/scanout/game/cache/save proof.
"""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from hangul_mixed_display import CODE, display
from hangul_native_tokens import tag, to_native_word
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB


def main():
    root=ROOT/'analysis/hangul_keyboard_v1';dp=root/'cpu_mixed_display/report.json'
    d=json.loads(dp.read_text(encoding='utf8'))
    if not d['passed'] or d['rom_integrated']:raise ValueError('mixed display scope')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dp.parent/n,h)
    product=ROOT/'poc/output/exe45_ko_development_keyboard_glyphs_v1.gba'
    identity='bc3af1afc5855f8e1161d6a5e5f6cffcfeb66952beb86edcc875107fb9e0d4bd'
    require_hash(product,identity);rom=product.read_bytes()
    manifest=product.with_suffix('.json');m=json.loads(manifest.read_text(encoding='utf8'))
    if m['output_sha256']!=identity or m['hangul_keyboard_glyphs']['input_hooks_installed']:raise ValueError('glyph-only ROM identity')
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    play_hash='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(play,play_hash)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    f=m['fixedcell_extension'];banks={0x08601738:f['font_offset'],0x08619EF8:f['mono_provider']['font_offset']}
    if f['cell_advance']!=8 or f['cell_bytes']!=64:raise ValueError('fixed cell profile')
    overlay=rom[0x1EE700:0x1EFF74];old=bytearray(original[0x1EE700:0x1EFF74])
    table_slot=0x67FC-0x5800  # F9-E5=20, four-byte table entries.
    if int.from_bytes(old[table_slot:table_slot+4],'little')!=0x030069D9:raise ValueError('original resident F9 dispatch')
    planned=[]
    for write in m['expected_writes']:
        at=write['offset'];end=at+write['bytes']
        if end<=0x1EE700 or at>=0x1EFF74:continue
        if not 0x1EE700<=at<end<=0x1EFF74:raise ValueError('overlay writer crosses bound')
        expected=bytes.fromhex(write['expected_hex']);final=bytes.fromhex(write['final_hex'])
        if len(expected)!=write['bytes'] or len(final)!=write['bytes'] or original[at:end]!=expected:raise ValueError('overlay writer source')
        old[at-0x1EE700:end-0x1EE700]=final;planned.append(write)
    if bytes(old)!=overlay:raise ValueError('resident overlay unexplained difference')
    if int.from_bytes(overlay[table_slot:table_slot+4],'little')!=0x08000001+f['hook_offset']:raise ValueError('resident F9 hook lookup')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);scopes=[]
    for start,end in ((0x6824,0x6890),(0x689C,0x68C2),(0x68C8,0x68FE)):
        data=rom[0x1E8F00+start:0x1E8F00+end];ins=list(cs.disasm(data,0x03000000+start))
        if sum(i.size for i in ins)!=len(data):raise ValueError('native parser boundaries')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('native parser ARMv4T')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native parser roundtrip')
        scopes.append(dict(start=hex(0x03000000+start),source_offset=hex(0x1E8F00+start),bytes=len(data),sha256=sha(data)))
    helper,isa=assemble_verified(CODE,0x08F00000,{})
    out=root/'cpu_editfield_parser';out.mkdir(exist_ok=True);(out/'display_helper.bin').write_bytes(helper)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,(len(rom)+4095)&~4095,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08F00000,4096);u.mem_write(0x08F00000,helper);u.mem_protect(0x08F00000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_write(0x03005800,overlay)
    u.mem_protect(0x03005000,0x2000,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x0FF00000,4096)
    surface,stream,stage,ctx,obj,sp,stop=0x02000101,0x02000503,0x02002004,0x02003000,0x02003100,0x03007F00,0x0FF00000
    stats=dict(parser_calls=0,syllable_provider_paths=0,partial_provider_tint_paths=0,native_token_provider_paths=0,mixed_slot_tint_paths=0,full_field_tint_paths=0,transfer_interceptions=0,maximum_emitted_stream_bytes=0)
    writes=[];transfers=[];copiers=[0]
    def write_hook(cpu,access,address,width,value,user):writes.append((address,width))
    def code_hook(cpu,address,size,user):
        if address==0x0300689C:copiers[0]+=1
        if address==0x08000850:
            transfers.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2)))
            # Native transfer's same-mode return is modeled, not BX LR;
            # this mov-lr-pc caller leaves an even LR in Thumb mode.
            stats['transfer_interceptions']+=1;cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_MEM_WRITE,write_hook);u.hook_add(UC_HOOK_CODE,code_hook)
    def cell(word,font):
        if word is None:index=0;at=font-0x08000000
        elif word<11191:
            index=word if word<11172 else word+1;at=banks[font]
        else:
            native=to_native_word(word);index=(native>>8)+0xE4 if native&255==0xE4 else native;at=font-0x08000000
        data=rom[at+index*64:at+(index+1)*64]
        if len(data)!=64:raise ValueError('cell extent')
        return data
    def run(words,font,cap=10,tint=0,cursor=0):
        raw=bytes([len(words),cap,cursor,255])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words))))
        wanted=display(raw,0);u.mem_write(surface,raw);u.mem_write(stream-4,b'\xA7'*49)
        stats['maximum_emitted_stream_bytes']=max(stats['maximum_emitted_stream_bytes'],len(wanted))
        u.mem_write(sp-44,b'\x5A'*44);u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(surface,stream,41,0)):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
        u.emu_start(0x08F00001,stop,count=10000)
        if u.reg_read(UC_ARM_REG_R0)!=len(wanted) or bytes(u.mem_read(stream,len(wanted)))!=wanted or bytes(u.mem_read(surface,24))!=raw:raise ValueError('native display stream')
        if any(not(stream<=a and a+n<=stream+len(wanted) or sp-36<=a and a+n<=sp) for a,n in writes):raise ValueError('display write boundary')
        before_stream=bytes(u.mem_read(stream-4,49))
        # No host writes to stream between emitted display and native parser.
        u.mem_write(stage-4,b'\xA7'*(cap*64+8));u.mem_write(ctx,b'\x00'*64);u.mem_write(ctx+0x38,struct.pack('<I',obj));u.mem_write(obj,b'\x00'*64)
        u.mem_write(sp-44,b'\x5A'*44);u.reg_write(UC_ARM_REG_CPSR,0x30)
        args=[stream,0xA5,stage,0x06010000,cap,1,font,tint*4,0x55,0x66,ctx,0x1234,0x5678,sp,stop|1]
        registers=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR]
        for r,v in zip(registers,args):u.reg_write(r,v)
        writes.clear();transfers.clear();hits=copiers[0]
        u.emu_start(0x03006825,stop,count=20000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_R0)!=len(words) or copiers[0]-hits!=cap:raise ValueError('native parser count/stack/copier')
        if transfers!=[(stage,0x06010000,cap*64)]:raise ValueError(f'native staging transfer boundary {transfers}')
        cells=b''.join(cell(w,font) for w in tuple(words)+(None,)*(cap-len(words)))
        add=0x44444444*tint;pixels=b''.join(struct.pack('<I',(struct.unpack_from('<I',cells,i)[0]+add)&0xFFFFFFFF) for i in range(0,len(cells),4))
        if bytes(u.mem_read(stage-4,cap*64+8))!=b'\xA7'*4+pixels+b'\xA7'*4:raise ValueError('native parser pixels/padding')
        if bytes(u.mem_read(stream-4,49))!=before_stream or bytes(u.mem_read(sp-44,4))!=b'\x5A'*4:raise ValueError('parser stream/stack bounds')
        expected_obj=bytearray(64);expected_obj[:3]=bytes([cap,cap,tint*4])
        if bytes(u.mem_read(obj,64))!=bytes(expected_obj):raise ValueError('parser object metadata/clear extent')
        if any(not(stage<=a and a+n<=stage+cap*64 or obj<=a and a+n<=obj+64 or sp-40<=a and a+n<=sp) for a,n in writes):raise ValueError('parser write boundary')
        stats['parser_calls']+=1
    print('native display -> fixed parser -> selected glyph -> native copier -> padded staging',flush=True)
    for font in banks:
        for rank in range(11172):run([rank],font,cap=1);stats['syllable_provider_paths']+=1
        for rank in range(11172,11191):
            for tint in range(4):run([rank],font,cap=1,tint=tint);stats['partial_provider_tint_paths']+=1
        for token in [bytes([i]) for i in range(228)]+[bytes([228,i]) for i in range(256)]:
            run([tag(token)],font,cap=1);stats['native_token_provider_paths']+=1
        for cap in range(1,11):
            for tint in range(4):
                run([],font,cap=cap,tint=tint)
                for word in (11171,11190):run([word]*cap,font,cap=cap,tint=tint);stats['full_field_tint_paths']+=1
                for slot in range(cap):
                    words=[tag(b'\x9B')]*cap;words[slot]=11190
                    run(words,font,cap=cap,tint=tint,cursor=slot);stats['mixed_slot_tint_paths']+=1
                    words[slot]=11171;run(words,font,cap=cap,tint=tint,cursor=slot+1);stats['mixed_slot_tint_paths']+=1
    glyph_report=root/'glyph_provider_cpu.json';g=json.loads(glyph_report.read_text(encoding='utf8'))
    if g['rom_sha256']!=identity or not g['native_copier_executed'] or g['vectors']!=22718:raise ValueError('font provider evidence identity')
    if stats['maximum_emitted_stream_bytes']!=41:raise ValueError('max field stream not tested')
    report=dict(id='exe45.hangul-keyboard.editfield-parser.v1',passed=True,rom_integrated=False,
        product_sha256=identity,current_play_rom_sha256=play_hash,source_sha256=profile['sha256'],counts=stats,
        cell_advance=8,cell_bytes=64,maximum_display_stream_bytes=41,parser_stack_fixture_bytes=40,transfer_intercepted=True,transfer_destination_fixture='0x06010000',
        overlay_origin=dict(source_offset='0x1EE700',IWRAM='0x03005800',bytes=len(overlay),sha256=sha(overlay),F9_slot='0x030067FC',planned_writes=planned),
        bounded_native_code=scopes,display_helper_ISA=isa,dependencies={'cpu_mixed_display':sha(dp.read_bytes())},
        glyph_provider_report_sha256=sha(glyph_report.read_bytes()),
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['bench_keyboard_editfield_parser.py','hangul_mixed_display.py','extended_dialogue.py','hangul_native_tokens.py']},
        artifacts={'display_helper.bin':sha(helper)},manifest_sha256=sha(manifest.read_bytes()),
        limits=['CPU fixture initializes render arguments/context directly; not observed keyboard font selection or actual game input/runtime.',
                'Transfer08000850 same-mode return is modeled after real padded staging: no upload/VRAM/scanout proof.',
                'No descriptor0 copy/cache41byte ownership, editor layout adoption, cursor draw hook, save or fresh-load support.',
                '484 native structural tokens tested here are not declared active input/glyph membership.',
                '40byte parser stack fixture excludes real transfer and upstream callers/IRQ.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(product,identity);require_hash(source,profile['sha256']);require_hash(play,play_hash)
    print('PASS native edit-field parser CPU',stats,flush=True)


if __name__=='__main__':main()
