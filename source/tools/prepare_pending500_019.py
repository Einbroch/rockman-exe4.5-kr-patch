"""Source-only native-capacity compiler preflight; no final ROM writer."""
import re
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi
from textpet_korean import prepare_plugins,command
from build_development_patch import compile_archive
from korean_codec import EXTRA_CHARACTER_INDICES
from prepare_batch500_019_inputs import SELECTION,OUT as INPUTS

OUT='analysis/pending_insertion_500_019_preflight_v3'
def main():
    selection=read(SELECTION);inputs=read(INPUTS+'/inputs.json');cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/selection['baseline_rom'],selection['baseline_sha256']);require_hash(ROOT/selection['individual_layout']['path'],selection['individual_layout']['sha256']);layouts=read(selection['individual_layout']['path'])['layouts']
    rows={f"{r['offset']:06X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};selected={i['archive']:i for i in selection['selected']};out=ROOT/OUT
    if out.exists():raise ValueError('Preserve prior source preflight')
    assets=[];extras=set()
    for item in inputs['inputs']:
        require_hash(ROOT/item['path'],item['sha256']);asset=deepcopy(read(item['path']))
        for u in asset['units']:
            if u['id'] in layouts:u['translation']=layouts[u['id']]
            extras.update(c for c in u['translation'] if c in EXTRA_CHARACTER_INDICES)
        row=rows[item['archive']]
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0]:raise ValueError('Raw source relocation scope')
        tpl=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig');count=int(re.search(r'^@size\s+(\d+)',tpl,re.M).group(1))
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=item['scripts'],literal_ids=item['selected_ids'],script_count=count,max_literal_rows=3,max_line_advance=132,max_compiled_bytes=65535,preserve_literal_numerals=True)
        profiles=[]
        for g in selected[item['archive']]['groups']:
            if 'template' in g:
                model=g['template'];profiles.append(dict(script=g['script'],suffix_id=model['suffix_id'],source_first_line=model['source_first_line'],first_line=model['first_line']))
        if profiles:scope['nickname_capacity_profiles']=profiles
        if profiles:
            from nickname_capacity import validate
            from build_development_patch import translate_literal_scope
            validate(source,tpl,translate_literal_scope(tpl,asset['units'],scope),profiles,set(item['selected_ids']))
        assets.append((item,asset,row,scope))
    out.mkdir();plugins=out/'plugins';prepare_plugins(plugins,extras);common=command(plugins);results=[]
    for item,asset,row,scope in assets:
        raw,proof=compile_archive(source,row,asset,scope,common,plugins,out/asset['archive'])
        results.append(dict(archive=asset['archive'],draft_path=item['path'],draft_sha256=item['sha256'],source_tpl=asset['source_tpl'],source_payload_sha256=proof['source_sha256'],selected_ids=item['selected_ids'],selected_units=item['units'],scripts=item['scripts'],script_count=scope['script_count'],source_bytes=proof['source_bytes'],compiled_bytes=len(raw),compiled_sha256=sha(raw),source_pointers=row['pointers'],source_native_roundtrip=proof['native_roundtrip'],protected_controls_unchanged=proof['protected_controls_unchanged'],semantic_roundtrip=proof['semantic_roundtrip'],binary_roundtrip=proof['binary_roundtrip'],unselected_scripts_unchanged=True,layout=proof['layout'],nickname_capacity_profiles=scope.get('nickname_capacity_profiles',[]),nickname_capacity_proof=proof.get('nickname_capacity_proof',[])))
        print('Preflight019',asset['archive'],item['units'],'PASS',flush=True)
    total=sum(r['selected_units'] for r in results)
    if total!=500:raise ValueError('Frozen500 denominator')
    frozen_write(out/'preflight.json',dict(schema=1,batch_id=selection['batch_id'],policy='development-draft; NON-DISTRIBUTION',source_sha256=sha(source),baseline_rom=selection['baseline_rom'],baseline_sha256=selection['baseline_sha256'],selection=dict(path=SELECTION,sha256=sha((ROOT/SELECTION).read_bytes())),individual_layout=selection['individual_layout'],total_units=total,applied_id_intersection=0,layout_candidates=[],archives=results,rom_written=False,runtime_tested=False,release_eligible=False,limits='Source-only complete selected scope compile/roundtrip/native nickname geometry. Cumulative carry ancestry, single writer, product integration, new-page runtime and Hangul input/save unresolved.'))
    print('PASS exact500 source-only preflight; ROM unchanged')

if __name__=='__main__':main()
