"""Exact032 Korean date/menu/choice/anniversary literal font and pixel proof."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from report_roll_pet import verify_route,pixels
from verify_pending500_005_displays import model


def main():
    rp=ROOT/'poc/output/pending500_032_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');rt=ROOT/'poc/runtime';out=ROOT/'analysis/pending500_032_v1';prefix='pending500-032-menu-';receipts=[]
    parents=[('home','pending500-032-v1-complete'),('register',prefix+'home'),('second',prefix+'register'),('cancel',prefix+'second'),('time-edit',prefix+'register'),('time',prefix+'time-edit'),('meal',prefix+'time'),('inventory','pending500-032-v1-complete'),('inventory-cancel',prefix+'inventory'),('inventory-reentry',prefix+'inventory-cancel'),('inventory-accept',prefix+'inventory')]
    for name,parent in parents:
        folder=rt/(prefix+name);r=verify_route(folder,m['output_sha256'],set())
        if r['state_origin']!=str(rt/parent/'result.json') or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('032 menu own normal ancestry')
        if any(t in (folder/'segment.lua').read_text(encoding='utf8') for t in ('emu.write','setState','AliasReads')):raise ValueError('032 menu intervention')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
    carry=read('analysis/pending_insertion_500_032_carry_v2/preflight.json');record=next(r for r in carry['archives'] if r['archive']=='659CB8');asset=read(record['merged_asset']['path']);cache={};pages=[]
    def data(script):
        if script not in cache:cache[script]=model(rom,m,cfg,'659CB8',script,record['script_count'],asset=asset)
        return cache[script]
    def widths(index):return struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
    def position(script,key,row,col):
        pool,units,expected,streams,ends=data(script);unit=next(u for u in units if u['id']==key);it=iter(streams[key]);positions={}
        for ch in unit['translation']:
            if ch=='\n':row+=1;col=0;continue
            stream=next(it);positions[stream]=row*10752+col*4;col+=widths(expected[stream]['index'])
        return positions,row,col
    def cursor_slots(folder):
        # Exact normal route receipts: native allocator reserves UI objects
        # before acquiring the dialogue cursor. Slot is not globally constant.
        if folder.name in (prefix+'register',prefix+'second'):return (16,)
        if folder.name==prefix+'meal':return (2,)
        return (1,)
    def inspect(folder,step,script,keys,positions,extra=None,origin=None):
        pool,units,expected,streams,ends=data(script);wanted={s:expected[s] for k in keys for s in streams[k]}
        if extra:wanted.update(extra)
        trace=read((origin or folder)/f'step_{step:03}_event_buffers.json');draws={d['stream']:d for d in trace['draws'] if d['stream'] in wanted};ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if set(draws)!=set(wanted) or any(d['glyph_index']!=wanted[s]['index'] or d['offset']!=positions[s] or d['context']!=0x0200FA20 for s,d in draws.items()):raise ValueError('032 literal/provider exact glyph positions '+folder.name)
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('032 menu active root/script/native origin')
        reads={x['index']:x['reads'] for x in trace['font_reads']};counts=Counter(v['index'] for v in wanted.values())
        if any(reads.get(i,0)<n*24 for i,n in counts.items()):raise ValueError('032 actual menu font CPU reads')
        proof=pixels(folder,step,list(draws.values()),wanted,rom,m,origin=(52,110),cursor_indices=cursor_slots(folder),cursor_screen_background=True);pages.append(dict(segment=folder.name,step=step,script=script,ids=keys,draw_trace_origin=str((origin or folder).relative_to(ROOT)),inherited_residency_only=origin is not None,**proof));return ram
    def ram_body(ram,address):
        result=[];i=address;start=address
        while i<start+32:
            b=ram[i];stream=0x02000000+i;i+=1
            if b==0xE5:return result
            if b==0xE4:b=228+ram[i];i+=1
            elif b>=0xE5:raise ValueError('032 current native RAM fixture encoding')
            if b>=441:raise ValueError('032 native fixture glyph bound')
            at=m['extension']['normal_font_offset']+b*96;result.append((stream,b,widths(b),rom[at:at+96]))
        raise ValueError('032 native RAM string terminator')
    # Current-date values must agree with the actual native cached month/day;
    # font positions are calculated independently, not copied from draw logs.
    home=rt/(prefix+'home');ram=(home/'step_003_gbaExtWorkRam.bin').read_bytes();keys=[f'659CB8:0:{i}' for i in range(3)];positions,row,col=position(0,keys[0],0,0);extra={}
    for key,field,address in [(keys[1],1,0x10AC0),(keys[2],2,0x10B40)]:
        value=ram[0x12EC0+field]
        if not 1<=value<=(12 if field==1 else 31):raise ValueError('032 actual current date domain')
        text=f'{value:2}';body=bytes(0 if c==' ' else int(c)+1 for c in text)+bytes.fromhex('e50000')
        if ram[address:address+5]!=body:raise ValueError('032 current date producer/cache/formatter value')
        for stream,index,w,glyph in ram_body(ram,address):positions[stream]=row*10752+col*4;extra[stream]=dict(index=index,record=glyph,ch='native-date',id='current-date');col+=w
        p,row,col=position(0,key,row,col);positions.update(p)
    inspect(home,3,0,keys,positions,extra)
    # F608 width7:176px mode, allocation85 ->text x97, padded label x105.
    keys=[f'659CB8:2:{i}' for i in range(3)];positions={}
    for key,row,col in [(keys[0],0,0),(keys[1],1,53),(keys[2],2,53)]:positions.update(position(2,key,row,col)[0])
    register=rt/(prefix+'register');inspect(register,3,2,keys,positions)
    for name,y in [('register',122),('second',136)]:
        folder=rt/(prefix+name);step=3 if name=='register' else 2
        if name=='second':
            # Only the cursor moves: retain the parent's render event trace,
            # but verify fresh current VRAM/OBJ/pixels under the exact parent.
            pool,units,expected,streams,ends=data(2);wanted={s:expected[s] for k in keys for s in streams[k]};trace=read(register/'step_003_event_buffers.json');ds={d['stream']:d for d in trace['draws'] if d['stream'] in wanted};r=(folder/'step_002_gbaExtWorkRam.bin').read_bytes()
            if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=2:raise ValueError('032 moved vertical cursor stays same menu')
            proof=pixels(folder,2,list(ds.values()),wanted,rom,m,origin=(52,110),cursor_indices=cursor_slots(folder),cursor_screen_background=True);pages.append(dict(segment=folder.name,step=2,script=2,ids=keys,inherited_residency_only=True,draw_trace_origin=str(register.relative_to(ROOT)),**proof))
        o=(folder/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,c=struct.unpack_from('<HHH',o,16*8)
        if (a&255,b&511,c&1023,c>>12,a>>14,b>>14)!=(y,89,1020,14,0,1):raise ValueError('032 actual vertical option cursor')
    cancel=(rt/(prefix+'cancel')/'step_002_gbaExtWorkRam.bin').read_bytes()
    if cancel[0xFA21]!=1:raise ValueError('032 BSeparate cancel returns original date-selection prompt1')
    # Native one-option possessions page with the normal legacy nickname.
    inv=rt/(prefix+'inventory');ram=(inv/'step_002_gbaExtWorkRam.bin').read_bytes();keys=[f'659CB8:10:{i}' for i in range(3)];positions,row,col=position(10,keys[0],0,0);extra={};body=ram_body(ram,0x10AC0)
    if sum(x[2] for x in body)>99:raise ValueError('032 current native nickname conditional bound')
    for stream,index,w,glyph in body:positions[stream]=row*10752+col*4;extra[stream]=dict(index=index,record=glyph,ch='native-nickname',id='native-nickname');col+=w
    p,row,col=position(10,keys[1],row,col);positions.update(p)
    if (row,col)!=(2,0):raise ValueError('032 inventory caption empty option row')
    positions.update(position(10,keys[2],2,8)[0]);inspect(inv,2,10,keys,positions,extra)
    # New horizontal confirmation24 is sampled before accepting the meal.
    script=24;keys=[f'659CB8:24:{i}' for i in range(3)];positions=position(script,keys[0],0,0)[0];positions.update(position(script,keys[1],2,48)[0]);w=sum(widths(data(script)[2][s]['index']) for s in data(script)[3][keys[1]]);positions.update(position(script,keys[2],2,48+w+8)[0]);inspect(rt/(prefix+'meal'),5,script,keys,positions)
    # New calendar51 caption and Korean Yes/No on the actual ten-native-title.
    prefix2='calendar-anniversary-032-product-';keys=['659CB8:51:6'];positions=position(51,keys[0],1,129)[0];inspect(rt/(prefix2+'delete-first-v1'),2,51,keys,positions)
    keys=[f'659CB8:51:{i}' for i in (7,8,9)];positions=position(51,keys[0],0,0)[0];positions.update(position(51,keys[1],2,48)[0]);w=sum(widths(data(51)[2][s]['index']) for s in data(51)[3][keys[1]]);positions.update(position(51,keys[2],2,48+w+8)[0]);inspect(rt/(prefix2+'delete-confirm-v1'),2,51,keys,positions)
    observed=sorted({key for p in pages for key in p['ids']});selection=read('analysis/pending_insertion_500_032_calendar_selection_v3/selection.json')
    if not set(observed)<=set(selection['selected_ids']):raise ValueError('032 sampled IDs are actual new selection')
    native=read(out/'anniversary_runtime.json')
    if not native['passed'] or native['baseline_sha256']!=m['output_sha256']:raise ValueError('032 native anniversary record/outcome evidence')
    frozen_write(out/'calendar_menu_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],pages=pages,new_Korean_literal_ids=observed,receipts=receipts,normal_routes=True,checker=dict(path='tools/verify_calendar_menu_product_032_v2.py',sha256=sha((ROOT/'tools/verify_calendar_menu_product_032_v2.py').read_bytes())),native_anniversary_outcomes=native['outcomes'],visual_review_pending=True,release_eligible=False,limits=['Bounded normal Rockman0/2/10/24/51 samples, current cached date/native nickname/ten-native-title, vertical focus and BSeparate cancel; not all500 natural scenes/Navi or wording/voice approval.','Moved vertical selection has inherited render trace and fresh residency/pixels, not new CPU drawing.','Anniversary52,FireMan7width,other helpers and native conditional geometry are CPU/static only; all writers/imports/save/reset/reload/full Hangul support remain open.']))
    print('032 current-date/vertical/single-option/horizontal/anniversary Korean literal font-OBJ-pixels PASS',len(observed),'new IDs')


if __name__=='__main__':main()
