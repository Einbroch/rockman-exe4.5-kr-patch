"""Weekday-conditioned tournament hint consumption with native name clearing."""
import json
from PIL import Image
from report_roll_pet import ROOT,read,sha,verify_route
from run_roll_pet_weekday import STEM,PREFIX,OUTDIR,DATE_ACTIONS,INTRO_ACTIONS

def weekday_route():
    m=read(ROOT/f'poc/output/{STEM}.json');names=['date','profile','navi-menu','select-roll','intro'];seen=set();routes=[]
    for i,name in enumerate(names):
        path=ROOT/'poc/runtime'/(PREFIX+'weekday-'+name);r=verify_route(path,m['output_sha256'],seen)
        parent=ROOT/'poc/runtime'/(PREFIX+'weekday-'+names[i-1] if i else PREFIX+'roll-cold-part1')/'result.json'
        if r.get('normal_play_checkpoint_eligible') is False or not r['complete'] or r['state_origin']!=str(parent):raise ValueError('weekday normal chain provenance')
        if name=='date' and (r['actions']!=DATE_ACTIONS or r['capture_steps']!=list(range(1,15))):raise ValueError('weekday normal date input recipe')
        if name=='intro' and (r['actions']!=INTRO_ACTIONS or r['capture_steps']!=[2,4,6,7]):raise ValueError('weekday normal greeting dismissal recipe')
        routes.append({'name':name,'result_sha256':sha((path/'result.json').read_bytes()),'rom_sha256':r['rom_sha256']})
    for s in [26,28,29]:
        r=read(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/'result.json')
        if r['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+'weekday-intro')/'result.json'):raise ValueError('weekday diagnostic parent')
    date=ROOT/'poc/runtime'/(PREFIX+'weekday-date')/'step_007.png'
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'normal_controller_only':True,'date_actions':DATE_ACTIONS,'date_ui_capture_sha256':sha(date.read_bytes()),'routes':routes,'limits':['Normal date entry only; PET target table lookup remains diagnostic alias.','Weekday source literals consumed with original weekday checks retained; native tournament progression unproven.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'weekday_route.json').write_text(json.dumps(result,indent=2),encoding='utf-8');return result

def main():
    import report_roll_pet_license as base
    route=weekday_route();previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,23,24,25,30,31,34,16,18,19,20,21,22,32,33,27,26,28,29];reports=base.main(new_units=5)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(720,320))
    for i,(s,step) in enumerate([(26,3),(26,5),(28,3),(28,5),(29,3)]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/f'step_{step:03}.png'),((i%3)*240,(i//3)*160))
    out=ROOT/'analysis'/OUTDIR;sheet.save(out/'weekday_diagnostic_pages.png')
    summary=read(out/'cumulative_runtime.json');summary['weekday_route_passed']=route['passed'];(out/'cumulative_runtime.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
