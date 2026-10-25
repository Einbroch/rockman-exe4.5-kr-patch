"""039 source-language menu observation, no ROM edits/forced calls."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from communication039_loaded_guards import arguments


def main():
    rom='poc/output/pending500_039_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-039-communication-v1-06';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('039 exact pre-loader checkpoint')
    cmd=[sys.executable,'-X','utf8','tools/capture_communication_labels040_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-039-label-trace040-v2','--probe','snapshot','--actions','a:2:180,none:1:60','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
