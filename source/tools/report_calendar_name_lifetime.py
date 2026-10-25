"""Verify current-ROM normal stage/pool transformations; no adoption claim.

Runtime evidence for unchanged keyboard. Distinguishes input person name from
final schedule title and default bypass, prerequisites to safe Hangul hooks.
"""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from korean_codec import encode_hangul

PREFIX='hangul-keyboard-calendar-lifetime-v1-'
STEPS={'menu':6,'time':6,'meal':7,'friend':4,'editor':3,'typed':8,'friend-register':3,'reenter':6}


def main():
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256'])
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity=read(ROOT/'analysis/hangul_keyboard_v1/cpu_calendar_bounded_commit/report.json')['current_rom_sha256'];require_hash(product,identity);rom=product.read_bytes();original=source.read_bytes()
    seen=set();routes=[];traces={};rams={}
    for name,step in STEPS.items():
        p=ROOT/'poc/runtime'/(PREFIX+name);result=verify_route(p,identity,seen);env=read(p/'name_lifetime_environment.json')
        if not env['observer_only'] or not env['no_RAM_or_save_injection'] or env['rom_sha256']!=identity:raise ValueError('observer scope')
        require_hash(ROOT/'tools/capture_calendar_name_lifetime.py',env['tool_sha256']);require_hash(ROOT/'tools/run_mesen_segment.py',env['runner_sha256'])
        for region in env['native_code']:
            a=region['offset'];b=a+region['bytes']
            if sha(original[a:b])!=region['sha256'] or rom[a:b]!=original[a:b]:raise ValueError('native source identity')
        trace=read(p/f'step_{step:03}_name_lifetime.json');ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if not trace['observer_only'] or len(ram)!=0x40000 or bytes.fromhex(trace['stage_hex'])!=ram[0x26280:0x26296] or bytes.fromhex(trace['pool0_hex'])!=ram[0x26080:0x260A9]:raise ValueError('snapshot observer agreement')
        traces[name]=trace;rams[name]=ram
        routes.append(dict(name=name,directory=str(p.relative_to(ROOT)).replace('\\','/'),step=step,result_sha256=sha((p/'result.json').read_bytes()),environment_sha256=sha((p/'name_lifetime_environment.json').read_bytes()),trace_sha256=sha((p/f'step_{step:03}_name_lifetime.json').read_bytes()),screenshot_sha256=sha((p/f'step_{step:03}.png').read_bytes()),actions=result['actions']))
    # Stage observer is positively calibrated by actual native commit writes.
    typed=traces['typed'];writes=typed['stage_writes']
    if len(writes)!=3 or {w['pc'] for w in writes}!={0x0803500C,0x0803501E,0x08035026} or [(w['address'],w['value']) for w in writes]!=[(0x02026280,1),(0x02026281,0x9B),(0x02026282,0xE5)]:raise ValueError('native stage writer positive calibration')
    if any(traces[n]['stage_writes'] or traces[n]['accesses'] for n in ('menu','time','meal','friend','editor')):raise ValueError('default/entry stage baseline differs')
    untouched=traces['time']['stage_hex']
    if any(traces[n]['stage_hex']!=untouched for n in ('meal','friend','editor')):raise ValueError('unchanged stage on default route')
    meal=encode_hangul('식사')+b'\xE5'
    events=traces['meal']['events'];register=[e for e in events if e['pc']==0x08037366]
    if len(register)!=1:raise ValueError('meal registered route')
    e=register[0];record=e['r0'];field=record+10
    if record!=0x02001310 or e['record']!=record or e['stage_hex']!=untouched or bytes.fromhex(e['record_hex'])[10:10+len(meal)]!=meal:raise ValueError('default bypass evidence')
    copies=[e for e in events if e['pc']==0x08032AC6 and e['r0']==0x02026080 and e['r1']==field]
    if len(copies)!=1 or bytes.fromhex(copies[0]['pool0_hex'])[:len(meal)]!=meal or copies[0]['r5']!=0x0200F550:raise ValueError('pool direct native commit')
    final_meal=rams['meal'][0x1310:0x1330]
    if final_meal[:2]!=b'\x03\x00' or final_meal[10:]!=meal+bytes(22-len(meal)):raise ValueError('meal persisted-in-RAM record')
    init=[e for e in traces['editor']['events'] if e['pc']==0x080355B6]
    if len(init)!=1 or (init[0]['r0'],init[0]['r1'],init[0]['r2'],init[0]['r3'],init[0]['lr'])!=(6,0x26,0x02026280,1,0x08030ECD):raise ValueError('friend actual input contract')
    stage=bytes.fromhex(typed['stage_hex']);pool=bytes.fromhex(typed['pool0_hex'])
    suffix=b'\xAE\xE4\x63\xE4\x69\xE5';title=b'\x9B'+suffix
    if stage[:3]!=b'\x01\x9B\xE5' or pool[:len(title)]!=title:raise ValueError('input vs final title transform')
    ar=next(a for a in read(product.with_suffix('.json'))['archives'] if a['archive']=='6368E8');base=ar['rom_offset'];offset=struct.unpack_from('<H',rom,base+0x45*2)[0]
    if rom[base+offset:base+offset+len(suffix)]!=suffix:raise ValueError('exact activity suffix script0x45')
    append=[e for e in typed['events'] if e['pc']==0x08032AC6 and e['r0']==0x08000000+base+offset and e['r1']==0x02026081]
    if len(append)!=1 or bytes.fromhex(append[0]['pool0_hex'])[:2]!=b'\x9B\xE5':raise ValueError('native suffix write source/destination')
    registered=traces['friend-register'];r=[e for e in registered['events'] if e['pc']==0x08037366]
    if len(r)!=1 or bytes.fromhex(r[0]['record_hex'])[10:10+len(title)]!=title or r[0]['stage_hex']!=typed['stage_hex']:raise ValueError('final title registration boundary')
    final_friend=rams['friend-register'][0x1310:0x1330]
    if final_friend[:2]!=b'\x03\x00' or final_friend[10:]!=title+bytes(22-len(title)):raise ValueError('friend full-title field')
    re=traces['reenter'];inits=[e for e in re['events'] if e['pc']==0x080355B6];imports=[e for e in re['events'] if e['pc']==0x0803558C]
    if len(inits)!=1 or len(imports)!=1 or inits[0]['r0']!=6 or inits[0]['r3']!=2 or imports[0]['r0']!=0x02026280 or imports[0]['lr']!=0x08030ED9 or re['stage_hex']!=typed['stage_hex'] or re['stage_writes']:raise ValueError('No->same-person import contract')
    # Do NOT transplant this native stage into the NEW bounded copier. Its first
    # byte/count is legacy, width depends on editing cap, and title != person.
    result=dict(id='exe45.hangul-keyboard.calendar-name-lifetime-runtime.v1',passed=True,rom_integrated=False,format_adopted=False,release_eligible=False,
        current_rom_sha256=identity,source_sha256=profile['sha256'],routes=routes,verified_same_ROM_ancestry_nodes=len(seen),
        default_meal=dict(stage_untouched=untouched,pool_name_hex=meal.hex(),registered_RAM_record_hex=final_meal.hex(),canonical_stage_bypassed=True),
        friend=dict(input_capacity=6,heading_script=0x26,caller=0x08030EAA,stage_prefix_hex=stage[:3].hex(),final_title_hex=title.hex(),activity_suffix_script=0x45,activity_suffix_hex=suffix.hex(),registered_RAM_record_hex=final_friend.hex(),No_reenter_imports_person_not_title=True),
        positive_stage_observer_calibration=dict(writes=3,PCs=sorted({w['pc'] for w in writes})),
        applicability=dict(bounded_commit_CPU_contract_preserved=True,bounded_commit_cannot_be_installed_unconditionally=True,
            reasons=['Default meal bypasses stage: NEW canonical must be produced on default path.',
                     'Friend input cap6 is distinct from cap10 final title storage; editor record width requires explicit conversion.',
                     'Native activity suffix is added only to pool and saved with title. Saving stage alone loses intended title text.',
                     'No re-entry imports original person name without suffix; final title must not become editor baseline.']),
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('capture_calendar_name_lifetime.py','report_calendar_name_lifetime.py')},
        limits=['Current exact playable ROM, normal controller branches from same-ROM checkpoints; original Japanese keyboard is intentionally unchanged. No Hangul keyboard screen or new-format runtime support.',
                'Registered RAM records only; no explicit save/reset/fresh-process reload in these segments. No old-save format discriminator or universal stage/IRQ/free RAM proof.',
                'Meal, friend one native character, No/re-entry observed; not all default names/calendar classes/anniversary/direct3355A path. Prior cap10 CPU proof remains scoped, not a natural caller integration claim.',
                'Snapshots/screenshots/observer receipts prove selected transitions. User data not injected; this does not establish hardware/RTC timing/audio or whole-game memory equivalence.'])
    out=ROOT/'analysis/hangul_keyboard_v1/calendar_name_lifetime.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(product,identity);require_hash(source,profile['sha256'])
    print('PASS current-ROM normal name lifetime/default bypass/final-title/reentry; NOT Hangul save support',len(routes),'routes',len(seen),'ancestry nodes',flush=True)


if __name__=='__main__':main()
