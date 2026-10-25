"""Two exact030 native opponent-chip display diagnostics, not031 admission."""
import struct
from collections import Counter
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from report_roll_pet import pixels
from bench_opponent_chips_031 import BASE,FIELDS,OUT as CPU

OUT='analysis/pending_insertion_500_031_opponent_chip_runtime_v1/verification.json'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/BASE;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cpu=read(CPU)
    if not cpu['passed'] or cpu['case_count']!=1580 or cpu['baseline_sha256']!=sha(rom):raise ValueError('031 actual producer CPU prerequisite')
    require_hash(ROOT/'tools/bench_opponent_chips_031.py',cpu['tool_sha256']);census=read(cpu['census']['path']);require_hash(ROOT/cpu['census']['path'],cpu['census']['sha256'])
    fixture=next(r for r in census['names'] if r['chip_id']==9);encoded=bytes.fromhex(fixture['raw_hex']);font=m['extension']['normal_font_offset']
    if len(encoded)!=9 or fixture['advance']!=88:raise ValueError('031 native max fixture')
    for r in cpu['native_ranges']:
        a,n=r['offset'],r['bytes']
        if sha(source[a:a+n])!=r['sha256'] or rom[a:a+n]!=source[a:a+n]:raise ValueError('031 native code/data applicability')
    own=0x08000000+next(a for a in m['archives'] if a['archive']=='65A608')['rom_offset'];pool=0x08000000+next(a for a in m['archives'] if a['archive']=='65CC78')['rom_offset']
    pages=[];receipts=[];sheet=Image.new('RGB',(720,360),'#20232a');draw=ImageDraw.Draw(sheet)
    for row,(short,name,script,offset) in enumerate((('lost','printMostLostToOpponentsChip',62,10752),('defeated','printMostDefeatedOpponentsChip',71,0))):
        folder=ROOT/'poc/runtime'/('opponent-chip-031-'+short+'-v1');r=read(folder/'result.json')
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] or (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('031 diagnostic quarantine')
        for p,h in r['artifacts'].items():require_hash(folder/p,h)
        if r['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('031 exact root/table alias')
        events=read(folder/'step_003_profile_trace.json')['events'];field=FIELDS[name]['record']+1
        if len(events)!=1 or events[0]['field']!=field or events[0]['cap']!=8 or not events[0]['restored'] or not bytes.fromhex(events[0]['hex']).startswith(encoded):raise ValueError('031 actual native reader/record restoration')
        event=events[0];trace=read(folder/'step_003_roll_pet.json');start=event['output'];ds=[d for d in trace['draws'] if start<=d['stream']<start+len(encoded)-1]
        if [(d['stream']-start,d['glyph_index'],d['offset'],d['context']) for d in ds]!=[(i,ch,offset+44*i,0x0200FA20) for i,ch in enumerate(encoded[:-1])]:raise ValueError('031 all eight RAM glyphs/offsets')
        expected={}
        for i,ch in enumerate(encoded[:-1]):
            glyph=rom[font+ch*96:font+(ch+1)*96]
            if glyph!=source[0x608758+ch*96:0x608758+(ch+1)*96] or struct.unpack_from('<I',rom,m['extension']['advance_offset']+ch*4)[0]!=11:raise ValueError('031 native glyph bytes/metric')
            expected[start+i]=dict(ch='native-chip',index=ch,record=glyph,id=name)
        counts=Counter(encoded[:-1]);reads={e['index']:e['reads'] for e in trace['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('031 native chip font CPU reads')
        proof=pixels(folder,3,ds,expected,rom,m,origin=(92,110))
        for step in (3,5):
            ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if ram[0xFA21]!=0 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or rom[cursor-0x08000000:cursor-0x08000000+2]!=b'\xE6\x00':raise ValueError('031 source waited page')
        ram=(folder/'step_007_gbaExtWorkRam.bin').read_bytes()
        if struct.unpack_from('<I',ram,0xFA50)[0]!=own:raise ValueError('031 normal PET return')
        for col,step in enumerate((3,5,7)):
            im=Image.open(folder/f'step_{step:03}.png').convert('RGB');sheet.paste(im,(col*240,row*180+20));draw.text((col*240+4,row*180+3),short+' '+str(step),fill='white')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
        pages.append(dict(provider=name,script=script,field=field,native_chip_id=9,native_glyphs=8,native_advance=88,reader_record_restored=True,ordered_two_source_waits=True,normal_PET_return=True,**proof))
    target=ROOT/OUT;target.parent.mkdir(parents=True,exist_ok=False);sheet.save(target.parent/'contact.png')
    paths=[CPU,'tools/verify_opponent_chip_031.py','tools/capture_opponent_chip_031.py']
    frozen_write(target,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),pages=pages,receipts=receipts,contact=dict(path=str((target.parent/'contact.png').relative_to(ROOT)),sha256=sha((target.parent/'contact.png').read_bytes()),screens=6),dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},screenshot_directly_viewed=False,product_admitted=False,rom_written=False,release_eligible=False,limits=['Own030 normal checkpoint with quarantined GutsMan62/71 read aliases on ownRockman host. Native chip9 records temporarily seeded at F90C and restored before rendering.','All eight chip RAM glyphs/fontCPU/OBJ/pixels and two original Japanese waited pages/return; NOT new Korean031 prose or all aggregate layouts.','393name native producerCPU is separate. No natural multiplayer acquisition/packet/player-name bound, complete histories/default/import/save state audit, Hangul or release claim.']))
    print('PASS031 two native opponent-chip paths/RAM-font-OBJ-pixels/source waits/PET return; no ROM written')

if __name__=='__main__':main()
