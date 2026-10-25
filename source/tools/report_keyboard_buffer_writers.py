"""Bounded native writer lifetime observation; no free RAM/ROM readiness claim."""
import json
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB


def main():
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    route=ROOT/'poc/runtime/hangul-keyboard-v1-buffer-writers'
    result=verify_route(route,identity,set())
    baseline=ROOT/'poc/runtime/hangul-keyboard-v1-transfer-lifetime'
    old=verify_route(baseline,identity,set())
    for k in ('rom_sha256','emulator_sha256','state_sha256','actions','total_frames','capture_steps'):
        if result[k]!=old[k]:raise ValueError('observer comparison baseline')
    env=read(route/'buffer_writers_environment.json')
    if not env['observer_only'] or not env['no_RAM_or_save_injection']:raise ValueError('observer intervention')
    for n,key in [('capture_keyboard_buffer_writers.py','tool_sha256'),('capture_keyboard_native.py','native_observer_sha256')]:require_hash(ROOT/'tools'/n,env[key])
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(product,identity);rom=product.read_bytes()
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    trace=read(route/'step_023_buffer_writers.json')
    if trace['violations'] or trace['cache_pending'] or trace['stage_pending'] or trace['stage_windows']!=860 or trace['stage_closed']!=860:raise ValueError('protected native intervals')
    rows=trace['providers']
    if len(rows)!=860:raise ValueError('provider population')
    for p in rows:
        if (p['index'],p['slot'],p['source'],p['destination'],p['bytes'],p['result'],p['next_slot'],p['editor_reads'])!=(0,0,0x0200FC80,0x020155F0,32,0x020155F0,1,5):raise ValueError('observed provider ABI')
        if p['copy_sp']!=p['sp']-40 or p['return_sp']!=p['sp']-32 or p['source_hex']!=p['cache_hex']:raise ValueError('copy lifecycle')
        if bytes.fromhex(p['cache41_hex'])!=bytes.fromhex(p['cache_hex'])+b'\0'*9:raise ValueError('native cache extension observation')
    groups=sorted(trace['groups'],key=lambda g:g['kind'])
    expected={'cache':(0x08000950,27520,0x020155F0,0x0201560F),'stage':(0x030068B6,275200,0x0201E800,0x0201ECFC)}
    if len(groups)!=2:raise ValueError('new observed writer requires review')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);instructions=[]
    for g in groups:
        if g['phase']!='other' or (g['pc'],g['hits'],g['min'],g['max'])!=expected[g['kind']]:raise ValueError('writer calibration')
        at=g['pc']-0x08000000 if g['kind']=='cache' else 0x1E8F00+g['pc']-0x03000000
        code=rom[at:at+2]
        if code!=original[at:at+2]:raise ValueError('writer source identity')
        i=next(cs.disasm(code,g['pc']))
        if i.size!=2 or i.mnemonic!=('strb' if g['kind']=='cache' else 'str') or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=code:raise ValueError('writer instruction profile')
        instructions.append(dict(kind=g['kind'],pc=hex(i.address),offset=at,hex=code.hex(),mnemonic=i.mnemonic,operands=i.op_str,write_bytes=1 if g['kind']=='cache' else 4))
    regions={'cache512':(0x155F0,512),'stage1280':(0x1E800,1280),'editor96':(0xFC40,96),'record10':(0x10A6,10)}
    matched=[];whole_diff=[]
    for step in result['capture_steps']:
        name=f'step_{step:03d}_gbaExtWorkRam.bin';a=(route/name).read_bytes();b=(baseline/name).read_bytes()
        for key,(start,n) in regions.items():
            if a[start:start+n]!=b[start:start+n]:raise ValueError('scoped native regression '+key)
            matched.append(dict(step=step,region=key,sha256=sha(a[start:start+n])))
        for suffix in ['gbaExtWorkRam','gbaIntWorkRam','gbaVideoRam','gbaPaletteRam','gbaSpriteRam']:
            name=f'step_{step:03d}_{suffix}.bin'
            if (route/name).read_bytes()!=(baseline/name).read_bytes():whole_diff.append(name)
    a=read(route/'step_001_state.json')['state'];b=read(baseline/'step_001_state.json')['state']
    differences={k:{'current':a[k],'baseline':b.get(k)} for k in a if a[k]!=b.get(k)}
    report=dict(id='exe45.hangul-keyboard.buffer-writer-observation.v1',passed=True,rom_integrated=False,rom_sha256=identity,source_sha256=profile['sha256'],route=str(route.relative_to(ROOT)).replace('\\','/'),providers=len(rows),descriptor_counts=dict(Counter(p['index'] for p in rows)),slot_counts=dict(Counter(p['slot'] for p in rows)),provider_entry_sp=sorted({hex(p['sp']) for p in rows}),provider_caller_LR=sorted({hex(p['lr']) for p in rows}),protected_cache_consumptions=860,protected_stage_intervals=860,observed_protected_writes=0,observed_extension_bytes=9,extension_bytes_all_zero=True,writer_groups=groups,writer_instructions=instructions,scoped_regression=dict(matched_regions=len(matched),samples=matched),whole_snapshot_regression=dict(byte_identical=not whole_diff,different_files=whole_diff,first_state_differences=differences,claim='Not a byte-identical full-game regression. RTC/CPU differences observed; causal explanation of every RAM difference not established.'),baseline_result_sha256=sha((baseline/'result.json').read_bytes()),tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['capture_keyboard_buffer_writers.py','report_keyboard_buffer_writers.py','capture_keyboard_native.py']},artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [route/'result.json',route/'buffer_writers_environment.json',route/'step_023_buffer_writers.json']},limits=['Only this normal Japanese4-cell route: initialization/edit/delete/B-No/Yes/commit/return, not all descriptor0 slots or game paths.','Write callbacks record addressed writes within512-byte cache/1280-byte stage windows. Observed writers are strb/str; not complete all-width bus or IRQ ownership proof.','Cache tail9bytes zero/unwritten is an observation, not adopted41-byte capacity or free-space proof. New-layout/cache hooks remain uninstalled.','Protects cache only after copy through enqueue and stage enqueue through copy return; earlier/future lifetime and whole producer population unresolved.','Full snapshot comparison failed; only36 specified buffer/record snapshots match. No Korean keyboard screen, persistence or fresh-load claim.'])
    (ROOT/'analysis/hangul_keyboard_v1/buffer_writers.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(product,identity);require_hash(source,profile['sha256'])
    print('PASS bounded native writer observation860 windows; scoped snapshots36 match; whole snapshot identity NOT passed',flush=True)


if __name__=='__main__':main()
