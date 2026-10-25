"""Equipment v2 exact-ROM roots, clear extent, glyphs, OBJ masks and regressions."""
import json,struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from equipment_labels import validate,ROOTS,HEADER_WIDTH
from folder_labels import title,HEADER_ROOT,validate_header_path
from archive_scripts import verify_untouched_scripts
from verify_tpi_index import lz77_decompress
from fixedcell_font import unpack_pixels
from report_fixedcell_runtime import verify_route
from report_pet_graphics_runtime import sample
from pet_graphics_font import construct

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def staged(p,c,rom):
    if not c['complete'] or c['tint'] or c['bytes']!=c['width']*c['height']*64 or len(c['glyphs'])*64!=c['bytes'] or c['copy_target']!=c['target'] or c['copy_source']!=c['stage']:raise ValueError('fixed-cell transfer extent')
    data=bytearray()
    for i,g in enumerate(c['glyphs']):
        if g['destination']!=c['stage']+i*64:raise ValueError('noncontiguous glyph stage')
        at=g['font']-0x08000000+g['index']*64
        if not 0<=at<=len(rom)-64:raise ValueError('font source bounds')
        data.extend(rom[at:at+64])
    if bytes(data)!=(p/f'fixed_{c["id"]:04}_stage.bin').read_bytes():raise ValueError('ROM-font -> stage mismatch')
    return bytes(data)

def main(stem='exe45_ko_development_equipment_labels_v2',prefix='equipment-labels-v2-',outdir='equipment_labels_v2'):
    rp=ROOT/f'poc/output/{stem}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/f'poc/output/{stem}_repro.gba',m['output_sha256'])
    sp=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes();native=validate(source)
    h=m['folder_labels']['header'];at=h['rom_offset'];root=0x08000000+at;clone=rom[at:at+h['compiled_bytes']]
    if sha(clone)!=h['compiled_sha256'] or rom[HEADER_WIDTH:HEADER_WIDTH+3]!=bytes([12,3,3]):raise ValueError('clone/clear width')
    for word in ROOTS+[HEADER_ROOT]:
        if struct.unpack_from('<I',rom,word)[0]!=root:raise ValueError('fixed-text root patch')
    for f in native['functions']:
        if sha(rom[f['start']:f['end']])!=f['sha256']:raise ValueError('native equipment instruction drift')
    protected=[(0x3C5BC,0x3C61C),(0x3EFA4,0x3EFC4),(0xD41A0,0xD41A4),(0x6E2B9C,0x6E2B9C+634)]
    if 'equipment_guides' not in m:protected.append((0x3C478,0x3C48C))
    for a,b in protected:
        if rom[a:b]!=source[a:b]:raise ValueError('Navi loader/dialogue/numeric storage altered')
    changed=set(range(1,38)) if 'weapons' in m['folder_labels'] else {1,2,3,4}
    preserved=verify_untouched_scripts(lz77_decompress(source,0x6E2B9C)[0],clone,76,changed)
    names=['cold-part1','cold-part2','folder-regression','equipment','focus'];paths={n:ROOT/('poc/runtime/'+prefix+n) for n in names};seen=set();routes={n:verify_route(p,m['output_sha256'],seen) for n,p in paths.items()}
    asset=read(ROOT/'translations/pet_menu_graphics_ko.json');pet,_=construct(source,asset);titleblock,_=title(source,asset)
    focus=[sample(paths['focus'],i,pet,i-1) for i in range(1,8)]
    p=paths['equipment'];font=0x08000000+m['fixedcell_extension']['font_offset'];nativefont=0x08601738
    finalroots=read(p/'step_015_equipment_roots.json')['calls'];shared=[c for c in finalroots if c['lr'] in (0x080D37F9,0x080D387B)]
    if any(c['root']!=root or c['font']!=nativefont or c['height']!=1 for c in shared):raise ValueError('equipment native root/consumer')
    titlecalls=[c for c in shared if c['script']==2]
    if len(titlecalls)!=2 or any(c['width']!=12 or c['target']!=0x060122C0 for c in titlecalls) or titlecalls[1]['frame']<=titlecalls[0]['frame']:raise ValueError('entry/reentry title clear')
    numeric=[c for c in finalroots if c['script']==63]
    if len(numeric)!=2 or any(c['root']!=0x0202BA7C for c in numeric):raise ValueError('numeric original RAM root')
    frames=[]
    for step in [7,9,11,15]:
        prefix=f'step_{step:03}';v=(p/(prefix+'_gbaVideoRam.bin')).read_bytes();o=(p/(prefix+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(p/(prefix+'.png')).convert('RGB');calls=read(p/(prefix+'_fixedcells.json'))['calls'];latest={c['target']:c for c in calls};rows=[]
        for target,word in [(0x060122C0,'  칩 폴더   '),(0x060133C0,'록 버스터'),(0x060139C0,'실드')]:
            c=latest[target];data=staged(p,c,rom);start=target-0x06000000
            if v[start:start+c['bytes']]!=data:raise ValueError('stage -> OBJ VRAM')
            expected=[(font,ord(ch)-0xAC00) if ch!=' ' else (nativefont,0) for ch in word]+[(nativefont,0)]*(c['width']-len(word))
            if [(g['font'],g['index']) for g in c['glyphs']]!=expected:raise ValueError('word/space/clear glyph sequence')
            masks={1:set(),2:set()};positions=[]
            for i in range(c['width']):
                tile=(start-0x10000)//32+i*2;found=[]
                for idx in range(128):
                    a,b,k=struct.unpack_from('<HHH',o,idx*8)
                    if not a&0x2300 and a>>14==2 and b>>14==0 and k&1023==tile:found.append((idx,b&511,a&255,k>>12))
                if len(found)!=1:raise ValueError('unique native letter OBJ')
                idx,x0,y0,palette=found[0];positions.append([idx,x0,y0,palette])
                for y,row in enumerate(unpack_pixels(data[i*64:i*64+64])):
                    for x,role in enumerate(row):
                        if role in masks:masks[role].add(im.getpixel((x0+x,y0+y)))
            if any(len(values)!=1 for values in masks.values()) or masks[1]==masks[2]:raise ValueError('equipment visible ink/shadow masks')
            if target==0x060122C0:
                if any(data[10*64:]):raise ValueError('two trailing title cells not blank')
                tail={im.getpixel((x,y)) for y in range(25,34) for x in range(188,204)}
                leading={im.getpixel((x,y)) for y in range(25,34) for x in range(110,122)}
                if len(tail)!=1 or tail!=leading or tail&masks[1] or tail&masks[2]:raise ValueError('trailing title background/stale numeric pixels')
            rows.append({'target':target,'wording':word,'cells':c['width'],'copy_bytes':c['bytes'],'letter_objects':positions,'colors':{role:list(next(iter(values))) for role,values in masks.items()},'visible_ink_and_shadow_masks_equal':True})
        ram=(p/(prefix+'_gbaExtWorkRam.bin')).read_bytes();matching=[]
        for pool in validate_header_path(source)['identical_native_header_sources']:
            raw=lz77_decompress(source,pool['pool'])[0]
            if ram[0x2BA7C:0x2BA7C+len(raw)]==raw:matching.append(pool['pool'])
        if not matching:raise ValueError('original Navi RAM no longer intact')
        frames.append({'step':step,'rows':rows,'matching_original_navi_pools':matching,'title_tail_is_blank_background':True,'screenshot_sha256':sha((p/(prefix+'.png')).read_bytes())})
    p=paths['folder-regression'];folder=[]
    for step in [9,12,15,16]:
        prefix=f'step_{step:03}';v=(p/(prefix+'_gbaVideoRam.bin')).read_bytes();im=Image.open(p/(prefix+'.png')).convert('RGB');calls=read(p/(prefix+'_fixedcells.json'))['calls'];c=[x for x in calls if x['target']==0x06007C00][-1];data=staged(p,c,rom)
        if v[0x7C00:0x7E00]!=data or v[0x10A00:0x10B00]!=titleblock:raise ValueError('folder title/header regression')
        colors={0:set(),1:set(),2:set()}
        for i in range(8):
            entries=[struct.unpack_from('<H',v,0xE800+(3+y)*64+(12+i)*2)[0] for y in [0,1]]
            if entries!=[0xB1E0+i*2,0xB1E1+i*2]:raise ValueError('folder header tilemap')
            for y,row in enumerate(unpack_pixels(data[i*64:i*64+64])):
                for x,role in enumerate(row):colors[role].add(im.getpixel((96+i*8+x,24+y)))
        if any(len(values)!=1 for values in colors.values()) or len({next(iter(values)) for values in colors.values()})!=3:raise ValueError('folder pixel regression')
        folder.append({'step':step,'font_stage_vram_map_pixels_match':True})
    cache=read(p/'final_folder_cache.json');copies=read(p/'final_chip_ko.json')['verified_word_copies']
    if not(cache['resets']>0 and cache['hits']>0 and copies>0 and cache['checks']==cache['hits']+copies):raise ValueError('folder cache ABI regression')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,160));sheet.paste(Image.open(ROOT/'poc/runtime/folder-labels-v1-equipment-roots/step_007.png'),(0,0));sheet.paste(Image.open(paths['equipment']/'step_007.png'),(240,0));sheet.save(out/'before_after.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'source_sha256':m['source_sha256'],'rom_sha256':m['output_sha256'],'byte_identical_rebuild':True,'translated_units':m['translated_units'],'new_units':3,'native_scope':native,'protected_clone_scripts':len(preserved),'native_root_calls':finalroots,'equipment_screens':frames,'folder_screens':folder,'pet_focus_screens':focus,'cache':cache,'verified_folder_copies':copies,'routes':{n:{'receipt_sha256':sha((paths[n]/'result.json').read_bytes()),'captures':r['steps_captured'],'complete':r['complete']} for n,r in routes.items()},'failed_candidate':{'rom':'poc/output/exe45_ko_development_equipment_labels_v1.gba','sha256':'aa4cc6bf6b2572ba88752af629f2ea6beadf541851217956c9eb626a3d255a4f','issue':'Header12 visible OBJ cells but native width10 leaves stale numeric glyphs after shorter Korean text; preserved, not current'},'limits':['Three shared fixed equipment labels only; other weapon names remain Japanese','Equipment guide dialogues and baked buster attack caption remain Japanese and pending','No full-game/hardware/audio/wording release approval'],'comparison_sha256':sha((out/'before_after.png').read_bytes())}
    if 'equipment_guides' in m:result['limits'][1]='Equipment guide rendering evaluated separately; OBJ buster attack caption remains Japanese and pending'
    if 'weapons' in m['folder_labels']:result['limits'][0]='Additional33 weapon names evaluated separately; this report checks unchanged Rockman/default equipment and folder/PET regressions'
    if 'equipment_attack_caption' in m:result['limits'][1]='Guides and caption evaluated by their separate exact-ROM reports; this report covers default equipment/folder/PET'
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json')
    return result

if __name__=='__main__':main()
