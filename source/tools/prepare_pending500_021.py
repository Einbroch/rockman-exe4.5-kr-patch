"""Exact500 source-only compile, with script-specific development full-box scope."""
import re
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_batch500_016_inputs import prepare
from select_batch500_021 import SELECTION,LAYOUT
from verify_tpi_index import parse_tpi
from textpet_korean import prepare_plugins,command
from build_development_patch import compile_archive
from korean_codec import EXTRA_CHARACTER_INDICES

INPUTS='analysis/pending_insertion_500_021_inputs_v1'
OUT='analysis/pending_insertion_500_021_preflight_v1'
def materialize():return prepare(SELECTION,INPUTS,allow_carry=True)

def main():
    s=read(SELECTION);require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={f"{r['offset']:06X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};selected={i['archive']:i for i in s['selected']};items=materialize();out=ROOT/OUT
    if out.exists():raise ValueError('Preserve source preflight')
    assets=[];extras=set()
    for item in items:
        require_hash(ROOT/item['path'],item['sha256']);asset=read(item['path']);layouts=read(s['individual_layout']['path'])['layouts'];
        for unit in asset['units']:
            if unit['id'] in layouts:unit['translation']=layouts[unit['id']]
        tpl=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig');count=int(re.search(r'^@size\s+(\d+)',tpl,re.M).group(1));groups=selected[item['archive']]['groups'];names=[g['template'] for g in groups if 'template' in g];full=[g['fullbox_profile'] for g in groups if 'fullbox_profile' in g]
        if names and full:raise ValueError('Separate archive consumer classes')
        width=180 if full else 132;scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=item['scripts'],literal_ids=item['selected_ids'],script_count=count,max_literal_rows=3,max_line_advance=width,max_compiled_bytes=65535,preserve_literal_numerals=True)
        if names:scope['nickname_capacity_profiles']=names
        if full:scope['fullbox_capacity_profiles']=full
        extras.update(c for u in asset['units'] for c in u['translation'] if c in EXTRA_CHARACTER_INDICES);assets.append((item,asset,rows[item['archive']],scope))
    out.mkdir();plugins=out/'plugins';prepare_plugins(plugins,extras);common=command(plugins);results=[]
    for item,a,row,scope in assets:
        raw,p=compile_archive(source,row,a,scope,common,plugins,out/a['archive']);results.append(dict(archive=a['archive'],draft_path=item['path'],draft_sha256=item['sha256'],selected_ids=item['selected_ids'],selected_units=item['units'],scripts=item['scripts'],script_count=scope['script_count'],source_bytes=p['source_bytes'],compiled_bytes=len(raw),compiled_sha256=sha(raw),source_pointers=row['pointers'],layout=p['layout'],nickname_capacity_profiles=scope.get('nickname_capacity_profiles',[]),fullbox_capacity_profiles=scope.get('fullbox_capacity_profiles',[]),nickname_capacity_proof=p.get('nickname_capacity_proof',[]),fullbox_capacity_proof=p.get('fullbox_capacity_proof',[]),source_native_roundtrip=p['native_roundtrip'],protected_controls_unchanged=p['protected_controls_unchanged'],semantic_roundtrip=p['semantic_roundtrip'],binary_roundtrip=p['binary_roundtrip']));print('Preflight021',a['archive'],item['units'],'PASS',flush=True)
    if sum(r['selected_units'] for r in results)!=500:raise ValueError('Exact500')
    frozen_write(out/'preflight.json',dict(schema=1,batch_id=s['batch_id'],policy='development-draft; NON-DISTRIBUTION',source_sha256=sha(source),baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],selection=dict(path=SELECTION,sha256=sha((ROOT/SELECTION).read_bytes())),individual_layout=s['individual_layout'],total_units=500,applied_id_intersection=0,layout_candidates=[],archives=results,rom_written=False,runtime_tested=False,release_eligible=False,limits='Source-only500; full-box development extent runtime pending. Cumulative/product/runtime/human review not established.'))
    print('PASS exact500 source-only preflight')
if __name__=='__main__':main()
