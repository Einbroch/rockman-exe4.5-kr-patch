"""Exact-ROM anniversary confirmation, preset transfer, branches and records."""
import json,struct
from PIL import Image
import report_gutsman_calendar_anniversary as prior
import report_gutsman_calendar_register as pages
import report_gutsman_calendar_confirmation as ancestry
from report_roll_pet import ROOT,read,sha,static
from report_fixedcell_runtime import verify_route
from calendar_anniversary_confirmation import DIALOGUE,LABELS,validate
from korean_codec import encode_hangul
from fixedcell_font import bdf_cells,unpack_pixels
from run_gutsman_calendar_anniversary_confirmation import STEM,PREFIX,OUTDIR

def fixed_name(p,step,word,rom,m):
    cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();body=encode_hangul(word)+b'\xe5'
    if ram[0x26080:0x26080+len(body)]!=body:raise ValueError('anniversary preset ROM-to-name-buffer')
    calls=read(p/(cp+'_fixedcells.json'))['calls'];wanted=[ord(ch)-0xAC00 for ch in word];fc=m['fixedcell_extension']['mono_provider'];provider=0x08000000+fc['font_offset'];glyphs=bdf_cells(ROOT/fc['font']['path'],set(word),fc['raster'])
    matches=[c for c in calls if c['target']==0x06013800 and [g['index'] for g in c['glyphs'][:len(word)]]==wanted]
    if len(matches)!=1:raise ValueError('anniversary fixed-name caller population')
    c=matches[0]
    if not c['complete'] or len(c['glyphs'])!=10 or c['bytes']!=640 or c['copy_source']!=c['stage'] or c['copy_target']!=c['target']:raise ValueError('anniversary ten-cell name clear')
    records=[]
    for i,g in enumerate(c['glyphs']):
        at=g['font']-0x08000000+g['index']*64;record=rom[at:at+64]
        if i<len(word):
            if g['font']!=provider or record!=glyphs[word[i]]:raise ValueError('anniversary name BDF/provider')
        elif g['index']!=0 or g['font']!=0x08619EF8:raise ValueError('anniversary name blank provider')
        if g['destination']!=c['stage']+i*64:raise ValueError('anniversary contiguous name stage')
        records.append(record)
    stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();v=(p/(cp+'_gbaVideoRam.bin')).read_bytes()
    if stage!=b''.join(records) or v[0x13800:0x13A80]!=stage:raise ValueError('anniversary name font-stage-VRAM')
    im=Image.open(p/(cp+'.png')).convert('RGB');o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();colors={};cells=[]
    for i,record in enumerate(records):
        tile=448+i*2;matches=[j for j in range(128) if struct.unpack_from('<H',o,j*8+4)[0]&1023==tile]
        if len(matches)!=1:raise ValueError('anniversary unique name OBJ')
        a,b,k=struct.unpack_from('<HHH',o,matches[0]*8)
        if a&0x2300 or a>>14!=2 or b>>14!=0 or (b&511,a&255)!=(88+i*8,41):raise ValueError('anniversary name geometry')
        for yy,line in enumerate(unpack_pixels(record)):
            for xx,role in enumerate(line):colors.setdefault(role,set()).add(im.getpixel(((b&511)+xx,(a&255)+yy)))
        cells.append(dict(cell=i,character=word[i] if i<len(word) else ' ',xy=[b&511,a&255],record_sha256=sha(record)))
    if set(colors)!={1,3,4} or any(len(s)!=1 for s in colors.values()) or len({next(iter(s)) for s in colors.values()})!=3:raise ValueError('anniversary name full mask/blank clear')
    return dict(word=word,encoded_hex=body.hex(),raw_bytes=len(body),name_field_bytes=22,logical_cells=len(word),display_cells=10,stage_vram_bytes=640,visible_cells=cells,screenshot_sha256=sha((p/(cp+'.png')).read_bytes()))

def query_name(p,word,rom,m):
    cp='step_004';calls=read(p/(cp+'_fixedcells.json'))['calls'];wanted=[ord(ch)-0xAC00 for ch in word]
    matches=[c for c in calls if c['target']==0x0600A000 and [g['index'] for g in c['glyphs'][:len(word)]]==wanted]
    if len(matches)!=1:raise ValueError('anniversary query name population')
    c=matches[0];count=len(word)+10
    # Source script72 prints buffer1, then ten literal blanks. Its transfer
    # includes name+ten cells, while the row tilemap exposes only ten cells.
    if not c['complete'] or c['bytes']!=count*64 or len(c['glyphs'])!=count or c['bytes']>0x400 or c['copy_target']!=c['target'] or c['copy_source']!=c['stage']:raise ValueError('anniversary query transfer/next-row capacity')
    fc=m['fixedcell_extension']['mono_provider'];glyphs=bdf_cells(ROOT/fc['font']['path'],set(word),fc['raster']);records=[]
    for i,g in enumerate(c['glyphs']):
        at=g['font']-0x08000000+g['index']*64;record=rom[at:at+64]
        if i<len(word):
            if g['font']!=0x08000000+fc['font_offset'] or record!=glyphs[word[i]]:raise ValueError('anniversary query glyph supply')
        elif g['index']!=0 or g['font']!=0x08619EF8:raise ValueError('anniversary query blank clear')
        if g['destination']!=c['stage']+i*64:raise ValueError('anniversary query contiguous staging')
        records.append(record)
    stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();v=(p/(cp+'_gbaVideoRam.bin')).read_bytes()
    if stage!=b''.join(records) or v[0xA000:0xA000+len(stage)]!=stage:raise ValueError('anniversary query stage/VRAM')
    io=(p/(cp+'_display_io.bin')).read_bytes();state=read(p/(cp+'_state.json'))['state'];control=struct.unpack_from('<H',io,12)[0]
    if control!=0x1E4A or any(state[f'ppu.bgLayers[2].scroll{x}'] for x in ['X','Y']):raise ValueError('anniversary query BG2 geometry')
    im=Image.open(p/(cp+'.png')).convert('RGB');colors={}
    for i in range(10):
        entries=[struct.unpack_from('<H',v,0xF000+(5+y)*64+(15+i)*2)[0] for y in [0,1]]
        if entries!=[0xA100+i*2,0xA101+i*2]:raise ValueError('anniversary query BG tilemap consumer')
        rendered=b''.join(v[0x8000+(k&1023)*32:0x8000+(k&1023)*32+32] for k in entries)
        if rendered!=records[i]:raise ValueError('anniversary query visible cell')
        for yy,line in enumerate(unpack_pixels(rendered)):
            for xx,role in enumerate(line):colors.setdefault(role,set()).add(im.getpixel((120+i*8+xx,40+yy)))
    if set(colors)!={1,3,4} or any(len(x)!=1 for x in colors.values()) or len({next(iter(x)) for x in colors.values()})!=3:raise ValueError('anniversary query screenshot masks/clearing')
    return dict(word=word,script=72,renderer='BG2 fixed-cell mono',decoded_cells=count,transfer_bytes=len(stage),next_row_gap_bytes=0x400-len(stage),visible_cells=10,visible_pixels=1280,screen_origin=[120,40],screenshot_sha256=sha((p/(cp+'.png')).read_bytes()))

def main():
    prior.STEM=STEM;prior.PREFIX=PREFIX;prior.OUTDIR=OUTDIR
    result=prior.main(anniversary_confirmation=True)
    m,rom,e,streams,_=static(STEM,'665698');pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='665698');a=read(ROOT/DIALOGUE);validate(a);validate(read(ROOT/LABELS));units={u['id']:u for u in a['units']};rt=ROOT/'poc/runtime';proofs=[];branches={}
    unchanged='0000000101060000000000000000000000000000000000000000000000000000'
    for kind,word in [('self','생일'),('school','개교기념일')]:
        name='anniversary-'+kind+'-accept';p,_=ancestry.checked_route(name,'register-anniversary-accept' if kind=='self' else 'anniversary-second',m,pool)
        dialogue=pages.exact_page(p,2,33,[f'665698:33:{i}' for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(30,))
        fixed=fixed_name(p,2,word,rom,m)
        o=(p/'step_002_gbaSpriteRam.bin').read_bytes();cur=struct.unpack_from('<HHH',o,30*8)
        if (cur[0]&255,cur[1]&511,cur[2]&1023,cur[2]>>12)!=(136,85,1020,14):raise ValueError('anniversary default Yes focus')
        for suffix,parent in [('no-focus',name),('no-accept',kind+'-no-focus'),('b-cancel',name),('yes-accept',name)]:
            q,_=ancestry.checked_route(kind+'-'+suffix,parent,m,pool);ram=(q/'step_002_gbaExtWorkRam.bin').read_bytes();record=ram[0x1310:0x1330]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool:raise ValueError('anniversary branch native root')
            if suffix=='no-focus':
                o=(q/'step_002_gbaSpriteRam.bin').read_bytes();cur=struct.unpack_from('<HHH',o,30*8)
                if ram[0xFA21]!=33 or (cur[0]&255,cur[1]&511,cur[2]&1023,cur[2]>>12)!=(136,121,1020,14):raise ValueError('anniversary No focus')
            if suffix!='yes-accept' and record.hex()!=unchanged:raise ValueError('anniversary cancel changed record')
            if suffix in ('no-accept','b-cancel') and ram[0xFA21]!=31:raise ValueError('anniversary cancel must return to type31')
            if suffix=='yes-accept':
                body=encode_hangul(word)+b'\xe5'
                header=bytes.fromhex('350000010106000000')+bytes([0 if kind=='self' else 1])
                if ram[0xFA21]!=0 or record[:10]!=header or record[10:10+len(body)]!=body or record[10+len(body):]!=bytes(22-len(body)):raise ValueError('anniversary committed header/name/terminator/tail')
            branches[kind+'-'+suffix]=dict(script=ram[0xFA21],record=record.hex(),screenshot_sha256=sha((q/'step_002.png').read_bytes()))
        query=rt/(PREFIX+kind+'-query');r=verify_route(query,m['output_sha256'],set())
        if r['state_origin']!=str(rt/(PREFIX+kind+'-yes-accept')/'result.json'):raise ValueError('anniversary query ancestry')
        committed=bytes.fromhex(branches[kind+'-yes-accept']['record']);qram=(query/'final_gbaExtWorkRam.bin').read_bytes()
        if qram[0x1310:0x1330]!=committed:raise ValueError('anniversary query record changed')
        query_proof=query_name(query,word,rom,m)
        proofs.append(dict(kind=kind,dialogue=dialogue,fixed_name=fixed,committed_record=committed.hex(),query_record_preserved=True,query_script=qram[0xFA21],same_session_query=query_proof))
    out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(720,320));shots=[('anniversary-self-accept',2),('self-no-focus',2),('self-yes-accept',2),('anniversary-school-accept',2),('school-no-focus',2),('school-yes-accept',2)]
    for i,(name,step) in enumerate(shots):sheet.paste(Image.open(rt/(PREFIX+name)/f'step_{step:03}.png'),(i%3*240,i//3*160))
    sheet.save(out/'anniversary_confirmation.png');result.update(anniversary_confirmation_pages=proofs,anniversary_confirmation_branches=branches,new_literal_units=5,selected_text_units=2304)
    query_sheet=Image.new('RGB',(480,160))
    for i,kind in enumerate(['self','school']):query_sheet.paste(Image.open(rt/(PREFIX+kind+'-query')/'step_004.png'),(i*240,0))
    query_sheet.save(out/'anniversary_queries.png')
    result['limits']+=['Birthday/school default names and confirmation33 tested on 1 January; both committed32-byte records and same-session BG2 list names verified. Query transfers12/15 cells (name+ten source blanks), within1024-byte row intervals. Native keyboard, arbitrary Hangul editing, anniversary native-save/cold reload and old-save compatibility remain open. Original Japanese 正月 holiday/date weekday labels remain untranslated.']
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Anniversary two preset names + confirmation33 + Yes/No/B + commit records: PASS');return result
if __name__=='__main__':main()
