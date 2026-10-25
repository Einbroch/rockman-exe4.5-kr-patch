"""Guarded page2 selector/CPU shim candidate; does not install a ROM hook."""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from hangul_keyboard_action_shim import CODE
from hangul_native_tokens import tag
from extended_dialogue import assemble_verified, Cs, CS_ARCH_ARM, CS_MODE_THUMB
from bench_hangul_composer_thumb import *


def assemble(address=0x08303000):
    page='cmp r2, #0\nbne action_handled'
    command='cmp r1, #3\nbne action_handled\nmovs r1, #41'
    if CODE.count(page)!=1 or CODE.count(command)!=1:raise ValueError('action source contract')
    code=CODE.replace(page,'''cmp r2, #2
beq action_latin
cmp r2, #1
bhi action_handled''').replace(command,'''cmp r1, #3
beq action_left
cmp r1, #4
bne action_handled
movs r1, #128
lsls r1, r1, #8
b action_dispatch
action_left:
movs r1, #41''')
    code=code.replace('action_command:', '''action_latin:
movs r2, #15
muls r1, r2, r1
adds r1, r1, r0
lsls r1, r1, #1
ldr r2, latin
ldrh r1, [r2, r1]
ldr r2, inactive
cmp r1, r2
beq action_handled
b action_dispatch
action_command:''')
    return assemble_verified(code,address,dict(editor=0x0200FC40,selectors=0x09301000,
        latin=0x09301100,inactive=0xFFFF,context=0x09300000,helper=0x08F0D001))


def main():
    base=ROOT/'analysis/hangul_keyboard_v1';out=base/'latin_input';out.mkdir(exist_ok=True)
    p=base/'keyboard_labels/report.json';d=read(p)
    if not d['passed'] or d['rom_integrated']:raise ValueError('label dependency scope')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(p.parent/n,h)
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename']
    require_hash(source,profile['sha256']);rom=source.read_bytes()
    legacy=read(base/'legacy_edit.json');page=legacy['selector_table']['pages'][2]
    table=struct.unpack_from('<I',rom,0x35748)[0]-0x08000000
    off=table+struct.unpack_from('<H',rom,table+8)[0];tokens=[];positions=[];end=off
    while rom[end]!=0xE5:
        positions.append(end);n=2 if rom[end]==0xE4 else 1
        tokens.append(rom[end:end+n]);end+=n
        if len(tokens)>90:raise ValueError('page2 selector extent')
    if len(tokens)!=75 or [t.hex() for t in tokens]!=page['tokens'] or sha(rom[off:end+1])!=page['region_sha256']:
        raise ValueError('guarded source page2 changed')
    tbl=ROOT/'external/textpet-plugins/exe45-utf8.tbl'
    mapping=dict(line.split('=',1) for line in tbl.read_text(encoding='utf-8-sig').splitlines() if '=' in line)
    # Execute the original row*15+column and variable-width token walker.
    # Stop before native overwrite; no legacy editor or save is mutated.
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ins=list(cs.disasm(rom[0x354A0:0x354C8],0x080354A0))
    if sum(i.size for i in ins)!=40:raise ValueError('native picker instruction extent')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,4096);ed=0x02000000
    for i,pos in enumerate(positions):
        u.mem_write(ed+6,bytes([i%15,i//15,2]));before=bytes(u.mem_read(ed,4096))
        u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_R4,ed)
        u.emu_start(0x080354A1,0x080354C8,count=2000)
        if u.reg_read(UC_ARM_REG_PC)!=0x080354C8 or u.reg_read(UC_ARM_REG_R3)!=0x08000000+pos or bytes(u.mem_read(ed,4096))!=before:
            raise ValueError('native cell-to-token picker')
    words=[tag(t) if t!=b'\0' else 0xFFFF for t in tokens]+[0xFFFF]*15
    cells=[dict(index=i,column=i%15,row=i//15,active=w!=0xFFFF,
                token_hex=tokens[i].hex() if i<75 else None,
                source_character=mapping[tokens[i].hex().upper()] if i<75 else None,
                canonical_identity=w if w!=0xFFFF else None) for i,w in enumerate(words)]
    # Independently traverse original skip data, not candidate input code.
    skip=struct.unpack_from('<I',rom,0x35148)[0]-0x08000000;end_skip=skip
    entries={}
    while rom[end_skip]!=255:
        e=rom[end_skip:end_skip+12];entries[tuple(e[:2])]=e;end_skip+=12
        if end_skip-skip>1200:raise ValueError('skip table extent')
    seen={(0,0)};queue=[(0,0)]
    for x,y in queue:
        for j,(nx,ny) in zip((2,4,6,8),((x,(y-1)%6),(x,(y+1)%6),((x-1)%16,y),((x+1)%16,y))):
            target=tuple(entries[(nx,ny)][j:j+2]) if (nx,ny) in entries else (nx,ny)
            if target not in seen:seen.add(target);queue.append(target)
    active={(c['column'],c['row']) for c in cells if c['active']}
    blank={(c['column'],c['row']) for c in cells if not c['active']}
    if not active<=seen or blank&seen or len(active)!=56:raise ValueError('native navigation/active selector agreement')
    blob,isa=assemble();(out/'shim.bin').write_bytes(blob)
    (out/'selectors.bin').write_bytes(struct.pack('<90H',*words))
    report=dict(passed=True,rom_integrated=False,source_sha256=profile['sha256'],
        dependencies={'keyboard_labels/report.json':sha(p.read_bytes())},cells=cells,
        native_picker=dict(start=0x354A0,bytes=40,sha256=sha(rom[0x354A0:0x354C8]),CPU_calls=75,
            instruction_listing=[dict(address=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]),
        native_table=dict(offset=off,bytes=end+1-off,sha256=sha(rom[off:end+1])),
        native_navigation=dict(offset=skip,bytes=end_skip+1-skip,sha256=sha(rom[skip:end_skip+1]),
            active_reachable=56,inactive_reachable=0),native_table_sha256=sha(tbl.read_bytes()),
        active_cells=56,inactive_cells=34,ISA=isa,
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in
            ('prepare_keyboard_latin_input.py','hangul_keyboard_action_shim.py','hangul_native_tokens.py')},
        artifacts={n:sha((out/n).read_bytes()) for n in ('shim.bin','selectors.bin')},
        limits=['Selector candidate: 26 uppercase Latin letters, 10 digits, 20 original symbols. No lowercase repertoire expansion.',
            'Source space placeholders disabled; dedicated Korean-labelled space command remains available.',
            'Native picker execution proves token coordinates, not new shim/editor integration, scanout, confirmation or persistence.',
            'Fixture addresses are not adopted ROM/RAM placement. No ROM or save modification.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);print('PASS native picker75; active Latin/digit/symbol56, inactive34')


if __name__=='__main__':main()
