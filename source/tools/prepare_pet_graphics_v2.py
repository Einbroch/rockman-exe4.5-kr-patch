"""Convert corrected imagegen lettering into source-preserving native 4bpp tiles.

No icons/frames/colors from the generated canvas are adopted. Only its measured
letter masks are converted to the native 8px text band with palette role 4.
"""
import argparse,json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash

TILES=[(0x84,0x8C),(0xA4,0x9C),(0xB0,0xB8),(0xC4,0xCC),(0xD8,0xE0),(0xEC,0xF4),(0x100,0x108)]
BASE=0x6303B8

def decode(block,left,right):
    return [[(block[(tile-0x80)*32+(y%8)*4+(x%8)//2]>>(4*(x%2)))&15
        for x in range(64) for tile in [((left,right)[x//32]+y//8*4+(x%32)//8)]] for y in range(16)]

def encode(block,pixels,left,right):
    for y,row in enumerate(pixels):
        for x,role in enumerate(row):
            tile=(left,right)[x//32]+y//8*4+(x%32)//8
            at=(tile-0x80)*32+(y%8)*4+(x%8)//2;shift=4*(x%2)
            block[at]=(block[at]&~(15<<shift))|(role<<shift)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--version',type=int,default=2);ap.add_argument('--threshold',type=int,default=112);args=ap.parse_args()
    if args.version<2 or not 1<=args.threshold<=255:raise ValueError('format parameters')
    out=ROOT/f'translations/pet_graphics_v{args.version}'
    if out.exists():raise ValueError('fresh output required')
    inv=json.loads((ROOT/'analysis/pet_labels_v1/inventory.json').read_text())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,inv['source_sha256'])
    block=source.read_bytes()[BASE:BASE+0x1200];target=bytearray(block)
    candidate=ROOT/'analysis/pet_labels_v1/candidate_02_tongsin.png';im=Image.open(candidate).convert('RGBA')
    if im.size!=(1160,1355):raise ValueError('corrected image applicability')
    palette=(ROOT/'poc/runtime/roll-tactics-v1-cold-part2/step_040_gbaPaletteRam.bin').read_bytes()
    atlas=Image.new('RGBA',(64,112));units=[]
    for row,(left,right) in enumerate(TILES):
        original=decode(block,left,right);roundtrip=bytearray(block);encode(roundtrip,original,left,right)
        if roundtrip!=block:raise ValueError('unchanged roundtrip')
        clean=[list(r) for r in original]
        for y in range(1,9):
            for x in range(1,64):
                if original[y][x] not in (1,4):raise ValueError('background/letter roles')
                clean[y][x]=1
        top=[20,215,412,610,810,1008,1205][row]
        mask=Image.new('L',(850,92))
        for y in range(92):
            for x in range(850):
                r,g,b,a=im.getpixel((210+x,top+y))
                if a>=240 and r>=90 and g>=145 and b>=145:mask.putpixel((x,y),255)
        bbox=mask.getbbox()
        if bbox is None:raise ValueError('empty generated lettering')
        width=[32,32,16,63,16,16,16][row]
        # Native-format sampling of the adopted letter mask, not generated frame art.
        small=mask.crop(bbox).resize((width,8),Image.Resampling.BOX)
        pixels=[list(r) for r in clean];x0=max(1,(64-width)//2)
        for y in range(8):
            for x in range(width):
                if small.getpixel((x,y))>=args.threshold:pixels[y+1][x+x0]=4
        encode(target,pixels,left,right)
        unit=inv['units'][row]
        units.append({'id':unit['id'],'source':unit['source'],'translation':unit['translation'],
            'state':'needs_review','tiles':[left,right],'generated_mask_bbox':[210+bbox[0],top+bbox[1],210+bbox[2],top+bbox[3]],
            'native_text_rect':[x0,1,width,8],'source_pixels_sha256':sha(bytes(c for r in original for c in r)),
            'clean_pixels_sha256':sha(bytes(c for r in clean for c in r)),
            'final_pixels_sha256':sha(bytes(c for r in pixels for c in r))})
        for y in range(16):
            for x in range(64):
                if not (1<=x<64 and 1<=y<9) and pixels[y][x]!=original[y][x]:raise ValueError('protected pixel changed')
                role=pixels[y][x];raw=struct.unpack_from('<H',palette,0x200+9*32+role*2)[0]
                atlas.putpixel((x,row*16+y),tuple(((raw>>s)&31)*255//31 for s in (0,5,10))+(255 if role else 0,))
    out.mkdir();(out/'native_obj_block.bin').write_bytes(target)
    atlas.save(out/'native_letter_atlas.png');atlas.resize((512,896),Image.Resampling.NEAREST).save(out/'native_letter_reference_8x.png')
    record={'schema':1,'policy':'development-draft; NON-DISTRIBUTION','source_sha256':inv['source_sha256'],
        'source_offset':BASE,'bytes':len(block),'source_block_sha256':sha(block),'final_block_sha256':sha(target),
        'candidate_path':str(candidate.relative_to(ROOT)),'candidate_sha256':sha(candidate.read_bytes()),
        'tool_sha256':sha(Path(__file__).read_bytes()),'mask_rule':f'RGBA alpha>=240,r>=90,g>=145,b>=145 within measured interior crop; BOX sample native8px band, threshold{args.threshold}',
        'protected_policy':'Only x1..63,y1..8 inside seven 64x16 text pairs; roles1(background)/4(letter), every other pixel unchanged',
        'unchanged_roundtrip':True,'units':units,'review':'needs_native_screen_review','release_eligible':False}
    (out/'manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
