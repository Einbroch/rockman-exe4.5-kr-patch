"""Verify isolated normal96 prompt/No/B route; NOT erase/success/failure QA."""
import json,struct
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha
from report_fixedcell_runtime import verify_route
from capture_save_initialize import ROM,ROM_SHA,MESEN_SHA,FIXTURE_SHA

def read(p):return json.loads(p.read_text(encoding='utf8'))

def main():
    rp=ROOT/ROM;require_hash(rp,ROM_SHA);rom=rp.read_bytes();m=read(rp.with_suffix('.json'))
    repro=ROOT/'poc/output/exe45_ko_development_save_initialize_v1_repro.gba';require_hash(repro,ROM_SHA)
    if rom!=repro.read_bytes():raise ValueError('independent full-byte rebuild')
    seedpath=ROOT/'analysis/save_initialize_v1/runtime_seed.json';seed=read(seedpath)
    if seed['rom_sha256']!=ROM_SHA or seed['fixture_sha256']!=FIXTURE_SHA or seed['old_ROM_savestate_used']:raise ValueError('QA seed identity')
    require_hash(Path(seed['fixture_path']),FIXTURE_SHA);require_hash(Path(seed['qa_destination']),FIXTURE_SHA)
    summary=read(ROOT/'analysis/full_scope_save_initialize_v1/inventory.json')['summary']
    if summary['baseline_rom_sha256']!=ROM_SHA or summary['parse_errors'] or summary['selected_catalog_literal_units']!=2596:raise ValueError('catalog identity')
    routes={};seen=set()
    for phase in ('title','prompt','cancel'):
        p=ROOT/f'poc/runtime/save-initialize-v1-{phase}';r=verify_route(p,ROM_SHA,seen);e=read(p/'qa_environment.json')
        if r['emulator_sha256']!=MESEN_SHA or r['probe']!='snapshot':raise ValueError('runtime environment')
        require_hash(Path(r['emulator_path']),MESEN_SHA)
        if e['rom_sha256']!=ROM_SHA or e['seed_receipt_sha256']!=sha(seedpath.read_bytes()) or e['RAM_injection']:raise ValueError('seed/observer binding')
        if not e['qa_sav_unchanged'] or e['qa_sav_before_sha256']!=FIXTURE_SHA or e['qa_sav_after_sha256']!=FIXTURE_SHA:raise ValueError('SAV changed')
        require_hash(p/'qa_save_before.sav',FIXTURE_SHA)
        changed=[n for n in e['files_before'].keys()|e['files_after'].keys() if e['files_before'].get(n)!=e['files_after'].get(n)]
        if changed!=e['changed_files'] or any(n!=rp.stem+'.rtc' for n in changed):raise ValueError('unrelated persistent changes')
        if phase=='title' and r['state_origin'] is not None:raise ValueError('cold boot required')
        for name in ('segment.lua',):
            if any(x in (p/name).read_text(encoding='utf8') for x in ('emu.write','setState','AliasReads')):raise ValueError('RAM intervention')
        routes[phase]=dict(result_sha256=sha((p/'result.json').read_bytes()),environment_sha256=sha((p/'qa_environment.json').read_bytes()),actual_capture_tool_sha256=e['tool_sha256'],actions=r['actions'],state_origin=r['state_origin'],captures=r['steps_captured'],changed_files=changed,qa_sav_unchanged=True)
    if routes['prompt']['actions']!='none:1:7,up:2:15,none:1:7,a:2:120,none:1:120' or routes['cancel']['actions']!='none:1:7,b:2:120,none:1:120':raise ValueError('normal prompt/B plan')
    p=ROOT/'poc/runtime/save-initialize-v1-prompt';ram=(p/'step_005_gbaExtWorkRam.bin').read_bytes()
    common=next(a for a in m['archives'] if a['archive']=='6368E8');root=0x08000000+common['rom_offset']
    if ram[0xfa21]!=96 or struct.unpack_from('<I',ram,0xfa50)[0]!=root:raise ValueError('wrong script/root')
    cursor=struct.unpack_from('<HHH',(p/'step_005_gbaSpriteRam.bin').read_bytes(),0)
    if (cursor[1]&511,cursor[0]&255)!=(101,136):raise ValueError('observed No cursor changed')
    out=ROOT/'analysis/save_initialize_v1'
    result=dict(passed=True,rom_sha256=ROM_SHA,rom_bytes=len(rom),independent_rebuild_byte_identical=True,catalog_counts=summary['counts'],script96_observed=True,root=root,observed_No_cursor_xy=[101,136],source_Yes_erase_route_executed=False,qa_native_sav_sha256=FIXTURE_SHA,qa_sav_unchanged=True,user_saves_touched=False,fixture_import_before_coldboot=True,old_ROM_savestate_used=False,routes=routes,screenshots={phase:sha((ROOT/f'poc/runtime/save-initialize-v1-{phase}'/name).read_bytes()) for phase,name in (('prompt','step_005.png'),('cancel','step_003.png'))},report_tool_sha256=sha(Path(__file__).read_bytes()),release_eligible=False,limits=['Actual normal UI96 prompt/labels observed on imported native QA SAV. Assistant inspected Korean text/No cursor and B return-to-title screenshots; presentation human review pending.', 'No erase execution. Scripts97/98 initialization/progress/failure/retry/success six literals and fresh-save regression remain unverified.', 'Snapshots establish selected script/root, cursor and screenshots, not a full font-read-to-VRAM/pixel-chain proof or all consumers. Previous17/21 runtime evidence is not inherited.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS normal script96 prompt/No/B isolated route, SAV unchanged, independent rebuild; NOT erase6 runtime')

if __name__=='__main__':main()
