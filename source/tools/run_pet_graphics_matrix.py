"""New graphics ROM cold-chain, seven native menu states and unchanged folder route."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

def main():
    rom=ROOT/'poc/output/exe45_ko_development_pet_graphics_v1.gba';m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    old=ROOT/'poc/runtime';prefix='pet-graphics-v1-'
    routes=[]
    for name,parent,tool in [('cold-part1',None,'run_mesen_segment.py'),('cold-part2','cold-part1','capture_pet_graphics_load.py')]:
        receipt=json.loads((old/('roll-tactics-v1-'+name)/'result.json').read_text())
        if receipt['rom_sha256']!='1ca65635bcfb92ff3845bf7b75cf6491a045f32cceda5ec16eca977d7d45f31f' or not receipt['complete']:raise ValueError('recipe source')
        routes.append((name,parent,tool,receipt['actions'],receipt['capture_steps']))
    routes.append(('focus','cold-part2','run_mesen_segment.py','b:2:60,'+','.join(['down:2:45']*6),list(range(1,8))))
    actions=['b:2:60'];captures=[]
    for row in range(7):
        actions+=['a:2:70','none:1:30'];captures.append(len(actions))
        actions+=['b:2:50'];captures.append(len(actions))
        if row<6:actions+=['down:2:40']
    routes.append(('prompts','cold-part2','run_mesen_segment.py',','.join(actions),captures))
    folder=json.loads((old/'roll-tactics-v1-folder-regression/result.json').read_text())
    routes.append(('folder-regression','cold-part2','capture_chip_folder_qa.py',folder['actions'],folder['capture_steps']))
    for name,parent,tool,actions,captures in routes:
        out=old/(prefix+name)
        if out.exists():raise ValueError('fresh route required:'+name)
        args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--expect-rom-sha256',m['output_sha256'],
            '--mesen',str(old/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot',
            '--actions',actions,'--capture-steps',','.join(map(str,captures)),'--timeout','240']
        if parent:
            state=old/(prefix+parent);args+=['--state',str(state/'checkpoint.mss'),'--state-origin',str(state/'result.json')]
        print('START',name,flush=True)
        rc=subprocess.run(args,cwd=ROOT).returncode
        if rc:return rc
        print('DONE',name,flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
