"""Exact038 hint native-load diagnostic from own pre-jack-in state."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native038_loaded_guards import arguments

def main():
    rom='poc/output/pending500_038_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    normal=read('analysis/pending500_038_v2/normal_path_v1.json')
    if not normal['passed'] or normal['rom_sha256']!=m['output_sha256']:raise ValueError('Own038 verified normal route required')
    parent='poc/runtime/pending500-038-normal-v1-06';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own038 state only')
    oldpath='poc/runtime/pending500-036-qualified-native-a1-v1/result.json';authority=read('analysis/pending500_036_v1/native_boundaries_v1.json')
    key=next(k for k in authority['receipts'] if k.replace('\\','/')==oldpath);require_hash(ROOT/oldpath,authority['receipts'][key]);old=read(oldpath)
    actions=old['actions'].split(',')[:19]
    if len(actions)!=19:raise ValueError('Known pre-load controller recipe')
    cmd=[sys.executable,'-X','utf8','tools/capture_hint_load038_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-038-hint-qualified-load-v1','--probe','snapshot','--actions',','.join(actions),'--capture-steps','19','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
