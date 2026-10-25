"""Qualifier plus native nickname/mail rendering; not receipt/progress proof."""
from PIL import Image
from report_roll_pet import ROOT
from run_roll_pet_mail import STEM,PREFIX,OUTDIR

def main():
    import report_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,23,24,25,30,31,34,16,18,19,20,21,22,32,33];reports=base.main(new_units=2)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(480,160))
    for i,s in enumerate([32,33]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/'step_003.png'),(i*240,0))
    sheet.save(ROOT/'analysis'/OUTDIR/'mail_diagnostic_pages.png');return reports

if __name__=='__main__':main()
