"""Compose native folder row observer with per-frame bank/copy/write inventory."""
import json
from pathlib import Path
import capture_chip_other_consumer_v2 as consumer
import capture_chip_library_probe as survey
from build_visibility_poc import sha


def main():
    fixed=consumer.base.library.fixed
    code=survey.PROBE
    if code.count('local libraryActive=false')!=1:
        raise ValueError('lifetime start anchor drift')
    # Observe before folder initialization, not only after the first name row.
    code=code.replace('local libraryActive=false','local libraryActive=true')
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpChipSurvey(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpChipSurvey('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:
            raise ValueError('lifetime capture anchor drift')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=consumer.main()
    out=Path(fixed.value('--out'))
    d=json.loads((out/'final_chip_survey.json').read_text())
    (out/'folder_lifetime_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'survey_tool_sha256':sha(Path(survey.__file__).read_bytes()),'checked_frames':d['checked_frames'],
        'scope':'read-only all-route active BG-map/copy/write inventory at 06008000..06008FFF; NOT free-space adoption',
        'maps_or_writes_are_observations_only':True},indent=2),encoding='utf-8')
    print('folder lifetime frames:',d['checked_frames'],'writes:',d['candidate_write_count'],'map histogram:',len(d['candidate_map_tile_histogram']))
    return rc


if __name__=='__main__':
    raise SystemExit(main())
