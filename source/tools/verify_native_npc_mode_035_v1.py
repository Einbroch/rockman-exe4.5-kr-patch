"""035v2 actual native caller/renderer proof with explicit actor-mode bypass.

This does NOT certify normal actor selection, all500 pages, saves or release.
"""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels
from field_npc_rom_product_035_v2 import verify_final
from verify_tpi_index import lz77_decompress


def check(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    rp=ROOT/'poc/output/pending500_035_v2.gba'
    rom=rp.read_bytes(); m=read(rp.with_suffix('.json')); cfg=read('project.json')
    require_hash(rp,m['output_sha256'])
    sp=ROOT/cfg['source_profile']['filename']; require_hash(sp,cfg['source_profile']['sha256'])
    source=sp.read_bytes(); verify_final(source,rom,m['keyitem_rom'])
    check(source[0x6EDE6:0x6EDF2]==rom[0x6EDE6:0x6EDF2]==bytes.fromhex('287f9c216958e0f7bafc25e0'),'Native NPC script/mode/call contract')
    folder=ROOT/'poc/runtime/pending500-035-fixed-native-mode-diag-v1'
    receipt=read(folder/'result.json')
    check(receipt['complete'] and receipt['return_code']==0 and receipt['rom_sha256']==sha(rom),'Complete same-ROM run')
    check(receipt['normal_play_checkpoint_eligible'] is False and not (folder/'checkpoint.mss').exists() and (folder/'diagnostic_checkpoint.mss').exists(),'Diagnostic state quarantine')
    for name,h in receipt['artifacts'].items(): require_hash(folder/name,h)
    require_hash(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe',receipt['emulator_sha256'])
    # Verify this input really comes from this ROM's own normal startup chain.
    parent=read(receipt['state_origin']); chain=[]; seen=set()
    require_hash(folder/'input.mss',receipt['state_sha256'])
    while True:
        check(parent['complete'] and parent['return_code']==0 and parent['rom_sha256']==sha(rom) and parent.get('normal_play_checkpoint_eligible',True),'Normal parent binding')
        key=parent['artifacts'].get('checkpoint.mss'); check(key and key not in seen,'Normal checkpoint identity/cycle'); seen.add(key)
        chain.append(key)
        if not parent.get('state_origin'): break
        require_hash(ROOT/parent['state_origin'].replace('\\','/').split('Rockman exe 4.5/')[-1],sha((ROOT/parent['state_origin'].replace('\\','/').split('Rockman exe 4.5/')[-1]).read_bytes()))
        previous=read(parent['state_origin'])
        check(previous['artifacts']['checkpoint.mss']==parent['state_sha256'],'Parent state edge')
        parent=previous
    check(chain[0]==receipt['state_sha256'],'Diagnostic input normal checkpoint')
    manifest=read('analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json')
    spec=next(x for x in manifest['archives'] if x['archive']=='79D650')
    require_hash(ROOT/spec['asset']['path'],spec['asset']['sha256'])
    ar=next(x for x in m['keyitem_rom']['npc035']['archives'] if x['archive']=='79D650')
    pool,units,expected,streams,ends=model(rom,m,cfg,'79D650',1,255,record=ar,asset=read(spec['asset']['path']))
    check([u['id'] for u in units]==['79D650:1:0','79D650:1:1'],'Declared two literals')
    native=lz77_decompress(source,0x79D650)[0]
    alias=read(folder/'mode_alias.json'); entries=read(folder/'npc_entries.json')['entries']
    readers=read(folder/'field_loader.json')['readers']; selectors=read(folder/'native_selector.json')['selectors']
    check(alias['aliases']==2 and alias['original_actor_mode_still']==1 and len(alias['events'])==len(entries)==len(readers)==len(selectors)==2,'Two isolated native invocations')
    for a,e,r,s in zip(alias['events'],entries,readers,selectors):
        check((a['pc'],a['address'],a['original'],a['returned'],a['actor'])==(0x0806EDEA,0x0200AB7C,1,0,0x0200AAE0),'Exact bypass boundary')
        regs=e['registers']
        check((regs['0'],regs['1'],regs['5'],regs['14'])==(0,0,0x0200AAE0,0x0806EDF1),'Actual source caller ABI')
        check((r['pc'],r['r0'],r['r1'],r['lr'])==(0x0804F76E,0x02039800,0,0x0806EDF1),'Cached source reader ABI')
        check((s['root'],s['script'],s['caller_lr'])==(pool,0,0x0804F773) and s['cycles']>0,'Corrected product selector result')
        check(a['frame']==e['frame']==r['frame']==s['frame'],'Connected same-frame invocation')
    pages=[]
    for step,lower,ordinal in [(4,0,0),(5,4,1),(7,6,0),(8,7,1)]:
        prefix=f'step_{step:03}'; ram=(folder/(prefix+'_gbaExtWorkRam.bin')).read_bytes()
        check(ram[0x39800:0x39800+len(native)]==native,'Actual native source retained')
        check(struct.unpack_from('<I',ram,0xAB7C)[0]==1,'Actor mode memory unchanged')
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C); key=units[ordinal]['id']
        check(root==pool and ptr==ends[key] and rom[ptr-0x08000000:ptr-0x08000000+2]==b'\xe6\x00','Exact native page wait')
        check(tuple(ram[0xFA38:0xFA3A])==(52,110),'Native origin')
        state=read(folder/(prefix+'_roll_pet.json'))
        previous=read(folder/f'step_{lower:03}_roll_pet.json') if lower else {'font_reads':[]}
        lower_frame=read(folder/f'step_{lower:03}.json')['frame'] if lower else 0
        upper_frame=read(folder/(prefix+'.json'))['frame']
        draws=[d for d in state['draws'] if lower_frame<d['frame']<=upper_frame]
        check([d['stream'] for d in draws]==streams[key],'Complete fresh ordered page, no stale coverage')
        counts=Counter(d['glyph_index'] for d in draws)
        old={x['index']:x['reads'] for x in previous['font_reads']}; now={x['index']:x['reads'] for x in state['font_reads']}
        check(all(now.get(i,0)-old.get(i,0)>=24*n for i,n in counts.items()),'Fresh CPU font reads')
        widths=[0,0,0]; rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752)
            w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0]
            check(row<3 and off//4+w<=180,'Adopted NPC box width')
            widths[row]=max(widths[row],off//4+w)
            rects.append((52+off//4,110+row*14,52+off//4+w,122+row*14))
        proof=pixels(folder,step,draws,expected,rom,m,origin=(52,110),cursor_screen_background=True)
        im=Image.open(folder/(prefix+'.png')).convert('RGB'); bg=im.getpixel((233,110))
        vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        check(all(im.getpixel(p)==bg for p in vacant),'Page clears preceding text')
        pages.append(dict(step=step,id=key,translation=units[ordinal]['translation'],line_widths=widths,page_clear_pixels=len(vacant),**proof))
    # Closed windows must have no enabled normal-text palette14 OBJs.
    for step in [6,9,10]:
        o=(folder/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
        active=[i for i in range(128) for a,b,k in [struct.unpack_from('<HHH',o,i*8)] if not a&0x2300 and k>>12==14]
        check(not active,'Dialogue text OBJ disabled after closing')
    def position(step):
        r=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        scene=struct.unpack_from('<I',r,0xF300)[0]-0x02000000
        player=struct.unpack_from('<I',r,scene+0x28)[0]-0x02000000
        return list(struct.unpack_from('<3i',r,player+0x24))
    check(position(9)!=position(10),'Field movement after second close')
    result=dict(passed=True,scope='Qualified native caller/renderer diagnostic; actor dialog-mode read1->0 at source6EDEA only',rom_sha256=sha(rom),normal_origin_segments=len(chain),runtime_receipt=dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())),native_source_preserved_bytes=len(native),aliases=alias,pages=pages,selector_emulated_cycles=[s['cycles'] for s in selectors],actual_cached_reader_calls=2,close_reentry_and_post_close_movement=True,natural_actor_selection_verified=False,release_eligible=False,limits=['Two literals in one archive, not all500 or all9 archives.','Actor-specific mode selection bypassed by read alias; not natural NPC acquisition.','Emulated selector cycles only, no worst-case timing/hardware/audio/save certification.'])
    result['tools']={name:sha((ROOT/'tools'/name).read_bytes()) for name in ['verify_native_npc_mode_035_v1.py','capture_native_npc_mode_035_v1.py','verify_pending500_005_displays.py','report_roll_pet.py']}
    frozen_write(ROOT/'analysis/pending500_035_v2/native_mode_display_v1.json',result)
    print('PASS qualified native caller, four complete page displays, CPU fonts/OBJ/screen, close/reentry/movement; natural actor selection remains OPEN')


if __name__=='__main__': main()
