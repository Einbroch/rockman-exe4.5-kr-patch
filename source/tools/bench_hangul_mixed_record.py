"""Mixed record encode CPU + selected-format HOST import, not game save proof."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from hangul_mixed_record import assemble_encoder,pack_surface,unpack_selected_record,surface_from_compact
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_display import display
from hangul_mixed_legacy_import import import_legacy
from hangul_record_candidate import pack as old_pack
from hangul_native_tokens import tag


def main():
    root=ROOT/'analysis/hangul_keyboard_v1';dep=root/'cpu_mixed_display/report.json';d=json.loads(dep.read_text(encoding='utf8'))
    if not d['passed'] or d['rom_integrated']:raise ValueError('display dependency')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dep.parent/n,h)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble_encoder();out=root/'cpu_mixed_record';out.mkdir(exist_ok=True);(out/'encoder.bin').write_bytes(blob)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08F04000,4096);u.mem_write(0x08F04000,blob);u.mem_protect(0x08F04000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,8192);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,dst,sp,stop=0x02000101,0x02001103,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(calls=0,rejected=0,word_domain=0,cap10_last_slot_syllables=0,host_roundtrips=0,pure_candidate_compatibility=0,maximum_record_bytes=0)
    def run(raw,available=24,capacity=22,mode=0,source=src,target=dst):
        try:wanted=pack_surface(raw)
        except ValueError:wanted=None
        if available<24 or mode!=0 or wanted is not None and (capacity<len(wanted) or not(source+24<=target or target+len(wanted)<=source)):wanted=None
        u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(source,raw);expected=bytearray(u.mem_read(0x02000000,8192))
        u.mem_write(sp-100,b'\x5A'*100);u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(source,target,available|capacity<<16,mode)):u.reg_write(r,v)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();u.emu_start(0x08F04001,stop,count=10000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_R0)!=(len(wanted) if wanted else 0) or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('record encode ABI')
        if wanted:expected[target-0x02000000:target-0x02000000+len(wanted)]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(expected) or bytes(u.mem_read(sp-100,4))!=b'\x5A'*4:raise ValueError('record encode atomic/bounds')
        if any(not(sp-96<=a and a+n<=sp or wanted is not None and target<=a and a+n<=target+len(wanted)) for a,n in writes):raise ValueError('record unexpected write')
        stats['calls']+=1;stats['rejected']+=wanted is None
        if wanted:
            # HOST import of actual emitted bytes; not native decoder evidence.
            saved=bytes(u.mem_read(target,len(wanted)));loaded=unpack_selected_record(saved,raw[1])
            if display(surface_from_compact(loaded),1)!=display(raw,1):raise ValueError('committed identity redisplay')
            stats['host_roundtrips']+=1;stats['maximum_record_bytes']=max(stats['maximum_record_bytes'],len(wanted))
        return wanted
    def surface(words,cap=4,cursor=0,active=255):
        return bytes([len(words),cap,cursor,active])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words))))
    for w in range(65536):
        run(surface([w]));stats['word_domain']+=1
    for rank in range(11172):
        run(surface([0]*9+[rank],10));stats['cap10_last_slot_syllables']+=1
    for cap in range(1,11):
        for count in range(cap+1):
            for w in (0,11171,11172,11190,tag(b'\x9B'),tag(b'\xE4\x98'),tag(b'\xE4\xE5')):
                raw=surface([w]*count,cap);result=run(raw)
                if result and w<11172 and cap<=8:
                    if result!=old_pack(chr(0xAC00+w)*count,cap):raise ValueError('pure wire compatibility')
                    stats['pure_candidate_compatibility']+=1
        raw=surface([0],cap)
        for n in range(2*cap+2):run(raw,capacity=n)
    valid=surface([0])
    for i in range(24):
        r=bytearray(valid);r[i]^=255;run(bytes(r))
    for n in range(24):run(valid,available=n)
    for mode in (1,2,255):run(valid,mode=mode)
    for delta in range(-9,24):run(valid,target=src+delta)
    for a in range(4):
        for b in range(4):run(valid,source=src+a,target=dst+b)
    for cap in range(1,11):
        for value in range(256):
            good=pack_surface(surface([229],cap))
            for raw in (bytes([value])+good[1:],good[:-1]+bytes([value])):
                try:decoded=unpack_selected_record(raw,cap)
                except ValueError:continue
                if raw!=good:raise ValueError('selected record structural rejection')
    collision=pack_surface(surface([229],4))
    if MixedReplay.restore(import_legacy(collision,4)).model.state.cells!=():raise ValueError('legacy ambiguity reproduction')
    # Execute the unchanged original importer as well, not only the HOST model.
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source_path=ROOT/profile['filename'];require_hash(source_path,profile['sha256']);original=source_path.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    play_hash='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(play,play_hash)
    if play.read_bytes()[0x3558C:0x355BE]!=original[0x3558C:0x355BE]:raise ValueError('original importer changed')
    u.mem_map(0x08000000,len(original));u.mem_write(0x08000000,original)
    u.mem_protect(0x08000000,len(original),UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x0200F000,4096)
    editor,cells=0x0200FC40,0x0200FC60
    u.mem_write(src,collision);u.mem_write(editor,b'\xA7'*96)
    for offset in (16,20,24):u.mem_write(editor+offset,struct.pack('<I',cells))
    expected=bytearray(u.mem_read(editor,96));expected[32:34]=b'\xE5\x00'
    u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_R0,src)
    saved=[editor]+[0x13579000+i for i in range(1,len(regs))]
    for r,v in zip(regs,saved):u.reg_write(r,v)
    u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1)
    u.mem_write(sp-8,b'\x5A'*8);writes.clear();u.emu_start(0x0803558D,stop,count=10000)
    if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)):raise ValueError('original ambiguity ABI')
    if bytes(u.mem_read(editor,96))!=bytes(expected) or bytes(u.mem_read(src,len(collision)))!=collision or bytes(u.mem_read(sp-8,4))!=b'\x5A'*4:raise ValueError('original ambiguity output')
    if any(not(cells<=a and a+n<=cells+2 or editor+24<=a and a+n<=editor+28 or sp-4<=a and a+n<=sp) for a,n in writes):raise ValueError('original ambiguity write bound')
    report=dict(id='exe45.hangul-keyboard.mixed-record-candidate.v1',passed=True,rom_integrated=False,format_adopted=False,caller_selected_new_format_required=True,native_encoder=True,native_record_importer=False,encoder_bytes=len(blob),own_stack_bytes=60,nested_stack_bytes=96,max_record_bytes=22,counts=stats,legacy_ambiguity_counterexample=dict(record_hex=collision.hex(),new_identity='곥',legacy_identity='empty',reason='Legacy importer ignores first marker and terminates at byte1 E5; marker alone is not established discrimination.'),dependencies={'cpu_mixed_display':sha(dep.read_bytes())},ISA=isa,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['hangul_mixed_record.py','bench_hangul_mixed_record.py','hangul_mixed_display.py','hangul_mixed_cache_bridge.py','hangul_mixed_replay_state.py','hangul_mixed_editor.py','hangul_mixed_legacy_import.py','hangul_record_candidate.py']},artifacts={'encoder.bin':sha(blob)},limits=['Record width2*cap+2 follows proposed fixed-width contract, not proven adopted extent of every game field or native save serialization.','Structural484 native tokens are not keyboard/glyph/save membership; partial/empty rejection covered, no player-facing confirmation hook.','Actual encoded bytes are imported/redisplayed by HOST only. Native packed-record importer, format discriminator/migration, native normalize bypass and all redisplay/save/fresh-load consumers remain unimplemented.','Caller-owned surface/output/disjoint stack only; no ROM/RAM ownership adoption, product build writes or runtime Hangul screen.'])
    report.update(source_sha256=profile['sha256'],current_rom_sha256=play_hash,
                  original_import_leaf_sha256=sha(original[0x3558C:0x355BE]),
                  legacy_counterexample_original_leaf_executed=True)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS mixed committed record CPU encode / HOST selected import',stats,'automatic legacy discrimination NOT adopted',flush=True)


if __name__=='__main__':main()
