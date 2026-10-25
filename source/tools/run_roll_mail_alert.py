"""Own-ROM native mail notification and existing focused regression routes."""
import sys,subprocess
from report_roll_pet import ROOT,read
import run_roll_pet_weekday as weekday
STEM='exe45_ko_development_roll_mail_alert_v1'
PREFIX='roll-mail-alert-v1-'
OUTDIR='roll_mail_alert_v1'
ACTIONS='none:1:60,a:2:180,a:2:180,a:2:180,a:2:60,none:1:90,none:1:120,none:1:90,a:2:180,none:1:180'

def arrival(stem,prefix,parent):
    m=read(ROOT/f'poc/output/{stem}.json');origin=ROOT/'poc/runtime'/parent
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('mail arrival own-ROM parent')
    args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_mail_alert.py'),'--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(prefix+'arrival')),'--probe','snapshot','--actions',ACTIONS,'--capture-steps','1,2,3,4,5,6,7,8,9,10','--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
    subprocess.run(args,cwd=ROOT,check=True)

def main():
    previous=weekday.STEM,weekday.PREFIX,weekday.OUTDIR
    try:weekday.STEM=STEM;weekday.PREFIX=PREFIX;weekday.OUTDIR=OUTDIR;weekday.main()
    finally:weekday.STEM,weekday.PREFIX,weekday.OUTDIR=previous
    arrival(STEM,PREFIX,PREFIX+'weekday-select-roll')

if __name__=='__main__':main()
