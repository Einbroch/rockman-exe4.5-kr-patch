"""Finite competition literal/RAM/font/OBJ pixel evidence, not tournament progress."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from report_roll_pet_license import literal_end
from run_roll_competition import STEM,PREFIX,OUTDIR

def main():
    m,rom,e,streams,checks=static(STEM,'6615A8');ar=next(a for a in m['archives'] if a['archive']=='6615A8');pool=0x08000000+ar['rom_offset'];asset=read(ROOT/'translations/roll_competition_ko.json');units={u['id']:u for u in asset['units']};pages=[];covered=set()
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();oldm=read(ROOT/'poc/output/exe45_ko_development_dialogue_chip_name_v1.json');old=(ROOT/'poc/output/exe45_ko_development_dialogue_chip_name_v1.gba').read_bytes()
    if sha(old)!=oldm['output_sha256']:raise ValueError('previous baseline identity')
    # Relocation changes addresses; compare exact compiled payloads, not a
    # misleading whole-ROM byte diff that would exempt arbitrary tail edits.
    for previous in oldm['archives']:
        current=next(a for a in m['archives'] if a['archive']==previous['archive'])
        if (current['compiled_sha256']!=previous['compiled_sha256'] or current['translated_units']!=previous['translated_units'] or rom[current['rom_offset']:current['rom_offset']+current['compiled_bytes']]!=old[previous['rom_offset']:previous['rom_offset']+previous['compiled_bytes']]):raise ValueError('previous dialogue payload changed')
    if len(m['archives'])!=17 or m['translated_units']!=1065:raise ValueError('build denominator')
    for script in [1,2,10,20,21,22,23]:
        path=ROOT/'poc/runtime'/(PREFIX+f'script{script}');receipt=verify_route(path,m['output_sha256'],set());env=read(path/'competition_environment.json')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256']:raise ValueError('alias evidence')
        if env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or receipt.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in receipt['artifacts'] or receipt['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+'roll-intro')/'result.json'):raise ValueError('quarantine/parent identity')
        for file,key in [('capture_roll_competition.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256'),('capture_roll_return.py','ram_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer drift')
        groups=[(2,[0]),(4,[1])] if script==1 else [(2,[0]),(4,[1]),(6,[2])] if script==2 else [(2,[0])] if script==10 else [(2,[0,1])]
        for step,literals in groups:
            cp=f'step_{step:03}';state=read(path/(cp+'_roll_pet.json'));ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();keys=[f'6615A8:{script}:{i}' for i in literals];selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in state['draws'] if d['stream'] in selected};expected=dict(e);native=[]
            if set(last)!=set(selected) or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or state['calls']!=[{'frame':8,'root':pool,'script':0,'lr':0x08037F27}]:raise ValueError('native consumer/literal coverage')
            has_name=(script==2 and literals==[1]) or script in [10,20,21,22,23]
            if has_name:
                native=list({d['stream']:d for d in read(path/(cp+'_talk_ram.json'))['draws']}.values());native.sort(key=lambda d:d['stream']);start_row=1 if script>=20 else 0
                if len(native)!=4 or ram[native[0]['stream']-0x02000000:native[0]['stream']-0x02000000+5]!=bytes.fromhex('9b9ba2cae5'):raise ValueError('source-native nickname bytes')
                for i,d in enumerate(native):
                    index=ram[d['stream']-0x02000000];record=source[0x608758+index*96:0x608758+(index+1)*96]
                    if d['stream']!=native[0]['stream']+i or d['glyph_index']!=index or d['offset']!=start_row*10752+i*44 or d['context']!=0x0200FA20 or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record or struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]!=11:raise ValueError('nickname font/geometry')
                    expected[d['stream']]={'ch':'native nickname','index':index,'record':record,'id':'native_RAM_nickname'}
            for key in keys:
                row,advance=(1,44) if script>=20 and key.endswith(':1') else (0,44) if has_name and script<20 else (0,0);cursor=iter(streams[key])
                for ch in units[key]['translation']:
                    if ch=='\n':row+=1;advance=0;continue
                    stream=next(cursor)
                    if last[stream]['offset']!=row*10752+advance*4:raise ValueError('literal combined geometry')
                    advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
            end=literal_end(rom,streams[keys[-1]],e)
            if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('protected key wait')
            draws=[last[s] for s in selected]+native;counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('font CPU consumption')
            proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
            for d in draws:
                row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
            vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
            if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('stale text pixels')
            pages.append({'script':script,'step':step,'units':keys,'nickname':has_name,'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});covered.update(keys)
    if covered!=set(units):raise ValueError('finite selected scope incomplete')
    from bench_dialogue_chip_name import main as bench
    b=bench(STEM,OUTDIR)
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'previous_16_archive_payloads_identical':True,'normal_runtime_units':[],'diagnostic_renderer_units':sorted(covered),'pages':pages,'name_selector_cpu_vectors':b['vectors'],'limits':['Seven pointer/table read alias routes, not native tournament entry/results/flag progression.','Native nickname ああくん only; not Hangul keyboard/input or arbitrary nickname population.','Prior name selector retained and synthetic CPU checked; no new native chip-quest progression proof.','No audio/save/RTC/hardware/full-game/release or human wording approval.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'competition_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'passed':True,'units':len(covered),'pages':len(pages)}));return result

if __name__=='__main__':main()
