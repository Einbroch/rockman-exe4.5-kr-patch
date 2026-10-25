"""Own030 normal calendar registration -> producer -> RAM Hangul -> OBJ/pixels."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from report_roll_pet import pixels,verify_route
from korean_codec import encode_hangul
from bench_event_buffers_031 import BASE,OUT as CPU

OUT='analysis/pending_insertion_500_031_event_runtime_v1/verification.json'
PREFIX='event-buffers-031-'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256'])
    rp=ROOT/BASE;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cpu=read(CPU)
    if not cpu['passed'] or cpu['cases']!=3024 or cpu['baseline_sha256']!=sha(rom):raise ValueError('031 event CPU prerequisite')
    for p,h in cpu['dependencies'].items():require_hash(ROOT/p,h)
    receipts=[];rt=ROOT/'poc/runtime';parent='pending500-030-v1-complete'
    for suffix in ('calendar','time','meal-register','meal-query'):
        folder=rt/(PREFIX+suffix+'-v1');r=verify_route(folder,m['output_sha256'],set())
        if r['state_origin']!=str(rt/parent/'result.json') or not r.get('normal_play_checkpoint_eligible',True) or (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('031 normal same-ROM ancestry')
        lua=(folder/'segment.lua').read_text(encoding='utf8')
        if any(s in lua for s in ('emu.write','setState','AliasReads')):raise ValueError('031 event intervention')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
        parent=folder.name
    body=encode_hangul('식사')+b'\xE5';preset=0x08000000+next(a for a in m['archives'] if a['archive']=='6368E8')['rom_offset']
    if struct.unpack_from('<I',rom,0x32AD8)[0]!=preset:raise ValueError('031 actual preset table pointer')
    address=preset+struct.unpack_from('<H',rom,preset-0x08000000+124)[0]
    if rom[address-0x08000000:address-0x08000000+len(body)]!=body:raise ValueError('031 actual preset bytes')
    reg=rt/(PREFIX+'meal-register-v1');events=read(reg/'step_007_event_buffers.json')['events']
    copies=[e for e in events if e['kind']=='copy']
    if [(e['r0'],e['r1']) for e in copies]!=[(address,0x02026080),(0x02026080,0x0200131A)]:raise ValueError('031 native preset lookup/commit')
    record=bytes.fromhex('03000001010602000002')+body+bytes(13)
    if (reg/'step_007_gbaExtWorkRam.bin').read_bytes()[0x1310:0x1330]!=record:raise ValueError('031 native committed calendar record')
    q=rt/(PREFIX+'meal-query-v1');data=read(q/'step_005_event_buffers.json');ram=(q/'step_005_gbaExtWorkRam.bin').read_bytes();events=data['events']
    if [e['kind'] for e in events]!=['copy','F90C-entry','name-entry','copy','name-return','F90C-entry']:raise ValueError('031 ordered actual name producer/reader')
    entry,copy,returned,reader=events[2:]
    if any(e['record']!=0x02001310 or bytes.fromhex(e['record_hex'])!=record for e in events):raise ValueError('031 native current-record lifetime')
    if (copy['r0'],copy['r1'],copy['lr'])!=(0x0200131A,0x02014E54,0x08034131) or returned['r0']!=8:raise ValueError('031 name copy exact source/target/return')
    if bytes.fromhex(returned['buffer_hex'])!=body+bytes(23) or reader['buffer_hex']!=returned['buffer_hex'] or not entry['frame']<=copy['frame']<=returned['frame']<reader['frame']:raise ValueError('031 producer-to-descriptor lifetime')
    pool=0x08000000+next(a for a in m['archives'] if a['archive']=='65B8E4')['rom_offset']
    if any(e['root']!=pool for e in events) or rom[entry['r4']-0x08000000:entry['r4']-0x08000000+4]!=bytes.fromhex('fc032d00') or rom[reader['r4']-0x08000000:reader['r4']-0x08000000+3]!=bytes.fromhex('f90c43'):raise ValueError('031 actual Rockman command streams')
    if ram[0x1310:0x1330]!=record or ram[0x14E54:0x14E74]!=body+bytes(23) or ram[0x10C40:0x10C60]!=body+bytes(23):raise ValueError('031 record/descriptor/scratch residency')
    ds=[d for d in data['draws'] if 0x02010C40<=d['stream']<0x02010C48];font=m['extension'];glyphs=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],set('식사'));expected={}
    if [(d['stream'],d['offset'],d['context']) for d in ds]!=[(0x02010C40,10796,0x0200FA20),(0x02010C44,10844,0x0200FA20)]:raise ValueError('031 ordered two Hangul RAM glyphs')
    for ch,d in zip('식사',ds):
        index=font['legacy_index_view']+ord(ch)-0xAC00;glyph=rom[font['normal_font_offset']+index*96:font['normal_font_offset']+(index+1)*96]
        if d['glyph_index']!=index or glyph!=glyphs[ch] or struct.unpack_from('<I',rom,font['advance_offset']+index*4)[0]!=12:raise ValueError('031 actual font/advance')
        expected[d['stream']]=dict(ch=ch,index=index,record=glyph,id='native-calendar-meal')
    reads={d['index']:d['reads'] for d in data['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in Counter(d['glyph_index'] for d in ds).items()):raise ValueError('031 actual font CPU consumption')
    proof=pixels(q,5,ds,expected,rom,m)
    cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
    if rom[cursor-0x08000000:cursor-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('031 source wait/clear boundary')
    final=(q/'step_009_gbaExtWorkRam.bin').read_bytes();own=0x08000000+next(a for a in m['archives'] if a['archive']=='65A608')['rom_offset']
    if struct.unpack_from('<I',final,0xFA50)[0]!=own:raise ValueError('031 normal PET return')
    screenshots=[rt/(PREFIX+s+'-v1')/f'step_{step:03}.png' for s,step in [('calendar',6),('time',6),('meal-register',7),('meal-query',5),('meal-query',7),('meal-query',9)]]
    deps=[CPU,'tools/bench_event_buffers_031.py','tools/capture_event_buffers_031.py','tools/verify_event_buffers_031.py','tools/run_mesen_segment.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(sp.read_bytes()),baseline_rom=BASE,baseline_sha256=sha(rom),policy='normal controller registration/query on own030; NON-DISTRIBUTION',receipts=receipts,producer=dict(record=0x02001310,name_offset=10,name_bytes=9,buffer=0x02014E54,scratch=0x02010C40,descriptor=67,native_copy_bytes=32,record_preserved=True,producer_to_reader_same_bytes=True),glyphs=proof,wait_clear_preserved=True,normal_PET_return=True,screenshots={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in screenshots},dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,product_admitted=False,release_eligible=False,limits=['One native same-session Rockman meal registration/query; not all Navi callers, event classes, generated suffix names or 10glyph GBA boundary.','The two Korean glyphs were already in030. Source Japanese clock suffix remains visible; no new031 prose applied.','CPU time-value tests do not prove all printed time widths or RTC correctness.','No Hangul keyboard commit/save/reload or full-game proof.']))
    print('PASS031 actual030 preset-record-producer-descriptor-scratch-font-OBJ-pixels/wait/PET return; no new ROM',flush=True)


if __name__=='__main__':main()
