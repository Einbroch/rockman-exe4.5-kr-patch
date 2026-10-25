"""Guide ROM-owned cold-chain and normal equipment/folder/PET routes."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

def main(stem='exe45_ko_development_equipment_guides_v1',prefix='equipment-guides-v1-',weapons=False,caption=False):
    rom=ROOT/f'poc/output/{stem}.gba';meta=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,meta['output_sha256'])
    runtime=ROOT/'poc/runtime';routes=[]
    for name,parent,tool in [('cold-part1',None,'run_mesen_segment.py'),('cold-part2','cold-part1','capture_pet_graphics_load.py'),('folder-regression','cold-part2','capture_folder_labels_qa.py'),('equipment','cold-part2','capture_equipment_guides.py'),('focus','cold-part2','run_mesen_segment.py')]:
        if name=='equipment' and caption:tool='capture_attack_caption_supply.py'
        r=json.loads((runtime/('equipment-labels-v2-'+name)/'result.json').read_text())
        if r['rom_sha256']!='2c25fa199817caa94765e7f5c5d94370cd54f477f72dbf6d5fbb46a534faa0ea' or not r['complete']:raise ValueError('recipe receipt')
        routes.append((name,parent,tool,r['actions'],r['capture_steps']))
    if weapons:
        routes.append(('weapon-cycle-r3','equipment','capture_equipment_guides.py','none:1:60,down:2:60,right:2:60,none:1:60,right:2:60,none:1:60,left:2:60,left:2:60,right:2:60,right:2:60,b:2:90,a:2:60,a:2:180,down:2:60,none:1:60',[3,5,6,7,8,9,10,11,13,14,15]))
    for name,parent,tool,actions,captures in routes:
        out=runtime/(prefix+name)
        if out.exists():raise ValueError('fresh route required:'+name)
        args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--expect-rom-sha256',meta['output_sha256'],'--mesen',str(runtime/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,captures)),'--timeout','240']
        if parent:
            state=runtime/(prefix+parent);args+=['--state',str(state/'checkpoint.mss'),'--state-origin',str(state/'result.json')]
        print('START',name,flush=True);rc=subprocess.run(args,cwd=ROOT).returncode
        if rc:return rc
        print('DONE',name,flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
