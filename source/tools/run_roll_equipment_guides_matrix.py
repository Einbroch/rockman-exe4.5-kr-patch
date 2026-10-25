"""Replay normal Roll selection recipes, never reuse prior-ROM state data."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

RECIPE_ROM='fafc0a85d217fad5b614fa0b5f6155f195cb6406ded300c10952aac8d56cff2d'

def main(stem,prefix,pet_probe=False,intro_probe=False,gutsman=False,numberman=False,numberman_intro_probe=False,numberman_pet_probe=False):
    rom=ROOT/f'poc/output/{stem}.gba';m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    runtime=ROOT/'poc/runtime'
    # Prefix destinations are fresh, recipe receipts supply controller input
    # only. Every checkpoint parent below was created in this exact run.
    recipes=['roll-equipment-v1-rockman-cold-part1','roll-equipment-v1-select-survey','roll-equipment-v1-select-survey2','roll-equipment-v1-select-survey3','roll-equipment-v1-select-roll','roll-equipment-v1-roll-intro','roll-equipment-v1-roll-equipment']
    names=['cold-part1','date','profile','navi-menu','select-roll','intro','equipment']
    if gutsman and numberman:raise ValueError('select one Navi route')
    if numberman_intro_probe and not numberman:raise ValueError('NumberMan intro observation requires NumberMan route')
    if numberman_pet_probe and not numberman:raise ValueError('NumberMan PET observation requires NumberMan route')
    if gutsman or numberman:
        if pet_probe or intro_probe:raise ValueError('GutsMan route uses normal controller-only runner, not Roll observers')
        names[-3]='select-numberman' if numberman else 'select-gutsman';names=names[:-1];recipes=recipes[:-1]
    for i,(name,recipe) in enumerate(zip(names,recipes)):
        r=json.loads((runtime/recipe/'result.json').read_text());out=runtime/(prefix+name)
        if not r['complete'] or r['rom_sha256']!=RECIPE_ROM or out.exists():raise ValueError('recipe identity or fresh route required')
        tool='capture_attack_caption_supply.py' if name=='equipment' else 'run_mesen_segment.py'
        if pet_probe and name in ['select-roll','intro']:tool='capture_roll_pet.py'
        if intro_probe and name=='select-roll':tool='capture_roll_intro.py'
        if numberman_intro_probe and name=='select-numberman':tool='capture_numberman_intro.py'
        if numberman_pet_probe and name=='intro':tool='capture_numberman_pet.py'
        actions=r['actions']
        if (gutsman or numberman) and name in ['select-gutsman','select-numberman']:
            if actions.count('right:2:60')!=1:raise ValueError('selection recipe anchor')
            actions=actions.replace('right:2:60',','.join(['right:2:60']*(3 if numberman else 2)),1)
        args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(runtime/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,r['capture_steps'])),'--timeout','240']
        if i:
            parent=runtime/(prefix+names[i-1]);args+=['--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        print('START',name,flush=True);rc=subprocess.run(args,cwd=ROOT).returncode
        if rc:return rc
    return 0

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--stem',default='exe45_ko_development_roll_equipment_guides_v1');ap.add_argument('--prefix',required=True);ap.add_argument('--pet-probe',action='store_true');ap.add_argument('--intro-probe',action='store_true');ap.add_argument('--gutsman',action='store_true');ap.add_argument('--numberman',action='store_true');ap.add_argument('--numberman-intro-probe',action='store_true');ap.add_argument('--numberman-pet-probe',action='store_true');args=ap.parse_args();raise SystemExit(main(args.stem,args.prefix,args.pet_probe,args.intro_probe,args.gutsman,args.numberman,args.numberman_intro_probe,args.numberman_pet_probe))
