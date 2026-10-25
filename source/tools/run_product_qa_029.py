"""Exact029 development QA; no distribution package or ROM mutation."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_029_v1.gba';rp=ROOT/rom;meta=read(rp.with_suffix('.json'));h=meta['output_sha256'];require_hash(rp,h)
    def run(*args):
        print('QA029',args[0],flush=True)
        subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,check=True)
    run('tools/verify_layout500_product_029.py','--out','analysis/pending500_029_v1/integration_pre_repro.json')
    run('tools/bench_profile_arrays_product_029.py')
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_029_v1/a3_cpu.json')
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_029_v1/b0_cpu.json','--field-b0')
    run('tools/verify_layout500_integrity_024.py','--rom',rom,'--out','analysis/pending500_029_v1/integrity.json')
    run('tools/verify_native_control_product_029.py')
    run('tools/run_first_mail_regression.py','--rom',rom,'--prefix','pending500-029-v1','--expanded-startup-captures')
    run('tools/verify_layout500_normal_029.py')
    actions=read('poc/runtime/pending500-029-v1-complete/result.json')['actions']+',b:2:120,r:2:240,none:1:120,a:2:240,none:1:120,a:2:180,none:1:120'
    for case in ('initializer-older-bro','initializer-fav-show'):
        run('tools/capture_profile_product_029.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-029-v1-raw-'+case,'--probe','snapshot','--actions',actions,'--timeout','300','--state','poc/runtime/pending500-029-v1-pagecycle/checkpoint.mss','--state-origin','poc/runtime/pending500-029-v1-pagecycle/result.json','--display-case',case,'--capture-steps','34,37,39,41')
    run('tools/verify_profile_product_029.py')
    print('QA029 mechanical stages finished. Visual inspection/repro/finalizer still required.',flush=True)

if __name__=='__main__':main()
