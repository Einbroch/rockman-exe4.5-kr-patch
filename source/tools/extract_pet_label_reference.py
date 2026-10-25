"""Extract native OBJ menu strips, without changing pixels or ROM."""
import json, struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import verify_route

ROWS = [
    ('tournament','トーナメント','토너먼트',75,68,67,66),
    ('jack_in','プラグイン','플러그인',74,64,65,63),
    ('equipment','そうび','장비',73,62,61,60),
    ('library','データライブラリ','데이터 라이브러리',72,59,58,57),
    ('mail','Eメール','메일',71,56,55,54),
    ('communication','つうしん','통신',70,53,52,51),
    ('save','セーブ','저장',69,50,49,48),
]

def main():
    out=ROOT/'analysis/pet_labels_v1'
    if out.exists(): raise ValueError('fresh output required')
    route=ROOT/'poc/runtime/roll-tactics-v1-cold-part2'
    m=json.loads((ROOT/'poc/output/exe45_ko_development_roll_tactics_v1.json').read_text())
    verify_route(route,m['output_sha256'],set())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']
    require_hash(source,m['source_sha256']);rom=source.read_bytes()
    v=(route/'step_040_gbaVideoRam.bin').read_bytes()
    p=(route/'step_040_gbaPaletteRam.bin').read_bytes()
    o=(route/'step_040_gbaSpriteRam.bin').read_bytes()
    if rom[0x6303B8:0x6315B8]!=v[0x11000:0x12200]:raise ValueError('source block differs')
    atlas=Image.new('RGBA',(96,112));units=[]
    for row,(key,jp,ko,*indices) in enumerate(ROWS):
        objects=[];xbase=None
        for index in indices:
            a,b,c=struct.unpack_from('<HHH',o,index*8)
            if a&0x2300 or (a>>14) not in (0,1) or c>>12!=9:raise ValueError('OBJ format')
            shape=a>>14;size=b>>14
            w,h=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)]][shape][size]
            x=b&511;y=a&255;tile=c&1023
            if xbase is None:xbase=x
            if h!=16:raise ValueError('OBJ height')
            for py in range(h):
                for px in range(w):
                    t=tile+(py//8)*(w//8)+px//8
                    byte=v[0x10000+t*32+(py%8)*4+(px%8)//2]
                    role=(byte>>(4*(px%2)))&15
                    raw=struct.unpack_from('<H',p,0x200+9*32+role*2)[0]
                    rgba=tuple(((raw>>s)&31)*255//31 for s in (0,5,10))+(255 if role else 0,)
                    atlas.putpixel((x-xbase+px,row*16+py),rgba)
            objects.append({'oam_index':index,'attributes':[a,b,c],'screen_xy':[x,y],
                'size':[w,h],'tile':tile,'rom_offset':0x6303B8+(tile-0x80)*32})
        units.append({'id':'pet.obj.'+key,'source':jp,'translation':ko,'state':'needs_review',
            'edit_rect':[16,row*16,64,16],'protected':'icon x0..15 and edge x80..95; transparency and frame',
            'objects':objects})
    out.mkdir();atlas.save(out/'native_atlas.png')
    atlas.resize((768,896),Image.Resampling.NEAREST).save(out/'native_reference_8x.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','formal_image_handoff':'BLOCKED: missing overall image inventory and text-review/font handoff',
        'source_sha256':m['source_sha256'],'rom_sha256':m['output_sha256'],
        'receipt_sha256':sha((route/'result.json').read_bytes()),'tool_sha256':sha(Path(__file__).read_bytes()),
        'source_block':[0x6303B8,0x6315B8],'source_vram_equal':True,
        'native_atlas_sha256':sha((out/'native_atlas.png').read_bytes()),
        'scope':'Seven PET menu OBJ labels on one native screen only; raw palette preview, not final LCD composition; loader/focus variants not yet proven',
        'review_notes':'Existing PET dialogue terminology retained. Full library label may exceed 64px at original height; no silent abbreviation.',
        'units':units,'release_eligible':False}
    (out/'inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(out)

if __name__=='__main__':main()
