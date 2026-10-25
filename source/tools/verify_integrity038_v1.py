"""Actual038 byte/metadata corruption rejection, memory-only diagnostic."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from field_native_rom_product_038_v2 import verify_final


def main():
    rp=ROOT/'poc/output/pending500_038_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();verify_final(source,rom,m['keyitem_rom']);rows=[];n=m['keyitem_rom']['npc038']
    def test(name,mutate):
        target=bytearray(rom);meta=deepcopy(m['keyitem_rom']);mutate(target,meta)
        try:verify_final(source,bytes(target),meta)
        except (ValueError,KeyError,IndexError) as e:rows.append(dict(name=name,rejected=True,error=str(e)));return
        raise ValueError('038 corrupted component accepted: '+name)
    def flip(t,at):t[at]^=1
    classes=[(kind,next(p['scene'] for p in n['placements'] if p['source_class']==kind)) for kind in sorted({p['source_class'] for p in n['placements']})]
    for kind,scene in classes:
        i=next(i for i,p in enumerate(n['placements']) if (p['source_class'],p['scene'])==(kind,scene));p=n['placements'][i]
        positions={'target-first':p['rom_offset'],'target-last':p['rom_offset']+p['compiled_bytes']-1,'native-first':p['native_copy_offset'],'native-last':p['native_copy_offset']+p['native_copy_bytes']-1,'original-compression':p['source_row']['offset'],'original-pointer':p['source_row']['pointers'][0]}
        positions.update({field:n['descriptor_offset']+i*28+j*4 for j,field in enumerate(['descriptor-target','descriptor-native','descriptor-size','descriptor-scene','descriptor-root','descriptor-caller','descriptor-script-count'])})
        for name,at in positions.items():test(kind+'-'+hex(scene)+'-'+name,lambda t,meta,at=at:flip(t,at))
        print('PASS038 corruption group',kind,hex(scene),flush=True)
    for name,at in [('stub',0x4FB4C),('wrapper-first',n['code_offset']),('wrapper-last',n['code_offset']+n['code_bytes']-1),('prior037-wrapper',m['keyitem_rom']['npc037']['code_offset'])]:test(name,lambda t,meta,at=at:flip(t,at))
    test('missing-placement',lambda t,meta:meta['npc038']['placements'].pop())
    test('wrong-chain-address',lambda t,meta:meta['npc037'].update(code_offset=meta['npc037']['code_offset']+4))
    frozen_write(ROOT/'analysis/pending500_038_v2/integrity_v1.json',dict(passed=True,rom_sha256=sha(rom),valid_product_accepted=True,rejected_fixture_count=len(rows),fixtures=rows,rom_written=False,runtime_tested=False,release_eligible=False,scope='Controlled actual artifact byte/metadata corruption refusal in memory; not all malformed input or runtime',dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_integrity038_v1.py','tools/field_native_rom_product_038_v2.py']}))
    print('PASS038',len(rows),'actual-image corruption refusals')


if __name__=='__main__':main()
