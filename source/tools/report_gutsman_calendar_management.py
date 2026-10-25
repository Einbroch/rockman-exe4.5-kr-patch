"""Finite management selection, normal deletion pages and RAM-name glyph evidence."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels
from report_gutsman_calendar_register import exact_page
import report_gutsman_calendar_navigation as prior
import report_gutsman_calendar_confirmation as ancestry
from run_gutsman_calendar_management import STEM,PREFIX,OUTDIR,ROUTES
from gutsman_calendar_management import CHILD,validate
from korean_codec import encode_character
from build_visibility_poc import bdf_glyphs

def ram_name(p,step,word,m,rom):
    cp=f'step_{step:03}';obs=read(p/(cp+'_roll_pet.json'));ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();bias=m['extension']['legacy_index_view'];wanted=[ord(c)-0xAC00+bias for c in word]
    draws=[d for d in obs['draws'] if 0x02000000<=d['stream']<0x02040000 and d['glyph_index'] in wanted]
    last={d['stream']:d for d in draws};draws=sorted(last.values(),key=lambda d:d['offset'])
    if len(draws)!=len(word) or [d['glyph_index'] for d in draws]!=wanted:raise ValueError('anniversary deletion real RAM name draw population')
    font=m['extension']['normal_font_offset'];glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],set(word));expected={};advance=19
    for ch,d in zip(word,draws):
        offset=d['stream']-0x02000000;index=d['glyph_index'];record=rom[font+index*96:font+(index+1)*96]
        if ram[offset:offset+4]!=encode_character(ch) or record!=glyphs[ch] or d['context']!=0x0200FA20 or d['offset']!=10752+advance*4:raise ValueError('deletion RAM/name/quote geometry/font')
        expected[d['stream']]=dict(ch=ch,index=index,record=record,id='dynamic-anniversary-name',script=52)
        advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
    reads={v['index']:v['reads'] for v in obs['font_reads']};counts=Counter(d['glyph_index'] for d in draws)
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('deletion dynamic name CPU font reads')
    return dict(word=word,ram_streams=[d['stream'] for d in draws],actual_CPU_draws=True,**pixels(p,step,draws,expected,rom,m,origin=(52,110),cursor_indices=()))

def main(schedule_delete=False,frequency_names=False):
    prior.STEM=STEM;prior.PREFIX=PREFIX;prior.OUTDIR=OUTDIR;result=prior.main(management=True,schedule_delete=schedule_delete,frequency_names=frequency_names)
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset']for a in m['archives']if a['archive']=='665698');asset=read(ROOT/CHILD);validate(asset);units={u['id']:u for u in asset['units']};ancestry.PREFIX=PREFIX
    paths={}
    for name,parent,_ in ROUTES:
        p,r=ancestry.checked_route(name,parent,m,pool);env=read(p/'calendar_prompts_environment.json')
        if env.get('management_observer_sha256')!=sha((ROOT/'tools/capture_gutsman_calendar_management.py').read_bytes()) or env.get('additional_stream_range')!=[0x02000000,0x02040000]:raise ValueError('management observer provenance')
        paths[name]=p
    pages=[exact_page(paths['delete-selector'],5,5,[f'665698:5:{i}'for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(16,)),exact_page(paths['delete-first-page'],2,52,['665698:52:3'],m,rom,e,streams,pool,units),exact_page(paths['delete-confirm'],2,52,[f'665698:52:{i}'for i in [4,5,6]],m,rom,e,streams,pool,units,cursor_indices=(1,))]
    for name,x in [('delete-confirm',85),('delete-no-focus',121)]:
        o=(paths[name]/'step_002_gbaSpriteRam.bin').read_bytes();a,b,c=struct.unpack_from('<HHH',o,8)
        if (a&255,b&511,c&1023,c>>12,a>>14,b>>14)!=(136,x,1020,14,0,1):raise ValueError('deletion native choice index1/position/shape')
    dynamic=ram_name(paths['delete-first-page'],2,'생일',m,rom)
    # The choice page must clear the prior dynamic event name and prose.
    im=Image.open(paths['delete-confirm']/'step_002.png').convert('RGB');bg=im.getpixel((233,124))
    if any(im.getpixel((x,y))!=bg for y in range(124,136) for x in range(52,234)):raise ValueError('delete confirmation did not clear name row')
    pre=(paths['delete-confirm']/'step_002_gbaExtWorkRam.bin').read_bytes()[0x1310:0x1330];branches={}
    for name in ['delete-no-accept','delete-b-cancel','delete-yes-accept']:
        p=paths[name];ram=(p/'step_002_gbaExtWorkRam.bin').read_bytes();record=ram[0x1310:0x1330]
        if name!='delete-yes-accept' and record!=pre:raise ValueError('deletion cancellation changed birthday record')
        if name=='delete-yes-accept' and (pre==bytes(32) or record!=bytes(32)):raise ValueError('deletion Yes did not clear birthday record')
        branches[name]=dict(record=record.hex(),record_changed=record!=pre,screenshot_sha256=sha((p/'step_002.png').read_bytes()))
    observed={f'665698:5:{i}'for i in range(3)}|{f'665698:52:{i}'for i in [3,4,5,6]};extra=[]
    # Record only scenes whose real script/root and complete draws were observed.
    for name in ['overwrite-candidate','overwrite-after-confirm','help-navigation']:
        p=paths[name]
        for ramfile in sorted(p.glob('step_*_gbaExtWorkRam.bin')):
            step=int(ramfile.name[5:8]);ram=ramfile.read_bytes();script=ram[0xFA21]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or script not in [30,32,40,41,42,43,44,45]:continue
            keys=[u['id']for u in asset['units'][22:]if int(u['id'].split(':')[1])==script];obs=read(p/f'step_{step:03}_roll_pet.json');seen={d['stream']for d in obs['draws']}
            if keys and all(set(streams[k])<=seen for k in keys):
                extra.append(exact_page(p,step,script,keys,m,rom,e,streams,pool,units,cursor_indices=(2,)if script==30 else ()));observed.update(keys)
    new={u['id']for u in asset['units'][22:]};out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(720,320));shots=[('delete-selector',5),('delete-first-page',2),('delete-confirm',2),('delete-no-focus',2),('delete-no-accept',2),('delete-yes-accept',2)]
    for i,(name,s) in enumerate(shots):sheet.paste(Image.open(paths[name]/f'step_{s:03}.png'),(i%3*240,i//3*160))
    sheet.save(out/'calendar_management.png');result.update(passed=True,management_static=checks,management_pages=pages+extra,dynamic_deletion_name=dynamic,deletion_branches=branches,management_added_literal_units=23,management_runtime_observed_units=sorted(observed),management_static_only_units=sorted(new-observed),limits=result['limits']+['Deletion uses one isolated test birthday on Jan1; native persistent deletion save/reload, old saves, arbitrary Hangul input and other event/name consumers unverified. Unobserved error/full/overwrite/place/help branches remain static-only, not runtime complete.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Management23 static; normal deletion pages/name/Yes/No/B: PASS');return result
if __name__=='__main__':main()
