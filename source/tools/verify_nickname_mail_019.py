"""Six-character native-name interaction and first-mail CPU/OBJ/pixel proof."""
import argparse, json, struct
from collections import Counter
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT, require_hash, sha
from korean_codec import encode_hangul
from archive_scripts import script_spans
from report_roll_pet import pixels

def read(path): return json.loads(path.read_text(encoding='utf8'))

def main():
    p=argparse.ArgumentParser(); p.add_argument('--rom',type=Path,required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args()
    m=read(a.rom.with_suffix('.json')); require_hash(a.rom,m['output_sha256']); rom=a.rom.read_bytes()
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename']; require_hash(source,m['source_sha256']); native=source.read_bytes()
    entry=ROOT/'poc/runtime/pending500-019-native-name-six-v1'; mail=ROOT/'poc/runtime/pending500-019-native-name-six-mail-v1'
    evidence={}
    for folder in (entry,mail):
        r=read(folder/'result.json')
        if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['steps_captured']!=r['steps_expected']: raise ValueError('runtime receipt')
        for name,h in r['artifacts'].items(): require_hash(folder/name,h); evidence[str((folder/name).relative_to(ROOT))]=h
        evidence[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
    def ram(folder,step): return (folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
    editor=[]
    for step in range(16,25):
        data=ram(entry,step); expected_length=min(step-15,6) if step<=22 else (5 if step==23 else 6)
        if data[0xFC44]!=6 or struct.unpack_from('<I',data,0xFC58)[0]!=0x0200FC60+expected_length*2 or data[0xFC60:0xFC60+expected_length*2]!=b'\x9D\0'*expected_length or data[0xFC60+expected_length*2:0xFC62+expected_length*2]!=bytes.fromhex('9800' if expected_length<6 else 'e500'): raise ValueError('native editor capacity/delete')
        editor.append(dict(step=step,length=expected_length,capacity=6))
    owner=b'\x01'+b'\x9D'*6+b'\xE5'+bytes(6); nickname=b'\x9D'*6+bytes.fromhex('ABE406CAE5')
    events=read(mail/'final_nickname_events.json')['events']
    if [e['pc'] for e in events]!=[0x08038F60,0x08038F82,0x080517D0,0x0805181A] or any(bytes.fromhex(e['owner'])!=owner or e['gender']!=1 for e in events) or any(not bytes.fromhex(e['nickname']).startswith(nickname) for e in events[1:]): raise ValueError('normal producer/provider events')
    ar=next(x for x in m['archives'] if x['archive']=='65B220'); pool=0x08000000+ar['rom_offset']; raw=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    script=script_spans(raw,255)[1]; suffix=b'\x87\xE8'+encode_hangul('메일이야')+b'\x83\x83'; marker=b'\xF9\x0C\x01'+suffix+b'\xE6\x00\xF1'
    if script.count(marker)!=1 or raw.count(script)!=1: raise ValueError('exact first-mail suffix/command')
    suffix_at=pool+raw.index(script)+script.index(marker)+3; wait_at=suffix_at+len(suffix)
    font=m['extension']['normal_font_offset']; width_at=m['extension']['advance_offset']; expected={}; offsets={}; buf=0x02010AC0
    indices=[157]*6+[171,234,202]; positions=[buf+i for i in range(8)]+[buf+9]
    width=0
    for stream,index in zip(positions,indices):
        record=rom[font+index*96:font+(index+1)*96]
        if record!=native[0x608758+index*96:0x608758+(index+1)*96]: raise ValueError('native font identity')
        expected[stream]=dict(index=index,record=record,id='native_nickname',ch='native'); offsets[stream]=width*4
        width+=struct.unpack_from('<I',rom,width_at+index*4)[0]
    name_width=width; row=0; at=0
    while at<len(suffix):
        stream=suffix_at+at; code=suffix[at]
        if code==0xE8: row+=1; width=0; at+=1; continue
        if code==0xF9:
            if suffix[at+1]!=0xFC: raise ValueError('unknown suffix command')
            index=442+struct.unpack_from('<H',suffix,at+2)[0]; at+=4
        else: index=code; at+=1
        expected[stream]=dict(index=index,record=rom[font+index*96:font+(index+1)*96],id='65B220:1:1',ch='suffix'); offsets[stream]=row*10752+width*4
        width+=struct.unpack_from('<I',rom,width_at+index*4)[0]
        if width>132: raise ValueError('aggregate overflow')
    pages=[]
    for step in (17,18):
        data=ram(mail,step); obs=read(mail/f'step_{step:03}_roll_pet.json'); name=read(mail/f'step_{step:03}_return_ram.json')['draws']
        draws={d['stream']:d for d in obs['draws']+name if d['stream'] in expected}
        if set(draws)!=set(expected) or data[0xE50:0xE5E]!=owner or data[0xE5F:0xE5F+len(nickname)]!=nickname or data[0x10AC0:0x10AC0+len(nickname)]!=nickname: raise ValueError('resident name/literal population')
        if any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=expected[s]['index'] for s,d in draws.items()): raise ValueError('combined runtime geometry')
        if struct.unpack_from('<I',data,0xFA4C)[0]!=wait_at or rom[wait_at-0x08000000:wait_at-0x08000000+3]!=bytes.fromhex('E600F1'): raise ValueError('ordered keyWait')
        counts=Counter(e['index'] for e in expected.values()); reads={r['index']:r['reads'] for r in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()): raise ValueError('CPU font reads')
        proof=pixels(mail,step,list(draws.values()),expected,rom,m)
        im=Image.open(mail/f'step_{step:03}.png').convert('RGB'); occupied=set()
        for stream,e in expected.items():
            rr,xx=divmod(offsets[stream],10752); w=struct.unpack_from('<I',rom,width_at+e['index']*4)[0]
            occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(92+xx//4,92+xx//4+w))
        vacant={(x,y) for y in range(110,140) for x in range(92,234)}-occupied
        if any(im.getpixel(xy)!=im.getpixel((231,112)) for xy in vacant): raise ValueError('vacant pixels/residue')
        pages.append(dict(step=step,nickname_advance=name_width,first_row_advance=name_width+11,keywait=wait_at,vacant_pixels_cleared=len(vacant),**proof))
    report=dict(schema=1,status='NORMAL_NATIVE_NAME_BOUNDARY_RUNTIME_VERIFIED_NOT_HANGUL_INPUT',rom_sha256=m['output_sha256'],editor=editor,sixth_accepted=True,seventh_rejected=True,delete_reinsert_verified=True,native_E406_renderer_index=234,owner_hex=owner.hex(),nickname_hex=nickname.hex(),pages=pages,events=events,evidence=evidence,tools={name:sha((ROOT/'tools'/name).read_bytes()) for name in ('verify_nickname_mail_019.py','capture_nickname_mail_019.py','capture_roll_pet.py','capture_roll_return.py')},limits=['Normal controller route from same018 boot checkpoint; no RAM/progress/ROM writes or read aliases.','Native Japanese name plus Japanese honorific and existing Korean mail suffix. New ASCII comma page not runtime tested.','No native save/reset/fresh reload or Hangul input/serialization proof.','One native owner glyph and Rockman/female suffix; not all input repertoire or all Navi suffix runtime population.','No new500 selection, insertion approval, product ROM or distribution output.'])
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS native6/7/delete/commit ->99px nickname ->110px first row, two keyWait captures,',pages[0]['pixels'],'pixels')

if __name__=='__main__': main()
