"""Reject corrupted hint placement/metadata on an immutable actual-ROM baseline."""
import argparse,copy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from hint_rom_data import verify_final
from keyitem_rom_data import verify_final as verify_selector

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('Preserve integrity evidence')
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();meta=m['keyitem_rom']
    ids=verify_final(source,rom,meta);verify_selector(source,rom,meta)
    if len(ids)!=364:raise ValueError('Hint ID denominator')
    r=meta['hint_archives'][0];cases=[]
    def reject(name,at=None,change=None,selector=False):
        b=bytearray(rom);mm=copy.deepcopy(meta)
        if at is not None:b[at]^=1
        if change:change(mm)
        try:(verify_selector if selector else verify_final)(source,bytes(b),mm)
        except (ValueError,KeyError,IndexError):cases.append(name)
        else:raise ValueError('Accepted corrupt fixture '+name)
    reject('last-native-comparison-byte',r['native_copy_offset']+r['native_copy_bytes']-1)
    reject('clone-last-byte',r['rom_offset']+r['compiled_bytes']-1)
    reject('original-compressed-source',int(r['archive'],16)+4)
    reject('original-table-pointer',r['source_pointers'][0])
    reject('descriptor-selected-slot',meta['hint_guard']['descriptor_address']-0x08000000)
    reject('descriptor-unselected-slot',meta['hint_guard']['descriptor_address']-0x08000000+13*16)
    reject('metadata-selected-unit-count',change=lambda x:x['hint_archives'][0].update(translated_units=r['translated_units']+1))
    reject('metadata-native-capacity-claim',change=lambda x:x['hint_archives'][0].update(native_ram_archive_retained=False))
    reject('metadata-compiled-length',change=lambda x:x['hint_archives'][0].update(compiled_bytes=r['compiled_bytes']-1))
    reject('selector-entry-stub',meta['install_offset'],selector=True)
    reject('selector-final-wrapper',meta['hint_wrapper']['proof']['address']-0x08000000,selector=True)
    frozen_write(out,dict(schema=1,passed=True,rom_sha256=sha(rom),hint_units=len(ids),rejected_fixture_count=len(cases),rejected_fixtures=cases,runtime_tested=False,release_eligible=False))
    print('PASS actual hint integrity;',len(cases),'corruption fixtures rejected')

if __name__=='__main__':main()
