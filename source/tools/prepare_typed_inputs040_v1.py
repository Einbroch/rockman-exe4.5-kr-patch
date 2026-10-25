"""Register040 authored500/carry8 inputs, explicitly pending runtime admission.

No runtime result or previous-ROM extraction becomes authored wording. The
CPU test covers only initializer prefix; tournament live route still missing.
"""
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals,resolve_units,skeleton
from survey_aggregate_pet_033 import replace_exact
from consumer_links040_v1 import contracts,source_population,CLASSES
from build_development_patch import validate_characters
from fixture_typed040_v1 import SOURCE,BASE,BASE_SHA

OUT='analysis/pending_insertion_500_040_typed_inputs_v1'


def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);m=read(BASE.replace('.gba','.json'));s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json');cpu=read(SOURCE+'/selector_cpu_v1.json');bbs=read(SOURCE+'/bbs_boundary_v2.json')
    if not v['passed'] or v['units']!=500 or v['inherited_units']!=8 or v['rom_written'] or not cpu['passed'] or cpu['baseline_sha256']!=BASE_SHA or not bbs['passed'] or bbs['baseline_sha256']!=BASE_SHA:raise ValueError('040 source/CPU/qualified BBS prerequisites')
    for report in (s,v,cpu,bbs):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    chosen={arc:gs[0]['source_class'] for arc,gs in groups.items()};pool={p['archive']:p for p in source_population(source,chosen)};abi=contracts(source);out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);records=[];seen=set();carry=set();plugins=ROOT/SOURCE/'compile_v1/plugins'
    for r in v['archives']:
        arc=r['archive'];gs=groups[arc];kind=chosen[arc];units=[];new=[];old=[];lineage=[];parent=r['parent_asset']
        if parent:
            if m['active_communication_owners039'].get(arc)!=parent:raise ValueError('040 one039 active carry owner')
            require_hash(ROOT/parent['path'],parent['sha256']);old=deepcopy(resolve_units(read(parent['path'])))
        for g in gs:
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']));value=g['explicit_layouts'][u['id']]
                if value.replace('\n',' ')!=u['translation'].replace('\n',' ') or u['state']!='needs_review' or a['source_sha256']!=sha(source) or a['source_tpl']!=r['source_tpl']:raise ValueError('040 canonical words/state lineage')
                u['canonical_wording']=u['translation'];u['translation']=value;new.append(u);lineage.append(d)
        units=old+new
        if units!=r['units'] or len({u['id'] for u in units})!=len(units) or {u['id'] for u in new}!=set(r['new_ids']) or {u['id'] for u in old}!=set(r['inherited_ids']):raise ValueError('040 complete current authored conversion')
        for key in ('source_tpl','target_tpl','compiled'):require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');raw={u.key:u.text for u in literals(original)}
        if any(u['source']!=raw[u['id']] for u in units):raise ValueError('040 source protected literal')
        target=replace_exact(original,{u['id']:u['translation'] for u in units})
        if skeleton(target)!=skeleton(original):raise ValueError('040 exact source controls')
        cap=132 if kind=='communication-help' else 168 if kind=='battle-BBS-trial' else 180;scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_ids=sorted(u['id'] for u in units),literal_scripts=sorted({int(u['id'].split(':')[1]) for u in units}),script_count=r['script_count'],max_literal_rows=3,max_line_advance=cap,preserve_literal_numerals=True,storage='typed-native-identity-ROM-clone',native_root=CLASSES[kind]['root'],guarded_reader_return_lr=CLASSES[kind]['caller_lr'],saved_outer_reader_return_lr=CLASSES[kind]['outer_lr'],original_compressed_source_retained=True)
        metrics=validate_characters(target,plugins/'exe45-utf8.tbl',scope,{u['id'] for u in units})
        if metrics!=r['layout']:raise ValueError('040 typed metric refinement differs')
        ap=out/(arc+'_asset.json');asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=arc,source_sha256=sha(source),source_tpl=r['source_tpl'],source_archive_sha256=r['source_sha256'],consumer='normal-dialogue',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units,new_ids=r['new_ids'],inherited_ids=r['inherited_ids'],parent_asset_lineage=([parent] if parent else []),selected_wording_lineage=dict(selection=ref(ROOT/SOURCE/'selection.json'),canonical_drafts=lineage,within_page_LF_only=True,word_boundaries_only=True),insertion_ready=False)
        frozen_write(ap,asset);p=pool[arc]
        if {x['pointer'] for x in p['references']}!=set(r['source_row']['pointers']):raise ValueError('040 finite TPI/typed lookup reference equality')
        records.append(dict(archive=arc,source_class=kind,source_row=r['source_row'],source_lookup_references=p['references'],source_tpl=r['source_tpl'],target_tpl=r['target_tpl'],compiled=r['compiled'],compiled_sha256=r['compiled']['sha256'],compiled_bytes=r['compiled_bytes'],asset=ref(ap),new_ids=r['new_ids'],new_scripts=sorted(g['script'] for g in gs),inherited_ids=r['inherited_ids'],parent_asset=parent,parent_record_identity=r['parent_record_identity'],scope=scope,layout=metrics,native_bytes=r['native_bytes'],native_sha256=r['source_sha256'],unselected_current039_scripts=r['unselected_current039_scripts'],profiles=[dict(script=g['script'],source_class=kind,geometry=g['geometry']) for g in gs],product_admitted=False));seen.update(r['new_ids']);carry.update(r['inherited_ids']);print('PASS040 typed authored input',arc,'new',len(new),'carry',len(old),flush=True)
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(carry)!=8 or len(records)!=10:raise ValueError('040 exact500/carry8/10 registry population')
    paths=['tools/prepare_typed_inputs040_v1.py','tools/consumer_links040_v1.py','tools/typed_rom_selector040_v1.py',SOURCE+'/selection.json',SOURCE+'/verification_v1.json',SOURCE+'/selector_cpu_v1.json',SOURCE+'/bbs_boundary_v2.json']
    frozen_write(out/'manifest.json',dict(schema=1,status='040_AUTHORED500_PLUS_CARRY8_REGISTERED_NOT_RUNTIME_ADMITTED',source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,new_units=500,inherited_units=8,archives=records,selector_contract=abi,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},rom_written=False,new_units_applied=0,product_admitted=False,consumer_runtime_prerequisites_complete=False,release_eligible=False,limits=['Typed registry only; no product installer/primary/repro or040 ROM.','CPU initializer PREFIX is not full native initialization, UI, loader, rendering/timing/audio proof.','BBS source qualified Japanese two-page boundary observed. Korean040168px page/caches/terminal/close need exact-product runtime.','6E93C8 is tournament dialogue. Source23-Navi table/loader/reader and CPU prefix established; live tournament loader/context/display route still missing.','Communication151 must preserve authored8 and prior661 consumers. Existing039/038 whole-image gates must not be relaxed.']))
    print('PASS040 registered500/carry8/10; tournament live context still missing; NO ROM')


if __name__=='__main__':main()
