"""Native school-subject recipes; survey first, then fresh cumulative ROM."""
import argparse,json,struct
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read,verify_route
import run_roll_food as food
import run_roll_fortune_matrix as matrix
STEM='exe45_ko_development_roll_subjects_v1'
PREFIX='roll-subjects-v1-'
SCENES=[('strong',27,'roll-family-brothers-survey-v1-7',15,1),('weak',29,'roll-family-brothers-survey-v2-3',10,2)]
BASELINE='986450bc2c3e6aef7688428863e4a0ca478c2ce9b5b60f6628917caecc283bd9'
RECIPE_ROM='b7227159ae498da3ac3da7e6620d1582170086c20d7e76d778aa7efd8353bb67'

def subject_recipe(scene):
    name,script,route,total,confirmations=scene;path=ROOT/'poc/runtime'/route;r=read(path/'result.json');calls=read(path/'step_010_roll_pet.json')['calls']
    if not r['complete'] or r['rom_sha256']!=RECIPE_ROM or r['actions_total']!=total or len(calls)!=1 or calls[0]['script']!=script or calls[0]['lr']!=0x08037F27:raise ValueError('native subject recipe identity')
    # Ignore later confirmations in the old long survey. Do not reach input.
    return ','.join(r['actions'].split(',')[:10]+['a:2:180']*confirmations+['none:1:180'])

def survey():
    matrix.STEM='exe45_ko_development_roll_food_v1';m=read(ROOT/f'poc/output/{matrix.STEM}.json')
    if m['output_sha256']!=BASELINE:raise ValueError('subject survey baseline')
    pool=0x08000000+next(a for a in m['archives'] if a['archive']=='661858')['rom_offset']
    def run(scene):
        name,script,_,_,_=scene;route='roll-subjects-survey-v1-'+name
        matrix.segment('capture_roll_family.py',route,'roll-food-v1-jackin',subject_recipe(scene));p=ROOT/'poc/runtime'/route;r=verify_route(p,BASELINE,set());ram=(p/'final_gbaExtWorkRam.bin').read_bytes();calls=read(p/f"step_{r['actions_total']:03}_roll_pet.json")['calls']
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or len(calls)!=1 or calls[0]['script']!=script or calls[0]['lr']!=0x08037F27:raise ValueError('subject baseline native scene')
        return {'route':route,'script':script,'calls':calls,'actions':r['actions'],'stopped_before_input_confirmation':True}
    with ThreadPoolExecutor(max_workers=2) as executor:results=list(executor.map(run,SCENES))
    out=ROOT/'analysis/roll_subjects_survey_v1';out.mkdir(parents=True,exist_ok=True);dest=out/'native_scenes.json'
    if dest.exists():raise ValueError('fresh subject survey required')
    dest.write_text(json.dumps({'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':BASELINE,'results':results},ensure_ascii=False,indent=2),encoding='utf-8');print(results)

def main(outdir='roll_subjects_v1'):
    previous=food.STEM,food.PREFIX
    try:food.STEM=STEM;food.PREFIX=PREFIX;food.main(outdir)
    finally:food.STEM,food.PREFIX=previous
    matrix.STEM=STEM;matrix.PREFIX=PREFIX
    for scene in SCENES:matrix.segment('capture_roll_family.py',PREFIX+scene[0],PREFIX+'jackin',subject_recipe(scene))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--survey',action='store_true');args=ap.parse_args()
    if args.survey:survey()
    else:main()
