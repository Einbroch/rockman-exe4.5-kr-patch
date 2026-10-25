"""Verify exact retained BG/VRAM/screenshot folder-name samples."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from fixedcell_font import bdf_cells,unpack_pixels
from report_chip_library_runtime import read,require
from chip_library_extension import decode_name
from report_fixedcell_runtime import verify_route


def visible_folder(path,step,rows,cells,native,table):
    prefix=f'step_{step:03d}'
    video=(path/f'{prefix}_gbaVideoRam.bin').read_bytes()
    io=(path/f'{prefix}_display_io.bin').read_bytes()
    trace=read(path/f'{prefix}_chip_ko.json')
    shot=Image.open(path/f'{prefix}.png').convert('RGB')
    ctrl=struct.unpack_from('<H',io,10)[0]
    require(((ctrl>>2)&3)==1 and ((ctrl>>8)&31)==29 and not ctrl&0xC080,'folder BG geometry')
    require(video[0x4200:0x6600]==native[0x601738:0x603B38],'folder native resident font changed')
    records=[]
    for row,text in rows.items():
        found=[r for r in trace['rows'] if r['upper']==0x0202A680+row*32 and decode_name(bytes.fromhex(r['text_hex']),table)==text]
        require(bool(found),'missing folder parser-return row')
        buffered=[bytes.fromhex(found[-1][k]) for k in ('top_hex','bottom_hex')]
        for col in range(8):
            entries=[struct.unpack_from('<H',video,0xE800+(5+row*2+dy)*64+(14+col)*2)[0] for dy in (0,1)]
            require(entries==[struct.unpack_from('<H',buffered[dy],col*2)[0] for dy in (0,1)],'folder BG/returned-map mismatch')
            if col>=len(text):
                require(entries==[0,0],'folder padding not cleared')
                continue
            ch=text[col]
            if ch in cells:
                tile=514+row*16+col*2;glyph=cells[ch]
            else:
                code=next(k for k,v in table.items() if v==ch)
                tile=16+code*2;glyph=native[0x601738+code*64:0x601738+code*64+64]
            require(entries==[0x2000+tile,0x2001+tile],'folder Hangul/native +16/palette mapping')
            actual=b''.join(video[0x4000+(e&1023)*32:0x4000+(e&1023)*32+32] for e in entries)
            require(actual==glyph,'folder actual glyph residency')
            pixels=unpack_pixels(actual);colors=[]
            for role in (1,2):
                mask={(x,y) for y in range(16) for x in range(8) if pixels[y][x]==role}
                require(bool(mask),'empty folder ink/shadow')
                observed={shot.getpixel(((14+col)*8+x,(5+row*2)*8+y)) for x,y in mask}
                require(len(observed)==1,'folder screenshot color mismatch')
                color=next(iter(observed))
                measured={(x,y) for y in range(16) for x in range(8) if shot.getpixel(((14+col)*8+x,(5+row*2)*8+y))==color}
                require(measured==mask,'folder screenshot ink/shadow pixel mask')
                colors.append(color)
            require(colors[0]!=colors[1],'folder ink/shadow contrast')
            records.append({'row':row,'column':col,'character':ch,'glyph_sha256':sha(actual),'pixel_masks_match':True})
    return records


def main():
    build='6790782b403f07f5f850cb985e6aedf012dc8334736b4f9988e4f74379a6fd41'
    m=read(ROOT/'poc/output/exe45_ko_development_chip_folder_v2.json')
    for suffix in ('','_repro'):
        require_hash(ROOT/f'poc/output/exe45_ko_development_chip_folder_v2{suffix}.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename']
    require_hash(source,m['source_sha256'])
    native=source.read_bytes()
    p=ROOT/'poc/runtime/chip-folder-v2-normal'
    r=verify_route(p,build,set())
    require(r['return_code']==0 and not list(p.glob('*failed*')),'folder route fault')
    e=read(p/'folder_qa_environment.json')
    require_hash(ROOT/'tools/capture_chip_folder_qa.py',e['tool_sha256'])
    require(e['passed'],'folder observer failed')
    f=m['fixedcell_extension']
    cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    pixels={step:visible_folder(p,step,rows,cells,native,table) for step in (8,9,12)}
    empty=(p/'step_011_gbaVideoRam.bin').read_bytes()
    require(all(struct.unpack_from('<H',empty,0xE800+(5+row*2+dy)*64+(14+col)*2)[0]==0 for row in range(7) for dy in (0,1) for col in range(8)),'empty-list stale map')
    c=read(p/'final_folder_cache.json')
    copies=read(p/'final_chip_ko.json')['verified_word_copies']
    require(c['checks']==c['hits']+copies and copies==17 and c['resets']==1,'normal cold-copy/reset denominator')
    out=ROOT/'analysis/exe45_chip_folder_pixels_v2.json'
    require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded normal folder glyph/palette/bias/padding/cache pixels; broader regression pending',
        'result_sha256':sha((p/'result.json').read_bytes()),'visible_names':pixels,'empty_step':11,'cache':c,'copies':copies,
        'limits':['folder/library/name-input exit and reentry pending','changing 56-cell timing pending','99 draft units, not new wording approval or release QA']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS folder real Hangul/digit pixel masks, empty clear and left-return:',c)


if __name__=='__main__':
    main()
