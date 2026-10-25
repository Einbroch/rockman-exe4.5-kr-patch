"""Natural035 NPC conversation, four pages twice, no read aliases/injections."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels
from verify_tpi_index import lz77_decompress


def need(ok,msg):
    if not ok:raise ValueError(msg)


def main():
    rp=ROOT/'poc/output/pending500_035_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    first=ROOT/'analysis/pending500_035_v2/natural_first_display_v1.json';p=read(first)
    need(p['passed'] and p['rom_sha256']==sha(rom) and p['id']=='79D650:20:0' and p['native_loads'],'Normal first-page/source acquisition prerequisite')
    for link in p['checkpoint_chain']:require_hash(ROOT/link['path'],link['sha256'])
    f2=ROOT/'poc/runtime/pending500-035-fixed-orange-npc-v2';f3=ROOT/'poc/runtime/pending500-035-fixed-orange-npc-v3';r2=read(f2/'result.json');r3=read(f3/'result.json')
    need(r3['state_origin']==str(f2/'result.json') and r3['state_sha256']==r2['artifacts']['checkpoint.mss'],'Direct normal conversation state edge')
    manifest=read('analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json');entry=next(r for r in manifest['archives'] if r['archive']=='79D650');require_hash(ROOT/entry['asset']['path'],entry['asset']['sha256']);asset=read(entry['asset']['path']);record=next(r for r in m['keyitem_rom']['npc035']['archives'] if r['archive']=='79D650')
    pool,units,expected,streams,ends=model(rom,m,cfg,'79D650',20,255,record=record,asset=asset);native=lz77_decompress(source,0x79D650)[0]
    need([u['id'] for u in units]==[f'79D650:20:{i}' for i in range(4)],'Four actual script20 units')
    calls=[]
    for f,r in [(f2,r2),(f3,r3)]:
        need(r['complete'] and r['return_code']==0 and r['rom_sha256']==sha(rom) and r.get('normal_play_checkpoint_eligible',True) and not r.get('mode_alias') and not r['scope'].startswith('DIAGNOSTIC'),'Natural same-ROM receipt')
        for name,h in r['artifacts'].items():require_hash(f/name,h)
        entries=read(f/'npc_entries.json')['entries'];readers=read(f/'field_loader.json')['readers'];selectors=read(f/'native_selector.json')['selectors']
        need(len(entries)==len(readers)==len(selectors)==1,'Exactly one natural conversation open per segment')
        e=entries[0];rr=readers[0];s=selectors[0];regs=e['registers']
        need((regs['0'],regs['1'],regs['5'],regs['14'])==(20,0,0x0200AD68,0x0806EDF1),'Native actor script/mode/caller')
        need((rr['pc'],rr['r0'],rr['r1'],rr['lr'])==(0x0804F76E,0x02039800,20,0x0806EDF1),'Original cached reader ABI')
        need((s['script'],s['root'],s['caller_lr'])==(20,pool,0x0804F773) and s['cycles']>0 and e['frame']==rr['frame']==s['frame'],'Native call to corrected clone')
        calls.append(dict(receipt=str((f/'result.json').relative_to(ROOT)),**s))
    pages=[dict(id=p['id'],segment=f2.name,step=2,**p['pixels'])]
    for step,previous,ordinal in [(1,0,1),(2,1,2),(3,2,3),(5,4,0),(6,5,1),(7,6,2),(8,7,3)]:
        cp=f'step_{step:03}';ram=(f3/(cp+'_gbaExtWorkRam.bin')).read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C);key=units[ordinal]['id']
        need(root==pool and ptr==ends[key] and rom[ptr-0x08000000:ptr-0x08000000+2]==b'\xe6\x00','Current page exact native keyWait')
        need(ram[0x39800:0x39800+len(native)]==native and struct.unpack_from('<I',ram,0xAE04)[0]==0,'Native source/actor mode remains original')
        need(tuple(ram[0xFA38:0xFA3A])==(52,110),'Native text origin')
        state=read(f3/(cp+'_roll_pet.json'));old=read(f3/f'step_{previous:03}_roll_pet.json') if previous else dict(font_reads=[])
        lower=read(f3/f'step_{previous:03}.json')['frame'] if previous else 0;upper=read(f3/(cp+'.json'))['frame']
        draws=[d for d in state['draws'] if lower<d['frame']<=upper]
        need([d['stream'] for d in draws]==streams[key],'Fresh ordered glyph coverage, no stale draws')
        now={x['index']:x['reads'] for x in state['font_reads']};before={x['index']:x['reads'] for x in old['font_reads']};counts=Counter(d['glyph_index'] for d in draws)
        need(all(now.get(i,0)-before.get(i,0)>=24*n for i,n in counts.items()),'Fresh CPU glyph reads')
        rects=[];widths=[0,0,0]
        for d in draws:
            row,off=divmod(d['offset'],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+4*d['glyph_index'])[0]
            need(row<3 and off%4==0 and off//4+w<=(168 if row==2 else 180),'Normal NPC adopted display range')
            widths[row]=max(widths[row],off//4+w);rects.append((52+off//4,110+row*14,52+off//4+w,122+row*14))
        proof=pixels(f3,step,draws,expected,rom,m,origin=(52,110),cursor_screen_background=True)
        im=Image.open(f3/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        need(all(im.getpixel(pos)==bg for pos in vacant),'Native page clearing')
        pages.append(dict(id=key,segment=f3.name,step=step,line_widths=widths,cleared_pixels=len(vacant),**proof))
    for step in [4,9,10]:
        o=(f3/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
        active=[i for i in range(128) for a,b,k in [struct.unpack_from('<HHH',o,i*8)] if not a&0x2300 and k>>12==14]
        need(not active,'Text OBJs disabled after both closures')
    # The first left input faced the walking actor and was collision-blocked.
    # Keep that failed movement observation; prove control with an away input.
    f4=ROOT/'poc/runtime/pending500-035-fixed-orange-npc-v4';r4=read(f4/'result.json')
    need(r4['complete'] and r4['return_code']==0 and r4['rom_sha256']==sha(rom) and r4['state_sha256']==r3['artifacts']['checkpoint.mss'] and r4['state_origin']==str(f3/'result.json') and r4.get('normal_play_checkpoint_eligible',True),'Post-close normal movement origin')
    for name,h in r4['artifacts'].items():require_hash(f4/name,h)
    ram9=(f3/'step_009_gbaExtWorkRam.bin').read_bytes();ram10=(f4/'step_001_gbaExtWorkRam.bin').read_bytes()
    need(ram9[0xFB54:0xFB60]!=ram10[0xFB54:0xFB60],'Actual normal movement away from actor after closing')
    result=dict(passed=True,scope='Normal coldboot/acquisition/controller/native actor selection -> corrected035 clone -> CPU glyph/OBJ/screen and four-page close/reentry',rom_sha256=sha(rom),natural_actor_selection_verified=True,first_page_report=dict(path=str(first.relative_to(ROOT)),sha256=sha(first.read_bytes())),native_calls=calls,pages=pages,unique_ids=[u['id'] for u in units],actual_native_source_retained_bytes=len(native),alias_or_state_injection_used=False,close_reentry_post_close_movement=True,movement_receipt=dict(path=str((f4/'result.json').relative_to(ROOT)),sha256=sha((f4/'result.json').read_bytes())),movement_note='Left input collided with walking actor; subsequent up+right moved normally. No state edit.',release_eligible=False,all500_runtime_or_semantic_review=False,timing_scope='Observed selector emulated cycles70487/70488 only, not worst-case/hardware/audio/save',dependencies={name:sha((ROOT/'tools'/name).read_bytes()) for name in ['verify_natural_npc_035_v2.py','capture_field_loader_035_v7.py','verify_native_npc_display_035_v1.py','verify_pending500_005_displays.py','report_roll_pet.py']})
    frozen_write(ROOT/'analysis/pending500_035_v2/natural_cached_display_v2.json',result)
    print('PASS035 NATURAL NPC four units/eight pages, native call/clone/CPU glyph/OBJ/pixels/clear/close/reentry/movement')


if __name__=='__main__':main()
