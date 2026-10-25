"""Strict native PET default conversation font/VRAM/screen proof."""
import json,struct
from collections import Counter
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from run_roll_pet_talk import STEM,PREFIX,OUTDIR,ACTIONS

def talk_report():
    m,rom,e,streams,checks=static(STEM,'664E28');key='664E28:10:0';selected=streams[key];path=ROOT/'poc/runtime'/(PREFIX+'talk');r=verify_route(path,m['output_sha256'],set());project=read(ROOT/'project.json')
    if r['actions']!=ACTIONS or r['actions_total']!=3 or r['capture_steps']!=[1,2,3] or r['emulator_sha256']!=project['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('PET talk route/emulator identity')
    ar=next(a for a in m['archives'] if a['archive']=='664E28');pool=0x08000000+ar['rom_offset'];pages=[]
    source=(ROOT/project['source_profile']['filename']).read_bytes();nw=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    asset=next(a for a in m['translation_assets'] if a.get('archive')=='664E28')
    text=next(u for u in read(ROOT/asset['path'])['units'] if u['id']==key)['translation']
    for step in [2,3]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();s=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in s['draws'] if d['stream'] in selected}
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=10 or set(last)!=set(selected):raise ValueError('PET talk root/script/literal coverage')
        calls=s['calls']
        if len(calls)!=1 or calls[0]['root']!=pool or calls[0]['script']!=0 or calls[0]['lr']!=0x08037F27:raise ValueError('PET talk native entry0 jump10')
        native={d['stream']:d for d in read(path/(cp+'_talk_ram.json'))['draws']};ordered=[native[k] for k in sorted(native)];offset=0;nickname='';expected=dict(e)
        if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xE5:raise ValueError('PET talk native nickname span')
        for d in ordered:
            index=ram[d['stream']-0x02000000];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0];record=source[0x608758+index*96:0x608758+(index+1)*96]
            if index!=d['glyph_index'] or d['offset']!=offset or index not in codes or d['context']!=0x0200FA20 or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,nw+index*4)[0]:raise ValueError('PET talk nickname native font/advance/geometry')
            expected[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*advance
        draws=[last[k] for k in selected];row=0;advance=offset//4;cursor=iter(selected)
        for ch in text:
            if ch=='\n':row+=1;advance=0;continue
            stream=next(cursor);d=last[stream]
            if d['offset']!=row*10752+advance*4:raise ValueError('PET talk exact line geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
        counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in s['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('PET talk CPU font read coverage')
        proof=pixels(path,step,draws+ordered,expected,rom,m)
        end=max(selected)+1;position=struct.unpack_from('<I',ram,0xFA4C)[0]
        if rom[end-0x08000000:end-0x08000000+5]!=bytes.fromhex('e600f1edff') or position!=end:raise ValueError('PET talk native keyWait/clearMsg/waitHold boundary')
        pages.append({'step':step,'nickname':nickname,'nickname_width':offset//4,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),'native_entry_calls':calls,**proof})
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'normal_runtime_units':[key],'static':checks,'pages':pages,'limits':['Default exploration conversation only; other progress branches unverified.','Native captured nickname retained; Hangul name input/save not claimed.','Whole-game/hardware/audio/release QA pending.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'talk_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def main():
    import report_roll_subjects as subjects
    previous=subjects.STEM,subjects.PREFIX
    try:subjects.STEM=STEM;subjects.PREFIX=PREFIX;reports=subjects.main(OUTDIR)
    finally:subjects.STEM,subjects.PREFIX=previous
    reports.append(talk_report());expected=read(ROOT/f'poc/output/{STEM}.json')['output_sha256']
    if len(reports)!=15 or not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==expected for r in reports):raise ValueError('PET talk cumulative exact-ROM reports')
    (ROOT/'analysis'/OUTDIR/'cumulative_runtime.json').write_text(json.dumps({'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':expected,'reports_total':15},indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
