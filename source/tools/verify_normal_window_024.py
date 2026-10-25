"""023 shared normal-window sample; explicitly NOT024's unbuilt500 display."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    rp=ROOT/'poc/output/pending500_023_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    folder=ROOT/'poc/runtime/pending500-024-baseline023-normal-order-v2';receipt=read(folder/'result.json')
    asset_ref=next(r for r in m['translation_assets'] if r.get('archive')=='71551C');require_hash(ROOT/asset_ref['path'],asset_ref['sha256']);asset=read(asset_ref['path'])
    pool,units,expected,streams,ends=model(rom,m,cfg,'71551C',17,62,asset=asset)
    if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] is not False or receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=17):raise ValueError('Diagnostic identity')
    for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
    if (folder/'checkpoint.mss').exists() or len(units)!=4:raise ValueError('Diagnostic quarantine/pages')
    rows=[];images=[]
    for step,u in zip((3,5,7,9),units):
        name=f'step_{step:03}';ram=(folder/(name+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(name+'_roll_pet.json'));e={s:expected[s] for s in streams[u['id']]};offsets={};row=width=0;it=iter(streams[u['id']]);widths=[]
        for ch in u['translation']:
            if ch=='\n':widths.append(width);row+=1;width=0;continue
            s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
            if row>2 or width>(168 if row==2 else 180):raise ValueError('Normal row capacity')
        widths.append(width);draws={d['stream']:d for d in trace['draws'] if d['stream'] in e}
        if set(draws)!=set(e) or any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=e[s]['index'] for s,d in draws.items()):raise ValueError('Actual normal renderer offsets')
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600') or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('Native wait/origin')
        reads={r['index']:r['reads'] for r in trace['font_reads']};counts=Counter(g['index'] for g in e.values())
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Actual font CPU consumption')
        proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=(52,110));im=Image.open(folder/(name+'.png')).convert('RGB');occupied=set()
        for s,g in e.items():
            rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0];occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(52+xx//4,52+xx//4+w))
        vacant={(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138)}-occupied
        if any(im.getpixel(p)!=im.getpixel((233,110)) for p in vacant):raise ValueError('Previous-page residue')
        rows.append(dict(id=u['id'],step=step,row_widths=widths,wait_pointer=ptr,vacant_pixels_cleared=len(vacant),**proof));images.append(im)
    ram=(folder/'step_011_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
    end=rows[-1]['wait_pointer']+2;trace=read(folder/'step_011_normal_end.json')
    if rom[end-0x08000000:end-0x08000000+2]!=b'\xE5\xE5' or not trace['entries'] or len(trace['exits'])!=1 or any(e['stream']!=end for e in trace['entries']) or trace['exits'][0]['stream']!=end or trace['exits'][0]['active']!=0:raise ValueError('Native first end/inactive transition')
    own=next(r for r in m['archives'] if r['archive']=='65A608');own_pool=0x08000000+own['rom_offset']
    if ram[0xFA20]!=1 or root!=own_pool or rom[ptr-0x08000000:ptr-0x08000000+4]!=bytes.fromhex('edff0000'):raise ValueError('Original own PET reopens after end')
    images.append(Image.open(folder/'step_011.png').convert('RGB'));out=ROOT/'analysis/pending_insertion_500_024_shared_runtime_v1';out.mkdir(parents=True,exist_ok=False);sheet=Image.new('RGB',(720,320))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    sheet.save(out/'normal_order_pages.png')
    frozen_write(out/'verification.json',dict(schema=1,passed=True,baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),source_asset=asset_ref,receipt=dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())),pages=rows,native_origin=[52,110],native_context_inactive_after_first_end=True,native_end_trace=trace,source_duplicate_end_not_advanced=True,original_own_pet_reopened=dict(archive='65A608',root=root,hold_pointer=ptr),contact_sheet=dict(path=str((out/'normal_order_pages.png').relative_to(ROOT)),sha256=sha((out/'normal_order_pages.png').read_bytes())),new500_rendered=False,read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,limits='Actual023 msgOpen-before-portrait shared consumer sample only,1/3/1/2rows/clear/exit followed by original PET reopening. Not an idle empty window or absence of legitimate PET text OBJ. Source pointer/table read aliases do not prove minigame route, native NPC scene, conditionals, guard effects or the unbuilt024500 ROM. No ROM/RAM/progression/save writes or active normal checkpoint promotion.'))
    print('PASS actual023 normal-window shared path:4 pages/font/OBJ/pixels/waits/clears/first-of-two-E5 exit;NOT024500 runtime')


if __name__=='__main__':main()
