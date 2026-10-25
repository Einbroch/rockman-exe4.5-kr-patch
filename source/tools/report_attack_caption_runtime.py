"""Exact compressed caption -> BIOS output -> resident asset -> OBJ pixels."""
import json,struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from attack_caption import construct,decode,BASE,STORED,TILES,BYTES
from fixedcell_font import unpack_pixels
from report_equipment_labels_runtime import staged
from report_equipment_weapons_runtime import main as weapons_report

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main(stem='exe45_ko_development_attack_caption_v2',prefix='attack-caption-v1-',outdir='attack_caption_v2',roll=False):
    rp=ROOT/f'poc/output/{stem}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);require_hash(rp.with_name(stem+'_repro.gba'),m['output_sha256']);rom=rp.read_bytes()
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();asset_path=ROOT/'translations/equipment_attack_caption_ko.json';asset=read(asset_path);stored,payload,record=construct(source,asset)
    if m['equipment_attack_caption']['asset_sha256']!=sha(asset_path.read_bytes()) or rom[BASE:BASE+STORED]!=stored:raise ValueError('caption artifact/source input binding')
    if any(m['equipment_attack_caption'][k]!=v for k,v in record.items()):raise ValueError('caption generated record drift')
    for a,b in [(0x3C414,0x3C44C),(0x29164,0x291AA),(0xEC140,0xEC15C),(0x5131A4,0x5131C4)]:
        if rom[a:b]!=source[a:b]:raise ValueError('caption native loader/codec/next asset altered')
    if roll:
        from report_equipment_guides_runtime import main as guides_report
        weapons=guides_report(stem,prefix,outdir+'/guides_regression',roll=True)
    else:weapons=weapons_report(stem,prefix,outdir+'/weapons_regression')
    p=ROOT/('poc/runtime/'+prefix+'equipment');rows=decode(payload[TILES:TILES+BYTES]);final=read(p/'step_015_caption_supply.json')
    outputs=final['outputs']
    if len(outputs)!=2 or any((p/o['file']).read_bytes()!=payload for o in outputs):raise ValueError('native BIOS decompression full payload')
    loads=[x for x in final['loads'] if x['source']==0x08512FA0]
    copies=[x for x in final['loads'] if x['target']==0x06013C00 and x.get('site')==0x080EC140]
    if len(loads)!=2 or len(copies)!=2 or any(x['source']!=0x0202BF9C or x['r2']!=256 or x['outer_lr_at_sp16']!=0x08000833 for x in copies):raise ValueError('caption native upload route/extent')
    oldp=ROOT/'poc/runtime/attack-caption-source-v5';oldrom=(ROOT/'poc/output/exe45_ko_development_equipment_weapons_v1.gba').read_bytes();oldcalls=read(oldp/'step_007_fixedcells.json')['calls'];oldnum=[c for c in oldcalls if c['target']==0x06013F40][-1];olddata=staged(oldp,oldnum,oldrom)
    pages=[]
    for step in [7,9,11,15]:
        cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();v=(p/(cp+'_gbaVideoRam.bin')).read_bytes();o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(p/(cp+'.png')).convert('RGB')
        if ram[0x2BF7C:0x2BF7C+len(payload)-4]!=payload[4:] or v[0x13C00:0x13F00]!=payload[TILES:TILES+BYTES]:raise ValueError('caption native resident asset/OBJ VRAM')
        objects={}
        for i in range(128):
            a,b,k=struct.unpack_from('<HHH',o,i*8)
            if not a&0x2300 and (k&1023) in [480,488,496,506,508,510]:objects[k&1023]=(i,b&511,a&255,k>>12,a>>14,b>>14)
        if any(objects.get(tile,())[1:]!=(x,80,3,1,2) for tile,x in [(480,128),(488,160),(496,192)]):raise ValueError('caption native96x16 geometry/palette')
        calls=read(p/(cp+'_fixedcells.json'))['calls'];num=[c for c in calls if c['target']==0x06013F40][-1];data=staged(p,num,rom)
        if data!=olddata or v[0x13F40:0x14000]!=data:raise ValueError('attack number source/stage/VRAM unchanged')
        overlay=set();numcolors={1:set(),2:set()}
        for j in range(3):
            ob=objects.get(506+j*2)
            if not ob or ob[1:]!=(200+j*8,80,3,2,0):raise ValueError('numeric unchanged OBJ geometry')
            for yy,row in enumerate(unpack_pixels(data[j*64:(j+1)*64])):
                for xx,role in enumerate(row):
                    if role:
                        xy=(200+j*8+xx,80+yy);overlay.add(xy);numcolors[role].add(im.getpixel(xy))
        if any(len(c)!=1 for c in numcolors.values()) or numcolors[1]==numcolors[2]:raise ValueError('attack number visible mask')
        colors={role:set() for role in [11,12,13,14,15]};pixels=0
        for y,row in enumerate(rows):
            for x,role in enumerate(row):
                xy=(128+x,80+y)
                if role and xy not in overlay:colors[role].add(im.getpixel(xy));pixels+=1
        if any(len(c)!=1 for c in colors.values()) or colors[13]==colors[15]:raise ValueError('caption screen palette role masks')
        pages.append({'step':step,'native_bios_payload_and_ram_verified':True,'caption_vram_objects_pixels_match':True,'checked_nontransparent_pixels':pixels,'role_colors':{k:list(next(iter(c))) for k,c in colors.items()},'numeric_overlay_pixels':len(overlay),'attack_number_unchanged':True,'screenshot_sha256':sha((p/(cp+'.png')).read_bytes())})
    out=ROOT/'analysis'/outdir;sheet=Image.new('RGB',(480,160));sheet.paste(Image.open(oldp/'step_007.png'),(0,0));sheet.paste(Image.open(p/'step_007.png'),(240,0));sheet.save(out/'before_after.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_text_units':m['translated_units'],'new_graphic_labels':1,'translated_graphic_labels_total':9,'byte_identical_rebuild':True,'caption':record,'native_decompressions':outputs,'native_uploads':copies,'pages':pages,'weapons_guides_folder_pet_regression':weapons['passed'],'runtime_filename_binding':'Prefix v1 consumed v1 ROM; final v2 ROM is byte-identical SHA256, so same exact-artifact runtime evidence applies','comparison_sha256':sha((out/'before_after.png').read_bytes()),'limits':['Caption normal-play runtime uses Rockman only; not all Navi gameplay','Other Navi dialogue and full-game untranslated text remain; complete-corpus denominator not established','Human wording/visual approval, full playthrough, hardware/audio/release QA pending']}
    result['runtime_filename_binding']='Route receipts and recursive checkpoint chain verified against this exact ROM SHA256; filenames alone are not evidence'
    if roll:
        result['roll_guides_regression']=result.pop('weapons_guides_folder_pet_regression')
        result['limits'][0]='Caption normal-play runtime Navi1 Roll; Rockman separately verified on this exact ROM; no all-Navi gameplay claim'
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json');return result

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--stem',default='exe45_ko_development_attack_caption_v2');ap.add_argument('--prefix',default='attack-caption-v1-');ap.add_argument('--outdir',default='attack_caption_v2');args=ap.parse_args()
    main(args.stem,args.prefix,args.outdir)
