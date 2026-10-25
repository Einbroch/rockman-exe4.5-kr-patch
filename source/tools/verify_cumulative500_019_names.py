"""Bounded nickname plus new Korean suffix CPU/font/OBJ/pixel evidence."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_019_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes();pages=[]
    for case,archive,script,count,step,limit in [('comma','65B74C',2,25,3,111),('honorific','6B5A70',1,4,5,131)]:
        pool,units,expected,streams,ends=model(rom,m,cfg,archive,script,count,asset_folder='analysis/pending_insertion_500_019_cumulative_v1')
        # The honorific's first literal is a separate earlier page.
        selected=units if case=='comma' else units[1:]
        folder=ROOT/f'poc/runtime/pending500-019-v1-name-{case}';receipt=read(folder/'result.json');d=receipt['display_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=m['output_sha256'] or receipt['normal_play_checkpoint_eligible'] is not False or d!={'roots':1,'entries':1,'navi':0,'root':pool,'script':script}:raise ValueError('Name diagnostic identity')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Diagnostic quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(folder/(cp+'_roll_pet.json'));name=read(folder/(cp+'_return_ram.json'))['draws']
        native_bytes=b'\x9D'*6+bytes.fromhex('ABE406CAE5');buffer=0x02010AC0
        if ram[0x952]!=1 or ram[0xE50:0xE58]!=b'\x01'+b'\x9D'*6+b'\xE5' or ram[0xE5F:0xE5F+len(native_bytes)]!=native_bytes or ram[0x10AC0:0x10AC0+len(native_bytes)]!=native_bytes:raise ValueError('Native worst name residency')
        indices=[157]*6+[171,234,202];positions=[buffer+i for i in range(8)]+[buffer+9]
        e={s:expected[s] for u in selected for s in streams[u['id']]};offsets={};row=0;width=0
        def literal(u):
            nonlocal row,width
            it=iter(streams[u['id']])
            for ch in u['translation']:
                if ch=='\n':row+=1;width=0;continue
                stream=next(it);offsets[stream]=row*10752+width*4
                width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
                if width>132 or row>2:raise ValueError('Static aggregate geometry')
        literal(selected[0])
        if width!=0:raise ValueError('Native name column-zero')
        name_row=row
        for stream,index in zip(positions,indices):
            record=rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]
            if record!=source[0x608758+index*96:0x608758+(index+1)*96]:raise ValueError('Native glyph identity')
            e[stream]=dict(ch='native name',id='native_nickname',index=index,record=record);offsets[stream]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
        if width!=99:raise ValueError('Native maximum-name width')
        suffix=selected[-1];first=suffix['translation'].split('\n')[0]
        first_width=width+sum(struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0] for s in streams[suffix['id']][:len(first)])
        if first_width!=limit:raise ValueError('Name/suffix boundary')
        literal(suffix)
        draws={r['stream']:r for r in obs['draws']+name if r['stream'] in e}
        if set(draws)!=set(e) or any(r['context']!=0x0200FA20 or r['offset']!=offsets[s] or r['glyph_index']!=e[s]['index'] for s,r in draws.items()):raise ValueError('Actual aggregate glyph geometry')
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=pool or ptr!=ends[suffix['id']] or rom[ptr-0x08000000:ptr-0x08000000+3]!=bytes.fromhex('E600F1') or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('Native keyWait/window')
        reads={r['index']:r['reads'] for r in obs['font_reads']};counts=Counter(g['index'] for g in e.values())
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Native/translated CPU font reads')
        proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=(92,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
        for s,g in e.items():
            rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0]
            occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(92+xx//4,92+xx//4+w))
        vacant={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138)}-occupied
        if any(im.getpixel(p)!=im.getpixel((233,110)) for p in vacant):raise ValueError('Name page residual ink')
        pages.append(dict(case=case,step=step,ids=[u['id'] for u in selected],nickname_advance=99,nickname_row=name_row,aggregate_name_row_advance=first_width,wait_stream=ptr,vacant_pixels_cleared=len(vacant),receipt_sha256=sha((folder/'result.json').read_bytes()),**proof))
    frozen_write(ROOT/'analysis/pending500_019_v1/name_display_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],pages=pages,read_alias_diagnostic=True,natural_event_or_save_verified=False,release_eligible=False,limits='Two actual019 quick-box name-boundary pages with native six-glyph/female Rockman name. No full-box sample, post-final-wait event/exit/reentry, all221 profiles, other Navi suffix route, automatic Hangul input/save or human semantic approval.'))
    print('PASS new comma111px/honorific131px: native name + Korean suffix CPU/font/OBJ/pixels/keyWait/clearing')
if __name__=='__main__':main()
