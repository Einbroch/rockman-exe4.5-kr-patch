"""Fresh ROM-owned cold chain and bounded equipment/PET regression."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

def main():
    rom=ROOT/'poc/output/exe45_ko_development_folder_labels_v1.gba'
    meta=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,meta['output_sha256'])
    runtime=ROOT/'poc/runtime';prefix='folder-labels-v1-'
    routes=[]
    for name,parent,tool in [('cold-part1',None,'run_mesen_segment.py'),('cold-part2','cold-part1','capture_pet_graphics_load.py'),('folder-regression','cold-part2','capture_folder_labels_qa.py')]:
        recipe=json.loads((runtime/('pet-graphics-v1-'+name)/'result.json').read_text())
        if recipe['rom_sha256']!='2ec5cf763c8cf063cc67e2e02609a3097de2471425792670c5172e523ae69f40' or not recipe['complete']:raise ValueError('recipe receipt')
        routes.append((name,parent,tool,recipe['actions'],recipe['capture_steps']))
    routes.append(('focus','cold-part2','run_mesen_segment.py','b:2:60,'+','.join(['down:2:45']*6),list(range(1,8))))
    for name,parent,tool,actions,captures in routes:
        out=runtime/(prefix+name)
        if out.exists():raise ValueError('fresh route required:'+name)
        args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--expect-rom-sha256',meta['output_sha256'],'--mesen',str(runtime/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,captures)),'--timeout','240']
        if parent:
            state=runtime/(prefix+parent);args+=['--state',str(state/'checkpoint.mss'),'--state-origin',str(state/'result.json')]
        print('START',name,flush=True)
        rc=subprocess.run(args,cwd=ROOT).returncode
        if rc:return rc
        print('DONE',name,flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
