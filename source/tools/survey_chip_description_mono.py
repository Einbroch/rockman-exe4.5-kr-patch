"""Bind observed native descriptions to source scripts and mono staging bytes."""
import json
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import parse_tpi
from archive_scripts import script_spans
from tpl_literals import literals
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require


def main():
    m=read(ROOT/'poc/output/exe45_ko_development_chip_folder_v3.json');build=m['output_sha256']
    rom=ROOT/'poc/output/exe45_ko_development_chip_folder_v3.gba';require_hash(rom,build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256'])
    native=source.read_bytes();row=next(r for r in parse_tpi(ROOT/'external/textpet-indexes/exe45.tpi') if r['offset']==0x76937C)
    require(not row['compressed'] and not row['size_header'],'description native pool encoding')
    at=row['offset'];payload=native[at:at+row['size']]
    require(rom.read_bytes()[at:at+len(payload)]==payload,'description pool changed')
    spans=script_spans(payload,256);offsets=[struct.unpack_from('<H',payload,i*2)[0] for i in range(256)]
    texts={int(l.key.split(':')[1]):l.text for l in literals((ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig'))}
    records=[];seen=set();p=ROOT/'poc/runtime/chip-folder-v3-normal-r1';verify_route(p,build,seen)
    for step in (8,9,12):
        calls=read(p/f'step_{step:03d}_fixedcells.json')['calls']
        for c in calls:
            if c['font']!=0x08619EF8 or c['id'] in {r['call_id'] for r in records}: continue
            require(c['complete'] and c['width']==10 and c['height']==3 and c['bytes']==1920,'mono geometry')
            script_offset=c['stream']-0x08000000-at
            require(script_offset in offsets,'description stream not script start')
            script=offsets.index(script_offset)
            require(c['prefix_hex'].startswith(spans[script][:min(64,len(spans[script]))].hex().upper()),'description bytes do not match source')
            stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();deltas=set()
            for g in c['glyphs']:
                require(g['font']==0x08619EF8 and 0<=g['index']<448,'mono native glyph bounds')
                off=g['destination']-c['copy_source'];require(0<=off<=len(stage)-64 and off%64==0,'mono stage cell bounds')
                expected=native[0x619EF8+g['index']*64:0x619EF8+(g['index']+1)*64]
                actual=stage[off:off+64]
                for i in range(0,64,4):
                    deltas.add((struct.unpack_from('<I',actual,i)[0]-struct.unpack_from('<I',expected,i)[0])&0xFFFFFFFF)
            require(len(deltas)==1,'native mono copier word-add transform inconsistent')
            records.append({'call_id':c['id'],'script':script,'source_text':texts.get(script),
                'stream':c['stream'],'width':10,'height':3,'stage_bytes':1920,'copy_target':c['copy_target'],
                'glyphs_verified':len(c['glyphs']),'word_add_tint':next(iter(deltas)),
                'stage_sha256':sha(stage),'source_script_sha256':sha(spans[script])})
    require(records,'missing mono positive evidence')
    bank=native[0x619EF8:0x620EF8]
    roles=Counter(n for b in bank for n in (b&15,b>>4))
    out=ROOT/'analysis/exe45_chip_description_mono_native_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'source_sha256':m['source_sha256'],
        'status':'native description source/script/mono staging verified; Hangul implementation pending',
        'pool':row,'pool_sha256':sha(payload),'font':{'start':0x619EF8,'bytes':len(bank),'glyphs':448,'glyph_bytes':64,'sha256':sha(bank),'nibble_counts':dict(roles)},
        'runtime_result_sha256':sha((p/'result.json').read_bytes()),'calls':records,
        'limits':['nibble counts are not palette role approval','sprite palette/actual scanout and full-text consumer population pending',
                  'existing F9FC provider only supplies big-font roles, not safe for translated mono input']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('native mono descriptions:',[(r['script'],r['glyphs_verified'],hex(r['copy_target'])) for r in records])


if __name__=='__main__':
    main()
