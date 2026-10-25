"""Own-ROM normal cold chains for four sibling question/answer branches."""
from report_roll_pet import ROOT,read
import run_roll_family_sisters as sisters
import run_roll_fortune_matrix as matrix

STEM='exe45_ko_development_roll_family_siblings_v1'
PREFIX='roll-family-siblings-v1-'
SURVEY_ROM='b7227159ae498da3ac3da7e6620d1582170086c20d7e76d778aa7efd8353bb67'
BROTHERS=[('older-brother','roll-family-brothers-survey-v2-10',1,2),('younger-brother','roll-family-brothers-survey-v3-18',3,4)]

def brother_recipe(route,script):
    p=ROOT/'poc/runtime'/route;r=read(p/'result.json');calls=read(p/'step_010_roll_pet.json')['calls']
    if not r['complete'] or r['rom_sha256']!=SURVEY_ROM or r['actions_total']!=10 or len(calls)!=1 or calls[0]['script']!=script or calls[0]['lr']!=0x08037F27:raise ValueError('normal brother entry recipe identity')
    # Survey stops on first page. Four A confirmations reach the separate
    # choice page, not name entry; retain original page/choice semantics.
    return r['actions']+','+','.join(['a:2:180']*4+['none:1:180'])

def main(outdir='roll_family_siblings_v1'):
    previous=sisters.STEM,sisters.PREFIX
    try:sisters.STEM=STEM;sisters.PREFIX=PREFIX;sisters.main(outdir)
    finally:sisters.STEM,sisters.PREFIX=previous
    matrix.STEM=STEM;matrix.PREFIX=PREFIX
    for name,recipe,question,response in BROTHERS:
        matrix.segment('capture_roll_family.py',PREFIX+name+'-entry',PREFIX+'jackin',brother_recipe(recipe,question))
        for branch,actions in [('yes','none:1:60,a:2:180,none:1:180'),('no','none:1:60,right:2:60,left:2:60,right:2:60,a:2:180,none:1:180')]:
            matrix.segment('capture_roll_family.py',PREFIX+name+'-'+branch,PREFIX+name+'-entry',actions)

if __name__=='__main__':main()
