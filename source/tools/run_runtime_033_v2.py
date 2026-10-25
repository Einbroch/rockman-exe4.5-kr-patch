"""Actual033 own coldboot plus quarantined native3choice/manager samples."""
import argparse
import subprocess
import sys
from build_visibility_poc import ROOT, require_hash
from cumulative_batch500 import read


def main():
    p = argparse.ArgumentParser(); p.add_argument('--samples-only', action='store_true'); a = p.parse_args()
    rom = 'poc/output/pending500_033_v1.gba'; rp = ROOT/rom; m = read(rp.with_suffix('.json')); require_hash(rp, m['output_sha256']); h = m['output_sha256']
    proof = read('analysis/pending500_033_v1/integration_pre_repro.json')
    if not proof['passed'] or proof['rom_sha256'] != h: raise ValueError('033 static product prerequisite')
    if not a.samples_only:
        subprocess.run([sys.executable, '-X', 'utf8', 'tools/run_first_mail_regression.py', '--rom', rom,
                        '--prefix', 'pending500-033-v1', '--expanded-startup-captures'], cwd=ROOT, check=True)
    parent = 'poc/runtime/pending500-033-v1-complete'; prefix = 'b:2:120,r:2:240,none:1:120'
    cases = [
        ('vertical-three', 'vertical-three-cancel', prefix+',a:2:240,none:1:120,down:2:60,down:2:60,up:2:60,up:2:60,left:2:60,right:2:60,down:2:60,down:2:60,b:2:180,none:1:120', '3,5,6,7,8,9,10,11,12,13,14,15'),
        ('vertical-three', 'vertical-three-a0', prefix+',a:2:240,none:1:120,a:2:180,none:1:120', '3,5,6,7'),
        ('vertical-three', 'vertical-three-a1', prefix+',a:2:240,none:1:120,down:2:60,a:2:180,none:1:120', '3,5,6,7,8'),
        ('vertical-three', 'vertical-three-a2', prefix+',a:2:240,none:1:120,down:2:60,down:2:60,a:2:180,none:1:120', '3,5,6,7,8,9'),
        ('manager', 'manager-cancel', prefix+',a:2:240,none:1:120,a:2:240,none:1:120,right:2:60,left:2:60,right:2:60,b:2:180,none:1:120,a:2:180,none:1:120', '3,5,7,8,9,10,11,12,13,14')]
    for case, name, actions, captures in cases:
        print('QA033 diagnostic', name, flush=True)
        subprocess.run([sys.executable, '-X', 'utf8', 'tools/capture_choices_033_v2.py', '--rom', rom, '--expect-rom-sha256', h,
                        '--mesen', 'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe', '--out', 'poc/runtime/pending500-033-v1-raw-'+name,
                        '--probe', 'snapshot', '--actions', actions, '--timeout', '240', '--state', parent+'/checkpoint.mss',
                        '--state-origin', parent+'/result.json', '--display-case', case, '--capture-steps', captures], cwd=ROOT, check=True)
    print('033 capture receipts finished; artifact/pixel/choice verification and direct visual review still required', flush=True)


if __name__ == '__main__': main()

