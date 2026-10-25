"""Own030 normal calendar script50: five buffers, clear and Yes/No/B."""
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from report_roll_pet import pixels,verify_route
from bench_event_buffers_031 import BASE
from bench_event_frequency_031 import OUT as CPU

OUT='analysis/pending_insertion_500_031_calendar_delete_runtime_v1/verification.json'


def main():
    m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256']);rom=(ROOT/BASE).read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();cpu=read(CPU)
    if not cpu['passed'] or cpu['baseline_sha256']!=sha(rom) or cpu['case_count']!=50 or cpu['maximum_current_frequency_width']!=35:raise ValueError('031 calendar frequency prerequisite')
    for p,h in cpu['dependencies'].items():require_hash(ROOT/p,h)
    rt=ROOT/'poc/runtime';prefix='event-fullquick-031-delete-';receipts=[]
    ancestry=[('selector','event-buffers-031-other-register-v1'),('list',prefix+'selector-v1'),('first',prefix+'list-v1'),('confirm',prefix+'first-v1'),('no',prefix+'confirm-v1'),('cancel',prefix+'confirm-v1'),('yes',prefix+'confirm-v1')]
    for name,parent in ancestry:
        folder=rt/(prefix+name+'-v1');r=verify_route(folder,m['output_sha256'],set())
        if r['state_origin']!=str(rt/parent/'result.json') or r.get('normal_play_checkpoint_eligible') is False or (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('031 calendar normal ancestry')
        if any(t in (folder/'segment.lua').read_text(encoding='utf8') for t in ('emu.write','setState','AliasReads')):raise ValueError('031 calendar observer intervention')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
    folder=rt/(prefix+'first-v1');ram=(folder/'step_002_gbaExtWorkRam.bin').read_bytes();trace=read(folder/'step_002_event_buffers.json');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='659CB8')['rom_offset'];ctx=ram[0xFA20:0xFAF8]
    if struct.unpack_from('<I',ctx,0x30)[0]!=pool or ctx[1]!=50 or list(ctx[0x18:0x1C])!=[52,110,225,141] or struct.unpack_from('<H',ctx,100)[0]!=5:raise ValueError('031 fullquick actual root/script/default origin/five slots')
    freq=next(b for b in cpu['bodies'] if b['image']=='030' and b['frequency']==0);frequency=bytes.fromhex(freq['raw_hex']);title=bytes.fromhex('e406')*8+b'\xE5';expected_record=bytes.fromhex('03000001010602000004')+title+bytes(5)
    if ram[0x1310:0x1330]!=expected_record:raise ValueError('031 calendar current record')
    slots=[(0x10AC0,b'\0\3\xE5'),(0x10B40,b'\1\1\xE5'),(0x10BC0,bytes.fromhex('5e6ae5')),(0x10C40,frequency),(0x10CC0,title)]
    if any(ram[a:a+len(body)]!=body for a,body in slots):raise ValueError('031 all five actual resident buffers')
    expected_sequence=[(0x02010AC0,0,0),(0x02010AC1,3,32),(0x02010B40,1,120),(0x02010B41,1,164),(0x02010BC0,94,240),(0x02010BC1,106,284),(0x02010C40,2,360),(0x02010C41,freq['glyphs'][1],404),(0x02010C45,freq['glyphs'][2],452)]+[(0x02010CC0+i*2,234,10828+i*44) for i in range(8)]
    draws=trace['draws']
    if [(d['stream'],d['glyph_index'],d['offset']) for d in draws]!=expected_sequence or any(d['context']!=0x0200FA20 for d in draws):raise ValueError('031 ordered five buffer glyphs')
    korean_chars={chr(0xAC00+i-m['extension']['legacy_index_view']) for i in freq['glyphs'] if i>=m['extension']['legacy_index_view']};bdf=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],korean_chars);expected={};counts={}
    for d in draws:
        i=d['glyph_index'];a=m['extension']['normal_font_offset']+i*96;glyph=rom[a:a+96]
        if i<441:
            if glyph!=source[0x608758+i*96:0x608758+(i+1)*96]:raise ValueError('031 native calendar font')
        elif glyph!=bdf[chr(0xAC00+i-m['extension']['legacy_index_view'])]:raise ValueError('031 Korean frequency font')
        expected[d['stream']]=dict(ch='native-calendar-value',index=i,record=glyph,id='actual-five-buffers');counts[i]=counts.get(i,0)+1
    reads={d['index']:d['reads'] for d in trace['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('031 calendar font CPU reads')
    proof=pixels(folder,2,draws,expected,rom,m,origin=(52,110));cursor=struct.unpack_from('<I',ctx,0x2C)[0]
    if rom[cursor-0x08000000:cursor-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('031 calendar source wait/clear')
    confirm=rt/(prefix+'confirm-v1');im=Image.open(confirm/'step_002.png').convert('RGB');bg=im.getpixel((233,124))
    if any(im.getpixel((x,y))!=bg for y in range(124,136) for x in range(52,234)):raise ValueError('031 prior title row not cleared')
    for name,step,x in [('confirm',2,85),('no',2,131)]:
        o=(rt/(prefix+name+'-v1')/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,c=struct.unpack_from('<HHH',o,8)
        if (a&255,b&511,c&1023,c>>12,a>>14,b>>14)!=(136,x,1020,14,0,1):raise ValueError('031 actual choice cursor position/shape')
    outcomes={}
    for name,step in [('no',3),('cancel',2),('yes',2)]:
        r=(rt/(prefix+name+'-v1')/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();value=r[0x1310:0x1330]
        if value!=(bytes(32) if name=='yes' else expected_record) or r[0xFA20]!=0:raise ValueError('031 Yes/No/B record/closed dialogue')
        outcomes[name]=dict(record_deleted=name=='yes',native_dialogue_closed=True)
    deps=[CPU,'tools/verify_calendar_delete_runtime_031.py','tools/capture_event_buffers_031.py']
    screenshots=[(folder,2),(confirm,2)]+[(rt/(prefix+s+'-v1'),n) for s,n in [('no',2),('no',3),('cancel',2),('yes',2)]]
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,baseline_rom=BASE,baseline_sha256=sha(rom),source_sha256=sha(source),receipts=receipts,native_root='659CB8',script=50,origin=[52,110],dynamic_slots=5,frequency=frequency.hex(),glyphs=proof,prior_name_row_cleared_pixels=182*12,source_wait_clear=True,choice_outcomes=outcomes,screenshots={str((p/f'step_{n:03}.png').relative_to(ROOT)):sha((p/f'step_{n:03}.png').read_bytes()) for p,n in screenshots},screenshots_directly_viewed=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},product_admitted=False,rom_written=False,new_units_applied=0,release_eligible=False,limits=['Actual030 normal Rockman calendar delete50, frequency0 and native8 other-title. Source Japanese prompts/labels remain; these are not translated031 screenshots.','One same-session native allocation, five-slot residency and Yes/No/B branches, not all title/default/imported/date classes or persistence.','Representative calendar50 link only; other Navi static membership and final031 Korean aggregate layout/choice QA still required.']))
    print('031 calendar normal five-buffers/font-OBJ-pixels/clear/Yes-No-B PASS; no ROM',flush=True)


if __name__=='__main__':main()
