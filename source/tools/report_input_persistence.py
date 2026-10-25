"""Audit retained native Japanese answer edit/commit/save/cold-load evidence."""
import json, struct
from pathlib import Path
from PIL import Image, ImageDraw
from build_visibility_poc import ROOT, require_hash, sha
from report_fixedcell_runtime import verify_route, read

ROM_SHA='68260ec96c118939efa66f24f077dd06d375bdebffb8246529bcdfd6c45e87a6'
PREFIX='input-entry-v1-'
STEM='exe45_ko_development_input_confirmation_v1'

def main():
    require_hash(ROOT/f'poc/output/{STEM}.gba',ROM_SHA)
    require_hash(ROOT/'poc/output/exe45_ko_development_input_confirmation_v1_r3.gba',ROM_SHA)
    require_hash(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba','588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    out=ROOT/'analysis/input_entry_v1';out.mkdir(exist_ok=True)
    routes={};seen=set();snapshots=[]
    for name in ['capacity','header-source','leave','save-enter','save-commit','save-enter-corrected','save-accept','save-overwrite','save-success-snapshot','cold-continue','cold-continue-snapshot','reloaded-pet','reloaded-pet-confirmed']:
        p=ROOT/'poc/runtime'/(PREFIX+name);r=verify_route(p,ROM_SHA,seen)
        if any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('intervention')
        routes[name]=dict(result_sha256=sha((p/'result.json').read_bytes()),actions=r['actions'],state_origin=r['state_origin'],steps=r['steps_captured'])
        for step in r['capture_steps']:
            ramfile=p/f'step_{step:03}_gbaExtWorkRam.bin'
            if not ramfile.exists():continue
            ram=ramfile.read_bytes()
            snapshots.append(dict(route=name,step=step,record_hex=ram[0x10a6:0x10ad].hex(),editing_hex=ram[0xfc80:0xfc90].hex(),script=ram[0xfa21],root=struct.unpack_from('<I',ram,0xfa50)[0],screenshot_sha256=sha((p/f'step_{step:03}.png').read_bytes())))
    def snap(name,step):return next(s for s in snapshots if s['route']==name and s['step']==step)
    for step,prefix in [(2,'9b989898e5'),(4,'9b9b9898e5'),(6,'9b9b9b98e5'),(8,'9b9b9b9be5'),(10,'9b9b9b9be5'),(12,'9b9b9b98e5'),(14,'9b9b9b9be5')]:
        if not snap('capacity',step)['editing_hex'].startswith(prefix):raise ValueError('editing boundary')
    expected='019b9b9b9be500'
    if snap('capacity',17)['record_hex']!='007e7e7ee50000':raise ValueError('premature commit')
    for name,step in [('capacity',19),('save-success-snapshot',1),('cold-continue-snapshot',8),('reloaded-pet-confirmed',5)]:
        if snap(name,step)['record_hex']!=expected:raise ValueError('native persistence mismatch')
    success=snap('save-success-snapshot',1)
    if success['script']!=28 or success['root']!=0x0881a018:raise ValueError('not native save success28')
    for name in ['cold-continue','cold-continue-snapshot']:
        if routes[name]['state_origin'] is not None:raise ValueError('not cold boot')
    savechecks={}
    for name in ['save-enter','save-commit','save-enter-corrected','save-accept','save-overwrite','save-success-snapshot','cold-continue','cold-continue-snapshot','reloaded-pet','reloaded-pet-confirmed']:
        p=ROOT/'poc/runtime'/(PREFIX+name);env=read(p/'save_environment.json');own=read(p/'input_save_environment.json');before=env['files_before'];after=env['files_after']
        if not all(own[k] for k in ['observer_only','no_RAM_or_save_injection']) or own['rom_sha256']!=ROM_SHA:raise ValueError('save observer identity')
        for file,meta in own['originals_preserved'].items():require_hash(p/'persistent_files_before'/file,meta['sha256'])
        for file,meta in after.items():require_hash(p/'persistent_files_after'/file,meta['sha256'])
        changed=[file for file in before.keys()|after.keys() if before.get(file)!=after.get(file)]
        if any(file not in [STEM+'.sav',STEM+'.rtc'] for file in changed):raise ValueError('unrelated persistence changed')
        a=before[STEM+'.sav']['sha256'];b=after[STEM+'.sav']['sha256']
        if (name=='save-overwrite') != (a!=b):raise ValueError('unexpected save write/no write')
        savechecks[name]=dict(before_sha256=a,after_sha256=b,changed_files=changed,environment_sha256=sha((p/'save_environment.json').read_bytes()),prior_backup_sha256=own['originals_preserved'][STEM+'.sav']['sha256'])
    if savechecks['save-overwrite']['after_sha256']!=savechecks['cold-continue-snapshot']['before_sha256']:raise ValueError('cold loaded wrong save')
    rows=read(ROOT/'poc/runtime'/f'{PREFIX}header-source/step_003_fixedcells.json')['calls']
    header=[c for c in rows if c['stream']==0x08800451]
    if len(header)!=1:raise ValueError('header stream')
    h=header[0]
    if (h['stage'],h['target'],h['width'],h['height'],h['font'],h['bytes'])!=(0x0201c800,0x0600b800,2,10,0x08619ef8,1280):raise ValueError('header consumer')
    pages=[('capacity',8,'four native characters'),('capacity',10,'fifth input rejected'),('capacity',12,'B deletes one'),('capacity',19,'Yes / native reaction93'),('save-success-snapshot',1,'native save success28'),('reloaded-pet-confirmed',5,'cold-continue / Gutsman PET')]
    sheet=Image.new('RGB',(720,376),'white');draw=ImageDraw.Draw(sheet)
    for i,(name,step,label) in enumerate(pages):
        x=i%3*240;y=i//3*188;draw.text((x+4,y+3),label,fill='black');sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+name)/f'step_{step:03}.png').convert('RGB'),(x,y+24))
    sheet.save(out/'native_input_pages.png')
    report=dict(passed=True,scope='native Japanese weak-subject input field only; development observation, not new translation',release_eligible=False,rom_unchanged_sha256=ROM_SHA,added_translation_units=0,record_window='020010A6..020010AC',committed_record_hex=expected,routes=routes,snapshots=snapshots,save_checks=savechecks,header_source_consumer={k:h[k] for k in ['stream','stage','target','width','height','font','bytes']},pages_sha256=sha((out/'native_input_pages.png').read_bytes()),observer_sha256=sha((ROOT/'tools/capture_input_save.py').read_bytes()),report_tool_sha256=sha(Path(__file__).read_bytes()),rejected_save_navigation=['save-enter: jack-in then tournament because PET index1 retained; not save','save-commit: continuation of wrong menu route; unchanged SAV, not save evidence'],limits=['Four single-byte native Japanese characters; not Hangul logical capacity or field ABI proof.','Leading 01 remains constant marker, not character count. E5/98 byte terminator risk remains.','Cold load proves record persistence; field-specific normal conversational redisplay/descriptor writer and existing-save Hangul compatibility remain unresolved.','Header source consumer observed, but header33 still Japanese and no new ROM built.','Prior build tool pins are historical; these new observer/report tools are separately hashed, not part of that old build pin population.','Whole-game translation, images, RTC/shop and release review remain open.'])
    (out/'native_input_persistence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(dict(passed=True,record=expected,save=savechecks['save-overwrite'],report=str(out/'native_input_persistence.json')),ensure_ascii=False))

if __name__=='__main__':main()
