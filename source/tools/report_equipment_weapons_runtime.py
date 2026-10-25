"""Finite33 weapon encoding/font audit plus native Rockman charge-shot cycling."""
import json,struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans,verify_untouched_scripts
from verify_tpi_index import lz77_decompress
from tpl_literals import resolve_units
from korean_codec import encode_character
from fixedcell_font import bdf_cells,unpack_pixels
from equipment_weapons import SCRIPTS,merge
from equipment_labels import validate
from report_equipment_labels_runtime import staged
from report_equipment_guides_runtime import main as guides
from report_fixedcell_runtime import verify_route

STEM='exe45_ko_development_equipment_weapons_v1';PREFIX='equipment-weapons-v1-';OUT='equipment_weapons_v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main(stem=STEM,prefix=PREFIX,outdir=OUT):
    STEM,PREFIX,OUT=stem,prefix,outdir
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();native=validate(source)
    guides(STEM,PREFIX,OUT+'/guides_regression')
    h=m['folder_labels']['header'];clone=rom[h['rom_offset']:h['rom_offset']+h['compiled_bytes']];root=0x08000000+h['rom_offset'];spans=script_spans(clone,76)
    original_spans=script_spans(lz77_decompress(source,0x6E2B9C)[0],76)
    preserved=verify_untouched_scripts(lz77_decompress(source,0x6E2B9C)[0],clone,76,set(range(1,38)))
    base=read(ROOT/'translations/equipment_labels_ko.json');additional=read(ROOT/'translations/equipment_weapons_ko.json');merged=merge(base,additional)
    units=resolve_units(additional);fe=m['fixedcell_extension'];font=0x08000000+fe['font_offset'];nativefont=0x08601738
    wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'};cells=bdf_cells(ROOT/fe['font']['path'],wanted,fe['raster'])
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    allscripts={s for record in native['weapon_selector_records'] for s in record['scripts']};coverage=[]
    for u in units:
        script=int(u['id'].split(':')[1]);text=u['translation'];encoded=b''.join(encode_character(c) if c in wanted else codes[c] for c in text)
        # All selected source units are standalone one-literal/end scripts.
        if original_spans[script][-1:]!=b'\xe5' or spans[script]!=encoded+b'\xe5' or len(text)>9 or script not in allscripts:raise ValueError('weapon encoding/end/capacity/selector coverage')
        for c in text:
            if c in wanted:
                at=fe['font_offset']+(ord(c)-0xAC00)*64
                if rom[at:at+64]!=cells[c]:raise ValueError('full weapon Korean glyph supply')
            else:
                if len(codes[c])!=1:raise ValueError('weapon native Latin/space representation')
                at=0x601738+codes[c][0]*64
                if rom[at:at+64]!=source[at:at+64]:raise ValueError('weapon native Latin/space font supply')
        coverage.append({'id':u['id'],'source':u['source'],'translation':text,'state':u['state'],'cells':len(text),'advance_pixels':len(text)*8,'selector_navis':[r['navi'] for r in native['weapon_selector_records'] if script in r['scripts']],'exact_literal_and_end':True,'all_hangul_font_records_verified':True})
    p=ROOT/('poc/runtime/'+PREFIX+'weapon-cycle-r3');route=verify_route(p,m['output_sha256'],set());pages=[];observed=[]
    for step in [3,5,6,7,8,9,10,13,14,15]:
        cp=f'step_{step:03}';v=(p/(cp+'_gbaVideoRam.bin')).read_bytes();o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(p/(cp+'.png')).convert('RGB')
        calls=read(p/(cp+'_fixedcells.json'))['calls'];roots=read(p/(cp+'_equipment_roots.json'))['calls'];rc=[c for c in roots if c['lr']==0x080D387B and c['target']==0x060133C0][-1]
        if rc['root']!=root or rc['script'] not in [3,4,5] or rc['width']!=9 or rc['height']!=1:raise ValueError('native weapon root/selection contract')
        script=rc['script'];word=next(u['translation'] for u in resolve_units(merged) if u['id']==f'6E2B9C:{script}:0');c=[c for c in calls if c['target']==0x060133C0][-1];data=staged(p,c,rom)
        initial=root+struct.unpack_from('<H',clone,script*2)[0]
        if c['stream']!=initial or c['width']!=9 or c['height']!=1 or c['bytes']!=576 or v[0x133C0:0x13600]!=data:raise ValueError('weapon stream/capacity/stage/VRAM')
        expected=[(font,ord(ch)-0xAC00) if ch in wanted or '\uac00'<=ch<='\ud7a3' else (nativefont,codes[ch][0]) for ch in word]+[(nativefont,0)]*(9-len(word))
        if [(g['font'],g['index']) for g in c['glyphs']]!=expected:raise ValueError('weapon glyph selection and full9-cell padding')
        colors={1:set(),2:set()};positions=[];blank=set();origin=None
        for i in range(9):
            tile=(0x133C0-0x10000)//32+i*2;objects=[]
            for idx in range(128):
                a,b,k=struct.unpack_from('<HHH',o,idx*8)
                if not a&0x2300 and a>>14==2 and b>>14==0 and k&1023==tile:objects.append((idx,b&511,a&255,k>>12))
            if len(objects)!=1:raise ValueError('weapon native OBJ identity')
            idx,x0,y0,palette=objects[0]
            if origin is None:
                origin=x0
                if origin not in [129,134]:raise ValueError('native weapon focus origin')
            # Native focus shifts the entire row5px left, and its final
            # clear-only OBJ has an additional3px gap (also in baseline).
            if [x0,y0]!=[origin+i*8+(3 if i==8 else 0),39]:raise ValueError('weapon native focus geometry')
            positions.append([idx,x0,y0,palette])
            for y,row in enumerate(unpack_pixels(data[i*64:i*64+64])):
                for x,role in enumerate(row):
                    if role in colors:colors[role].add(im.getpixel((x0+x,y0+y)))
                    if i>=len(word) and 43<=y0+y<=51:blank.add(im.getpixel((x0+x,y0+y)))
        if any(len(vals)!=1 for vals in colors.values()) or colors[1]==colors[2]:raise ValueError('weapon visible ink/shadow masks')
        # Clear cells use transparent palette0: native arrows and PET imagery
        # behind the shorter focused row remain visible, not a flat backdrop.
        # Prove no stale glyph by zero OBJ tile roles over all trailing cells.
        if any(data[len(word)*64:]):raise ValueError('weapon trailing OBJ tiles not cleared')
        observed.append(script);pages.append({'step':step,'script':script,'wording':word,'font_stage_vram_objects_pixels_match':True,'trailing_cells_blank':True,'trailing_screen_background_scope':'Transparent cleared OBJ cells reveal native selection arrows/PET background; no uniform RGB requirement','native_objects':positions,'screenshot_sha256':sha((p/(cp+'.png')).read_bytes())})
    if 3 not in observed or 5 not in observed or observed[-1]!=5:raise ValueError('charge shot transition/reentry coverage')
    out=ROOT/'analysis'/OUT;sheet=Image.new('RGB',(720,160))
    for i,step in enumerate([3,5,15]):sheet.paste(Image.open(p/f'step_{step:03}.png'),(240*i,0))
    sheet.save(out/'weapon_cycle.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'new_units':33,'byte_identical_rebuild':True,'protected_common_clone_scripts':len(preserved),'finite_weapon_scope':coverage,'normal_play_screens':pages,'observed_scripts':observed,'route_receipt_sha256':sha((p/'result.json').read_bytes()),'contact_sheet_sha256':sha((out/'weapon_cycle.png').read_bytes()),'guide_folder_equipment_pet_regression':True,'limits':['All33 names statically checked for selectors, exact encoding/end, width and Hangul font supply; normal-play additional name sample is Rockman charge shot only, not all Navi/gameplay routes','Other Navi dialogues and attack-power OBJ caption remain Japanese','Full-game, hardware, audio, human naming/presentation/release approval pending']}
    if 'equipment_attack_caption' in m:result['limits'][1]='Other Navi dialogues remain Japanese; caption evaluated by its separate exact-ROM report'
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json');return result

if __name__=='__main__':main()
