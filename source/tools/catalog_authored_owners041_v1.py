"""Resolve040 physical consumer records back to authored assets, never ROM text."""
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import resolve_units
from prepare_repartition500 import layout_records
from survey_pending041_v1 import BASE,BASE_SHA
from verify_tpi_index import lz77_decompress


def main():
    require_hash(ROOT/BASE,BASE_SHA);m=read(BASE.replace('.gba','.json'));rom=(ROOT/BASE).read_bytes();index=defaultdict(list);seen=set()
    for entry in m['translation_assets']:
        pair=(entry['path'].replace('\\','/'),entry['sha256'])
        if pair in seen:continue
        seen.add(pair);require_hash(ROOT/entry['path'],entry['sha256']);a=read(entry['path'])
        if a.get('schema') not in (1,2) or not isinstance(a.get('units'),list) or not a.get('archive'):continue
        units=resolve_units(a)
        if len({u['id'] for u in units})!=len(units):raise ValueError('041 authored owner duplicate units')
        index[(a['archive'],frozenset(u['id'] for u in units))].append(dict(path=pair[0],sha256=pair[1]))
    rows=[];missing=[]
    for r in layout_records(m):
        if 'rom_offset' not in r:continue
        ids=frozenset(u['id'] for u in r['layout']);candidates=index[(r['archive'],ids)];payload=rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']]
        if r.get('compression'):
            cp=r['compression'];payload,used=lz77_decompress(rom,r['rom_offset'])
            if sha(rom[r['rom_offset']:r['rom_offset']+cp['stored_bytes']])!=cp['stored_sha256'] or used>cp['stored_bytes']:raise ValueError('041 compressed physical storage')
        if sha(payload)!=r['compiled_sha256']:raise ValueError('041 prior physical consumer hash')
        row=dict(archive=r['archive'],rom_offset=r['rom_offset'],compiled_sha256=r['compiled_sha256'],compiled_bytes=r['compiled_bytes'],ids=sorted(ids),authored_set_matches=candidates,compiled_authored_match_verified=False)
        rows.append(row)
        if not candidates:missing.append(dict(archive=r['archive'],rom_offset=r['rom_offset'],units=len(ids)))
    out=dict(status='041_AUTHORED_OWNER_SET_CATALOG_NOT_RECOMPILE_OR_PRODUCT_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,physical_records=len(rows),authored_set_match_records=sum(bool(x['authored_set_matches']) for x in rows),missing_set_matches=missing,records=rows,rom_written=False,product_admitted=False,release_eligible=False,limits=['Set equality only: recompile candidate authored words and compare exact current physical payload before carry admission.','Multiple payload variants may share IDs with differing layout; never resolve them by last-writer wins.','Metadata-only records without rom_offset remain in040 metadata; this catalog has only physical consumers.'],dependencies={'tools/catalog_authored_owners041_v1.py':sha((ROOT/'tools/catalog_authored_owners041_v1.py').read_bytes())})
    frozen_write(ROOT/'analysis/pending_insertion_500_041_inventory_v1/authored_owners.json',out)
    print('041 physical authored-set matches',out['authored_set_match_records'],'/',len(rows),'unresolved',len(missing))


if __name__=='__main__':main()
