"""008 native program pages and ThunderMan options: actual font/OBJ pixels."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from cumulative_batch500_008 import OUT
from verify_pending500_005_displays import model
from report_roll_pet import pixels
from archive_scripts import script_spans
def main():
    rp=ROOT/'poc/output/exe45_ko_development_pending500_008_v1.gba';m=read(str(rp.with_suffix('.json').relative_to(ROOT)));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');pages=[];images=[];covered=set()
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    # ThunderMan24 has native targets25/26, not Rockman0 targets1/2.
    native_select=bytes.fromhex('ec0680191aff')
    if script_spans(source[0x776650:0x776650+6405],138)[24].count(native_select)!=1:raise ValueError('Source-pinned ThunderMan select contract')
    for case,archive,script,count in [('prog','71551C',11,62),('communication','776650',24,138)]:
        pool,units,expected,streams,ends=model(rom,m,cfg,archive,script,count,asset_folder=OUT)
        folder=ROOT/f'poc/runtime/pending500-008-v1-display-{case}';receipt=json.loads((folder/'result.json').read_text(encoding='utf8'));d=receipt['display_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is not False or d['root']!=pool or d['script']!=script or d['roots']!=1 or d['entries']!=1 or d['navi']!=0:raise ValueError('Diagnostic artifact/context')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        for ordinal,step in enumerate((2,4,6)):
            selected=units if case=='communication' else [units[ordinal]];keys=[u['id'] for u in selected];selected_streams=[s for key in keys for s in streams[key]]
            state=json.loads((folder/f'step_{step:03}_roll_pet.json').read_text(encoding='utf8'));ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('Native root/text origin')
            last={x['stream']:x for x in state['draws'] if x['stream'] in selected_streams}
            if set(last)!=set(selected_streams):raise ValueError('Actual glyph population')
            draws=[last[s] for s in selected_streams];reads={x['index']:x['reads'] for x in state['font_reads']};counts=Counter(x['glyph_index'] for x in draws)
            if any(draw['glyph_index']!=expected[draw['stream']]['index'] for draw in draws) or any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Actual font CPU reads')
            if ptr!=ends[keys[-1]]:raise ValueError('Native waiting pointer')
            if case=='prog':
                if rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Native keyWait')
            else:
                if rom[ptr-0x08000000:ptr-0x08000000+6]!=native_select:raise ValueError('Native ThunderMan select')
                o=(folder/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0)
                if a&0x2300 or k&1023!=1020 or (b&511,a&255)!=(44,136 if step==4 else 122):raise ValueError('Option cursor up/down/reentry')
            proof=pixels(folder,step,draws,expected,rom,m,origin=(52,110),cursor_screen_background=True)
            if case=='prog':
                im=Image.open(folder/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((233,110));rects=[]
                for draw in draws:
                    row,off=divmod(draw['offset'],10752);left=52+off//4;top=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+draw['glyph_index']*4)[0];rects.append((left,top,left+width,top+12))
                vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(point)!=bg for point in vacant):raise ValueError('Stale program page pixels')
                proof['vacant_pixels_cleared']=len(vacant)
            covered.update(keys);pages.append(dict(case=case,step=step,ids=keys,text=[u['translation'] for u in selected],current_pointer=ptr,**proof));images.append(Image.open(folder/f'step_{step:03}.png'))
    if len(covered)!=6:raise ValueError('Six new literal population')
    out=ROOT/'analysis/pending500_008_v1';montage=out/'changed_pages.png'
    if montage.exists():raise ValueError('Preserve screenshot evidence')
    sheet=Image.new('RGB',(720,320))
    for i,img in enumerate(images):sheet.paste(img,(i%3*240,i//3*160))
    sheet.save(montage)
    frozen_write(out/'display_runtime.json',dict(passed=True,rom_sha256=sha(rom),diagnostic_rendered_ids=sorted(covered),pages=pages,read_alias_diagnostic=True,natural_event_or_choice_result_or_save_verified=False,release_eligible=False))
    print('PASS six new literals: exact waits/select/cursor/font/OBJ pixels; no outcome/save claim')
if __name__=='__main__':main()
