"""Own030 normal other-title native8 capacity, registration and RAM display."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from report_roll_pet import verify_route,pixels
from bench_event_buffers_031 import BASE

OUT='analysis/pending_insertion_500_031_event_native_boundary_v1/verification.json'


def main():
    rp=ROOT/BASE;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rt=ROOT/'poc/runtime';prefix='event-buffers-031-';parent=prefix+'time-v1';receipts=[]
    for short in ('other','other-picker','other-eight','other-register','other-query'):
        folder=rt/(prefix+short+'-v1');r=verify_route(folder,m['output_sha256'],set())
        if r['state_origin']!=str(rt/parent/'result.json') or r.get('normal_play_checkpoint_eligible') is False or (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('031 native title normal ancestry')
        if any(t in (folder/'segment.lua').read_text(encoding='utf8') for t in ('emu.write','setState','AliasReads')):raise ValueError('031 native title intervention')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())));parent=folder.name
    typed=rt/(prefix+'other-eight-v1');observations=[]
    for step,length in ((1,0),(2,1),(9,8),(10,8)):
        ram=(typed/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if list(ram[0xFC44:0xFC49])!=[8,37,6,5,0] or any(struct.unpack_from('<I',ram,a)[0]!=0x0200FC60+length*2 for a in (0xFC54,0xFC58)) or ram[0xFC60:0xFC71]!=bytes.fromhex('e406')*length+b'\x98\0'*(8-length)+b'\xE5':raise ValueError('031 actual cap8 wide editor state')
        observations.append(dict(step=step,length=length,capacity=8,token_hex='e406',heading=37))
    body=bytes.fromhex('e406')*8+b'\xE5';expected_record=bytes.fromhex('03000001010602000004')+body+bytes(5)
    reg=rt/(prefix+'other-register-v1');ram=(reg/'step_004_gbaExtWorkRam.bin').read_bytes()
    if ram[0x1310:0x1330]!=expected_record:raise ValueError('031 normal native other-title registration')
    q=rt/(prefix+'other-query-v1');ram=(q/'step_005_gbaExtWorkRam.bin').read_bytes();trace=read(q/'step_005_event_buffers.json');es=trace['events'];names=[e for e in es if e['kind'] in ('name-entry','name-return')]
    if len(names)!=2 or any(e['record']!=0x02001310 or bytes.fromhex(e['record_hex'])!=expected_record for e in names) or names[1]['r0']!=16 or not bytes.fromhex(names[1]['buffer_hex']).startswith(body):raise ValueError('031 actual native boundary producer')
    copy=[e for e in es if e['kind']=='copy' and e['r0']==0x0200131A and e['r1']==0x02014E54]
    if len(copy)!=1 or copy[0]['lr']!=0x08034131 or ram[0x1310:0x1330]!=expected_record or ram[0x14E54:0x14E65]!=body or ram[0x10C40:0x10C51]!=body:raise ValueError('031 boundary record-buffer-scratch')
    ds=[d for d in trace['draws'] if 0x02010C40<=d['stream']<0x02010C50]
    if [(d['stream'],d['glyph_index'],d['offset'],d['context']) for d in ds]!=[(0x02010C40+2*i,234,10796+44*i,0x0200FA20) for i in range(8)]:raise ValueError('031 boundary eight native RAM glyphs')
    at=m['extension']['normal_font_offset']+234*96;glyph=rom[at:at+96]
    if glyph!=source[0x608758+234*96:0x608758+235*96] or struct.unpack_from('<I',rom,m['extension']['advance_offset']+234*4)[0]!=11:raise ValueError('031 native boundary actual font/metrics')
    if next(e['reads'] for e in trace['font_reads'] if e['index']==234)<8*24:raise ValueError('031 native boundary font CPU reads')
    expected={d['stream']:dict(ch='native-E406',index=234,record=glyph,id='native-other-cap8') for d in ds};proof=pixels(q,5,ds,expected,rom,m)
    cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
    if rom[cursor-0x08000000:cursor-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('031 boundary wait/clear')
    final=(q/'step_009_gbaExtWorkRam.bin').read_bytes();own=0x08000000+next(a for a in m['archives'] if a['archive']=='65A608')['rom_offset']
    if struct.unpack_from('<I',final,0xFA50)[0]!=own:raise ValueError('031 boundary normal PET return')
    deps=['tools/verify_event_native_boundary_031.py','tools/capture_event_buffers_031.py','analysis/pending_insertion_500_031_event_title_bounds_v1/cpu.json']
    screenshots=[typed/f'step_{s:03}.png' for s in (9,10,11)]+[q/f'step_{s:03}.png' for s in (5,7,9)]
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,baseline_rom=BASE,baseline_sha256=sha(rom),source_sha256=sha(source),receipts=receipts,native_editor_observations=observations,eighth_accepted=True,ninth_rejected=True,native_title_bytes=17,native_title_advance=88,normal_registration_and_query=True,glyphs=proof,wait_clear_preserved=True,normal_PET_return=True,screenshots={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in screenshots},screenshots_directly_viewed=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},new_units_applied=0,rom_written=False,release_eligible=False,limits=['Native Japanese other-title editor cap8/heading37 on actual030; NOT cap10 anniversary, friend+suffix, arbitrary imported name or new Hangul input.','Normal same-session native8 registration/display and source Japanese clock suffix, no new Korean prose or save/reload proof.']))
    print('031 actual native8 boundary/edit-cap/register/producer/font-OBJ-pixels/PET PASS; no ROM',flush=True)


if __name__=='__main__':main()
