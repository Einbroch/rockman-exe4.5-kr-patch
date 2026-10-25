"""Controlled in-memory corruption rejection for actual036 three scene classes."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from field_npc_rom_product_036_v1 import verify_final

def main():
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();verify_final(source,rom,m['keyitem_rom']);rows=[];n=m['keyitem_rom']['npc036']
    def test(name,mutate):
        target=bytearray(rom);meta=deepcopy(m['keyitem_rom']);mutate(target,meta)
        try:verify_final(source,bytes(target),meta)
        except (ValueError,KeyError,IndexError) as e:rows.append(dict(name=name,rejected=True,error=str(e)));return
        raise ValueError('036 corrupted component accepted: '+name)
    def flip(t,at):t[at]^=1
    for scene in (0xA0,0xA1,0xA3):
        i=next(i for i,p in enumerate(n['placements']) if p['scene']==scene);p=n['placements'][i]
        positions={'target-first':p['rom_offset'],'target-last':p['rom_offset']+p['compiled_bytes']-1,'native-first':p['native_copy_offset'],'native-last':p['native_copy_offset']+p['native_copy_bytes']-1,'original-compression':p['source_row']['offset'],'original-pointer':p['source_row']['pointers'][0]}
        positions.update({field:n['descriptor_offset']+i*16+j*4 for j,field in enumerate(['descriptor-target','descriptor-native','descriptor-size','descriptor-scene'])})
        for name,at in positions.items():test(hex(scene)+'-'+name,lambda t,meta,at=at:flip(t,at))
        test(hex(scene)+'-metadata-scene',lambda t,meta,i=i:meta['npc036']['placements'][i].update(scene=0xB0))
    for name,at in [('stub',0x4FB4C),('wrapper-first',n['code_offset']),('wrapper-last',n['code_offset']+n['code_bytes']-1),('prior035-wrapper',m['keyitem_rom']['npc035']['code_offset'])]:test(name,lambda t,meta,at=at:flip(t,at))
    test('missing-placement',lambda t,meta:meta['npc036']['placements'].pop())
    test('wrong-chain-address',lambda t,meta:meta['npc035'].update(code_offset=meta['npc035']['code_offset']+4))
    frozen_write(ROOT/'analysis/pending500_036_v1/integrity_v1.json',dict(passed=True,rom_sha256=sha(rom),valid_product_accepted=True,rejected_fixture_count=len(rows),fixtures=rows,rom_written=False,runtime_tested=False,release_eligible=False,scope='Controlled actual artifact byte/metadata corruption refusal in memory, not all malformed input or runtime proof',dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_integrity036_v1.py','tools/field_npc_rom_product_036_v1.py']}))
    print('PASS036 valid image accepted;',len(rows),'actual-image in-memory corruption fixtures rejected')

if __name__=='__main__':main()
