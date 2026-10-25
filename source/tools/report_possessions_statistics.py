"""Native64-cell transfer, visible BG2 cells and untouched counter proof."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,verify_route
from build_visibility_poc import require_hash
from archive_scripts import script_spans
from possessions_statistics import validate,CHILD,ADDED,LABELS
from fixedcell_font import bdf_cells,unpack_pixels,pack_pixels
from korean_codec import encode_character
from run_possessions_statistics import STEM,PREFIX

def main(stem=STEM,prefix=PREFIX,outdir='possessions_statistics_v1'):
    STEM,PREFIX=stem,prefix
    m=read(ROOT/f'poc/output/{STEM}.json');rom=(ROOT/f'poc/output/{STEM}.gba').read_bytes()
    require_hash(ROOT/f'poc/output/{STEM}.gba',m['output_sha256']);require_hash(ROOT/f'poc/output/{STEM}_repro.gba',m['output_sha256'])
    validate(read(ROOT/CHILD));oldstem='exe45_ko_development_keyitem_empty_v1'
    old=(ROOT/f'poc/output/{oldstem}.gba').read_bytes();om=read(ROOT/f'poc/output/{oldstem}.json');require_hash(ROOT/f'poc/output/{oldstem}.gba',om['output_sha256'])
    ar=next(a for a in m['archives'] if a['archive']=='6368E8');oa=next(a for a in om['archives'] if a['archive']=='6368E8')
    payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];sp=script_spans(payload,255)
    osp=script_spans(old[oa['rom_offset']:oa['rom_offset']+oa['compiled_bytes']],255)
    if any(sp[i]!=osp[i] for i in range(255) if i!=80) or ar['translated_units']!=13:raise ValueError('one script80 delta only')
    text=ADDED['translation'];body=b''.join(bytes([0]) if c==' ' else encode_character(c) for c in text)
    if sp[80]!=body+b'\xe5':raise ValueError('translated64-cell literal / terminator')
    for a in om['archives']:
        if a['archive']=='6368E8':continue
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if n['compiled_sha256']!=a['compiled_sha256']:raise ValueError('previous58 payload drift')
    root=0x08000000+ar['rom_offset'];oldroot=0x08000000+oa['rom_offset']
    if len(ar['pointers'])!=15 or any(struct.unpack_from('<I',rom,p)[0]!=root for p in ar['pointers']):raise ValueError('all15 roots')
    cursor=root+struct.unpack_from('<H',payload,160)[0]
    source_cursor=oldroot+struct.unpack_from('<H',old,oa['rom_offset']+160)[0]
    spec=read(ROOT/'tools/specs/exe45_fixedcell_visibility_v1.json');require_hash(ROOT/spec['font']['path'],spec['font']['sha256'])
    cells=bdf_cells(ROOT/spec['font']['path'],set(text)-{' '},spec['raster']);font=0x08000000+m['fixedcell_extension']['font_offset'];encoded=[];records=[]
    for ch in text:
        provider=0x08601738 if ch==' ' else font;index=0 if ch==' ' else ord(ch)-0xAC00
        native=rom[provider-0x08000000+index*64:provider-0x08000000+(index+1)*64]
        expected=old[0x601738:0x601778] if ch==' ' else cells[ch]
        if native!=expected:raise ValueError('BDF/native space/provider supply')
        # Native copier adds tint4 to each palette nibble (all native roles0..2).
        pixels=unpack_pixels(native)
        if any(v not in (0,1,2) for row in pixels for v in row):raise ValueError('tint overflow/unexpected role')
        records.append(pack_pixels([[v+4 for v in row] for row in pixels]));encoded.append((cursor,index,provider));cursor+=1 if ch==' ' else 4
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);pages=[]
    for name in ['inventory','empty-close']:
        p=ROOT/'poc/runtime'/(PREFIX+name);verify_route(p,m['output_sha256'],set());cp='step_002'
        q=ROOT/'poc/runtime'/('keyitem-empty-v1-'+name);verify_route(q,om['output_sha256'],set())
        calls=read(p/(cp+'_fixedcells.json'))['calls'];ocalls=read(q/(cp+'_fixedcells.json'))['calls']
        match=[c for c in calls if c['stream']==encoded[0][0]];orig=[c for c in ocalls if c['stream']==source_cursor]
        if len(match)!=1 or len(orig)!=1:raise ValueError('one native statistics call')
        c=match[0];o=orig[0]
        for k,v in dict(stage=0x0201B800,target=0x0600A000,width=16,height=16,font=0x08601738,tint=4,bytes=4096,caller_lr=0x080554BA,complete=True).items():
            if c[k]!=v or o[k]!=v:raise ValueError('statistics source ABI/stage/target/extent')
        if c['copy_source']!=c['stage'] or c['copy_target']!=c['target'] or len(c['glyphs'])!=64:raise ValueError('statistics transfer boundary')
        for i,(g,expect) in enumerate(zip(c['glyphs'],encoded)):
            if (g['stream'],g['index'],g['font'])!=expect or g['destination']!=c['stage']+64*i:raise ValueError('native cell decode')
        staged=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();vram=(p/(cp+'_gbaVideoRam.bin')).read_bytes();ovram=(q/(cp+'_gbaVideoRam.bin')).read_bytes()
        if staged!=b''.join(records) or vram[0xA000:0xB000]!=staged:raise ValueError('font/tint/stage4096/VRAM')
        # Digits/Z and battle results use separate source scripts81/82, not headings.
        counter=[]
        for script,target,stage in [(81,0x0600B000,0x0201C800),(82,0x06013000,0x0201D800)]:
            cc=[x for x in calls if x['target']==target and x['stage']==stage and x['bytes']==2048]
            oo=[x for x in ocalls if x['target']==target and x['stage']==stage and x['bytes']==2048]
            if len(cc)!=1 or len(oo)!=1:raise ValueError('counter consumer population')
            actual=(p/f"fixed_{cc[0]['id']:04d}_stage.bin").read_bytes();prior=(q/f"fixed_{oo[0]['id']:04d}_stage.bin").read_bytes();start=target-0x06000000
            if actual!=prior or vram[start:start+2048]!=ovram[start:start+2048] or actual!=vram[start:start+2048]:raise ValueError('counter glyph/VRAM drift')
            counter.append(dict(script=script,stage=stage,target=target,bytes=2048,source_identical=True))
        state=read(p/(cp+'_state.json'))['state'];io=(p/(cp+'_display_io.bin')).read_bytes()
        if struct.unpack_from('<H',io,12)[0]!=0x1E4A or any(state[f'ppu.bgLayers[2].scroll{x}'] for x in ['X','Y']):raise ValueError('BG2 geometry')
        pal=(p/(cp+'_gbaPaletteRam.bin')).read_bytes();opal=(q/(cp+'_gbaPaletteRam.bin')).read_bytes()
        if pal[0x140:0x160]!=opal[0x140:0x160]:raise ValueError('native BG palette10')
        im=Image.open(p/(cp+'.png')).convert('RGB');oi=Image.open(q/(cp+'.png')).convert('RGB');colors={};ocolors={}
        for row in range(4):
            for col in range(10):
                entries=[struct.unpack_from('<H',vram,0xF000+(3+row*2+y)*64+(4+col)*2)[0] for y in (0,1)]
                if entries!=[0xA100+row*32+col*2,0xA101+row*32+col*2]:raise ValueError('BG2 four-row tilemap')
                record=b''.join(vram[0x8000+(k&1023)*32:0x8000+(k&1023)*32+32] for k in entries)
                oldrecord=b''.join(ovram[0x8000+(k&1023)*32:0x8000+(k&1023)*32+32] for k in entries)
                if record!=records[row*16+col]:raise ValueError('visible cell supply')
                for yy,line in enumerate(unpack_pixels(record)):
                    for xx,role in enumerate(line):colors.setdefault(role,set()).add(im.getpixel((32+col*8+xx,24+row*16+yy)))
                for yy,line in enumerate(unpack_pixels(oldrecord)):
                    for xx,role in enumerate(line):ocolors.setdefault(role,set()).add(oi.getpixel((32+col*8+xx,24+row*16+yy)))
        if set(colors)!={4,5,6} or any(len(x)!=1 for x in colors.values()) or colors!=ocolors or len({next(iter(x)) for x in colors.values()})!=3:raise ValueError('all5120 pixels incl blanks/stale Japanese/native palette')
        pages.append(dict(route=name,decoded_cells=64,transfer_bytes=4096,visible_cells=40,visible_pixels=5120,labels=list(LABELS),counter_proof=counter,screenshot_sha256=sha((p/(cp+'.png')).read_bytes())))
    sheet=Image.new('RGB',(480,160))
    for i,name in enumerate(['inventory','empty-close']):sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+name)/'step_002.png'),(i*240,0))
    sheet.save(out/'possessions_statistics.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_text_units=m['translated_units'],new_literal_units=1,new_visible_labels=4,protected_other_scripts=254,previous58_archive_payloads_identical=True,all15_roots_verified=True,pages=pages,limits=['Only observed zero-counters inventory path and B return; nonzero battle record not exercised.','Keyitem descriptions38, Hangul input/edit/commit/redisplays/fresh reload and old-save compatibility, RTC and whole-ROM completion remain open. Human wording/presentation review pending.'])
    if 'keyitem_rom' in m:
        result['new_literal_units']=0
        result['limits']=['Existing statistics labels regression on integrated keyitem ROM; zero counters only.','Keyitem clone has separate verification; Hangul input/persistence/old-save/whole-ROM/human review remain open.']
    (out/'statistics_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Statistics64 decoded/4096bytes/40cells/5120pixels/counters unchanged: PASS');return result
if __name__=='__main__':
    import report_keyitem_empty as prior
    prior.STEM=STEM;prior.PREFIX=PREFIX;prior.OUTDIR='possessions_statistics_v1';prior.RAWDIR=f'poc/build/{STEM}'
    prior.main(statistics=True);main()
