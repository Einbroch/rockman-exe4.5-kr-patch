"""Finite exact-ROM renderer matrix; intervention provenance stays explicit."""
import json,struct
from collections import Counter
from PIL import Image
from report_keyitem_full_rom import static,ROOT,PREFIX
from report_roll_pet import read,sha,require_hash,pixels,verify_route
from capture_keyitem_rom_matrix import CASES

def main():
    m,rom,e,streams,geometry,_=static();p=ROOT/'poc/runtime'/ (PREFIX+'matrix-r3');r=verify_route(p,m['output_sha256'],set());env=read(p/'key_matrix_environment.json')
    if not env['passed']or r.get('normal_play_checkpoint_eligible')is not False or len(env['entries'])!=len(CASES)or env['count_aliases']!=10:raise ValueError('matrix diagnostic contract')
    require_hash(ROOT/'tools/capture_keyitem_rom_matrix.py',env['self_sha256'])
    codes={v:bytes.fromhex(k)for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()if '='in line for k,v in [line.split('=',1)]if len(v)==1}
    pages=[];observed=set();sheet=Image.new('RGB',(240*5,160*8))
    for i,(script,count)in enumerate(CASES):
        step=2+4*i;cp=f'step_{step:03d}';obs=read(p/(cp+'_roll_pet.json'));alias=read(p/(cp+'_key_matrix.json'))['entries'][-1]
        if (alias['entry'],alias['script'],alias['count'])!=(i+1,script,count):raise ValueError('matrix selected entry')
        wanted={s for s,g in e.items()if g['script']==script};last={d['stream']:d for d in obs['draws']if d['stream']in wanted and d['frame']>=alias['frame']}
        if set(last)!=wanted:raise ValueError('missing full literal glyph population '+str(script))
        draws=[last[s]for s in sorted(wanted)];expected=dict(e);quantity=[]
        if script in [6,7,16,17,18]:
            # Native number format scratch stream, observed in zero-count
            # diagnostic; check exact digits, offsets and glyph supply.
            digits=str(count);numeric=[d for d in obs['draws']if 0x02010AC0<=d['stream']<0x02010AC0+len(digits) and d['frame']>=alias['frame']]
            selected={d['stream']:d for d in numeric}
            if set(selected)!={0x02010AC0+j for j in range(len(digits))}:raise ValueError('quantity digits absent')
            prefix=max(d['offset']+struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0]*4 for d in draws if e[d['stream']]['id']==f'709408:{script}:0')
            for j,ch in enumerate(digits):
                stream=0x02010AC0+j;d=selected[stream];idx=codes[ch][0];at=m['extension']['normal_font_offset']+idx*96
                if d['glyph_index']!=idx or d['offset']!=prefix+44*j:raise ValueError('quantity value/geometry')
                expected[stream]=dict(ch=ch,index=idx,record=rom[at:at+96],id=f'709408:{script}:quantity',script=script);quantity.append(d)
            suffix=sorted((d for d in draws if e[d['stream']]['id']==f'709408:{script}:1'),key=lambda d:d['offset'])
            if suffix[0]['offset']!=prefix+44*len(digits):raise ValueError('quantity suffix aggregate geometry')
        counts=Counter(d['glyph_index']for d in draws+quantity);reads={x['index']:x['reads']for x in obs['font_reads']}
        if any(reads.get(g,0)<n*24 for g,n in counts.items()):raise ValueError('matrix CPU font supply')
        page=pixels(p,step,draws+quantity,expected,rom,m,origin=(52,110),cursor_indices=())
        units=sorted({e[s]['id']for s in wanted});observed.update(units);sheet.paste(Image.open(p/(cp+'.png')),(240*(i%5),160*(i//5)))
        pages.append(dict(script=script,count=count,step=step,units=units,scope=env['scope'],screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),**page))
    if len(observed)!=39:raise ValueError('all39 literal matrix')
    out=ROOT/'analysis/keyitem_full_rom_v1';sheet.save(out/'renderer_matrix.png')
    result=dict(passed=True,rom_sha256=m['output_sha256'],scope=env['scope'],normal_play_claim=False,rendered_literal_units=sorted(observed),pages=pages,
        quantity_values=[0,255],count_aliases=10,release_eligible=False,limits=['Not normal item acquisition/selection or other02031000 consumer proof.','Human wording/terminology/presentation review and full project conditions remain open.'])
    (out/'renderer_matrix.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Renderer matrix all39 literals / 0,255 quantities PASS')
if __name__=='__main__':main()
