"""Native Guts R10/return plus quarantined representative and nickname pages."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_gutsman_pet import main as pet_regression
from report_gutsman_schedule_alarm import alarm_pages
from report_gutsman_talk_name import name_page
from run_gutsman_pet_talk import STEM,PREFIX,OUTDIR,SCRIPTS
def main():
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2278,57,675),oldstem='exe45_ko_development_gutsman_battle_results_v1',outdir=OUTDIR+'/pet_regression',inventory_outdir='full_scope_gutsman_pet_talk_v1',added_literal_units=0)
    m,rom,e,s,c=static(STEM,'66A844');pool=0x8000000+next(a for a in m['archives'] if a['archive']=='66A844')['rom_offset'];rt=ROOT/'poc/runtime';p=rt/(PREFIX+'normal-talk');r=verify_route(p,m['output_sha256'],set())
    if r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json') or r.get('normal_play_checkpoint_eligible') is False or any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('normal native R ancestry/intervention')
    normal=alarm_pages(p,10,10,m,rom,e,s,pool,unit_asset='gutsman_pet_talk_ko.json')
    if [x['step'] for x in normal]!=[2]:raise ValueError('normal R10 complete page')
    petpool=0x8000000+next(a for a in m['archives'] if a['archive']=='665F3C')['rom_offset'];before=read(p/'step_002_roll_pet.json');after=read(p/'step_004_roll_pet.json');ram=(p/'step_004_gbaExtWorkRam.bin').read_bytes()
    if len(before['calls'])!=1 or before['calls'][0]['root']!=pool or before['calls'][0]['script']!=0 or before['calls'][0]['lr']!=0x08037F27 or before['calls']!=after['calls'] or before['draws']!=after['draws'] or ram[0xFA21]!=1 or struct.unpack_from('<I',ram,0xFA50)[0]!=petpool:raise ValueError('native R entry/exit/menu return')
    diagnostic=[]
    for script in [*SCRIPTS,31]:
        p=rt/(PREFIX+f'script{script}');r=verify_route(p,m['output_sha256'],set());env=read(p/'talk_environment.json')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json'):raise ValueError('own parent/quarantine')
        for file,key in [('capture_gutsman_pet_talk_diagnostic.py','tool_sha256'),('capture_gutsman_pet_talk.py','observer_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer drift')
        if script==31 and sha((ROOT/'tools/capture_gutsman_pet_talk_nickname_diagnostic.py').read_bytes())!=env['nickname_scope_tool_sha256']:raise ValueError('nickname diagnostic scope drift')
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        for g in env['native_guards']:
            if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('native consumer guard drift')
        if script in [12,31]:
            found=[name_page(p,2,f'66A844:{script}:0',0,m,rom,e,s,pool)]
            if script==31:found+=alarm_pages(p,31,0,m,rom,e,s,pool,unit_asset='gutsman_pet_talk_ko.json',only_keys=['66A844:31:1'])
        else:found=alarm_pages(p,script,0,m,rom,e,s,pool,unit_asset='gutsman_pet_talk_ko.json')
        for page in found:
            obs=read(p/f"step_{page['step']:03}_roll_pet.json")
            if len(obs['calls'])!=1 or obs['calls'][0]['root']!=pool or obs['calls'][0]['script']!=0 or obs['calls'][0]['lr']!=0x08037F27:raise ValueError('diagnostic native caller')
        diagnostic.extend(found)
    if len(diagnostic)!=13:raise ValueError('representative finite diagnostic scope')
    covered={x['unit'] for x in normal+diagnostic};out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,800))
    for i,x in enumerate(normal+diagnostic):sheet.paste(Image.open(rt/x['route']/f"step_{x['step']:03}.png"),(i%3*240,i//3*160))
    sheet.save(out/'talk_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=31,selected_text_units=2278,static=c,previous56_payloads_identical=True,pet_regression=baseline,normal_pages=normal,normal_runtime_units=sorted(x['unit'] for x in normal),diagnostic_renderer_pages=diagnostic,static_only_units=sorted(set(s)-covered),native_menu_return_step=4,remaining_catalog=baseline['remaining_catalog'],limits=['31 of33 source literals; entire script13/two literals and native chip104 name remain untranslated. Roll-only printChip Korean name selector not widened or changed.','Normal R script0->10 one full page plus exit/PET return. Initial script31/name/two-page assumption failed on unchanged ROM; failure preserved in handoff.','Diagnostic11/12/17/25/27/33/34/31 thirteen pages stop at keyWait; entry alias only, native root/portrait unchanged. Two captured source-native nickname samples, not arbitrary/Hangul name persistence. No acquired item/license/incident/tournament/date/weekday or quest completion proof. Other17 selected literals static-only.','Own NumberMan fresh save/cold continue/3pages,Guts intro2/PET8scenes22units regressions; other prior content not rerun. Existing56 payloads/graphics unchanged.','Whole text/images/inline/fixed population/name editing->committed record->all redisplays->persistent reload->old-save compatibility/prior arrow53pixel/human wording review remain unresolved.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts talk31 static / native R10+return / diagnostic13 pages PASS');return result
if __name__=='__main__':main()
