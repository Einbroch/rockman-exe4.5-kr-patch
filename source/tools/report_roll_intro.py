"""Roll first-meeting stream, page clearing, glyph pixels and exact-ROM QA."""
import struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route

def main(stem='exe45_ko_development_roll_intro_v1',prefix='roll-intro-v1-roll-',outdir='roll_intro_v1'):
    m,rom,expected,streams,checks=static(stem,'65F9AC');p=ROOT/('poc/runtime/'+prefix+'select-roll');receipt=verify_route(p,m['output_sha256'],set());ar=next(a for a in m['archives'] if a['archive']=='65F9AC');root=0x08000000+ar['rom_offset'];pages=[]
    for step in receipt['capture_steps']:
        cp=f'step_{step:03}';state=read(p/(cp+'_roll_pet.json'));ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes()
        if struct.unpack_from('<I',ram,0xFA50)[0]!=root or ram[0xFA21]!=1:continue
        cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
        for unit in ['65F9AC:1:0','65F9AC:1:1']:
            # Only the current literal page can supply a screenshot. The older
            # page's retained trace cannot make the newly cleared page pass.
            if not min(streams[unit])<=cursor<=max(streams[unit])+5:continue
            relevant=[d for d in state['draws'] if d['stream'] in streams[unit]];last={d['stream']:d for d in relevant}
            if set(last)!=set(streams[unit]):continue
            draws=[last[s] for s in streams[unit]];counts=Counter(expected[d['stream']]['index'] for d in draws);reads={r['index']:r['reads'] for r in state['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('intro full font CPU reads')
            proof=pixels(p,step,draws,expected,rom,m);pages.append({'step':step,'unit':unit,**proof,'screenshot_sha256':sha((p/(cp+'.png')).read_bytes())})
    if {x['unit'] for x in pages}!={'65F9AC:1:0','65F9AC:1:1'}:raise ValueError('two normal intro pages not fully observed')
    selected=[next(x for x in pages if x['unit']==u) for u in ['65F9AC:1:0','65F9AC:1:1']]
    if selected[1]['step']<=selected[0]['step']:raise ValueError('intro page progression/order')
    # Text rectangle that became blank must not retain earlier glyphs. The
    # second page consumes fewer columns than the first; verify the vacant
    # right-hand region has exactly the same window RGB as its empty row.
    im=Image.open(p/f"step_{selected[1]['step']:03}.png").convert('RGB')
    # x234 is the preserved native green window border, not text background.
    # Observed blank text interior ends at x233; do not count border as a stale glyph.
    bg=im.getpixel((231,132));tail={im.getpixel((x,y)) for x in range(202,234) for y in range(124,136)}
    if tail!={bg}:raise ValueError('intro previous-page tail/stale pixels')
    before=read(p/f"step_{selected[1]['step']:03}_roll_pet.json");exit_step=selected[1]['step']+1;after=read(p/f'step_{exit_step:03}_roll_pet.json');exit_ram=(p/f'step_{exit_step:03}_gbaExtWorkRam.bin').read_bytes();next_root=struct.unpack_from('<I',exit_ram,0xFA50)[0]
    if len(before['calls'])!=1 or before['calls'][0]['root']!=root or before['calls'][0]['script']!=1 or before['calls']!=after['calls'] or before['draws']!=after['draws'] or next_root==root:raise ValueError('intro native entry/exit root and trace lifetime')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,160))
    for i,page in enumerate(selected):sheet.paste(Image.open(p/f"step_{page['step']:03}.png"),(i*240,0))
    sheet.save(out/'first_meeting.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'pages':pages,'runtime_observed_units':['65F9AC:1:0','65F9AC:1:1'],'runtime_open_units':['65F9AC:2:0','65F9AC:2:1','65F9AC:2:2'],'previous_page_cleared':True,'limits':['Source script2 trigger and normal return/reinstallation path unverified; three drafts static only','Roll daily/date-based dialogue remains Japanese','Human meaning/visual approval, whole-game/hardware/audio/release QA pending']}
    result['native_entry']=before['calls'][0];result['exit']={'step':exit_step,'next_root':next_root,'old_draws_and_calls_stopped':True,'next_dialogue_untranslated':True}
    fortune=next((a for a in m['archives'] if a['archive']=='65FF3C'),None)
    if fortune and next_root==0x08000000+fortune['rom_offset']:
        result['exit']['next_dialogue_untranslated']=False
        result['exit']['next_dialogue_partially_translated']=True
        result['limits'][1]='Roll fortune archive partially translated; consult the exact-ROM fortune report for observed/open units'
    import json
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json');return result

if __name__=='__main__':main()
