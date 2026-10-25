"""Undernet renderer-only alias; no progress/target acquisition forcing."""
import json,sys
from pathlib import Path
import capture_roll_pet_license as base
from build_visibility_poc import ROOT,sha
from archive_scripts import script_spans

def main():
    a=sys.argv;out=Path(a[a.index('--out')+1]);script=int(a[a.index('--talk-script')+1])
    if script!=27:raise ValueError('unregistered undernet diagnostic')
    source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
    if not script_spans(source[0x664E28:0x664E28+2158],255)[27].startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')):raise ValueError('undernet source entry commands')
    base.SCRIPTS=[27];rc=base.main();p=out/'license_environment.json';e=json.loads(p.read_text());e.update(wrapper='capture_roll_pet_undernet.py',wrapper_sha256=sha(Path(__file__).read_bytes()),scope='DIAGNOSTIC PET alias0 to27 renderer only; not undernet progression or target encounter.');p.write_text(json.dumps(e,indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
