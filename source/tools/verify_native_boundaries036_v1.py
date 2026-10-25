"""Byte-bound composition of native LZ and native caller/selector diagnostics.

This does NOT turn either qualified experiment into natural A1/A3 progression.
The prerequisite source-load attempts retained a failed whole-path status;
only their exact native decompression snapshots are credited to the load link.
"""
import struct
from collections import Counter
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();manifest=read('analysis/pending_insertion_500_036_npc_inputs_v1/manifest.json');parent=ROOT/'poc/runtime/pending500-036-sunday-natural-npc-v2';pr=read(parent/'result.json');loads=[];calls=[];pages=[];images=[];refs={};covered=set();a0=lz77_decompress(source,0x79CF04)[0]
    for case,arc,scene,steps,closed in [('a1','7AAF94',0xA1,[(2,[0]),(3,[1]),(5,[2,3]),(6,[2,3]),(7,[4])],8),('a3','7B469C',0xA3,[(2,[0]),(3,[1,2]),(4,[1,2]),(5,[3]),(6,[4])],7)]:
        payload=lz77_decompress(source,int(arc,16))[0];ld=ROOT/('poc/runtime/pending500-036-qualified-native-'+case+('-v1' if case=='a1' else '-load-v1'));lr=read(ld/'result.json');q=lr['qualified_scene']
        if lr['rom_sha256']!=sha(rom) or lr['return_code']!=0 or lr['normal_play_checkpoint_eligible'] is not False or lr['complete'] is not False or q!={'native_loads':1,'weekday_reads':1,'lookup_scene_reads':1,'lookup_sub_reads':1,'selector_scene_reads':0,'source':0x08000000+int(arc,16)}:raise ValueError('Qualified load-only evidence scope')
        for name,h in lr['artifacts'].items():require_hash(ld/name,h)
        ob=read(ld/'field_loader.json');first=next(e for e in ob['events'] if e['pc']==0x0804F724)
        if (first['r0'],first['r1'],first['scene'],first['sub'],first['selector'])!=(0x08000000+int(arc,16),0x02039800,0xA0,0,0) or (ld/'load_001_02039800.bin').read_bytes()[:len(payload)]!=payload:raise ValueError('Actual native LZ->RAM bytes')
        loads.append(dict(case=case,archive=arc,qualified_lookup=dict(scene=scene,sub=3,weekday=5),actual_game_scene=0xA0,native_bytes=len(payload),native_sha256=sha(payload),snapshot=str((ld/'load_001_02039800.bin').relative_to(ROOT)),whole_attempt_status='FAILED_SELECTOR_NOT_REACHED; only native load snapshot credited'))
        refs[str((ld/'result.json').relative_to(ROOT))]=sha((ld/'result.json').read_bytes())
        d=ROOT/('poc/runtime/pending500-036-native-boundary-'+case+'-v1');r=read(d/'result.json');b=r['resident_boundary']
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or r['state_origin']!=str(parent/'result.json') or r['state_sha256']!=pr['artifacts']['checkpoint.mss'] or b!={'resident_reads':len(payload),'scene_reads':1,'min_offset':0,'max_offset':len(payload)-1}:raise ValueError('Qualified native selector boundary identity')
        if (d/'checkpoint.mss').exists() or not (d/'diagnostic_checkpoint.mss').exists():raise ValueError('Diagnostic checkpoint quarantine')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        require_hash(ROOT/r['native_load_prerequisite']['path'],r['native_load_prerequisite']['sha256'])
        e=read(d/'npc_entries.json')['entries'];rr=read(d/'field_loader.json')['readers'];ss=read(d/'native_selector.json')['selectors']
        if len(e)!=1 or len(rr)!=1 or len(ss)!=1:raise ValueError('Exactly one actual original actor/cached call')
        g=e[0]['registers']
        if (g['0'],g['1'],g['5'],g['14'])!=(0,0,0x0200ABB8,0x0806EDF1) or (rr[0]['pc'],rr[0]['r0'],rr[0]['r1'],rr[0]['lr'])!=(0x0804F76E,0x02039800,0,0x0806EDF1):raise ValueError('Native actor/script/mode/caller not preserved')
        rec=next(x for x in m['keyitem_rom']['npc036']['archives'] if x['archive']==arc);assetref=next(x for x in manifest['archives'] if x['archive']==arc)['asset'];require_hash(ROOT/assetref['path'],assetref['sha256']);asset=read(assetref['path']);pool,units,expected,streams,ends=model(rom,m,cfg,arc,0,255,record=rec,asset=asset)
        if (ss[0]['script'],ss[0]['root'],ss[0]['caller_lr'])!=(0,pool,0x0804F773) or ss[0]['cycles']<=0:raise ValueError('Actual native036 selector result')
        final=(d/'final_gbaExtWorkRam.bin').read_bytes()
        if final[0x39800:0x39800+len(a0)]!=a0 or struct.unpack_from('<I',final,0xABB8+0x9C)[0]!=0:raise ValueError('Borrowed source RAM/actor mode mutated')
        refs[str((d/'result.json').relative_to(ROOT))]=sha((d/'result.json').read_bytes());calls.append(dict(case=case,**ss[0]))
        for step,ordinals in steps:
            keys=[units[i]['id'] for i in ordinals];ee={s:expected[s] for k in keys for s in streams[k]};cp=f'step_{step:03}';ram=(d/(cp+'_gbaExtWorkRam.bin')).read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C);t=read(d/(cp+'_roll_pet.json'));draws={x['stream']:x for x in t['draws'] if x['stream'] in ee};options=len(ordinals)==2
            if root!=pool or ptr!=ends[keys[-1]] or tuple(ram[0xFA38:0xFA3A])!=(52,110) or set(draws)!=set(ee) or any(x['context']!=0x0200FA20 or x['glyph_index']!=ee[s]['index'] for s,x in draws.items()):raise ValueError('Qualified native glyph/page/root/origin')
            op=rom[ptr-0x08000000:ptr-0x08000000+6]
            if not(op==bytes.fromhex('ec068001ffff') if options else op[:2]==bytes.fromhex('e600')):raise ValueError('Native wait/choice boundary')
            counts=Counter(x['index'] for x in ee.values());reads={x['index']:x['reads'] for x in t['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Actual normal font CPU reads')
            for x in draws.values():
                row,off=divmod(x['offset'],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*x['glyph_index'])[0]
                if not 0<=row<3 or off%4 or off//4+w>(168 if row==2 else 180):raise ValueError('Qualified native row extent')
            proof=pixels(d,step,list(draws.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True)
            im=Image.open(d/(cp+'.png')).convert('RGB')
            if options:
                a,c,k=struct.unpack_from('<3H',(d/(cp+'_gbaSpriteRam.bin')).read_bytes());left=step==(5 if case=='a1' else 3)
                if a&0x2300 or (c&511,a&255,k&1023,k>>12)!=((60 if left else 119),108,1020,14):raise ValueError('Qualified native horizontal choice cursor')
            else:
                bg=im.getpixel((233,110));rects=[]
                for x in draws.values():
                    row,off=divmod(x['offset'],10752);xx=52+off//4;yy=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*x['glyph_index'])[0];rects.append((xx,yy,xx+w,yy+12))
                if any(im.getpixel((x,y))!=bg for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<dd for a,b,c,dd in rects)):raise ValueError('Qualified native page clearing')
            pages.append(dict(case=case,step=step,ids=keys,**proof));covered.update(keys);images.append((case,step,im))
        for step in [closed,closed+1]:
            o=(d/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
            if any(not a&0x2300 and k>>12==14 for i in range(128) for a,c,k in [struct.unpack_from('<3H',o,i*8)]):raise ValueError('Native close text OBJ removal')
            images.append((case,step,Image.open(d/f'step_{step:03}.png').convert('RGB')))
        before=(d/f'step_{closed:03}_gbaExtWorkRam.bin').read_bytes();after=(d/f'step_{closed+1:03}_gbaExtWorkRam.bin').read_bytes()
        if before[0xFB54:0xFB60]==after[0xFB54:0xFB60]:raise ValueError('Post-close native movement not observed')
    if len(covered)!=10 or len(pages)!=10:raise ValueError('Finite two-scene diagnostic coverage')
    out=ROOT/'analysis/pending500_036_v1/native_boundary_contact_v1.png'
    if out.exists():raise ValueError('Preserve contact gallery')
    sheet=Image.new('RGB',(960,180*((len(images)+3)//4)),'#20232a');draw=ImageDraw.Draw(sheet)
    for i,(case,step,im) in enumerate(images):x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+3,y+3),case+' '+str(step),fill='white')
    sheet.save(out)
    frozen_write(ROOT/'analysis/pending500_036_v1/native_boundaries_v1.json',dict(passed=True,rom_sha256=sha(rom),scope='Composed byte-identical native LZ load and qualified normal actor/caller/036selector/font/video boundaries, not natural A1/A3 acquisition',native_loads=loads,native_calls=calls,pages=pages,rendered_unique_ids=sorted(covered),receipts=refs,natural_A1_A3_acquisition_verified=False,unchanged_A0_RAM_actor_mode_and_native_caller_verified=True,close_B_cancel_and_post_close_movement_verified=True,contact_sheet=dict(path=str(out.relative_to(ROOT)),sha256=sha(out.read_bytes()),screens=len(images)),visual_review_pending=True,release_eligible=False,limits=['The first native-load attempt reached mandatory first-visit training instead of the target NPC and remains a failed whole-path attempt.','Load boundary and selector boundary were exercised in separate qualified runs joined by the full1914/1695 byte native LZ result; not a single natural A1/A3 run.','Actual A1/A3 actor placement, progression, calendar/branch acquisition, battle-Yes/rewards/saves and full500 semantic review remain unverified.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_native_boundaries036_v1.py','tools/capture_native_scene036_v1.py','tools/capture_native_boundary036_v1.py','tools/run_native_boundary036_v1.py','tools/capture_field_loader_036_v1.py','tools/verify_pending500_005_displays.py','tools/report_roll_pet.py']}))
    print('PASS036 two qualified native LZ/caller/selector boundaries,10IDs/10pages, B cancel/close/movement; NOT natural A1/A3 acquisition')

if __name__=='__main__':main()
