"""Current relocated Guts talk root, one-shot read-only PET alarm aliases."""
import capture_gutsman_schedule_alarm as base
import json,sys
from pathlib import Path
from build_visibility_poc import sha
def main():
    rc=base.main(scripts=(1,2,4,6),relocated_talk=True)
    out=Path(sys.argv[sys.argv.index('--out')+1]);p=out/'alarm_environment.json';env=json.loads(p.read_text())
    env['wrapper_sha256']=sha(Path(__file__).read_bytes());p.write_text(json.dumps(env,indent=2),encoding='utf8');return rc
if __name__=='__main__':raise SystemExit(main())
