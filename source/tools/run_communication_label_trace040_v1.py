"""Observe untranslated039 small-label source reads; no040 artifact or edits."""
import sys,struct,subprocess
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress
from communication039_loaded_guards import arguments


def main():
    rom='poc/output/pending500_039_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);native=lz77_decompress(sp.read_bytes(),0x6F56B8)[0];lo=0x02024000+struct.unpack_from('<H',native,5*2)[0];hi=0x02024000+struct.unpack_from('<H',native,7*2)[0];parent='poc/runtime/pending500-039-communication-v1-06';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('039 own pre-communication loader state')
    cmd=[sys.executable,'-X','utf8','tools/run_mesen_segment.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-039-label-trace040-v1','--probe','textread','--watch-start',hex(lo),'--watch-end',hex(hi),'--actions','a:2:180,none:1:60','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
