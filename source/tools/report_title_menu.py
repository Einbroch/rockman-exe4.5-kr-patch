"""Exact title artifact: native decompression, transfer, resident tiles and states."""
import json
import argparse
import struct
from build_visibility_poc import ROOT, sha
from verify_tpi_index import lz77_decompress
from title_menu_graphics import BASE, STORED, decode


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--weekend',action='store_true');args=parser.parse_args()
    product_stem='exe45_ko_development_weekend_menu_v1' if args.weekend else 'exe45_ko_development_title_menu_v1'
    prefix='weekend-menu-v1' if args.weekend else 'title-menu-v1'
    rompath=ROOT/f'poc/output/{product_stem}.gba'
    product=rompath.read_bytes()
    previous=(ROOT/('poc/output/exe45_ko_development_title_menu_v1.gba' if args.weekend else 'poc/output/exe45_ko_development_save_keyboard_fonts_v1.gba')).read_bytes()
    manifest=json.loads(rompath.with_suffix('.json').read_text(encoding='utf-8'))
    if sha(product)!=manifest['output_sha256'] or len(product)!=len(previous):
        raise ValueError('Exact artifact mismatch')
    if any(a!=b and not BASE<=i<BASE+STORED for i,(a,b) in enumerate(zip(product,previous))):
        raise ValueError('Prior cumulative content changed')
    payload,_=lz77_decompress(product,BASE)
    if args.weekend:
        old_payload,_=lz77_decompress(previous,BASE)
        if any(decode(old_payload,col)!=decode(payload,col) for col in (0,10)):
            raise ValueError('Prior new-game/continue pixels changed')
    observer=ROOT/f'poc/runtime/{prefix}-observer'
    if (observer/'native_title_decompressed.bin').read_bytes()!=payload:
        raise ValueError('Native decompression differs')
    copy=json.loads((observer/'native_title_copy.json').read_text())
    if copy!={'source':0x0201C004,'destination':0x06010800,'bytes':1664}:
        raise ValueError('Native transfer ABI mismatch')
    artifacts={}
    states=[]
    for folder,steps in [(prefix+'-nosave',[2,3]),(prefix+'-withsave',[2,3,4,5,6] if args.weekend else [2,3,4]),
                         (prefix+'-observer',[2,3] if args.weekend else [2])]:
        base=ROOT/'poc/runtime'/folder
        receipt=json.loads((base/'result.json').read_text())
        if receipt['rom_sha256']!=sha(product) or not receipt['complete'] or receipt['return_code']!=0:
            raise ValueError('Incomplete or mismatched runtime')
        if receipt['state_origin'] is not None:
            raise ValueError('Must cross title loader from cold boot')
        artifacts[str((base/'result.json').relative_to(ROOT))]=sha((base/'result.json').read_bytes())
        for step in steps:
            stem=f'step_{step:03d}'
            video=(base/(stem+'_gbaVideoRam.bin')).read_bytes()
            if video[0x10800:0x10800+1664]!=payload[4:]:
                raise ValueError('Entire native resident sheet mismatch')
            oam=(base/(stem+'_gbaSpriteRam.bin')).read_bytes()
            objects=[struct.unpack_from('<HHH',oam,i*8) for i in range(128)]
            labels=[]
            for column in ([0,10,16] if args.weekend else [0,10]):
                entries=[(a,b,c) for a,b,c in objects if (c&1023)==0x40+column and (a&0x300)!=0x200]
                # No-save displays only new-game (native placement differs).
                if column!=0 and folder==prefix+'-nosave':
                    continue
                if not entries:
                    raise ValueError('Menu OBJ consumer missing')
                if folder==prefix+'-withsave':
                    selected_column=({2:10,3:0,4:10,5:16,6:10}[step] if args.weekend else (0 if step==3 else 10))
                    if entries[0][2]>>12!=(2 if column==selected_column else 3):
                        raise ValueError('Focused/unfocused palette transition differs')
                labels.append(dict(column=column,attributes=list(entries[0])))
            states.append(dict(folder=folder,step=step,labels=labels))
            for suffix in ['.png','_gbaVideoRam.bin','_gbaSpriteRam.bin','_gbaPaletteRam.bin']:
                p=base/(stem+suffix);artifacts[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    for filename in ['native_title_decompressed.bin','native_title_copy.json']:
        p=observer/filename;artifacts[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    if (ROOT/f'poc/output/{product_stem}_repro.gba').read_bytes()!=product:
        raise ValueError('Primary rebuild differs')
    for folder,step in [(prefix+'-nosave',4),(prefix+'-withsave',7 if args.weekend else 5)]:
        p=ROOT/f'poc/runtime/{folder}/step_{step:03d}.png';artifacts[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    if args.weekend:
        for step in (4,5):
            p=observer/f'step_{step:03d}.png';artifacts[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    report=dict(schema=1,rom_sha256=sha(product),title_menu_verified=True,
                native_decompression_equal=True,native_vram_copy=copy,
                prior_cumulative_rom_bytes_preserved=True,title_states=states,
                weekend_menu_verified=args.weekend,
                weekend_focused_palette_verified=args.weekend,
                weekend_entry_transition_observed=args.weekend,
                primary_rebuild_byte_identical=True,
                no_save_new_game_transition_observed=True,
                saved_continue_transition_observed=True,
                screenshots_assistant_inspected=True,
                fresh_process_reload_verified=False,
                limits=['Title labels only; no new native save was committed in this regression.',
                        'Continue seeded with prior exact baseline native SAV; only title graphics differ.',
                        'Automatic Hangul keyboard and full translation integration remain incomplete.'],
                artifacts=artifacts)
    out=observer/'verification.json'
    if out.exists():raise ValueError('Preserve evidence')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS title native LZ/VRAM/OBJ/menu transitions and cumulative scope')


if __name__=='__main__':main()
