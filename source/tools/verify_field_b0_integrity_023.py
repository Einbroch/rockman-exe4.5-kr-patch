"""Actual-ROM corruption fixtures; reject partial/corrupt B0 clone integration."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from keyitem_rom_data import verify_final


def main():
    rp=ROOT/'poc/output/pending500_023_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    verify_final(source,rom,m['keyitem_rom']);records=[]
    def check(name,mutate):
        target=bytearray(rom);meta=deepcopy(m['keyitem_rom']);mutate(target,meta)
        try:verify_final(source,bytes(target),meta)
        except (ValueError,KeyError,IndexError) as ex:records.append(dict(fixture=name,rejected=True,error=str(ex)));return
        raise ValueError('Corruption accepted: '+name)
    def flip(target,at):target[at]^=1
    first=m['keyitem_rom']['b0_hint_archives'][0]
    for name,at in [('compiled-byte',first['rom_offset']),('native-compare-first',first['native_copy_offset']),('native-compare-last',first['native_copy_offset']+first['native_copy_bytes']-1),('descriptor',m['keyitem_rom']['b0_hint_guard']['descriptor_address']-0x08000000),('original-compressed',int(first['archive'],16)),('original-pointer',first['source_pointers'][0]),('original-loader',0x4F734),('new-wrapper-code',m['keyitem_rom']['b0_hint_wrapper']['proof']['address']-0x08000000),('composed-installer',0x4FB4C)]:
        check(name,lambda target,meta,at=at:flip(target,at))
    check('missing-record',lambda target,meta:meta['b0_hint_archives'].pop())
    check('wrong-native-extent',lambda target,meta:meta['b0_hint_archives'][0].update(native_copy_bytes=1))
    check('wrong-navi',lambda target,meta:meta['b0_hint_archives'][0].update(navi_index=1))
    check('wrong-asset-identity',lambda target,meta:meta['b0_hint_archives'][0].update(asset_sha256='0'*64))
    check('wrong-layout',lambda target,meta:meta['b0_hint_archives'][0]['layout'][0]['line_advance_pixels'].append(1))
    check('unregistered-descriptor-field',lambda target,meta:meta['b0_hint_guard'].update(unknown=0))
    frozen_write(ROOT/'analysis/pending500_023_v1/integrity.json',dict(schema=1,passed=True,rom_sha256=sha(rom),positive_valid_product_accepted=True,rejected_fixture_count=len(records),fixtures=records,rom_written=False,release_eligible=False,limits='Controlled corruption of one frozen product in memory, not gameplay or a general malicious-metadata proof. Source loader/table/compressed storage, descriptor, cloned source/text/layout identity, wrapper and composed stub covered.'))
    print('PASS B0 valid product accepted; corruption fixtures rejected',len(records))


if __name__=='__main__':main()
