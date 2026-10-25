"""Fresh033 canonical pending population; inventory, NOT insertion approval."""
import re
from collections import defaultdict,Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from tpl_literals import literals
from field_hint_capacity import events

BASE='poc/output/pending500_033_v1.gba'
BASE_SHA='7b8c060e97b1eba154327750a7474d001211a68ed1b451363d265256aae26041'
OUT='analysis/pending_insertion_500_034_inventory_v1/census.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'))
    if meta['output_sha256']!=BASE_SHA:raise ValueError('034 current product identity')
    prior=read('analysis/pending500_033_v1/batch_status.json')
    if prior['rom_sha256']!=BASE_SHA or prior['new_units']!=500:raise ValueError('034 previous batch identity')
    applied={u['id'] for r in layout_records(meta) for u in r['layout']};primary={r['archive']:r for r in meta['archives']}
    cov='analysis/translation_first_v1/coverage.json'; old=read('analysis/pending_insertion_500_033_survey_v1/survey.json')
    require_hash(ROOT/cov,old['pinned_coverage']['sha256']);pool=defaultdict(list)
    for p,h in read(cov)['draft_asset_hashes'].items():
        require_hash(ROOT/p,h);a=read(p)
        for u in a['units']:pool[u['id']].append((p,h,u,a))
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    grouped=defaultdict(list); pending=set()
    for key,options in pool.items():
        if key in applied:continue
        if len({(u['source'],u['translation'],u['state']) for _,_,u,_ in options})!=1:raise ValueError('034 conflicting canonical '+key)
        p,h,u,a=options[0]
        if not re.search(r'[\u3040-\u30ff\u3400-\u9fff]',u['source']):continue
        if not u['translation'] or u['state']!='needs_review' or a['source_sha256']!=sha(source):raise ValueError('034 draft policy/source')
        arc,script,ordinal=key.split(':');grouped[arc,int(script)].append((p,h,u,a));pending.add(key)
    groups=[];storage=Counter();topology=Counter();commands=Counter();cache={};hashes={}
    for (arc,script),items in sorted(grouped.items()):
        row=rows[arc];ref=items[0][3]['source_tpl']
        if arc not in cache:
            require_hash(ROOT/ref['path'],ref['sha256']);text=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
            cache[arc]={int(x[1]):x[0] for x in re.finditer(r'^script (\d+) \w+ \{[\s\S]*?(?=^script\s|\Z)',text,re.M)}
            hashes[arc]=sha(payload_of(source,row))
        original='@archive '+arc+'\n'+cache[arc][script];lit={u.key:u.text for u in literals(original)}
        for _,_,u,a in items:
            if a['source_tpl']!=ref or a['source_archive_sha256']!=hashes[arc] or lit.get(u['id'])!=u['source']:raise ValueError('034 source literal binding')
        source_jp={k for k,v in lit.items() if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',v)}
        ids={u['id'] for _,_,u,_ in items};seq=events(original)
        control=[d[0] for _,k,d in seq if k=='command']; significant=[x for x in control if x not in {'mugshotShow','msgOpen','msgOpenQuick','keyWait','clearMsg','end','textSpeed'}]
        route=('compressed' if row['compressed'] else 'size-header' if row['size_header'] else 'unresolved-reference' if not row['pointers'] or row['pointers']==[0] else 'raw-existing' if arc in primary else 'raw-new')
        whole=ids==source_jp and not(source_jp&applied)
        n=len(ids);storage[route]+=n
        if route=='raw-existing' and whole:
            topology[' '.join(sorted(set(significant)))]+=n;commands.update({x:n for x in set(significant)})
        groups.append(dict(archive=arc,script=script,ids=sorted(ids),units=n,source_tpl=ref,source_row=row,source_archive_sha256=hashes[arc],
                           drafts=[dict(id=u['id'],path=p,sha256=h) for p,h,u,_ in items],storage=route,
                           all_japanese_literals_unapplied=whole,already_applied_ids_in_script=sorted(source_jp&applied),commands=control,
                           significant_commands=sorted(set(significant)),selector_count=control.count('select'),product_admitted=False))
    if set().union(*(set(g['ids']) for g in groups))!=pending:raise ValueError('034 census denominator')
    deps=[cov,'analysis/pending500_033_v1/batch_status.json','analysis/pending_insertion_500_033_survey_v1/survey.json','tools/inspect_remaining_034.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='CURRENT033_PENDING_CANONICAL_INVENTORY_NOT_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,
        source_sha256=sha(source),canonical_pending_japanese_units=len(pending),groups=groups,storage_unit_counts=dict(storage),
        raw_existing_whole_script_topologies=dict(topology.most_common()),raw_existing_whole_command_units=dict(commands.most_common()),
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,release_eligible=False,
        limits='Pinned canonical Japanese-text drafts only, not complete-game/image denominator. Whole script classification is not renderer/provider/geometry/caller/storage admission.'))
    print('034 canonical pending',len(pending),'units;',dict(storage));print('RAW-existing whole-script topologies',topology.most_common(22))


if __name__=='__main__':main()
