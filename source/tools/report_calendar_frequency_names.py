"""Frequency source->E5 stage->32byte text buffer->CPU/font/VRAM/pixels."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels
from archive_scripts import script_spans,verify_untouched_scripts
from calendar_frequency_names import CHILD,validate,raw,ADDED
from run_calendar_frequency_names import STEM,PREFIX,OUTDIR,KINDS
import report_gutsman_calendar_schedule_delete as regression
import report_gutsman_calendar_confirmation as ancestry
import report_gutsman_calendar_anniversary_confirmation as ann
from report_gutsman_calendar_register import exact_page
from build_visibility_poc import bdf_glyphs
def main():
    regression.STEM=STEM;regression.PREFIX=PREFIX;regression.OUTDIR=OUTDIR;result=regression.main(frequency_names=True)
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));rom=rp.read_bytes();a=next(a for a in m['archives']if a['archive']=='6368E8');pool=0x08000000+a['rom_offset'];payload=rom[a['rom_offset']:a['rom_offset']+a['compiled_bytes']];sp=script_spans(payload,255);asset=read(ROOT/CHILD);validate(asset);source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    protected=verify_untouched_scripts(source[0x6368E8:0x6368E8+2337],payload,255,{int(u['id'].split(':')[1])for u in asset['units']})
    if len(protected)!=243 or a['translated_units']!=12 or not a['protected_controls_unchanged']or not a['binary_roundtrip']:raise ValueError('frequency selected scope/controls')
    for i,u in enumerate(ADDED,119):
        if sp[i]!=raw(u['translation']):raise ValueError('frequency compiled rawE5/32 extent')
    fm=m['extension'];font=fm['normal_font_offset'];bias=fm['legacy_index_view'];glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],{c for u in ADDED for c in u['translation']if c!='1'})
    dm,_,e,streams,_=static(STEM,'665698');dpool=0x08000000+next(a['rom_offset']for a in m['archives']if a['archive']=='665698');ancestry.PREFIX=PREFIX;rt=ROOT/'poc/runtime';samples=[]
    units={u['id']:u for u in read(ROOT/'translations/gutsman_calendar_schedule_delete_ko.json')['units']}
    for i,(kind,u) in enumerate(zip(KINDS,ADDED),119):
        name='frequency-'+kind+'-first';parent='schedule-delete-list'if kind=='once'else'frequency-'+kind+'-list';p,r=ancestry.checked_route(name,parent,m,dpool);env=read(p/'calendar_prompts_environment.json')
        if env.get('frequency_observer_sha256')!=sha((ROOT/'tools/capture_calendar_frequency_copy.py').read_bytes())or env.get('frequency_write_range')!=[0x02010C40,0x02010CC0]:raise ValueError('frequency observer provenance')
        obs=read(p/'step_002_frequency_copy.json');data=raw(u['translation']);at=pool+struct.unpack_from('<H',payload,i*2)[0]
        if len(obs['lookups'])!=1 or (obs['lookups'][0]['r0'],obs['lookups'][0]['r1'],obs['lookups'][0]['r2'])!=(pool,i,0x02014E54):raise ValueError('frequency native lookup id/root/stage')
        if len(obs['stages'])!=1 or (obs['stages'][0]['source'],obs['stages'][0]['target'],obs['stages'][0]['bytes'])!=(at,0x02014E54,len(data)):raise ValueError('frequency E5 source copy')
        stage=bytes.fromhex(obs['stages'][0]['hex32']);transfers=[x for x in obs['transfers']if x['bytes']==32]
        if stage[:len(data)]!=data or len(transfers)!=1 or (transfers[0]['source'],transfers[0]['target'],transfers[0]['lr'])!=(0x02014E54,0x02010C40,0x08051805)or bytes.fromhex(transfers[0]['hex32'])!=stage:raise ValueError('frequency native32 transfer')
        if [(x['address'],x['value'])for x in obs['reads']]!=[(at+j,b)for j,b in enumerate(data)]:raise ValueError('frequency exact ROM reads')
        writes={x['address']:x['value']for x in obs['writes']}
        if writes!={0x02010C40+j:b for j,b in enumerate(stage)}:raise ValueError('frequency copied32 target bytes')
        ram=(p/'step_002_gbaExtWorkRam.bin').read_bytes()
        if ram[0x10C40:0x10C60]!=stage or ram[0xFA21]!=50:raise ValueError('frequency residency and normal50')
        pet=read(p/'step_002_roll_pet.json');draws=[];expected={};cursor=0x02010C40;advance=90
        for ch in u['translation']:
            index=2 if ch=='1'else ord(ch)-0xAC00+bias;size=1 if ch=='1'else 4
            ds=[d for d in pet['draws']if d['stream']==cursor]
            if len(ds)!=1 or ds[0]['glyph_index']!=index or ds[0]['context']!=0x0200FA20 or ds[0]['offset']!=advance*4:raise ValueError('frequency actual RAM draw/index/geometry')
            record=rom[font+index*96:font+(index+1)*96]
            if record!=(source[0x608758+index*96:0x608758+(index+1)*96]if ch=='1'else glyphs[ch]):raise ValueError('frequency font supply')
            expected[cursor]=dict(ch=ch,index=index,record=record,id=u['id'],script=50);draws.append(ds[0]);advance+=struct.unpack_from('<I',rom,fm['advance_offset']+index*4)[0];cursor+=size
        reads={x['index']:x['reads']for x in pet['font_reads']};counts=Counter(d['glyph_index']for d in draws)
        if any(reads.get(k,0)<24*n for k,n in counts.items()):raise ValueError('frequency CPU font reads')
        proof=pixels(p,2,draws,expected,rom,m,origin=(52,110),cursor_indices=())
        body=exact_page(p,2,50,['665698:50:5'],m,rom,e,streams,dpool,units)
        samples.append(dict(kind=kind,id=u['id'],translation=u['translation'],lookup=obs['lookups'][0],stage=obs['stages'][0],transfer=transfers[0],raw_bytes=len(data),header_end_x=52+advance,body=body,**proof))
    names={}
    for kind,word in [('self','생일'),('school','개교기념일')]:
        p=rt/(PREFIX+'anniversary-'+kind+'-accept');q=rt/(PREFIX+kind+'-query')
        ancestry.checked_route('anniversary-'+kind+'-accept','register-anniversary-accept'if kind=='self'else'anniversary-second',m,dpool);ancestry.checked_route(kind+'-query',kind+'-yes-accept',m,dpool)
        names[kind]=dict(confirmation=ann.fixed_name(p,2,word,rom,m),query=ann.query_name(q,word,rom,m))
    out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(1200,160))
    for i,kind in enumerate(KINDS):sheet.paste(Image.open(rt/(PREFIX+'frequency-'+kind+'-first')/'step_002.png'),(i*240,0))
    sheet.save(out/'frequency_names.png')
    result.update(passed=True,frequency_names_samples=samples,frequency_static_units=5,frequency_runtime_observed_units=[u['id']for u in ADDED],frequency_native_copy_bytes=32,protected_calendar_scripts=len(protected),retained_anniversary_names=names,limits=result['limits']+['Five normal frequency names on committed meal deletion50 verified. Other consumers, holiday/date/weekday text and graphics, arbitrary Hangul entry, native persistent schedule reload and old saves remain unverified.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Five normal frequency lookup/copy/font/VRAM/pixels + retained names: PASS');return result
if __name__=='__main__':main()
