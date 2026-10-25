"""Borrow proven native actor/caller; independently proven resident boundary."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    case=sys.argv[1]
    if case not in ('a1','a3'):raise ValueError('a1/a3')
    rom='poc/output/pending500_036_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    actions=['up+left:20:10','a:2:180']
    if case=='a1':actions+=['a:2:180','none:1:90','a:2:180','right:2:90','b:2:180','a:2:24','down+right:20:60']
    else:actions+=['a:2:180','right:2:90','b:2:180','a:2:180','a:2:24','down+right:20:60']
    parent='poc/runtime/pending500-036-sunday-natural-npc-v2'
    subprocess.run([sys.executable,'-X','utf8','tools/capture_native_boundary036_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-036-native-boundary-'+case+'-v1','--probe','snapshot','--boundary-case',case,'--actions',','.join(actions),'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180'],cwd=ROOT,check=True)

if __name__=='__main__':main()
