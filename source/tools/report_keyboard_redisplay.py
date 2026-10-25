"""Bound observed redisplay and temporary-text adjacent field; no adoption."""
import json, struct
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read, verify_route
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB

def main():
    route=ROOT/'poc/runtime/hangul-keyboard-v1-redisplay-r2'
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    result=verify_route(route,identity,set());env=read(route/'redisplay_environment.json')
    if not env['observer_only'] or not env['no_RAM_or_save_injection']:raise ValueError('intervention')
    for n,k in [('capture_keyboard_redisplay.py','tool_sha256'),('capture_keyboard_native.py','native_observer_sha256')]:require_hash(ROOT/'tools'/n,env[k])
    trace=route/'step_025_redisplay.json';data=read(trace);events=data['events'];reads=data['reads']
    providers=[p for p in events if p['kind']=='provider'];calls=[p for p in events if p['kind']=='call']
    if len(providers)!=860 or {p['index'] for p in providers}!={0}:raise ValueError('native provider route')
    for p in providers:
        if (p['source'],p['bound'],p['slot'],p['result'],p['next_slot'])!=(0x0200FC80,32,0,0x020155F0,1):raise ValueError('provider ABI')
        if p['cache_hex'][:64]!=p['source_hex']:raise ValueError('cache copy')
    entry=next(p for p in calls if p['pc']==0x08032AC6 and p['r1']==0x02014E74)
    returned=next(p for p in calls if p['pc']==0x08035030)
    refresh=[p for p in calls if p['pc']==0x08038B94]
    alias=next(p for p in calls if p['pc']==0x08032AC6 and p['r0']==p['r1']==0x020010A7)
    if entry['frame']!=1075 or returned['r0']!=1 or not returned['temporary_hex'].startswith('9be5') or alias['frame']!=1092 or [p['r0'] for p in refresh]!=list(range(26)):raise ValueError('native refresh/commit boundary')
    adjacent=[p for p in reads if p['pc']==0x08036A74]
    if len(adjacent)!=1 or adjacent[0]['address']!=0x02014E94 or adjacent[0]['frame']!=1242:raise ValueError('adjacent field observation')
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(product,identity);current=product.read_bytes()
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x36A64,0x36A90),(0x38B94,0x38C10),(0x32AC6,0x32AD8)]:
        raw=rom[a:b]
        if current[a:b]!=raw:raise ValueError('native code identity')
        ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('native instruction extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native ISA roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    # The literal plus the actual adds/ldr establish a four-byte independent
    # count, with a following word list on the nonzero branch. Not a RAM allocator.
    if struct.unpack_from('<I',rom,0x36AAC)[0]!=0x02014DD0 or current[0x36AAC:0x36AB0]!=rom[0x36AAC:0x36AB0]:raise ValueError('adjacent base literal')
    ins={i.address:(i.mnemonic,i.op_str) for i in cs.disasm(rom[0x36A70:0x36A8E],0x08036A70)}
    for a,v in {0x08036A70:('ldr','r4, [pc, #0x38]'),0x08036A72:('adds','r4, #0xc4'),0x08036A74:('ldr','r5, [r4]'),0x08036A7A:('adds','r4, #4'),0x08036A7C:('ldr','r0, [r4]')}.items():
        if ins[a]!=v:raise ValueError('adjacent count/list semantics')
    snapshots=[]
    for step in result['capture_steps']:
        ram=(route/f'step_{step:03d}_gbaExtWorkRam.bin').read_bytes()
        snapshots.append(dict(step=step,record_hex=ram[0x10A6:0x10B0].hex(),temporary_hex=ram[0x14E74:0x14E94].hex(),adjacent_count=struct.unpack_from('<I',ram,0x14E94)[0],script=ram[0xFA21]))
    if any(p['record_hex']!='019be57ee50000000000' for p in snapshots):raise ValueError('committed record regression')
    report=dict(id='exe45.hangul-keyboard.native-redisplay-observation.v1',passed=True,rom_integrated=False,
        source_sha256=profile['sha256'],rom_sha256=identity,route=str(route.relative_to(ROOT)).replace('\\','/'),
        providers=len(providers),provider_indices=dict(Counter(p['index'] for p in providers)),
        native_refresh=dict(frame=1092,metadata_indices=list(range(26)),selected_alias_copy=alias),
        temporary_commit=dict(entry=entry,returned=returned),
        adjacent_field=dict(address='0x02014E94',bytes=4,temporary_offset=32,observed=adjacent[0],literal_offset=0x36AAC,base='0x02014DD0',following_word_list='0x02014E98'),
        expansion_risks=[dict(capacity=c,maximum_stream_bytes=4*c+1,overlap_count_bytes=max(0,min(4,4*c+1-32))) for c in (4,6,8,10)],
        scoped_read_count=len(reads),native_code=regions,snapshots=snapshots,
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('capture_keyboard_redisplay.py','report_keyboard_redisplay.py','capture_keyboard_native.py')},
        artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in (route/'result.json',route/'redisplay_environment.json',trace)},
        limits=['Native Japanese cap4 record only. No generated Hangul code runs in the game.',
                'Observed all26 refresh entries on one return; no all-field writer or save graph claim.',
                'Only descriptor0 fixed-cell providers observed. Post-confirm dialogue does not establish descriptor16 or temporary-text glyph consumption.',
                'Read callback scope uses addressed accesses; snapshots and read starts are not a complete bus/writer/lifetime proof.',
                'Independent count at temporary+32 disproves safe41-byte expansion there. Less-than32-byte capacity is not thereby adopted.',
                'No RAM reservation, record discrimination, Korean screen, native save/reload or ROM integration.'])
    (ROOT/'analysis/hangul_keyboard_v1/native_redisplay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS native redisplay:26 refresh entries;860 descriptor0 providers; temporary+32 independent count observed; no Hangul integration',flush=True)

if __name__=='__main__':main()
