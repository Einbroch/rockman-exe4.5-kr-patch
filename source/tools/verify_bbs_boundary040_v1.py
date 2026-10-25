"""Qualified039 original BBS load/reader/two-page pixels; NOT040 Korean proof."""
import re,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from tpl_literals import literals
from report_roll_pet import pixels
from consumer_links040_v1 import contracts


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rp=ROOT/'poc/output/pending500_039_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();contracts(source);d=ROOT/'poc/runtime/pending500-039-bbs-boundary040-v2';r=read(d/'result.json')
    if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or len(r['loaded_rom_guards'])!=6 or (d/'checkpoint.mss').exists() or not (d/'diagnostic_checkpoint.mss').exists():raise ValueError('040 BBS diagnostic binding/quarantine')
    for name,h in r['artifacts'].items():require_hash(d/name,h)
    parent=ROOT/r['state_origin'];p=read(parent);require_hash(parent.parent/'checkpoint.mss',r['state_sha256'])
    if p['rom_sha256']!=sha(rom) or p['artifacts']['checkpoint.mss']!=r['state_sha256'] or p.get('normal_play_checkpoint_eligible') is False:raise ValueError('040 same039 normal parent')
    trace=read(d/'bbs_boundary.json')
    if trace['tile_aliases']!=[dict(frame=0,address=0x02004ADE,original=0,returned=0xF4)] or source[0x56948]!=10:raise ValueError('040 exact original F4-to-script10 diagnostic')
    events=trace['events'];field=[e for e in events if e['pc']==0x0806A502]
    if len(field)!=1 or (field[0]['registers']['0'],field[0]['registers']['1'])!=(0x0203C800,10):raise ValueError('040 original field reader/script10')
    for pc,src,dest,num in [(0x0804B80C,0x08700F6C,0x0202E000,1),(0x0804B816,0x087000AC,0x02032000,2)]:
        calls=[e for e in events if e['pc']==pc];native=lz77_decompress(source,src-0x08000000)[0]
        if len(calls)!=1 or (calls[0]['registers']['0'],calls[0]['registers']['1'])!=(src,dest) or (d/f'bbs_native_{num:03}_{src:08X}.bin').read_bytes()!=native:raise ValueError('040 actual BBS original compressed load')
    calls=trace['calls']
    if len(calls)!=1 or (calls[0]['root'],calls[0]['script'],calls[0]['lr'])!=(0x02032000,9,0x0804B5AF):raise ValueError('040 actual BBS reader/common caller')
    native=lz77_decompress(source,0x7000AC)[0];tpl=(ROOT/'analysis/full_scope_v1/source_tpl/7000AC.tpl').read_text(encoding='utf-8-sig');allunits=[u for u in literals(tpl) if u.key.startswith('7000AC:9:')];count=struct.unpack_from('<H',native)[0]//2;span=script_spans(native,count)[9];start=0x02032000+struct.unpack_from('<H',native,18)[0];codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1};pages=[]
    for ordinal,step in [(0,14),(0,15),(1,17)]:
        unit=allunits[ordinal];encoded=b''.join(b'\xe8' if c=='\n' else codes[c] for c in unit.text)
        if span.count(encoded)!=1:raise ValueError('040 original BBS literal boundary uniqueness')
        cursor=start+span.index(encoded);expected={};streams=[]
        for c in unit.text:
            if c=='\n':cursor+=1;continue
            code=codes[c]
            if len(code)==1 and code[0]<0xE4:index=code[0]
            elif len(code)==2 and code[0]==0xE4:index=228+code[1]
            else:raise ValueError('040 unmodeled original glyph code')
            rec=rom[m['extension']['normal_font_offset']+96*index:m['extension']['normal_font_offset']+96*(index+1)]
            if rec!=source[0x608758+96*index:0x608758+96*(index+1)]:raise ValueError('040 original BBS font bytes')
            expected[cursor]=dict(ch=c,index=index,record=rec,id=unit.key);streams.append(cursor);cursor+=len(code)
        state=read(d/f'step_{step:03}_roll_pet.json');last={x['stream']:x for x in state['draws'] if x['stream'] in streams}
        if set(last)!=set(streams):raise ValueError('040 original BBS full current page glyph stream')
        draws=[last[s] for s in streams];ram=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=0x02032000 or ptr!=cursor or ram[ptr-0x02000000:ptr-0x02000000+2]!=bytes.fromhex('e600') or tuple(ram[0xFA38:0xFA3A])!=(32,68) or ram[0x32000:0x32000+len(native)]!=native:raise ValueError('040 BBS root/stream/keyWait/origin/residency')
        reads={x['index']:x['reads'] for x in state['font_reads']};needed=Counter(x['glyph_index'] for x in draws)
        if any(reads.get(i,0)<24*n for i,n in needed.items()):raise ValueError('040 BBS actual font reads')
        proof=pixels(d,step,draws,expected,rom,m,origin=(32,68),cursor_screen_background=True);im=Image.open(d/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((215,100));rects=[]
        for x in draws:
            row,off=divmod(x['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+x['glyph_index']*4)[0];left=32+off//4;top=68+row*14;rects.append((left,top,left+width,top+12))
        vacant=[(x,y) for y in range(68,108) for x in range(32,200) if not any(a<=x<c and b<=y<e for a,b,c,e in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('040 BBS native page clearing/blank body pixels')
        pages.append(dict(step=step,literal=unit.key,origin=[32,68],native_RAM_root=root,wait_pointer=ptr,vacant_body_pixels_checked=len(vacant),native_page_clearing_verified=True,**proof))
    deps=['tools/verify_bbs_boundary040_v1.py','tools/capture_bbs_boundary040_v1.py','tools/run_bbs_boundary040_v2.py','tools/consumer_links040_v1.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_040_source_v2/bbs_boundary_v1.json',dict(passed=True,scope=__doc__,baseline_sha256=sha(rom),source_sha256=sha(source),source_archive='7000AC',native_bytes=len(native),actual_reader_calls=calls,load_events=[e for e in events if e['pc'] in (0x0804B80C,0x0804B816)],pages=pages,source_message_model=dict(origin=[32,68],trial_Korean_row_limits=[168,168,168],trial_right_edge=200,arrow=[202,108],Korean_runtime_still_required=True),receipt=dict(path=str((d/'result.json').relative_to(ROOT)),sha256=sha((d/'result.json').read_bytes())),only_intervention=trace['tile_aliases'],game_RAM_ROM_PC_or_caller_writes=False,natural_board_access_verified=False,Korean040_display_verified=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Qualified original Japanese BBS source9 two pages/three displays only, not040 Korean pixels or all336 BBS strings.','F4 read alias uses original field table and source script/startBBS; it is not natural field acquisition.','B at last probe advanced another page; terminal EDFF/close/back/reentry not yet certified.','168px trial Korean constraint is inside the tested blank-body rectangle, not maximum renderer capacity or full Korean cache/timing proof.']))
    print('PASS040 qualified039 native BBS loads -> actual root/caller -> source2pages/font/OBJ/pixels/clear; NOT040 Korean')


if __name__=='__main__':main()
