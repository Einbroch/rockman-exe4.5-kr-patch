"""Observe random results via normal delayed confirmations, no state edits."""
import json,struct
from build_visibility_poc import ROOT
import run_roll_fortune_matrix as matrix

STEM='exe45_ko_development_roll_fortune_v2'
PREFIX='roll-fortune-v2-'

def main(outdir='roll_fortune_v2'):
    matrix.STEM=STEM;matrix.PREFIX=PREFIX
    r=json.loads((ROOT/'poc/runtime/roll-equipment-v1-select-roll/result.json').read_text())
    if not r['complete'] or r['rom_sha256']!=matrix.RECIPE_ROM:raise ValueError('recipe identity')
    actions=','.join(r['actions'].split(',')[:12])
    matrix.segment('capture_roll_fortune.py',PREFIX+'result-ready',PREFIX+'roll-navi-menu',actions)
    meta=json.loads((ROOT/f'poc/output/{STEM}.json').read_text());ar=next(x for x in meta['archives'] if x['archive']=='65FF3C');root=0x08000000+ar['rom_offset']
    ready=ROOT/'poc/runtime'/(PREFIX+'result-ready');ram=(ready/'final_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]!=root or ram[0xFA21]!=0:raise ValueError('normal result-ready root/script')
    results=[]
    for delay in [97,211,389]:
        name=f'sample-{delay}'
        matrix.segment('capture_roll_fortune.py',PREFIX+name,PREFIX+'result-ready',f'none:1:{delay},'+','.join(['a:2:180']*7))
        path=ROOT/'poc/runtime'/(PREFIX+name);scripts=[]
        for p in sorted(path.glob('step_*_gbaExtWorkRam.bin')):
            b=p.read_bytes()
            if struct.unpack_from('<I',b,0xFA50)[0]==root:scripts.append(b[0xFA21])
        results.append({'route':name,'delay_frames':delay+1,'observed_scripts':sorted(set(scripts))})
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True)
    (out/'normal_sample_routes.json').write_text(json.dumps({'policy':'development-draft; NON-DISTRIBUTION','scope':'normal input timing samples; no assurance of distinct random outcomes','rom_sha256':meta['output_sha256'],'results':results},indent=2),encoding='utf-8')
    print(results)

if __name__=='__main__':main()
