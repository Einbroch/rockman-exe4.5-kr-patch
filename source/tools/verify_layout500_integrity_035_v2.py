"""Accept actual024 then reject controlled A3/B0 clone corruptions in memory."""
import argparse
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from field_npc_rom_product_035_v2 import verify_final


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_035_v2.gba')
    p.add_argument('--out',default='analysis/pending500_035_v2/integrity.json');a=p.parse_args()
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
    npc=m['keyitem_rom']['npc035'];first=npc['placements'][0]
    for name,at in [('stub',0x4FB4C),('code',npc['code_offset']),('descriptor',npc['descriptor_offset']),('target-first',first['rom_offset']),('target-last',first['rom_offset']+first['compiled_bytes']-1),('native-first',first['native_copy_offset']),('native-last',first['native_copy_offset']+first['native_copy_bytes']-1),('original-compression',first['source_row']['offset']),('original-pointer',first['source_row']['pointers'][0])]:
        check('NPC-'+name,lambda target,meta,at=at:flip(target,at))
    caller_literal=npc['code_offset']+npc['wrapper']['proof']['literal_offset']
    check('NPC-v1-wrong-return-literal',lambda target,meta:target.__setitem__(caller_literal,0x6F))
    frozen_write(ROOT/a.out,dict(schema=1,passed=True,rom_sha256=sha(rom),positive_valid_product_accepted=True,
        rejected_fixture_count=len(records),fixtures=records,rom_written=False,release_eligible=False,
        limits='Controlled actual035 A3/B0/NPC corruption fixtures, not gameplay or a general malicious-metadata proof.'))
    print('PASS035 valid product accepted;',len(records),'A3/B0/NPC corruption fixtures rejected')


if __name__=='__main__':main()
