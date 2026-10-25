"""Actual031 mechanical/runtime checks, no distribution packaging."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read


def main():
    rom='poc/output/pending500_031_v1.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);h=m['output_sha256']
    def run(*args):
        print('QA031',args[0],flush=True);subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,check=True)
    run('tools/verify_layout500_product_031.py','--out','analysis/pending500_031_v1/integration_pre_repro.json')
    for name in ('bench_profile_chips_product_031.py','bench_profile_arrays_product_031.py','bench_profile_product_031.py','bench_opponent_chips_product_031.py','bench_event_buffers_product_031.py','bench_event_time_format_product_031.py','bench_event_frequency_product_031.py'):run('tools/'+name)
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_031_v1/a3_cpu.json')
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_031_v1/b0_cpu.json','--field-b0')
    run('tools/verify_layout500_integrity_024.py','--rom',rom,'--out','analysis/pending500_031_v1/integrity.json')
    run('tools/verify_native_control_product_031.py')
    run('tools/run_first_mail_regression.py','--rom',rom,'--prefix','pending500-031-v1','--expanded-startup-captures')
    run('tools/verify_layout500_normal_031.py')
    actions='b:2:120,r:2:240,none:1:120,a:2:240,none:1:120,a:2:180,none:1:120'
    for case in ('lost-chip-max','defeated-chip-max'):
        run('tools/capture_opponent_chip_product_031.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-031-v1-opponent-'+case,'--probe','snapshot','--actions',actions,'--timeout','240','--state','poc/runtime/pending500-031-v1-complete/checkpoint.mss','--state-origin','poc/runtime/pending500-031-v1-complete/result.json','--display-case',case,'--capture-steps','3,5,7')
    run('tools/verify_opponent_chip_product_031.py')
    parent='pending500-031-v1-complete';prefix='pending500-031-calendar-'
    routes=[('calendar',parent,'b:2:120,right:2:90,none:1:90,a:2:90,a:2:90,a:2:90'),('time',prefix+'calendar','none:1:30,up:2:90,none:1:10,up:2:90,a:2:90,a:2:90'),('meal',prefix+'time','none:1:30,down:2:90,none:1:10,down:2:90,a:2:90,none:1:10,a:2:90'),('selector',prefix+'meal','none:1:30,down:2:90,none:1:30,down:2:90,a:2:120'),('list',prefix+'selector','none:1:30,a:2:120'),('first',prefix+'list','none:1:30,a:2:120'),('confirm',prefix+'first','none:1:30,a:2:120'),('no',prefix+'confirm','none:1:30,right:2:120,a:2:120'),('cancel',prefix+'confirm','none:1:30,b:2:120'),('yes',prefix+'confirm','none:1:30,a:2:120'),('reentry',prefix+'no','none:1:30,a:2:120')]
    for name,parent,actions in routes:
        run('tools/capture_event_buffers_product_031.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/'+prefix+name,'--probe','snapshot','--actions',actions,'--timeout','240','--state','poc/runtime/'+parent+'/checkpoint.mss','--state-origin','poc/runtime/'+parent+'/result.json')
    run('tools/verify_calendar_delete_product_031.py')
    print('QA031 finished; direct visual review and independent repro remain.',flush=True)


if __name__=='__main__':main()
