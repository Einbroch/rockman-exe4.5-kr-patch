"""Exact native wait pointers for reflowed/new body literals; diagnostic, not natural acquisition."""
import argparse,json,struct
from build_visibility_poc import ROOT,sha,require_hash
from batch500_002_rom import entries
from pending500_002_pages import specification
from PIL import Image,ImageDraw

TARGETS=[(26,41,1,11,0),(26,49,1,11,0),(26,49,1,12,1),
         (26,55,2,12,0),(26,55,2,13,1),(28,36,2,12,0),(24,33,1,11,0)]


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('Preserve previous evidence')
    rp=ROOT/a.rom;meta=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));source=ROOT/cfg['source_profile']['filename'];require_hash(source,cfg['source_profile']['sha256'])
    assets={x[2]['archive']:x[2] for x in entries(source.read_bytes())}
    records={r['archive']:r for r in meta['keyitem_rom']['mission_mail_archives']}
    pages,_=specification();table={}
    for line in (ROOT/f'poc/build/{rp.stem}/plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            k,v=line.split('=',1)
            if len(v)==1:table[v]=bytes.fromhex(k)
    observations=[];artifacts={};sheet=Image.new('RGB',(960,360),'#222222');draw=ImageDraw.Draw(sheet)
    for j,(index,script,literal,step,page) in enumerate(TARGETS):
        name={26:'6DED88',28:'6E01AC',24:'6DE2C8'}[index];key=f'{name}:{script}:{literal}'
        unit=next(x for x in assets[name]['units'] if x['id']==key)
        text=pages['pages'].get(key,[unit['translation']])[page]
        encoded=b''.join(b'\xe8' if c=='\n' else table[c] for c in text)
        record=records[name];root=0x08000000+record['rom_offset']
        raw=rom[record['rom_offset']:record['rom_offset']+record['compiled_bytes']]
        start=int.from_bytes(raw[script*2:script*2+2],'little')
        end=int.from_bytes(raw[(script+1)*2:(script+1)*2+2],'little') if script+1<record['script_count'] else len(raw)
        at=raw.find(encoded,start,end)
        if at<0 or raw.find(encoded,at+1,end)>=0 or raw[at+len(encoded):at+len(encoded)+2]!=b'\xe6\x00':raise ValueError('Unique native wait identity '+key)
        folder=ROOT/f'poc/runtime/{a.prefix}-{index}-{script}'
        result=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if not result['complete'] or result['rom_sha256']!=sha(rom) or not result['native_body_resident_exact'] or result['normal_play_checkpoint_eligible'] is not False:raise ValueError('Diagnostic receipt identity')
        if index==26 and not result['entry_script0_setup_preserved']:raise ValueError('Native setup bypassed')
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        pointer,base=struct.unpack_from('<2I',ram,0xFA20+0x2C)
        if pointer!=root+at+len(encoded) or base!=root:raise ValueError('Actual native wait mismatch '+key+' page'+str(page))
        widths=[sum(12 if '\uac00'<=ch<='\ud7a3' or ch==',' else 8 if ch==' ' else 11 for ch in line) for line in text.split('\n')]
        if len(widths)>3 or max(widths)>152 or len(widths)==3 and widths[2]>132:raise ValueError('Displayed page geometry')
        for path,digest in result['artifacts'].items():
            file=folder/path;require_hash(file,digest);artifacts[str(file.relative_to(ROOT))]=digest
        artifacts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        screenshot=folder/f'step_{step:03}.png';sheet.paste(Image.open(screenshot).convert('RGB'),((j%4)*240,(j//4)*180+20))
        draw.text(((j%4)*240,(j//4)*180),key+' page'+str(page+1),fill='white')
        observations.append(dict(id=key,page=page+1,step=step,translation=text,line_advance_pixels=widths,
            root=base,wait_pointer=pointer,screenshot=str(screenshot.relative_to(ROOT))))
    image=out.with_suffix('.png');sheet.save(image);artifacts[str(image.relative_to(ROOT))]=sha(image.read_bytes())
    report=dict(passed=True,rom_sha256=sha(rom),rows=observations,artifacts=artifacts,visual_review='pending sheet inspection',
        scope='Seven exact literal/page waits after quarantined native loader/table aliases. Native setup/RAM retained. NOT natural acquisition/progression/reward/save verification.',release_eligible=False)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS seven exact new body page waits; original RAM/source setup retained')


if __name__=='__main__':main()
