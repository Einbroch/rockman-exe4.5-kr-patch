"""Exact native folder consumer and active BG ownership evidence, no hook."""
import json
import struct
from build_visibility_poc import ROOT, require_hash, sha
from archive_scripts import script_spans
from chip_library_extension import decode_name
from report_fixedcell_runtime import verify_route


def main():
    build='16afa15fb530f1aded001691767f39fecb44394fab0e20760eeedd9408833241'
    source=ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba'
    require_hash(source,'588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    native=source.read_bytes()
    p=ROOT/'poc/runtime/chip-names-batch01-v1-folder-survey-v2'
    r=verify_route(p,build,set())
    if r['return_code']!=0 or not r['complete'] or list(p.glob('*failed*')):
        raise ValueError('folder observer/route failed')
    e=json.loads((p/'other_consumer_v2_environment.json').read_text())
    require_hash(ROOT/'tools/capture_chip_other_consumer.py',e['tool_sha256'])
    require_hash(ROOT/'tools/capture_chip_other_consumer_v2.py',e['adapter_sha256'])
    d=json.loads((p/'final_other_consumer.json').read_text())
    if not e['hit'] or d['alternate_calls']!=sum(row['calls'] for row in d['rows']):
        raise ValueError('alternate positive hit denominator')
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    blobs={}
    for at,size,n in [(0x765190,2437,256),(0x765B18,1103,137)]:
        pool=native[at:at+size]
        for i,blob in enumerate(script_spans(pool,n)):
            blobs[0x08000000+at+struct.unpack_from('<H',pool,i*2)[0]]=(i,blob)
    rows=[]
    for row in d['rows']:
        index,blob=blobs[row['stream']]
        if bytes.fromhex(row['text_hex'])!=blob or row['caller']!=0x0803CB7B or row['lower']!=row['upper']+16:
            raise ValueError('native folder source/caller identity')
        if row['upper'] not in range(0x0202A680,0x0202A760,32) or row['base']!=0x2010:
            raise ValueError('native folder buffer/palette/base')
        rows.append({'row':(row['upper']-0x0202A680)//32,'script':index,'source':decode_name(blob,table),'calls':row['calls']})
    io=(p/'step_002_display_io.bin').read_bytes()
    vram=(p/'step_002_gbaVideoRam.bin').read_bytes()
    display=struct.unpack_from('<H',io,0)[0]
    usage=[]
    for bg in range(4):
        ctrl=struct.unpack_from('<H',io,8+bg*2)[0]
        charbase=((ctrl>>2)&3)*0x4000
        mapbase=((ctrl>>8)&31)*0x800
        hits=[]
        blocks=[1,2,2,4][ctrl>>14]
        for cell in range(blocks*1024):
            entry=struct.unpack_from('<H',vram,(mapbase+cell*2)%0x10000)[0]
            address=0x06000000+charbase+(entry&1023)*32
            if 0x06008040<=address<0x06008EB0:
                hits.append({'map_address':0x06000000+(mapbase+cell*2)%0x10000,'tile_address':address,'entry':entry})
        usage.append({'bg':bg,'enabled':bool(display&(1<<(8+bg))),'char_base':0x06000000+charbase,
                      'screen_base':0x06000000+mapbase,'old_library_working_set_map_entries':len(hits),'samples':hits[:12]})
    out=ROOT/'analysis/exe45_chip_folder_native_runtime_v1.json'
    if out.exists():
        raise ValueError('refuse report overwrite')
    report={'rom_sha256':build,'status':'PASS native folder consumer/source/row ABI observation; Korean folder names NOT implemented',
            'result_sha256':sha((p/'result.json').read_bytes()),'calls':d['alternate_calls'],'rows':rows,'bg_ownership':usage,
            'finding':'Folder BG0 charbase is 06008000, but this sample has no active map entries to library working cells. Nonzero bytes do not prove ownership or vacancy; dynamic load/reference/lifetime survey remains required before allocation.',
            'old_bank_nonzero_bytes':sum(bool(b) for b in vram[0x8040:0x8EB0]),
            'excluded_attempt':'folder-survey v1 observer wrongly paired native empty-row bypass with parser return; v2 excludes confirmed 0803CB62 branch',
            'rejected_hypothesis':'BG0 charbase alone was hypothesized to imply active old-bank references; actual map scan found zero, so that claim is rejected',
            'limits':['single tilemap snapshot is not whole-route ownership or globally-free proof','no new hook or allocation',
                      'root-selector zero hits are negative observation for this route, not unreachability']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS native folder rows',rows,'old library bank active BG map references',[(u['bg'],u['old_library_working_set_map_entries']) for u in usage if u['enabled']])


if __name__=='__main__':
    main()
