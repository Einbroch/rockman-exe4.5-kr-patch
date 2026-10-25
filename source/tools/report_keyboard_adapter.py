"""Bind bounded normal native editor ownership and caller evidence."""
import json,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    route=ROOT/'poc/runtime/hangul-keyboard-v1-adapter'
    result=read(route/'result.json');verify_route(route,identity,set())
    require_hash(Path(result['rom_path']),identity);rom=Path(result['rom_path']).read_bytes()
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    env=read(route/'adapter_environment.json')
    for path,key in [('capture_keyboard_adapter.py','tool_sha256'),('capture_keyboard_native.py','native_observer_sha256')]:require_hash(ROOT/'tools'/path,env[key])
    if not env['observer_only'] or env['window']!=[0x0200fc60,0x0200fca0]:raise ValueError('observer scope')
    trace=read(route/'step_023_adapter.json');snapshots=[]
    for step in result['capture_steps']:
        ram=(route/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        snapshots.append(dict(step=step,script=ram[0xfa21],editor_mode=ram[0xfc40],cursor=hex(struct.unpack_from('<I',ram,0xfc54)[0]),end=hex(struct.unpack_from('<I',ram,0xfc58)[0]),words_hex=ram[0xfc60:0xfc70].hex(),flat_hex=ram[0xfc80:0xfc90].hex(),record_hex=ram[0x10a6:0x10b0].hex()))
    bystep={s['step']:s for s in snapshots}
    if bystep[1]['script']!=29 or bystep[4]['editor_mode']!=12 or bystep[14]['editor_mode']!=16 or bystep[17]['editor_mode']!=12 or bystep[21]['script']!=93:raise ValueError('normal editor/No/Yes route')
    if bystep[5]['words_hex']!=bystep[10]['words_hex'] or bystep[8]['words_hex']==bystep[10]['words_hex'] or bystep[17]['words_hex']!=bystep[10]['words_hex']:raise ValueError('input/B/No preserves draft')
    if not bystep[21]['record_hex'].startswith('019be5'):raise ValueError('native commit')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);instructions=[]
    observed=sorted({a['pc'] for a in trace['accesses']}|{a['pc'] for a in trace['calls']})
    for pc in observed:
        offset=pc-0x08000000
        if original[offset:offset+4]!=rom[offset:offset+4]:raise ValueError('native observed instruction changed')
        ins=next(decoder.disasm(rom[offset:offset+4],pc),None)
        if ins is None or ins.size!=2:raise ValueError('observed Thumb-1 boundary')
        instructions.append(dict(pc=hex(pc),hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
    reads=[a for a in trace['accesses'] if a['pc']==0x0800094e and a['kind']=='read']
    if len(reads)!=2 or min(a['min'] for a in reads)!=0x0200fc80 or max(a['max'] for a in reads)!=0x0200fc9f or any(a['lr']!=0x03006a4c for a in reads):raise ValueError('flattened display copy not observed')
    iwram=(route/'step_004_gbaIntWorkRam.bin').read_bytes()
    code=list(decoder.disasm(iwram[0x6a1c:0x6a60],0x03006a1c))
    if not any(i.address==0x03006a4a and i.mnemonic=='bx' and i.op_str=='r3' for i in code):raise ValueError('IWRAM copy caller')
    descriptor=struct.unpack_from('<II',rom,0x526d0)
    if descriptor!=(0x0200fc80,32):raise ValueError('editor descriptor0')
    init=original[0x355b6:0x355f6]
    if init!=rom[0x355b6:0x355f6] or original[0x3574c:0x35750]!=struct.pack('<I',0x0200fc40):raise ValueError('native initializer baseline')
    init_code=list(decoder.disasm(init,0x080355b6))
    if not any(i.address==0x080355be and i.mnemonic=='movs' and i.op_str=='r1, #0x60' for i in init_code):raise ValueError('initializer clear width')
    call=next(a for a in trace['calls'] if a['pc']==0x080353b0)
    sp=call['sp'];bottom=sp-444
    out=ROOT/'analysis/hangul_keyboard_v1/adapter.json'
    report=dict(id='exe45.hangul-keyboard.adapter-observation.v1',passed=True,rom_integrated=False,claim='bounded native editor callers, display-copy ownership and normal B/No/Yes transitions; no adopted Hangul RAM/stack ABI',rom_sha256=identity,source_sha256=profile['sha256'],route='poc/runtime/hangul-keyboard-v1-adapter',snapshots=snapshots,observed_calls=trace['calls'],observed_accesses=trace['accesses'],observed_instructions=instructions,native_initializer=dict(address='0x080355b6',clear_start='0x0200fc40',clear_bytes=96,code_sha256=sha(init),observed_on_route=any(a['pc']==0x080355b6 for a in trace['calls'])),display_copy=dict(descriptor_index=0,pointer=hex(descriptor[0]),bytes=descriptor[1],native_copy='0x0800094c',IWRAM_caller='0x03006a4a',IWRAM_slice_sha256=sha(iwram[0x6a1c:0x6a60])),compact_overlay_candidate=dict(start='0x0200fc60',end_exclusive='0x0200fca0',bytes=64,adopted=False,requires_coordinated_replacement=['word-cell insert/delete and pointer counts','per-frame padding/flattening','descriptor0 display-copy source','validation/commit/imported-record readers']),stack_candidate=dict(editor_entry_sp=hex(sp),wrapper_bytes=444,bottom_if_called_directly=hex(bottom),adopted=False,reason='Observed SP is four-byte but not eight-byte aligned; shim/IRQ/data ownership and maximum stack depth remain unresolved.'),normal_route=dict(native_B=True,No_returns_to_editor_and_preserves_draft=True,Yes_commits_one_native_Japanese_character=True,Hangul_runtime=False),tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['capture_keyboard_adapter.py','report_keyboard_adapter.py']},artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [route/'result.json',route/'adapter_environment.json',route/'step_023_adapter.json']},limits=['Positive observations only; not complete lifetime/writer population or free RAM proof.','Initializer is statically verified but not entered on this preinitialized checkpoint route.','Normal native Japanese route, no Hangul hooks or user saves modified.','ROM install withheld until coordinated display/edit/record bridge and stack invariants are established.'])
    report['stack_candidate']['entry_aligned8']=(sp%8==0)
    report['stack_candidate']['reason']='Observed entry SP alignment is known; shim/IRQ/data ownership and maximum stack depth remain unresolved.'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS adapter observation; No return verified; descriptor0 copy32 observed; stack/overlay adoption pending')

if __name__=='__main__':main()
