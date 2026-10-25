"""Keep unresolved7794EC in backlog; replace one batch slot by real mail14."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from survey_aggregate_pet_033 import replace_exact
from guarded_default_quick_geometry041_v1 import validate
from compare_archive_payloads import payload_of
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from tpl_literals import literals
from prepare_repartition500 import layout_records

OUT='analysis/pending_insertion_500_041_source_v8'


def main():
    old='analysis/pending_insertion_500_041_source_v7/selection.json';s=read(old);c=read('analysis/pending_insertion_500_041_inventory_v1/census.json');cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'))
    if s['selected_units']!=500 or s['rom_written']:raise ValueError('041 exact prior source500')
    deferred=[g for g in s['groups'] if g['archive']=='7794EC']
    if len(deferred)!=1 or deferred[0]['ids']!=['7794EC:247:0']:raise ValueError('041 exact unresolved source slot')
    g=deepcopy(next(g for g in c['groups'] if g['archive']=='6DD0B8' and g['script']==14));sr=g['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);original=(ROOT/sr['path']).read_text(encoding='utf-8-sig');native=payload_of(source,g['source_row']);raw={u.key:u.text for u in literals(original)};units=[];values={}
    for d in g['drafts']:
        require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']));text=place(u['translation'],(132,132,132))
        if a['source_sha256']!=sha(source) or a['source_tpl']!=sr or u['source']!=raw[u['id']] or u['state']!='needs_review' or text is None or text.replace('\n',' ')!=u['translation'].replace('\n',' ') or not protected_edges(u['source'],text):raise ValueError('041 protected canonical mail14')
        units.append(u);values[u['id']]=text
    ids=set(g['ids']);count=130
    for p in layout_records(m):
        if p['archive']!=g['archive'] or 'rom_offset' not in p:continue
        before=lz77_decompress(rom,p['rom_offset'])[0] if p.get('compression') else rom[p['rom_offset']:p['rom_offset']+p['compiled_bytes']]
        if sha(before)!=p['compiled_sha256'] or script_spans(before,count)[14]!=script_spans(native,count)[14] or ids&{u['id'] for u in p['layout']}:raise ValueError('041 selected current untouched mail14')
    import json
    g.update(source_class='unbound-guarded-default-quick',geometry=json.loads(json.dumps(validate(original,replace_exact(original,values),[14],ids))),geometry_ids=sorted(ids),explicit_layouts=values,canonical_units=units,script_count=count,current_unselected_script_identity_verified=True,wording_changed=False,product_admitted=False)
    s=deepcopy(s);s['groups']=[x for x in s['groups'] if x['archive']!='7794EC']+[g];s['groups'].sort(key=lambda x:(x['archive'],x['script']));keys=[k for x in s['groups'] for k in x['ids']]
    if len(keys)!=500 or len(set(keys))!=500:raise ValueError('041 exact replacement500')
    s['candidate_groups']=deepcopy(s['groups']);s['selected_ids']=sorted(keys);s['candidate_units']=500;s['candidate_classes']={kind:sum(x['units'] for x in s['groups'] if x['source_class']==kind) for kind in sorted({x['source_class'] for x in s['groups']})};s['status']='041_REPARTITIONED500_SOURCE_ONLY_NATIVE_BINDING_PENDING';s['deferred_replaced_source']=[dict(id='7794EC:247:0',reason='Actual native lookup/caller unresolved; remains canonical unapplied backlog, NOT excluded from overall translation scope.',preserved_prior_selection=old)];s['repartition_wording_changes']=0;s['dependencies'].update({p:sha((ROOT/p).read_bytes()) for p in [old,'tools/repartition_source500_041_v8.py','tools/guarded_default_quick_geometry041_v1.py','analysis/pending_insertion_500_041_inventory_v1/census.json']});frozen_write(ROOT/OUT/'selection.json',s);print('041 exact500 repartition: mail14 replaces unresolved debug flag247; backlog preserved;53archives/445scripts; NO ROM')


if __name__=='__main__':main()
