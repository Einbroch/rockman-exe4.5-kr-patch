"""Verify actual cumulative500 ROM, independent rebuild, writes and selectors."""
import argparse,json,struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,verify_product_lineage,entries,frozen_write
from keyitem_rom_data import verify_final
from audit_startup_ui import audit
ROM_LINEAGE=verify_product_lineage
ENTRIES=entries

def main():
    ap=argparse.ArgumentParser()
    for key in ('rom','cpu','out'):ap.add_argument('--'+key,required=True)
    a=ap.parse_args();rp=ROOT/a.rom;meta=read(str(rp.with_suffix('.json').relative_to(ROOT)));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    proof=ROM_LINEAGE(source,rom,meta);proof['merged_archives']=sorted(proof['merged_archives'])
    records={r['archive']:r for r in meta['archives']}
    for _,row,asset,_,_,_ in ENTRIES(source):
        record=records[asset['archive']]
        for p in row['pointers']:
            if struct.unpack_from('<I',rom,p)[0]!=0x08000000+record['rom_offset']:raise ValueError('Final pointer binding')
    verify_final(source,rom,meta['keyitem_rom'])
    cpu=read(a.cpu)
    if not cpu['passed'] or cpu['rom_sha256']!=sha(rom):raise ValueError('Selector CPU binding')
    result=dict(passed=True,rom=a.rom,rom_sha256=sha(rom),new_units=proof['new_units'],total_units=meta['translated_units'],primary_archives=len(meta['archives']),lineage=proof,artifact_audit=audit(rp),cpu_vectors=cpu['vectors'],runtime_scene_approval=False,release_eligible=False,limits='All selected natural routes, choices/results/persistence and automatic Hangul input/save remain unverified.')
    if (ROOT/a.out).exists():raise ValueError('Preserve verification evidence')
    frozen_write(ROOT/a.out,result);print('PASS actual',proof['new_units'],'delta; total',meta['translated_units'],'carry scripts preserved; independent rebuild identical')
if __name__=='__main__':main()
