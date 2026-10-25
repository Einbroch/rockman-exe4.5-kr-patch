"""Actual035 new-literal CPU/font/OBJ/pixel/wait/page diagnostic evidence."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

OUT='analysis/pending500_035_v1/npc_displays.json'

def main():
    rp=ROOT/'poc/output/pending500_035_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    manifest=read('analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json');selected={k for r in manifest['archives'] for k in r['new_ids']};pages=[];receipts={};images=[];covered=set()
    for case,arc,script,n in [('plaza','7A32A8',21,4),('portraits','79D650',61,4),('weekend','7A4DD4',30,2)]:
        rec=next(r for r in manifest['archives'] if r['archive']==arc);record=next(r for r in m['keyitem_rom']['npc035']['archives'] if r['archive']==arc);asset=read(rec['asset']['path'])
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,255,record=record,asset=asset);folder=ROOT/('poc/runtime/pending500-035-v1-npc-display-'+case);receipt=read(folder/'result.json');d=receipt['display_diagnostic']
        if len(units)!=n or not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] is not False or d!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('035 exact diagnostic identity')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('035 diagnostic quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        for i,u in enumerate(units):
            step=3+2*i;cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if u['id'] not in selected or root!=pool or tuple(ram[0xFA38:0xFA3A])!=(52,110) or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('035 native selected text/origin/wait')
            ee={s:expected[s] for s in streams[u['id']]};draws={d['stream']:d for d in trace['draws'] if d['stream'] in ee}
            if set(draws)!=set(ee) or any(d['context']!=0x0200FA20 or d['glyph_index']!=ee[s]['index'] for s,d in draws.items()):raise ValueError('035 actual glyph stream')
            for d in draws.values():
                row,off=divmod(d['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*d['glyph_index'])[0]
                if not 0<=row<3 or off%4 or off//4+width>(168 if row==2 else 180):raise ValueError('035 actual row extent')
            counts=Counter(g['index'] for g in ee.values());reads={r['index']:r['reads'] for r in trace['font_reads']}
            if any(reads.get(index,0)<24*num for index,num in counts.items()):raise ValueError('035 glyph CPU reads')
            proof=pixels(folder,step,list(draws.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True)
            covered.add(u['id']);pages.append(dict(case=case,step=step,id=u['id'],native_wait=ptr,**proof));images.append((case,step,Image.open(folder/(cp+'.png')).convert('RGB')))
    sheet=Image.new('RGB',(960,180*((len(images)+3)//4)),(35,35,35))
    from PIL import ImageDraw
    label=ImageDraw.Draw(sheet)
    for i,(case,step,im) in enumerate(images):x=(i%4)*240;y=(i//4)*180;sheet.paste(im,(x,y+20));label.text((x+3,y+3),case+' '+str(step),fill='white')
    path=ROOT/'analysis/pending500_035_v1/npc_displays_contact.png';sheet.save(path)
    deps=['tools/verify_npc_displays_035.py','tools/capture_npc_displays_035_v2.py','tools/verify_pending500_005_displays.py','tools/report_roll_pet.py','analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,rom_sha256=sha(rom),new_rendered_ids=sorted(covered),pages=pages,receipts=receipts,contact_sheet=dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes())),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},runtime_tested=True,visual_review_pending=True,release_eligible=False,
        limits='Actual035 clone glyph/CPU/OBJ/pixels and ten source wait/page transitions under quarantined PET root/script read aliases. Does NOT prove native A0 loading, NPC selector/caller/weekday or natural acquisition, complete500 semantics, saves or Hangul input.'))
    print('035 actual new NPC display',len(pages),'pages',len(covered),'IDs PASS; direct visual review pending')

if __name__=='__main__':main()
