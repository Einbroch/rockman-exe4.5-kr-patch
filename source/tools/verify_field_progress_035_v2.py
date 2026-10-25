"""Bind added normal035v2 route observations without promoting diagnostic state."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress


def main():
    rp=ROOT/'poc/output/pending500_035_v2.gba'; m=read(rp.with_suffix('.json')); require_hash(rp,m['output_sha256'])
    cfg=read('project.json'); sp=ROOT/cfg['source_profile']['filename']; require_hash(sp,cfg['source_profile']['sha256'])
    native=lz77_decompress(sp.read_bytes(),0x79D650)[0]
    suffixes=['caller-entry-v1']+['coordinate-route-v'+str(i) for i in range(1,5)]+['coordinate-battle-v2','coordinate-route-v5','coordinate-route-v6']
    results=[]; cached=0
    for suffix in suffixes:
        folder=ROOT/'poc/runtime'/('pending500-035-fixed-'+suffix); r=read(folder/'result.json')
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible',True) is False: raise ValueError('Normal route identity')
        for name,h in r['artifacts'].items():require_hash(folder/name,h)
        parent=read(r['state_origin'])
        if not parent['complete'] or parent['rom_sha256']!=r['rom_sha256'] or parent['artifacts']['checkpoint.mss']!=r['state_sha256'] or parent.get('normal_play_checkpoint_eligible',True) is False:raise ValueError('Normal state edge')
        require_hash(folder/'input.mss',r['state_sha256'])
        ram=(folder/'final_gbaExtWorkRam.bin').read_bytes()
        retained=ram[0x39800:0x39800+len(native)]==native
        # route-v4 ends in an actual battle (directly viewed); field-source
        # residency is not claimed while the battle owns this scratch region.
        if not retained and suffix!='coordinate-route-v4':raise ValueError('Actual native field source identity: '+suffix)
        scene=struct.unpack_from('<I',ram,0xF300)[0]-0x02000000
        player=struct.unpack_from('<I',ram,scene+0x28)[0]-0x02000000
        pos=[v/65536 for v in struct.unpack_from('<3i',ram,player+0x24)]
        obs=read(folder/'field_loader.json'); calls=[x for x in obs['readers'] if x['pc']==0x0804F76E]; cached+=len(calls)
        results.append(dict(path=str(folder.relative_to(ROOT)),receipt_sha256=sha((folder/'result.json').read_bytes()),checkpoint_sha256=r['artifacts']['checkpoint.mss'],position=pos,cached_reader_hits=len(calls),other_readers=obs['readers'],native_source_retained_bytes=len(native) if retained else 0,source_residency_scope='field' if retained else 'battle scratch; no field-residency claim'))
    if cached:raise ValueError('New cached evidence requires display verification before progress report')
    result=dict(passed=True,scope='Added normal-route acquisition and caller observations, NOT native cached display proof',rom_sha256=m['output_sha256'],normal_segments=results,cached_reader_hits=cached,natural_cached_selection_verified=False,diagnostic_display_report='analysis/pending500_035_v2/native_mode_display_v1.json',latest_checkpoint=results[-1]['path']+'/checkpoint.mss',latest_origin=results[-1]['path']+'/result.json',directly_viewed_screens=['pending500-035-fixed-coordinate-route-v4/step_003.png','pending500-035-fixed-coordinate-battle-v2/step_053.png','pending500-035-fixed-coordinate-route-v5/step_002.png','pending500-035-fixed-coordinate-route-v6/step_003.png'],findings=['Normal sourceNPC call6EDEC has actor+9C mode1 for common entrance actor; cached mode0 candidate actors observed separately.','Battle completed, HP100->80. Red bridge reached; position142.75,-144 cannot walk directly toward candidate132,-220 due collision.','Do not repeat straight NW at this edge. Internet1 reference map shows separate green/red routes; map is route hypothesis, not execution proof.'],release_eligible=False,tool_sha256=sha((ROOT/'tools/verify_field_progress_035_v2.py').read_bytes()))
    frozen_write(ROOT/'analysis/pending500_035_v2/normal_field_progress_v2.json',result)
    print('PASS eight normal segments and artifact/state edges; seven field sources retained, one battle residency excluded; natural cached call remains0')


if __name__=='__main__':main()
