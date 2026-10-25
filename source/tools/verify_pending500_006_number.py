"""Four NumberMan return/result literals: wait/font/OBJ pixels/page clearing."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_roll_pet import pixels
from verify_pending500_005_displays import model

def read(p):return json.loads(p.read_text(encoding='utf8'))

def main():
    rp=ROOT/'poc/output/exe45_ko_development_pending500_006_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read(ROOT/'project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    require_hash(ROOT/'poc/output/exe45_ko_development_pending500_006_v1_repro.gba',sha(rom));pages=[];images=[];covered=set()
    for case,archive,script,count in [('return','68787C',2,4),('draw','68C2CC',3,5)]:
        pool,units,expected,streams,ends=model(rom,m,cfg,archive,script,count,'analysis/pending_insertion_500_006_rom');folder=ROOT/f'poc/runtime/pending500-006-v1-number-{case}';receipt=read(folder/'result.json');d=receipt['alert_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is not False or d['root_aliases']!=d['entry_aliases']!=1 or d['native_navi']!=8 or receipt['display_archive']!=archive:raise ValueError('Diagnostic binding')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        for ordinal,step in enumerate((2,4)):
            key=units[ordinal]['id'];selected=streams[key];state=read(folder/f'step_{step:03}_roll_pet.json');ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or ptr!=ends[key] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Exact native root/keyWait')
            if tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('Source explicit text origin')
            last={x['stream']:x for x in state['draws'] if x['stream'] in selected}
            if set(last)!=set(selected):raise ValueError('Literal draw coverage')
            draws=[last[s] for s in selected];reads={x['index']:x['reads'] for x in state['font_reads']};counts=Counter(x['glyph_index'] for x in draws)
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Actual font CPU reads')
            proof=pixels(folder,step,draws,expected,rom,m);im=Image.open(folder/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((233,110));rects=[]
            for x in draws:
                row,off=divmod(x['offset'],10752);left=92+off//4;top=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+x['glyph_index']*4)[0];rects.append((left,top,left+width,top+12))
            vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
            if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('Stale page pixels')
            covered.add(key);images.append(im);pages.append(dict(id=key,case=case,step=step,current_pointer=ptr,exact_keywait=True,vacant_pixels_cleared=len(vacant),**proof))
    if len(covered)!=4:raise ValueError('Four selected literals')
    out=ROOT/'analysis/pending_insertion_500_006_rom';sheet=Image.new('RGB',(480,320))
    for i,im in enumerate(images):sheet.paste(im,(i%2*240,i//2*160))
    sheet.save(out/'number_pages_v1.png')
    result=dict(passed=True,rom_sha256=sha(rom),diagnostic_rendered_ids=sorted(covered),pages=pages,native_numberman_portrait_context_retained=True,contact_sheet_sha256=sha((out/'number_pages_v1.png').read_bytes()),
        normal_scene_selection_verified=False,release_eligible=False,limits=['Four newly inserted literals in NumberMan-native pointer/table read-alias display diagnostics; not natural jack-out/battle draw progression/reward/save.','Other496 new literals have static whole-script/pointer/font checks, not direct runtime scene review.'])
    (out/'number_runtime_v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS four NumberMan literals, native waits/font/OBJ pixels and clearing')

if __name__=='__main__':main()
