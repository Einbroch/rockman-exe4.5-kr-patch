"""Equipment-label ROM-owned cold chain, three focus states and regressions."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

def main():
    rom=ROOT/'poc/output/exe45_ko_development_equipment_labels_v2.gba';meta=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,meta['output_sha256'])
    runtime=ROOT/'poc/runtime';prefix='equipment-labels-v2-';routes=[]
    for name,parent,tool in [('cold-part1',None,'run_mesen_segment.py'),('cold-part2','cold-part1','capture_pet_graphics_load.py'),('folder-regression','cold-part2','capture_folder_labels_qa.py')]:
        r=json.loads((runtime/('folder-labels-v1-'+name)/'result.json').read_text())
        if r['rom_sha256']!='b4afc0967d53276dd23fb5980014be4ecbc3eafabb79694a20d44b5e782d1360' or not r['complete']:raise ValueError('recipe receipt')
        routes.append((name,parent,tool,r['actions'],r['capture_steps']))
    recipe=json.loads((runtime/'folder-labels-v1-equipment-roots/result.json').read_text())
    routes.append(('equipment','cold-part2','capture_equipment_labels.py',recipe['actions']+',b:2:90,a:2:60,a:2:180,none:1:180',[7,9,11,12,15]))
    routes.append(('focus','cold-part2','run_mesen_segment.py','b:2:60,'+','.join(['down:2:45']*6),list(range(1,8))))
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
