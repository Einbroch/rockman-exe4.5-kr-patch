"""Normal native loaded NPC -> corrected clone -> current Korean pixels proof."""
import argparse,struct
from collections import Counter
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from verify_pending500_005_displays import model
from report_roll_pet import pixels
from field_npc_rom_product_036_v1 import verify_final

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--folder',required=True);ap.add_argument('--step',required=True,type=int);ap.add_argument('--out',required=True);args=ap.parse_args()
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();verify_final(source,rom,m['keyitem_rom'])
    folder=ROOT/args.folder;cp=f'step_{args.step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();ptr,pool=struct.unpack_from('<2I',ram,0xFA4C)
    records=m['keyitem_rom']['npc036']['archives'];record=next(r for r in records if 0x08000000+r['rom_offset']==pool);arc=record['archive']
    manifest=read('analysis/pending_insertion_500_036_npc_inputs_v1/manifest.json');entry=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(entry['asset']['path'])
    chain=[];loads=[];origin=folder/'result.json';seen=set()
    while origin:
        if origin in seen:raise ValueError('checkpoint origin cycle')
        seen.add(origin);r=read(origin);d=origin.parent
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('not current normal chain')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        chain.append({'path':str(origin.relative_to(ROOT)),'sha256':sha(origin.read_bytes())})
        if (d/'field_loader.json').exists():
            events=read(d/'field_loader.json');starts=[e for e in events['events'] if e['pc']==0x0804F724]
            for i,e in enumerate(starts,1):
                if e['r0']!=0x08000000+int(arc,16) or e['scene']!=0xA0:continue
                native=lz77_decompress(source,int(arc,16))[0]
                if (d/f'load_{i:03d}_02039800.bin').read_bytes()[:len(native)]!=native:raise ValueError('native acquired payload differs')
                loads.append({'receipt':str(origin.relative_to(ROOT)),'selector':e['selector'],'sub':e['sub'],'native_bytes':len(native),'native_sha256':sha(native)})
        if r['state_origin']:
            parent=Path(r['state_origin']);pr=read(parent)
            if r['state_sha256']!=pr['artifacts']['checkpoint.mss']:raise ValueError('state origin checksum link')
            origin=parent
        else:origin=None
    if not loads:raise ValueError('no actual native source load in normal chain')
    native=read(folder/'native_selector.json');calls=[r for r in native['selectors'] if r['root']==pool and r['caller_lr']==0x0804F773 and r['cycles']>0]
    if not calls:raise ValueError('no actual native selector result')
    payload=rom[record['rom_offset']:record['rom_offset']+record['compiled_bytes']];spans=script_spans(payload,255)
    candidates=[]
    for script in sorted({int(u['id'].split(':')[1]) for u in asset['units']}):
        start=pool+struct.unpack_from('<H',payload,2*script)[0]
        if start<=ptr<start+len(spans[script]):candidates.append(script)
    if len(candidates)!=1:raise ValueError(('ambiguous current selected script',candidates,hex(ptr)))
    actual_script=candidates[0];_,units,expected,streams,ends=model(rom,m,cfg,arc,actual_script,255,record=record,asset=asset)
    matched=[u for u in units if ends[u['id']]==ptr]
    if len(matched)!=1 or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('current page not exact selected literal native wait')
    unit=matched[0];ee={s:expected[s] for s in streams[unit['id']]};trace=read(folder/(cp+'_roll_pet.json'));draws={d['stream']:d for d in trace['draws'] if d['stream'] in ee}
    if set(draws)!=set(ee) or any(d['context']!=0x0200FA20 or d['glyph_index']!=ee[s]['index'] for s,d in draws.items()):raise ValueError('CPU glyph stream mismatch')
    origin_xy=tuple(ram[0xFA38:0xFA3A])
    if origin_xy!=(52,110):raise ValueError('unexpected native full-box origin')
    for d in draws.values():
        row,off=divmod(d['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*d['glyph_index'])[0]
        if not 0<=row<3 or off%4 or off//4+width>(168 if row==2 else 180):raise ValueError('native rendered extent')
    counts=Counter(g['index'] for g in ee.values());reads={r['index']:r['reads'] for r in trace['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU font reads')
    proof=pixels(folder,args.step,list(draws.values()),ee,rom,m,origin=origin_xy,cursor_screen_background=True)
    frozen_write(ROOT/args.out,{'passed':True,'rom_sha256':sha(rom),'scope':'Normal coldboot/controller/native field loading and cached NPC caller, no read aliases/state injections','archive':arc,'id':unit['id'],'translation':unit['translation'],'actual_render_script':actual_script,'native_calls':calls,'native_loads':loads,'checkpoint_chain':chain,'native_wait':ptr,'native_origin':origin_xy,'pixels':proof,'screenshot':{'path':str((folder/(cp+'.png')).relative_to(ROOT)),'sha256':sha((folder/(cp+'.png')).read_bytes())},'release_eligible':False,'all500_runtime_or_semantic_review':False,'timing_scope':'Mesen emulated cpu.cycleCount delta for observed selector calls only; no audio or hardware-wide timing claim','dependencies':{f'tools/{p}':sha((ROOT/'tools'/p).read_bytes()) for p in ['verify_native_npc_display_036_v1.py','capture_field_loader_036_v1.py','verify_pending500_005_displays.py','report_roll_pet.py']}})
    print('PASS native load/caller/clone/glyph/OBJ/pixels',unit['id'],unit['translation'])

if __name__=='__main__':main()
