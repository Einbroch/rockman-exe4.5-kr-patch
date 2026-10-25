"""Bound exact folder lifecycle observations without declaring free VRAM."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route


def main():
    build='16afa15fb530f1aded001691767f39fecb44394fab0e20760eeedd9408833241'
    p=ROOT/'poc/runtime/chip-names-batch01-v1-folder-lifetime-v2'
    r=verify_route(p,build,set())
    if not r['complete'] or r['return_code']!=0 or list(p.glob('*failed*')):
        raise ValueError('lifetime route failed')
    e=json.loads((p/'folder_lifetime_v2_environment.json').read_text())
    for filename,key in [('capture_chip_folder_lifetime.py','tool_sha256'),
                         ('capture_chip_library_probe.py','survey_tool_sha256'),
                         ('capture_chip_folder_lifetime_v2.py','adapter_sha256')]:
        require_hash(ROOT/'tools'/filename,e[key])
    d=json.loads((p/'final_chip_survey.json').read_text())
    n=json.loads((p/'final_other_consumer.json').read_text())
    if d['checked_frames']<=100 or n['alternate_calls']<=0 or not d['control_map_write_count']:
        raise ValueError('missing observer positive controls')
    overlaps=[c for c in d['copies'] if c['destination']<0x06009000 and c['destination']+c['bytes']>0x06008000]
    references=d['candidate_map_tile_histogram']
    private_refs=[x for x in references if 0x06008040<=x['tile_address']<0x06008EB0]
    writes=d['candidate_write_count']
    if not overlaps or not writes or not references:
        raise ValueError('lifecycle inventory positive evidence missing')
    out=ROOT/'analysis/exe45_chip_folder_lifetime_v1.json'
    if out.exists():
        raise ValueError('refuse report overwrite')
    report={'rom_sha256':build,'status':'PASS bounded native folder lifecycle inventory; allocation unadopted',
            'result_sha256':sha((p/'result.json').read_bytes()),'checked_frames':d['checked_frames'],
            'native_name_calls':n['alternate_calls'],'candidate_write_operations':writes,
            'candidate_write_sites':d['candidate_write_sites'],'candidate_map_histogram':references,
            'library_private_cell_map_references':private_refs,'overlapping_helper_copies':overlaps,
            'control_map_write_count':d['control_map_write_count'],
            'findings':['Initialization writes the old library candidate bank; it is not permanently free',
                        'This recorded route references 06008000 transition tile but no 06008040..06008EAF cell/tag tiles',
                        'Folder names are seven rows at 0202A680 with base 2010; library guard/palette/base cannot be blindly reused'],
            'excluded_attempt':'folder-lifetime v1 composed dump function name mismatch; owned process terminated, failed artifacts retained; no ROM change',
            'next_requirements':['identify exact initializer copy completion and reset contract',
                                 'scope new selector/renderer and normalize Hangul tile base separately from native base 16',
                                 'prove exit/reentry and name-input owner transitions on any future folder candidate'],
            'limits':['no global free-space, sprite-bank, scanout tearing, audio, hardware or translation completion claim']}
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS native folder lifetime:',d['checked_frames'],'frames;',writes,'writes; private map refs:',len(private_refs))


if __name__=='__main__':
    main()
