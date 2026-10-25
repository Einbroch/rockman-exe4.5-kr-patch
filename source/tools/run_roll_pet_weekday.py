"""Normal Monday date-entry branch plus quarantined tournament hint displays."""
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read
import run_roll_pet_undernet as undernet
STEM='exe45_ko_development_roll_pet_weekday_v1'
PREFIX='roll-pet-weekday-v1-'
OUTDIR='roll_pet_weekday_v1'
DATE_ACTIONS='a:2:180,a:2:180,a:2:180,up:2:30,none:1:30,up:2:30,none:1:30,a:2:180,a:2:180,a:2:180,a:2:180,a:2:180,a:2:180,a:2:180'
INTRO_ACTIONS='none:1:60,a:2:180,a:2:180,a:2:180,a:2:180,a:2:180,a:2:180'

def weekday_chain(stem,prefix,parent):
    from run_roll_equipment_guides_matrix import RECIPE_ROM
    m=read(ROOT/f'poc/output/{stem}.json');origin=ROOT/'poc/runtime'/parent
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('weekday own-ROM parent')
    recipes=['roll-equipment-v1-select-survey','roll-equipment-v1-select-survey2','roll-equipment-v1-select-survey3','roll-equipment-v1-select-roll','roll-equipment-v1-roll-intro']
    names=['date','profile','navi-menu','select-roll','intro']
    for name,recipe in zip(names,recipes):
        r=read(ROOT/'poc/runtime'/recipe/'result.json')
        if not r['complete'] or r['rom_sha256']!=RECIPE_ROM:raise ValueError('weekday input recipe identity')
        tool='capture_roll_intro.py' if name=='select-roll' else 'capture_roll_pet.py' if name=='intro' else 'run_mesen_segment.py'
        actions=DATE_ACTIONS if name=='date' else r['actions'];steps=range(1,15) if name=='date' else r['capture_steps'];out=ROOT/'poc/runtime'/(prefix+name)
        if name=='intro':actions=INTRO_ACTIONS;steps=[2,4,6,7]
        args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,steps)),'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        subprocess.run(args,cwd=ROOT,check=True);origin=out

def diagnostics(stem,prefix,parent):
    m=read(ROOT/f'poc/output/{stem}.json');origin=ROOT/'poc/runtime'/parent
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('weekday diagnostic own-ROM parent')
    def run(s):
        actions='none:1:7,r:2:180,none:1:180'+(',a:2:180,none:1:180' if s in [26,28] else '')
        args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_pet_weekday.py'),'--talk-script',str(s),'--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/f'{prefix}script{s}'),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        subprocess.run(args,cwd=ROOT,check=True)
    with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(run,[26,28,29]))

def main():
    previous=undernet.STEM,undernet.PREFIX,undernet.OUTDIR
    try:undernet.STEM=STEM;undernet.PREFIX=PREFIX;undernet.OUTDIR=OUTDIR;undernet.main()
    finally:undernet.STEM,undernet.PREFIX,undernet.OUTDIR=previous
    weekday_chain(STEM,PREFIX+'weekday-',PREFIX+'roll-cold-part1')
    diagnostics(STEM,PREFIX,PREFIX+'weekday-intro')

if __name__=='__main__':main()
