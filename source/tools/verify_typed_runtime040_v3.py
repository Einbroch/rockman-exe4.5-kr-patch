"""Exact040 qualified Korean consumer evidence; separate from natural acquisition."""
import argparse,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def bind(folder,m,version='040',guards=8):
    d=ROOT/folder;r=read(d/'result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is not False or len(r['loaded_rom_guards'])!=guards or (d/'checkpoint.mss').exists() or not (d/'diagnostic_checkpoint.mss').exists():raise ValueError('040 exact diagnostic receipt/quarantine')
    for name,h in r['artifacts'].items():require_hash(d/name,h)
    child=r;ancestry=[]
    while child['state_origin']:
        parent=ROOT/child['state_origin'];p=read(parent)
        if not p['complete'] or p['rom_sha256']!=m['output_sha256'] or p.get('normal_play_checkpoint_eligible') is False or p['artifacts']['checkpoint.mss']!=child['state_sha256']:raise ValueError('040 same-ROM normal ancestor')
        require_hash(parent.parent/'checkpoint.mss',child['state_sha256']);ancestry.append(dict(path=str(parent.relative_to(ROOT)),sha256=sha(parent.read_bytes())));child=p
    if not ancestry[-1]['path'].replace('\\','/').endswith(f'pending500-{version}-normal-v1-01/result.json'):raise ValueError('040 own coldboot ancestry')
    return d,r,ancestry


def setup(rom,m,cfg,arc,script):
    rec=next(r for r in m['keyitem_rom']['typed040']['archives'] if r['archive']==arc);ar=m['active_typed_owners040'][arc];require_hash(ROOT/ar['path'],ar['sha256']);asset=read(ar['path'])
    return model(rom,m,cfg,arc,script,rec['script_count'],record=rec,asset=asset)


def page(d,step,key,mp,rom,m,native,root,origin,terminal,clear=False):
    pool,units,expected,streams,ends=mp;wanted=streams[key];state=read(d/f'step_{step:03}_roll_pet.json');ram=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,actual=struct.unpack_from('<2I',ram,0xFA4C)
    if actual!=pool or ptr!=ends[key] or rom[ptr-0x08000000:ptr-0x08000000+len(terminal)]!=terminal or tuple(ram[0xFA38:0xFA3A])!=origin or ram[root-0x02000000:root-0x02000000+len(native)]!=native:raise ValueError('040 Korean exact root/stream/native residency/wait/origin '+key)
    last={x['stream']:x for x in state['draws'] if x['stream'] in wanted}
    if set(last)!=set(wanted):raise ValueError('040 full current Korean page glyph stream '+key)
    draws=[last[s] for s in wanted];needed=Counter(x['glyph_index'] for x in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in needed.items()):raise ValueError('040 actual Korean font CPU reads '+key)
    proof=pixels(d,step,draws,expected,rom,m,origin=origin,cursor_screen_background=True);vacant=0
    if clear:
        im=Image.open(d/f'step_{step:03}.png').convert('RGB');x0,y0=origin;xend=200 if origin==(32,68) else 234;bg=im.getpixel((205,100) if origin==(32,68) else (233,110));rects=[]
        for draw in draws:
            row,off=divmod(draw['offset'],10752);width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+draw['glyph_index']*4)[0];left=x0+off//4;top=y0+row*14;rects.append((left,top,left+width,top+12))
        for y in range(y0,y0+40):
            for x in range(x0,xend):
                if origin==(52,110) and x>=224 and y>=138:continue
                if not any(a<=x<c and b<=y<e for a,b,c,e in rects):
                    if im.getpixel((x,y))!=bg:raise ValueError('040 Korean page clearing/blank body '+key)
                    vacant+=1
    return dict(step=step,literal=key,wording=next(u['translation'] for u in units if u['id']==key),root=pool,wait_pointer=ptr,native_RAM_residency_verified=True,origin=list(origin),vacant_body_pixels_checked=vacant,**proof)


def tournament(rom,m,cfg,source):
    folder='poc/runtime/pending500-040-tournament-v1';d,r,ancestry=bind(folder,m);t=read(d/'tournament_route.json');events=t['events'];aliases=t['registration_read_aliases'];native=lz77_decompress(source,0x6E93C8)[0]
    if not t['state_intervention'] or len(aliases)!=3 or any({k:v for k,v in x.items() if k!='frame'}!=dict(address=0x02004BF7,original=0,returned=8,pc=0x080287C4,lr=0x08049721) for x in aliases):raise ValueError('040 exact qualified tournament read aliases')
    ordered=[0x080493B4,0x08046530,0x08046568,0x08046650,0x08047976,0x080466AA,0x08047958,0x0804795E,0x0804FB4C];cursor=-1
    for pc in ordered:
        candidates=[i for i,e in enumerate(events) if i>cursor and e['pc']==pc]
        if not candidates:raise ValueError('040 original PET tournament setup/loader/reader order')
        cursor=candidates[0]
    common=events[cursor]
    if (common['registers']['0'],common['registers']['1'],common['registers']['14'])!=(0x02024000,0,0x08047963):raise ValueError('040 actual tournament common ABI')
    starts=[e for e in events if e['pc']==0x08047976]
    if t['loads']!=2 or len(starts)!=2 or any((e['registers']['0'],e['registers']['1'],e['mode'],e['ui_kind'])!=(0x086E93C8,0x02024000,0x24,0) for e in starts) or any((d/f'tournament_native_{i:03}.bin').read_bytes()!=native for i in (1,2)):raise ValueError('040 original tournament full LZ/native bytes')
    mp=setup(rom,m,cfg,'6E93C8',0);pool=mp[0];selected=read(d/'typed_selections040.json')['selections'];calls=[x for x in selected if x['script']==0]
    if len(calls)!=1 or calls[0]['selected_root']!=pool:raise ValueError('040 tournament actual selected clone')
    pages=[page(d,step,f'6E93C8:0:{n}',mp,rom,m,native,0x02024000,(52,110),bytes.fromhex('e600'),True) for n,step in enumerate((11,12,13,14))]
    later=[e for e in events if e['pc']==0x0804FB4C and (e['registers']['0'],e['registers']['1'],e['registers']['14'])==(0x02024000,5,0x08047963)]
    if len(later)!=1 or later[0]['frame']<=common['frame']:raise ValueError('040 intro end to original next script5')
    return dict(pages=pages,source_archive='6E93C8',original_route=ordered,selected_clones=calls,original_load_events=starts,only_read_aliases=aliases,own_coldboot_ancestry=ancestry,receipt=dict(path=folder+'/result.json',sha256=sha((d/'result.json').read_bytes())),original_following_script5_verified=True,natural_registration_verified=False,limits=['Silver intro0 four Korean pages only, not Gold/Official/Navi branches or all13 literals.','Registration-read intervention bypasses acquisition/mail; no tournament outcome/exit/reentry proof.'])


def closed(d,step,rom,native,pool,mode):
    ram=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();o=(d/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
    active=[i for i in range(128) if not (a:=struct.unpack_from('<H',o,i*8)[0])&0x2300 and a>>14<3 and struct.unpack_from('<H',o,i*8+4)[0]>>12==14]
    at=ptr-0x02032000 if pool==0x02032000 else ptr-0x08000000;image=native if pool==0x02032000 else rom
    if ram[0xFA20]!=0 or ram[0x4AD0]!=mode or root!=pool or image[at:at+2]!=bytes.fromhex('edff') or active or (mode==0x20 and ram[0x32000:0x32000+len(native)]!=native):raise ValueError('BBS original automatic closure/field mode/native residency')
    return dict(step=step,context_active=0,retained_root=root,terminal_pointer=ptr,enabled_palette14_objects=len(active),main_mode=mode,native_RAM_verified=ram[0x32000:0x32000+len(native)]==native,native_RAM_lifetime='Required in BBS list; field exit legitimately reuses this shared RAM')


def bbs(rom,m,cfg,source):
    folder='poc/runtime/pending500-040-bbs-v2';d,r,ancestry=bind(folder,m);t=read(d/'bbs_boundary.json');native=lz77_decompress(source,0x7000AC)[0]
    if t['tile_aliases']!=[dict(frame=0,address=0x02004ADE,original=0,returned=0xF4)]:raise ValueError('040 exact qualified BBS environment read')
    fields=[e for e in t['events'] if e['pc']==0x0806A502]
    if len(fields)!=1 or (fields[0]['registers']['0'],fields[0]['registers']['1'])!=(0x0203C800,10):raise ValueError('040 original F4/script10/startBBS')
    for pc,src,dest,num in [(0x0804B80C,0x08700F6C,0x0202E000,1),(0x0804B816,0x087000AC,0x02032000,2)]:
        calls=[e for e in t['events'] if e['pc']==pc];payload=lz77_decompress(source,src-0x08000000)[0]
        if len(calls)!=1 or (calls[0]['registers']['0'],calls[0]['registers']['1'])!=(src,dest) or (d/f'bbs_native_{num:03}_{src:08X}.bin').read_bytes()!=payload:raise ValueError('040 original BBS header/body full LZ')
    if len(t['calls'])!=2 or any((e['root'],e['script'],e['lr'])!=(0x02032000,9,0x0804B5AF) for e in t['calls']):raise ValueError('040 actual BBS original body/reentry ABI')
    mp=setup(rom,m,cfg,'7000AC',9);pool=mp[0];selected=read(d/'typed_selections040.json')['selections']
    if len(selected)!=2 or any((e['script'],e['selected_root'])!=(9,pool) for e in selected):raise ValueError('040 BBS actual selected clone twice')
    pages=[page(d,14,'7000AC:9:0',mp,rom,m,native,0x02032000,(32,68),bytes.fromhex('e600'),True)]
    pages.extend(page(d,15+n,f'7000AC:9:{n}',mp,rom,m,native,0x02032000,(32,68),bytes.fromhex('e600'),True) for n in range(1,10))
    closure=closed(d,25,rom,native,pool,0x20)
    pages.append(page(d,26,'7000AC:9:0',mp,rom,m,native,0x02032000,(32,68),bytes.fromhex('e600'),True))
    pages.append(page(d,27,'7000AC:9:0',mp,rom,m,native,0x02032000,(32,68),bytes.fromhex('e600'),True))
    oldd,oldr,olda=bind('poc/runtime/pending500-040-bbs-v1',m)
    if len(read(oldd/'bbs_boundary.json')['calls'])!=1:raise ValueError('040 original trial call count')
    exitproof=[closed(oldd,step,rom,native,pool,mode) for step,mode in [(25,0x20),(26,0x20),(27,4),(28,4)]]
    basepath='poc/output/pending500_039_v1.gba';bm=read(basepath.replace('.gba','.json'));require_hash(ROOT/basepath,bm['output_sha256']);br=(ROOT/basepath).read_bytes()
    bd,breceipt,ba=bind('poc/runtime/pending500-039-bbs-terminal040-v1',bm,'039',6);bt=read(bd/'bbs_boundary.json')
    if bt['tile_aliases']!=t['tile_aliases'] or len(bt['calls'])!=1 or (bt['calls'][0]['root'],bt['calls'][0]['script'],bt['calls'][0]['lr'])!=(0x02032000,9,0x0804B5AF) or (bd/'bbs_native_002_087000AC.bin').read_bytes()!=native:raise ValueError('039 original BBS control scope')
    baseline=[closed(bd,step,br,native,0x02032000,mode) for step,mode in [(25,0x20),(26,0x20),(27,4),(28,4)]]
    for step in (27,28):
        kr=(oldd/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()[0x32000:0x32000+len(native)]
        jp=(bd/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()[0x32000:0x32000+len(native)]
        if kr!=jp:raise ValueError('040 field-reused shared BBS RAM differs from039 original consumer control')
    ranges=[(0x507A8,0x507BC),(0x553E8,0x55414),(0x4B5C4,0x4B62C)]
    if any(rom[a:b]!=source[a:b] or br[a:b]!=source[a:b] for a,b in ranges):raise ValueError('original EDFF/set8/caller test8/close code unchanged')
    return dict(pages=pages,source_archive='7000AC',actual_body_calls=t['calls'],selected_clones=selected,only_read_aliases=t['tile_aliases'],automatic_terminal_close=closure,post_close_to_list_and_reentry_verified=True,exit_to_field=exitproof,original_Japanese_consumer_control=dict(rom_sha256=sha(br),receipt=dict(path=str((bd/'result.json').relative_to(ROOT)),sha256=sha((bd/'result.json').read_bytes())),ancestry=ba,terminal_and_exit=baseline,scope='039 cumulative ROM with unchanged Japanese BBS consumer, not unmodified retail whole-game'),unchanged_original_code_ranges=ranges,causal_interpretation='EDFF handler507A8 sets flag8 via553E8; BBS caller4B5D8 tests8 and closes via4FC54. Retained context root is not a visible window.',own_coldboot_ancestry=ancestry,receipt=dict(path=folder+'/result.json',sha256=sha((d/'result.json').read_bytes())),exit_trial_receipt=dict(path=str((oldd/'result.json').relative_to(ROOT)),sha256=sha((oldd/'result.json').read_bytes())),natural_board_access_verified=False,limits=['Post9 ten Korean pages plus first-page reentry only, not all336 BBS literals or maximum168px capacity.','Original heading/list remain Japanese; tile-read intervention does not prove natural board acquisition.','Earlier v1 expectation of a visible terminal hold and reentry29 was rejected; v1 evidence retained, no ROM change.'])



def communication(rom,m,cfg,source):
    folder='poc/runtime/pending500-040-new-communication-v1';d,r,ancestry=bind(folder,m);q=read(d/'qualified_navi040.json')['reads'];native=lz77_decompress(source,0x6F8D00)[0]
    if len(q)!=1 or {k:v for k,v in q[0].items() if k!='frame'}!=dict(address=0x02004AD1,original=0,returned=19,pc=0x08000CF0,lr=0x080448CF):raise ValueError('040 loader-only qualified Navi read')
    t=read(d/'communication_trace.json');loads=[e for e in t['events'] if e['pc']==0x080448D6]
    if t['loads']!=1 or len(loads)!=1 or (loads[0]['registers']['0'],loads[0]['registers']['1'])!=(0x086F8D00,0x02024000) or (d/'communication_native_001.bin').read_bytes()!=native:raise ValueError('040 original lookup/LZ/shared RAM new communication')
    mp=setup(rom,m,cfg,'6F8D00',16);pool=mp[0];t=read(d/'communication_nested.json');calls=[x for x in t['calls'] if x['script']==16];selected=[x for x in t['selectors'] if x['script']==16]
    if not calls or not selected or any((x['root'],x['lr'],x['saved_outer_lr'])!=(0x02024000,0x0804F7BD,0x080448C7) for x in calls) or any(x['selected_root']!=pool for x in selected):raise ValueError('040 real nested communication caller/typed clone')
    commands=t['commands'];zero=[e for e in commands if e['pc']==0x08051098];holds=[e for e in commands if e['pc']==0x08050754]
    if not zero or len(holds)<2 or any((e['op'],e['arg'],e['context'])!=(0xED,0xFF,0x0200FA20) for e in holds):raise ValueError('040 real zero-speed and hold commands')
    proof=page(d,3,'6F8D00:16:0',mp,rom,m,native,0x02024000,(92,110),bytes.fromhex('edff0000'))
    mp15=setup(rom,m,cfg,'6F8D00',15);calls15=[x for x in t['calls'] if x['script']==15];sel15=[x for x in t['selectors'] if x['script']==15]
    if not calls15 or not sel15 or any((x['root'],x['lr'],x['saved_outer_lr'])!=(0x02024000,0x0804F7BD,0x080448C7) for x in calls15) or any(x['selected_root']!=mp15[0] for x in sel15):raise ValueError('040 nested caller for second help')
    proof15=page(d,4,'6F8D00:15:0',mp15,rom,m,native,0x02024000,(92,110),bytes.fromhex('edff0000'))
    for step in (1,2,3,4,5,6):
        ram=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0x4AD1]!=0:raise ValueError('040 actual player Navi changed')
    ram=(d/'step_005_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('040 new communication Bcancel')
    return dict(pages=[proof,proof15],source_archive='6F8D00',source_load_events=loads,actual_nested_calls=calls+calls15,selected_clones=selected+sel15,actual_control_counts=dict(F000=len(zero),EDFF=len(holds)),only_read_aliases=q,actual_player_Navi_unchanged=True,cancel_to_PET_verified=True,own_coldboot_ancestry=ancestry,receipt=dict(path=folder+'/result.json',sha256=sha((d/'result.json').read_bytes())),natural_Navi19_acquisition_verified=False,limits=['Two new6F8D00:16:0 and15:0 Korean help pages, not all151 new help literals.','Only communication loader Navi read changes0->19; actual player remains0. No Navi19 acquisition or multiplayer outcomes.','Japanese small labels unchanged; no Hangul persistence/hardware/audio/human approval.'])


def main():
    p=argparse.ArgumentParser();p.add_argument('consumer',choices=['tournament','bbs','communication']);a=p.parse_args();rp=ROOT/'poc/output/pending500_040_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();audit=read('analysis/pending500_040_v2/integration.json');normal=read('analysis/pending500_040_v2/normal_path_v1.json')
    if not audit['passed'] or not normal['passed'] or audit['rom_sha256']!=sha(rom) or normal['rom_sha256']!=sha(rom):raise ValueError('040 audited and own normal regression artifact')
    result=globals()[a.consumer](rom,m,cfg,source);cap='new_communication' if a.consumer=='communication' else a.consumer;paths=['tools/verify_typed_runtime040_v3.py','tools/verify_typed_runtime040_v2.py','tools/verify_typed_runtime040_v1.py','tools/capture_'+cap+'040_v1.py','tools/run_'+cap+'040_v1.py','analysis/pending500_040_v2/integration.json','analysis/pending500_040_v2/normal_path_v1.json']
    if a.consumer=='bbs':paths+=['tools/run_bbs040_v2.py','tools/run_bbs_terminal_baseline040_v1.py','tools/capture_bbs_boundary040_v1.py']
    result.update(passed=True,scope=__doc__,rom_sha256=sha(rom),source_sha256=sha(source),consumer=a.consumer,game_RAM_ROM_PC_or_caller_writes=False,runtime_includes_full_original_initialization=True,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths})
    frozen_write(ROOT/'analysis/pending500_040_v2'/(cap+'_runtime_v1.json'),result);print('PASS040 qualified Korean',a.consumer,len(result['pages']),'page displays/font/OBJ/pixels; NOT natural acquisition/fullgame/release')


if __name__=='__main__':main()




