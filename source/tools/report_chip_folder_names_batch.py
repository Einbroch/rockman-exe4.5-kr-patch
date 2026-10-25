"""Source-bound actual 30-name folder clone and held-page pixel proof."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from chip_library_extension import compile_clone
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells
from report_chip_folder_pixels import visible_folder


def main():
    stem='exe45_ko_development_chip_folder_v3';m=read(ROOT/f'poc/output/{stem}.json')
    build=m['output_sha256'];rom=ROOT/f'poc/output/{stem}.gba';require_hash(rom,build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256'])
    native=source.read_bytes();e=m['chip_folder_extension']
    asset_path=ROOT/'translations/library_chip_names_batch01_ko.json'
    a=next(a for a in m['translation_assets'] if a['path']==str(asset_path.relative_to(ROOT)))
    require_hash(asset_path,a['sha256'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    require_hash(ROOT/e['spec_path'],e['spec_sha256'])
    clone,record=compile_clone(native,read(ROOT/e['spec_path']),read(asset_path),table)
    require(rom.read_bytes()[e['clone_offset']:e['clone_offset']+len(clone)]==clone,'folder final clone mismatch')
    names={u['script']:u['text'] for u in record['units']}
    require(set(names)==set(range(1,31)) and len(record['unselected_scripts'])==226,'folder draft denominator')
    f=m['fixedcell_extension'];require_hash(ROOT/f['font']['path'],f['font']['sha256'])
    cells=bdf_cells(ROOT/f['font']['path'],{c for name in names.values() for c in name if '\uac00'<=c<='\ud7a3'},f['raster'])
    p=ROOT/'poc/runtime/chip-folder-v3-all30-stable';r=verify_route(p,build,set())
    env=read(p/'folder_batch_environment.json')
    require_hash(ROOT/'tools/capture_chip_folder_names_batch.py',env['tool_sha256'])
    require(r['return_code']==0 and r.get('normal_play_checkpoint_eligible') is False and env['passed'],'folder batch scope/fault')
    require(env['covered_scripts']==list(range(1,31)),'folder name coverage')
    pixels={};pages={}
    for step in (15,16,17):
        epoch=read(p/f'step_{step:03d}_folder_batch.json')['epochs']
        require((epoch-1)%30>=2,'page snapshot too close to transition')
        start=((epoch-1)//30)*7
        rows={row:names[(start+row)%30+1] for row in range(7)}
        pixels[step]=visible_folder(p,step,rows,cells,native,table);pages[step]=rows
    out=ROOT/'analysis/exe45_chip_folder_names_batch_v3.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded 30-name folder clone; diagnostic, NON-DISTRIBUTION',
        'result_sha256':sha((p/'result.json').read_bytes()),'environment':env,'held_pages':pages,'pixel_masks':pixels,
        'limits':['not 30 acquired chips or unchanged screen contents during normal play','not synthetic 56-changing-cell timing',
                  'all wording needs review; no full-game/audio/hardware release claim']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS actual 30-name folder clone and held-page screenshot glyph masks')


if __name__=='__main__':
    main()
