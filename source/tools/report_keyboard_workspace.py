"""Audit the observed keyboard neighborhood; reject an adjacent RAM candidate."""
import json
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    p=ROOT/'poc/runtime/hangul-keyboard-v1-workspace-r2';r=read(p/'result.json');identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';verify_route(p,identity,set());require_hash(Path(r['rom_path']),identity);rom=Path(r['rom_path']).read_bytes()
    env=read(p/'workspace_environment.json');require_hash(ROOT/'tools/capture_keyboard_workspace.py',env['tool_sha256']);require_hash(ROOT/'tools/capture_keyboard_native.py',env['native_observer_sha256'])
    trace=read(p/'step_023_workspace.json')
    if trace['observed_window']!=env['window']:raise ValueError('observed workspace extent')
    candidate=[0x0200fca0,0x0200fca0+276]
    conflicts=[a for a in trace['accesses'] if a['min']<candidate[1] and a['max']>=candidate[0]]
    if not conflicts or not any(a['pc']==0x0804a466 for a in conflicts):raise ValueError('expected adjacent live access not captured')
    decoded=[];cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for pc in sorted({a['pc'] for a in conflicts}):
        at=pc-0x08000000;ins=next(cs.disasm(rom[at:at+4],pc),None)
        if ins is None:raise ValueError('observed instruction decode')
        decoded.append(dict(pc=hex(pc),hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
    snapshots=[]
    for step in r['capture_steps']:
        ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();snapshots.append(dict(step=step,script=ram[0xfa21],edit_words_hex=ram[0xfc60:0xfc72].hex(),record_hex=ram[0x10a6:0x10b0].hex()))
    if snapshots[0]['script']!=29 or snapshots[-1]['script']!=93:raise ValueError('native entry/exit route')
    out=ROOT/'analysis/hangul_keyboard_v1/workspace.json'
    result=dict(id='exe45.hangul-keyboard.workspace-observation.v1',passed=True,claim='adjacent276-byte workspace candidate rejected by positive CPU access evidence; NOT free RAM proof',rom_sha256=identity,tool_sha256=sha(Path(__file__).read_bytes()),route_result_sha256=sha((p/'result.json').read_bytes()),trace_sha256=sha((p/'step_023_workspace.json').read_bytes()),observer_sha256=env['tool_sha256'],candidate=dict(start=hex(candidate[0]),end_exclusive=hex(candidate[1]),bytes=276,adopted=False,decision='rejected',reason='existing CPU readers/writers overlap during normal keyboard/dialogue route'),conflicting_accesses=conflicts,first_observed_instructions=decoded,snapshots=snapshots,limits=['Only observed read/write addresses on this route; no full RAM allocator/owner/lifetime graph.','The No attempt did not establish cancellation: step17 remains script10; no No-return pass claimed.','Normal native Japanese input/confirm path; no Hangul key selection/state injection or ROM edits.','ExistingFC60 editing andFC80 flattened bytes are distinct surfaces; their coordinated replacement is a future design candidate, not adopted RAM.'])
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('PASS adjacent276-byte RAM candidate rejected;',len(conflicts),'access groups overlap; no free RAM claim')

if __name__=='__main__':main()
