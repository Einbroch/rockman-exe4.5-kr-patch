"""Incident location render proofs; progression flags preserved, not forced."""
from PIL import Image
from report_roll_pet import ROOT
from run_roll_pet_events import STEM,PREFIX,OUTDIR

def main():
    import report_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,23,24,25,30,31,34,16,18,19,20,21,22];reports=base.main(new_units=6)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(720,320))
    for i,s in enumerate([16,18,19,20,21,22]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/'step_003.png'),((i%3)*240,(i//3)*160))
    sheet.save(ROOT/'analysis'/OUTDIR/'events_diagnostic_pages.png');return reports

if __name__=='__main__':main()
