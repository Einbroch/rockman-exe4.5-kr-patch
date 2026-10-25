"""Two exact caller guards, actual native copy128/RAM/font/OBJ/screen, and exit."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_roll_pet_license import literal_end
from report_gutsman_schedule_alarm import alarm_pages
from report_gutsman_pet import main as pet_regression
from bench_dialogue_chip_name import main as bench
from build_visibility_poc import bdf_glyphs
from run_gutsman_chipquest import STEM,PREFIX,OUTDIR

def chip_pages(path,archive,m,rom,e,streams,pool):
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();h=m['dialogue_chip_name'];name=0x08000000+h['name_offset'];block=rom[h['name_offset']:h['name_offset']+128]
    if len(block)!=128 or sha(block)!=h['name_block_sha256'] or block[:h['name_bytes']].hex()!=h['name_hex'] or block[h['name_bytes']:]!=b'\xe5'*(128-h['name_bytes']):raise ValueError('bounded chip name block')
    isguts=archive=='66A844';unit_asset='gutsman_pet_chipquest_ko.json' if isguts else 'roll_pet_chipquest_ko.json';units={u['id']:u for u in read(ROOT/'translations'/unit_asset)['units']};keys=[f'{archive}:13:0',f'{archive}:13:1'] if isguts else ['664E28:13:1'];command=h['gutsman_command_stream'] if isguts else h['command_stream'];glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],set(h['name'][:-1]));pages=[]
    for step in [2,3]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(path/(cp+'_roll_pet.json'));proof=read(path/(cp+('_chip_selector.json' if isguts else '_name_selector.json')));chip=read(path/(cp+('_return_ram.json' if isguts else '_chip_draws.json')))['draws']
        if ram[0xFA21]!=0 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or len(proof['abi'])!=2 or [v['label'] for v in proof['abi']]!=['entry','continuation']:raise ValueError('actual chip entry/ABI crossings')
        if rom[command-0x08000000:command-0x08000000+4]!=bytes.fromhex('f9006801'):raise ValueError('protected printChip buffer0/chip104 precondition')
        # Buffer0 is the protected invocation argument. The completed-page RAM
        # snapshot contains the later increment to1, not the entry live-in.
        before,after=[v['regs'] for v in proof['abi']];expectedregs=list(before);expectedregs[0]=name;expectedregs[1]=0x02010AC0;expectedregs[2]=0;expectedregs[7]=before[5]+100
        if before[0]+before[1]!=h['native_name_stream'] or before[4]!=command or before[5]!=h['context'] or after!=expectedregs:raise ValueError('chip all-register/SP/LR ABI')
        copies=proof['copy_reads']
        if len(copies)!=128 or any(c['address']!=name+127-i or c['remaining']!=127-i or c['value']!=block[127-i] or c['source']!=name or c['destination']!=0x02010AC0 for i,c in enumerate(copies)) or ram[0x10AC0:0x10B40]!=block:raise ValueError('chip native128 copy/RAM residency')
        expected=dict(e);wanted={a for k in keys for a in streams[k]};last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted};draws=[];row=0;width=0
        if set(last)!=wanted or obs['calls']!=[dict(frame=8,root=pool,script=0,lr=0x08037F27)]:raise ValueError('literal coverage/native caller')
        def literal(key):
            nonlocal row,width
            it=iter(streams[key])
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;width=0;continue
                stream=next(it);d=last[stream]
                if d['context']!=0x0200FA20 or d['offset']!=row*10752+width*4:raise ValueError('chip combined literal geometry')
                width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0];draws.append(d)
                if width>132:raise ValueError('chip combined row overflow')
        if isguts:literal(keys[0])
        else:
            quote=command-1;d=next(d for d in obs['draws'] if d['stream']==quote)
            if d['glyph_index']!=146 or d['offset']!=0:raise ValueError('Roll source opening quote')
            expected[quote]=dict(ch='「',index=146,record=source[0x608758+146*96:0x608758+147*96],id='Roll preserved opening quote');draws.append(d);width=11
        if width!=11 or row!=(1 if isguts else 0) or len(chip)!=4:raise ValueError('chip insertion row/opening quote/population')
        cursor=0x02010AC0
        for ch,d in zip(h['name'],chip):
            index=2 if ch=='1' else ord(ch)-0xAC00+m['extension']['legacy_index_view'];record=source[0x608758+2*96:0x608758+3*96] if ch=='1' else glyphs[ch];advance=11 if ch=='1' else 12
            if d['stream']!=cursor or d['glyph_index']!=index or d['context']!=0x0200FA20 or d['offset']!=row*10752+width*4 or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record or struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]!=advance:raise ValueError('chip RAM codec/font/advance/geometry')
            expected[cursor]=dict(ch=ch,index=index,record=record,id='chip104 normal RAM reuse');draws.append(d);width+=advance;cursor+=1 if ch=='1' else 4
        if width!=58 or ram[cursor-0x02000000]!=0xE5:raise ValueError('chip name width/terminator')
        literal(keys[-1]);end=literal_end(rom,streams[keys[-1]],e)
        if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+5]!=bytes.fromhex('e600f1edff'):raise ValueError('protected chip keyWait/clear/waitHold')
        counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('chip CPU font read coverage')
        pp=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');occupied=set()
        for d in draws:
            rr,off=divmod(d['offset'],10752);x=92+off//4;y=110+rr*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
        a,b,k=struct.unpack_from('<HHH',(path/(cp+'_gbaSpriteRam.bin')).read_bytes(),0);arrow=set()
        if k&1023==1016 and k>>12==14:
            if (a,b)!=(141,16609):raise ValueError('chip unknown native arrow')
            arrow={(x,y) for y in range(141,157) for x in range(225,240)}
        if occupied&arrow:raise ValueError('chip glyph/native arrow overlap')
        baseline=Image.open(ROOT/'poc/runtime/numberman-intro-v1-select-numberman-full/step_008.png').convert('RGB')
        if any(im.getpixel((x,y))!=baseline.getpixel((x,y)) for y in range(110,140) for x in [234,235]):raise ValueError('chip right border')
        vacant={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied|arrow}
        if any(im.getpixel(xy)!=im.getpixel((231,112)) for xy in vacant):raise ValueError('chip stale pixels')
        pages.append(dict(route=path.name,step=step,units=keys,name=h['name'],name_width=47,combined_name_row_width=81 if isguts else 69,copy_bytes=128,all_registers_SP_LR_match_source_contract=True,vacant_pixels_cleared=len(vacant),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**pp))
    for step in [4,5]:
        if struct.unpack_from('<I',(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes(),0xFA50)[0]==pool:raise ValueError('chip dialogue exit')
    return pages

def main():
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2280,57,675),oldstem='exe45_ko_development_gutsman_pet_talk_v1',outdir=OUTDIR+'/pet_regression',inventory_outdir='full_scope_gutsman_chipquest_v1',added_literal_units=0,changed_archives=('66A844',))
    m,rom,e,s,c=static(STEM,'66A844');h=m['dialogue_chip_name'];rt=ROOT/'poc/runtime';pool=0x08000000+next(a for a in m['archives'] if a['archive']=='66A844')['rom_offset'];p=rt/(PREFIX+'normal-talk');r=verify_route(p,m['output_sha256'],set())
    if r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json') or any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','Aliases']):raise ValueError('normal own R ancestry/intervention')
    normal=alarm_pages(p,10,10,m,rom,e,s,pool,unit_asset='gutsman_pet_chipquest_ko.json');petpool=0x08000000+next(a for a in m['archives'] if a['archive']=='665F3C')['rom_offset'];ram=(p/'step_004_gbaExtWorkRam.bin').read_bytes()
    if ram[0xFA21]!=1 or struct.unpack_from('<I',ram,0xFA50)[0]!=petpool or read(p/'step_002_roll_pet.json')['draws']!=read(p/'step_004_roll_pet.json')['draws']:raise ValueError('normal R exit/menu')
    p=rt/(PREFIX+'chip13');r=verify_route(p,m['output_sha256'],set());env=read(p/'talk_environment.json')
    if not env['passed'] or not env['observer_only'] or env['entry_aliases']!=1 or env['script']!=13 or env['rom_sha256']!=m['output_sha256'] or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json') or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('Guts chip quarantine/ancestry')
    for f,k in [('capture_gutsman_chipquest.py','chip_wrapper_sha256'),('capture_gutsman_pet_talk_diagnostic.py','tool_sha256'),('capture_gutsman_pet_talk.py','observer_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
        if sha((ROOT/'tools'/f).read_bytes())!=env[k]:raise ValueError('Guts chip observer drift')
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    for g in env['native_guards']:
        if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('Guts native consumer drift')
    guts=chip_pages(p,'66A844',m,rom,e,s,pool)
    restored=alarm_pages(p,10,10,m,rom,e,s,pool,unit_asset='gutsman_pet_chipquest_ko.json')
    if [x['step'] for x in restored]!=[6]:raise ValueError('diagnostic alias one-shot reentry restoration')
    chain=read(rt/(PREFIX+'roll-select')/'roll_selection_chain.json');parent='normal-reload-select'
    if chain['rom_sha256']!=m['output_sha256']:raise ValueError('Roll selection exact ROM')
    for route in chain['routes']:
        q=rt/(PREFIX+route);receipt=verify_route(q,m['output_sha256'],set())
        if receipt['state_origin']!=str(rt/(PREFIX+parent)/'result.json') or receipt.get('normal_play_checkpoint_eligible') is False or any(x in (q/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','Aliases']):raise ValueError('Roll native selection ancestry')
        parent=route
    if parent!=chain['final_parent']:raise ValueError('Roll final parent')
    p=rt/(PREFIX+'roll-chip13');r=verify_route(p,m['output_sha256'],set());env=read(p/'name_selector_environment.json');alias=read(p/'license_environment.json')
    if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json') or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or not alias['passed'] or alias['aliases']!=1 or alias['displayed_entry']!=13:raise ValueError('Roll chip quarantine/ancestry')
    for f,k,record in [('capture_dialogue_chip_name.py','tool_sha256',env),('capture_roll_chipquest.py','base_wrapper_sha256',env),('capture_roll_pet_license.py','tool_sha256',alias),('capture_roll_pet_talk.py','observer_sha256',alias),('capture_roll_pet.py','probe_sha256',alias)]:
        if sha((ROOT/'tools'/f).read_bytes())!=record[k]:raise ValueError('Roll chip observer drift')
    _,_,re,rs,rc=static(STEM,'664E28');rp=0x08000000+next(a for a in m['archives'] if a['archive']=='664E28')['rom_offset'];roll=chip_pages(p,'664E28',m,rom,re,rs,rp)
    if rom[0x765190:0x765190+2437]!=source[0x765190:0x765190+2437] or any(rom[a:a+8]!=source[a:a+8] for a in [0x1F7F0,0x22AF8,0x3866C,0x3CB98,0x42F98,0x4CAA8,0x4E6A4,0x4E79C,0x51664]):raise ValueError('shared native name pool/root drift')
    b=bench(STEM,OUTDIR)
    if b['vectors']!=64:raise ValueError('two guards/fallback CPU vector population')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(960,160))
    for i,x in enumerate([guts[0],roll[0],normal[0],restored[0]]):sheet.paste(Image.open(rt/x['route']/f"step_{x['step']:03}.png"),(i*240,0))
    sheet.save(out/'chip_pages.png');result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],new_literal_units=2,new_name_wordings=0,selected_text_units=2280,static=c,pet_regression=baseline,normal_pages=normal,guts_chip_pages=guts,roll_chip_pages=roll,diagnostic_native_R_reentry=restored,synthetic_cpu_vectors=b['vectors'],remaining_catalog=baseline['remaining_catalog'],limits=['33/33 Guts R literal drafts selected, not whole ROM completion or human wording approval.','Guts13 and Roll13 use separate exact stream guards and shared existing chip104 name draft. Other name/context/stream combinations native; synthetic64 CPU vectors not every gameplay caller.','Chip pages are quarantined read-alias renderer evidence, not native quest progression/chip acquisition. Native source-name pool and nine shared root pairs unchanged.','Normal R10 + menu, NumberMan save/cold continue/Guts intro/PET regressions; other prior talk branches not rerun. Hangul name persistence/all redisplays/old-save compatibility, whole graphics/inline/fixed population/prior arrow53pixel remain open.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts33 static; Guts/Roll chip name ABI/copy128/font/VRAM/screen/exit and normal regressions PASS');return result

if __name__=='__main__':main()
