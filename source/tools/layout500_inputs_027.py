"""Fail-closed027 admission: exact500 direct-profile literals in11 new RAW arcs.

No arbitrary user records or Hangul persistence claim. Bounds require the
unchanged native editor/reader and valid native records, not descriptor bytes.
"""
import re
import struct
from collections import Counter, defaultdict
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from tpl_literals import literals, resolve_units, skeleton
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from prepare_repartition500 import layout_records
from survey_pet_quick_reflow_024 import replace_for_analysis
from pet_profile_capacity_027_v2 import validate as profile_validate
from profile_provider_bounds_027_v2 import bounds
from build_development_patch import validate_literal_numerals
from prepare_layout500_027 import OUT as SELECTION, CPU, TESTS, SURVEY, verify_dependencies

MANIFEST='analysis/pending_insertion_500_027_carry_v2/preflight.json'
MANIFEST_SHA='2824eef4e7155308205752249f3417841bdceb2b9ee9cc747e9298fe0865d3c0'
OUT='analysis/pending_insertion_500_027_input_gate_v1/verification.json'


def checked_ref(ref):
    require_hash(ROOT/ref['path'],ref['sha256'])
    return ROOT/ref['path']


def values(tpl):
    return [(i.key,i.language,i.text) for i in literals(tpl)]


def load_inputs(source):
    require_hash(ROOT/MANIFEST,MANIFEST_SHA)
    manifest=read(MANIFEST);selection=read(SELECTION)
    mechanical=read('analysis/pending_insertion_500_027_compile500_v1/verification.json')
    for record in (manifest,selection,mechanical,read(TESTS),read(SURVEY)):
        verify_dependencies(record)
    if not manifest['passed'] or not mechanical['passed'] or manifest['source_sha256']!=sha(source):
        raise ValueError('027 immutable source/compiler applicability')
    baseline_path=ROOT/manifest['baseline_rom'];require_hash(baseline_path,manifest['baseline_sha256'])
    baseline=baseline_path.read_bytes();meta=read(baseline_path.with_suffix('.json'))
    checked_ref(selection['baseline_metadata'])
    cpu=read(CPU);require_hash(ROOT/'tools/bench_profile_providers_027_v2.py',cpu['tool_sha256'])
    if not cpu['passed'] or cpu['case_count']!=304 or cpu['baseline_sha256']!=sha(baseline) or bounds(source,baseline)!=cpu['provider_bounds']:
        raise ValueError('027 actual026 native304 applicability')
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    from verify_tpi_index import parse_tpi
    catalog={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    parents={r['archive'] for r in layout_records(meta)}
    applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    groups=defaultdict(list)
    for g in selection['groups']:groups[g['archive']].append(g)
    if len(manifest['archives'])!=11 or len(groups)!=11 or set(groups)!={r['archive'] for r in manifest['archives']}:
        raise ValueError('027 exact newRAW archive population')
    seen=set();counts=Counter();admitted=[]
    for r in manifest['archives']:
        arc=r['archive'];row=r['source_row']
        if arc in parents or r['storage']!='new-raw' or r['old_record'] is not None or r['parent'] is not None or r['carry_units']:
            raise ValueError('027 not genuinely new raw archive')
        if row!=catalog[arc] or row['compressed'] or row['size_header'] or not row['pointers']:
            raise ValueError('027 source catalog RAW storage')
        native=payload_of(source,row)
        if sha(native)!=r['source_payload_sha256'] or baseline[row['offset']:row['offset']+row['size']]!=native:
            raise ValueError('027 native storage applicability')
        for p in row['pointers']:
            if struct.unpack_from('<I',source,p)[0]!=0x08000000+row['offset'] or baseline[p:p+4]!=source[p:p+4]:
                raise ValueError('027 source pointer applicability')
        if checked_ref(r['carry_compiled']).read_bytes()!=native or sha(native)!=r['parent_compiled_sha256']:
            raise ValueError('027 native parent reconstruction')
        units=resolve_units(read(checked_ref(r['merged_asset'])));ids={u['id'] for u in units}
        if len(ids)!=len(units) or ids!=set(r['new_ids']) or ids&(seen|applied) or len(ids)!=r['new_units']:
            raise ValueError('027 distinct exact new literal IDs')
        original=checked_ref(groups[arc][0]['source_tpl']).read_text(encoding='utf-8-sig')
        target=checked_ref(r['merged_tpl']).read_text(encoding='utf-8-sig')
        if skeleton(original)!=skeleton(target) or values(target)!=values(replace_for_analysis(original,units)):
            raise ValueError('027 protected commands/unselected literals changed')
        for g in groups[arc]:
            if g['source_row']!=row or g['profile']!='pet-direct-profile':raise ValueError('027 unsupported consumer')
            selected=set(g['ids']);subset=[u for u in units if u['id'] in selected]
            whole={i.key for i in literals(original) if int(i.key.split(':')[1])==g['script'] and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',i.text)}
            if whole!=selected or selected!={u['id'] for u in subset}:raise ValueError('027 whole-script literal denominator')
            expected=[]
            for link in g['drafts']:
                a=read(checked_ref(link));matches=[u for u in a['units'] if u['id']==link['id']]
                if len(matches)!=1 or a['source_tpl']!=g['source_tpl']:raise ValueError('027 source/draft identity')
                u=matches[0];v=g['explicit_layouts'].get(u['id'],u['translation'])
                if u['state']!='needs_review' or v.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('027 unapproved prose/state change')
                expected.append(dict(id=u['id'],source=u['source'],translation=v,state=u['state']))
            if sorted(expected,key=lambda u:u['id'])!=sorted(subset,key=lambda u:u['id']):raise ValueError('027 wording identity')
            proposed=replace_for_analysis(original,subset)
            proof=profile_validate(original,proposed,[g['script']],selected,selection['native_nickname_bound'])
            if proof!=g['geometry']:raise ValueError('027 current direct-provider page geometry')
            counts[g['profile']]+=len(subset)
        validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        payload=checked_ref(r['compiled']).read_bytes()
        if len(payload)!=r['compiled_bytes'] or len(payload)>65535:raise ValueError('02716bit payload extent')
        if verify_untouched_scripts(native,payload,r['script_count'],set(r['new_scripts']))!=r['unselected_parent_scripts']:
            raise ValueError('027 untouched script bytes changed')
        if set(r['new_scripts'])!={int(i.split(':')[1]) for i in ids}:raise ValueError('027 script scope')
        seen|=ids;admitted.append((r,payload))
    if len(seen)!=500 or seen!=set(selection['selected_ids']) or counts!=Counter(selection['profiles']):raise ValueError('027 exact500 union')
    return admitted,dict(new_units=500,carry_units=0,archives=11,profiles=dict(counts),storage={'new-raw':11})


def main():
    cfg=read('project.json');p=ROOT/cfg['source_profile']['filename'];require_hash(p,cfg['source_profile']['sha256'])
    _,summary=load_inputs(p.read_bytes())
    deps=[MANIFEST,SELECTION,CPU,TESTS,'tools/layout500_inputs_027.py','tools/pet_profile_capacity_027_v2.py','tools/profile_provider_bounds_027_v2.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='SOURCE_BOUND027_INPUT_GATE_PASS_NOT_ROM',passed=True,**summary,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,runtime_tested=False,release_eligible=False,limits='Valid native profile records only; actual027 allocation/write plan/repro/runtime pending. No Hangul commit/save/redisplay claim.'))
    print('PASS027 input gate',summary)


if __name__=='__main__':main()
