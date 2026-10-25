"""Own exact-ROM normal chain, followed by native schedule deletion."""
import run_gutsman_calendar_management as base
STEM='exe45_ko_development_gutsman_calendar_schedule_delete_v1'
PREFIX='gutsman-calendar-schedule-delete-v1-'
OUTDIR='gutsman_calendar_schedule_delete_v1'
ROUTES=[
('schedule-delete-selector','yes-accept','none:1:7,down:2:90,none:1:7,down:2:90,a:2:90'),
('schedule-delete-list','schedule-delete-selector','none:1:7,a:2:90'),
('schedule-delete-first','schedule-delete-list','none:1:7,a:2:90'),
('schedule-delete-confirm','schedule-delete-first','none:1:7,a:2:90'),
('schedule-delete-no-focus','schedule-delete-confirm','none:1:7,right:2:90'),
('schedule-delete-no-accept','schedule-delete-no-focus','none:1:7,a:2:90'),
('schedule-delete-b-cancel','schedule-delete-confirm','none:1:7,b:2:90'),
('schedule-delete-yes-accept','schedule-delete-confirm','none:1:7,a:2:90'),
]
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    for name,parent,actions in ROUTES:base.capture(name,parent,actions)
if __name__=='__main__':main()
