"""Read-only normal-input timing survey; no forced entry or RAM edits."""
import argparse,json,struct
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read,verify_route
import run_roll_fortune_matrix as matrix

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--delays',default='1,7,17,31,63,127');ap.add_argument('--prefix',default='roll-family-brothers-survey-v1-');ap.add_argument('--entry-only',action='store_true')
    ap.add_argument('--stem',default='exe45_ko_development_roll_family_sisters_v1');ap.add_argument('--parent',default='roll-family-sisters-v1-jackin');ap.add_argument('--outdir',default='analysis/roll_family_brothers_survey');a=ap.parse_args()
    matrix.STEM=a.stem;m=read(ROOT/f'poc/output/{matrix.STEM}.json');parent=a.parent;recipe=read(ROOT/'poc/runtime/roll-family-survey-v1/result.json')
    if not recipe['complete'] or recipe['rom_sha256']!='dddc3a3d5c4f6c73f5f1e54be62ace5b919f839528b5caa3408482f9c9a85163':raise ValueError('survey recipe identity')
    pool=0x08000000+next(x for x in m['archives'] if x['archive']=='661858')['rom_offset']
    def run(delay):
        name=a.prefix+str(delay);tail=','.join(recipe['actions'].split(',')[:9]) if a.entry_only else recipe['actions'];actions=f'none:1:{delay},'+tail;matrix.segment('capture_roll_family.py',name,parent,actions);p=ROOT/'poc/runtime'/name;r=verify_route(p,m['output_sha256'],set());b=(p/'final_gbaExtWorkRam.bin').read_bytes();root=struct.unpack_from('<I',b,0xFA50)[0];calls=read(p/f"step_{r['actions_total']:03}_roll_pet.json")['calls']
        if root!=pool:raise ValueError('survey not family pool')
        return {'route':name,'delay_frames':delay+1,'native_script':b[0xFA21],'calls':calls,'actions':actions,'receipt':'poc/runtime/'+name+'/result.json'}
    delays=[int(n) for n in a.delays.split(',')]
    with ThreadPoolExecutor(max_workers=3) as executor:results=list(executor.map(run,delays))
    out=ROOT/a.outdir;out.mkdir(parents=True,exist_ok=True)
    dest=out/(a.prefix.rstrip('-')+'.json')
    if dest.exists():raise ValueError('fresh survey report required')
    dest.write_text(json.dumps({'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],'scope':'Normal controller timing experiment. No condition/randomness/player-gender claim. Previous receipt supplies inputs only.','results':results},ensure_ascii=False,indent=2),encoding='utf-8');print(results)

if __name__=='__main__':main()
