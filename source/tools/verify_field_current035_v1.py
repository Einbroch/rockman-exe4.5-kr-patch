"""Bind normal route/clock/source payload observations; no inferred NPC pass."""
import json,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress

def main():
    rp=ROOT/'poc/output/pending500_035_v1.gba';h='41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd'
    require_hash(rp,h);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    snippets={}
    for a,b in [(0x2E292,0x2E318),(0x2E42C,0x2E438),(0x6156,0x615C),(0x61C8,0x61CC)]:
        if rom[a:b]!=source[a:b]:raise ValueError('native calendar instruction drift')
        snippets[f'{a:X}']={'end':b,'sha256':sha(source[a:b]),'hex':source[a:b].hex()}
    selected={int(x['source_archive'],16) for x in read(rp.with_suffix('.json'))['keyitem_rom']['npc035']['placements']}
    records=[]
    dirs=sorted((ROOT/'poc/runtime').glob('pending500-035-current-native-*'))+sorted((ROOT/'poc/runtime').glob('pending500-035-current-day4-*'))
    for d in dirs:
        receipt=read(d/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=h:raise ValueError('current035 normal receipt mismatch')
        for name,hh in receipt['artifacts'].items():require_hash(d/name,hh)
        item={'directory':str(d.relative_to(ROOT)),'receipt_sha256':sha((d/'result.json').read_bytes()),'frames':receipt['total_frames'],'loads':[]}
        if (d/'field_loader.json').exists():
            obs=read(d/'field_loader.json');starts=[e for e in obs['events'] if e['pc']==0x0804F724]
            if len(starts)!=obs['loads']:raise ValueError('loader event count')
            for i,e in enumerate(starts,1):
                off=e['r0']-0x08000000
                payload,_=lz77_decompress(source,off)
                dump=(d/f'load_{i:03d}_02039800.bin').read_bytes()
                if dump[:len(payload)]!=payload:raise ValueError('actual native load bytes differ')
                item['loads'].append({'source_archive':f'{off:X}','native_payload_bytes':len(payload),'payload_sha256':sha(payload),'scene':e['scene'],'sub':e['sub'],'selector':e['selector'],'selected035':off in selected})
            item['native_reader_calls']=obs['readers']
        if (d/'native_selector.json').exists():item['selector_observation']=read(d/'native_selector.json')
        records.append(item)
    out=ROOT/'analysis/pending500_035_v1/native_field_progress_v1.json'
    if out.exists():raise ValueError('refusing observation overwrite')
    report={'rom_sha256':h,'source_sha256':cfg['source_profile']['sha256'],'scope':'normal controller input on035; no state/ROM/RAM aliases or injections','native_calendar_source_snippets':snippets,'observations':records,'selected_native_loads':sum(x['selected035'] for r in records for x in r['loads']),'native_cached_reader_hits':sum(e['pc']==0x0804F76E for r in records for e in r.get('native_reader_calls',[])),'native_selector_display_pass':False,'remaining':'Connect actual NPC interaction to selected clone, font/pages, exit/reentry and timing. Load equality alone does not prove Korean display.','tools':{n:sha((ROOT/'tools'/n).read_bytes()) for n in ['capture_field_loader_035_v3.py','capture_field_loader_035_v4.py','run_field_current035_v1.py','run_field_current035_day4_v1.py','verify_field_current035_v1.py']}}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:report[k] for k in ['selected_native_loads','native_cached_reader_hits','native_selector_display_pass']},ensure_ascii=False))

if __name__=='__main__':main()
