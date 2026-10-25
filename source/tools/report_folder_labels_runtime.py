"""Bound new folder header/title ROM, native consumers, residency and pixels."""
import json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from folder_labels import title,validate_header_path,HEADER_ROOT,TITLE_BASE
from archive_scripts import script_spans,verify_untouched_scripts
from verify_tpi_index import lz77_decompress
from fixedcell_font import unpack_pixels
from report_fixedcell_runtime import verify_route
from report_pet_graphics_runtime import sample
from pet_graphics_font import construct

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    rompath=ROOT/'poc/output/exe45_ko_development_folder_labels_v1.gba';meta=read(rompath.with_suffix('.json'));require_hash(rompath,meta['output_sha256'])
    require_hash(ROOT/'poc/output/exe45_ko_development_folder_labels_v1_repro.gba',meta['output_sha256'])
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();rom=rompath.read_bytes()
    asset=read(ROOT/'translations/pet_menu_graphics_ko.json');block,tmeta=title(source,asset);pet,_=construct(source,asset)
    nativepath=validate_header_path(source);header=meta['folder_labels']['header'];offset=header['rom_offset']
    clone=rom[offset:offset+header['compiled_bytes']];require_hash(ROOT/read(ROOT/'project.json')['source_profile']['filename'],meta['source_sha256'])
    if sha(clone)!=header['compiled_sha256'] or int.from_bytes(rom[HEADER_ROOT:HEADER_ROOT+4],'little')!=0x08000000+offset:raise ValueError('private clone identity')
    if rom[TITLE_BASE:TITLE_BASE+256]!=block or rom[0x3E45C:HEADER_ROOT]!=source[0x3E45C:HEADER_ROOT] or rom[0x3C5BC:0x3C61C]!=source[0x3C5BC:0x3C61C] or rom[0x6E2B9C:0x6E2B9C+634]!=source[0x6E2B9C:0x6E2B9C+634]:raise ValueError('native code/pool protection')
    payload=lz77_decompress(source,0x6E2B9C)[0];preserved=verify_untouched_scripts(payload,clone,76,{1})
    paths={name:ROOT/('poc/runtime/folder-labels-v1-'+name) for name in ['cold-part1','cold-part2','folder-regression','focus']}
    seen=set();routes={name:verify_route(p,meta['output_sha256'],seen) for name,p in paths.items()}
    focus=[sample(paths['focus'],step,pet,step-1) for step in range(1,8)]
    p=paths['folder-regression'];native=read(p/'step_016_folder_labels.json');calls=native['header_calls']
    if len(calls)!=1:raise ValueError('isolated header call count')
    expected={'root':0x08000000+offset,'script':1,'stage':0x0201FC00,'target':0x06007C00,'width':8,'height':1,'font':0x08601738,'tint':0,'lr':0x0803E473}
    if any(calls[0][k]!=v for k,v in expected.items()):raise ValueError('native header consumer')
    reads=native['title_first_reads']
    if native['title_read_events']<128 or len(reads)!=64:raise ValueError('title native read extent')
    for i,r in enumerate(reads):
        if r['address']!=0x08000000+TITLE_BASE+i*2 or r['value']!=struct.unpack_from('<H',block,i*2)[0] or r['pc']!=0xB8E or r['r0']!=0x08000000+TITLE_BASE or r['r1']!=0x06010A00:raise ValueError('title native halfword copy')
    fixed=[c for c in read(p/'step_016_fixedcells.json')['calls'] if c['target']==0x06007C00]
    if len(fixed)!=1 or fixed[0]['stream']!=0x08000000+offset+int.from_bytes(clone[2:4],'little'):raise ValueError('header script lookup')
    f=fixed[0];font=0x08000000+meta['fixedcell_extension']['font_offset']
    expectedglyphs=[(font,ord('칩')-0xAC00),(0x08601738,0),(font,ord('폴')-0xAC00),(font,ord('더')-0xAC00)]+[(0x08601738,0)]*4
    if [(g['font'],g['index']) for g in f['glyphs']]!=expectedglyphs:raise ValueError('Korean header/space/clear glyphs')
    expectedstage=bytearray()
    for i,g in enumerate(f['glyphs']):
        if g['destination']!=f['stage']+i*64:raise ValueError('header contiguous staging')
        at=g['font']-0x08000000+g['index']*64;expectedstage.extend(rom[at:at+64])
    if not f['complete'] or f['bytes']!=512 or f['copy_source']!=f['stage'] or f['copy_target']!=f['target'] or bytes(expectedstage)!=(p/f'fixed_{f["id"]:04}_stage.bin').read_bytes():raise ValueError('header ROM-font staging/upload')
    transfers=[{k:f[k] for k in ['id','stream','stage','target','width','height','font','bytes']}]
    cache=read(p/'final_folder_cache.json');chip=read(p/'final_chip_ko.json')
    if not(cache['resets']>0 and cache['hits']>0 and chip['verified_word_copies']>0 and cache['checks']==cache['hits']+chip['verified_word_copies']):raise ValueError('folder cache regression')
    frames=[]
    for step in routes['folder-regression']['capture_steps']:
        prefix=f'step_{step:03}';v=(p/(prefix+'_gbaVideoRam.bin')).read_bytes();o=(p/(prefix+'_gbaSpriteRam.bin')).read_bytes();io=(p/(prefix+'_display_io.bin')).read_bytes();state=read(p/(prefix+'_state.json'))['state'];im=Image.open(p/(prefix+'.png')).convert('RGB')
        if v[0x10A00:0x10B00]!=block:raise ValueError('title OBJ residency')
        locations=[]
        for tile,x in [(0x50,86),(0x54,118)]:
            found=[]
            for i in range(128):
                a,b,c=struct.unpack_from('<HHH',o,i*8)
                if a==0x4002 and b==0x4000+x and c==0xC400+tile:found.append(i)
            if len(found)!=1:raise ValueError('title native OBJ placement')
            locations.append(found[0])
        titlecolors={role:{im.getpixel((86+x,2+y)) for y in range(8) for x in range(22,45) if (block[x//8*32+y*4+x%8//2]>>(4*(x%2)))&15==role} for role in [0,15]}
        if any(len(c)!=1 for c in titlecolors.values()) or titlecolors[0]==titlecolors[15]:raise ValueError('title screen mask')
        control=struct.unpack_from('<H',io,10)[0];charbase=((control>>2)&3)*0x4000;mapbase=((control>>8)&31)*0x800
        if control&0xC080 or any(state[f'ppu.bgLayers[1].scroll{axis}'] for axis in ['X','Y']):raise ValueError('header BG geometry')
        if v[0x7C00:0x7E00]!=(p/f'fixed_{f["id"]:04}_stage.bin').read_bytes():raise ValueError('header upload residency')
        colors={0:set(),1:set(),2:set()}
        for i in range(8):
            entries=[struct.unpack_from('<H',v,mapbase+(3+y)*64+(12+i)*2)[0] for y in [0,1]]
            base=(0x7C00-charbase)//32
            if entries!=[0xB000+base+i*2,0xB000+base+1+i*2]:raise ValueError('header BG map')
            glyph=b''.join(v[charbase+(e&1023)*32:charbase+(e&1023)*32+32] for e in entries)
            for y,row in enumerate(unpack_pixels(glyph)):
                for x,role in enumerate(row):colors[role].add(im.getpixel((96+i*8+x,24+y)))
        if any(len(c)!=1 for c in colors.values()) or len({next(iter(c)) for c in colors.values()})!=3:raise ValueError('header screenshot masks')
        ram=(p/(prefix+'_gbaExtWorkRam.bin')).read_bytes()
        matches=[]
        for pool in nativepath['identical_native_header_sources']:
            nativepayload=lz77_decompress(source,pool['pool'])[0]
            if ram[0x2BA7C:0x2BA7C+len(nativepayload)]==nativepayload:matches.append(pool['pool'])
        if not matches:raise ValueError('original Navi RAM payload changed')
        frames.append({'step':step,'screenshot_sha256':sha((p/(prefix+'.png')).read_bytes()),'title_oam_indices':locations,'title_role_colors':{k:list(next(iter(v))) for k,v in titlecolors.items()},'header_role_colors':{k:list(next(iter(v))) for k,v in colors.items()},'original_navi_ram_payload_preserved':True,'matching_native_navi_pools':matches})
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':meta['output_sha256'],'source_sha256':meta['source_sha256'],'byte_identical_rebuild':True,'translated_units':meta['translated_units'],'new_labels':['장비','칩 폴더'],'native_header_call':calls[0],'native_title_read_events':native['title_read_events'],'checked_title_reads':len(reads),'protected_clone_scripts':len(preserved),'fixedcell_transfers':transfers,'folder_cache':cache,'folder_verified_word_copies':chip['verified_word_copies'],'folder_screens':frames,'pet_focus_screens':focus,'routes':{name:{'receipt_sha256':sha((paths[name]/'result.json').read_bytes()),'captures':r['steps_captured'],'complete':r['complete']} for name,r in routes.items()},'limits':['Bounded ninth equipment/folder screen and PET focus regression only','Other graphic words, full-game/hardware/audio/user wording approval remain unverified']}
    out=ROOT/'analysis/folder_labels_v1';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(480,160));sheet.paste(Image.open(ROOT/'poc/runtime/pet-graphics-v1-folder-regression/step_016.png'),(0,0));sheet.paste(Image.open(p/'step_016.png'),(240,0));sheet.save(out/'before_after.png')
    result['comparison_sha256']=sha((out/'before_after.png').read_bytes());(out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json')

if __name__=='__main__':main()
