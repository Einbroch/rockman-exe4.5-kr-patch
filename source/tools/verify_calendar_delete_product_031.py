"""Actual031 Korean calendar50 literal/RAM font-OBJ-pixel and choice proof."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels,verify_route
from korean_codec import encode_hangul


def main():
    rp=ROOT/'poc/output/pending500_031_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');rt=ROOT/'poc/runtime';prefix='pending500-031-calendar-'
    parents=[('calendar','pending500-031-v1-complete'),('time',prefix+'calendar'),('meal',prefix+'time'),('selector',prefix+'meal'),('list',prefix+'selector'),('first',prefix+'list'),('confirm',prefix+'first'),('no',prefix+'confirm'),('cancel',prefix+'confirm'),('yes',prefix+'confirm'),('reentry',prefix+'no')];receipts=[]
    for name,parent in parents:
        folder=rt/(prefix+name);r=verify_route(folder,m['output_sha256'],set())
        if r['state_origin']!=str(rt/parent/'result.json') or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('031 product calendar normal ancestry')
        if any(s in (folder/'segment.lua').read_text(encoding='utf8') for s in ('emu.write','setState','AliasReads')):raise ValueError('031 product calendar intervention')
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
    carry=read('analysis/pending_insertion_500_031_carry_v1/preflight.json');record=next(r for r in carry['archives'] if r['archive']=='659CB8');asset=read(record['merged_asset']['path']);pool,units,expected,streams,ends=model(rom,m,cfg,'659CB8',50,record['script_count'],asset=asset);by={u['id']:u for u in units}
    if set(by)!={f'659CB8:50:{i}' for i in (5,6,7,8)}:raise ValueError('031 product calendar four new literals')
    body=encode_hangul('식사')+b'\xE5';registered=bytes.fromhex('03000001010602000002')+body+bytes(13);pages=[]
    font=m['extension']['normal_font_offset'];bias=m['extension']['legacy_index_view'];frequency=next(x for x in read('analysis/pending500_031_v1/frequency_cpu.json')['bodies'] if x['image']=='030' and x['frequency']==0)
    dynamic=[(0x02010AC0,0,0),(0x02010AC1,3,32),(0x02010B40,1,120),(0x02010B41,1,164),(0x02010BC0,94,240),(0x02010BC1,106,284),(0x02010C40,2,360),(0x02010C41,frequency['glyphs'][1],404),(0x02010C45,frequency['glyphs'][2],452),(0x02010CC0,bias+ord('식')-0xAC00,10828),(0x02010CC4,bias+ord('사')-0xAC00,10876)]
    def inspect(folder,step,keys,offsets,extra=None):
        data=read(folder/f'step_{step:03}_event_buffers.json');ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();wanted={s:expected[s] for key in keys for s in streams[key]}
        if extra:wanted.update(extra)
        ds={d['stream']:d for d in data['draws'] if d['stream'] in wanted}
        if set(ds)!=set(wanted) or any(d['glyph_index']!=wanted[s]['index'] or d['context']!=0x0200FA20 or d['offset']!=offsets[s] for s,d in ds.items()):raise ValueError('031 complete calendar literal/provider glyph offsets')
        if tuple(ram[0xFA38:0xFA3A])!=(52,110) or struct.unpack_from('<I',ram,0xFA50)[0]!=pool:raise ValueError('031 product calendar root/origin')
        reads={d['index']:d['reads'] for d in data['font_reads']};counts=Counter(e['index'] for e in wanted.values())
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('031 product calendar actual font CPU')
        proof=pixels(folder,step,list(ds.values()),wanted,rom,m,origin=(52,110));pages.append(dict(segment=folder.name,step=step,ids=keys,**proof));return ram
    def literal_offsets(key,row,width):
        result={};it=iter(streams[key])
        for ch in by[key]['translation']:
            if ch=='\n':row+=1;width=0;continue
            s=next(it);result[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
        return result
    first_key='659CB8:50:5';offsets=literal_offsets(first_key,1,19+24);offsets.update({a:o for a,i,o in dynamic});extra={a:dict(ch='native-calendar-value',index=i,record=rom[font+i*96:font+(i+1)*96],id='five-native-insertions') for a,i,o in dynamic}
    first=rt/(prefix+'first');ram=inspect(first,2,[first_key],offsets,extra)
    if ram[0x1310:0x1330]!=registered or ram[0x10CC0:0x10CC9]!=body or struct.unpack_from('<H',ram,0xFA84)[0]!=5 or struct.unpack_from('<I',ram,0xFA4C)[0]!=ends[first_key]:raise ValueError('031 native meal record/five-slot/source wait')
    cursor=ends[first_key]-0x08000000
    if rom[cursor:cursor+3]!=bytes.fromhex('e600f1'):raise ValueError('031 calendar wait/clear preserved')
    label_keys=['659CB8:50:7','659CB8:50:8'];prompt='659CB8:50:6';yes_x=85;no_x=yes_x+8+sum(struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0] for s in streams[label_keys[0]])
    choice_offsets=literal_offsets(prompt,0,0);choice_offsets.update(literal_offsets(label_keys[0],2,yes_x+8-52));choice_offsets.update(literal_offsets(label_keys[1],2,no_x+8-52))
    for name,step,x in [('confirm',2,yes_x),('no',2,no_x)]:
        folder=rt/(prefix+name);r=inspect(folder,step,[prompt]+label_keys,choice_offsets);o=(folder/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,c=struct.unpack_from('<HHH',o,8)
        if (a&255,b&511,c&1023,c>>12,a>>14,b>>14)!=(136,x,1020,14,0,1):raise ValueError('031 Korean option cursor')
        im=Image.open(folder/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((233,124))
        if any(im.getpixel((xx,yy))!=bg for yy in range(124,136) for xx in range(52,234)):raise ValueError('031 Korean choice clears old name row')
    outcomes={}
    for name,step in [('no',3),('cancel',2),('yes',2)]:
        r=(rt/(prefix+name)/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if r[0x1310:0x1330]!=(bytes(32) if name=='yes' else registered) or r[0xFA20]!=0:raise ValueError('031 Korean choice actual outcome')
        outcomes[name]=dict(record_deleted=name=='yes',dialogue_closed=True)
    inspect(rt/(prefix+'reentry'),2,[first_key],offsets,extra)
    dependencies=['tools/verify_calendar_delete_product_031.py','tools/capture_event_buffers_product_031.py','analysis/pending_insertion_500_031_carry_v1/preflight.json','analysis/pending500_031_v1/frequency_cpu.json']
    frozen_write(ROOT/'analysis/pending500_031_v1/calendar_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,new_Korean_literal_ids=sorted(by),native_Hangul_meal_registered=True,five_slot_residency=True,Korean_choices_and_clear=True,outcomes=outcomes,normal_reentry=True,receipts=receipts,dependencies={p:sha((ROOT/p).read_bytes()) for p in dependencies},visual_review_pending=True,release_eligible=False,limits=['Own031 normal calendar meal/once and four newRockman50 Korean literals only; other77archive layouts static, not all natural histories/Navi/loops.','No native save/reset/reload, Hangul keyboard integration, anniversary/imported title or full-game/semantic approval claim.']))
    print('031 actual four Korean calendar literals/five buffers/choices/Yes-No-B/reentry PASS',flush=True)


if __name__=='__main__':main()
