"""Freeze exact500 distinct layout inputs; no primary admission or ROM write."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from survey_pet_quick_reflow_024 import place,replace_for_analysis
from normal_page_capacity_024 import validate

FULL='analysis/pending_insertion_500_024_fullbox_v1/survey.json'
QUICK='analysis/pending_insertion_500_024_quick_reflow_v2/survey.json'
NORMAL='analysis/pending_insertion_500_024_normal_v3/survey.json'
FLAGS='analysis/pending_insertion_500_024_pet_flags_v2/survey.json'
OUT='analysis/pending_insertion_500_024_selection_v1/selection.json'


def main():
    full,quick,normal,flags = (read(p) for p in (FULL,QUICK,NORMAL,FLAGS))
    baseline=full['baseline_rom'];digest=full['baseline_sha256']
    require_hash(ROOT/baseline,digest)
    meta=read(baseline.replace('.gba','.json'))
    applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    selected=[];seen=set()
    for profile,report in (('fullbox',full),('quick-within-page-lf-proposal',quick),('normal-pages',normal),('pet-flags-within-page-lf-proposal',flags)):
        if report['baseline_sha256']!=digest or report['rom_written']:
            raise ValueError('Survey baseline scope')
        for g in report['candidate_groups']:
            row=deepcopy(g);row['profile']=profile
            row['explicit_layouts']={key:value['after'] for key,value in g.get('layouts',{}).items()}
            row['explicit_layouts'].update(g.get('individual_layouts',{}))
            if seen & set(g['ids']):raise ValueError('Overlapping candidates')
            seen.update(g['ids']);selected.append(row)
    # One complete two-literal WindMan success script. Only its second literal
    # needs one extra LF; the wording and existing two waited pages are fixed.
    path='translations/virus_practice_success_draft_ko.json';asset=read(path)
    keys=['7C802C:3:0','7C802C:3:1'];units=[];layouts={};links=[]
    cov=read('analysis/translation_first_v1/coverage.json')
    require_hash(ROOT/path,cov['draft_asset_hashes'][path])
    for key in keys:
        u=deepcopy(next(u for u in asset['units'] if u['id']==key));v=place(u['translation'])
        if v is None or v.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('WindMan unchanged wording')
        if v!=u['translation']:layouts[key]=v
        u['translation']=v;units.append(u);links.append(dict(id=key,path=path,sha256=sha((ROOT/path).read_bytes())))
    ref=asset['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);original=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
    geometry=validate(original,replace_for_analysis(original,units),[3],set(keys),full['native_nickname_applicability_bound'],88)
    from verify_tpi_index import parse_tpi
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x7C802C)
    if row['compressed'] or row['size_header'] or not row['pointers'] or seen & set(keys):raise ValueError('WindMan source scope')
    selected.append(dict(profile='normal-within-page-lf-proposal',archive='7C802C',script=3,ids=keys,units=2,drafts=links,source_tpl=ref,explicit_layouts=layouts,geometry=geometry,source_row=row,storage='raw-known-pointer',product_admitted=False));seen.update(keys)
    if len(seen)!=500 or applied & seen or sum(g['units'] for g in selected)!=500:raise ValueError('Exact new500 identities')
    # All links stay source-bound. No mutable or ambiguous canonical wording.
    from compare_archive_payloads import payload_of
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for g in selected:
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);a=read(link['path']);u=next(u for u in a['units'] if u['id']==link['id'])
            if a['source_tpl']!=g['source_tpl'] or a['source_archive_sha256']!=sha(payload_of(source,g['source_row'])) or u['state']!='needs_review':raise ValueError('Canonical source identity')
            value=g['explicit_layouts'].get(u['id'],u['translation'])
            if value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('Selected wording changed')
    deps=[FULL,QUICK,NORMAL,FLAGS,'analysis/pending_insertion_500_024_compile_v2/verification.json','tools/prepare_layout500_024.py','tools/normal_page_capacity_024.py','tools/pet_flag_page_capacity_024.py','analysis/translation_first_v1/coverage.json']
    frozen_write(ROOT/OUT,dict(schema=1,status='EXACT500_SOURCE_LAYOUT_SELECTION_NOT_ROM_ADMISSION',source_sha256=sha(source),baseline_rom=baseline,baseline_sha256=digest,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},planned_new_units=500,profiles={'fullbox':187,'quick-within-page-lf-proposal':85,'normal-pages':186,'pet-flags-within-page-lf-proposal':40,'normal-within-page-lf-proposal':2},groups=selected,selected_ids=sorted(seen),rom_written=False,insertion_ready=False,release_eligible=False,limits='Exact500 not-yet-applied literal IDs. Layout/opaque preserved conditionals are analysis only, not branch-effect/runtime approval. Source-only compile, source-bound product gates, cumulative023 carry merge, final write plan/repro and actual-ROM CPU/GBA verification remain required.'))
    print('PASS exact500 layout selection',len(selected),'whole script groups;',len({g['archive'] for g in selected}),'archives;NO ROM written')


if __name__=='__main__':main()
