"""Finite GutsMan save prose and normal save/overwrite-cancel evidence."""
import json,struct
from collections import Counter
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from tpl_literals import resolve_units
from archive_scripts import script_spans

STEM='exe45_ko_development_gutsman_save_poc_v1'
PREFIX='gutsman-save-poc-v1-'

def main():
    m,rom,e,streams,checks=static(STEM,'6DA21C');ar=next(a for a in m['archives'] if a['archive']=='6DA21C');pool=0x08000000+ar['rom_offset']
    if m['translated_units']!=1129 or len(m['archives'])!=21:raise ValueError('selected denominator')
    for root in ar['pointers']:
        if struct.unpack_from('<I',rom,root)[0]!=pool:raise ValueError('save root')
    oldstem='exe45_ko_development_save_surface_poc_v1';oldm=read(ROOT/f'poc/output/{oldstem}.json');old=(ROOT/f'poc/output/{oldstem}.gba').read_bytes()
    if sha(old)!=oldm['output_sha256']:raise ValueError('previous artifact')
    if rom[0x6333A4:0x6334A4]!=old[0x6333A4:0x6334A4] or m['save_title_graphics']['final_block_sha256']!=oldm['save_title_graphics']['final_block_sha256']:raise ValueError('prior save title drift')
    for pointer in ar['pointers']:
        if struct.unpack_from('<I',rom,pointer)[0]!=pool:raise ValueError('all save roots')
    for before in oldm['archives']:
        now=next(a for a in m['archives'] if a['archive']==before['archive'])
        if before['archive']=='6DA21C':
            p=script_spans(old[before['rom_offset']:before['rom_offset']+before['compiled_bytes']],120)
            q=script_spans(rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']],120)
            if any(p[i]!=q[i] for i in range(120) if i not in range(25,30)):raise ValueError('previous 115 scripts')
        elif before['compiled_sha256']!=now['compiled_sha256'] or old[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]!=rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]:raise ValueError('previous20 archive payload drift')
    units=resolve_units(read(ROOT/'translations/rockman_roll_gutsman_save_ko.json'))
    if units[:37]!=resolve_units(read(ROOT/'translations/rockman_roll_save_surface_ko.json')):raise ValueError('previous37 translation drift')
    rt=ROOT/'poc/runtime';pages=[]
    cases=[('save-enter',11,25,['6DA21C:25:0','6DA21C:25:1','6DA21C:25:2']),('save-overwrite',6,26,['6DA21C:26:0']),('save-overwrite',9,26,['6DA21C:26:1','6DA21C:26:2']),('save-timing',8,27,['6DA21C:27:0']),('save-commit',7,28,['6DA21C:28:0'])]
    sheet=Image.new('RGB',(480,480))
    for i,(name,step,script,keys) in enumerate(cases):
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],set());cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));env=read(p/'save_environment.json')
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or not env['observer_only'] or env['self_sha256']!=sha((ROOT/'tools/capture_roll_save.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()):raise ValueError('observer/current save consumer')
        wanted=[s for key in keys for s in streams[key]];last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
        if set(last)!=set(wanted):raise ValueError('complete selected page')
        draws=[last[s] for s in wanted];counts=Counter(d['glyph_index'] for d in draws);reads={v['index']:v['reads'] for v in obs['font_reads']}
        if any(reads.get(index,0)<24*n for index,n in counts.items()):raise ValueError('CPU actual font reads')
        proof=pixels(p,step,draws,e,rom,m,cursor_indices=(0,) if script in (25,26) else ())
        pages.append({'route':p.name,'step':step,'script':script,'units':keys,'screenshot_sha256':sha((p/(cp+'.png')).read_bytes()),**proof});sheet.paste(Image.open(p/(cp+'.png')),(i%2*240,i//2*160))
    chain=['cold-part1','date','profile','navi-menu','select-gutsman','intro']
    for i,name in enumerate(chain):
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],set())
        if (i==0 and r['state_origin'] is not None) or (i and Path(r['state_origin']).resolve()!=(rt/(PREFIX+chain[i-1])/'result.json').resolve()):raise ValueError('fresh own-ROM cold route')
    for name,parent in [('save-enter','intro'),('save-commit','save-enter'),('save-overwrite','save-commit'),('save-timing','save-enter')]:
        if Path(read(rt/(PREFIX+name)/'result.json')['state_origin']).resolve()!=(rt/(PREFIX+parent)/'result.json').resolve():raise ValueError('save route ancestry')
    sav=STEM+'.sav';rtc=STEM+'.rtc';ce=read(rt/(PREFIX+'save-commit')/'save_environment.json');oe=read(rt/(PREFIX+'save-overwrite')/'save_environment.json');before=ce['files_before'][sav];after=ce['files_after'][sav]
    if before!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or after['bytes']!=65536 or before==after or sha((rt/(PREFIX+'save-commit')/'persistent_files_after'/sav).read_bytes())!=after['sha256']:raise ValueError('native disk save')
    if oe['files_before'][sav]!=after or oe['files_after'][sav]!=after:raise ValueError('overwrite No altered disk save')
    for env in (ce,oe,read(rt/(PREFIX+'save-timing')/'save_environment.json')):
        for name in set(env['files_before'])|set(env['files_after']):
            if name not in (sav,rtc) and env['files_before'].get(name)!=env['files_after'].get(name):raise ValueError('unrelated test saves changed')
    # Option focus No uses the native cursor; subsequent cancel returns to PET.
    ram=(rt/(PREFIX+'save-overwrite')/'step_011_gbaExtWorkRam.bin').read_bytes();o=(rt/(PREFIX+'save-overwrite')/'step_011_gbaSpriteRam.bin').read_bytes()
    if ram[0xFA21]!=26 or struct.unpack_from('<H',o,2)[0]&511!=144:raise ValueError('overwrite No focus')
    out=ROOT/'analysis/gutsman_save_poc_v1';out.mkdir(parents=True,exist_ok=True);sheet.save(out/'save_pages.png')
    observed=sorted({k for p in pages for k in p['units']});result={'passed':True,'policy':'functional-poc; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':16,'selected_units':1129,'static':checks,'previous20_payloads_identical':True,'previous115_save_scripts_identical':True,'pages':pages,'normal_observed_gutsman_units':observed,'open_gutsman_units':sorted({u['id'] for u in units[37:]}-set(observed)),'save_disk_before':before,'save_disk_after':after,'overwrite_No_preserves_disk':True,'tool_sha256':sha(Path(__file__).read_bytes()),'limits':['Failure/retry and invalid-data messages mechanically verified only; not induced in gameplay.','Prior save title/counter/labels retained byte-identically; their current GutsMan visible page is inspected, not full all-Navi verification.','Own normal GutsMan save and overwrite-cancel only; no fresh persistence reload on this successor.','Hangul name input/editing, old-save compatibility, full-game/RTC/audio/hardware and human release review remain open.']}
    (out/'save_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('GutsMan save normal pages/native disk edge/overwrite No: PASS');return result

if __name__=='__main__':main()
