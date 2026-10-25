"""Read-only ownership survey for prospective 56 uint16 cache tags."""
import json
from pathlib import Path
import capture_chip_wordcopy_qa as word
import capture_chip_library_probe as survey
from build_visibility_poc import sha


def main():
    fixed = word.base.library.fixed
    # Reuse complete enabled-mode-0 BG map enumeration and write counters.
    # The candidate still copies every cell; this tool allocates no RAM/VRAM.
    probe = survey.PROBE
    probe = "local function ownerFail(s) write('ownership_failed.txt',s);emu.stop(1);error(s) end\n" + probe.replace('error(', 'ownerFail(')
    fixed.PROBE += probe
    for name, dump in [('capture(name)', 'name'), ('finish()', "'final'")]:
        old = 'local function ' + name + '\n'
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError('ownership capture anchor drift')
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, old + ' dumpLibraryChipSurvey(' + dump + ')\n')
    rc = word.main()
    out = Path(fixed.value('--out'))
    data = json.loads((out / 'final_chip_survey.json').read_text(encoding='utf-8'))
    valid = not (out / 'ownership_failed.txt').exists() and data['checked_frames'] > 0 and data['control_map_write_count'] > 0 and data['candidate_write_count'] > 0
    (out / 'cache_ownership_environment.json').write_text(json.dumps({
        'tool_sha256': sha(Path(__file__).read_bytes()), 'survey_tool_sha256': sha(Path(survey.__file__).read_bytes()),
        'proposed_tag_start': 0x06008E40, 'proposed_tag_bytes': 112,
        'scope': 'normal input observation only; no cache tags written or adopted; frame-end map samples do not exclude transient consumers',
        'positive_controls': valid}, indent=2), encoding='utf-8')
    if not valid:
        r = json.loads((out / 'result.json').read_text())
        r['complete'] = False
        (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
