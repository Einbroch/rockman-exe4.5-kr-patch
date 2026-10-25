"""Only newly modeled normal source command forms; preserve compiled272."""
from collections import defaultdict, Counter
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from verify_tpi_index import parse_tpi
from tpl_literals import replace_literals
from fullbox_layout import place
from survey_batch500_017_layout import protected_edges
from normal_page_capacity_024 import validate


def main(out='analysis/pending_insertion_500_024_normal_v3/survey.json'):
    p = 'analysis/pending_insertion_500_024_survey_v1/survey.json'
    s = read(p)
    require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    compiled = read('analysis/pending_insertion_500_024_compile_v2/verification.json')
    existing = {u['id'] for r in compiled['archives'] for u in r['units']}
    require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256'])
    pool = defaultdict(list)
    for path,h in read(s['pinned_coverage']['path'])['draft_asset_hashes'].items():
        require_hash(ROOT/path,h)
        a = read(path)
        for u in a['units']:
            pool[u['id']].append((path,h,u,a))
    cfg = read('project.json')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows = {format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    full = read('analysis/pending_insertion_500_024_fullbox_v1/survey.json')
    good,bad = [],[]
    for g in s['unresolved_groups']+s['candidates']:
        if existing & set(g['ids']) or not set(g.get('reasons',[])) <= {'adopted_normal_geometry','variable_insertion','different_storage_adapter'}:
            continue
        row = rows[g['archive']]
        hint = row['compressed'] and not row['size_header'] and len(row['pointers'])==1 and row['pointers'][0] in range(0x54180,0x541D4,4)
        if row['compressed'] and not hint or row['size_header'] or not row['pointers'] or row['pointers']==[0]:
            continue
        units,refs,layouts = [],[],{}
        for key in g['ids']:
            opts = pool[key]
            if not opts or len({(u['source'],u['translation'],u['state']) for _,_,u,_ in opts})!=1:
                raise ValueError('Frozen wording ambiguity')
            path,h,u,a = opts[0]
            u = deepcopy(u)
            value = place(u['translation'])
            if value is None or not protected_edges(u['source'],value):
                bad.append(dict(archive=g['archive'],script=g['script'],reason='Same-wording layout'));break
            if value != u['translation']:
                layouts[key] = value
            u['translation'] = value
            units.append(u);refs.append(dict(id=key,path=path,sha256=h))
        else:
            ref = a['source_tpl']
            require_hash(ROOT/ref['path'],ref['sha256'])
            original = (ROOT/ref['path']).read_text(encoding='utf-8-sig')
            try:
                geometry = validate(original,replace_literals(original,units),[g['script']],set(g['ids']),full['native_nickname_applicability_bound'],88)
            except ValueError as ex:
                bad.append(dict(archive=g['archive'],script=g['script'],reason=str(ex)));continue
            good.append(dict(archive=g['archive'],script=g['script'],ids=g['ids'],units=len(g['ids']),drafts=refs,source_tpl=ref,individual_layouts=layouts,geometry=geometry,source_row=row,storage='A3-clone-merge' if hint else 'raw-known-pointer',product_admitted=False))
    deps = [p,'analysis/pending_insertion_500_024_compile_v2/verification.json','tools/normal_page_capacity_024.py','tools/survey_normal_pages_024.py']
    frozen_write(ROOT/out,dict(schema=1,status='ADDITIONAL_NORMAL_COMMAND_ANALYSIS_NOT_PRODUCT_ADMISSION',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},candidate_units=sum(g['units'] for g in good),candidate_groups=good,rejection_counts=dict(Counter(g['reason'] for g in bad)),rejections=bad,rom_written=False,release_eligible=False,limits='Excludes already compiled272. Same wording/LF count, explicit normal msgOpen and aggregate180/180/168; timing and portrait source commands preserved. Actual native initialization/portrait applicability, whole binary roundtrip, carry integration, product gate and runtime remain separate.'))
    print('Additional normal candidates',sum(g['units'] for g in good),'groups',len(good));print(Counter(g['reason'] for g in bad).most_common(8))


if __name__ == '__main__':
    main()
