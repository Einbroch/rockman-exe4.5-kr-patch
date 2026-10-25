"""Bounded native reader marker execution + existing normal-route records.

Not automatic discrimination, all legacy writers, or save compatibility proof.
CPU starts after the game's prerequisite flag gate and stops before RNG.
"""
import json,struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';inventory_path=base/'consumer_inventory.json'
    inv=read(inventory_path);require_hash(ROOT/'tools/analyze_keyboard_consumers.py',inv['tool_sha256'])
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=inv['current_rom_sha256'];require_hash(product,identity);play=product.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ins=[]
    for i in cs.disasm(rom[0x38BAA:0x38BD2],0x08038BAA):
        code=rom[i.address-0x08000000:i.address-0x08000000+i.size]
        if i.size!=2 or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=code:raise ValueError('reader ISA roundtrip')
        ins.append(dict(pc=hex(i.address),hex=code.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    if sum(len(bytes.fromhex(x['hex'])) for x in ins)!=40:raise ValueError('reader instruction coverage')
    # Normalize ends at32AD8; the following font literal is already patched.
    regions=[dict(offset=a,bytes=b-a,sha256=sha(rom[a:b])) for a,b in [(0x38BAA,0x38BD2),(0x35000,0x35034),(0x3558C,0x355BE),(0x32AC6,0x32AD8)]]
    for r in regions:
        a=r['offset'];b=a+r['bytes']
        if play[a:b]!=rom[a:b]:raise ValueError('native marker code changed')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096)
    sp=0x03007F00;writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    counts=dict(reader_calls=0,zero_marker_skipped=0,nonzero_marker_selected=0)
    for row in inv['metadata_rows']:
        at=row['metadata_offset'];raw=rom[at:at+16]
        if raw.hex()!=row['metadata_hex']:raise ValueError('metadata identity')
        count,cap=raw[0],raw[2];stride=cap*2+2;start=int(row['field_start'],16)
        if count>16:raise ValueError('native selected-index scratch capacity')
        for slot in range(count):
            for marker in range(256):
                u.mem_write(start,bytes(count*stride));u.mem_write(start+slot*stride,bytes([marker]))
                before=bytes(u.mem_read(start,count*stride));u.mem_write(sp-4,b'\x5A'*40)
                u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_R6,0x08000000+at);u.reg_write(UC_ARM_REG_R7,sp)
                u.reg_write(UC_ARM_REG_SP,sp);writes.clear();u.emu_start(0x08038BAB,0x08038BD2,count=1000)
                if u.reg_read(UC_ARM_REG_PC)!=0x08038BD2 or u.reg_read(UC_ARM_REG_SP)!=sp:raise ValueError('reader loop boundary')
                scratch=bytes(u.mem_read(sp,32));expected=1 if marker else 0
                if scratch[17]!=expected or marker and scratch[0]!=slot:raise ValueError('reader marker semantics')
                if bytes(u.mem_read(start,count*stride))!=before or bytes(u.mem_read(sp-4,4))!=b'\x5A'*4 or bytes(u.mem_read(sp+32,4))!=b'\x5A'*4:raise ValueError('reader bounded writes')
                if any(not(sp<=a and a+n<=sp+32) for a,n in writes):raise ValueError('reader unexpected write')
                counts['reader_calls']+=1;counts['zero_marker_skipped']+=marker==0;counts['nonzero_marker_selected']+=marker!=0
    route=ROOT/'poc/runtime/hangul-keyboard-v1-buffer-writers';result=verify_route(route,identity,set())
    observations=[];markers=Counter();artifacts={str((route/'result.json').relative_to(ROOT)).replace('\\','/'):sha((route/'result.json').read_bytes())}
    for step in result['capture_steps']:
        path=route/f'step_{step:03d}_gbaExtWorkRam.bin';data=path.read_bytes()
        if len(data)!=0x40000:raise ValueError('EWRAM snapshot extent')
        artifacts[str(path.relative_to(ROOT)).replace('\\','/')]=sha(data)
        for row in inv['metadata_rows']:
            start=int(row['field_start'],16)-0x02000000;stride=row['derived_native_stride']
            for slot in range(row['count']):
                record=data[start+slot*stride:start+(slot+1)*stride]
                if len(record)!=stride:raise ValueError('record snapshot extent')
                markers[record[0]]+=1
                observations.append(dict(step=step,descriptor=row['descriptor_index'],slot=slot,address=hex(0x02000000+start+slot*stride),marker=record[0],record_hex=record.hex()))
    report=dict(id='exe45.hangul-keyboard.record-marker-analysis.v1',passed=True,rom_integrated=False,
                format_discriminator_adopted=False,source_sha256=profile['sha256'],current_rom_sha256=identity,
                counts=counts,metadata_rows=len(inv['metadata_rows']),reader_loop_start='0x08038BAA',reader_loop_end='0x08038BD2',
                prerequisite_gate_executed=False,RNG_selection_executed=False,
                observed_snapshot_count=len(result['capture_steps']),observed_markers=dict(sorted(markers.items())),
                observations=observations,native_code=regions,instructions=ins,
                inventory_sha256=sha(inventory_path.read_bytes()),tools={'analyze_keyboard_record_markers.py':sha((ROOT/'tools/analyze_keyboard_record_markers.py').read_bytes())},artifacts=artifacts,
                confirmed=['Bounded original selector includes any nonzero marker, not a format enum or bit1-only flag.',
                           'Original writer0803500A..3500C sets marker1; original importer ignores it. This does not establish every legacy writer or save value.',
                           'All existing observed marker values describe only selected normal-route snapshots. They do not reserve other values for a new format.'],
                limits=['26 metadata rows and their slots only; starts after prerequisite gate and stops before RNG/BIOS division/normalize. No full reader ABI or game-flow execution claim.',
                        'RAM record snapshots are not raw persistent save representation or migration coverage.',
                        'No automatic format discrimination adopted; all writers/import/default/save consumers must be accounted for before installing mixed-record hooks.'])
    (base/'record_markers.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS bounded marker selector',counts,'observed markers',dict(markers),'automatic discrimination NOT adopted',flush=True)

if __name__=='__main__':main()
