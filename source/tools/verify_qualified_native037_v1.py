"""Qualified037 native LZ/caller/selector/font/OBJ/pixel composition evidence.

All three target scenes remain NON-natural; separate runs join only through
full native payload byte identity. Human review and board gameplay are open.
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
    rp=ROOT/'poc/output/pending500_037_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();manifest=read('analysis/pending_insertion_500_037_native_inputs_v2/manifest.json');parent=ROOT/'poc/runtime/pending500-037-normal-v1-16';pr=read(parent/'result.json');loads=[];calls=[];pages=[];images=[];refs={};covered=set();a0=lz77_decompress(source,0x79CF04)[0]
    specs=[('a1','7A7FC4',0xA1,[(2,[0]),(3,[1]),(4,[2,3]),(5,[2,3]),(6,[4])],7),('a2','7ADD74',0xA2,[(2,[0]),(3,[1]),(4,[2]),(5,[3,4]),(6,[3,4]),(7,[5])],8),('a3','7B39D0',0xA3,[(2,[0]),(3,[1]),(4,[2,3]),(5,[2,3]),(6,[4])],7)]
    for case,arc,scene,steps,closed in specs:
        payload=lz77_decompress(source,int(arc,16))[0];ld=ROOT/('poc/runtime/pending500-037-qualified-load-'+case+'-v1');lr=read(ld/'result.json')
        if not lr['complete'] or lr['rom_sha256']!=sha(rom) or lr['normal_play_checkpoint_eligible'] is not False or lr['selector_display_verified'] is not False or lr['target_archive']!=arc:raise ValueError('037 qualified load scope')
        for name,h in lr['artifacts'].items():require_hash(ld/name,h)
        if (ld/'qualified_native_001.bin').read_bytes()!=payload:raise ValueError('037 actual native LZ bytes')
        loads.append(dict(case=case,archive=arc,native_bytes=len(payload),native_sha256=sha(payload),lookup_alias=lr['lookup_alias'],scope='Exact037 qualified original source lookup/LZ/RAM only'))
        refs[str((ld/'result.json').relative_to(ROOT))]=sha((ld/'result.json').read_bytes())
        d=ROOT/('poc/runtime/pending500-037-qualified-boundary-'+case+'-v1');r=read(d/'result.json');b=r['resident_boundary']
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or r['state_origin']!=str(parent/'result.json') or r['state_sha256']!=pr['artifacts']['checkpoint.mss'] or b['scene_reads']!=1 or b['resident_reads']<len(payload) or (b['min_offset'],b['max_offset'])!=(0,len(payload)-1):raise ValueError('037 qualified resident identity boundary')
        if (d/'checkpoint.mss').exists() or not (d/'diagnostic_checkpoint.mss').exists():raise ValueError('037 diagnostic checkpoint quarantine')
        for name,h in r['artifacts'].items():require_hash(d/name,h)
        require_hash(ROOT/r['native_load_prerequisite']['path'],r['native_load_prerequisite']['sha256'])
        entries=read(d/'npc_entries.json')['entries'];readers=read(d/'field_loader.json')['readers'];selectors=read(d/'native_selector.json')['selectors']
        if len(entries)!=1 or len(readers)!=1 or len(selectors)!=1:raise ValueError('037 exactly one original NPC actor/caller')
        g=entries[0]['registers'];rr=readers[0];ss=selectors[0]
        if (g['0'],g['1'],g['5'],g['14'])!=(0,0,0x0200ABB8,0x0806EDF1) or (rr['pc'],rr['r0'],rr['r1'],rr['lr'])!=(0x0804F76E,0x02039800,0,0x0806EDF1):raise ValueError('037 original actor/script/mode/BL preconditions')
        rec=next(x for x in m['keyitem_rom']['npc037']['archives'] if x['archive']==arc);assetref=next(x for x in manifest['archives'] if x['archive']==arc)['asset'];require_hash(ROOT/assetref['path'],assetref['sha256']);asset=read(assetref['path']);pool,units,expected,streams,ends=model(rom,m,cfg,arc,0,255,record=rec,asset=asset)
        if (ss['script'],ss['root'],ss['caller_lr'],ss['native_root'])!=(0,pool,0x0804F773,0x02039800) or ss['cycles']<=0:raise ValueError('037 actual selector result')
        final=(d/'final_gbaExtWorkRam.bin').read_bytes()
        if final[0x39800:0x39800+len(a0)]!=a0 or struct.unpack_from('<I',final,0xABB8+0x9C)[0]!=0:raise ValueError('037 borrowed native RAM/actor mode changed')
        refs[str((d/'result.json').relative_to(ROOT))]=sha((d/'result.json').read_bytes());calls.append(dict(case=case,**ss));cursor_positions=[]
        for step,ordinals in steps:
            keys=[units[i]['id'] for i in ordinals];ee={s:expected[s] for k in keys for s in streams[k]};cp=f'step_{step:03}';ram=(d/(cp+'_gbaExtWorkRam.bin')).read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C);t=read(d/(cp+'_roll_pet.json'));draws={x['stream']:x for x in t['draws'] if x['stream'] in ee};options=len(ordinals)==2
            if root!=pool or ptr!=ends[keys[-1]] or tuple(ram[0xFA38:0xFA3A])!=(52,110) or set(draws)!=set(ee) or any(x['context']!=0x0200FA20 or x['glyph_index']!=ee[s]['index'] for s,x in draws.items()):raise ValueError(('037 qualified glyph/page/root',case,step))
            op=rom[ptr-0x08000000:ptr-0x08000000+6]
            if not(op==bytes.fromhex('ec068001ffff') if options else op[:2]==bytes.fromhex('e600')):raise ValueError('037 wait/choice parser boundary')
            counts=Counter(x['index'] for x in ee.values());reads={x['index']:x['reads'] for x in t['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('037 font CPU reads')
            for x in draws.values():
                row,off=divmod(x['offset'],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*x['glyph_index'])[0]
                if not 0<=row<3 or off%4 or off//4+w>(168 if row==2 else 180):raise ValueError('037 actual glyph extent')
            proof=pixels(d,step,list(draws.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True);im=Image.open(d/(cp+'.png')).convert('RGB')
            if options:
                a,c,k=struct.unpack_from('<3H',(d/(cp+'_gbaSpriteRam.bin')).read_bytes())
                if a&0x2300 or (a&255,k&1023,k>>12)!=(108,1020,14) or not 52<=c&511<234:raise ValueError('037 choice cursor visible extent')
                cursor_positions.append(c&511)
            else:
                bg=im.getpixel((233,110));rects=[]
                for x in draws.values():
                    row,off=divmod(x['offset'],10752);xx=52+off//4;yy=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*x['glyph_index'])[0];rects.append((xx,yy,xx+w,yy+12))
                if any(im.getpixel((x,y))!=bg for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<dd for a,b,c,dd in rects)):raise ValueError('037 page text not cleared')
            pages.append(dict(case=case,step=step,ids=keys,**proof));covered.update(keys);images.append((case,step,im))
        if len(cursor_positions)!=2 or cursor_positions[0]>=cursor_positions[1]:raise ValueError('037 right input did not move choice cursor')
        for step in [closed,closed+1]:
            o=(d/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
            if any(not a&0x2300 and k>>12==14 for i in range(128) for a,c,k in [struct.unpack_from('<3H',o,i*8)]):raise ValueError('037 text OBJ not removed after close')
            images.append((case,step,Image.open(d/f'step_{step:03}.png').convert('RGB')))
        before=(d/f'step_{closed:03}_gbaExtWorkRam.bin').read_bytes();after=(d/f'step_{closed+1:03}_gbaExtWorkRam.bin').read_bytes()
        if before[0xFB54:0xFB60]==after[0xFB54:0xFB60]:raise ValueError('037 post-close movement missing')
    if len(covered)!=16 or len(pages)!=16:raise ValueError('037 finite diagnostic page denominator')
    out=ROOT/'analysis/pending500_037_v2/qualified_native_contact_v1.png'
    if out.exists():raise ValueError('Preserve prior contact sheet')
    sheet=Image.new('RGB',(960,180*((len(images)+3)//4)),'#20232a');draw=ImageDraw.Draw(sheet)
    for i,(case,step,im) in enumerate(images):x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+3,y+3),case+' '+str(step),fill='white')
    sheet.save(out)
    frozen_write(ROOT/'analysis/pending500_037_v2/qualified_native_v1.json',dict(passed=True,rom_sha256=sha(rom),scope=__doc__,native_loads=loads,native_calls=calls,pages=pages,rendered_unique_ids=sorted(covered),receipts=refs,natural_A1_A2_A3_acquisition_verified=False,original_actor_mode_source_RAM_and_BL_verified=True,close_B_cancel_and_post_close_movement_verified=True,contact_sheet=dict(path=str(out.relative_to(ROOT)),sha256=sha(out.read_bytes()),screens=len(images)),visual_review_pending=True,release_eligible=False,limits=['Separate qualified load and read-alias selector runs; no natural target actor/scene route proved.','Observed Mesen CPU cycles only, not worst-case/hardware/audio certification.','Board gameplay, all500 runtime coverage, Hangul commit/save/redisplay and human approval remain open.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_qualified_native037_v1.py','tools/capture_native_load037_v1.py','tools/capture_native_boundary037_v1.py','tools/capture_field_loader_037_v1.py','tools/report_roll_pet.py','tools/verify_pending500_005_displays.py']}))
    print('PASS037 three QUALIFIED native boundaries,16IDs/16page-or-choice displays; NOT natural acquisition')


if __name__=='__main__':main()
