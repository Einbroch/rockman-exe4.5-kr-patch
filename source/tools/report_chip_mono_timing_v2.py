"""Exact new-ROM affected maximum workloads and native description callers."""
import json
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require


def main():
    stem='exe45_ko_development_chip_mono_cannon_v2';m=read(ROOT/f'poc/output/{stem}.json');build=m['output_sha256']
    for suffix in ('','_repro'): require_hash(ROOT/f'poc/output/{stem}{suffix}.gba',build)
    require_hash(ROOT/read(ROOT/'project.json')['source_profile']['filename'],m['source_sha256'])
    seen=set();reports={}
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-changing56';r=verify_route(p,build,seen)
    e=read(p/'folder_changing_environment.json');d=read(p/'final_folder_changing.json');n=len(d['groups'])
    require_hash(ROOT/'tools/capture_chip_folder_changing.py',e['tool_sha256'])
    gaps=Counter(b['frame']-a['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
    require(r['return_code']==0 and r.get('normal_play_checkpoint_eligible') is False and e['passed'] and e['rom_sha256']==build and dict(gaps)=={1:n-1} and n>100,'folder changing/cadence')
    require(d['copies']==56*n and d['descriptor_reads']==7*n and all(g['rows']==7 and g['copies']==56 for g in d['groups']),'folder denominator')
    reports['folder']={'groups':n,'actual_copies':d['copies'],'cadence':dict(gaps),'result_sha256':sha((p/'result.json').read_bytes())}
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-library-full-icons';r=verify_route(p,build,seen)
    e=read(p/'full_icons_environment.json');d=read(p/'final_timing.json');n=len(d['groups'])
    require_hash(ROOT/'tools/capture_chip_late_wait_full_icons.py',e['tool_sha256'])
    gaps=Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
    require(r['return_code']==0 and r.get('normal_play_checkpoint_eligible') is False and e['passed'] and e['cadence_all_one'] and dict(gaps)=={1:n-1} and n>100,'library changing/cadence')
    require(len(d['copies'])==56*n and len(d['icons'])==7*n and all(g['rows']==7 and g['copies']==56 for g in d['groups']),'library denominator')
    reports['library']={'groups':n,'actual_copies':len(d['copies']),'icon_copies':len(d['icons']),'cadence':dict(gaps),'result_sha256':sha((p/'result.json').read_bytes())}
    parents={}
    for part,menu,phase in (('folder',0,16),('library',8,4)):
        p=ROOT/f'poc/runtime/chip-mono-cannon-v2-{part}-parent';r=verify_route(p,build,seen);e=read(p/'mono_parent_environment.json');d=read(p/'final_mono_parents.json')
        require_hash(ROOT/'tools/capture_chip_mono_parent.py',e['tool_sha256'])
        require(r['return_code']==0 and e['passed'] and d['calls'],'native parent observation failure')
        require(all(c['outer_lr']==0x080D4D09 and c['wrapper_lr']==0x080554BA and c['root_job']==28 and c['menu']==menu and c['phase']==phase and c['context']==0x0200F2C0 and c['width']==10 and c['height']==3 for c in d['calls']),'native mono caller/context mismatch')
        parents[part]={'native_consumer_entry':0x080D4CE0,'pool_literal':0x080D4D0C,'calls':d['calls'],'result_sha256':sha((p/'result.json').read_bytes())}
    require_hash(ROOT/'poc/runtime/chip-matrix-saves'/f'{stem}.sav','6de509d736812dab55b6828088c750496e701bf2690763ba14f65f519a4536b6')
    out=ROOT/'analysis/exe45_chip_mono_timing_v2.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded muted-Mesen affected maximum copy/cadence and native mono caller binding',
        'reproducible':True,'workloads':reports,'normal_parents':parents,
        'limits':['synthetic name/descriptor workloads, not ordinary acquired play','group cadence is not scanout tearing, audio or hardware timing proof',
                  'normal folder/library use D4D0C consumer; 2165C and D2B58 reachability/runtime still pending','102 drafts; not complete-game release']},indent=2),encoding='utf-8')
    print('PASS new-ROM folder/library maximum copies/cadence and normal D4D0C mono callers')


if __name__=='__main__': main()
