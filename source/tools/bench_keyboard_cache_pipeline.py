"""Actual compact edit/cache -> native20-cell parser -> queue -> BIOS-model copy.

CPU integration fixture, NOT an installed keyboard hook or emulator screen.
Native queue code runs; only CpuFastSet BIOS semantics are modeled.
"""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from hangul_mixed_cache_bridge import assemble as cache_assemble, stream
from hangul_mixed_keyedit_thumb import assemble as edit_assemble
from hangul_mixed_replay_state import MixedReplay, KEYS
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag, to_native_word
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB


def main():
    root=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_cache_bridge','cpu_mixed_keyedit','cpu_editfield_parser','cpu_composer'):
        path=root/name/'report.json';r=json.loads(path.read_text(encoding='utf8'))
        if not r['passed'] or r['rom_integrated']:raise ValueError('pipeline dependency scope')
        for n,h in r['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in r['artifacts'].items():require_hash(path.parent/n,h)
        deps[name]=sha(path.read_bytes())
    life=root/'transfer_lifetime.json';l=json.loads(life.read_text(encoding='utf8'))
    if not l['passed'] or l['font']!='0x08619EF8' or l['render_cells']!=20:raise ValueError('native route evidence')
    require_hash(ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba',l['rom_sha256'])
    for n,h in l['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in l['artifacts'].items():require_hash(ROOT/n,h)
    product=ROOT/'poc/output/exe45_ko_development_keyboard_glyphs_v1.gba'
    identity='bc3af1afc5855f8e1161d6a5e5f6cffcfeb66952beb86edcc875107fb9e0d4bd'
    require_hash(product,identity);rom=product.read_bytes()
    manifest=product.with_suffix('.json');m=json.loads(manifest.read_text(encoding='utf8'))
    parser=json.loads((root/'cpu_editfield_parser/report.json').read_text(encoding='utf8'))
    if m['output_sha256']!=identity or parser['product_sha256']!=identity:raise ValueError('font identity')
    require_hash(manifest,parser['manifest_sha256'])
    overlay=rom[0x1EE700:0x1EFF74]
    if sha(overlay)!=parser['overlay_origin']['sha256']:raise ValueError('verified overlay')
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    scopes=[];cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    for a,b in ((0x7D4,0x846),(0x848,0x880),(0x97C,0x98A),(0xEC140,0xEC144)):
        data=rom[a:b];ins=list(cs.disasm(data,0x08000000+a))
        if data!=original[a:b] or sum(i.size for i in ins)!=len(data):raise ValueError('native queue source')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('native Thumb profile')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('queue roundtrip')
        scopes.append(dict(offset=a,bytes=len(data),sha256=sha(data)))
    cache,cache_isa=cache_assemble();edit,edit_isa=edit_assemble(0x08F02000)
    if sha(cache)!=json.loads((root/'cpu_cache_bridge/report.json').read_text(encoding='utf8'))['artifacts']['helper.bin']:raise ValueError('cache binary agreement')
    out=root/'cpu_cache_pipeline';out.mkdir(exist_ok=True)
    (out/'cache.bin').write_bytes(cache);(out/'edit.bin').write_bytes(edit)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    n=(len(rom)+4095)&~4095;u.mem_map(0x08000000,n);u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,n,UC_PROT_READ|UC_PROT_EXEC)
    for pc,blob in ((0x08F01000,cache),(0x08F02000,edit)):
        u.mem_map(pc,4096);u.mem_write(pc,blob);u.mem_protect(pc,4096,UC_PROT_READ|UC_PROT_EXEC)
    table=(root/'cpu_composer/transitions.bin').read_bytes();n=(len(table)+4095)&~4095
    u.mem_map(0x09000000,n);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,n,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_write(0x03005800,overlay)
    u.mem_protect(0x03005000,0x2000,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x06000000,0x20000);u.mem_map(0x0FF00000,4096)
    src,dst,stage,ctx,obj,sp,stop=0x0200FC54,0x020155F0,0x0201E800,0x0200FBE0,0x02003000,0x03007F00,0x0FF00000
    counter,queue,target=0x02010724,0x02012730,0x0600B000
    regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
    writes=[];bios_calls=[];stats=dict(renders=0,native_key_actions=0,rejected_key_actions=0,history_pop_actions=0,queue_saturation_rejections=0,maximum_stream_bytes=0)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def code_hook(cpu,pc,size,user):
        if pc==0x080EC140:
            a,b,c=(cpu.reg_read(r) for r in regs[:3])
            if (a,b,c)!=(stage,target,320):raise ValueError('unexpected CpuFastSet request')
            bios_calls.append((a,b,c));cpu.mem_write(b,bytes(cpu.mem_read(a,c*4)))
            # Service modeled, normal source BX LR still executes.
            cpu.reg_write(UC_ARM_REG_PC,0x080EC143)
    u.hook_add(UC_HOOK_CODE,code_hook)
    def call(pc,args,stack):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        for i,r in enumerate(regs):u.reg_write(r,args[i] if i<len(args) else 0x13579000+i)
        expected={r:u.reg_read(r) for r in regs[4:12]}
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
        u.emu_start(pc|1,stop,count=60000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('pipeline return/stack')
        return u.reg_read(UC_ARM_REG_R0),expected
    def allow(ranges):
        if any(not any(lo<=a and a+n<=hi for lo,hi in ranges) for a,n in writes):raise ValueError('unexpected pipeline write')
    def glyph(w):
        if w is None:at=0x619EF8;index=0
        elif w<11191:at=m['fixedcell_extension']['mono_provider']['font_offset'];index=w if w<11172 else w+1
        else:
            at=0x619EF8;v=to_native_word(w);index=(v>>8)+0xE4 if v&255==0xE4 else v
        return rom[at+index*64:at+(index+1)*64]
    def render(c,tint=0,saturate=False):
        raw=c.serialize()
        if bytes(u.mem_read(src,76))!=raw:raise ValueError('CPU edit state not retained')
        wanted=stream(raw);u.mem_write(dst-4,b'\xA7'*49)
        value,saved=call(0x08F01000,[src,dst,76|41<<16,0x09000000],112)
        if value!=len(wanted) or bytes(u.mem_read(dst-4,49))!=b'\xA7'*4+wanted+b'\xA7'*(45-len(wanted)) or any(u.reg_read(r)!=v for r,v in saved.items()):raise ValueError('cache ABI/output')
        allow([(dst,dst+len(wanted)),(sp-112,sp)])
        saved_stream=bytes(u.mem_read(dst-4,49));u.mem_write(stage-4,b'\xA7'*1288);u.mem_write(target-4,b'\xA7'*1288)
        u.mem_write(ctx,b'\0'*64);u.mem_write(ctx+0x38,struct.pack('<I',obj));u.mem_write(obj,b'\0'*64)
        u.mem_write(counter,struct.pack('<I',96 if saturate else 0));u.mem_write(queue,b'\xA7'*1920)
        value,_=call(0x03006824,[dst,0xA5,stage,target,20,1,0x08619EF8,tint*4,0x55,0x66,ctx],56)
        cells=c.model.state.cells;pixels=b''.join(glyph(w) for w in cells+(None,)*(20-len(cells)))
        pixels=b''.join(struct.pack('<I',(struct.unpack_from('<I',pixels,i)[0]+0x44444444*tint)&0xFFFFFFFF) for i in range(0,1280,4))
        if value!=len(cells) or bytes(u.mem_read(stage-4,1288))!=b'\xA7'*4+pixels+b'\xA7'*4 or bytes(u.mem_read(target-4,1288))!=b'\xA7'*1288:raise ValueError('parser stage/deferred semantics')
        allow([(stage,stage+1280),(obj,obj+64),(ctx+0x30,ctx+0x34),(counter,counter+4),(queue,queue+20),(sp-56,sp)])
        if saturate:
            if bytes(u.mem_read(queue,1920))!=b'\xA7'*1920 or struct.unpack('<I',u.mem_read(counter,4))[0]!=96:raise ValueError('queue full handling')
            stats['queue_saturation_rejections']+=1
        else:
            if struct.unpack('<5I',u.mem_read(queue,20))!=(stage,target,1280,0xFFFFFFFF,2) or struct.unpack('<I',u.mem_read(counter,4))[0]!=1:raise ValueError('native enqueue record')
            bios_calls.clear();call(0x080007DC,[],48);allow([(counter,counter+4),(sp-48,sp)])
            if bios_calls!=[(stage,target,320)] or bytes(u.mem_read(target-4,1288))!=b'\xA7'*4+pixels+b'\xA7'*4 or struct.unpack('<I',u.mem_read(counter,4))[0]!=0:raise ValueError('queue drain/BIOS-model output')
        if bytes(u.mem_read(src,76))!=raw or bytes(u.mem_read(dst-4,49))!=saved_stream:raise ValueError('source/cache lifetime')
        stats['renders']+=1;stats['maximum_stream_bytes']=max(stats['maximum_stream_bytes'],len(wanted))
    for cap in range(1,11):
        for n in range(cap+1):
            for word in (0,11171,11172,11190,tag(b'\x9B'),tag(b'\xE4\x98'),tag(b'\xE4\xE5')):
                c=MixedReplay(cap);c.model.state=Snapshot((word,)*n,0,None);c._rebase();u.mem_write(src,c.serialize());render(c)
        for tint in range(4):
            c=MixedReplay(cap);c.load((11171,)*cap);u.mem_write(src,c.serialize());render(c,tint)
    c=MixedReplay(10);u.mem_write(src,c.serialize())
    for action in [KEYS.index(k) for k in 'ㄱㄱㅗㅏㅣㄹㄱ'*10]+[40]*70+[40,41,65535]:
        old=c.serialize();accepted=c.backspace() if action==40 else c.press(KEYS[action]) if action<40 else False
        value,saved=call(0x08F02000,[src,action,76,0x09000000],196)
        if value!=int(accepted) or bytes(u.mem_read(src,76))!=c.serialize() or any(u.reg_read(r)!=v for r,v in saved.items()):raise ValueError('uninterrupted CPU keyedit')
        allow([(src,src+76),(sp-196,sp)])
        stats['native_key_actions']+=1;stats['rejected_key_actions']+=not accepted;stats['history_pop_actions']+=action==40 and accepted
        render(c)
    c=MixedReplay(10);c.load((11171,)*10);u.mem_write(src,c.serialize());render(c,saturate=True)
    report=dict(id='exe45.hangul-keyboard.cache-pipeline.v1',passed=True,rom_integrated=False,product_sha256=identity,source_sha256=profile['sha256'],counts=stats,render_cells=20,transfer_bytes=1280,parser_with_enqueue_stack_bytes=56,queue_drain_stack_bytes=48,edit_stack_bytes=196,cache_stack_bytes=112,BIOS_service_modeled=True,transfer_intercepted=False,dependencies=deps,transfer_lifetime_report_sha256=sha(life.read_bytes()),manifest_sha256=sha(manifest.read_bytes()),ISA=dict(cache=cache_isa,edit=edit_isa),native_code=scopes,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['bench_keyboard_cache_pipeline.py','hangul_mixed_cache_bridge.py','hangul_mixed_keyedit_thumb.py','hangul_mixed_replay_state.py','hangul_mixed_editor.py','hangul_native_tokens.py']},artifacts={n:sha((out/n).read_bytes()) for n in ['cache.bin','edit.bin']},limits=['CPU fixture owns all RAM and render arguments: does not adopt native cache41 extent, hook ABI or game/IRQ stack budget.','Real parser/copier/queue enqueue/drain code executes, but BIOS CpuFastSet is modeled and no VBlank timing/scanout/emulator Hangul screen is established.','20-cell mono route from native observations; source receives initial fixture states. After initial setup70 edits and70 pops reach pixels without host rewriting state/cache/stage.','Native structural tokens are not proof of input/glyph membership; no commit/record/save/fresh-load implementation.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(product,identity);require_hash(source,profile['sha256'])
    print('PASS compact CPU edit/cache -> original20-cell parser/queue -> modeled BIOS',stats,flush=True)


if __name__=='__main__':main()
