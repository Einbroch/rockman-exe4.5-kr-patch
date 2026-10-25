"""Fresh034 bounded CPU regression suite, no runtime/rendering assertion."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read


def main():
    rp=ROOT/'poc/output/pending500_034_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    for stem in ('profile_chips','profile_arrays','profile','opponent_chips','event_buffers','event_time_format','event_frequency','calendar_date','calendar_current_date','choice_sfx','vertical_wide'):
        subprocess.run([sys.executable,'-X','utf8','tools/bench_'+stem+'_product_034.py'],cwd=ROOT,check=True)
    subprocess.run([sys.executable,'-X','utf8','tools/verify_native_controls_034.py'],cwd=ROOT,check=True)
    print('034 fresh CPU suite completed; no GBA/runtime/release claim')


if __name__=='__main__':main()
