"""Exact two-question extension; keep prior nine draft identities intact."""
from report_roll_pet import ROOT,read
from run_roll_calendar_content import STEM,PREFIX,OUTDIR
UNIT_COUNT=11
def main():
    old=read(ROOT/'translations/roll_calendar_dialogue_ko.json');new=read(ROOT/'translations/roll_calendar_content_ko.json');d={u['id']:u for u in new['units']}
    if len(d)!=11 or any(d[u['id']]!=u for u in old['units']) or set(d)-{u['id'] for u in old['units']}!={'65F11C:22:0','65F11C:23:0'}:raise ValueError('prior draft identity/extension scope')
    import report_roll_calendar_dialogue as base
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.ASSET='roll_calendar_content_ko.json';base.UNIT_COUNT=UNIT_COUNT
    base.SAMPLES=[('calendar',4,1),('calendar',5,2),('calendar',6,20),('time',5,21),('time',6,22),('promise',3,23),('meal',5,24)]
    result=base.main();base.regressions();return result
if __name__=='__main__':main()
