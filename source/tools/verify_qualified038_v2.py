"""Exact038 qualified new NPC/hint native-load to font/OBJ/pixel evidence.

Separate original-source load and real-caller runs join by full payload
identity only. Does not prove natural A4 or A3/ShadowMan acquisition.
"""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_038_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();manifest=read('analysis/pending_insertion_500_038_native_inputs_v1/manifest.json');rows=[];receipts={}
    cases=[('npc','7B5110',0,0x02039800,0x0804F773,0x0804F76E,0x0806EDF1,2,3,4,'qualified_native_001.bin'),('hint','78AE58',10,0x0203D800,0x0804F807,0x0804F802,0x0806A825,1,2,3,'qualified_hint_001.bin')]
    for kind,arc,script,nroot,caller,bl,upstream,page,closed,moved,filename in cases:
        ld=ROOT/f'poc/runtime/pending500-038-{kind}-qualified-load-v1';d=ROOT/f'poc/runtime/pending500-038-{kind}-qualified-boundary-v1';load=read(ld/'result.json');r=read(d/'result.json');payload=lz77_decompress(source,int(arc,16))[0]
        for folder,result in [(ld,load),(d,r)]:
            if not result['complete'] or result['rom_sha256']!=sha(rom) or result['normal_play_checkpoint_eligible'] is not False or len(result['loaded_rom_guards'])!=4 or result['target_archive']!=arc:raise ValueError('038 qualified identity/scope')
            if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Diagnostic state quarantine')
            for name,h in result['artifacts'].items():require_hash(folder/name,h)
            receipts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        if (ld/filename).read_bytes()!=payload or load['native_sha256']!=sha(payload) or not load['native_source_pointer_and_LZ_unmodified'] or load['selector_display_verified']:raise ValueError('038 original native load boundary')
        require_hash(ROOT/r['native_load_prerequisite']['path'],r['native_load_prerequisite']['sha256'])
        if r['native_load_prerequisite']['decompressed_sha256']!=sha(payload):raise ValueError('038 joined source identity')
        parent=ROOT/r['state_origin'];pr=read(parent)
        if not pr['complete'] or pr['rom_sha256']!=sha(rom) or pr.get('normal_play_checkpoint_eligible') is False or r['state_sha256']!=pr['artifacts']['checkpoint.mss']:raise ValueError('Own038 normal input state')
        require_hash(parent.parent/'checkpoint.mss',r['state_sha256']);receipts[str(parent.relative_to(ROOT))]=sha(parent.read_bytes())
        b=r['resident_boundary']
        if b['scene_reads']!=1 or b['resident_reads']<len(payload) or (b['min_offset'],b['max_offset'])!=(0,len(payload)-1):raise ValueError('038 full native resident comparison')
        rec=next(x for x in m['keyitem_rom']['npc038']['archives'] if x['archive']==arc);assetref=next(x for x in manifest['archives'] if x['archive']==arc)['asset'];require_hash(ROOT/assetref['path'],assetref['sha256']);asset=read(assetref['path'])
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,255,record=rec,asset=asset)
        if len(units)!=1:raise ValueError('Finite one-page literal scope')
        key=units[0]['id'];ee={s:expected[s] for s in streams[key]}
        calls=read(d/'native_selector.json')['selectors'];readers=read(d/'field_loader.json')['readers']
        if len(calls)!=1 or len(readers)!=1:raise ValueError('Exactly one real original caller')
        call=calls[0];reader=readers[0]
        if (call['script'],call['root'],call['caller_lr'],call['native_root'])!=(0,pool,caller,nroot) or (reader['pc'],reader['r0'],reader['r1'],reader['lr'])!=(bl,nroot,0,upstream):raise ValueError('Original provider/BL/root/selector contract')
        cp=f'step_{page:03}';ram=(d/(cp+'_gbaExtWorkRam.bin')).read_bytes();t=read(d/(cp+'_roll_pet.json'));draws={x['stream']:x for x in t['draws'] if x['stream'] in ee}
        if struct.unpack_from('<2I',ram,0xFA4C)!=(ends[key],pool) or tuple(ram[0xFA38:0xFA3A])!=(52,110) or set(draws)!=set(ee) or any(x['context']!=0x0200FA20 or x['glyph_index']!=ee[s]['index'] for s,x in draws.items()):raise ValueError('038 current Korean page/glyph/context')
        if rom[ends[key]-0x08000000:ends[key]-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Original wait boundary')
        counts=Counter(x['index'] for x in ee.values());reads={x['index']:x['reads'] for x in t['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('038 actual font CPU supply')
        for x in draws.values():
            line,off=divmod(x['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*x['glyph_index'])[0]
            if not 0<=line<3 or off%4 or off//4+width>(168 if line==2 else 180):raise ValueError('038 actual text extent')
        proof=pixels(d,page,list(draws.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True)
        before=(d/f'step_{closed:03}_gbaExtWorkRam.bin').read_bytes();after=(d/f'step_{moved:03}_gbaExtWorkRam.bin').read_bytes();original=(parent.parent/'final_gbaExtWorkRam.bin').read_bytes()
        for mem in (ram,before,after):
            if mem[nroot-0x02000000:nroot-0x02000000+0x1000]!=original[nroot-0x02000000:nroot-0x02000000+0x1000] or mem[0x4ad4]!=0xA0 or mem[0x4ad1]!=0:raise ValueError('Qualified alias changed real native RAM/scene/Navi')
        if before[0xFB54:0xFB60]==after[0xFB54:0xFB60]:raise ValueError('Post-close movement absent')
        for step in (closed,moved):
            o=(d/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
            if any(not a&0x2300 and k>>12==14 for i in range(128) for a,c,k in [struct.unpack_from('<3H',o,i*8)]):raise ValueError('Closed dialogue OBJ remains')
        rows.append(dict(kind=kind,archive=arc,id=key,native_bytes=len(payload),native_sha256=sha(payload),selector=call,resident_boundary=b,page=page,pixels=proof,closed=closed,movement=moved,natural_acquisition_verified=False,agent_visual_review_pending=True))
    deps=['tools/verify_qualified038_v2.py','tools/capture_native_load038_v2.py','tools/capture_native_boundary038_v1.py','tools/capture_hint_load038_v1.py','tools/capture_hint_boundary038_v1.py','tools/report_roll_pet.py','tools/verify_pending500_005_displays.py','analysis/pending_insertion_500_038_native_inputs_v1/manifest.json']
    frozen_write(ROOT/'analysis/pending500_038_v2/qualified_npc_hint_v1.json',dict(passed=True,rom_sha256=sha(rom),scope=__doc__,rows=rows,receipts=receipts,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},release_eligible=False,natural_acquisition_verified=False,limits=['Two representative qualified new pages only, not all500 screens or natural target acquisition.','Muted Mesen, no hardware/audio/timing certification. Hangul commit/save/redisplay and full human review open.']))
    print('PASS038 qualified new NPC/hint native LZ, real callers, selector, Korean font/OBJ/pixels and close/movement')

if __name__=='__main__':main()
