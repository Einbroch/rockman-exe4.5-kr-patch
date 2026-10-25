"""Own cold/save/PET route plus possessions and adjacent calendar samples."""
import run_gutsman_pet as base
import run_gutsman_calendar_management as management
STEM='exe45_ko_development_gutsman_calendar_inventory_v1'
PREFIX='gutsman-calendar-inventory-v1-'
OUTDIR='gutsman_calendar_inventory_v1'
ROUTES=[
('inventory','select-gutsman','none:1:7,left:2:90'),
('inventory-accept','inventory','none:1:7,a:2:90'),
('inventory-cancel','inventory','none:1:7,b:2:90'),
('inventory-reenter','inventory-cancel','none:1:7,left:2:90'),
('calendar','select-gutsman','none:1:7,right:2:90,none:1:90,a:2:90,a:2:90,a:2:90'),
('time-stable','calendar','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90,a:2:180'),
('confirmation','time-stable','none:1:7,down:4:90,none:1:10,down:4:90,a:2:90'),
('yes-accept','confirmation','none:1:7,a:2:90'),
('delete-selector','yes-accept','none:1:7,down:2:90,none:1:7,down:2:90,a:2:90'),
('delete-list','delete-selector','none:1:7,a:2:90'),
('delete-first','delete-list','none:1:7,a:2:90')]
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.main()
    management.STEM=STEM;management.PREFIX=PREFIX
    for name,parent,actions in ROUTES:management.capture(name,parent,actions)
if __name__=='__main__':main()
