"""Source-root/field/guard binding and locked-word caption layout proposals."""
import re
from collections import Counter
from copy import deepcopy
from itertools import product
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_034 import OUT as CENSUS,BASE,BASE_SHA
from tpl_literals import literals,resolve_units
from survey_aggregate_pet_033 import replace_exact,variants
from pet_list_capacity_034 import validate

OUT='analysis/pending_insertion_500_034_list_layout_v1/survey.json'


def main():
    census=read(CENSUS);require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'))
    provider='analysis/pending_insertion_500_034_list_consumers_cpu_v1/cpu.json';cpu=read(provider)
    if not cpu['passed'] or cpu['baseline_sha256']!=BASE_SHA:raise ValueError('List consumer CPU applicability')
    for p,h in cpu['dependencies'].items():require_hash(ROOT/p,h)
    first=read('analysis/pending_insertion_500_034_list_formatter_cpu_v1/cpu.json');fields={f['list_selector'][0]:f for f in first['fields']}
    roots={r['source_archive'] for r in cpu['roots']};owners={}
    for r in meta['archives']:
        links=[a for a in meta['translation_assets'] if a.get('archive')==r['archive'] and not a.get('scope','').startswith('read-only inherited')]
        if len(links)==1:owners[r['archive']]=links[0]
    good=[];bad=[];templates={};oldassets={};drafts={};excluded=[]
    for g in census['groups']:
        if 'printStringBuffer1' not in g['commands']:continue
        arc,script=g['archive'],g['script']
        if arc not in roots or script not in fields or g['storage']!='raw-existing':
            excluded.append(dict(archive=arc,script=script,units=g['units'],reason='Not declared source producer field/root/storage'));continue
        if arc not in owners:raise ValueError('Ambiguous list parent owner')
        if arc not in templates:
            ref=g['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);templates[arc]=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
            owner=owners[arc];require_hash(ROOT/owner['path'],owner['sha256']);oldassets[arc]=resolve_units(read(owner['path']))
        original='@archive '+arc+'\n'+re.search(r'^script '+str(script)+r' \w+ \{[\s\S]*?(?=^script\s|\Z)',templates[arc],re.M).group()
        sourcelit={u.key:u.text for u in literals(original)};units=[]
        old=[u for u in oldassets[arc] if int(u['id'].split(':')[1])==script]
        if {u['id'] for u in old}!=set(g['already_applied_ids_in_script']):raise ValueError('List parent population mismatch')
        locked={u['id']:u['translation'] for u in old}
        for link in g['drafts']:
            p=link['path']
            if p not in drafts:require_hash(ROOT/p,link['sha256']);drafts[p]=read(p)
            u=next(u for u in drafts[p]['units'] if u['id']==link['id'])
            if u['source']!=sourcelit[u['id']] or u['state']!='needs_review':raise ValueError('List canonical source/state')
            units.append(u)
        errors=[];accepted=None;allids=set(g['ids'])|set(locked)
        choices=[variants(u['source'],u['translation']) for u in units]
        # Finite same-word LF placements only. Validator owns all source
        # controls and aggregate nickname/caption/dynamic-list bounds.
        for values in product(*choices):
            replacements=dict(locked);replacements.update({u['id']:v for u,v in zip(units,values)})
            target=replace_exact(original,replacements)
            try:geometry=validate(original,target,[script],allids,99,fields[script])
            except ValueError as ex:errors.append(str(ex));continue
            accepted=dict(deepcopy(g),profile='pet-native-list-conditional',geometry=geometry,geometry_ids=sorted(allids),native_field=fields[script],explicit_layouts={u['id']:v for u,v in zip(units,values) if v!=u['translation']},locked_parent_units=[dict(id=u['id'],source=u['source'],translation=u['translation'],state=u['state']) for u in old],parent_asset=owners[arc],parent_compiled_script_identity_pending=True,product_admitted=False)
            break
        if accepted:good.append(accepted)
        else:bad.append(dict(archive=arc,script=script,units=g['units'],ids=g['ids'],reason=' | '.join(sorted(set(errors))) or 'No protected-edge placement'))
    deps=[CENSUS,provider,'analysis/pending_insertion_500_034_list_formatter_cpu_v1/cpu.json','tools/survey_pet_lists_034.py','tools/pet_list_capacity_034.py','tools/survey_aggregate_pet_033.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='SOURCE_BOUND_LIST_CAPTION_LAYOUT_PROPOSALS_NOT_COMPILED_OR_ADMITTED',baseline_rom=BASE,baseline_sha256=BASE_SHA,candidate_units=sum(g['units'] for g in good),candidate_groups=good,rejections=bad,excluded=excluded,source_profile_root_count=len(roots),source_field_rows=sorted(f['row'] for f in fields.values()),source_global5_count_pointer=0x0200FA6C,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,release_eligible=False,limits=['Existing canonical words and locked parent literals only; protected controls and finite native guards validated.','Not added to prepared275: compiler/parent/cumulative checks, model refusal fixtures, exact500 gates and own-ROM runtime still required.','Conditional native-valid records only. Full graphics/editor/page lifetime not proven by partial CPU observations; no Hangul commit/save claim.']))
    print('034 list caption proposals',sum(g['units'] for g in good),len(good),'scripts;',len(bad),'rejected;',len(excluded),'excluded;NO ROM')
    print(Counter(g['reason'] for g in bad))


if __name__=='__main__':main()
