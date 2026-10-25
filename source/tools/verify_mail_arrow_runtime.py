"""Bind eight corrected literals to actual native keyWaits and diagnostic captures."""
import argparse,json,struct
from build_visibility_poc import ROOT,require_hash,sha
from batch500_rom import entries
from run_mail_arrow_diagnostics import CASES
from mission_reward_model import validate
from PIL import Image,ImageDraw

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('preserve verification')
    rp=ROOT/a.rom;m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    assets={x[2]['archive']:x[2] for x in entries(source)};records={r['archive']:r for r in m['keyitem_rom']['mission_mail_archives']}
    table={}
    for line in (ROOT/f'poc/build/{rp.stem}/plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            k,v=line.split('=',1)
            if len(v)==1:table[v]=bytes.fromhex(k)
    proof=validate(source,assets['6DE3E0']['units'],records['6DE3E0']['layout']);rows=[];artifacts={};sheet=Image.new('RGB',(960,360),'#222222');draw=ImageDraw.Draw(sheet)
    for j,(index,script,literal) in enumerate(CASES):
        name='6DE3E0' if index==25 else '6DF988';key=f'{name}:{script}:{literal}'
        unit=next(u for u in assets[name]['units'] if u['id']==key);record=records[name];root=0x08000000+record['rom_offset'];raw=rom[record['rom_offset']:record['rom_offset']+record['compiled_bytes']]
        encoded=b''.join(b'\xe8' if c=='\n' else table[c] for c in unit['translation']);at=raw.find(encoded)
        if at<0 or raw.find(encoded,at+1)>=0 or raw[at+len(encoded):at+len(encoded)+2]!=b'\xe6\x00':raise ValueError('corrected literal keyWait identity')
        folder=ROOT/f'poc/runtime/{a.prefix}{"-setup" if index==25 else ""}-{index}-{script}';r=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if index==25 and not r.get('entry_script0_setup_preserved'):raise ValueError('mission entry layout setup bypassed')
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or not r['native_body_resident_exact']:raise ValueError('diagnostic ROM/residency binding')
        step=10+literal;ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,base=struct.unpack_from('<2I',ram,0xFA20+0x2C)
        if base!=root or ptr!=root+at+len(encoded):raise ValueError('actual corrected literal not at native wait '+key)
        widths=next(x['line_advance_pixels'] for x in record['layout'] if x['id']==key)
        if len(widths)!=3 or max(widths)>152 or widths[2]>132:raise ValueError('arrow row budget')
        for path,digest in r['artifacts'].items():
            f=folder/path
            if sha(f.read_bytes())!=digest:raise ValueError('diagnostic evidence changed')
            artifacts[str(f.relative_to(ROOT))]=digest
        artifacts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        img=folder/f'step_{step:03}.png';sheet.paste(Image.open(img).convert('RGB'),((j%4)*240,(j//4)*180+20));draw.text(((j%4)*240,(j//4)*180),key,fill='white')
        rows.append(dict(id=key,step=step,wait_pointer=ptr,root=base,line_advance_pixels=widths,translation=unit['translation'],screenshot=str(img.relative_to(ROOT))))
    sheet_path=out.with_suffix('.png');sheet.save(sheet_path);artifacts[str(sheet_path.relative_to(ROOT))]=sha(sheet_path.read_bytes())
    repro=rp.with_name(rp.stem+'_repro.gba')
    if repro.read_bytes()!=rom:raise ValueError('independent rebuild differs')
    result=dict(passed=True,rom_sha256=sha(rom),corrected_units=8,newly_translated_units=0,independent_rebuild_identical=True,rows=rows,reward_width_proof=proof,artifacts=artifacts,visual_review='pending contact-sheet inspection',scope='Eight exact translated literals at native keyWait boundaries after diagnostic loader/table aliases; NOT natural mission acquisition/progression/reward/save QA',release_eligible=False)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS eight corrected mail literals at native waits and arrow budgets')

if __name__=='__main__':main()
