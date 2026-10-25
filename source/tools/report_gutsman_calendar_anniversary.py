"""Normal anniversary prompt, 48-cell transfer, visible masks and branch proof."""
import json,struct
from PIL import Image
import report_gutsman_calendar_register as prior
import report_gutsman_calendar_confirmation as ancestry
from report_roll_pet import ROOT,read,sha,static
from archive_scripts import script_spans,verify_untouched_scripts
from fixedcell_font import unpack_pixels,bdf_cells
from korean_codec import encode_character
from calendar_anniversary_labels import validate_parent,CHILD
from run_gutsman_calendar_anniversary import STEM,PREFIX,OUTDIR

def main(anniversary_confirmation=False):
    prior.STEM=STEM;prior.PREFIX=PREFIX;prior.OUTDIR=OUTDIR
    result=prior.main(anniversary=True,anniversary_confirmation=anniversary_confirmation)
    m,rom,e,streams,_=static(STEM,'665698');pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='665698')
    asset_name='gutsman_calendar_anniversary_confirmation_ko.json' if anniversary_confirmation else 'gutsman_calendar_anniversary_ko.json'
    units={u['id']:u for u in read(ROOT/'translations'/asset_name)['units']}
    p,_=ancestry.checked_route('register-anniversary-accept','register-menu-second',m,pool)
    page=prior.exact_page(p,2,31,['665698:31:0'],m,rom,e,streams,pool,units)
    asset=read(ROOT/CHILD);validate_parent(asset);text=asset['units'][-1]['translation']
    ar=next(a for a in m['archives'] if a['archive']=='6368E8');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    if len(verify_untouched_scripts(source[0x6368E8:0x6368E8+2337],payload,255,{0,60,62,63,73,74,75} if anniversary_confirmation else {0,60,62,63,73}))!=(248 if anniversary_confirmation else 250):raise ValueError('anniversary protected fixed scripts')
    body=b''.join(bytes([0]) if ch==' ' else encode_character(ch) for ch in text)+b'\xe5'
    if script_spans(payload,255)[73]!=body:raise ValueError('anniversary exact 48-cell encoding')
    start=0x08000000+ar['rom_offset']+struct.unpack_from('<H',payload,73*2)[0]
    calls=[c for c in read(p/'step_002_fixedcells.json')['calls'] if c['stream']==start]
    if len(calls)!=1:raise ValueError('anniversary fixed parser population')
    c=calls[0]
    if not c['complete'] or c['bytes']!=3072 or len(c['glyphs'])!=48 or c['caller_lr']!=0x080554BA or c['target']!=0x06013800 or c['copy_source']!=c['stage'] or c['copy_target']!=c['target']:raise ValueError('anniversary parser/copy extent')
    font=m['fixedcell_extension']['mono_provider'];glyphs=bdf_cells(ROOT/font['font']['path'],set(text)-{' '},font['raster']);records=[];cursor=start
    for i,(ch,g) in enumerate(zip(text,c['glyphs'])):
        index=0 if ch==' ' else ord(ch)-0xAC00;provider=0x08619EF8 if ch==' ' else 0x08000000+font['font_offset']
        record=source[0x619EF8:0x619F38] if ch==' ' else glyphs[ch]
        if (g['stream'],g['index'],g['font'],g['destination'])!=(cursor,index,provider,c['stage']+i*64):raise ValueError('anniversary decoded cell/provider')
        if rom[provider-0x08000000+index*64:provider-0x08000000+(index+1)*64]!=record:raise ValueError('anniversary font source')
        records.append(record);cursor+=1 if ch==' ' else len(encode_character(ch))
    stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();v=(p/'step_002_gbaVideoRam.bin').read_bytes()
    if stage!=b''.join(records) or v[0x13800:0x14400]!=stage:raise ValueError('anniversary ROM/stage/VRAM')
    im=Image.open(p/'step_002.png').convert('RGB');o=(p/'step_002_gbaSpriteRam.bin').read_bytes();ref=ROOT/'poc/runtime/gutsman-calendar-register-v1-register-anniversary-accept';old_o=(ref/'step_002_gbaSpriteRam.bin').read_bytes();pal=(p/'step_002_gbaPaletteRam.bin').read_bytes();oldpal=(ref/'step_002_gbaPaletteRam.bin').read_bytes();visible=[];colors={}
    for row in range(3):
        for cell in range(10):
            i=row*16+cell;tile=448+i*2;matches=[j for j in range(128) if struct.unpack_from('<H',o,j*8+4)[0]&1023==tile]
            if len(matches)!=1:raise ValueError('anniversary unique visible OBJ')
            j=matches[0];a,b,k=struct.unpack_from('<HHH',o,j*8)
            if o[j*8:j*8+6]!=old_o[j*8:j*8+6] or a&0x2300 or a>>14!=2 or b>>14!=0 or (b&511,a&255)!=(88+cell*8,41+row*16):raise ValueError('anniversary native geometry')
            if pal[0x200+(k>>12)*32:0x220+(k>>12)*32]!=oldpal[0x200+(k>>12)*32:0x220+(k>>12)*32]:raise ValueError('anniversary palette')
            for yy,line in enumerate(unpack_pixels(records[i])):
                for xx,role in enumerate(line):colors.setdefault(role,set()).add(im.getpixel(((b&511)+xx,(a&255)+yy)))
            visible.append(dict(cell=i,character=text[i],sprite=j,xy=[b&511,a&255],glyph_sha256=sha(records[i])))
    if set(colors)!={1,3,4} or any(len(x)!=1 for x in colors.values()) or len(set(next(iter(x)) for x in colors.values()))!=3:raise ValueError('anniversary full screenshot masks/blank clear')
    branches={};rt=ROOT/'poc/runtime';expected='0000000101060000000000000000000000000000000000000000000000000000'
    for name,parent,script in [('anniversary-second','register-anniversary-accept',31),('anniversary-third','anniversary-second',31),('anniversary-cancel','register-anniversary-accept',7),('anniversary-self-accept','register-anniversary-accept',33),('anniversary-school-accept','anniversary-second',33)]:
        q,_=ancestry.checked_route(name,parent,m,pool);ram=(q/'step_002_gbaExtWorkRam.bin').read_bytes()
        if ram[0xFA21]!=script or ram[0x1310:0x1330].hex()!=expected:raise ValueError('anniversary branch/record')
        branches[name]=dict(script=script,record=expected,screenshot_sha256=sha((q/'step_002.png').read_bytes()))
    for name,y in [('register-anniversary-accept',42),('anniversary-second',58),('anniversary-third',74)]:
        o=(rt/(PREFIX+name)/'step_002_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,30*8)
        if (a&255,b&511,k>>12)!=(y,72,14):raise ValueError('anniversary focus geometry')
    q=rt/(PREFIX+'anniversary-other-accept');from report_fixedcell_runtime import verify_route
    r=verify_route(q,m['output_sha256'],set());ram=(q/'step_002_gbaExtWorkRam.bin').read_bytes()
    if r['state_origin']!=str(rt/(PREFIX+'anniversary-third')/'result.json') or ram[0xFA21]!=9 or struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+ar['rom_offset'] or ram[0x1310:0x1330].hex()!=expected:raise ValueError('anniversary other keyboard branch')
    branches['anniversary-other-accept']=dict(script=9,archive='6368E8',record=expected,keyboard_untranslated=True)
    out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(720,320));shots=['register-anniversary-accept','anniversary-second','anniversary-third','anniversary-cancel','anniversary-self-accept','anniversary-other-accept']
    for i,name in enumerate(shots):sheet.paste(Image.open(rt/(PREFIX+name)/'step_002.png'),(i%3*240,i//3*160))
    sheet.save(out/'calendar_anniversary.png');result.update(anniversary_prompt=page,anniversary_labels=dict(unit='6368E8:73:0',decoded_cells=48,stage_vram_bytes=3072,visible_cells=visible,colors={k:list(next(iter(v))) for k,v in colors.items()}),anniversary_branches=branches,new_literal_units=5 if anniversary_confirmation else 2,selected_text_units=2304 if anniversary_confirmation else 2299)
    result['limits']+=['Anniversary menu31/73 and three focus positions verified. B returns script7. Other to original Japanese keyboard9. Anniversary confirmation/commit verified by successor report.' if anniversary_confirmation else 'Anniversary menu31/73 and three focus positions verified. B returns script7. Birthday/school accept to original Japanese confirmation33; Other to original Japanese keyboard9. No anniversary commit/persistence claim.']
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Anniversary prompt + 48-cell source/stage/VRAM + 30 visible masks + focus/B/three accepts: PASS');return result

if __name__=='__main__':main()
