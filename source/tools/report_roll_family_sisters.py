"""Normal older/younger sister scenes plus same-current-ROM regressions."""
from report_roll_pet import ROOT,read
from run_roll_family_sisters import STEM,PREFIX

def main(outdir='roll_family_sisters_v1'):
    import report_roll_family as family
    previous=family.STEM,family.PREFIX
    try:
        family.STEM=STEM;family.PREFIX=PREFIX+'older-'
        older=family.main(outdir+'/older',5,6,(9,10,11,12,13,14))
        family.PREFIX=PREFIX+'younger-'
        younger=family.main(outdir+'/younger')
    finally:family.STEM,family.PREFIX=previous
    import report_roll_plugout as plug
    import report_roll_return as ret
    reports=[older,younger]
    for module,out in [(plug,'plugout_regression'),(ret,'return_regression')]:
        previous=module.STEM,module.PREFIX
        try:module.STEM,module.PREFIX=STEM,PREFIX;reports.append(module.main(outdir+'/'+out))
        finally:module.STEM,module.PREFIX=previous
    from report_roll_intro import main as intro
    from report_roll_pet import main as pet
    from report_roll_fortune import main as fortune
    from report_attack_caption_runtime import main as caption
    reports.extend([intro(STEM,PREFIX+'roll-',outdir+'/greeting_regression'),pet(STEM,PREFIX,outdir+'/pet_regression'),fortune(STEM,PREFIX,outdir,('sample-97','sample-211','sample-389')),caption(STEM,PREFIX+'rockman-',outdir+'/rockman_regression'),caption(STEM,PREFIX+'roll-',outdir+'/roll_caption',roll=True)])
    expected=read(ROOT/f'poc/output/{STEM}.json')['output_sha256']
    if not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==expected for r in reports):raise ValueError('cumulative runtime reports')
    return reports

if __name__=='__main__':main()
