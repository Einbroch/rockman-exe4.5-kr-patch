"""Scope-limited trace audit and first observed Thumb instruction decoding."""
import json,struct
from pathlib import Path
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route,read
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    p=ROOT/'poc/runtime/hangul-keyboard-v1-native-edit';r=read(p/'result.json');verify_route(p,r['rom_sha256'],set());rp=Path(r['rom_path']);require_hash(rp,r['rom_sha256']);rom=rp.read_bytes()
    env=read(p/'keyboard_environment.json')
    if not env['observer_only'] or not env['no_RAM_or_save_injection'] or any(k in (p/'segment.lua').read_text() for k in ['emu.write','setState','AliasReads']):raise ValueError('intervention')
    trace=read(p/'step_015_keyboard.json');writes=trace['writes'];calls=trace['calls'];changed=[w for w in writes if w['before']!=w['value']]
    bypc=Counter(w['pc'] for w in changed);decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);decoded=[]
    for pc,n in sorted(bypc.items()):
        at=pc-0x08000000
        if not 0<=at<len(rom)-4:raise ValueError('observed writer outside ROM')
        ins=next(decoder.disasm(rom[at:at+4],pc),None)
        if ins is None:raise ValueError('unsupported observed writer')
        decoded.append(dict(pc=hex(pc),changed_writes=n,first_instruction_hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
    rows=[]
    for step in r['capture_steps']:
        t=read(p/f'step_{step:03}_keyboard.json');ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        rows.append(dict(step=step,edit_words_hex=ram[0xfc60:0xfc6a].hex(),flattened_hex=ram[0xfc80:0xfc90].hex(),record_hex=ram[0x10a6:0x10b0].hex(),keyboard_controls_hex=ram[0xfc40:0xfc60].hex(),script=ram[0xfa21]))
    expected={2:'9b989898e5',5:'9b9c9898e5',7:'9b989898e5',9:'9b9c9898e5'}
    for step,value in expected.items():
        if not rows[step-1]['flattened_hex'].startswith(value):raise ValueError('native edit/delete trace')
    if rows[-1]['record_hex']!='019b9ce5e50000000000' or rows[-1]['script']!=93:raise ValueError('native commit')
    entry=next(c for c in calls if c['pc']==0x08032ac6 and c['r0']==0x020010a7 and c['r1']==0x02014e74)
    exitcall=next(c for c in calls if c['pc']==0x08035030)
    if exitcall['r0']!=2 or not exitcall['temporary_hex'].startswith('9b9ce5'):raise ValueError('temporary copy/count')
    out=ROOT/'analysis/hangul_keyboard_v1';out.mkdir(exist_ok=True)
    data=dict(passed=True,scope='read-only native two Japanese characters input/delete/commit; not Hangul runtime',rom_sha256=r['rom_sha256'],route_result_sha256=sha((p/'result.json').read_bytes()),trace_sha256=sha((p/'step_015_keyboard.json').read_bytes()),observer_sha256=env['tool_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),snapshots=rows,changed_write_instructions=decoded,normalizer_entry=entry,normalizer_exit=exitcall,observations=['FC60 editing uses 16-bit cells; FC80 is flattened byte representation regenerated at observed PC08035636.','Normal commit copies two native bytes; 08032AC6 copies to02014E74 and returns2 in r0 on observed path.','Default record-like markers are visible at0200109C/020010A6/020010B0, ten-byte spacing; field ABI/reader population not yet established.'],limits=['Only the first instruction at actually observed writer PCs decoded; no complete CFG/reference/ISA coverage claim.','Marker2/custom Hangul format and ten-byte record width are NOT adopted or proven safe.','No ROM code, glyph, save or input modifications. Host composition model is not integrated.'])
    (out/'native_boundaries.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(dict(passed=True,changed_write_instructions=decoded,snapshots=rows[1:9:3]),ensure_ascii=False))
if __name__=='__main__':main()
