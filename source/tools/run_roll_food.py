"""Fresh own-ROM cumulative chains and native favorite-food entry recipe."""
from report_roll_pet import ROOT,read
import run_roll_family_siblings as siblings
import run_roll_fortune_matrix as matrix
STEM='exe45_ko_development_roll_food_v1'
PREFIX='roll-food-v1-'

def food_recipe():
    path=ROOT/'poc/runtime/roll-family-brothers-survey-v3-19'
    r=read(path/'result.json');calls=read(path/'step_010_roll_pet.json')['calls']
    if not r['complete'] or r['rom_sha256']!=siblings.SURVEY_ROM or r['actions_total']!=10 or len(calls)!=1 or calls[0]['script']!=11 or calls[0]['lr']!=0x08037F27:raise ValueError('native food recipe identity')
    return r['actions']+',a:2:180,a:2:180,none:1:180'

def main(outdir='roll_food_v1'):
    previous=siblings.STEM,siblings.PREFIX
    try:siblings.STEM=STEM;siblings.PREFIX=PREFIX;siblings.main(outdir)
    finally:siblings.STEM,siblings.PREFIX=previous
    matrix.STEM=STEM;matrix.PREFIX=PREFIX
    matrix.segment('capture_roll_family.py',PREFIX+'food',PREFIX+'jackin',food_recipe())

if __name__=='__main__':main()
