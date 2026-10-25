"""Fix composed observer dump name; preserve prior failed probe and ROM."""
import json
from pathlib import Path
import capture_chip_folder_lifetime as base
from build_visibility_poc import sha


def main():
    old='local function dumpLibraryChipSurvey(name)'
    if base.survey.PROBE.count(old)!=1:
        raise ValueError('survey dump definition anchor drift')
    base.survey.PROBE=base.survey.PROBE.replace(old,'local function dumpChipSurvey(name)')
    rc=base.main()
    out=Path(base.consumer.base.library.fixed.value('--out'))
    e=json.loads((out/'folder_lifetime_environment.json').read_text())
    e['adapter_sha256']=sha(Path(__file__).read_bytes())
    (out/'folder_lifetime_v2_environment.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
    return rc


if __name__=='__main__':
    raise SystemExit(main())
