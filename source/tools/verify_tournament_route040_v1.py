"""Qualified039 PET -> native tournament load -> intro0 four pages; NOT040."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from consumer_links040_v1 import contracts
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from tpl_literals import literals
from report_roll_pet import pixels


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rp=ROOT/'poc/output/pending500_039_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();contracts(source)
    folder='poc/runtime/pending500-039-tournament-route040-v4';d=ROOT/folder;r=read(d/'result.json')
    if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or not r['state_intervention'] or len(r['loaded_rom_guards'])!=6 or (d/'checkpoint.mss').exists() or not (d/'diagnostic_checkpoint.mss').exists():raise ValueError('040 tournament diagnostic binding/quarantine')
    for name,h in r['artifacts'].items():require_hash(d/name,h)
    parent=ROOT/r['state_origin'];p=read(parent);require_hash(parent.parent/'checkpoint.mss',r['state_sha256'])
    if p['rom_sha256']!=sha(rom) or p['artifacts']['checkpoint.mss']!=r['state_sha256'] or p.get('normal_play_checkpoint_eligible') is False:raise ValueError('040 own039 normal PET parent')
    t=read(d/'tournament_route.json');events=t['events'];aliases=t['registration_read_aliases']
    if t['state_intervention'] is not True or [a['frame'] for a in aliases]!=[252,895,895] or any({k:v for k,v in a.items() if k!='frame'}!=dict(address=0x02004BF7,original=0,returned=8,pc=0x080287C4,lr=0x08049721) for a in aliases):raise ValueError('040 exact registration flag92 read alias')
    seq=[(0x080493B4,895),(0x08046530,895),(0x08046568,895),(0x08046650,899),(0x08047976,899),(0x080466AA,923),(0x08047958,923),(0x0804795E,923),(0x0804FB4C,923),(0x0804FB90,923)]
    slots=[]
    for pc,frame in seq:
        matches=[i for i,e in enumerate(events) if (e['pc'],e['frame'])==(pc,frame)]
        if len(matches)!=1:raise ValueError('040 actual original PET tournament setup chain')
        slots.append(matches[0])
    if slots!=sorted(slots):raise ValueError('040 original tournament ordering')
    e=events[slots[4]];args=e['registers']
    if (args['0'],args['1'],e['mode'],e['ui_kind'])!=(0x086E93C8,0x02024000,0x24,0):raise ValueError('040 original tournament loader/UIkind0')
    native=lz77_decompress(source,0x6E93C8)[0]
    if t['loads']!=2 or any((d/f'tournament_native_{i:03}.bin').read_bytes()!=native for i in (1,2)):raise ValueError('040 two actual native tournament LZ results')
    common=events[slots[8]]
    if (common['registers']['0'],common['registers']['1'],common['registers']['14'])!=(0x02024000,0,0x08047963):raise ValueError('040 actual tournament common root/script/caller')
    later=[e for e in events if e['pc']==0x0804FB4C and e['registers']['0']==0x02024000 and e['registers']['1']==5]
    if len(later)!=1 or later[0]['frame']<=923 or later[0]['registers']['14']!=0x08047963:raise ValueError('040 original intro end -> original next script5')
    baseline=read('poc/runtime/pending500-039-tournament-route040-v2/tournament_route.json')
    if baseline['state_intervention'] or baseline['loads'] or any(e['pc']==0x080493B4 for e in baseline['events']):raise ValueError('040 unchanged control route without registration blocked')
    count=struct.unpack_from('<H',native)[0]//2;span=script_spans(native,count)[0];start=0x02024000+struct.unpack_from('<H',native)[0];tpl=(ROOT/'analysis/full_scope_v1/source_tpl/6E93C8.tpl').read_text(encoding='utf-8-sig');units=[u for u in literals(tpl) if u.key.startswith('6E93C8:0:')]
    if len(units)!=4:raise ValueError('040 exact source introduction literal count')
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1};pages=[]
    for ordinal,step in enumerate((11,12,13,14)):
        u=units[ordinal];encoded=b''.join(b'\xe8' if c=='\n' else codes[c] for c in u.text)
        if span.count(encoded)!=1:raise ValueError('040 unique source tournament literal')
        cursor=start+span.index(encoded);expected={};streams=[]
        for ch in u.text:
            if ch=='\n':cursor+=1;continue
            code=codes[ch]
            if len(code)==1 and code[0]<0xE4:index=code[0]
            elif len(code)==2 and code[0]==0xE4:index=228+code[1]
            else:raise ValueError('040 unmapped source glyph')
            record=rom[m['extension']['normal_font_offset']+96*index:m['extension']['normal_font_offset']+96*(index+1)]
            if record!=source[0x608758+96*index:0x608758+96*(index+1)]:raise ValueError('040 original tournament glyph identity')
            expected[cursor]=dict(ch=ch,index=index,record=record,id=u.key);streams.append(cursor);cursor+=len(code)
        state=read(d/f'step_{step:03}_roll_pet.json');last={x['stream']:x for x in state['draws'] if x['stream'] in streams}
        if set(last)!=set(streams):raise ValueError('040 complete original tournament page glyph consumption')
        draws=[last[s] for s in streams];ram=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=0x02024000 or ptr!=cursor or ram[ptr-0x02000000:ptr-0x02000000+2]!=bytes.fromhex('e600') or tuple(ram[0xFA38:0xFA3A])!=(52,110) or ram[0x24000:0x24000+len(native)]!=native:raise ValueError('040 tournament root/stream/keyWait/origin/residency')
        counts=Counter(x['glyph_index'] for x in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('040 original tournament actual font read')
        proof=pixels(d,step,draws,expected,rom,m,origin=(52,110),cursor_screen_background=True)
        pages.append(dict(step=step,literal=u.key,origin=[52,110],wait_pointer=ptr,native_residency_verified=True,**proof))
    deps=['tools/verify_tournament_route040_v1.py','tools/capture_tournament_route040_v4.py','tools/run_tournament_route040_v4.py','tools/capture_tournament_route040_v2.py','tools/run_tournament_route040_v2.py','tools/consumer_links040_v1.py'];control='poc/runtime/pending500-039-tournament-route040-v2/result.json'
    frozen_write(ROOT/'analysis/pending_insertion_500_040_source_v2/tournament_boundary_v1.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(rom),source_archive='6E93C8',script_count=count,native_bytes=len(native),original_route=seq,actual_common_call=common,pages=pages,only_interventions=aliases,game_RAM_ROM_PC_or_caller_writes=False,natural_registration_verified=False,Korean040_display_verified=False,release_eligible=False,receipt=dict(path=folder+'/result.json',sha256=sha((d/'result.json').read_bytes())),unmodified_control=dict(path=control,sha256=sha((ROOT/control).read_bytes())),route_reference=dict(url='https://gamefaqs.gamespot.com/gba/921255-rockman-exe-45-real-operation/faqs/34214',role='External original-game route proposal: registration mail, weekend and PET Tournament choice; target path independently observed here, natural prerequisites bypassed only as recorded.'),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['One qualified Silver intro0/four Japanese pages, not all13 new Korean literals or Gold/Official/Navi branches.','Registration92 read alias bypasses natural registration/mail acquisition; original PET confirmation/initializer/mode24/loader/reader intact.','Original intro0 end and subsequent script5 verified by original reader call, not tournament outcomes/completion/exit/reentry.','All states quarantined; no user emulator or native saves changed.']))
    print('PASS040 qualified039 PET -> source6E93C8 native LZ -> intro0 four source pages/font/OBJ/pixels -> next original script5; NOT040 Korean')


if __name__=='__main__':main()
