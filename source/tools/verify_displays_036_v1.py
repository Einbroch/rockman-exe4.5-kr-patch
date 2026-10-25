"""Current036 selected pages/options, glyph/font/OBJ pixels and cancel return."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');manifest=read('analysis/pending_insertion_500_036_npc_inputs_v1/manifest.json');selected={k for r in manifest['archives'] for k in r['new_ids']};proofs=[];refs={};covered=set();returns=[]
    plans=[('a0','79CF04',30,[(3,[0]),(5,[1])],6),('a1','7AAF94',0,[(3,[0]),(5,[1]),(7,[2,3]),(8,[2,3]),(9,[4])],11),('a3','7B469C',0,[(3,[0]),(5,[1,2]),(6,[1,2]),(7,[3]),(8,[4])],9)]
    origin=ROOT/'poc/runtime/pending500-036-v1-complete/result.json';parent=read(origin)
    for case,arc,script,steps,closed in plans:
        record=next(r for r in m['keyitem_rom']['npc036']['archives'] if r['archive']==arc);entry=next(r for r in manifest['archives'] if r['archive']==arc);require_hash(ROOT/entry['asset']['path'],entry['asset']['sha256']);asset=read(entry['asset']['path']);pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,255,record=record,asset=asset)
        folder=ROOT/('poc/runtime/pending500-036-v1-display-'+case);r=read(folder/'result.json')
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or r['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('036 quarantined diagnostic applicability')
        if r['state_origin']!=str(origin) or r['state_sha256']!=parent['artifacts']['checkpoint.mss'] or (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('036 own normal parent / diagnostic quarantine')
        for p,h in r['artifacts'].items():require_hash(folder/p,h)
        refs[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        for step,ordinals in steps:
            keys=[units[i]['id'] for i in ordinals];ee={s:expected[s] for key in keys for s in streams[key]};cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C);trace=read(folder/(cp+'_roll_pet.json'));draws={d['stream']:d for d in trace['draws'] if d['stream'] in ee}
            if not set(keys)<=selected or root!=pool or tuple(ram[0xFA38:0xFA3A])!=(52,110) or ptr!=ends[keys[-1]]:raise ValueError('036 exact selected wait/root/origin')
            opcode=rom[ptr-0x08000000:ptr-0x08000000+6];options=len(ordinals)==2
            if not (opcode==bytes.fromhex('ec068001ffff') if options else opcode[:2]==bytes.fromhex('e600')):raise ValueError('036 exact native select/wait opcode')
            if set(draws)!=set(ee) or any(d['context']!=0x0200FA20 or d['glyph_index']!=ee[s]['index'] for s,d in draws.items()):raise ValueError('036 actual glyph CPU stream')
            for d in draws.values():
                row,off=divmod(d['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*d['glyph_index'])[0]
                if not 0<=row<3 or off%4 or off//4+width>(168 if row==2 else 180):raise ValueError('036 rendered extent')
            counts=Counter(g['index'] for g in ee.values());reads={x['index']:x['reads'] for x in trace['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('036 actual CPU font reads')
            proof=pixels(folder,step,list(draws.values()),ee,rom,m,origin=(52,110),cursor_screen_background=True)
            if options:
                a,b,k=struct.unpack_from('<3H',(folder/(cp+'_gbaSpriteRam.bin')).read_bytes());wanted=60 if (case=='a1' and step==7) or (case=='a3' and step==5) else 119
                if a&0x2300 or (b&511,a&255,k&1023,k>>12)!=(wanted,108,1020,14):raise ValueError('036 native horizontal cursor')
            else:
                # Background outside current glyph extents must be freshly clear.
                from PIL import Image
                im=Image.open(folder/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
                for d in draws.values():
                    row,off=divmod(d['offset'],10752);x=52+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*d['glyph_index'])[0];rects.append((x,y,x+w,y+12))
                if any(im.getpixel((x,y))!=bg for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)):raise ValueError('036 page clear residue')
            covered.update(keys);proofs.append(dict(case=case,step=step,ids=keys,pointer=ptr,options=options,**proof))
        ram=(folder/f'step_{closed:03}_gbaExtWorkRam.bin').read_bytes();root=struct.unpack_from('<I',ram,0xFA50)[0];old=next(x for x in m['archives'] if x['archive']=='65DA28') if False else None
        # All three independently return to the same ordinary Rockman PET root.
        returns.append(root)
        if root==pool or root<0x08000000 or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('036 cancel/end did not restore ordinary PET')
    if len(set(returns))!=1 or len(covered)!=12:raise ValueError('036 finite diagnostic coverage / shared return')
    image='analysis/pending500_036_v1/diagnostic_contact_v1.png'
    frozen_write(ROOT/'analysis/pending500_036_v1/display_runtime_v1.json',dict(passed=True,rom_sha256=sha(rom),scope='Quarantined PET read-alias diagnostics of actual036 clones; no native scene acquisition/036-selector claim',new_rendered_ids=sorted(covered),complete_page_or_option_displays=len(proofs),pages=proofs,receipts=refs,page_clearing_verified=True,horizontal_default_right_and_B_cancel_verified=True,ordinary_PET_return_root=returns[0],contact_sheet=dict(path=image,sha256=sha((ROOT/image).read_bytes())),visual_review_pending=True,release_eligible=False,limits=['Not natural A0/A1/A3 NPC loading/caller/selector or timing, battle/Yes branch, reward, save, all500 semantic approval.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_displays_036_v1.py','tools/capture_npc_displays_036_v1.py','tools/run_displays_036_v1.py','tools/verify_pending500_005_displays.py','tools/report_roll_pet.py']}))
    print('PASS036 12 new IDs /12 page-or-option displays, font/OBJ/pixels/page clear/cancel-return')

if __name__=='__main__':main()
