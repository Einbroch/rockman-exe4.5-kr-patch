"""Two-page undernet hint rendering; not progression or encounter proof."""
from PIL import Image
from report_roll_pet import ROOT
from run_roll_pet_undernet import STEM,PREFIX,OUTDIR

def main():
    import report_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,23,24,25,30,31,34,16,18,19,20,21,22,32,33,27];reports=base.main(new_units=2)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(480,160))
    for i,step in enumerate([3,5]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script27'/f'step_{step:03}.png'),(i*240,0))
    sheet.save(ROOT/'analysis'/OUTDIR/'undernet_diagnostic_pages.png');return reports

if __name__=='__main__':main()
