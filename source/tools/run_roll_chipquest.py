"""Fresh shared-consumer normal regressions and one quarantined chip104 page."""
import sys,subprocess
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_roll_chipquest_v1'
PREFIX='roll-chipquest-v1-'
OUTDIR='roll_chipquest_v1'

def main():
    import run_roll_pet_license as base
    from run_roll_pet_weekday import weekday_chain
    from run_roll_mail_alert import arrival
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[];base.focused()
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    weekday_chain(STEM,PREFIX+'weekday-',PREFIX+'roll-cold-part1')
    arrival(STEM,PREFIX,PREFIX+'weekday-select-roll')
    m=read(ROOT/f'poc/output/{STEM}.json');origin=ROOT/'poc/runtime'/(PREFIX+'roll-intro')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_chipquest.py'),'--talk-script','13','--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+'script13')),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180','--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],cwd=ROOT,check=True)

if __name__=='__main__':main()
