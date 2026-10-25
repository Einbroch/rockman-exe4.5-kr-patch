"""Original L provider/caller with qualified native identity at selector only."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native038_loaded_guards import arguments

def main():
    rom='poc/output/pending500_038_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    parent='poc/runtime/pending500-038-hint-controls-observe-v1';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own038 settled hint normal state required')
    entries=read(parent+'/hint_entries.json')['entries']
    if not any(x['pc']==0x0804F7FC and x['script_provider']==0 and x['Navi']==0 for x in entries):raise ValueError('Own038 original L hint route not observed')
    load='poc/runtime/pending500-038-hint-qualified-load-v1/result.json'
    cmd=[sys.executable,'-X','utf8','tools/capture_hint_boundary038_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-038-hint-qualified-boundary-v1','--probe','snapshot','--actions','l:2:180,a:2:180,down+right:20:60','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--boundary-archive','78AE58','--native-load-origin',str(ROOT/load),'--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
