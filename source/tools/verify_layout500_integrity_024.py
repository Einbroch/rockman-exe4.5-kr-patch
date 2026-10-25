"""Accept actual024 then reject controlled A3/B0 clone corruptions in memory."""
import argparse
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from keyitem_rom_data_024 import verify_final


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_024_v1.gba')
    p.add_argument('--out',default='analysis/pending500_024_v1/integrity.json');a=p.parse_args()
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    verify_final(source,rom,m['keyitem_rom']);records=[]
    def check(name,mutate):
        target=bytearray(rom);meta=deepcopy(m['keyitem_rom']);mutate(target,meta)
        try:verify_final(source,bytes(target),meta)
        except (ValueError,KeyError,IndexError) as ex:
            records.append(dict(fixture=name,rejected=True,error=str(ex)));return
        raise ValueError('024 corrupted clone accepted: '+name)
    def flip(target,at):target[at]^=1
    for group,key in [('A3','hint_archives'),('B0','b0_hint_archives')]:
        first=m['keyitem_rom'][key][0];guard='hint_guard' if group=='A3' else 'b0_hint_guard'
        for name,at in [('compiled-first',first['rom_offset']),('compiled-last',first['rom_offset']+first['compiled_bytes']-1),
                        ('native-last',first['native_copy_offset']+first['native_copy_bytes']-1),
                        ('descriptor',m['keyitem_rom'][guard]['descriptor_address']-0x08000000),
                        ('original-pointer',first['source_pointers'][0])]:
            check(group+'-'+name,lambda target,meta,at=at:flip(target,at))
        check(group+'-missing-record',lambda target,meta,key=key:meta[key].pop())
        check(group+'-wrong-layout',lambda target,meta,key=key:meta[key][0]['layout'][0]['line_advance_pixels'].append(1))
        check(group+'-wrong-asset',lambda target,meta,key=key:meta[key][0].update(asset_sha256='0'*64))
    frozen_write(ROOT/a.out,dict(schema=1,passed=True,rom_sha256=sha(rom),positive_valid_product_accepted=True,
        rejected_fixture_count=len(records),fixtures=records,rom_written=False,release_eligible=False,
        limits='Controlled frozen024 A3/B0 corruption fixtures, not gameplay or a general malicious-metadata proof.'))
    print('PASS024 valid product accepted;',len(records),'A3/B0 corruption fixtures rejected')


if __name__=='__main__':main()
