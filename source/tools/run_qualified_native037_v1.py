"""Finite037 qualified NPC load/reader diagnostics, never natural coverage."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

CASES={'a1':'7A7FC4','a2':'7ADD74','a3':'7B39D0'}


def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ('load','boundary') or sys.argv[2] not in CASES:raise ValueError('load|boundary a1|a2|a3')
    stage,case=sys.argv[1:];archive=CASES[case];rom='poc/output/pending500_037_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    if stage=='load':
        history='poc/runtime/pending500-036-qualified-native-a1-v1/result.json';authority=read('analysis/pending500_036_v1/native_boundaries_v1.json');key=next(k for k in authority['receipts'] if k.replace('\\','/')==history);require_hash(ROOT/history,authority['receipts'][key]);old=read(history)
        actions=old['actions'].split(',')[:19]
        if len(actions)!=19:raise ValueError('Qualified load input recipe extent')
        parent='poc/runtime/pending500-037-normal-v1-06';tool='tools/capture_native_load037_v1.py';extra=['--qualified-archive',archive];captures='19'
    else:
        parent='poc/runtime/pending500-037-normal-v1-16';tool='tools/capture_native_boundary037_v1.py';load='poc/runtime/pending500-037-qualified-load-'+case+'-v1/result.json';extra=['--boundary-archive',archive,'--native-load-origin',str(ROOT/load)]
        actions=['up+left:20:10','a:2:180','a:2:180']
        if case=='a2':actions+=['a:2:180']
        actions+=['a:2:180','right:2:90','b:2:180','a:2:24','down+right:20:60'];captures=','.join(map(str,range(1,len(actions)+1)))
    origin=read(parent+'/result.json')
    if not origin['complete'] or origin['rom_sha256']!=m['output_sha256'] or origin.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own037 normal seed prerequisite')
    cmd=[sys.executable,'-X','utf8',tool,'--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-037-qualified-'+stage+'-'+case+'-v1','--probe','snapshot','--actions',','.join(actions),'--capture-steps',captures,'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300']+extra
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
