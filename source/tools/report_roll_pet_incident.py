"""Incident two-page render diagnostics plus focused same-ROM regressions."""
from PIL import Image
from report_roll_pet import ROOT,read
from run_roll_pet_incident import STEM,PREFIX,OUTDIR

def main():
    import report_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[11,12,14,15,17,31];reports=base.main(new_units=3)
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    sheet=Image.new('RGB',(720,160))
    for i,(s,step) in enumerate([(17,2),(17,4),(31,3)]):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/f'step_{step:03}.png'),(i*240,0))
    sheet.save(ROOT/'analysis'/OUTDIR/'incident_diagnostic_pages.png');return reports

if __name__=='__main__':main()
