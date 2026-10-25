"""Possessions aggregate, native nickname, one option, accept/B/reentry pixels."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_pet import main as regression
from report_gutsman_calendar_register import exact_page
import report_gutsman_calendar_confirmation as ancestry
from gutsman_calendar_inventory import CHILD,validate,ADDED,PROFILE,template
from run_gutsman_calendar_inventory import STEM,PREFIX,OUTDIR,ROUTES
def main():
    result=regression(stem=STEM,prefix=PREFIX,expected_counts=(2348,58,674),oldstem='exe45_ko_development_calendar_frequency_names_v1',outdir=OUTDIR,inventory_outdir='full_scope_'+OUTDIR,added_literal_units=3,changed_archives=('665698',))
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset']for a in m['archives']if a['archive']=='665698');asset=read(ROOT/CHILD);validate(asset);units={u['id']:u for u in asset['units']};ancestry.PREFIX=PREFIX;paths={}
    for name,parent,_ in ROUTES:
        p,r=ancestry.checked_route(name,parent,m,pool)
        if read(p/'calendar_prompts_environment.json').get('management_observer_sha256')!=sha((ROOT/'tools/capture_gutsman_calendar_management.py').read_bytes()):raise ValueError('inventory RAM observer provenance')
        paths[name]=p
    baseline=ROOT/'poc/runtime/calendar-frequency-names-v1-inventory-side-probe';verify_route(baseline,'9a635be2e6f26ff835bdafd742a2042143183c337e04dc1d5d77884a18bae06b',set());source_ram=(baseline/'step_002_gbaExtWorkRam.bin').read_bytes();source_obs=read(baseline/'step_002_roll_pet.json');native=source_ram[0x10AC0:0x10AC5]
    if native!=bytes.fromhex('9b9ba5b9e5')or source_ram[0xFA21]!=10:raise ValueError('pinned source nickname/scene')
    source_draws=[d for d in source_obs['draws']if 0x02010AC0<=d['stream']<0x02010AC4]
    if [d['offset']for d in source_draws]!=[132,176,220,264]:raise ValueError('source nickname prefix geometry')
    samples=[]
    for name in ['inventory','inventory-reenter']:
        p=paths[name];ram=(p/'step_002_gbaExtWorkRam.bin').read_bytes();obs=read(p/'step_002_roll_pet.json');key=[u['id']for u in ADDED]
        body=exact_page(p,2,10,key,m,rom,e,streams,pool,units,cursor_indices=(1,))
        if ram[0x10AC0:0x10AC5]!=native:raise ValueError('native nickname bytes changed')
        draws=[d for d in obs['draws']if 0x02010AC0<=d['stream']<0x02010AC4];expected={};font=m['extension']['normal_font_offset']
        if len(draws)!=4:raise ValueError('native nickname actual draw population')
        for i,d in enumerate(draws):
            idx=native[i]
            if d['stream']!=0x02010AC0+i or d['glyph_index']!=idx or d['context']!=0x0200FA20 or d['offset']!=(32+i*11)*4:raise ValueError('native nickname aggregate coordinates')
            record=rom[font+idx*96:font+(idx+1)*96];source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
            if record!=source[0x608758+idx*96:0x608758+(idx+1)*96]:raise ValueError('native nickname font retained')
            expected[d['stream']]=dict(ch=f'native-byte-{idx:02x}',index=idx,record=record,id='native-nickname',script=10)
        reads={x['index']:x['reads']for x in obs['font_reads']};counts=Counter(d['glyph_index']for d in draws)
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('native nickname CPU font supply')
        nickname=pixels(p,2,draws,expected,rom,m,origin=(52,110),cursor_indices=(1,))
        last={d['stream']:d for d in obs['draws']};prefix=[last[s]for s in streams[key[0]]];suffix=[last[s]for s in streams[key[1]]]
        if [d['offset']for d in prefix]!=[0,48,96]or suffix[0]['offset']!=304 or suffix[1]['offset']!=10752:raise ValueError('inventory exact aggregate prefix/name/suffix/newline')
        if last[streams[key[2]][0]]['offset']!=21536:raise ValueError('inventory native one-option row')
        a,b,c=struct.unpack_from('<HHH',(p/'step_002_gbaSpriteRam.bin').read_bytes(),8)
        if (a&255,b&511,c&1023,c>>12)!=(136,44,1020,14):raise ValueError('inventory native option cursor')
        samples.append(dict(route=name,body=body,nickname=nickname,nickname_width=44,total_first_row=88,static_prefix_suffix=44,source_first_row=88))
    branches={}
    for name,old in [('inventory-accept','inventory-source-accept'),('inventory-cancel','inventory-source-cancel')]:
        p=paths[name];bp=ROOT/'poc/runtime'/('calendar-frequency-names-v1-'+old);verify_route(bp,'9a635be2e6f26ff835bdafd742a2042143183c337e04dc1d5d77884a18bae06b',set());current=(p/'step_002_gbaExtWorkRam.bin').read_bytes();before=(bp/'step_002_gbaExtWorkRam.bin').read_bytes()
        if current[0xFA21]!=before[0xFA21]or current[0x10AC0:0x10AC5]!=native or current[0x1310:0x1330]!=before[0x1310:0x1330]:raise ValueError('inventory branch script/nickname/schedule isolation')
        if name=='inventory-accept' and Image.open(p/'step_002.png').convert('RGB').crop((1,104,239,155)).tobytes()!=Image.open(bp/'step_002.png').convert('RGB').crop((1,104,239,155)).tobytes():raise ValueError('native key-item empty screen changed')
        branches[name]=dict(script=current[0xFA21],schedule_record_unchanged=True,nickname_unchanged=True)
    calendar=paths['calendar'];retained=[exact_page(calendar,4,1,['665698:1:0'],m,rom,e,streams,pool,units),exact_page(calendar,5,2,[f'665698:2:{i}'for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(16,)),exact_page(paths['confirmation'],5,24,[f'665698:24:{i}'for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(2,)),exact_page(paths['delete-first'],2,50,['665698:50:5'],m,rom,e,streams,pool,units)]
    from calendar_frequency_names import raw
    p=paths['delete-first'];ram=(p/'step_002_gbaExtWorkRam.bin').read_bytes();obs=read(p/'step_002_roll_pet.json');body=raw('1회만')
    if ram[0x10C40:0x10C40+len(body)]!=body:raise ValueError('retained once frequency RAM buffer')
    expected={};draws=[];cursor=0x02010C40;advance=90;font=m['extension']['normal_font_offset'];reads={x['index']:x['reads']for x in obs['font_reads']}
    for ch in '1회만':
        idx=2 if ch=='1'else ord(ch)-0xAC00+m['extension']['legacy_index_view'];ds=[d for d in obs['draws']if d['stream']==cursor]
        if len(ds)!=1 or ds[0]['glyph_index']!=idx or ds[0]['offset']!=advance*4 or ds[0]['context']!=0x0200FA20 or reads.get(idx,0)<24:raise ValueError('retained once frequency actual RAM glyph')
        expected[cursor]=dict(ch=ch,index=idx,record=rom[font+idx*96:font+(idx+1)*96],id='retained-once-frequency',script=50);draws.append(ds[0]);cursor+=1 if ch=='1'else 4;advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+idx*4)[0]
    frequency=pixels(p,2,draws,expected,rom,m,origin=(52,110),cursor_indices=())
    out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(960,160))
    for i,name in enumerate(['inventory','inventory-accept','inventory-cancel','inventory-reenter']):sheet.paste(Image.open(paths[name]/'step_002.png'),(i*240,0))
    sheet.save(out/'inventory.png');result.update(passed=True,inventory_static=checks,inventory_samples=samples,inventory_branches=branches,retained_calendar_pages=retained,retained_once_frequency=frequency,inventory_runtime_observed_units=[u['id']for u in ADDED],limits=result['limits']+['Only captured native four-byte nickname; arbitrary Hangul name entry/all redisplays/persistent reload/old saves unverified. Native empty key-item accept route retained; populated inventory and acquisition unverified. Previous complete calendar/frequency/alarm runtime reports are not automatically transferred to this ROM; once-frequency sample only rerun here.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Possessions3 + aggregate/native nickname/one option/accept/B/reentry: PASS');return result
if __name__=='__main__':main()
