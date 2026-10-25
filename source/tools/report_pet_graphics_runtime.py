"""Bound ROM->native reads->OBJ residency->all seven visible letter masks."""
import json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from pet_graphics_font import construct
from prepare_pet_graphics_v2 import BASE,TILES,decode

def sample(route,step,block,expected_focus=None):
    prefix=f'step_{step:03}';v=(route/(prefix+'_gbaVideoRam.bin')).read_bytes();o=(route/(prefix+'_gbaSpriteRam.bin')).read_bytes()
    if v[0x11000:0x12200]!=block:raise ValueError('resident PET graphics differ')
    screenshot=Image.open(route/(prefix+'.png')).convert('RGB');rows=[]
    for row,(left,right) in enumerate(TILES):
        found=[]
        for index in range(128):
            a,b,c=struct.unpack_from('<HHH',o,index*8)
            if not a&0x2300 and a>>14==1 and b>>14==2 and c&1023==left and c>>12 in (8,9) and a&255==16+row*12:
                found.append((b&511,a&255,c>>12))
        if len(found)!=1:raise ValueError('unique PET text OBJ')
        x0,y0,palette=found[0];pixels=decode(block,left,right);colors={}
        for role in (1,4):
            colors[role]={screenshot.getpixel((x0+x,y0+y)) for y in range(1,9) for x in range(1,64) if pixels[y][x]==role}
            if len(colors[role])!=1:raise ValueError(f'visible pixel mask mismatch:{route.name}/{step}/row{row}/role{role}')
        if colors[1]==colors[4]:raise ValueError('letter invisible')
        rows.append({'row':row,'xy':[x0,y0],'palette':palette,'letter_rgb':list(next(iter(colors[4]))),
            'background_rgb':list(next(iter(colors[1]))),'all_interior_pixels_match_role_masks':True})
    if expected_focus is not None:
        active=[r['row'] for r in rows if r['xy'][0]==137 and r['palette']==8]
        if active!=[expected_focus]:raise ValueError('native focus progression')
    return {'route':route.name,'step':step,'screenshot_sha256':sha((route/(prefix+'.png')).read_bytes()),'rows':rows}

def main():
    rom=ROOT/'poc/output/exe45_ko_development_pet_graphics_v1.gba';m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'));source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']
    block,prepared=construct(source.read_bytes(),asset)
    if rom.read_bytes()[BASE:BASE+0x1200]!=block:raise ValueError('ROM graphic identity')
    repro=ROOT/'poc/output/exe45_ko_development_pet_graphics_v1_repro.gba';require_hash(repro,m['output_sha256'])
    baseline=ROOT/'poc/output/exe45_ko_development_roll_tactics_v1.gba';require_hash(baseline,'1ca65635bcfb92ff3845bf7b75cf6491a045f32cceda5ec16eca977d7d45f31f')
    a=baseline.read_bytes();b=rom.read_bytes()
    if len(a)!=len(b) or a[:BASE]!=b[:BASE] or a[BASE+0x1200:]!=b[BASE+0x1200:]:raise ValueError('unrelated baseline ROM differences')
    routes={};samples=[]
    for name in ['cold-part1','cold-part2','focus','prompts','folder-regression']:
        p=ROOT/('poc/runtime/pet-graphics-v1-'+name);routes[name]=verify_route(p,m['output_sha256'],set())
        if name=='focus':samples.extend(sample(p,step,block,step-1) for step in range(1,8))
        if name=='prompts':samples.extend(sample(p,step,block) for step in routes[name]['capture_steps'])
    reads=json.loads((ROOT/'poc/runtime/pet-graphics-v1-cold-part2/step_040_pet_source_reads.json').read_text())
    for i,r in enumerate(reads['first_reads']):
        if r['address']!=0x086303B8+i*4 or r['value']!=struct.unpack_from('<I',block,i*4)[0] or r['pc']!=0xC18:
            raise ValueError('new ROM native source-read identity')
        if r['r0']!=0x086303B8+(i//8+1)*32 or r['r1']!=0x06011000+(i//8)*32:raise ValueError('native copy destination progression')
    if len(reads['first_reads'])!=160:raise ValueError('retained native reads count')
    result={'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],'source_sha256':m['source_sha256'],
        'tool_sha256':sha(Path(__file__).read_bytes()),'prepared_asset':prepared,'passed':True,'byte_identical_rebuild':True,
        'baseline_only_pet_block_changed':True,'baseline_text_units':m['translated_units'],'new_graphic_labels':7,
        'native_read_events':reads['total'],'checked_first_native_read_events':160,'visible_label_mask_samples':samples,
        'routes':{name:{'receipt_sha256':sha((ROOT/('poc/runtime/pet-graphics-v1-'+name)/'result.json').read_bytes()),
            'captures':r['steps_captured'],'complete':r['complete']} for name,r in routes.items()},
        'limits':['Native PET seven labels and confirm/cancel/focus only; no actual communication or save operation',
            'Folder route completed; no new comprehensive folder glyph-pixel report','All other graphic text remains outside this bounded result',
            'Audio muted; hardware/full-game/user wording review pending'],'release_eligible':False}
    sheet=Image.new('RGB',(720,480))
    frames=[(ROOT/'poc/runtime/pet-graphics-v1-focus',step) for step in range(1,8)]
    frames+=[(ROOT/'poc/runtime/pet-graphics-v1-prompts',23),(ROOT/'poc/runtime/pet-graphics-v1-folder-regression',16)]
    for index,(route,step) in enumerate(frames):
        frame=Image.open(route/f'step_{step:03}.png').convert('RGB')
        if frame.size!=(240,160):raise ValueError('native screenshot dimensions')
        sheet.paste(frame,((index%3)*240,(index//3)*160))
    sheet_path=ROOT/'analysis/pet_font_v2/runtime_contact_sheet.png';sheet.save(sheet_path)
    result['contact_sheet_sha256']=sha(sheet_path.read_bytes())
    out=ROOT/'analysis/pet_font_v2/runtime.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
