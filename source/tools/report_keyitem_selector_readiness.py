"""Analysis receipts only; never builds or modifies a ROM."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import lz77_decompress
from report_roll_pet import verify_route

STEM='exe45_ko_development_possessions_statistics_v1'
def main():
    out=ROOT/'analysis/keyitem_selector_readiness_v1'
    if out.exists():raise ValueError('preserve analysis evidence')
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba';require_hash(source,m['source_sha256']);original=source.read_bytes()
    cpu=ROOT/'analysis/keyitem_rom_selector_probe_v1_r2/report.json';bench=json.loads(cpu.read_text(encoding='utf8'))
    if not bench['passed'] or bench['vectors']!=624 or bench['baseline_rom_sha256']!=sha(rom):raise ValueError('CPU evidence baseline')
    root=struct.unpack_from('<I',rom,0x34a2c)[0];payload,_=lz77_decompress(rom,root-0x08000000)
    rt=ROOT/'poc/runtime/keyitem-residency-v1-ui-positive'
    route=verify_route(rt,sha(rom),set())
    env=json.loads((rt/'key_residency_environment.json').read_text(encoding='utf8'))
    if not env['observer_only'] or env['self_sha256']!=sha((ROOT/'tools/capture_keyitem_residency.py').read_bytes()):raise ValueError('observer provenance')
    lua=(rt/'segment.lua').read_text(encoding='utf8')
    if any(x in lua for x in ['emu.write','setState','AliasReads']):raise ValueError('intervention')
    events=json.loads((rt/'step_008_key_residency.json').read_text(encoding='utf8'))['events']
    if [x['kind']for x in events]!=['ui-loader','decompress','lookup']*2:raise ValueError('entry/reentry observation')
    for x in events:
        r=x['registers']
        if x['kind']=='decompress' and (r['r0'],r['r1'],r['r14'])!=(root,0x02020800,0x080349F1):raise ValueError('native loader')
        if x['kind']=='lookup' and (r['r0'],r['r1'],r['r14'])!=(0x02020800,32,0x0803497F):raise ValueError('native lookup guard')
    pages=[]
    for step in [4,5,8]:
        p=rt/f'step_{step:03d}_gbaExtWorkRam.bin';ram=p.read_bytes()
        if ram[0x20800:0x20800+len(payload)]!=payload or ram[0xFA21]!=32 or struct.unpack_from('<I',ram,0xFA50)[0]!=0x02020800:raise ValueError('native RAM payload/root/script')
        pages.append(dict(step=step,ram_sha256=sha(ram),payload_bytes=len(payload),header_hex=payload[:16].hex(),script=32))
    # Exact source revision: FC03 dispatch table, item-count handler, and
    # callee's ldrb (not the command's uint8 item argument) bound result.
    checks={0x51e74:struct.pack('<I',0x0805258C),0x5258c+0x31*4:struct.pack('<I',0x08034851),
            0x34850:bytes.fromhex('00b5fbf751fd014b186000bd'),0x3485c:struct.pack('<I',0x0200FA6C),
            0x30314:bytes.fromhex('085c004200bd'),0x3031a:bytes.fromhex('002000bd')}
    for at,b in checks.items():
        if original[at:at+len(b)]!=b:raise ValueError('count source proof '+hex(at))
    draft=ROOT/'analysis/keyitem_translation_draft_v1/draft.json';require_hash(draft,bench['draft_sha256'])
    units=json.loads(draft.read_text(encoding='utf8'))['units']
    codes={v:bytes.fromhex(k)for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()if '='in line for k,v in [line.split('=',1)]if len(v)==1}
    bias=m['extension']['legacy_index_view'];adv=m['extension']['advance_offset'];font=m['extension']['normal_font_offset']
    def width(text):
        n=0
        for ch in text:
            idx=ord(ch)-0xAC00+bias if '\uac00'<=ch<='\ud7a3' else codes[ch][0]
            if len(rom[font+idx*96:font+(idx+1)*96])!=96:raise ValueError('missing glyph record')
            n+=struct.unpack_from('<I',rom,adv+idx*4)[0]
        return n
    quantities=[]
    for script in [6,7,16,17,18]:
        selected=[u for u in units if int(u['id'].split(':')[1])==script]
        prefix=selected[0]['translation'].split('\n')[-1];suffix=selected[1]['translation']
        values=[dict(value=n,text=prefix+str(n)+suffix,width_px=width(prefix+str(n)+suffix))for n in range(256)]
        quantities.append(dict(script=script,all_256_values_checked=True,max_width_px=max(v['width_px']for v in values),examples=[values[i]for i in [0,9,10,99,100,255]]))
    result=dict(analysis_only=True,rom_modified=False,new_translation_units_applied=0,release_eligible=False,
        baseline_rom_sha256=sha(rom),source_sha256=sha(original),cpu_report_sha256=sha(cpu.read_bytes()),cpu_vectors=624,
        runtime_scope='Unmodified latest product; normal empty-keyitem entry, hold and B/reentry. No selector execution in GBA.',
        route=route,events=events,pages=pages,normal_ui_guard_preconditions_observed=True,
        second_consumer_normal_route_reached=False,absence_is_not_dead_code_proof=True,
        quantity_static_proof=dict(command='FC0331',table=0x0805258C,handler=0x08034850,count_function=0x080302F8,
            unsigned_byte_load=0x08030314,unavailable_returns_zero=0x0803031A,buffer_word=0x0200FA6C,range=[0,255],
            checked_source_bytes={hex(k):v.hex()for k,v in checks.items()},quantity_line_widths=quantities,
            limit='Static storage/advance bound only; printBuffer formatting and renderer geometry still require execution.'),
        pending=['Primary immutable-source builder integration and exact final-hook verification.',
            'All39 wording/glossary and dynamic renderer/quantity layout review.',
            'New-ROM native runtime and second-consumer/fallback regression.',
            'Whole-project Hangul input/edit/commit/redisplay/persistent reload/old-save compatibility.'])
    out.mkdir();(out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(normal_ui_guard_preconditions_observed=True,quantity_range=[0,255],quantity_max_widths=[x['max_width_px']for x in quantities],rom_modified=False)))
if __name__=='__main__':main()
