"""Native A1/A3 qualified source lookup/load/selector display experiments."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    case=sys.argv[1]
    if case not in ('a1','a3'):raise ValueError('a1 or a3')
    rom='poc/output/pending500_036_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);network=[]
    for name in ('field-walk-v2','field-walk-v3','field-portal-v1','field-portal-v2'):network+=read('poc/runtime/pending500-035-baseline034-'+name+'/result.json')['actions'].split(',')
    if len(network)!=19:raise ValueError('HomeB0 to A0 normal input recipe')
    actions=network+['a:2:150']*6+['up+right:185:10','up+left:18:10','up+right:46:10','down+right:18:10','up+right:360:10','up+left:88:10','a:2:180']
    if len(actions)!=32:raise ValueError('Qualified first-page step')
    if case=='a1':actions+=['a:2:180','none:1:90','a:2:180','none:1:90','right:2:90','b:2:180','none:1:90','a:2:24','down+right:20:60'];captures='19,25,31,32,33,35,37,38,40,41'
    else:actions+=['a:2:180','right:2:90','b:2:180','a:2:180','a:2:24','down+right:20:60'];captures='19,25,31,32,33,34,35,36,37,38'
    parent='poc/runtime/pending500-036-sunday-plugin-confirm-v1'
    subprocess.run([sys.executable,'-X','utf8','tools/capture_native_scene036_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-036-qualified-native-'+case+'-v1','--probe','snapshot','--native-scene',case,'--actions',','.join(actions),'--capture-steps',captures,'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300'],cwd=ROOT,check=True)

if __name__=='__main__':main()
