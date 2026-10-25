"""Register039 canonical authored words + explicit word-boundary LF inputs.

No prior-ROM text extraction is a build input; no ROM is emitted. The CPU
prefix test does not establish complete native initialization or GBA runtime.
"""
import json
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from fixture_communication039_v1 import OUT as SOURCE
from communication_rom_selector039_v1 import contracts,source_population
from tpl_literals import literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from profile_quick_geometry039_v1 import validate
from profile_layout039_v1 import reconstruct
from build_development_patch import validate_characters,validate_literal_numerals
from textpet_korean import prepare_plugins
from korean_codec import EXTRA_CHARACTER_INDICES
from prepare_repartition500 import layout_records
from archive_scripts import verify_untouched_scripts

OUT='analysis/pending_insertion_500_039_communication_inputs_v1'


def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/SOURCE/'selection.json','966a22eca30229b56984dead96e05d4c71bf0f3a8e464225432ea9ae3bdb1c08')
    require_hash(ROOT/SOURCE/'verification_v1.json','c838e808f881b49a936fa218c9b73ddefb09982098c426bebf95200934918576')
    s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json');reports=[SOURCE+'/selector_cpu_v2.json',SOURCE+'/native_controls_cpu_v1.json',SOURCE+'/baseline_boundary_v2.json']
    require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);meta=read(s['baseline_rom'].replace('.gba','.json'));oldids={u['id'] for r in layout_records(meta) for u in r['layout']};oldowners={r['archive'] for r in layout_records(meta)}
    for path in reports:
        r=read(path)
        if not r['passed'] or r['baseline_sha256']!=s['baseline_sha256'] or r['rom_written']:raise ValueError('039 exact baseline prerequisites')
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    for r in (s,v):
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    pool=source_population(source,set(groups));native={p['archive']:p for p in pool};abi=contracts(source);out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));records=[];seen=set()
    for r in v['archives']:
        arc=r['archive'];gs=groups[arc]
        if arc in oldowners:raise ValueError('039 unexpected carry owner')
        for key in ('source_tpl','target_tpl','compiled'):require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');raw={u.key:u.text for u in literals(original)};units=[];lineage=[]
        for g in gs:
            byid={p['id']:p['layout'] for p in g['layout_proposals']};subset={}
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']));p=byid[u['id']];value=g['explicit_layouts'][u['id']]
                if a['source_sha256']!=sha(source) or a['source_tpl']!=r['source_tpl'] or u['source']!=raw[u['id']] or u['state']!='needs_review' or u['id'] in seen|oldids or p['canonical']!=u['translation'] or p['soft_breaks'] or p['target']!=value or '\n'.join(p['lines'])!=value or reconstruct(p['lines'],p['break_kinds'])!=p['flat_wording'] or value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('039 authored source/wording/layout provenance')
                u['canonical_wording']=u['translation'];u['translation']=value;u['explicit_layout_proposal']=p;units.append(u);lineage.append(d);subset[u['id']]=value;seen.add(u['id'])
            if json.loads(json.dumps(validate(original,replace_exact(original,subset),[g['script']],set(g['ids'])),ensure_ascii=False))!=g['geometry']:raise ValueError('039 communication geometry')
        if units!=r['units']:raise ValueError('039 source compile authored-unit conversion')
        ids={u['id'] for u in units};target=replace_exact(original,{u['id']:u['translation'] for u in units})
        if skeleton(original)!=skeleton(target) or [(u.key,u.language,u.text) for u in literals(target)]!=[(u.key,u.language,u.text) for u in literals((ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig'))]:raise ValueError('039 complete protected target identity')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));n=native[arc]['payload'];payload=(ROOT/r['compiled']['path']).read_bytes();scripts=sorted(g['script'] for g in gs)
        kept=verify_untouched_scripts(n,payload,r['script_count'],set(scripts))
        if kept!=r['unselected_source_scripts'] or sha(n)!=r['source_sha256'] or set(r['source_row']['pointers'])!={p['pointer'] for p in native[arc]['references']}:raise ValueError('039 source table/unselected script contract')
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_ids=sorted(ids),literal_scripts=scripts,script_count=r['script_count'],max_literal_rows=3,max_line_advance=132,preserve_literal_numerals=True,storage='typed-communication-native-identity-ROM-clone',native_root=abi['root'],guarded_reader_return_lr=abi['inner_lr'],saved_outer_reader_return_lr=abi['outer_lr'],original_compressed_source_retained=True)
        layout=validate_characters(target,out/'plugins/exe45-utf8.tbl',scope,ids)
        ap=out/(arc+'_asset.json');asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=arc,source_sha256=sha(source),source_tpl=r['source_tpl'],source_archive_sha256=sha(n),consumer='normal-dialogue',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units,new_ids=sorted(ids),inherited_ids=[],selected_wording_lineage=dict(selection=ref(ROOT/SOURCE/'selection.json'),canonical_drafts=lineage,within_page_LF_only=True,word_boundaries_only=True),insertion_ready=False)
        frozen_write(ap,asset)
        records.append(dict(archive=arc,source_class='communication-help',source_row=r['source_row'],source_lookup_references=native[arc]['references'],source_tpl=r['source_tpl'],target_tpl=r['target_tpl'],asset=ref(ap),compiled=r['compiled'],compiled_bytes=len(payload),compiled_sha256=sha(payload),native_bytes=len(n),native_sha256=sha(n),scope=scope,layout=layout,new_ids=sorted(ids),new_scripts=scripts,inherited_ids=[],parent_record=None,translated_units=len(ids),unselected_source_scripts=kept,profiles=[dict(script=g['script'],profile=g['profile'],geometry=g['geometry']) for g in gs],product_admitted=False))
        print('PASS039 authored input',arc,len(ids),flush=True)
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(records)!=17:raise ValueError('039 registry exact500/17')
    deps=['tools/prepare_communication_inputs039_v1.py','tools/communication_rom_selector039_v1.py','tools/profile_quick_geometry039_v1.py','tools/profile_layout039_v1.py',SOURCE+'/selection.json',SOURCE+'/verification_v1.json']+reports
    frozen_write(out/'manifest.json',dict(schema=1,status='039_AUTHORED_PRODUCT_INPUTS_REGISTERED_NOT_INTEGRATED',source_sha256=sha(source),baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],new_units=500,inherited_units=0,archives=records,source_table_entries=23,source_archives=21,selector_contract=abi,plugin=plugin,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,product_admitted=False,runtime_tested=False,release_eligible=False,limits=['Authored input registration only; build integration and actual039 runtime pending.','CPU selector test skips common initializer tail4FB90..4FC20; complete initialization must be verified by subsequent product runtime.','mmbn45s menu labels, multiplayer negotiation, Hangul name persistence, image leftovers and full-project review not completed.']))
    print('PASS039 registered500 /17 authored assets; NO ROM')


if __name__=='__main__':main()
