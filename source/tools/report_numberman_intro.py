"""Seven normal NumberMan intro pages, clearing, prior payloads and save edge."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route

STEM='exe45_ko_development_numberman_intro_v1'
PREFIX='numberman-intro-v1-'

def main():
    m,rom,e,streams,checks=static(STEM,'6872B8')
    if m['translated_units']!=1152 or len(m['archives'])!=22:raise ValueError('selected scope')
    old=ROOT/'poc/output/exe45_ko_development_numberman_save_poc_v1.gba';pm=read(old.with_suffix('.json'));pr=old.read_bytes()
    if sha(pr)!=pm['output_sha256']:raise ValueError('previous identity')
    for a in pm['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['compiled_sha256']!=n['compiled_sha256'] or pr[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('previous21 payload drift')
    if rom[0x6333A4:0x6334A4]!=pr[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    rt=ROOT/'poc/runtime';chain=['cold-part1','date','profile','navi-menu','select-numberman','intro']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],set())
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
    p=rt/(PREFIX+'select-numberman-full');receipt=verify_route(p,m['output_sha256'],set())
    if receipt['state_origin']!=str(rt/(PREFIX+'navi-menu')/'result.json'):raise ValueError('intro pre-load side route ancestry')
    ar=next(x for x in m['archives'] if x['archive']=='6872B8');pool=0x08000000+ar['rom_offset'];pages=[]
    for key in streams:
        found=None
        for step in receipt['capture_steps']:
            cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes()
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=1:continue
            cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if not min(streams[key])<=cursor<=max(streams[key])+5:continue
            obs=read(p/(cp+'_roll_pet.json'));last={d['stream']:d for d in obs['draws'] if d['stream'] in streams[key]}
            if set(last)!=set(streams[key]):continue
            draws=[last[x] for x in streams[key]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('actual glyph CPU reads')
            proof=pixels(p,step,draws,e,rom,m);im=Image.open(p/(cp+'.png')).convert('RGB');occupied=set()
            for d in draws:
                row,off=divmod(d['offset'],10752);x0=92+off//4;y0=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
                occupied.update((x,y) for y in range(y0,y0+12) for x in range(x0,x0+width))
            blank={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied and not(x>=220 and y>=140)}
            if {im.getpixel(xy) for xy in blank}!={im.getpixel((231,112))}:raise ValueError('cleared page vacant region')
            found={'unit':key,'step':step,'screenshot_sha256':sha((p/(cp+'.png')).read_bytes()),'vacant_pixels_cleared':len(blank),**proof};break
        if found is None:raise ValueError('unobserved complete intro page: '+key)
        pages.append(found)
    if len(pages)!=7 or any(b['step']<=a['step'] for a,b in zip(pages,pages[1:])):raise ValueError('seven ordered pages')
    laststep=pages[-1]['step'];before=read(p/f'step_{laststep:03}_roll_pet.json');after=read(p/f'step_{laststep+1:03}_roll_pet.json');ram=(p/f'step_{laststep+1:03}_gbaExtWorkRam.bin').read_bytes()
    if not any(c['root']==pool and c['script']==1 for c in before['calls']) or before['calls']!=after['calls'] or before['draws']!=after['draws'] or struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('native entry/exit lifetime')
    for name,parent in [('save-enter','intro'),('save-commit','save-enter')]:
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],set())
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json'):raise ValueError('save ancestry')
    commit=rt/(PREFIX+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';rtc=STEM+'.rtc';b=env['files_before'][sav];a=env['files_after'][sav]
    if not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or b!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or a['bytes']!=65536 or b==a or sha((commit/'persistent_files_after'/sav).read_bytes())!=a['sha256']:raise ValueError('native disk save')
    for name in set(env['files_before'])|set(env['files_after']):
        if name not in(sav,rtc) and env['files_before'].get(name)!=env['files_after'].get(name):raise ValueError('unrelated save changed')
    ram=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savear=next(x for x in m['archives'] if x['archive']=='6DA21C')
    if ram[0xFA21]!=58 or struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+savear['rom_offset']:raise ValueError('native success58')
    out=ROOT/'analysis/numberman_intro_v1';out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,640))
    for i,page in enumerate(pages):sheet.paste(Image.open(p/f"step_{page['step']:03}.png"),(i%2*240,i//2*160))
    sheet.save(out/'first_meeting.png');result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':7,'selected_text_units':1152,'static':checks,'previous21_payloads_identical':True,'pages':pages,'native_entry_exit':True,'save_before':b,'save_after':a,'save_success_script':58,'tool_sha256':sha((ROOT/'tools/report_numberman_intro.py').read_bytes()),'limits':['Return script2/4649 wordplay retained untranslated; trigger not tested.','Save edge/success, not persistence reload or old-save compatibility.','No Hangul input/full-game/RTC/audio/hardware/human release approval.']}
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('seven NumberMan intro pages/clearing/native save: PASS');return result

if __name__=='__main__':main()
