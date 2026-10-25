"""Tournament display/page transition proofs plus focused own-ROM regression."""
from PIL import Image
from report_roll_pet import ROOT
from run_roll_pet_tournament import STEM,PREFIX,OUTDIR

def main():
    import report_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,23,24,25,30,31,34];reports=base.main(new_units=3)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(720,160))
    for i,(s,n) in enumerate([(30,3),(34,2),(34,4)]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/f'step_{n:03}.png'),(i*240,0))
    sheet.save(ROOT/'analysis'/OUTDIR/'tournament_diagnostic_pages.png');return reports

if __name__=='__main__':main()
