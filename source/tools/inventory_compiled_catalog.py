"""Reconcile compiled source IDs with the adopted732 archive extraction.

This survey does not consume authored graphics as dialogue assets and does not
claim all ROM text, natural reachability, semantic approval or release readiness.
"""
import argparse,json,re
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from verify_pending500_002_rom import clones,read_payload
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from tpl_literals import literals

def main():
    p=argparse.ArgumentParser()
    for k in ('rom','integration','out'):p.add_argument('--'+k,required=True)
    a=p.parse_args();rp=ROOT/a.rom;meta=read(str(rp.with_suffix('.json').relative_to(ROOT)));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    proof=read(a.integration)
    if not proof['passed'] or proof['rom_sha256']!=sha(rom):raise ValueError('Exact verified artifact prerequisite')
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    if sha(source)!=cfg['source_profile']['sha256']:raise ValueError('Immutable source')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows=parse_tpi(ROOT/cfg['text_catalog']['path']);prior=read('analysis/full_scope_v1/inventory.json');backlog=read('analysis/full_scope_v1/literal_backlog.json')
    if prior['summary']['source_sha256']!=sha(source) or backlog['source_sha256']!=sha(source) or prior['summary']['catalog_sha256']!=cfg['text_catalog']['sha256'] or prior['summary']['parse_errors']:raise ValueError('Adopted extraction/source boundary')
    originals={u['id']:u for u in backlog['units']};arcs={r['archive']:r for r in prior['archives']}
    if len(rows)!=732 or len(arcs)!=732 or len(originals)!=len(backlog['units']):raise ValueError('Catalog population')
    placed=set()
    for _,r in clones(meta):
        if sha(read_payload(rom,r))!=r['compiled_sha256'] or len(r['layout'])!=r['translated_units']:raise ValueError('Compiled population/hash')
        placed.update(u['id'] for u in r['layout'])
    # The manifest adds other consumer populations (chip-name reuse, headers,
    # separately placed raw providers). Its aggregate is NOT a distinct-ID
    # denominator for records carrying an immediate rom_offset.
    selected=set()
    for r in layout_records(meta):
        if len(r['layout'])!=r['translated_units']:raise ValueError('Compiled record population')
        selected.update(u['id'] for u in r['layout'])
    if not placed<=selected:raise ValueError('Placed/compiled record membership')
    statuses=Counter();archives=[];seen=set();pending=[];jp=re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
    for row in rows:
        archive=format(row['offset'],'X');bound=arcs[archive];tp=ROOT/f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
        require_hash(tp,bound['source_tpl_sha256']);native=payload_of(source,row)
        if sha(native)!=bound['source_payload_sha256']:raise ValueError('Source storage identity')
        counts=Counter();ids=[]
        for u in literals(tp.read_text(encoding='utf-8-sig')):
            old=originals[u.key]
            if u.key in seen or old['source']!=u.text or old['language']!=u.language or old['source_tpl_sha256']!=bound['source_tpl_sha256'] or old['source_payload_sha256']!=sha(native):raise ValueError('Extraction literal identity')
            seen.add(u.key)
            status='placed_clone_source_id' if u.key in placed else 'compiled_record_separate_placement' if u.key in selected else 'not_in_compiled_records_japanese' if jp.search(u.text) else 'not_in_compiled_records_non_japanese'
            statuses[status]+=1;counts[status]+=1
            if status=='not_in_compiled_records_japanese':ids.append(u.key);pending.append(u.key)
        archives.append(dict(archive=archive,counts=dict(counts),japanese_ids_absent_from_compiled_records=ids,source_tpl_sha256=bound['source_tpl_sha256'],source_payload_sha256=bound['source_payload_sha256'],compressed=row['compressed'],size_header=row['size_header'],pointers=row['pointers']))
    if seen!=set(originals) or selected-seen:raise ValueError('Extraction/compiled ID population')
    result=dict(schema=1,rom_sha256=sha(rom),source_sha256=sha(source),catalog_sha256=cfg['text_catalog']['sha256'],integration=dict(path=a.integration,sha256=sha((ROOT/a.integration).read_bytes())),prior_extraction=dict(inventory_sha256=sha((ROOT/'analysis/full_scope_v1/inventory.json').read_bytes()),backlog_sha256=sha((ROOT/'analysis/full_scope_v1/literal_backlog.json').read_bytes())),catalog_archives=len(archives),canonical_literals=len(seen),manifest_consumer_units=meta['translated_units'],distinct_compiled_record_ids=len(selected),distinct_placed_clone_ids=len(placed),counts=dict(statuses),archives=archives,release_eligible=False,limits=['Finite catalog732 only; inline text, graphics, input and unknown consumers remain outside this denominator.','Compiled source ID does not imply semantic/human approval or natural scene verification.','Absence from these records does not prove untranslated: chip-name and other providers require their own metadata adapters. Shared/dormant/debug/unknown-context members are not automatically excluded.','Manifest consumer unit count and distinct source-ID populations are different denominators; no global remaining-translation count or completion percentage.'])
    if (ROOT/a.out).exists():raise ValueError('Preserve survey evidence')
    frozen_write(ROOT/a.out,result);print('Catalog reconciliation',dict(statuses),'archives',len(archives))
if __name__=='__main__':main()
