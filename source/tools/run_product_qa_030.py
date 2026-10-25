"""Exact030 development QA, no distribution outputs or ROM mutation."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_030_v1.gba';rp=ROOT/rom;meta=read(rp.with_suffix('.json'));h=meta['output_sha256'];require_hash(rp,h)
    def run(*args):
        print('QA030',args[0],flush=True)
        subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,check=True)
    run('tools/verify_layout500_product_030.py','--out','analysis/pending500_030_v1/integration_pre_repro.json')
    for script in ('bench_profile_chips_product_030.py','bench_profile_arrays_product_030.py','bench_profile_product_030.py'):run('tools/'+script)
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_030_v1/a3_cpu.json')
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_030_v1/b0_cpu.json','--field-b0')
    run('tools/verify_layout500_integrity_024.py','--rom',rom,'--out','analysis/pending500_030_v1/integrity.json')
    run('tools/verify_native_control_product_030.py')
    run('tools/run_first_mail_regression.py','--rom',rom,'--prefix','pending500-030-v1','--expanded-startup-captures')
    run('tools/verify_layout500_normal_030.py')
    actions='b:2:120,r:2:240,none:1:120,a:2:240,none:1:120,a:2:180,none:1:120'
    for case in ('standard1-max','giga-max'):
        run('tools/capture_profile_chip_product_030.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-030-v1-raw-'+case,'--probe','snapshot','--actions',actions,'--timeout','240','--state','poc/runtime/pending500-030-v1-complete/checkpoint.mss','--state-origin','poc/runtime/pending500-030-v1-complete/result.json','--display-case',case,'--capture-steps','3,5,7')
    run('tools/verify_profile_chip_product_030.py')
    print('QA030 mechanical stages finished; direct visual review/repro/finalizer remain.',flush=True)

if __name__=='__main__':main()
