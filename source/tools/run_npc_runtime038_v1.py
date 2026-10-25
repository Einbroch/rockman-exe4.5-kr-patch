"""Two qualified A4 NPC boundaries on exact038, no old saved states."""
import sys,subprocess
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native038_loaded_guards import arguments

def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ('load','boundary'):raise ValueError('load|boundary')
    stage=sys.argv[1];rom='poc/output/pending500_038_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);normal=read('analysis/pending500_038_v2/normal_path_v1.json')
    if not normal['passed'] or normal['rom_sha256']!=m['output_sha256']:raise ValueError('Own038 normal audit required')
    if stage=='load':
        parent='poc/runtime/pending500-038-normal-v1-06';oldpath='poc/runtime/pending500-036-qualified-native-a1-v1/result.json';authority=read('analysis/pending500_036_v1/native_boundaries_v1.json');key=next(k for k in authority['receipts'] if k.replace('\\','/')==oldpath);require_hash(ROOT/oldpath,authority['receipts'][key]);actions=read(oldpath)['actions'].split(',')[:19]
        if len(actions)!=19:raise ValueError('Native load controller recipe')
        extra=['--qualified-archive','7B5110'];tool='tools/capture_native_load038_v1.py';captures='19'
    else:
        parent='poc/runtime/pending500-038-normal-v1-16';actions=['up+left:20:10','a:2:180','a:2:180','down+right:20:60'];extra=['--boundary-archive','7B5110','--native-load-origin',str(ROOT/'poc/runtime/pending500-038-npc-qualified-load-v1/result.json')];tool='tools/capture_native_boundary038_v1.py';captures='1,2,3,4'
    r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own038 normal seed')
    cmd=[sys.executable,'-X','utf8',tool,'--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-038-npc-qualified-'+stage+'-v1','--probe','snapshot','--actions',','.join(actions),'--capture-steps',captures,'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300']+extra+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
