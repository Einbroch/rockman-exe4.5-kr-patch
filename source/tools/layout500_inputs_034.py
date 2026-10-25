"""034 exact500 source-bound mixed-script input gate before allocation."""
import re
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals,resolve_units,skeleton
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts,script_spans
from prepare_repartition500 import layout_records
from survey_aggregate_pet_033 import replace_exact
from survey_batch500_017_layout import protected_edges
from build_development_patch import literal_scope,validate_literal_numerals
from compile_exact500_034 import VALIDATORS

MANIFEST='analysis/pending_insertion_500_034_carry500_v1/preflight.json'
# Written only after the immutable manifest exists; unknown/missing recipe fails.
MANIFEST_SHA=read('tools/specs/inputs034_version.json')['manifest_sha256']
OUT='analysis/pending_insertion_500_034_input_gate500_v1/verification.json'


def checked_ref(ref):
    require_hash(ROOT/ref['path'],ref['sha256']);return ROOT/ref['path']


def validate_group(original,target,g,units):
    ids={u['id'] for u in units};locked={u['id']:u for u in g['locked_parent_units']}
    if len(ids)!=len(units) or ids!=set(g['ids']) or ids&locked.keys():raise ValueError('034 group new/locked ID partition')
    source_literals={u.key:u.text for u in literals(original)}
    here={k for k,v in source_literals.items() if int(k.split(':')[1])==g['script'] and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',v)}
    if here!=ids|set(locked) or set(g['geometry_ids'])!=here:raise ValueError('034 whole Japanese script population including locked parent')
    expected=[]
    for link in g['drafts']:
        a=read(checked_ref(link));matches=[u for u in a['units'] if u['id']==link['id']]
        if len(matches)!=1 or a['source_tpl']!=g['source_tpl']:raise ValueError('034 canonical draft identity')
        u=matches[0];value=g['explicit_layouts'].get(u['id'],u['translation'])
        if u['source']!=source_literals[u['id']] or u['state']!='needs_review' or value.replace('\n',' ')!=u['translation'].replace('\n',' ') or not protected_edges(u['source'],value):raise ValueError('034 selected wording/protected edges')
        expected.append(dict(id=u['id'],source=u['source'],translation=value,state=u['state']))
    if sorted(expected,key=lambda x:x['id'])!=sorted(units,key=lambda x:x['id']):raise ValueError('034 selected wording/state mutated')
    if any(u['source']!=source_literals[k] for k,u in locked.items()):raise ValueError('034 locked source identity')
    validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    values={k:u['translation'] for k,u in locked.items()};values.update({u['id']:u['translation'] for u in units})
    proposed=replace_exact(original,values);actual={u.key:u.text for u in literals(target)}
    if any(actual[k]!=v for k,v in values.items()):raise ValueError('034 effective target/locked wording differs')
    validator=dict(VALIDATORS).get(g['profile'])
    if validator is None:raise ValueError('034 unknown consumer profile')
    proof=validator(original,proposed,[g['script']],set(g['geometry_ids']),99)
    if proof!=g['geometry']:raise ValueError('034 independently recomputed geometry differs')
    return proof


def load_inputs(source):
    recipe=read('tools/specs/inputs034_version.json')
    for p,h in recipe['dependencies'].items():require_hash(ROOT/p,h)
    require_hash(ROOT/MANIFEST,MANIFEST_SHA);manifest=read(MANIFEST)
    selection=read('analysis/pending_insertion_500_034_exact500_selection_v1/selection.json')
    mechanical=read('analysis/pending_insertion_500_034_compile500_v1/verification.json')
    preflight=read('analysis/pending_insertion_500_034_preflight500_v1/verification.json')
    for report in (manifest,selection,mechanical,preflight):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
        if report.get('passed') is False or report['rom_written']:raise ValueError('034 failed/unexpected product preparation')
    if sha(source)!=manifest['source_sha256'] or selection['planned_new_units']!=500 or mechanical['units']!=500 or preflight['prepared_new_literal_units']!=500:raise ValueError('034 exact500 supported source')
    baseline_path=ROOT/manifest['baseline_rom'];require_hash(baseline_path,manifest['baseline_sha256']);baseline=baseline_path.read_bytes();meta=read(baseline_path.with_suffix('.json'))
    if meta['output_sha256']!=manifest['baseline_sha256']:raise ValueError('034 current product metadata')
    # Native contracts are independently bound to actual source/current bytes.
    for path in recipe['native_evidence']:
        evidence=read(path)
        if not evidence['passed']:raise ValueError('034 native evidence failed')
        for region in evidence['native_ranges']:
            a,n=region['offset'],region['bytes']
            if sha(source[a:a+n])!=region['sha256'] or baseline[a:a+n]!=source[a:a+n]:raise ValueError('034 native source/current contract drift')
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    from verify_tpi_index import parse_tpi
    catalog={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    parents={r['archive']:r for r in meta['archives']};groups=defaultdict(list)
    for g in selection['groups']:groups[g['archive']].append(g)
    if len(manifest['archives'])!=len(groups) or len({r['archive'] for r in manifest['archives']})!=len(groups):raise ValueError('034 archive count/duplicate')
    compiled={r['archive']:r for r in mechanical['archives']};applied={u['id'] for r in layout_records(meta) for u in r['layout']};new_ids=set();counts=Counter();admitted=[]
    for rec in manifest['archives']:
        arc=rec['archive'];parent=parents.get(arc)
        if parent is None or rec['storage']!='raw-carry' or rec['old_record']!=parent or rec['source_row']!=catalog[arc] or rec['source_row']['compressed'] or rec['source_row']['size_header']:raise ValueError('034 finite existing RAW route/catalog')
        native=payload_of(source,rec['source_row'])
        if sha(native)!=rec['source_payload_sha256']:raise ValueError('034 immutable native payload')
        carry=checked_ref(rec['carry_compiled']).read_bytes();actual=baseline[parent['rom_offset']:parent['rom_offset']+parent['compiled_bytes']]
        if carry!=actual or sha(carry)!=rec['parent_compiled_sha256']:raise ValueError('034 reconstructed parent differs from actual033')
        asset=read(checked_ref(rec['merged_asset']));units=resolve_units(asset);before=resolve_units(read(checked_ref(rec['parent'])));selected=set(rec['new_ids']);oldids={u['id'] for u in before};ids={u['id'] for u in units}
        if len(ids)!=len(units) or oldids&selected or selected&(applied|new_ids) or ids!=oldids|selected or len(units)!=rec['carry_units']+rec['new_units']:raise ValueError('034 cumulative unit partition')
        if {u['id']:u for u in units if u['id'] in oldids}!={u['id']:u for u in before}:raise ValueError('034 old wording/state changed')
        original=checked_ref(groups[arc][0]['source_tpl']).read_text(encoding='utf-8-sig');target=checked_ref(rec['merged_tpl']).read_text(encoding='utf-8-sig')
        expected=replace_exact(original,{u['id']:u['translation'] for u in units})
        if skeleton(target)!=skeleton(original) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals(expected)]:raise ValueError('034 source controls/all effective literals')
        reconstructed=script_spans((ROOT/compiled[arc]['compiled']['path']).parent.joinpath(arc+'_parent.msg').read_bytes(),rec['script_count']);live=script_spans(actual,rec['script_count'])
        for g in groups[arc]:
            if reconstructed[g['script']]!=live[g['script']]:raise ValueError('034 locked parent script byte proof')
            validate_group(original,target,g,[u for u in units if u['id'] in set(g['ids'])]);counts[g['profile']]+=g['units']
        for k in oldids:
            before_scope=literal_scope(rec['parent_scope'],k);after_scope=literal_scope(rec['scope'],k)
            if any(before_scope.get(field)!=after_scope.get(field) for field in ('consumer','literal_language','max_literal_rows','max_line_advance')):raise ValueError('034 effective old consumer scope changed')
        payload=checked_ref(rec['compiled']).read_bytes()
        if len(payload)!=rec['compiled_bytes'] or len(payload)>65535 or verify_untouched_scripts(carry,payload,rec['script_count'],set(rec['new_scripts']))!=rec['unselected_parent_scripts']:raise ValueError('034 payload/unselected script constraint')
        if set(rec['new_scripts'])!={int(k.split(':')[1]) for k in selected}:raise ValueError('034 selected script set')
        new_ids|=selected;admitted.append((rec,payload))
    if len(new_ids)!=500 or new_ids!=set(selection['selected_ids']) or counts!=Counter(selection['profiles']):raise ValueError('034 exact500/profile denominator')
    return admitted,dict(new_units=500,carry_units=sum(r['carry_units'] for r,_ in admitted),archives=len(admitted),profiles=dict(counts),storage=dict(Counter(r['storage'] for r,_ in admitted)))


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);_,summary=load_inputs(sp.read_bytes())
    deps=[MANIFEST,'tools/layout500_inputs_034.py','tools/specs/inputs034_version.json']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,**summary,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits='Exact source/current033 full carry, locked mixed-script wording and geometry before allocation. Not final product, full writes/repro, own-ROM GBA runtime or semantic approval.'))
    print('034 exact500 source input gate PASS',summary)


if __name__=='__main__':main()
