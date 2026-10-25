"""Save title native copy/OBJ/pixel proof plus cup suffix fixed-cell proof."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha
from report_fixedcell_runtime import verify_route
from build_visibility_poc import require_hash
from save_title_graphics import construct,decode,BASE
from fixedcell_font import bdf_cells,unpack_pixels
from archive_scripts import script_spans
from korean_codec import encode_hangul
import report_save_labels as labels
STEM='exe45_ko_development_save_surface_poc_v1'
PREFIX='save-surface-poc-v1-'

def title_proof(p,rom,block,step=11):
    cp=f'step_{step:03}';obs=read(p/(cp+'_save_title.json'));v=(p/(cp+'_gbaVideoRam.bin')).read_bytes();o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(p/(cp+'.png')).convert('RGB')
    if not obs['observer_only'] or obs['read_events']!=128 or len(obs['first_reads'])!=128:raise ValueError('native title read extent')
    for i,r in enumerate(obs['first_reads']):
        if (r['address'],r['value'],r['pc'],r['r0'],r['r1'],r['r2'])!=(0x08000000+BASE+i*2,struct.unpack_from('<H',block,i*2)[0],0xB92,0x08000000+BASE,0x06010A00,128):raise ValueError('title native halfword copy')
    if v[0x10A00:0x10B00]!=block:raise ValueError('title OBJ residency')
    for x,tile in [(86,0x50),(118,0x54)]:
        if sum(struct.unpack_from('<HHH',o,i*8)==(0x4002,0x4000+x,0xC400+tile) for i in range(128))!=1:raise ValueError('title OBJ selection/geometry/palette')
    rows=decode(block);colors={r:{im.getpixel((86+x,2+y)) for y in range(8) for x in range(21,44) if rows[y][x]==r} for r in (0,15)}
    if any(len(c)!=1 for c in colors.values()) or colors[0]==colors[15]:raise ValueError('title visible pixel masks/contrast')
    return {'source_offset':BASE,'native_halfword_reads':128,'native_pc':0xB92,'target':0x06010A00,'two32x8_OBJ_tiles':[0x50,0x54],'position':[86,2],'palette':12,'font_residency_screen_pixels':True}

def main():
    old=labels.STEM,labels.PREFIX
    try:labels.STEM=STEM;labels.PREFIX=PREFIX;label_result=labels.main(surface=True)
    finally:labels.STEM,labels.PREFIX=old
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));rom=rp.read_bytes();source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();asset_path=ROOT/'translations/save_title_graphics_ko.json';block,meta=construct(source,read(asset_path));tm=m['save_title_graphics']
    if tm['asset_sha256']!=sha(asset_path.read_bytes()) or tm['final_block_sha256']!=sha(block) or rom[BASE:BASE+256]!=block:raise ValueError('title build identity')
    prior=ROOT/'poc/output/exe45_ko_development_save_labels_poc_v1.gba';pm=read(prior.with_suffix('.json'));pr=prior.read_bytes();require_hash(prior,pm['output_sha256'])
    raw=source[BASE:BASE+256];srcp=ROOT/'poc/runtime/save-surface-source-v1';verify_route(srcp,pm['output_sha256'],set());native_title=title_proof(srcp,pr,raw)
    p=ROOT/'poc/runtime'/(PREFIX+'save-labels');verify_route(p,m['output_sha256'],set());translated_title=title_proof(p,rom,block)
    cp='step_011';calls=read(p/(cp+'_fixedcells.json'))['calls'];ar=next(a for a in m['archives'] if a['archive']=='6DA21C');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];pool=0x08000000+ar['rom_offset'];stream=pool+struct.unpack_from('<H',payload,32)[0]
    oldar=next(a for a in pm['archives'] if a['archive']=='6DA21C');oldpayload=pr[oldar['rom_offset']:oldar['rom_offset']+oldar['compiled_bytes']];oldscript=script_spans(oldpayload,120)[16];newscript=script_spans(payload,120)[16]
    if newscript!=oldscript[:-2]+encode_hangul('개')+b'\xe5':raise ValueError('cup icons/numeric commands/terminator changed')
    chosen=[c for c in calls if c['stream']==stream and c['target']==0x06009A00]
    if len(chosen)!=1:raise ValueError('cup count native lookup')
    c=chosen[0];fc=m['fixedcell_extension'];glyph=bdf_cells(ROOT/fc['font']['path'],{'개'},fc['raster'])['개'];records=[]
    if not c['complete'] or c['width']!=5 or c['height']!=1 or c['bytes']!=320 or c['tint']!=0 or len(c['glyphs'])!=5:raise ValueError('native five-cell cup count extent')
    for i,g in enumerate(c['glyphs']):
        off=g['font']-0x08000000+g['index']*64;r=rom[off:off+64];records.append(r)
        if i<4 and (g['font']!=0x08601738 or r!=source[off:off+64]):raise ValueError('native cup icons/digits')
        if i==4 and (g['font']!=0x08000000+fc['font_offset'] or g['index']!=ord('개')-0xAC00 or r!=glyph):raise ValueError('cup suffix Hangul provider')
    stage=(p/f"fixed_{c['id']:04}_stage.bin").read_bytes();v=(p/(cp+'_gbaVideoRam.bin')).read_bytes();io=(p/(cp+'_display_io.bin')).read_bytes();im=Image.open(p/(cp+'.png')).convert('RGB');bg=struct.unpack_from('<H',io,8)[0];cb=((bg>>2)&3)*0x4000;sb=((bg>>8)&31)*0x800
    if stage!=b''.join(records) or v[0x9A00:0x9B40]!=stage:raise ValueError('cup font/stage/VRAM')
    for i,r in enumerate(records):
        entries=[struct.unpack_from('<H',v,sb+(7+dy)*64+(23+i)*2)[0] for dy in (0,1)]
        if entries!=[0x90D0+i*2,0x90D1+i*2] or b''.join(v[cb+(e&1023)*32:cb+(e&1023)*32+32] for e in entries)!=r:raise ValueError('cup BG consumption')
    pixels=unpack_pixels(glyph);colors=[]
    for role in (1,2):
        expected={(x,y) for y,row in enumerate(pixels) for x,val in enumerate(row) if val==role};cs={im.getpixel((216+x,56+y)) for x,y in expected}
        if len(cs)!=1:raise ValueError('cup suffix color')
        color=next(iter(cs));actual={(x,y) for y in range(16) for x in range(8) if im.getpixel((216+x,56+y))==color}
        if actual!=expected:raise ValueError('cup suffix visible glyph mask')
        colors.append(color)
    if colors[0]==colors[1]:raise ValueError('cup suffix contrast')
    out=ROOT/'analysis/save_surface_poc_v1';im.save(out/'save_surface.png');result={'passed':True,'policy':'functional-poc; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_text_units':1,'selected_text_units':1113,'added_graphic_labels':1,'selected_graphic_labels':15,'native_title':native_title,'translated_title':translated_title,'cup_suffix':{'source':'コ','translation':'개','native_icons_numbers_commands_unchanged':True,'native_cells':5,'font_stage_BG_screen_match':True,'numeric_value_observed':0},'label_and_save_regression':label_result,'tool_sha256':sha(Path(__file__).read_bytes()),'limits':['Roll normal save entry and native zero-cup counter; other numeric values not gameplay-induced.','Same shared save title/labels may be used by other Navi, not all Navi gameplay tested.','No full-game/Hangul input/editing/old-save compatibility/RTC/audio/hardware/human release approval.']}
    (out/'surface_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('save title and cup suffix normal pixels/native save: PASS');return result

if __name__=='__main__':main()
