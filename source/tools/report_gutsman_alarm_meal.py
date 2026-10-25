"""Six finite alarm pages, combined native nickname and retained regressions."""
from report_gutsman_alarm_followup import main
from run_gutsman_alarm_meal import STEM,PREFIX,OUTDIR
if __name__=='__main__':main(stem=STEM,prefix=PREFIX,outdir=OUTDIR,expected_counts=(2283,57,675),oldstem='exe45_ko_development_gutsman_alarm_followup_v1',unit_asset='gutsman_alarm_meal_ko.json',inventory_outdir='full_scope_gutsman_alarm_meal_v1',new_literal_units=1,meal=True)
