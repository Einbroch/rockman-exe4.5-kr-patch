"""038 board representative link proof, qualified tile read only, NOT natural."""
import struct
from collections import Counter
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_038_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    manifest=read('analysis/pending_insertion_500_038_native_inputs_v1/manifest.json');arc='799314';payload=lz77_decompress(source,int(arc,16))[0]
    rec=next(x for x in m['keyitem_rom']['npc038']['archives'] if x['archive']==arc)
    item=next(x for x in manifest['archives'] if x['archive']==arc);assetref=item['asset'];require_hash(ROOT/assetref['path'],assetref['sha256']);asset=read(assetref['path'])
    pool,units,expected,streams,ends=model(rom,m,cfg,arc,1,20,record=rec,asset=asset)
    if len(units)!=1 or units[0]['id']!='799314:1:0':raise ValueError('Finite board literal denominator')
    for a,b in [(0x2DC68,0x2DCC4),(0x6A4DC,0x6A510)]:
        if source[a:b]!=rom[a:b]:raise ValueError('Original event/caller code preservation')
    word=lambda at:struct.unpack_from('<I',source,at)[0]-0x08000000
    table=word(word(0x2D568+0x20*4))
    if table!=0x56944 or source[table+1]!=1:raise ValueError('Original F1 table target')
    d=ROOT/'poc/runtime/pending500-038-board-qualified-v1';r=read(d/'result.json');refs={}
    if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or len(r['loaded_rom_guards'])!=4:raise ValueError('Own artifact/diagnostic guard contract')
    if (d/'checkpoint.mss').exists() or not (d/'diagnostic_checkpoint.mss').exists():raise ValueError('Diagnostic state quarantine')
    for name,h in r['artifacts'].items():require_hash(d/name,h)
    refs[str((d/'result.json').relative_to(ROOT))]=sha((d/'result.json').read_bytes())
    # Trace the exact normal-state ancestry back to an actual source LZ run.
    current=r
    while current.get('state_origin'):
        p=ROOT/current['state_origin'];parent=read(p)
        if not parent['complete'] or parent['rom_sha256']!=sha(rom) or parent.get('normal_play_checkpoint_eligible') is False or current['state_sha256']!=parent['artifacts']['checkpoint.mss']:raise ValueError('Normal state ancestry')
        require_hash(p.parent/'checkpoint.mss',current['state_sha256']);refs[str(p.relative_to(ROOT))]=sha(p.read_bytes())
        if p.parent.name=='pending500-038-normal-v1-09':
            for name,h in parent['artifacts'].items():require_hash(p.parent/name,h)
            fl=read(p.parent/'field_loader.json')
            if not any(x['pc']==0x0804F730 and x['r0']==0x08799314 and x['r1']==0x0203C800 for x in fl['events']):raise ValueError('Actual source pointer/LZ entry')
            dumps=list(p.parent.glob('load_*_0203C800.bin'))
            if not dumps or any(p.read_bytes()[:len(payload)]!=payload for p in dumps):raise ValueError('Original LZ full native boundary')
            break
        current=parent
    else:raise ValueError('Source load ancestry not reached')
    tile=read(d/'board_tile_alias.json')['reads'];flags=[]
    if tile!=[dict(frame=f,address=0x02004ADE,original=0,returned=0xF1) for f in (0,300)]:raise ValueError('Exact diagnostic intervention scope')
    events=read(d/'board_dispatch.json')['events'];dispatch=[x for x in events if x['pc']==0x0802DCAA]
    if len(dispatch)!=2 or any((x['frame'],x['r1'],x['r4'],x['scene'])!=(f,1,1,0x02004AD0) for x,f in zip(dispatch,(0,300))):raise ValueError('Original table dispatch')
    b=read(d/'board_entries.json');ss=read(d/'native_selector.json')['selectors'];readers=read(d/'field_loader.json')['readers']
    if len(b['entries'])!=len(b['BL_arguments']) or len(ss)!=2 or len(readers)!=2 or len(b['entries'])!=2:raise ValueError('Exactly two board calls')
    for f,e,a,s,rr in zip((0,300),b['entries'],b['BL_arguments'],ss,readers):
        if e['frame']!=f or e['source_bytes']!=[0,0,0,0,1]+[0]*11 or a['object']!=e['object'] or (a['frame'],a['root'],a['script'])!=(f,0x0203C800,1):raise ValueError('Original event provider/BL args')
        if (rr['pc'],rr['r0'],rr['r1'])!=(0x0806A502,0x0203C800,1) or (s['frame'],s['script'],s['root'],s['caller_lr'],s['native_root'])!=(f,1,pool,0x0806A507,0x0203C800) or s['cycles']<=0:raise ValueError('Real board LR/selector/root')
    pages=[];images=[];key=units[0]['id'];ee={s:expected[s] for s in streams[key]}
    for step in range(1,6):
        cp=f'step_{step:03}';ram=(d/(cp+'_gbaExtWorkRam.bin')).read_bytes();o=(d/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(d/(cp+'.png')).convert('RGB');images.append(im)
        if ram[0x3C800:0x3C800+len(payload)]!=payload or ram[0x4ad4:0x4ad6]!=bytes([0xA0,0]) or ram[0x4ade]!=0 or ram[0x4fa4]!=0x30:raise ValueError('Native board/scene/flag RAM mutated')
        if step not in (1,3):
            if any(not a&0x2300 and k>>12==14 for i in range(128) for a,c,k in [struct.unpack_from('<3H',o,i*8)]):raise ValueError('Text OBJ remained after close')
            continue
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C);t=read(d/(cp+'_roll_pet.json'));draws={x['stream']:x for x in t['draws'] if x['stream'] in ee}
        if ptr!=ends[key] or root!=pool or tuple(ram[0xFA38:0xFA3A])!=(52,110) or set(draws)!=set(ee) or any(x['context']!=0x0200FA20 or x['glyph_index']!=ee[s]['index'] for s,x in draws.items()):raise ValueError('Board current context/stream/glyph identity')
        if rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Board original wait boundary')
        counts=Counter(x['index'] for x in ee.values());reads={x['index']:x['reads'] for x in t['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Board font CPU supply')
        rects=[]
        for x in draws.values():
            row,off=divmod(x['offset'],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*x['glyph_index'])[0]
            if not 0<=row<3 or off%4 or off//4+w>(168 if row==2 else 180):raise ValueError('Board actual extent')
            xx,yy=52+off//4,110+row*14;rects.append((xx,yy,xx+w,yy+12))
        bg=im.getpixel((233,110))
        if any(im.getpixel((x,y))!=bg for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<dd for a,b,c,dd in rects)):raise ValueError('Board vacant page pixels')
        proof=pixels(d,step,list(draws.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True)
        pages.append(dict(step=step,id=key,**proof))
    before=(d/'step_004_gbaExtWorkRam.bin').read_bytes();after=(d/'step_005_gbaExtWorkRam.bin').read_bytes()
    if before[0xFB54:0xFB60]==after[0xFB54:0xFB60]:raise ValueError('Movement after board close')
    out=ROOT/'analysis/pending500_038_v2';sheetpath=out/'board_qualified_contact_v1.png'
    if sheetpath.exists():raise ValueError('Preserve prior sheet')
    sheet=Image.new('RGB',(720,360),'#20232a');draw=ImageDraw.Draw(sheet)
    for i,im in enumerate(images):x,y=i%3*240,i//3*180;sheet.paste(im,(x,y+20));draw.text((x+3,y+3),'board '+str(i+1),fill='white')
    sheet.save(sheetpath)
    deps=['tools/verify_board_qualified038_v1.py','tools/capture_board_qualified038_v1.py','tools/capture_board_event038_v1.py','tools/capture_board038_v1.py','tools/run_board_qualified038_v1.py','tools/capture_field_loader_038_v1.py','tools/report_roll_pet.py','tools/verify_pending500_005_displays.py','analysis/pending_insertion_500_038_native_inputs_v1/manifest.json']
    frozen_write(out/'board_qualified_v1.json',dict(passed=True,rom_sha256=sha(rom),scope=__doc__,archive=arc,native_bytes=len(payload),native_sha256=sha(payload),rendered_ids=[key],original_dispatch=dispatch,original_board_entries=b,actual_selector_calls=ss,tile_read_aliases=tile,disabled_flag_read_aliases=flags,pages=pages,full_native_RAM_unchanged=True,close_reentry_close_movement_verified=True,natural_rock_acquisition_verified=False,release_eligible=False,agent_visual_review_pending=True,contact_sheet=dict(path=str(sheetpath.relative_to(ROOT)),sha256=sha(sheetpath.read_bytes()),screens=5),receipts=refs,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['One tile-read alias at original dispatch instruction, repeated twice; no flag alias or natural rock acquisition proof.','Representative board consumer link only, not all224 board literals/66archives or all500 actual screens.','Mesen muted; no hardware/worst-case/audio certification; Hangul commit/save/redisplay and human approval open.']))
    print('PASS038 qualified board full native source / real6A502-LR6A507 / selector / Korean glyph-font-OBJ-pixels / close-reentry-movement')

if __name__=='__main__':main()
