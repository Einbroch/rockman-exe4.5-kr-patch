"""Fresh cumulative ROM cold chains; prior receipts supply controller input only."""
from report_roll_pet import ROOT,read
import run_roll_fortune_matrix as matrix
import run_roll_fortune_samples as samples

STEM='exe45_ko_development_roll_family_sisters_v1'
PREFIX='roll-family-sisters-v1-'
PREVIOUS='c15aa3d4c421719e7efb5fa47e73ee8741a797bcc8f5313e477b721699822c14'

def recipe(name):
    r=read(ROOT/'poc/runtime'/('roll-family-sister-v1-'+name)/'result.json')
    if not r['complete'] or r['rom_sha256']!=PREVIOUS:raise ValueError('prior input recipe identity')
    return r['actions']

def main(outdir='roll_family_sisters_v1'):
    matrix.STEM=STEM;matrix.PREFIX=PREFIX
    if matrix.main():raise ValueError('cold matrix failed')
    samples.STEM=STEM;samples.PREFIX=PREFIX;samples.main(outdir)
    matrix.segment('capture_roll_jackin.py',PREFIX+'jackin',PREFIX+'roll-intro',recipe('jackin'))
    matrix.segment('capture_roll_plugout.py',PREFIX+'choices',PREFIX+'jackin',recipe('choices'))
    matrix.segment('capture_roll_return.py',PREFIX+'normal',PREFIX+'jackin',recipe('normal'))
    matrix.segment('capture_roll_return_defeat.py',PREFIX+'defeat-diagnostic',PREFIX+'jackin',recipe('defeat-diagnostic'))
    older=read(ROOT/'poc/runtime/roll-family-survey-v1/result.json')
    if not older['complete'] or older['rom_sha256']!='dddc3a3d5c4f6c73f5f1e54be62ace5b919f839528b5caa3408482f9c9a85163':raise ValueError('older sister recipe')
    matrix.segment('capture_roll_family.py',PREFIX+'older-entry',PREFIX+'jackin',older['actions'])
    matrix.segment('capture_roll_family.py',PREFIX+'younger-entry',PREFIX+'jackin',recipe('entry'))
    for sibling in ['older','younger']:
        for branch,actions in [('yes','none:1:60,a:2:180,none:1:180'),('no','none:1:60,right:2:60,left:2:60,right:2:60,a:2:180,none:1:180')]:
            matrix.segment('capture_roll_family.py',PREFIX+sibling+'-'+branch,PREFIX+sibling+'-entry',actions)

if __name__=='__main__':main()
