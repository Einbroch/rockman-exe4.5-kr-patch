"""Own031 native anniversary cap10 ->21byte record ->calendar51 five buffers."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from report_roll_pet import pixels,verify_route


def main():
    rp=ROOT/'poc/output/pending500_031_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rt=ROOT/'poc/runtime';prefix='calendar-anniversary-032-'
    parents=[('menu','pending500-031-v1-complete'),('types',prefix+'menu-v1'),('other',prefix+'types-v1'),('picker',prefix+'other-v1'),('ten',prefix+'picker-v1'),('register',prefix+'ten-v1'),('delete-selector',prefix+'register-v1'),('delete-list',prefix+'delete-selector-v1'),('delete-first',prefix+'delete-list-v1'),('delete-confirm',prefix+'delete-first-v1'),('delete-no',prefix+'delete-confirm-v1'),('delete-yes',prefix+'delete-confirm-v1')];receipts=[]
    for name,parent in parents:
        folder=rt/(prefix+name+'-v1');r=verify_route(folder,m['output_sha256'],set())
        if r['state_origin']!=str(rt/parent/'result.json') or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('032 anniversary own normal ancestry')
        if any(t in (folder/'segment.lua').read_text(encoding='utf8') for t in ('emu.write','setState','AliasReads')):raise ValueError('032 anniversary intervention')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
    typed=rt/(prefix+'ten-v1');observed=[]
    for step,length in [(1,0),(2,1),(11,10),(12,10)]:
        ram=(typed/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if list(ram[0xFC44:0xFC49])!=[10,39,6,5,0] or any(struct.unpack_from('<I',ram,a)[0]!=0x0200FC60+length*2 for a in (0xFC54,0xFC58)) or ram[0xFC60:0xFC75]!=bytes.fromhex('e406')*length+b'\x98\0'*(10-length)+b'\xE5':raise ValueError('032 actual native anniversary cap10 state')
        observed.append(dict(step=step,length=length,capacity=10,heading=39,token_hex='e406'))
    body=bytes.fromhex('e406')*10+b'\xE5';record=bytes.fromhex('05000001010600000000')+body+bytes(1)
    if (rt/(prefix+'register-v1')/'step_004_gbaExtWorkRam.bin').read_bytes()[0x1310:0x1330]!=record:raise ValueError('032 native anniversary record commit')
    folder=rt/(prefix+'delete-first-v1');ram=(folder/'step_002_gbaExtWorkRam.bin').read_bytes();trace=read(folder/'step_002_event_buffers.json');native=next(r for r in m['archives'] if r['archive']=='659CB8');pool=0x08000000+native['rom_offset']
    if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=51 or tuple(ram[0xFA38:0xFA3A])!=(52,110) or struct.unpack_from('<H',ram,0xFA84)[0]!=5 or ram[0x1310:0x1330]!=record or ram[0x10CC0:0x10CD5]!=body:raise ValueError('032 actual calendar51/root/five slots/record')
    weekday=next(b for b in read('analysis/pending_insertion_500_032_date_cpu_v1/cpu.json')['weekday_bodies'] if b['image']=='031' and b['weekday']==6)
    for at,want in [(0x10AC0,bytes.fromhex('0101e50000')),(0x10B40,bytes.fromhex('0002e50000')),(0x10BC0,bytes.fromhex('0002e50000')),(0x10C40,bytes.fromhex(weekday['raw_hex'])),(0x10CC0,body)]:
        if ram[at:at+len(want)]!=want:raise ValueError('032 actual five date/title values')
    events=trace['events'];names=[e for e in events if e['kind'] in ('name-entry','name-return')]
    if len(names)!=2 or any(e['record']!=0x02001310 or bytes.fromhex(e['record_hex'])!=record for e in names) or names[1]['r0']!=20 or not bytes.fromhex(names[1]['buffer_hex']).startswith(body):raise ValueError('032 actual native anniversary name producer')
    copies=[e for e in events if e['kind']=='copy' and e['r0']==0x0200131A and e['r1']==0x02014E54]
    if len(copies)!=1 or copies[0]['lr']!=0x08034131:raise ValueError('032 native21byte record->producer copy')
    ds=[d for d in trace['draws'] if 0x02010AC0<=d['stream']<0x02010D40];want=[(0x02010AC0,1,0),(0x02010AC1,1,44),(0x02010B40,0,132),(0x02010B41,2,164),(0x02010BC0,0,252),(0x02010BC1,2,284),(0x02010C40,weekday['glyphs'][0],404)]+[(0x02010CC0+2*i,234,10828+44*i) for i in range(10)]
    if [(d['stream'],d['glyph_index'],d['offset']) for d in ds]!=want or any(d['context']!=0x0200FA20 for d in ds):raise ValueError('032 ordered date/title native glyph geometry')
    expected={};counts={}
    for d in ds:
        i=d['glyph_index'];at=m['extension']['normal_font_offset']+i*96;glyph=rom[at:at+96]
        if glyph!=source[0x608758+i*96:0x608758+(i+1)*96]:raise ValueError('032 native date/title font identity')
        expected[d['stream']]=dict(index=i,record=glyph,ch='native-date-title',id='native-anniversary-cap10');counts[i]=counts.get(i,0)+1
    reads={f['index']:f['reads'] for f in trace['font_reads']}
    if any(reads.get(i,0)<n*24 for i,n in counts.items()):raise ValueError('032 actual native date/title CPU reads')
    proof=pixels(folder,2,ds,expected,rom,m,origin=(52,110));cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
    if rom[cursor-0x08000000:cursor-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('032 source native51 wait/clear')
    outcomes={}
    for name,step,deleted in [('delete-no',3,False),('delete-yes',2,True)]:
        data=(rt/(prefix+name+'-v1')/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if data[0x1310:0x1330]!=(bytes(32) if deleted else record) or data[0xFA20]!=0:raise ValueError('032 native51 Yes/No record result')
        outcomes[name]=dict(record_deleted=deleted,dialogue_closed=True)
    screenshots=[(typed,n) for n in (11,12)]+[(rt/(prefix+n+'-v1'),s) for n,s in [('register',4),('delete-first',2),('delete-confirm',2),('delete-no',3),('delete-yes',2)]]
    deps=['tools/verify_calendar_anniversary_032.py','tools/run_calendar_anniversary_probe_032.py','tools/capture_event_buffers_product_031.py','analysis/pending_insertion_500_032_date_cpu_v1/cpu.json']
    frozen_write(ROOT/'analysis/pending_insertion_500_032_anniversary_runtime_v1/verification.json',dict(schema=1,passed=True,baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),source_sha256=sha(source),receipts=receipts,editor_observations=observed,tenth_accepted=True,eleventh_rejected=True,native_title_bytes=21,native_title_advance=110,normal_registered_record_hex=record.hex(),actual_calendar_script=51,five_slots=True,glyphs=proof,outcomes=outcomes,source_wait_clear=True,screenshots={str((p/f'step_{s:03}.png').relative_to(ROOT)):sha((p/f'step_{s:03}.png').read_bytes()) for p,s in screenshots},screenshots_directly_viewed=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,release_eligible=False,limits=['Own031 native legacy anniversary-other cap10 only; two-byteE406 maximal token fixture. Not arbitrary imported/corrupt titles, all birthday presets/writers or new Hangul input.','Source Japanese calendar51 prompts/choices remain; no new Korean032 prose or script52 gameplay proof.','Normal same-session edit/commit/delete preview and Yes/No, not native save/reset/fresh reload, all dates or full gameplay.']))
    print('032 native anniversary10/21byte record/calendar51/five slots/17 glyphs/fontOBJpixels/Yes-No PASS; no ROM')


if __name__=='__main__':main()
