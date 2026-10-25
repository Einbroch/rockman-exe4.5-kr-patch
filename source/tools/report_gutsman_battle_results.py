"""Full three-expression renderer proof, not native win/loss/draw event proof."""
import json
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_gutsman_pet import main as pet_regression
from report_gutsman_schedule_alarm import alarm_pages
from run_gutsman_battle_results import STEM,PREFIX,OUTDIR
def main():
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2247,56,676),oldstem='exe45_ko_development_gutsman_schedule_alarm_v1',outdir=OUTDIR+'/pet_regression',inventory_outdir='full_scope_gutsman_battle_results_v1',added_literal_units=0)
    m,rom,e,s,c=static(STEM,'66A7A8');pool=0x8000000+next(a for a in m['archives'] if a['archive']=='66A7A8')['rom_offset'];rt=ROOT/'poc/runtime';q=[]
    for script in [1,2,3]:
        p=rt/(PREFIX+f'script{script}');r=verify_route(p,m['output_sha256'],set());env=read(p/'battle_environment.json')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json'):raise ValueError('own parent/quarantine')
        for file,key in [('capture_gutsman_battle_results.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer drift')
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        for g in env['native_guards']:
            if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('native guard drift')
        found=alarm_pages(p,script,0,m,rom,e,s,pool,unit_asset='gutsman_battle_results_ko.json')
        if len(found)!=1:raise ValueError('one complete result page')
        obs=read(p/f"step_{found[0]['step']:03}_roll_pet.json")
        if len(obs['calls'])!=1 or obs['calls'][0]['root']!=pool or obs['calls'][0]['script']!=0 or obs['calls'][0]['lr']!=0x08037F27:raise ValueError('virtual entry caller')
        q.extend(found)
    if {x['unit'] for x in q}!=set(s):raise ValueError('complete three-expression renderer scope')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,x in enumerate(q):sheet.paste(Image.open(rt/x['route']/f"step_{x['step']:03}.png"),(i*240,0))
    sheet.save(out/'diagnostic_result_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=3,selected_text_units=2247,static=c,previous55_payloads_identical=True,pet_regression=baseline,normal_runtime_new_units=[],diagnostic_renderer_pages=q,remaining_catalog=baseline['remaining_catalog'],limits=['Defeat1/victory2/draw3 PET renderer diagnostic only; not completed battles or native result-state/caller selection. Stops at keyWait, no exit/reentry/result-state/persistence claim.','Normal own NumberMan fresh save/cold continue/3pages,Guts intro2/PET8scenes22units exact-ROM regressions; previous other scenes not rerun.','Original controls and native Navi ROM bindings preserved; read aliases remain observer-only and diagnostic states cannot join normal chain.','Whole text/images/inline/fixed population/Hangul name editing->committed records->all redisplays->persistent reload->old-save compatibility unresolved. Prior native arrow53pixel issue and human wording review open.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts three results renderer and fresh normal PET/save regressions PASS');return result
if __name__=='__main__':main()
