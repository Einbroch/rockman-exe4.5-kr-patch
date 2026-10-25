"""Exact new literals: normal font CPU reads -> OBJ residency -> screenshots."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import OUT,read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels
STEM='exe45_ko_development_pending500_007_v1'
PREFIX='pending500-007-v1'
ASSET_FOLDER=OUT
OUTPUT_DIR='analysis/pending500_007_v1'
CASES=[('prog','71551C',17,62,(2,4,6,8),(52,110)),('family','6CDCD0',7,97,(2,4,6),(92,110))]
REQUIRE_CLEARING=False

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(str(rp.with_suffix('.json').relative_to(ROOT)));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    pages=[];images=[]
    for case,archive,script,count,steps,origin in CASES:
        pool,units,expected,streams,ends=model(rom,m,cfg,archive,script,count,asset_folder=ASSET_FOLDER)
        folder=ROOT/f'poc/runtime/{PREFIX}-display-{case}';receipt=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is not False:raise ValueError('Diagnostic identity')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        full_box='display_diagnostic' in receipt
        d=receipt['display_diagnostic'] if full_box else receipt['alert_diagnostic']
        if d['root']!=pool or d['script']!=script:raise ValueError('Native diagnostic consumer')
        if full_box and (d['roots']!=1 or d['entries']!=1 or d['navi']!=0):raise ValueError('Rockman origin')
        if not full_box and (d['root_aliases']!=1 or d['entry_aliases']!=1 or d['native_navi']!=8):raise ValueError('NumberMan origin')
        for ordinal,step in enumerate(steps):
            unit=units[ordinal];key=unit['id'];selected_streams=streams[key]
            state=json.loads((folder/f'step_{step:03}_roll_pet.json').read_text(encoding='utf8'));ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool:raise ValueError('Actual current root')
            last={x['stream']:x for x in state['draws'] if x['stream'] in selected_streams}
            if set(last)!=set(selected_streams):raise ValueError('Actual glyph population '+key)
            draws=[last[s] for s in selected_streams];reads={x['index']:x['reads'] for x in state['font_reads']};counts=Counter(x['glyph_index'] for x in draws)
            for draw in draws:
                target=expected[draw['stream']]
                if draw['glyph_index']!=target['index'] or reads[draw['glyph_index']]<counts[draw['glyph_index']]*24:raise ValueError('Actual font reads')
            if ptr!=ends[key] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Native keyWait boundary '+key)
            if tuple(ram[0xFA38:0xFA3A])!=origin:raise ValueError('Native text origin')
            pixel=pixels(folder,step,draws,expected,rom,m,origin=origin,cursor_screen_background=full_box)
            if REQUIRE_CLEARING:
                im=Image.open(folder/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((233,110));rects=[]
                for draw in draws:
                    row,off=divmod(draw['offset'],10752);left=origin[0]+off//4;top=origin[1]+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+draw['glyph_index']*4)[0];rects.append((left,top,left+width,top+12))
                vacant=[(x,y) for y in range(110,150) for x in range(origin[0],234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(point)!=bg for point in vacant):raise ValueError('Stale page pixels')
                pixel['vacant_pixels_cleared']=len(vacant)
            pages.append(dict(case=case,step=step,id=key,text=unit['translation'],normal_glyphs=len(draws),pixels=pixel))
            images.append(Image.open(folder/f'step_{step:03}.png').convert('RGB'))
    out=ROOT/OUTPUT_DIR
    montage=out/'changed_pages.png'
    if montage.exists():raise ValueError('Preserve screenshot evidence')
    sheet=Image.new('RGB',(240*4,160*max(2,(len(images)+3)//4)))
    for i,img in enumerate(images):sheet.paste(img,(i%4*240,i//4*160))
    sheet.save(montage)
    frozen_write(out/'display_runtime.json',dict(passed=True,rom_sha256=sha(rom),pages=pages,read_alias_diagnostic=True,natural_event_or_save_verified=False,release_eligible=False))
    print('PASS newly merged pages: CPU/font/OBJ/pixels; natural routes and choices not established')
if __name__=='__main__':main()
