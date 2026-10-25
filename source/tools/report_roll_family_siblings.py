"""Four normal sibling scenes and same-current-ROM cumulative regressions."""
from run_roll_family_siblings import STEM,PREFIX,BROTHERS
from report_roll_pet import ROOT,read

def main(outdir='roll_family_siblings_v1'):
    import report_roll_family_sisters as sisters
    previous=sisters.STEM,sisters.PREFIX
    try:sisters.STEM=STEM;sisters.PREFIX=PREFIX;reports=sisters.main(outdir)
    finally:sisters.STEM,sisters.PREFIX=previous
    import report_roll_family as family
    previous=family.STEM,family.PREFIX
    try:
        family.STEM=STEM
        for name,recipe,question,response in BROTHERS:
            family.PREFIX=PREFIX+name+'-';reports.append(family.main(outdir+'/'+name,question,response,(10,11,12,13,14,15)))
    finally:family.STEM,family.PREFIX=previous
    expected=read(ROOT/f'poc/output/{STEM}.json')['output_sha256']
    if len(reports)!=11 or not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==expected for r in reports):raise ValueError('cumulative sibling reports')
    return reports

if __name__=='__main__':main()
