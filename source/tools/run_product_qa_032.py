"""Exact032 source/static/CPU and normal-controller calendar QA; no packaging."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read


def main():
    rom='poc/output/pending500_032_v1.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);h=m['output_sha256']
    def run(*args):
        print('QA032',args[0],flush=True);subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,check=True)
    run('tools/verify_layout500_product_032.py','--out','analysis/pending500_032_v1/integration_pre_repro.json')
    for name in ('bench_profile_chips_product_032.py','bench_profile_arrays_product_032.py','bench_profile_product_032.py','bench_opponent_chips_product_032.py','bench_event_buffers_product_032.py','bench_event_time_format_product_032.py','bench_event_frequency_product_032.py','bench_calendar_date_product_032.py','bench_calendar_current_date_product_032.py'):run('tools/'+name)
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_032_v1/a3_cpu.json')
    run('tools/bench_hint_rom_reader_024.py','--rom',rom,'--out','analysis/pending500_032_v1/b0_cpu.json','--field-b0')
    run('tools/verify_layout500_integrity_024.py','--rom',rom,'--out','analysis/pending500_032_v1/integrity.json')
    run('tools/verify_native_control_product_032.py')
    run('tools/run_first_mail_regression.py','--rom',rom,'--prefix','pending500-032-v1','--expanded-startup-captures')
    run('tools/verify_layout500_normal_032.py')
    def route(name,parent,actions):
        run('tools/capture_event_buffers_product_032.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/'+name,'--probe','snapshot','--actions',actions,'--timeout','240','--state','poc/runtime/'+parent+'/checkpoint.mss','--state-origin','poc/runtime/'+parent+'/result.json')
    prefix='pending500-032-menu-'
    routes=[('home','pending500-032-v1-complete','b:2:120,right:2:90,none:1:90'),('register',prefix+'home','none:1:30,a:2:90,a:2:90'),('second',prefix+'register','none:1:30,down:2:90'),('cancel',prefix+'second','none:1:30,b:2:90'),('time-edit',prefix+'register','none:1:30,a:2:90'),('time',prefix+'time-edit','none:1:30,up:2:90,none:1:10,up:2:90,a:2:90,a:2:90'),('meal',prefix+'time','none:1:30,down:2:90,none:1:10,down:2:90,a:2:90,none:1:10,a:2:90'),('inventory','pending500-032-v1-complete','b:2:120,left:2:90'),('inventory-cancel',prefix+'inventory','none:1:30,b:2:90'),('inventory-reentry',prefix+'inventory-cancel','none:1:30,left:2:90'),('inventory-accept',prefix+'inventory','none:1:30,a:2:90')]
    for name,parent,actions in routes:route(prefix+name,parent,actions)
    prefix='calendar-anniversary-032-product-'
    routes=[('menu','pending500-032-v1-complete','b:2:120,right:2:90,none:1:90,a:2:90,a:2:90'),('types',prefix+'menu-v1','none:1:30,down:2:90,a:2:90'),('other',prefix+'types-v1','none:1:30,down:2:90,none:1:10,down:2:90,a:2:90'),('picker',prefix+'other-v1','none:1:30,up:2:30,right:2:30,right:2:30,right:2:30,right:2:30,right:2:30,right:2:30'),('ten',prefix+'picker-v1','none:1:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,a:2:30,start:2:120'),('register',prefix+'ten-v1','none:1:30,a:2:120,a:2:120,a:2:120'),('delete-selector',prefix+'register-v1','none:1:30,down:2:90,none:1:30,down:2:90,a:2:120'),('delete-list',prefix+'delete-selector-v1','none:1:30,down:2:90,a:2:120'),('delete-first',prefix+'delete-list-v1','none:1:30,a:2:120'),('delete-confirm',prefix+'delete-first-v1','none:1:30,a:2:120'),('delete-no',prefix+'delete-confirm-v1','none:1:30,right:2:120,a:2:120'),('delete-yes',prefix+'delete-confirm-v1','none:1:30,a:2:120')]
    for name,parent,actions in routes:route(prefix+name+'-v1',parent,actions)
    run('tools/verify_calendar_anniversary_product_032.py')
    run('tools/verify_calendar_menu_product_032.py')
    print('032 mechanical/runtime complete; direct visual review and repro audit still required',flush=True)


if __name__=='__main__':main()
