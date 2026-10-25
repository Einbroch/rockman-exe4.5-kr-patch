"""Replay controller recipes only; never import older-ROM checkpoints/saves."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

def main():
    rom=ROOT/'poc/output/exe45_ko_development_roll_escape_v1.gba';m=json.loads(rom.with_suffix('.json').read_text())
    require_hash(rom,m['output_sha256']);old=ROOT/'poc/runtime';prefix='roll-escape-v1-'
    routes=[
        ('cold-part1',None,'capture_megaman_escape.py',None),
        ('cold-part2','cold-part1','capture_megaman_escape.py',None),
        ('network-tutorial','cold-part2','capture_megaman_escape.py',None),
        ('battle-tutorial-complete','network-tutorial','capture_megaman_escape.py',None),
        ('l-target','battle-tutorial-complete','capture_megaman_escape.py',None),
        ('forbidden-clear','l-target','capture_megaman_escape.py',None),
        ('confirm-sample','battle-tutorial-complete','capture_megaman_escape_samples.py',2),
        ('success-sample','battle-tutorial-complete','capture_megaman_escape_samples.py',3),
        ('failure-sample','battle-tutorial-complete','capture_megaman_escape_samples.py',4),
        ('roll-confirm-sample','battle-tutorial-complete','capture_roll_escape_samples.py',8),
        ('roll-success-sample','battle-tutorial-complete','capture_roll_escape_samples.py',9),
        ('roll-failure-sample','battle-tutorial-complete','capture_roll_escape_samples.py',10),
        ('roll-forbidden-sample','battle-tutorial-complete','capture_roll_escape_samples.py',11),
        ('folder-regression','cold-part2','capture_chip_folder_qa.py',None),
        ('tactics-regression-r2','battle-tutorial-complete','capture_tactics_prompts.py',None)]
    for name,state,tool,script in routes:
        recipe=name.removeprefix('roll-')
        if name=='roll-forbidden-sample':recipe='success-sample'
        receipt=json.loads((old/('megaman-escape-v1-'+recipe)/'result.json').read_text())
        if receipt['rom_sha256']!='0edaf04c993efcdeced55e743e9f7a4dbbbdabab53d1ced99e759e8e69c1e97e' or not receipt['complete']:raise ValueError('recipe drift')
        out=old/(prefix+name)
        if out.exists():raise ValueError('fresh outputs required:'+name)
        args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--expect-rom-sha256',m['output_sha256'],
            '--mesen',str(old/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot',
            '--actions',receipt['actions'],'--capture-steps',','.join(map(str,receipt['capture_steps'])),'--timeout','240']
        if state:
            parent=old/(prefix+state)
            args+=['--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        if script is not None:args+=['--script',str(script)]
        print('START',name,flush=True)
        r=subprocess.run(args,cwd=ROOT)
        if r.returncode:return r.returncode
        print('DONE',name,flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
