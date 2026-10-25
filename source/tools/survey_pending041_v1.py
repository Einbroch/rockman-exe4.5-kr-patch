"""Current040 canonical pending language/control census; no input adoption/ROM."""
import re
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of

BASE='poc/output/pending500_040_v2.gba'
BASE_SHA='bf97f861fc244861d2728c67eff4adaf84e532bc321665073908b9e621add570'
OUT='analysis/pending_insertion_500_041_inventory_v1/census.json'
CENSUS='analysis/pending_insertion_500_035_inventory_v1/census.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'));rom=(ROOT/BASE).read_bytes();status=read('analysis/pending500_040_v2/batch_status.json')
    if status['current_ROM_sha256']!=BASE_SHA or not status['new040_three_classes_Korean_runtime_verified']:raise ValueError('040 exact artifact/representative prerequisite')
    c=read(CENSUS);applied={u['id'] for r in layout_records(meta) for u in r['layout']};pending={k for g in c['groups'] for k in g['ids']}-applied
    if len(pending)!=9424 or meta['translated_units']!=21122:raise ValueError('041 canonical remainder')
    cache={};archives={};groups=[];language=Counter();controls=Counter();storage=Counter();owners=defaultdict(list)
    for r in layout_records(meta):owners[r['archive']].append({k:r[k] for k in ('rom_offset','compiled_sha256','compiled_bytes') if k in r})
    for g in c['groups']:
        ids=set(g['ids'])&pending
        if not ids:continue
        if ids!=set(g['ids']):raise ValueError('041 partial-script canonical census requires reconciliation')
        arc=g['archive'];ref=g['source_tpl']
        if arc not in cache:
            require_hash(ROOT/ref['path'],ref['sha256']);text=(ROOT/ref['path']).read_text(encoding='utf-8-sig');cache[arc]={int(s):lang for s,lang in re.findall(r'^script (\d+) (\w+) \{',text,re.M)};native=payload_of(source,g['source_row'])
            if sha(native)!=g['source_archive_sha256']:raise ValueError('041 original native source identity')
            archives[arc]=dict(archive=arc,source_row=g['source_row'],source_tpl=ref,native_bytes=len(native),native_sha256=sha(native),current_owners=owners[arc])
        lang=cache[arc][g['script']];entry=dict(g,literal_language=lang,current_owners=owners[arc],current041_pending=True);groups.append(entry);language[(lang,g['storage'])]+=len(ids);storage[g['storage']]+=len(ids);controls[(lang,tuple(g['significant_commands']))]+=len(ids)
    result=dict(status='041_CURRENT039_PENDING_SOURCE_CENSUS_NOT_PRODUCT_INPUT',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),applied_IDs=len(applied),pending_IDs=len(pending),pending_scripts=len(groups),pending_archives=len(archives),language_storage_counts=[dict(language=k[0],storage=k[1],units=n) for k,n in language.most_common()],control_counts=[dict(language=k[0],commands=list(k[1]),units=n) for k,n in controls.most_common()],storage_counts=dict(storage),archives=list(archives.values()),groups=groups,rom_written=False,product_admitted=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in [CENSUS,'tools/survey_pending041_v1.py','analysis/pending500_040_v2/integration.json','analysis/pending500_040_v2/communication_runtime_v1.json']},limits=['Canonical draft IDs only; not total game/image workload.','No current translated text changed, no new source selection, compilation, consumer admission or040 ROM.'])
    frozen_write(ROOT/OUT,result)
    print('041 pending',len(pending),'scripts',len(groups),'archives',len(archives));print(result['language_storage_counts']);print('top controls',result['control_counts'][:16])


if __name__=='__main__':main()


