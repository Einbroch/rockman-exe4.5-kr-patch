"""Verify exact-ROM quarantined maximum folder transfer/cadence evidence."""
import json
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require


def main():
    m=read(ROOT/'poc/output/exe45_ko_development_chip_folder_v3.json');build=m['output_sha256']
    require_hash(ROOT/'poc/output/exe45_ko_development_chip_folder_v3.gba',build)
    require_hash(ROOT/'poc/output/exe45_ko_development_chip_folder_v3_repro.gba',build)
    require_hash(ROOT/read(ROOT/'project.json')['source_profile']['filename'],m['source_sha256'])
    p=ROOT/'poc/runtime/chip-folder-v3-changing56-r2';r=verify_route(p,build,set())
    e=read(p/'folder_changing_environment.json');d=read(p/'final_folder_changing.json')
    require_hash(ROOT/'tools/capture_chip_folder_changing.py',e['tool_sha256'])
    require(r['return_code']==0 and r.get('normal_play_checkpoint_eligible') is False and not list(p.glob('*failed*')),'changing scope/fault')
    require(e['rom_sha256']==build and e['passed'] and e['observed']==d,'observer identity')
    n=len(d['groups']);gaps=Counter(b['frame']-a['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
    require(n>100 and dict(gaps)=={1:n-1} and e['cadence_all_one'],'changing cadence')
    require(d['copies']==56*n and d['descriptor_reads']==7*n and all(g['rows']==7 and g['copies']==56 for g in d['groups']),'changing denominator')
    cycles=sorted(g['cycles'] for g in d['groups'])
    out=ROOT/'analysis/exe45_chip_folder_changing_v3.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded muted-Mesen synthetic changing 56-cell transfer/cadence',
        'result_sha256':sha((p/'result.json').read_bytes()),'environment_sha256':sha((p/'folder_changing_environment.json').read_bytes()),
        'groups':n,'actual_copies':d['copies'],'verified_rows':7*n,'cadence_frames':dict(gaps),
        'cycles':{'minimum':cycles[0],'median':cycles[n//2],'maximum':cycles[-1]},
        'excluded_attempts':['changing56','changing56-r1'],
        'limits':['synthetic descriptor/name reads, not normal wording or acquired chips','group cadence, not full scanout/tearing proof',
                  'no icon workload claim beyond native tested folder context','audio disabled, no hardware/full-game release claim']},indent=2),encoding='utf-8')
    print('PASS folder changing 56-cell:',n,'groups',d['copies'],'actual copies',dict(gaps))


if __name__=='__main__':
    main()
