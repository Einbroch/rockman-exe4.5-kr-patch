"""Explicit wrapper for unchanged PET alias machinery; renderer evidence only."""
import json,sys
from pathlib import Path
import capture_roll_pet_license as base
from build_visibility_poc import sha

def main():
    a=sys.argv;out=Path(a[a.index('--out')+1]);script=int(a[a.index('--talk-script')+1])
    if script not in [17,31]:raise ValueError('unregistered incident diagnostic')
    base.SCRIPTS=[17,31];rc=base.main();p=out/'license_environment.json';e=json.loads(p.read_text());e.update(wrapper='capture_roll_pet_incident.py',wrapper_sha256=sha(Path(__file__).read_bytes()),scope='DIAGNOSTIC PET alias0 to17/31 renderer only; not incident progress or native branch selection.');p.write_text(json.dumps(e,indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
