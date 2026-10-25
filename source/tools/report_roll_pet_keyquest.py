"""Key-quest diagnostic pixel proofs and same-ROM focused regressions."""
from PIL import Image
from report_roll_pet import ROOT
from run_roll_pet_keyquest import STEM,PREFIX,OUTDIR

def main():
    import report_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,23,24,25,31];reports=base.main(new_units=3)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(720,160))
    for i,s in enumerate([23,24,25]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/'step_003.png'),(i*240,0))
    sheet.save(ROOT/'analysis'/OUTDIR/'keyquest_diagnostic_pages.png');return reports

if __name__=='__main__':main()
